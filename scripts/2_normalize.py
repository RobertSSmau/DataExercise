"""Script 2: normalizza i dati mancanti con interpolazione lineare temporale."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.normalizer import run_normalize

if __name__ == "__main__":
    print("=== Normalizzazione dati ===")
    run_normalize()
    print("Normalizzazione completata.")
