import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.pdf_parser import parse_pruefauftrag

SGS_DIR = Path(__file__).resolve().parent.parent.parent


def test_altes_pdf_format_ohne_datum_im_labor():
    artikel = parse_pruefauftrag(SGS_DIR / "516575_PA_HG_Stand_26.02.2026.pdf")
    assert artikel.ian == "516575"
    assert artikel.warengruppe_code == "300010"
    assert artikel.pruefumfang == ["30% SPU/QSP", "ALT", "100%: PSI"]
    assert artikel.pruefumfang_komponenten["ALT"] == [
        "Chemie / LFGB",
        "Sicherheit & Norm / Sonder- & Funktionsparameter",
        "Selbstauskunft",
        "(Physikalische-) Produktspezifikationen",
    ]


def test_neues_pdf_format_mit_datum_im_labor():
    artikel = parse_pruefauftrag(SGS_DIR / "534644_PA_HG_Stand_07.07.2026.pdf")
    assert artikel.pruefumfang == ["30% SPU/QSP", "ALT", "100%: PSI"]
    assert artikel.pruefumfang_komponenten["100%: PSI"] == [
        "Verpackung / Transportverpackung",
        "Produktspezifikationen",
        "Verarbeitung (AQL)",
        "On-Site Testing",
    ]


def test_labor_ohne_sgs_im_namen_wird_nicht_uebersehen():
    """551747 nennt 'Eurofins' statt 'SGS' als Labor -- alle 3 Phasen müssen trotzdem erkannt werden."""
    artikel = parse_pruefauftrag(SGS_DIR / "551747_PA_HG_Stand_07.07.2026.pdf")
    assert artikel.pruefumfang == ["30% SPU/QSP", "ALT", "100%: PSI"]
    assert "chemikalienbeständig" in artikel.qualitaet.lower()


def test_zusaetzliche_pruefphasen_slt():
    artikel = parse_pruefauftrag(SGS_DIR / "559511_PA_HG_Stand_10.07.2026.pdf")
    assert "SLT" in artikel.pruefumfang
    assert "SLT SPU" in artikel.pruefumfang
    assert artikel.pruefumfang_komponenten["SLT"] == ["SLT (Standsicherheit)"]


def test_qualitaet_faengt_auslobungen_in_unterabschnitten_ein():
    """Bei manchen Prüfaufträgen liegen Auslobungen unter 'Spezifische Eigenschaften',
    das direkt zum Qualität-Block gehört und nicht als eigene Grenze behandelt werden darf."""
    artikel = parse_pruefauftrag(SGS_DIR / "551747_PA_HG_Stand_07.07.2026.pdf")
    assert "chemikalienbeständig" in artikel.qualitaet
    assert artikel.qualitaet.strip() != ""
