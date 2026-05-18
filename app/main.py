from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers import partecipazione, ricerca, serie, sopravvivenza

Base.metadata.create_all(engine)

app = FastAPI(
    title="FSD Esame 2024 — Mercato del lavoro IT",
    description=(
        "API REST per dati regionali italiani su partecipazione al mercato del lavoro, "
        "sopravvivenza imprese e spesa R&S, con 5 serie statistiche aggregate per macro-area."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(partecipazione.router)
app.include_router(sopravvivenza.router)
app.include_router(ricerca.router)
app.include_router(serie.router)

STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", include_in_schema=False)
def root():
    return FileResponse(str(STATIC_DIR / "index.html"))
