# Documento tecnico — FSD Esame 2024

Candidato: {COGNOME} {NOME}, reg. {NUMERO_REGISTRO}

---

## Il problema

La prova richiede di costruire una piccola pipeline dati che scarica tre dataset pubblici dal portale datiopen.it, li carica su un database, colma i buchi temporali tramite interpolazione lineare, calcola cinque serie statistiche aggregate per area geografica e le espone tramite un'API HTTP. È prevista anche, come punto facoltativo, una pagina web che visualizza i dati.

---

## Linguaggio e tecnologie scelte

Ho scelto Python perché è il linguaggio più adatto tra quelli affrontati nel corso per questo tipo di lavoro: gestire file CSV, interrogare un database relazionale e costruire un'API web richiede librerie che in Python sono mature e ben documentate.

Per la parte web ho usato FastAPI insieme a Uvicorn. FastAPI genera automaticamente la documentazione Swagger su /docs, il che è comodo sia per testare l'API durante lo sviluppo sia per mostrarla al valutatore senza dover aprire Postman o scrivere richieste a mano. Gestisce anche la validazione dei parametri di input tramite Pydantic, quindi non devo scrivere controlli manuali per ogni campo.

Come database ho scelto SQLite perché è un file singolo che non richiede l'installazione di un server, nessuna configurazione, nessuna credenziale. Per i volumi in gioco, venti regioni per una ventina di anni su tre dataset, è più che sufficiente. Ho usato SQLAlchemy come ORM per separare la logica applicativa dal database: se si volesse passare a MySQL o PostgreSQL basterebbe cambiare la stringa di connessione in config.py senza toccare il resto del codice.

Per leggere i CSV ho usato pandas perché rileva automaticamente il separatore e gestisce l'encoding senza dover scrivere codice di parsing manuale.

---

## Struttura del database

Ho creato cinque tabelle. La tabella regioni contiene i nomi canonici delle venti regioni italiane con la rispettiva macro-area geografica; serve da riferimento per le altre tabelle. Le tabelle partecipazione_lavoro, sopravvivenza_imprese e incidenza_ricerca contengono i dati grezzi importati dai tre dataset, ognuna con le colonne regione_id, anno, valore e un booleano interpolato che indica se il record è stato aggiunto dalla fase di normalizzazione o era presente nel CSV originale. Questa colonna permette al consumatore dell'API di sapere quali dati sono osservati e quali stimati.

Le cinque serie calcolate condividono un'unica tabella serie_calcolate, distinta dal campo tipo_serie che può valere PART_AREA, PART_NAZ, RIC_AREA, SOPR_NAZ o SOPR_AREA. Le serie nazionali hanno il campo area vuoto, quelle per area lo hanno popolato. Ho preferito una tabella sola a cinque tabelle separate perché la struttura del dato è identica e le query rimangono semplici.

Su ogni coppia (regione_id, anno) nelle tabelle grezze ho messo un vincolo di unicità a livello di database. Se il CSV contiene duplicati, il database li rifiuta con un errore piuttosto che accettarli silenziosamente.

---

## Aggregazione geografica

Le regioni vengono assegnate alle macro-aree secondo la tabella della commessa: Nord-ovest comprende Valle d'Aosta, Piemonte, Liguria e Lombardia; Nord-est comprende Trentino-Alto Adige, Veneto, Friuli-Venezia Giulia ed Emilia-Romagna; Centro comprende Toscana, Umbria, Marche, Lazio e Abruzzo; Sud comprende Molise, Campania, Puglia, Basilicata e Calabria; Isole comprende Sicilia e Sardegna.

Un problema che ho incontrato è che i tre dataset di datiopen.it usano nomi regionali non uniformi tra loro. Ad esempio il Trentino può apparire come "Trentino-Alto Adige", "Trentino Alto Adige" senza trattino, o "Trentino-Alto Adige/Südtirol". Ho costruito una tabella di alias che traduce questi nomi alternativi al nome canonico usato nel database prima di salvare qualsiasi riga.

---

## Normalizzazione dei dati mancanti

Per ogni dataset, per ogni regione, costruisco un dizionario che associa ogni anno al valore osservato. Poi scorro le coppie di anni noti consecutivi: se tra due anni c'è un gap, calcolo il passo come differenza tra i due valori divisa per l'ampiezza del gap e inserisco gli anni intermedi con il valore ottenuto sommando il passo progressivamente. Gli estremi del range non vengono mai estrapolati: se il primo dato di una regione è del 2003 e l'ultimo del 2018, non genero nulla prima del 2003 né dopo il 2018.

L'esempio della commessa è quello con il dato del 2001 e del 2004: il passo è (val_2004 - val_2001) / 3, il 2002 vale val_2001 più un passo, il 2003 vale val_2001 più due passi.

---

## Calcolo delle cinque serie

Le cinque serie sono tutte varianti dello stesso calcolo: media aritmetica semplice dei valori per anno, raggruppata per area geografica o a livello nazionale. Come indicato nella nota metodologica della commessa, non avendo le quantità di riferimento per le percentuali si usa la media non ponderata. Questo significa che ogni regione pesa uguale indipendentemente dalla sua dimensione demografica o economica.

La serie 1 calcola la media delle regioni di ogni area per il tasso di partecipazione al mercato del lavoro. La serie 2 fa la stessa cosa su tutte le regioni senza distinzione geografica, dando il dato nazionale. La serie 3 calcola la media dell'incidenza della spesa in ricerca e sviluppo per ognuna delle cinque aree. La serie 4 calcola il tasso di sopravvivenza delle imprese a livello nazionale. La serie 5 fa lo stesso per area geografica.

---

## API REST

Tutti gli endpoint accettano da_anno e a_anno come parametri obbligatori nella query string. Se a_anno è minore di da_anno, l'API risponde con HTTP 400 e un messaggio di errore. Tre endpoint restituiscono i dati grezzi delle tre tabelle di import, cinque endpoint restituiscono le serie calcolate. La documentazione interattiva è disponibile su /docs generata automaticamente da FastAPI.

---

## Interfaccia web

Come punto facoltativo della commessa ho realizzato una pagina HTML raggiungibile all'indirizzo radice del server. Permette di selezionare una delle cinque serie calcolate, impostare un intervallo di anni e vedere i risultati in una tabella generata dinamicamente. La comunicazione tra la pagina e il server avviene tramite chiamate HTTP all'API, come richiesto dalla commessa.

---

## Scelte non ovvie e assunzioni

Lo script di import è stato scritto in modo che sia rieseguibile senza effetti collaterali: ogni esecuzione cancella i dati precedenti e li reinserisce da capo. Questo evita duplicati e permette di rieseguire la pipeline se i dataset vengono aggiornati.

I dataset di datiopen.it usano il punto e virgola come separatore in alcuni casi e la virgola in altri. Il codice prova prima con il punto e virgola, e se il risultato ha meno di tre colonne riprova con il rilevamento automatico del separatore tramite pandas.

Le righe con nomi di regione non riconoscibili vengono scartate silenziosamente durante l'import. Questo riguarda tipicamente righe aggregate come "Italia" o "Nord" che nei CSV compaiono insieme ai dati regionali ma non corrispondono a nessuna delle venti regioni previste. Le righe con valori non convertibili a numero vengono anch'esse scartate.

Durante il download si controlla che la risposta del server sia effettivamente un CSV e non una pagina HTML: datiopen.it a volte risponde con una pagina di errore invece del file. Se questo accade, viene sollevato un errore con le istruzioni per il download manuale.

---

## Limiti noti

La media non è ponderata per popolazione o PIL: in un contesto reale si userebbe un peso demografico per regione per ottenere valori nazionali più rappresentativi. L'estrapolazione fuori dal range osservato non è implementata per non generare dati privi di basi empiriche. Non è presente nessun meccanismo di autenticazione perché non era richiesto dalla commessa.
