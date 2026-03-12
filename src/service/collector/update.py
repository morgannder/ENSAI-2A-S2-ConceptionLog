import json
import os
from pathlib import Path
import shutil

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
    Met à jour la base à l'aide d'un pseudonyme ou dans id de joueur et de sa plateforme

    Parameters
    ----------

    player_id: Optional[str] = None
        Platform id of the user to update

    user_input: Optional[str] = None
        Exact name of user to update

    num_input:
        Number of games requested to ballchasing API

    created_after: str = "2024-01-01T00:00:00Z"
        Creation date of the replay game on Ballchasing API
        Format : ISO-8601
        Date : YYY-MM-DDTHH:MM:SSZ
        following the "T" in format -> Timezone on UTC base
        (ex : UTC+1 -> T01:00:00Z)

    Returns
    -------
    Dict :
        Informations concernant la réussite ou l'échec

    Raises
    ------
    ValueError

    """

    client = BallchasingClient()
    players_dao = PlayerDAO()

    if num_input > 200:
        num_input = 200

    raw_list = client.search_games(
        player_name=user_input,
        player_id=player_id,
        count=num_input,
        created_after=date_max,
    )

    if raw_list == 0:
        return {
            "status": "failed",
            "informations": f"0 replay founds, player does not exist on Ballchasing.com after the following date : {date_max}",
        }

    try:
        with open(raw_list, encoding="utf-8") as f:
            raw_data = json.load(f)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier JSON: {e}")
        return None

    display_name = user_input
    matches = raw_data.get("list", [])
    latest_date = matches[0].get("date") if matches else None

    if player_id is not None:
        clean_id = player_id.split(":")[-1] if ":" in player_id else player_id
        db_player = players_dao.get_player_by_parameter("platform_user_id", clean_id)
        if db_player:
            display_name = db_player.name
    print("Parsing match list")
    parse_infos = parse_game_list()
    print("Downloading files")
    dl_infos = download_replays_from_list()
    print("Data import")
    files_to_import = list_files_to_import()
    if not files_to_import:
        print("No file to import.")

    else:
        for file_path in files_to_import:
            add_single_match(file_path)

    if DUMP_DIR.exists():
        shutil.rmtree(DUMP_DIR)
        os.makedirs(DUMP_DIR, exist_ok=True)

    Path("src/database/temp/id-date-list-temp.json").write_text("[]")
    Path("src/database/temp/raw_game_list.json").write_text("[]")
    print("Update finished")
    stats = parse_infos.get("data", {}) if isinstance(parse_infos, dict) else {}
    return {
        "player_name": display_name,
        "latest_match_date": latest_date,
        "status": dl_infos.get("status") if isinstance(dl_infos, dict) else "unknown",
        "message": dl_infos.get("informations") if isinstance(dl_infos, dict) else "",
        "details": stats,
    }
