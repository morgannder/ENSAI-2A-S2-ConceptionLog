from pathlib import Path


# CONFIG
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DUMP_DIR = BASE_DIR / "src" / "database" / "temp" / "file-dump-tmp"


def list_files_to_import():
    """
    établi la liste des fichiers dans file-dump-tmp pour l'importation en DB
    """

    if not DUMP_DIR.exists():
        print(f"Directory {DUMP_DIR} does not exist.")
        return []

    files = list(DUMP_DIR.glob("*.json"))
    return [str(f) for f in files]
