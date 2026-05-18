from app.services.calculator import media_per_anno


def test_media_per_anno_aggrega():
    valori = [
        (2010, 10.0), (2010, 20.0),
        (2011, 30.0), (2011, 40.0), (2011, 50.0),
        (2012, 100.0),
    ]
    out = media_per_anno(valori)
    assert out == {2010: 15.0, 2011: 40.0, 2012: 100.0}


def test_media_per_anno_vuoto():
    assert media_per_anno([]) == {}


def test_media_per_anno_singolo():
    assert media_per_anno([(2000, 42.0)]) == {2000: 42.0}
