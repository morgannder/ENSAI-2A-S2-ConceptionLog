import json
import os
from pathlib import Path
import shutil
import time

from src.dao.players_dao import PlayerDAO
from src.service.collector.api_client import BallchasingClient
from src.service.collector.db_importer import add_single_match
from src.service.collector.get_tmp_file import list_files_to_import
from src.service.collector.id_request_api import download_replays_from_list
from src.service.collector.parse import parse_game_list


# CONFIG
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DUMP_DIR = BASE_DIR / "src" / "database" / "temp" / "file-dump-tmp"


def run_full_update(
    user_input=None, player_id=None, num_input=1, date_max="2024-01-01T00:00:00Z"
):
    """
    Exécute la mise à jour complète en tant que Générateur (Yield)
    Renvoie uniquement des données JSON brutes pour le frontend.
    """
    client = BallchasingClient()
    players_dao = PlayerDAO()

    yield json.dumps({"step": 1, "total_steps": 4, "status": "searching"}) + "\n"

    raw_list_path = client.search_games(
        player_name=user_input,
        player_id=player_id,
        count=num_input,
        created_after=date_max,
    )

    if not raw_list_path:
        yield (
            json.dumps(
                {"status": "error", "message": "Aucun résultat trouvé sur Ballchasing."}
            )
            + "\n"
        )
        return

    try:
        with open(raw_list_path, encoding="utf-8") as f:
            raw_data = json.load(f)
    except Exception as e:
        yield (
            json.dumps({"status": "error", "message": f"Erreur de lecture JSON: {e}"})
            + "\n"
        )
        return

    display_name = user_input
    matches = raw_data.get("list", [])
    latest_date = matches[0].get("date") if matches else None

    # Recherche du nom dans la base si on n'a que l'ID
    if player_id is not None:
        clean_id = player_id.split(":")[-1] if ":" in player_id else player_id
        db_player = players_dao.get_player_by_parameter("platform_user_id", clean_id)
        if db_player:
            display_name = db_player.name

    yield json.dumps({"step": 2, "total_steps": 4, "status": "parsing"}) + "\n"
    parse_infos = parse_game_list()

    yield json.dumps({"step": 3, "total_steps": 4, "status": "downloading"}) + "\n"
    dl_infos = download_replays_from_list()

    yield json.dumps({"step": 4, "total_steps": 4, "status": "importing"}) + "\n"
    files_to_import = list_files_to_import()

    if not files_to_import:
        yield (
            json.dumps({"status": "info", "message": "Aucun nouveau match à importer."})
            + "\n"
        )
    else:
        total_files = len(files_to_import)
        start_time = time.time()

        for index, file_path in enumerate(files_to_import):
            add_single_match(file_path)
            current_count = index + 1

            # Notification toutes les 5 parties ou à la toute fin
            if current_count % 5 == 0 or current_count == total_files:
                elapsed_time = time.time() - start_time
                avg_time_per_file = elapsed_time / current_count
                files_left = total_files - current_count
                eta_seconds = round(files_left * avg_time_per_file, 1)
                percentage = round((current_count / total_files) * 100, 1)

                # Payload ultra-propre pour React
                yield (
                    json.dumps(
                        {
                            "status": "progress",
                            "current": current_count,
                            "total": total_files,
                            "percentage": percentage,
                            "eta_seconds": eta_seconds,
                        }
                    )
                    + "\n"
                )

    # Nettoyage des fichiers temporaires
    if DUMP_DIR.exists():
        shutil.rmtree(DUMP_DIR)
        os.makedirs(DUMP_DIR, exist_ok=True)

    Path("src/database/temp/id-date-list-temp.json").write_text("[]")
    Path("src/database/temp/raw_game_list.json").write_text("[]")

    stats = parse_infos.get("data", {}) if isinstance(parse_infos, dict) else {}

    # Message final de résumé complet
    yield (
        json.dumps(
            {
                "status": "completed",
                "player_name": display_name,
                "latest_match_date": latest_date,
                "dl_status": dl_infos.get("status")
                if isinstance(dl_infos, dict)
                else "unknown",
                "details": stats,
            }
        )
        + "\n"
    )
