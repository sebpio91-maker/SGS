"""Parser für den Lidl-Prüfauftrag (PDF).

Der Prüfauftrag ist ein Formular mit festen Feldnamen ("Label: Wert").
Die Strategie: alle bekannten Feldnamen im Text lokalisieren und den Wert
jedes Feldes als den Text zwischen diesem und dem nächst folgenden
bekannten Feldnamen nehmen. Produktspezifische Unterpunkte innerhalb von
Freitextfeldern (z. B. "Kennzeichnung", "Zubehör" innerhalb von
"Qualität") sind absichtlich NICHT als eigene Anker gelistet – sie
variieren stark je Produktkategorie und bleiben so unverändert Teil des
jeweiligen Freitexts.

Da bisher nur ein Beispieldokument vorliegt, ist der Parser defensiv:
nicht gefundene Felder bleiben None, und der vollständige Rohtext wird
immer mit gespeichert, damit nichts verloren geht, wenn sich das Format
in der Praxis leicht unterscheidet.

Bekannte Einschränkung: bei einigen Feldern mit mehrzeilig umbrochenem
Label (z. B. "Ref.-ergebnisse von / Vorgängern / übernehmen:") landet der
Wert in der PDF-Textextraktion mitten im Label statt danach, weil Label
und Wert als zweispaltige Tabelle zeilenweise interleaved werden. Diese
Felder (Batterie-Produktionsstätte, Ref.-Ergebnisse-Übernahme,
Anlieferung OS, Batterie im Lieferumfang, Sicherheitsdatenblatt
Gefahrgut) sind daher bewusst NICHT als eigene Anker gelistet – sie
tauchen nur unstrukturiert im `raw_text` auf. Keines dieser Felder wird
für die Prüfplan-Logik benötigt.
"""

import re

import pdfplumber

# Bekannte, feste Feldnamen des Prüfauftrags-Formulars (Reihenfolge ist
# für die Extraktion irrelevant, nur die Positionen im Text zählen).
FIELD_LABELS = [
    "IAN / Charge",
    "Artikelbezeichnung",
    "Listungsart",
    "Artikelkategorie",
    "IAN-Vorgänger",
    "VE",
    "EKL",
    "Früh. LT",
    "Warenbereich",
    "QM Ansprechparter",
    "Warengruppe",
    "Kostenstelle",
    "Text",
    "Ref.Vg EU/USA",
    "Lizenznehmer Lidl",
    "Lieferant",
    "Ansprechpartner",
    "Tel.-Nr.",
    "Fax",
    "E-mail",
    "Produktionsst.-ID",
    "Produktionsstätte",
    "Herkunftsland",
    "Anm. Herkunftsland",
    "Artikel",
    "Marke Lidl",
    "Marke Kaufland",
    "Maße",
    "Gewicht",
    "Brutto-Kolli-Gewicht",
    "Qualität",
    "Material",
    "Materialstärke",
    "Farbe",
    "Markenreferenz",
    "IOT",
    "NGO-Prüfung Bemerkung",
    "FFU Bemerkung",
    "Referenzprüfung",
    "Garantie",
    "Rücknahmegarantie",
    "Zertifizierungen",
    "RF-Sicherung",
    "Batterietyp",
    "Restlaufzeit in Tagen",
    "Sicherheitsdatenblatt",
    "Verpackung Zusatz",
    "Verpackung",
    "Sonstige Merkmale",
]

_AUFTRAGGEBER_RE = re.compile(r"Auftraggeber:\s*(.+)")
_LEADING_DATE_RE = re.compile(r"\b(\d{2}\.\d{2}\.\d{4})\b")

_SCOPE_KEYWORDS = {
    "chemie_lfgb": ["Chemie / LFGB", "Chemie/LFGB"],
    "sicherheit_norm": ["Sicherheit & Norm"],
    "produktspezifikation": ["Produktspezifikation"],
    "verpackung": ["Verpackung"],
    "verarbeitung_aql": ["Verarbeitung (AQL)"],
    "on_site_testing": ["On-Site Testing"],
    "standsicherheit": ["Standsicherheit"],
    "selbstauskunft": ["Selbstauskunft"],
}


_FOOTER_RE = re.compile(r"\n?Prüfauftrag\s+\S+\s*/\s*\S+\s*\(\d{2}\.\d{2}\.\d{4}\)\s*\d+\s*/\s*\d+")


def extract_text(pdf_source) -> str:
    """`pdf_source` ist ein Dateipfad oder ein datei-ähnliches Objekt
    (z. B. `io.BytesIO` eines hochgeladenen Uploads)."""
    with pdfplumber.open(pdf_source) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    # Fußzeile ("Prüfauftrag 559511 / 2604 (10.07.2026) 1 / 3") entfernen,
    # sonst hängt sie sich an den Wert des letzten Feldes jeder Seite an.
    return _FOOTER_RE.sub("", text)


def _build_label_pattern(label: str) -> re.Pattern:
    # Mehrwortige Labels können im PDF über Zeilenumbrüche getrennt sein
    # (z. B. "Sicherheitsdatenblatt\nGefahrgut:") – Leerzeichen im Label
    # werden daher als beliebiges Whitespace (inkl. Zeilenumbruch) erlaubt.
    escaped = re.escape(label).replace(r"\ ", r"\s+")
    return re.compile(rf"(?<![\w./]){escaped}\s*:")


def extract_fields(text: str) -> dict[str, str]:
    """Extrahiert alle bekannten Felder als {Label: Wert}.

    Wiederholte Labels (z. B. "Garantie" kommt zweimal vor) werden mit
    "\n" zusammengeführt.
    """
    raw_matches: list[tuple[int, int, str]] = []
    for label in FIELD_LABELS:
        pattern = _build_label_pattern(label)
        for m in pattern.finditer(text):
            raw_matches.append((m.start(), m.end(), label))

    # Ein kurzes Label kann als Teilstring eines längeren auftauchen
    # (z.B. "Gewicht" in "Brutto-Kolli-Gewicht", "Herkunftsland" in "Anm.
    # Herkunftsland") – bei Überlappung gewinnt der längere, zuerst
    # beginnende Treffer.
    raw_matches.sort(key=lambda item: (item[0], item[0] - item[1]))
    matches: list[tuple[int, int, str]] = []
    last_end = -1
    for start, end, label in raw_matches:
        if start < last_end:
            continue
        matches.append((start, end, label))
        last_end = end

    values: dict[str, list[str]] = {}
    for i, (_, end, label) in enumerate(matches):
        next_start = matches[i + 1][0] if i + 1 < len(matches) else len(text)
        value = text[end:next_start].strip()
        values.setdefault(label, []).append(value)

    return {label: "\n".join(parts).strip() for label, parts in values.items()}


def _first_line(value: str | None) -> str:
    """Erste Zeile eines Feldwerts.

    Einige mehrzeilig umbrochene Folge-Labels (z. B. "Produktionsstätte
    der Batterie(n):") können nicht als Anker erkannt werden und hängen
    daher als zusätzliche Zeilen an das vorangehende Feld (z. B.
    "Batterietyp") an. Der eigentliche Wert steht immer in der ersten
    Zeile, daher wird für Ja/Nein-artige Auswertungen nur diese benutzt.
    """
    if not value:
        return ""
    return value.splitlines()[0].strip()


def extract_header(text: str) -> dict[str, str | None]:
    auftraggeber_match = _AUFTRAGGEBER_RE.search(text)
    auftraggeber = auftraggeber_match.group(1).strip() if auftraggeber_match else None

    # Das Ausstellungsdatum steht am Dokumentanfang, nicht zwingend direkt
    # neben "Auftraggeber:" – nur in den ersten Zeilen suchen, damit nicht
    # versehentlich ein späteres Datum (z. B. aus dem Prüfumfang) greift.
    date_match = _LEADING_DATE_RE.search(text[:300])
    datum = date_match.group(1) if date_match else None

    return {"auftraggeber": auftraggeber, "datum": datum}


_PRUEFUMFANG_RE = re.compile(r"Prüfumfang\s*\n(.*?)\nQualitäten\b", re.DOTALL)


def extract_pruefumfang_block(text: str) -> str | None:
    m = _PRUEFUMFANG_RE.search(text)
    return m.group(1).strip() if m else None


def _mask_pruefumfang(text: str) -> str:
    # Der Prüfumfang-Freitext enthält keine der bekannten Feld-Labels und
    # würde sonst vom vorangehenden Feld (typischerweise "Herkunftsland")
    # verschluckt, da PDF-Textextraktion ihn direkt davor einreiht statt
    # in der visuellen Lesereihenfolge. Ein Leerzeichen wahrt die
    # Wortgrenze für das nachfolgende "Qualitäten"-Label.
    return _PRUEFUMFANG_RE.sub(" Qualitäten", text)


def determine_scope_categories(pruefumfang_text: str | None) -> list[str]:
    if not pruefumfang_text:
        return []
    found = []
    for key, keywords in _SCOPE_KEYWORDS.items():
        if any(kw in pruefumfang_text for kw in keywords):
            found.append(key)
    return found


def _is_affirmed(value: str | None) -> bool:
    if not value:
        return False
    return value.strip().lower() not in ("nein", "-", "")


def parse_pruefauftrag(pdf_source) -> dict:
    text = extract_text(pdf_source)
    pruefumfang_text = extract_pruefumfang_block(text)
    scope_categories = determine_scope_categories(pruefumfang_text)
    fields = extract_fields(_mask_pruefumfang(text))
    header = extract_header(text)

    batterietyp = _first_line(fields.get("Batterietyp"))
    has_battery = bool(batterietyp) and batterietyp.lower() not in ("keine", "-", "")

    qualitaet_text = fields.get("Qualität", "")
    has_manual = bool(
        re.search(r"montageanleitung|bedienungsanleitung", qualitaet_text, re.IGNORECASE)
    )

    ngo_bemerkung = fields.get("NGO-Prüfung Bemerkung")
    ffu_bemerkung = fields.get("FFU Bemerkung")

    return {
        "auftraggeber": header["auftraggeber"],
        "datum": header["datum"],
        "ian_charge": fields.get("IAN / Charge"),
        "artikelbezeichnung": fields.get("Artikelbezeichnung"),
        "artikelkategorie": fields.get("Artikelkategorie"),
        "warenbereich": fields.get("Warenbereich"),
        "warengruppe": fields.get("Warengruppe"),
        "lieferant": fields.get("Lieferant"),
        "lieferant_ansprechpartner": fields.get("Ansprechpartner"),
        "produktionsstaette": fields.get("Produktionsstätte"),
        "herkunftsland": fields.get("Herkunftsland"),
        "maße": fields.get("Maße"),
        "gewicht": fields.get("Gewicht"),
        "material": fields.get("Material"),
        "materialstaerke": fields.get("Materialstärke"),
        "farbe": fields.get("Farbe"),
        "zertifizierungen": fields.get("Zertifizierungen"),
        "verpackung": fields.get("Verpackung"),
        "pruefumfang_text": pruefumfang_text,
        "pruefumfang_kategorien": scope_categories,
        "has_battery": has_battery,
        "has_manual": has_manual,
        "referenzpruefung": _is_affirmed(_first_line(fields.get("Referenzprüfung"))),
        "ngo_pruefung": bool(ngo_bemerkung) or "NGO" in (pruefumfang_text or ""),
        "ffu_pruefung": bool(ffu_bemerkung) or "FFU" in (pruefumfang_text or ""),
        "raw_fields": fields,
        "raw_text": text,
    }
