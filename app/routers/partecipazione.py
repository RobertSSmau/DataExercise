# GET /api/partecipazione , restituisce i dati grezzi filtrati per anno.
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Partecipazione, Regione
from app.schemas import DatoRegionaleOut

router = APIRouter(prefix="/api/partecipazione", tags=["partecipazione"])


@router.get("", response_model=list[DatoRegionaleOut])
def list_partecipazione(
    da_anno: int = Query(..., ge=1900, le=2100, description="Anno iniziale (incluso)"),
    a_anno: int = Query(..., ge=1900, le=2100, description="Anno finale (incluso)"),
    db: Session = Depends(get_db),
):
    if a_anno < da_anno:
        raise HTTPException(status_code=400, detail="a_anno deve essere >= da_anno")
    q = (
        db.query(Partecipazione, Regione)
        .join(Regione, Regione.id == Partecipazione.regione_id)
        .filter(Partecipazione.anno >= da_anno, Partecipazione.anno <= a_anno)
        .order_by(Regione.nome, Partecipazione.anno)
    )
    return [
        DatoRegionaleOut(
            regione=r.nome,
            area=r.area,
            anno=p.anno,
            valore=p.valore,
            interpolato=p.interpolato,
        )
        for p, r in q.all()
    ]
