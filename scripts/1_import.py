"""Script 1: importa i 3 dataset pubblici da datiopen.it nel database."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.importer import run_import

if __name__ == "__main__":
    print("=== Import dati ===")
    run_import()
    print("Import completato.")
