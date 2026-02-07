import os
import shutil
from pathlib import Path
from src.service.collector.api_client import BallchasingClient
from src.service.collector.parse import parse_game_list
from src.service.collector.id_request_api import download_replays_from_list
from src.service.collector.get_tmp_file import list_files_to_import
from src.service.collector.db_importer import add_single_match 

# CONFIG
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DUMP_DIR = BASE_DIR / "src" / "database" / "temp" / "file-dump-tmp"

def run_full_update(pseudo=None, player_id=None):
    """Workflow complet basé sur le diagramme de gestion d'appel API."""
    
    print("🚀 Démarrage de la mise à jour...")
    client = BallchasingClient()
    
    # 1. Recherche des games (Created after 2024/01/01, Count=200)
    # print("📡 Étape 1 : Recherche des matchs sur l'API...")
    print("--- Test API Client ---")
    user_input = input("Pseudo (laisser vide pour ID) : ")
    id_input = None
    if not user_input:
        id_input = input("ID Joueur (ex: steam:76561198...) : ")

    raw_list = client.search_games(player_name=user_input, player_id=player_id)
    
    if not raw_list:
        print("❌ Aucune game trouvée ou erreur API.")
        return

    # 2. Parsing (Extraction ID et Date vers id-date-list-temp)
    print("Step 2 : Parsing match list")
    parse_game_list()

    # 3. Download (Get replay by ID vers file-dump-tmp)
    print("Step 3 : Downloading files")
    download_replays_from_list()

    # 4. Importation (Sur tous les fichiers du dump)
    print("Step 4 : Data import")
    files_to_import = list_files_to_import()
    
    if not files_to_import:
        print("⚠️ Aucun fichier à importer.")
    else:
        for file_path in files_to_import:
            add_single_match(file_path)

    # 5. Nettoyage (Delete all files in file-dump-tmp)
    print("Step 5 : Cleaning")
    if DUMP_DIR.exists():
        shutil.rmtree(DUMP_DIR)
        os.makedirs(DUMP_DIR, exist_ok=True)
    
    print("✨ Mise à jour terminée avec succès !")

if __name__ == "__main__":
    # Possibilité de passer le pseudo en dur pour le test
    #
    run_full_update()