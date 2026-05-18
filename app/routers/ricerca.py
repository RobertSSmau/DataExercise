from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Regione, Ricerca
from app.schemas import DatoRegionaleOut

router = APIRouter(prefix="/api/ricerca", tags=["ricerca"])


@router.get("", response_model=list[DatoRegionaleOut])
def list_ricerca(
    da_anno: int = Query(..., ge=1900, le=2100, description="Anno iniziale (incluso)"),
    a_anno: int = Query(..., ge=1900, le=2100, description="Anno finale (incluso)"),
    db: Session = Depends(get_db),
):
    if a_anno < da_anno:
        raise HTTPException(status_code=400, detail="a_anno deve essere >= da_anno")
    q = (
        db.query(Ricerca, Regione)
        .join(Regione, Regione.id == Ricerca.regione_id)
        .filter(Ricerca.anno >= da_anno, Ricerca.anno <= a_anno)
        .order_by(Regione.nome, Ricerca.anno)
    )
    return [
        DatoRegionaleOut(
            regione=r.nome,
            area=r.area,
            anno=x.anno,
            valore=x.valore,
            interpolato=x.interpolato,
        )
        for x, r in q.all()
    ]
