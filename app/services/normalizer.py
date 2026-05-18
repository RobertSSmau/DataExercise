"""Interpolazione lineare dei dati mancanti per anno, per regione."""
from __future__ import annotations

from app.database import SessionLocal
from app.models import Partecipazione, Ricerca, Sopravvivenza


def interpola_per_regione(serie: dict[int, float]) -> dict[int, tuple[float, bool]]:
    """
    Riceve {anno: valore} per una singola regione.
    Ritorna {anno: (valore, interpolato_bool)}.
    Gli anni mancanti tra due punti noti consecutivi vengono riempiti
    con interpolazione lineare. Non si estrapolano gli estremi.
    """
    if len(serie) < 2:
        return {a: (v, False) for a, v in serie.items()}

    anni_noti = sorted(serie)
    out: dict[int, tuple[float, bool]] = {a: (serie[a], False) for a in anni_noti}

    for i in range(len(anni_noti) - 1):
        a0, a1 = anni_noti[i], anni_noti[i + 1]
        gap = a1 - a0
        if gap <= 1:
            continue
        v0, v1 = serie[a0], serie[a1]
        passo = (v1 - v0) / gap
        for k in range(1, gap):
            out[a0 + k] = (v0 + passo * k, True)

    return out


def _normalizza_tabella(ModelCls, db) -> int:
    rows = db.query(ModelCls).all()
    per_regione: dict[int, dict[int, float]] = {}
    for r in rows:
        per_regione.setdefault(r.regione_id, {})[r.anno] = r.valore

    inseriti = 0
    for regione_id, serie in per_regione.items():
        interpolata = interpola_per_regione(serie)
        for anno, (valore, flag) in interpolata.items():
            if not flag:
                continue
            esiste = db.query(ModelCls).filter_by(regione_id=regione_id, anno=anno).first()
            if esiste:
                continue
            db.add(ModelCls(regione_id=regione_id, anno=anno, valore=valore, interpolato=True))
            inseriti += 1
    db.commit()
    return inseriti


def run_normalize() -> None:
    with SessionLocal() as db:
        for ModelCls in (Partecipazione, Sopravvivenza, Ricerca):
            n = _normalizza_tabella(ModelCls, db)
            print(f"{ModelCls.__tablename__}: aggiunti {n} record interpolati")
