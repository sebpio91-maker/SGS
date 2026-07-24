import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import matcher
from src.db import get_connection


def test_mechanik_treffer_fuer_regal_warengruppe():
    conn = get_connection()
    treffer = matcher.find_mechanik(conn, "300010")
    conn.close()
    produkte = {t.produkt for t in treffer}
    assert "(Aufbewahrungs-)Regal" in produkte
    assert len(treffer) >= 2  # mehrdeutig, Disambiguierung nötig


def test_mechanik_kein_treffer_fuer_unbekannte_warengruppe():
    conn = get_connection()
    treffer = matcher.find_mechanik(conn, "999999")
    conn.close()
    assert treffer == []


def test_normen_fallback_eindeutiger_treffer_campingtisch():
    conn = get_connection()
    status, treffer = matcher.find_normen(
        conn,
        {
            "kategorie": "Möbel",
            "produktart": "Tisch",
            "zielgruppe": "Privat",
            "einsatzort": "Outdoor",
            "bereich": "Camping",
            "produkt": "Campingtisch",
        },
    )
    conn.close()
    assert status == "unique"
    assert len(treffer) == 1
    assert treffer[0].preis == 570.0
    assert treffer[0].normen == "DIN EN 581-1 / DIN EN 518-3"


def test_normen_fallback_mehrdeutig_ohne_produkt():
    conn = get_connection()
    status, treffer = matcher.find_normen(
        conn,
        {
            "kategorie": "Möbel",
            "produktart": "Tisch",
            "zielgruppe": "Privat",
            "einsatzort": "Outdoor",
        },
    )
    conn.close()
    assert status == "ambiguous"
    assert len(treffer) > 1


def test_normen_fallback_keine_treffer():
    conn = get_connection()
    status, treffer = matcher.find_normen(conn, {"kategorie": "GibtEsNicht"})
    conn.close()
    assert status == "none"
    assert treffer == []


def test_sonderposten_zusatzkosten_armlehne_und_sitzplatz():
    conn = get_connection()
    kosten = matcher.find_zusatzkosten(
        conn,
        {"kategorie": "Möbel", "produktart": "Sitzmöbel"},
        ["Armlehne", "zusätzlicher Sitzplatz"],
    )
    conn.close()
    assert kosten == 350 + 170


def test_sonderposten_keine_eigenschaften_ergibt_null():
    conn = get_connection()
    kosten = matcher.find_zusatzkosten(conn, {"kategorie": "Möbel"}, [])
    conn.close()
    assert kosten == 0.0


def test_add_mechanik_regel_legt_neuen_datensatz_an():
    conn = get_connection()
    try:
        vorher = len(matcher.find_mechanik(conn, "555555"))
        neu = matcher.add_mechanik_regel(
            conn,
            lidl_bereich="Test",
            lidl_warengruppe="555.555 Testgruppe",
            warengruppe_code="555555",
            produkt="Testprodukt",
            norm_ek_ppm="DIN TEST 1234",
            anzahl_muster="2",
            kosten_vp=123.45,
            bemerkungen="von Test angelegt",
        )
        assert neu.id is not None
        assert neu.produkt == "Testprodukt"
        assert neu.kosten_vp == 123.45

        nachher = matcher.find_mechanik(conn, "555555")
        assert len(nachher) == vorher + 1
        assert any(t.produkt == "Testprodukt" for t in nachher)
    finally:
        conn.execute("DELETE FROM mechanik_regeln WHERE warengruppe_code = '555555'")
        conn.commit()
        conn.close()


def test_klassifiziere_komponente():
    assert matcher.klassifiziere_komponente("Chemie / LFGB") == "chemie"
    assert matcher.klassifiziere_komponente("Selbstauskunft") == "selbstauskunft"
    assert matcher.klassifiziere_komponente("(Physikalische-) Produktspezifikationen") == "produktspezifikation"
    assert matcher.klassifiziere_komponente("NGO") == "ngo"
    assert (
        matcher.klassifiziere_komponente("Sicherheit & Norm / Sonder- & Funktionsparameter")
        == "sicherheit_norm"
    )
    assert matcher.klassifiziere_komponente("Verpackung / Transportverpackung") == "sonstige"


def test_produktspezifikation_katalog_hat_bekannte_parameter():
    conn = get_connection()
    katalog = matcher.get_produktspezifikation_katalog(conn)
    conn.close()
    parameter = {p.parameter for p in katalog}
    assert "Korrosionsbeständigkeit" in parameter
    assert "Spülmaschinenfest" in parameter
    assert len(katalog) > 50
