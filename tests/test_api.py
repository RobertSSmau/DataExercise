"""Test di integrazione API (DB in-memory, non tocca dati reali)."""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_serves_html():
    r = client.get("/")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]


def test_partecipazione_range_valido():
    r = client.get("/api/partecipazione", params={"da_anno": 2010, "a_anno": 2015})
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_partecipazione_range_invertito():
    r = client.get("/api/partecipazione", params={"da_anno": 2020, "a_anno": 2010})
    assert r.status_code == 400


def test_sopravvivenza_range_valido():
    r = client.get("/api/sopravvivenza", params={"da_anno": 2010, "a_anno": 2015})
    assert r.status_code == 200


def test_ricerca_range_valido():
    r = client.get("/api/ricerca", params={"da_anno": 2010, "a_anno": 2015})
    assert r.status_code == 200


def test_serie_partecipazione_aree():
    r = client.get("/api/serie/partecipazione/aree", params={"da_anno": 2010, "a_anno": 2020})
    assert r.status_code == 200


def test_serie_partecipazione_nazionale():
    r = client.get("/api/serie/partecipazione/nazionale", params={"da_anno": 2010, "a_anno": 2020})
    assert r.status_code == 200


def test_serie_ricerca_aree():
    r = client.get("/api/serie/ricerca/aree", params={"da_anno": 2010, "a_anno": 2020})
    assert r.status_code == 200


def test_serie_sopravvivenza_nazionale():
    r = client.get("/api/serie/sopravvivenza/nazionale", params={"da_anno": 2010, "a_anno": 2020})
    assert r.status_code == 200


def test_serie_sopravvivenza_aree():
    r = client.get("/api/serie/sopravvivenza/aree", params={"da_anno": 2010, "a_anno": 2020})
    assert r.status_code == 200


def test_serie_range_invertito():
    r = client.get("/api/serie/partecipazione/aree", params={"da_anno": 2020, "a_anno": 2010})
    assert r.status_code == 400
