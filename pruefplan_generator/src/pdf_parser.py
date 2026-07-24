"""Extrahiert Artikeldaten aus einem Lidl/OWIM-Prüfauftrag-PDF.

Das PDF folgt durchgängig dem Muster 'Label: Wert' pro Zeile für die für uns
relevanten Kernfelder (IAN, Warengruppe, Artikelkategorie, Produktklassifizierung,
Batterietyp, Zertifizierungen, Herkunftsland, ...). Ein paar Felder (Material,
Materialstärke, Farbe) sind mehrzeilige Blöcke unter einer 'Label: Style_X:'-
Kopfzeile; die werden nur als Rohtext für die Anzeige mitgenommen, nicht für
das Matching verwendet.
"""

from __future__ import annotations

import re
from pathlib import Path

import pdfplumber

from src.models import ArtikelDaten
from src.db import normalize_warengruppe

# Reihenfolge der Top-Level-Labels im Dokument, wie sie im PDF auftauchen.
# Wird u.a. genutzt, um mehrzeilige Blöcke zu begrenzen.
_KNOWN_LABELS = [
    "IAN / Charge", "Artikelbezeichnung", "Initiale Charge", "Listungsart",
    "Artikelkategorie", "IAN-Vorgänger", "VE", "EKL", "Früh. LT", "Warenbereich",
    "QM Ansprechparter", "Warengruppe", "Kostenstelle", "Text", "Ref.Vg EU/USA",
    "Lizenznehmer Lidl", "Lieferant", "Ansprechpartner", "Tel.-Nr.", "Fax", "E-mail",
    "Produktionsst.-ID", "Produktionsstätte", "Herkunftsland", "Artikel",
    "Marke Lidl", "Marke Kaufland", "Maße", "Gewicht", "Brutto-Kolli-Gewicht",
    "Qualität", "Produktklassifizierung", "Artikelmerkmale", "Kennzeichnung",
    "Anleitung", "Material", "Materialstärke", "Farbe", "Markenreferenz",
    "IOT", "Bemerkung", "FFU Bemerkung", "Referenzprüfung", "Garantie",
    "Rücknahmegarantie", "Zertifizierungen", "RF-Sicherung", "Batterietyp",
    "Verpackung", "Verpackung Zusatz", "Sonstige Merkmale",
]


def _extract_lines(pdf_path: Path) -> list[str]:
    lines: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            lines.extend(text.split("\n"))
    return lines


def _single(lines: list[str], label: str) -> str:
    pattern = re.compile(r"^" + re.escape(label) + r"\s*:\s*(.*)$")
    for line in lines:
        m = pattern.match(line.strip())
        if m:
            return m.group(1).strip()
    return ""


def _block(lines: list[str], label: str, stop_labels: list[str] | None = None) -> str:
    """Bestlösung für mehrzeilige Blöcke: Zeilen ab dem Label bis zur nächsten
    Grenz-Label-Zeile (oder Trennlinie aus Unterstrichen).

    `stop_labels` überschreibt, welche Labels als Blockende zählen (Default:
    alle anderen bekannten Labels). Das ist nötig für Blöcke wie "Qualität",
    deren Unterabschnitte (z.B. "Artikelmerkmale", "Spezifische Eigenschaften")
    je nach Prüfauftrag mal als Teil des Blocks, mal als eigenständiges Feld
    auftauchen -- hier reicht eine engere, verlässliche Grenzliste."""
    pattern = re.compile(r"^" + re.escape(label) + r"\s*:\s*(.*)$")
    start_idx = None
    first_value = ""
    for i, line in enumerate(lines):
        m = pattern.match(line.strip())
        if m:
            start_idx = i
            first_value = m.group(1).strip()
            break
    if start_idx is None:
        return ""

    boundary_labels = stop_labels if stop_labels is not None else [l for l in _KNOWN_LABELS if l != label]
    label_re = re.compile(r"^(" + "|".join(re.escape(l) for l in boundary_labels) + r")\s*:")

    collected = [first_value] if first_value else []
    for line in lines[start_idx + 1 :]:
        stripped = line.strip()
        if not stripped or set(stripped) == {"_"}:
            continue
        if label_re.match(stripped):
            break
        collected.append(stripped)
    return "\n".join(c for c in collected if c)


# Felder, die im PDF zuverlässig ERST NACH dem gesamten Qualitäts-/Artikelmerkmale-
# Freitext folgen (in allen bisher gesehenen Prüfaufträgen) -- dienen als
# Blockende für die Qualität-Extraktion, s. _block()-Docstring.
_QUALITAET_STOP_LABELS = [
    "Material", "Materialstärke", "Farbe", "Markenreferenz", "IOT",
    "Zertifizierungen", "Garantie", "Rücknahmegarantie", "RF-Sicherung",
    "Batterietyp", "Anlieferung",
]


_PHASE_START_RE = re.compile(
    r"^(\d+%[:\s]*[A-Za-zÄÖÜäöüß/&\- ]*|ALT|SLT(?: SPU)?)\s*\([^()]*\)"
)


def _pruefumfang_bloecke(lines: list[str]) -> list[tuple[str, str]]:
    """Liste von (Phasen-Label, vollständiger Phasentext) für den Prüfumfang-Block.

    Prüfphasen-Zeilen im PDF erkennt man daran, dass sie mit '<Label> (...SGS...)'
    beginnen (Labor-Angabe in Klammern, mit oder ohne vorangestelltes Datum).
    Nachfolgende Zeilen ohne dieses Muster sind Fortsetzungen (Zeilenumbruch)
    des vorherigen Phasentexts."""
    bloecke: list[tuple[str, str]] = []
    in_block = False
    current_label: str | None = None
    current_parts: list[str] = []

    def flush() -> None:
        if current_label is not None:
            text = " ".join(current_parts)
            text = re.sub(r"\s+([,.):;])", r"\1", text)
            text = re.sub(r"\s+", " ", text).strip()
            bloecke.append((current_label, text))

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("Prüfumfang"):
            in_block = True
            continue
        if stripped == "Qualitäten":
            break
        if not in_block:
            continue
        m = _PHASE_START_RE.match(stripped)
        if m:
            flush()
            current_label = m.group(1).strip()
            current_parts = [stripped]
        elif current_label is not None:
            current_parts.append(stripped)
    flush()
    return bloecke


def _pruefumfang(lines: list[str]) -> list[str]:
    return [label for label, _ in _pruefumfang_bloecke(lines)]


def _pruefumfang_komponenten(lines: list[str]) -> dict[str, list[str]]:
    """Für jede Prüfphase mit 'bestehend aus X, Y, Z': die einzelnen Bestandteile
    (z.B. ALT -> ['Chemie / LFGB', 'Sicherheit & Norm / Sonder- & Funktionsparameter',
    'Selbstauskunft', '(Physikalische-) Produktspezifikationen'])."""
    marker = "bestehend aus"
    komponenten: dict[str, list[str]] = {}
    for label, text in _pruefumfang_bloecke(lines):
        idx = text.find(marker)
        if idx == -1:
            continue
        rest = text[idx + len(marker) :].strip()
        teile = [t.strip() for t in rest.split(",")]
        komponenten[label] = [t for t in teile if t]
    return komponenten


def _laenderdaten(lines: list[str]) -> list[str]:
    codes: list[str] = []
    in_block = False
    code_re = re.compile(r"^([A-Z]{2,6})\s+\d")
    excluded = {"LB", "VE", "LT"}
    for line in lines:
        stripped = line.strip()
        if stripped == "Länderdaten":
            in_block = True
            continue
        if stripped.startswith("Anlagen"):
            break
        if not in_block:
            continue
        m = code_re.match(stripped)
        if m and m.group(1) not in excluded and m.group(1) not in codes:
            codes.append(m.group(1))
    return codes


def parse_pruefauftrag(pdf_path: Path) -> ArtikelDaten:
    pdf_path = Path(pdf_path)
    lines = _extract_lines(pdf_path)

    ian_charge_raw = _single(lines, "IAN / Charge")
    ian, charge = "", ""
    if "/" in ian_charge_raw:
        parts = [p.strip() for p in ian_charge_raw.split("/", 1)]
        ian, charge = parts[0], parts[1] if len(parts) > 1 else ""
    else:
        ian = ian_charge_raw

    warengruppe_raw = _single(lines, "Warengruppe")
    zertifizierungen_raw = _single(lines, "Zertifizierungen")

    artikel = ArtikelDaten(
        ian=ian,
        charge=charge,
        ian_charge=f"{ian}_{charge}" if ian and charge else ian_charge_raw,
        artikelbezeichnung=_single(lines, "Artikelbezeichnung"),
        artikelkategorie=_single(lines, "Artikelkategorie"),
        ian_vorgaenger=_single(lines, "IAN-Vorgänger"),
        warengruppe=warengruppe_raw,
        warengruppe_code=normalize_warengruppe(warengruppe_raw),
        warenbereich=_single(lines, "Warenbereich"),
        lieferant=_single(lines, "Lieferant"),
        produktklassifizierung=_single(lines, "Produktklassifizierung"),
        qualitaet=_block(lines, "Qualität", stop_labels=_QUALITAET_STOP_LABELS),
        material=_block(lines, "Material"),
        materialstaerke=_block(lines, "Materialstärke"),
        farbe=_block(lines, "Farbe"),
        batterietyp=_single(lines, "Batterietyp"),
        rf_sicherung=_single(lines, "RF-Sicherung"),
        zertifizierungen=zertifizierungen_raw,
        herkunftsland=_single(lines, "Herkunftsland"),
        produktionsstaette=_single(lines, "Produktionsstätte"),
        pruefumfang=_pruefumfang(lines),
        pruefumfang_komponenten=_pruefumfang_komponenten(lines),
        laender=_laenderdaten(lines),
        quelle_datei=pdf_path.name,
    )
    return artikel


if __name__ == "__main__":
    import sys

    path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if path is None:
        raise SystemExit("Usage: python -m src.pdf_parser <pfad-zu-pruefauftrag.pdf>")
    result = parse_pruefauftrag(path)
    for key, value in result.__dict__.items():
        print(f"{key}: {value!r}")
