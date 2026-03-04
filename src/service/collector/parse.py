import hashlib
import json
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


# CONFIG
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
TEMP_DIR = BASE_DIR / "src" / "database" / "temp"
INPUT_FILE = TEMP_DIR / "raw_game_list.json"
OUTPUT_FILE = TEMP_DIR / "id-date-list-temp.json"
DB_PATH = BASE_DIR / "src" / "database" / "rocket_league.db"


engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)


def generate_hash_from_list_item(item):
    """
    Génère un ID unique à partir des joueurs, du temps de la partie et du score.
    Parameters
    ----------
    data : dict
        dictionnaire contenant toute une partie

    Returns
    -------
    str
        Hash (qui sera l'ID) généré à partir des méta données du match
    """
    p_ids = []
    for side in ["blue", "orange"]:
        for p in item.get(side, {}).get("players", []):
            uid = p.get("id", {}).get("id")
            if uid:
                p_ids.append(str(uid))

    p_ids.sort()

    blue_score = item.get("blue", {}).get("goals", 0)
    orange_score = item.get("orange", {}).get("goals", 0)
    duration = item.get("duration", 0)

    raw_str = f"{''.join(p_ids)}_{duration}_{blue_score}_{orange_score}"
    return hashlib.sha256(raw_str.encode()).hexdigest()


def parse_game_list():
    """
    Extrait les id es matchs dans les fichiers présents dans raw_game_list.json
    afin de pouvoir les télécharger par la suite
    """

    if not INPUT_FILE.exists():
        print("File is missing.")
        return

    with open(INPUT_FILE, encoding="utf-8") as f:
        data = json.load(f)

    replays = data.get("list", [])
    if not replays:
        print("Empty list.")
        return

    session = Session()
    matches_to_download = []
    skipped_count = 0

    for replay in replays:
        match_hash = generate_hash_from_list_item(replay)
        exists = session.execute(
            text("SELECT 1 FROM matches WHERE id = :id"), {"id": match_hash}
        ).fetchone()

        if exists:
            skipped_count += 1
        else:
            matches_to_download.append({"id": replay.get("id")})

    session.close()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(matches_to_download, f, indent=4)

    return {
        "data": {
            "total_analysed": len(replays),
            "already_in_db": skipped_count,
            "new_matches_downloaded": len(matches_to_download),
        }
    }
