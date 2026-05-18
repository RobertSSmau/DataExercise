# Documento Tecnico — FSD Esame 2024
**Candidato:** {COGNOME} {NOME} — Reg. {NUMERO_REGISTRO}

---

## 1. Analisi del problema

La prova richiede di:
1. Ingerire 3 dataset pubblici da datiopen.it relativi al mercato del lavoro italiano per regione.
2. Normalizzare i dati mancanti tramite interpolazione temporale.
3. Calcolare 5 serie statistiche aggregate per macro-area geografica e a livello nazionale.
4. Esporre tutti i dati via API HTTP REST con filtro temporale `da_anno` / `a_anno`.
5. (Facoltativo) Visualizzare una serie via interfaccia web.

---

## 2. Stack tecnologico e motivazioni

### Linguaggio: Python 3.11
Scelto tra i linguaggi del corso. Ha un ecosistema maturo per data-wrangling (pandas), web API (FastAPI) e ORM (SQLAlchemy). Rende il codice leggibile e conciso.

### Framework web: FastAPI + Uvicorn
- **FastAPI** genera automaticamente la documentazione Swagger (`/docs`) — utile sia per il test della prova che per il valutatore. Valida i parametri di input tramite Pydantic, riducendo il boilerplate di validazione.
- **Uvicorn** è il server ASGI consigliato da FastAPI, ad alte prestazioni.
- La comunicazione backend/frontend avviene via HTTP come richiesto dalla commessa.

### Database: SQLite + SQLAlchemy
- **SQLite** è un file singolo (`data/esame.db`): non richiede installazione, configurazione di servizi o credenziali. Il valutatore apre la cartella ed esegue subito.
- **SQLAlchemy** (ORM) disaccoppia il codice dal driver; passare a PostgreSQL/MySQL richiederebbe solo modificare `db_url` in `config.py` senza riscrivere la logica.
- Per i volumi di dati in esame (20 regioni × ~20 anni × 3 dataset) SQLite è più che sufficiente.

### Manipolazione dati: pandas
Auto-rileva il separatore CSV (`;` o `,`), gestisce encoding e conversione tipi, riducendo il codice di parsing.

---

## 3. Struttura del database

| Tabella | Descrizione |
|---|---|
| `regioni` | Lookup statica: 20 regioni italiane con il loro nome canonico e macro-area |
| `partecipazione_lavoro` | Dati grezzi dataset 1 (regione, anno, valore, interpolato) |
| `sopravvivenza_imprese` | Dati grezzi dataset 2 |
| `incidenza_ricerca` | Dati grezzi dataset 3 |
| `serie_calcolate` | Le 5 serie aggregate (tipo_serie, area nullable, anno, valore) |

La colonna `interpolato BOOLEAN` nelle tabelle grezze traccia i record aggiunti dalla fase di normalizzazione per trasparenza verso il consumatore dell'API.

Le 5 serie calcolate condividono un'unica tabella `serie_calcolate` distinta dal campo `tipo_serie` (`PART_AREA`, `PART_NAZ`, `RIC_AREA`, `SOPR_NAZ`, `SOPR_AREA`). Questa scelta riduce il numero di tabelle e semplifica le query.

---

## 4. Aggregazione geografica

Definita in `app/constants.py` secondo la tabella della commessa:
- **Nord-ovest:** Valle d'Aosta, Piemonte, Liguria, Lombardia
- **Nord-est:** Trentino-Alto Adige, Veneto, Friuli-Venezia Giulia, Emilia-Romagna
- **Centro:** Toscana, Umbria, Marche, Lazio, Abruzzo
- **Sud:** Molise, Campania, Puglia, Basilicata, Calabria
- **Isole:** Sicilia, Sardegna

Sono stati mappati anche alias comuni dei nomi regionali che datiopen.it usa in modo variabile tra i dataset (es. "Valle d'Aosta/Vallée d'Aoste", "Trentino Alto Adige" senza trattino, "Emilia Romagna").

---

## 5. Interpolazione dei dati mancanti

Implementata in `app/services/normalizer.py`. Algoritmo:
- Per ogni regione si costruisce un dizionario `{anno: valore}` con i dati noti.
- Tra ogni coppia di anni noti consecutivi `(a0, a1)` con gap > 1, vengono aggiunti gli anni intermedi con valore interpolato linearmente: `v(k) = v0 + (v1-v0)/gap * k`.
- Gli estremi del range temporale non vengono estrapolati (non si inventa dato fuori dal range osservato).
- I record interpolati vengono salvati nella stessa tabella con `interpolato=True`.

Esempio (da commessa): regione con dato 2001=X e 2004=Y; mancano 2002 e 2003. Passo = (Y-X)/3. Inserisco 2002=X+passo, 2003=X+2*passo.

---

## 6. Calcolo delle 5 serie

Implementato in `app/services/calculator.py`.

**Assunzione esplicita (nota metodologica):** non avendo le quantità di riferimento per le percentuali, come indicato nella commessa, si usa **media aritmetica semplice** tra regioni, non ponderata per popolazione o PIL.

| # | Serie | Tipo | Calcolo |
|---|---|---|---|
| 1 | Partecipazione lavoro per area | PART_AREA | media regioni dell'area, per anno |
| 2 | Partecipazione lavoro nazionale | PART_NAZ | media di tutte le regioni, per anno |
| 3 | Incidenza spesa R&S per area | RIC_AREA | media regioni dell'area, per anno |
| 4 | Sopravvivenza imprese nazionale | SOPR_NAZ | media di tutte le regioni, per anno |
| 5 | Sopravvivenza imprese per area | SOPR_AREA | media regioni dell'area, per anno |

---

## 7. API REST

Tutti gli endpoint accettano i parametri `da_anno` e `a_anno` come query string obbligatori. La validazione `a_anno >= da_anno` è implementata su tutti i router con risposta `HTTP 400` in caso di violazione.

Documentazione interattiva disponibile su `/docs` (Swagger UI auto-generata da FastAPI).

| Endpoint | Descrizione |
|---|---|
| `GET /api/partecipazione?da_anno=X&a_anno=Y` | Dati grezzi partecipazione |
| `GET /api/sopravvivenza?da_anno=X&a_anno=Y` | Dati grezzi sopravvivenza |
| `GET /api/ricerca?da_anno=X&a_anno=Y` | Dati grezzi ricerca R&S |
| `GET /api/serie/partecipazione/aree?...` | Serie 1 |
| `GET /api/serie/partecipazione/nazionale?...` | Serie 2 |
| `GET /api/serie/ricerca/aree?...` | Serie 3 |
| `GET /api/serie/sopravvivenza/nazionale?...` | Serie 4 |
| `GET /api/serie/sopravvivenza/aree?...` | Serie 5 |
| `GET /` | Pagina web con grafico Chart.js (facoltativo) |

---

## 8. Interfaccia web (facoltativo)

Pagina HTML statica (`app/static/index.html`) servita direttamente da FastAPI. Usa Chart.js (CDN) per il rendering dei grafici. Consente di selezionare qualsiasi delle 5 serie calcolate, impostare il range temporale, e visualizza il grafico a linee aggiornato via fetch all'API. La comunicazione frontend↔backend avviene via HTTP come richiesto dalla commessa.

---

## 9. Scelte non ovvie e assunzioni

- **Righe CSV scartate:** righe con nome regione non riconoscibile (es. aggregati "Italia") vengono scartate in import per non inquinare i calcoli medi. Idem per righe con valore non parsabile.
- **Idempotenza dell'import:** ogni riesecuzione dello script di import cancella e reinserisce i dati grezzi; le serie calcolate vengono ricalcolate ex-novo. Questo rende la pipeline rieseguibile in sicurezza.
- **Separatore CSV:** datiopen.it usa `;` su alcuni dataset e `,` su altri. Il parser prova prima `;`, poi rileva automaticamente il separatore con `pandas`.
- **Non si controlla l'univocità regione-anno in import:** il vincolo `UNIQUE(regione_id, anno)` è garantito a livello di DB (SQLAlchemy UniqueConstraint). Se il CSV contiene duplicati, SQLAlchemy solleva un'eccezione che viene propagata.

---

## 10. Avvio

```bash
pip install -r requirements.txt
python scripts/1_import.py      # scarica e importa i 3 dataset
python scripts/2_normalize.py   # interpola dati mancanti
python scripts/3_calculate.py   # calcola le 5 serie
python run.py                   # API su http://127.0.0.1:8000
```

---

## 11. Limiti noti / sviluppi futuri

- La media non è ponderata; in produzione si userebbe la popolazione attiva regionale come peso.
- L'estrapolazione fuori range non è implementata per evitare dati non fondati su osservazioni.
- Autenticazione non richiesta dalla commessa: non implementata.
- Il backend è sincrono (Uvicorn sync worker); per carichi elevati si userebbe FastAPI async + asyncpg su PostgreSQL.
