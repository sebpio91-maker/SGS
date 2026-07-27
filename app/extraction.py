"""Best-effort Extraktion von Kapiteln/Prüfpunkten aus hochgeladenen Norm-PDFs.

Das ist bewusst eine einfache, heuristische Vorstrukturierung (kein echtes
Norm-Parsing) - das Ergebnis ist ein Entwurf, der vor dem Übernehmen in die
Datenbank geprüft und angepasst werden soll.
"""
import re
from io import BytesIO

import pdfplumber

KAPITEL_RE = re.compile(
    r"^(?P<kapitel>\d+(?:\.\d+){0,4}|Anhang\s+[A-Z](?:\.\d+)?|[A-Z]\.\d+)"
    r"\s+(?P<ueberschrift>[A-ZÄÖÜ0-9(][^\n]{1,120})$"
)

NOISE_RE = re.compile(
    r"^(Seite \d+|DIN EN [\d\-]+|EN [\d\-]+:\d+|©.*|Lizenziert für.*|Nur zur.*)$",
    re.IGNORECASE,
)


def extract_text(file_bytes: bytes) -> str:
    text_parts = []
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)
    return "\n".join(text_parts)


def _clean_lines(raw_text: str):
    for line in raw_text.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        if NOISE_RE.match(stripped):
            continue
        yield stripped


def parse_kapitel_entwurf(raw_text: str):
    """Zerlegt den Fließtext heuristisch in Kapitel-Entwürfe.

    Rückgabe: Liste von {"kapitel", "ueberschrift", "inhalt"} in Reihenfolge.
    """
    lines = list(_clean_lines(raw_text))

    entries = []
    current = None
    content_buffer = []

    def flush():
        if current is not None:
            inhalt = "\n".join(content_buffer).strip()
            current["inhalt"] = inhalt or None
            entries.append(current)

    for line in lines:
        match = KAPITEL_RE.match(line)
        is_heading = bool(match) and not line.rstrip().endswith((".", ",", ";", ":"))
        if is_heading:
            flush()
            current = {
                "kapitel": match.group("kapitel"),
                "ueberschrift": match.group("ueberschrift").strip(),
            }
            content_buffer = []
        else:
            if current is not None:
                content_buffer.append(line)
    flush()

    return entries
