## Mercato del lavoro IT

Applicazione per la raccolta e analisi dei dati sul mercato del lavoro in Italia.
Scarica 3 dataset pubblici da datiopen.it, normalizza i dati mancanti con interpolazione lineare e calcola 5 serie statistiche aggregate per area geografica. Tutto viene esposto tramite API REST.

## Come si avvia

Prima di tutto crea e attiva un ambiente virtuale:

```
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Poi esegui i 3 script di pipeline nell'ordine, ognuno dipende dal precedente:

```
python scripts/1_import.py
python scripts/2_normalize.py
python scripts/3_calculate.py
```

Infine avvia il server:

```
python run.py
```

L'API è disponibile su http://127.0.0.1:8000 e la documentazione Swagger su http://127.0.0.1:8000/docs.

## Note

Il database è un file SQLite in data/esame.db, non serve configurare niente. Se il download automatico da datiopen.it non funziona, scarica manualmente i CSV e salvali in data/ come partecipazione.csv, sopravvivenza.csv e ricerca.csv.