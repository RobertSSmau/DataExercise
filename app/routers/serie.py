# Endpoint per le 5 serie statistiche calcolate (partecipazione, ricerca, sopravvivenza).
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SerieCalcolata
from app.schemas import SerieAreaOut, SerieNazionaleOut

router = APIRouter(prefix="/api/serie", tags=["serie calcolate"])


def _valida_range(da_anno: int, a_anno: int) -> None:
    if a_anno < da_anno:
        raise HTTPException(status_code=400, detail="a_anno deve essere >= da_anno")


def _query_area(db: Session, tipo: str, da_anno: int, a_anno: int):
    return (
        db.query(SerieCalcolata)
        .filter(
            SerieCalcolata.tipo_serie == tipo,
            SerieCalcolata.area.isnot(None),
            SerieCalcolata.anno >= da_anno,
            SerieCalcolata.anno <= a_anno,
        )
        .order_by(SerieCalcolata.area, SerieCalcolata.anno)
        .all()
    )


def _query_naz(db: Session, tipo: str, da_anno: int, a_anno: int):
    return (
        db.query(SerieCalcolata)
        .filter(
            SerieCalcolata.tipo_serie == tipo,
            SerieCalcolata.area.is_(None),
            SerieCalcolata.anno >= da_anno,
            SerieCalcolata.anno <= a_anno,
        )
        .order_by(SerieCalcolata.anno)
        .all()
    )


@router.get("/partecipazione/aree", response_model=list[SerieAreaOut])
def serie_partecipazione_aree(
    da_anno: int = Query(..., description="Anno iniziale"),
    a_anno: int = Query(..., description="Anno finale"),
    db: Session = Depends(get_db),
):
    _valida_range(da_anno, a_anno)
    return [
        SerieAreaOut(area=r.area, anno=r.anno, valore=r.valore)
        for r in _query_area(db, "PART_AREA", da_anno, a_anno)
    ]


@router.get("/partecipazione/nazionale", response_model=list[SerieNazionaleOut])
def serie_partecipazione_nazionale(
    da_anno: int = Query(...),
    a_anno: int = Query(...),
    db: Session = Depends(get_db),
):
    _valida_range(da_anno, a_anno)
    return [
        SerieNazionaleOut(anno=r.anno, valore=r.valore)
        for r in _query_naz(db, "PART_NAZ", da_anno, a_anno)
    ]


@router.get("/ricerca/aree", response_model=list[SerieAreaOut])
def serie_ricerca_aree(
    da_anno: int = Query(...),
    a_anno: int = Query(...),
    db: Session = Depends(get_db),
):
    _valida_range(da_anno, a_anno)
    return [
        SerieAreaOut(area=r.area, anno=r.anno, valore=r.valore)
        for r in _query_area(db, "RIC_AREA", da_anno, a_anno)
    ]


@router.get("/sopravvivenza/nazionale", response_model=list[SerieNazionaleOut])
def serie_sopravvivenza_nazionale(
    da_anno: int = Query(...),
    a_anno: int = Query(...),
    db: Session = Depends(get_db),
):
    _valida_range(da_anno, a_anno)
    return [
        SerieNazionaleOut(anno=r.anno, valore=r.valore)
        for r in _query_naz(db, "SOPR_NAZ", da_anno, a_anno)
    ]


@router.get("/sopravvivenza/aree", response_model=list[SerieAreaOut])
def serie_sopravvivenza_aree(
    da_anno: int = Query(...),
    a_anno: int = Query(...),
    db: Session = Depends(get_db),
):
    _valida_range(da_anno, a_anno)
    return [
        SerieAreaOut(area=r.area, anno=r.anno, valore=r.valore)
        for r in _query_area(db, "SOPR_AREA", da_anno, a_anno)
    ]
