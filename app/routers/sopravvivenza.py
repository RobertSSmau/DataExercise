# GET /api/sopravvivenza, restituisce i dati grezzi filtrati per anno.
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Regione, Sopravvivenza
from app.schemas import DatoRegionaleOut

router = APIRouter(prefix="/api/sopravvivenza", tags=["sopravvivenza"])


@router.get("", response_model=list[DatoRegionaleOut])
def list_sopravvivenza(
    da_anno: int = Query(..., ge=1900, le=2100, description="Anno iniziale (incluso)"),
    a_anno: int = Query(..., ge=1900, le=2100, description="Anno finale (incluso)"),
    db: Session = Depends(get_db),
):
    if a_anno < da_anno:
        raise HTTPException(status_code=400, detail="a_anno deve essere >= da_anno")
    q = (
        db.query(Sopravvivenza, Regione)
        .join(Regione, Regione.id == Sopravvivenza.regione_id)
        .filter(Sopravvivenza.anno >= da_anno, Sopravvivenza.anno <= a_anno)
        .order_by(Regione.nome, Sopravvivenza.anno)
    )
    return [
        DatoRegionaleOut(
            regione=r.nome,
            area=r.area,
            anno=s.anno,
            valore=s.valore,
            interpolato=s.interpolato,
        )
        for s, r in q.all()
    ]
