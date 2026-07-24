import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import matcher, suggest
from src.db import get_connection
from src.models import ArtikelDaten


def test_regal_kandidaten_werden_sinnvoll_bewertet():
    conn = get_connection()
    kandidaten = matcher.find_mechanik(conn, "300010")
    conn.close()
    bewertet = suggest.rank_kandidaten(
        kandidaten, "produkt", "Regal Liverpool mit 3 Fächern, weiß / Eiche Artisan", "Regal, Liverpool"
    )
    top_produkte = {k.produkt for k, score in bewertet if score == bewertet[0][1]}
    assert "(Aufbewahrungs-)Regal" in top_produkte
    assert bewertet[0][1] > 0


def test_score_exakter_substring_treffer():
    score = suggest.score_produkt("Kohlegrills", "Kohlegrill Kugelgrill schwarz")
    assert score > 0


def test_score_kein_treffer():
    score = suggest.score_produkt("Fahrradlenkerkorb", "Regal Liverpool mit 3 Fächern")
    assert score == 0.0


def test_produktspezifikationen_ranking_findet_spuelmaschinenfest():
    conn = get_connection()
    katalog = matcher.get_produktspezifikation_katalog(conn)
    conn.close()
    qualitaet_text = "Spezifische Eigenschaften: spülmaschinenfest, hitzebeständig bis 200°C"
    bewertet = suggest.rank_produktspezifikationen(katalog, qualitaet_text)
    top_parameter = bewertet[0][0]
    assert top_parameter in {"Spülmaschinenfest", "Hitzebeständigkeit"}
    assert bewertet[0][1] > 0


def test_produktspezifikationen_gruppiert_varianten_pro_parameter():
    conn = get_connection()
    katalog = matcher.get_produktspezifikation_katalog(conn)
    conn.close()
    bewertet = suggest.rank_produktspezifikationen(katalog, "irrelevanter Text ohne Treffer")
    parameter_namen = [p for p, _, _ in bewertet]
    assert len(parameter_namen) == len(set(parameter_namen))  # keine Duplikate
    korrosion = next(v for p, s, v in bewertet if p == "Korrosionsbeständigkeit")
    assert len(korrosion) > 1  # mehrere Varianten (Kammergröße/Laufzeit) vorhanden


def test_kategorie_fuer_parameter():
    assert suggest.kategorie_fuer_parameter("Mikrowellengeeignet") == "Küche"
    assert suggest.kategorie_fuer_parameter("Waschbarkeit") == "Textil"
    assert suggest.kategorie_fuer_parameter("Borstenabrundung") == "Sonstige"


def test_standardposition_immer():
    checked, begruendung = suggest.bewerte_standardposition("immer", ArtikelDaten())
    assert checked is True


def test_standardposition_batterie_erkannt():
    artikel = ArtikelDaten(batterietyp="Lithium-Ionen")
    checked, begruendung = suggest.bewerte_standardposition("batterie", artikel)
    assert checked is True
    assert "Lithium-Ionen" in begruendung


def test_standardposition_batterie_keine():
    artikel = ArtikelDaten(batterietyp="keine")
    checked, _ = suggest.bewerte_standardposition("batterie", artikel)
    assert checked is False


def test_standardposition_spielzeug_ueber_warenbereich():
    artikel = ArtikelDaten(warenbereich="Spielwaren")
    checked, _ = suggest.bewerte_standardposition("spielzeug", artikel)
    assert checked is True


def test_standardposition_elektrisch_ueber_batterie():
    artikel = ArtikelDaten(warenbereich="Hartware", batterietyp="AA")
    checked, _ = suggest.bewerte_standardposition("elektrisch", artikel)
    assert checked is True


def test_standardposition_lfgb_ist_immer_manuell():
    """LFGB (1005_PPM) wird laut Nutzer bislang manuell in der KV-Monitoringliste
    gepflegt, nicht aus dem Prüfumfang-Text abgeleitet -- daher nie automatisch an."""
    checked, begruendung = suggest.bewerte_standardposition("lfgb", ArtikelDaten())
    assert checked is False
    assert "manuell" in begruendung.lower()


def test_standardpositionen_katalog_vollstaendig():
    conn = get_connection()
    positionen = matcher.get_standard_pruefpositionen(conn)
    conn.close()
    codes = {p.code for p in positionen}
    assert codes == {"163_PPM", "1000_PPM", "1001_PPM", "1002_PPM", "1003_PPM", "1005_PPM", "112_PPM"}


def test_1001_ist_allgemeinfall_greift_ohne_spezifischere_pruefung():
    artikel = ArtikelDaten(warenbereich="Hartware", batterietyp="keine")
    checked, _ = suggest.bewerte_standardposition("allgemein", artikel)
    assert checked is True


def test_1001_entfaellt_bei_spielzeug():
    artikel = ArtikelDaten(warenbereich="Spielwaren")
    checked, _ = suggest.bewerte_standardposition("allgemein", artikel)
    assert checked is False


def test_1001_entfaellt_bei_elektrisch():
    artikel = ArtikelDaten(warenbereich="Hartware", batterietyp="Lithium-Ionen")
    checked, _ = suggest.bewerte_standardposition("allgemein", artikel)
    assert checked is False


def test_standardpositionen_katalog_hat_korrigierte_bedingung_fuer_1001():
    conn = get_connection()
    positionen = matcher.get_standard_pruefpositionen(conn)
    conn.close()
    eintrag = next(p for p in positionen if p.code == "1001_PPM")
    assert eintrag.bedingung == "allgemein"


def test_artikelkategorie_gruen_stern_ist_trivial():
    umfang, hinweis = suggest.pruefumfang_nach_artikelkategorie("Grün*")
    assert umfang == "0%"
    assert "trivial" in hinweis.lower()
    assert suggest.ist_trivialer_artikel("Grün*") is True
    assert suggest.ist_trivialer_artikel("Grün") is False


def test_artikelkategorie_gruen_40_prozent():
    umfang, _ = suggest.pruefumfang_nach_artikelkategorie("Grün")
    assert umfang == "40%"


def test_artikelkategorie_gelb_50_prozent():
    umfang, _ = suggest.pruefumfang_nach_artikelkategorie("Gelb")
    assert umfang == "50%"


def test_artikelkategorie_rot_60_bis_70_prozent():
    umfang, _ = suggest.pruefumfang_nach_artikelkategorie("Rot")
    assert umfang == "60–70%"


def test_artikelkategorie_unbekannt_oder_leer():
    umfang_leer, hinweis_leer = suggest.pruefumfang_nach_artikelkategorie("")
    umfang_unbekannt, hinweis_unbekannt = suggest.pruefumfang_nach_artikelkategorie("Blau")
    assert umfang_leer == ""
    assert umfang_unbekannt == ""
    assert "manuell" in hinweis_leer.lower()
    assert "Blau" in hinweis_unbekannt


def test_artikelkategorie_gross_kleinschreibung_und_leerzeichen_egal():
    umfang, _ = suggest.pruefumfang_nach_artikelkategorie("  grün  ")
    assert umfang == "40%"
