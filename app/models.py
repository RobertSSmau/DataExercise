from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Regione(Base):
    __tablename__ = "regioni"
    id = Column(Integer, primary_key=True)
    nome = Column(String, unique=True, nullable=False, index=True)
    area = Column(String, nullable=False, index=True)


class Partecipazione(Base):
    __tablename__ = "partecipazione_lavoro"
    __table_args__ = (UniqueConstraint("regione_id", "anno", name="uq_part_reg_anno"),)
    id = Column(Integer, primary_key=True)
    regione_id = Column(Integer, ForeignKey("regioni.id"), nullable=False, index=True)
    anno = Column(Integer, nullable=False, index=True)
    valore = Column(Float, nullable=False)
    interpolato = Column(Boolean, nullable=False, default=False)
    regione = relationship("Regione")


class Sopravvivenza(Base):
    __tablename__ = "sopravvivenza_imprese"
    __table_args__ = (UniqueConstraint("regione_id", "anno", name="uq_sopr_reg_anno"),)
    id = Column(Integer, primary_key=True)
    regione_id = Column(Integer, ForeignKey("regioni.id"), nullable=False, index=True)
    anno = Column(Integer, nullable=False, index=True)
    valore = Column(Float, nullable=False)
    interpolato = Column(Boolean, nullable=False, default=False)
    regione = relationship("Regione")


class Ricerca(Base):
    __tablename__ = "incidenza_ricerca"
    __table_args__ = (UniqueConstraint("regione_id", "anno", name="uq_ric_reg_anno"),)
    id = Column(Integer, primary_key=True)
    regione_id = Column(Integer, ForeignKey("regioni.id"), nullable=False, index=True)
    anno = Column(Integer, nullable=False, index=True)
    valore = Column(Float, nullable=False)
    interpolato = Column(Boolean, nullable=False, default=False)
    regione = relationship("Regione")


class SerieCalcolata(Base):
    __tablename__ = "serie_calcolate"
    __table_args__ = (UniqueConstraint("tipo_serie", "area", "anno", name="uq_serie"),)
    id = Column(Integer, primary_key=True)
    # PART_AREA, PART_NAZ, RIC_AREA, SOPR_NAZ, SOPR_AREA
    tipo_serie = Column(String, nullable=False, index=True)
    area = Column(String, nullable=True, index=True)  # NULL per serie nazionali
    anno = Column(Integer, nullable=False, index=True)
    valore = Column(Float, nullable=False)
