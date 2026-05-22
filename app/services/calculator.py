# Calcola le 5 serie statistiche aggregate e le salva nella tabella serie_calcolate.
from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from app.constants import AREE
from app.database import SessionLocal
from app.models import Partecipazione, Regione, Ricerca, SerieCalcolata, Sopravvivenza


def media_per_anno(coppie: Iterable[tuple[int, float]]) -> dict[int, float]:
    # media aritmetica semplice, non ponderata (come da nota metodologica della commessa)
    accum: dict[int, list[float]] = defaultdict(list)
    for anno, valore in coppie:
        accum[anno].append(valore)
    return {anno: sum(vs) / len(vs) for anno, vs in accum.items() if vs}


def _persisti_serie(db, tipo_serie: str, dati: dict[int, float], area: str | None = None) -> int:
    n = 0
    for anno, valore in dati.items():
        esiste = (
            db.query(SerieCalcolata)
            .filter_by(tipo_serie=tipo_serie, area=area, anno=anno)
            .first()
        )
        if esiste:
            esiste.valore = valore
        else:
            db.add(SerieCalcolata(tipo_serie=tipo_serie, area=area, anno=anno, valore=valore))
            n += 1
    db.commit()
    return n


def _serie_per_area(db, ModelCls, tipo_serie: str) -> int:
    totale = 0
    for area in AREE:
        coppie = (
            db.query(ModelCls.anno, ModelCls.valore)
            .join(Regione, Regione.id == ModelCls.regione_id)
            .filter(Regione.area == area)
            .all()
        )
        dati = media_per_anno(coppie)
        totale += _persisti_serie(db, tipo_serie, dati, area=area)
    return totale


def _serie_nazionale(db, ModelCls, tipo_serie: str) -> int:
    coppie = db.query(ModelCls.anno, ModelCls.valore).all()
    dati = media_per_anno(coppie)
    return _persisti_serie(db, tipo_serie, dati, area=None)


def run_calculate() -> None:
    with SessionLocal() as db:
        db.query(SerieCalcolata).delete()
        db.commit()

        n1 = _serie_per_area(db, Partecipazione, "PART_AREA")
        n2 = _serie_nazionale(db, Partecipazione, "PART_NAZ")
        n3 = _serie_per_area(db, Ricerca, "RIC_AREA")
        n4 = _serie_nazionale(db, Sopravvivenza, "SOPR_NAZ")
        n5 = _serie_per_area(db, Sopravvivenza, "SOPR_AREA")

        print(f"Serie calcolate:")
        print(f"  PART_AREA  (partecipazione per area)     : {n1} righe")
        print(f"  PART_NAZ   (partecipazione nazionale)    : {n2} righe")
        print(f"  RIC_AREA   (ricerca per area)            : {n3} righe")
        print(f"  SOPR_NAZ   (sopravvivenza nazionale)     : {n4} righe")
        print(f"  SOPR_AREA  (sopravvivenza per area)      : {n5} righe")
