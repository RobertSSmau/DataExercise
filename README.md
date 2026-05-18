Mercato del lavoro IT

## Avvio rapido

```bash
# 1. Crea e attiva venv
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
# source .venv/bin/activate    # Linux/Mac

# 2. Installa dipendenze
pip install -r requirements.txt

# 3. Pipeline dati (eseguire nell'ordine)
python scripts/1_import.py      # scarica e importa i 3 dataset da datiopen.it
python scripts/2_normalize.py   # interpola dati mancanti
python scripts/3_calculate.py   # calcola le 5 serie

# 4. Avvia API
python run.py                   # http://127.0.0.1:8000
```

## Endpoint

| Metodo | URL | Parametri |
|--------|-----|-----------|
| GET | `/api/partecipazione` | `da_anno`, `a_anno` |
| GET | `/api/sopravvivenza` | `da_anno`, `a_anno` |
| GET | `/api/ricerca` | `da_anno`, `a_anno` |
| GET | `/api/serie/partecipazione/aree` | `da_anno`, `a_anno` |
| GET | `/api/serie/partecipazione/nazionale` | `da_anno`, `a_anno` |
| GET | `/api/serie/ricerca/aree` | `da_anno`, `a_anno` |
| GET | `/api/serie/sopravvivenza/nazionale` | `da_anno`, `a_anno` |
| GET | `/api/serie/sopravvivenza/aree` | `da_anno`, `a_anno` |
| GET | `/docs` | Swagger UI auto-generata |
| GET | `/` | Pagina di plotting con Chart.js |

## Note

- Il DB è `data/esame.db` (SQLite, file singolo, zero configurazione).
- Se il download da datiopen.it fallisce, scarica manualmente i 3 CSV e salvali in `data/` come `partecipazione.csv`, `sopravvivenza.csv`, `ricerca.csv`.
