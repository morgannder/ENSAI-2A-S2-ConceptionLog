import json
from pathlib import Path
import time

from src.service.collector.api_client import BallchasingClient


# CONFIG
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
TEMP_DIR = BASE_DIR / "src" / "database" / "temp"
INPUT_LIST = TEMP_DIR / "id-date-list-temp.json"
DUMP_DIR = TEMP_DIR / "file-dump-tmp"


def download_replays_from_list():
    """
    Run extracted ID list and download each JSON file.
    """

    if not INPUT_LIST.exists():
        print(f"Error : file {INPUT_LIST} is missing.")
        return

    with open(INPUT_LIST, encoding="utf-8") as f:
        matches_to_download = json.load(f)

    if not matches_to_download:
        print("Match list is empty.")
        return

    client = BallchasingClient()
    print(f"Starting download {len(matches_to_download)} replays")

    count_success = 0
    for match in matches_to_download:
        match_id = match.get("id")
        if not match_id:
            continue

        success = client.download_replay(match_id)
        if success:
            count_success += 1

        time.sleep(0.55)

    print(f"Task finished ! Downloaded {count_success} files.")
    return DUMP_DIR


if __name__ == "__main__":
    download_replays_from_list()
