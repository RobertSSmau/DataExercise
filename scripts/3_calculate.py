"""Script 3: calcola le 5 serie statistiche richieste dalla commessa."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.calculator import run_calculate

if __name__ == "__main__":
    print("=== Calcolo serie ===")
    run_calculate()
    print("Calcolo completato.")
