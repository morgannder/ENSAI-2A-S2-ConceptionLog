import json
import hashlib
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# --- CONFIGURATION ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
TEMP_DIR = BASE_DIR / "src" / "database" / "temp"
INPUT_FILE = TEMP_DIR / "raw_game_list.json"
OUTPUT_FILE = TEMP_DIR / "id-date-list-temp.json"
DB_PATH = BASE_DIR / "src" / "database" / "rocket_league.db"

# Connexion DB pour vérification
engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)

def generate_hash_from_list_item(item):
    """
    Génère le hash à partir d'un item de la LISTE brute (structure différente du replay complet).
    """
    p_ids = []
    # Dans la liste, les joueurs sont directement sous 'blue'/'orange', pas de sous-clé 'stats'
    for side in ["blue", "orange"]:
        for p in item.get(side, {}).get("players", []):
            # Structure liste: p['id']['id'] existe bien
            uid = p.get("id", {}).get("id")
            if uid:
                p_ids.append(str(uid))
    p_ids.sort()

    # Dans la liste, les goals sont directement sous 'blue.goals', pas 'blue.stats.core.goals'
    blue_score = item.get("blue", {}).get("goals", 0)
    orange_score = item.get("orange", {}).get("goals", 0)
    duration = item.get("duration", 0)

    raw_str = f"{''.join(p_ids)}_{duration}_{blue_score}_{orange_score}"
    return hashlib.sha256(raw_str.encode()).hexdigest()

def parse_game_list():
    print(f"📖 Analyse intelligente de : {INPUT_FILE}")

    if not INPUT_FILE.exists():
        print(f"❌ Fichier introuvable. Lancez api_client.py avant.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    replays = data.get('list', [])
    if not replays:
        print("⚠️ Liste vide.")
        return

    session = Session()
    matches_to_download = []
    skipped_count = 0

    print(f"🔎 Vérification de {len(replays)} matchs contre la base de données...")

    for replay in replays:
        # 1. On génère le hash avec les données partielles de la liste
        match_hash = generate_hash_from_list_item(replay)

        # 2. On vérifie si ce hash existe déjà en DB
        exists = session.execute(
            text("SELECT 1 FROM matches WHERE id = :id"), 
            {"id": match_hash}
        ).fetchone()

        if exists:
            skipped_count += 1
        else:
            # 3. S'il n'existe pas, on l'ajoute à la liste de téléchargement
            # On garde l'ID Ballchasing pour le téléchargement
            matches_to_download.append({
                "id": replay.get("id"),
                "date": replay.get("date")
            })

    session.close()

    # Sauvegarde de la liste FILTRÉE
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(matches_to_download, f, indent=4)

    print(f"✅ Analyse terminée.")
    print(f"   - Total analysé : {len(replays)}")
    print(f"   - Déjà en base (ignorés) : {skipped_count}")
    print(f"   - Nouveaux à télécharger : {len(matches_to_download)}")
    print(f"💾 Liste de téléchargement générée : {OUTPUT_FILE}")

if __name__ == "__main__":
    parse_game_list()