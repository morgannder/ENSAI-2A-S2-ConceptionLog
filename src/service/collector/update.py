import os
from pathlib import Path
import shutil

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
    Run update based on user playername or user id
    """

    client = BallchasingClient()
    if user_input is None and player_id is None:
        num_input = input("How many matches ? (Max 200) : ")
        user_input = input("Pseudo (let empty for ID) : ").strip()
        user_input = f'"{user_input}"'
        player_id = None
        if not user_input:
            player_id = input("player ID (ex: steam:76561198...) : ")

    raw_list = client.search_games(
        player_name=user_input,
        player_id=player_id,
        count=num_input,
        created_after=date_max,
    )

    if not raw_list:
        return None

    print("Parsing match list")
    parse_game_list()
    print("Downloading files")
    download_replays_from_list()
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
    return True


if __name__ == "__main__":
    run_full_update()
