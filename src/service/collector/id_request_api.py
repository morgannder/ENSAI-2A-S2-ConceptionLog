import os
import json
import time
from pathlib import Path
from src.service.collector.api_client import BallchasingClient

# CONFIG
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
TEMP_DIR = BASE_DIR / "src" / "database" / "temp"
INPUT_LIST = TEMP_DIR / "id-date-list-temp.json"
DUMP_DIR = TEMP_DIR / "file-dump-tmp"

def download_replays_from_list():
    """
    Parcourt la liste des IDs extraits et télécharge chaque replay JSON.
    Correspond à l'étape 'id-request-api.py' du schéma.
    """
    if not INPUT_LIST.exists():
        print(f"❌ Erreur : Le fichier {INPUT_LIST} est introuvable. Lancez parser.py d'abord.")
        return

    # Création du dossier de destination s'il n'existe pas 
    os.makedirs(DUMP_DIR, exist_ok=True)

    # Lecture de la liste des IDs et dates [cite: 11]
    with open(INPUT_LIST, 'r', encoding='utf-8') as f:
        matches_to_download = json.load(f)

    if not matches_to_download:
        print("⚠️ La liste des matchs est vide.")
        return

    client = BallchasingClient()
    print(f"📥 Début du téléchargement de {len(matches_to_download)} replays...")

    count_success = 0
    for match in matches_to_download:
        match_id = match.get("id")
        if not match_id:
            continue

        # Téléchargement via le client API vers le dossier de dump 
        success = client.download_replay(match_id)
        
        if success:
            count_success += 1
        elif success is None:
            # Le fichier existait déjà, on ne le compte pas comme un nouvel import
            pass
        
        # Pause de sécurité pour respecter le Rate Limit de l'API
        time.sleep(0.55)

    print(f"✅ Terminé : {count_success} nouveaux replays téléchargés dans {DUMP_DIR}.")
    return DUMP_DIR

if __name__ == "__main__":
    download_replays_from_list()