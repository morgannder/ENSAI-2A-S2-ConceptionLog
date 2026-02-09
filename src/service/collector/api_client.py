import json
import os
from pathlib import Path
import time

from dotenv import load_dotenv
import requests


# CONFIG
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

env_path = BASE_DIR / ".env.local"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("BALLCHASING_API_KEY")
BASE_URL = "https://ballchasing.com/api/replays"

TEMP_DIR = BASE_DIR / "src" / "database" / "temp"
RAW_LIST_FILE = TEMP_DIR / "raw_game_list.json"
DUMP_DIR = TEMP_DIR / "file-dump-tmp"


class BallchasingClient:
    def __init__(self):
        if not API_KEY:
            raise ValueError(
                "Critical Error : Env var 'BALLCHASING_API_KEY' is not filed."
            )

        self.headers = {"Authorization": API_KEY}
        self.ensure_directories()

    def ensure_directories(self):
        """
        Create temp files if they dont exist
        """

        os.makedirs(TEMP_DIR, exist_ok=True)
        os.makedirs(DUMP_DIR, exist_ok=True)

    def search_games(
        self,
        count: int,
        player_name: str = None,
        player_id: str = None,
        created_after: str = "2024-01-01T00:00:00Z",
    ):
        """
        Search replays with the API and save the result.
        """

        params = {
            "created-after": created_after,
            "count": count,
            "sort-by": "replay-date",
            "sort-dir": "asc",
        }

        # Priority : ID
        if player_id:
            params["player-id"] = player_id
            print(f"ID Search: {player_id}")
        elif player_name:
            params["player-name"] = player_name
            print(f"Pseudo Search: {player_name}")
        else:
            print("Error : Please SAY SOMETHING.")
            return None

        print(f"API call to : {BASE_URL}")
        try:
            response = requests.get(BASE_URL, headers=self.headers, params=params)
            response.raise_for_status()

            data = response.json()
            count_found = len(data.get("list", []))
            print(f"Success : {count_found} replays found.")

            with open(RAW_LIST_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

            return RAW_LIST_FILE

        except requests.exceptions.RequestException as e:
            print(f"API Error : {e}")
            return None

    def download_replay(self, replay_id: str):
        """
        Download a match file (.JSON).
        """

        target_file = DUMP_DIR / f"{replay_id}.json"

        # Avoid downloading if match is already in DB
        if target_file.exists():
            return None

        url = f"{BASE_URL}/{replay_id}"
        try:
            print(f"Download : {replay_id}...")
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                with open(target_file, "w", encoding="utf-8") as f:
                    json.dump(response.json(), f, indent=4)
                return True
            elif response.status_code == 429:
                print("Rate Limit exceeded. Wait a little (2s).")
                time.sleep(2)
                return False
            else:
                print(f"Error {response.status_code} on  {replay_id}")
                return False

        except Exception as e:
            print(f"Error on :  {replay_id}: {e}")
            return False


if __name__ == "__main__":
    try:
        client = BallchasingClient()
        user_input = input("Pseudo (laisser vide pour ID) : ")
        id_input = None
        num_input = 2
        if not user_input:
            id_input = input("ID Joueur (ex: steam:76561198...) : ")

        client.search_games(player_name=user_input, player_id=id_input, count=num_input)
    except ValueError as e:
        print(e)
