from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class Settings:
    db_url: str = f"sqlite:///{ROOT / 'data' / 'esame.db'}"
    data_dir: Path = ROOT / "data"

    # URL diretti per il download CSV da datiopen.it
    # Se questi non funzionano, scaricare manualmente e salvare in data/
    url_partecipazione: str = (
        "http://www.datiopen.it/export/csv/"
        "Partecipazione-della-popolazione-al-mercato-del-lavoro-per-regione.csv"
    )
    url_sopravvivenza: str = (
        "http://www.datiopen.it/export/csv/"
        "Tasso-di-sopravvivenza-a-tre-anni-delle-imprese-dei-settori-"
        "ad-alta-intensita-di-conoscenza-per-regione.csv"
    )
    url_ricerca: str = (
        "http://www.datiopen.it/export/csv/"
        "Incidenza-della-spesa-delle-imprese-in-ricerca-e-sviluppo-sul-PIL-per-regione.csv"
    )


settings = Settings()
