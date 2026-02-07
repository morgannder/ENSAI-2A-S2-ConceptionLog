import os
from pathlib import Path

# CONFIG
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DUMP_DIR = BASE_DIR / "src" / "database" / "temp" / "file-dump-tmp"

def list_files_to_import():
    """Liste les fichiers dans file-dump-tmp pour l'importateur[cite: 13, 14]."""
    if not DUMP_DIR.exists():
        print(f"⚠️ Le dossier {DUMP_DIR} n'existe pas.")
        return []

    # On récupère tous les fichiers .json du dossier
    files = list(DUMP_DIR.glob("*.json"))
    
    # On retourne une liste de chaînes de caractères (chemins complets)
    print([str(f) for f in files])
    return [str(f) for f in files]

if __name__ == "__main__":
    found_files = list_files_to_import()
    print(f"📂 {len(found_files)} fichiers trouvés dans le dump.")