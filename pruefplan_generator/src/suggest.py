"""Keyword-basierte Disambiguierung: wenn eine Warengruppe mehrere Produkt-
Kandidaten hat, wird per einfachem Textabgleich (Artikelbezeichnung /
Produktklassifizierung gegen die 'produkt'-Spalte) eine Rangfolge vorgeschlagen.
Kein ML — Transparenz statt Blackbox; der Nutzer bestätigt/korrigiert in der UI.
"""

from __future__ import annotations

import re
from typing import TypeVar

from src.models import ArtikelDaten

_WORD_RE = re.compile(r"[a-zäöüß0-9]+")
_MIN_SUBSTRING_LEN = 4


def _normalize_tokens(text: str) -> set[str]:
    if not text:
        return set()
    return set(_WORD_RE.findall(text.lower()))


def _token_score(produkt_token: str, artikel_tokens: set[str]) -> float:
    if produkt_token in artikel_tokens:
        return 1.0
    if len(produkt_token) >= _MIN_SUBSTRING_LEN:
        for token in artikel_tokens:
            if len(token) >= _MIN_SUBSTRING_LEN and (produkt_token in token or token in produkt_token):
                return 0.5
    return 0.0


def score_produkt(produkt: str, *texte: str) -> float:
    """0.0 (kein Treffer) bis 1.0 (alle Produkt-Wörter im Artikeltext gefunden)."""
    produkt_tokens = _normalize_tokens(produkt)
    if not produkt_tokens:
        return 0.0
    artikel_tokens: set[str] = set()
    for t in texte:
        artikel_tokens |= _normalize_tokens(t)
    if not artikel_tokens:
        return 0.0
    scores = [_token_score(pt, artikel_tokens) for pt in produkt_tokens]
    return sum(scores) / len(scores)


T = TypeVar("T")


def rank_kandidaten(kandidaten: list[T], produkt_attr: str, *texte: str) -> list[tuple[T, float]]:
    """Sortiert Kandidaten (mit einem `.produkt`-Attribut o.ä.) nach Trefferstärke
    gegen die gegebenen Artikeltexte, absteigend."""
    bewertet = [
        (k, score_produkt(getattr(k, produkt_attr), *texte)) for k in kandidaten
    ]
    bewertet.sort(key=lambda paar: paar[1], reverse=True)
    return bewertet


def rank_produktspezifikationen(
    katalog: list, *texte: str
) -> list[tuple[str, float, list]]:
    """Gruppiert den Produktspezifikationen-Katalog nach eindeutigem `parameter`-
    Namen und bewertet jede Gruppe per Textabgleich gegen die Auslobungen (primär
    `ArtikelDaten.qualitaet`, ergänzend Artikelbezeichnung/Produktklassifizierung).

    Rückgabe: [(parameter, score, [alle Varianten-Zeilen für diesen Parameter]), ...],
    absteigend nach Score sortiert. Innerhalb einer Gruppe ist der Score das
    Maximum über alle Varianten (unterschiedliche `produkt`/`mak_paket`-Zeilen
    desselben Parameters)."""
    gruppen: dict[str, list] = {}
    for eintrag in katalog:
        gruppen.setdefault(eintrag.parameter, []).append(eintrag)

    bewertet = []
    for parameter, varianten in gruppen.items():
        score = score_produkt(parameter, *texte)
        bewertet.append((parameter, score, varianten))
    bewertet.sort(key=lambda tripel: tripel[1], reverse=True)
    return bewertet


# Grobe Kategorien-Zuordnung fürs UI-Gruppieren, übernommen aus dem manuellen
# Beispiel in Preisliste_Mechanik_v2.xlsm!Auswahl (Spalten KÜCHE/TEXTIL/OUTDOOR/
# MATERIAL). Rein zur Anzeige gedacht -- ein Parameter kann in mehreren Kategorien
# auftauchen, unbekannte Parameter landen unter "Sonstige".
PRODUKTSPEZIFIKATION_KATEGORIEN: dict[str, list[str]] = {
    "Küche": [
        "Korrosionsbeständigkeit", "Hitzebeständigkeit", "Kältebeständigkeit",
        "Spülmaschinengeeignet", "Spülmaschinenfest", "Isolationsprüfung Kühlfunktion",
        "Isolationsprüfung Warmhaltung", "Volumenangaben", "Mikrowellengeeignet",
    ],
    "Textil": [
        "UV-Beständigkeit", "UV Schutz (UV Standard 801)", "Wasserabweisung",
        "Wasserdurchlässigkeit, Wassersäule, Wasserdichtheit", "Reibechtheit",
        "Wasserechtheit", "Schweißechtheit", "Waschechtheit", "Lichtechtheit",
        "Meerwasser", "Bügelechtheit", "Echtheit gegen Chlorwasser",
        "Faserzusammensetzung", "Waschbarkeit", "Reißfestigkeit", "Scheuerbeständigkeit",
    ],
    "Outdoor": [
        "Korrosionsbeständigkeit", "UV-Beständigkeit", "Witterungsbeständigkeit",
        "Frostbeständigkeit, Temperaturbeständigkeit", "Kältebeständigkeit",
    ],
    "Material / Sonstiges": [
        "Härteangaben", "Materialangaben", "Berstdruck", "Klebkraft",
        "Vergrößerungsfaktoren", "Traglast (wenn nicht sicherheitsrelevant)",
    ],
}


def kategorie_fuer_parameter(parameter: str) -> str:
    """Erste passende Kategorie für einen Parameter, sonst 'Sonstige'."""
    parameter_norm = parameter.strip()
    for kategorie, parameter_liste in PRODUKTSPEZIFIKATION_KATEGORIEN.items():
        if parameter_norm in parameter_liste:
            return kategorie
    return "Sonstige"


def _hat_batterie(artikel: ArtikelDaten) -> bool:
    wert = (artikel.batterietyp or "").strip().lower()
    return wert not in ("", "keine", "kein", "nein", "-", "none")


def _ist_spielzeug(artikel: ArtikelDaten) -> bool:
    text = f"{artikel.warenbereich} {artikel.artikelkategorie}".lower()
    return "spiel" in text


def _ist_elektrisch(artikel: ArtikelDaten) -> bool:
    text = artikel.warenbereich.lower()
    return "elektro" in text or "e&e" in text or _hat_batterie(artikel)


def bewerte_standardposition(bedingung: str, artikel: ArtikelDaten) -> tuple[bool, str]:
    """Vorauswahl + Begründung für eine feste Standard-Prüfposition (163_PPM,
    1000-1005_PPM, 112_PPM). Heuristiken für 'spielzeug'/'elektrisch' basieren
    auf Textabgleich mit Warenbereich/Artikelkategorie -- unsicherer als die
    anderen Bedingungen, da bislang keine Toy-/E&E-Beispiel-Prüfaufträge vorlagen;
    daher immer manuell prüfbar/änderbar in der UI.

    LFGB (1005_PPM) wird NICHT automatisch erkannt: laut Nutzer wurde das bislang
    manuell in der KV-Monitoringliste gepflegt, 'Chemie / LFGB' im Prüfumfang-Text
    ist dafür kein zuverlässiges Signal (steht praktisch immer dort)."""
    if bedingung == "immer":
        return True, "gilt für alle Produkte"
    if bedingung == "allgemein":
        spezifischer = _ist_spielzeug(artikel) or _ist_elektrisch(artikel)
        if not spezifischer:
            return True, "greift, sofern nicht auch 1005_PPM (Lebensmittelkontakt) zutrifft — ggf. manuell abwählen"
        return False, "entfällt, da eine spezifischere Kennzeichnungsprüfung zutrifft (Spielzeug/elektrisch)"
    if bedingung == "batterie":
        if _hat_batterie(artikel):
            return True, f"Batterietyp im Prüfauftrag: '{artikel.batterietyp}'"
        return False, "kein Batterietyp im Prüfauftrag hinterlegt"
    if bedingung == "spielzeug":
        if _ist_spielzeug(artikel):
            return True, "Warenbereich/Artikelkategorie deutet auf Spielzeug hin"
        return False, "kein Hinweis auf Spielzeug im Warenbereich (bitte manuell prüfen)"
    if bedingung == "elektrisch":
        if _ist_elektrisch(artikel):
            return True, "Warenbereich deutet auf ein elektrisches Produkt hin bzw. Batterietyp vorhanden"
        return False, "kein Hinweis auf ein elektrisches Produkt (bitte manuell prüfen)"
    if bedingung == "lfgb":
        return False, "bislang manuell in der KV-Monitoringliste gepflegt — keine automatische Erkennung, bitte manuell auswählen"
    return False, "unbekannte Bedingung"


# Normangaben in der Mechanik-/Normenauswahl-Datenbank sind immer für eine
# Vollprüfung (100%) hinterlegt. Je nach im Prüfauftrag vorgegebener
# Artikelkategorie wird davon nur ein Teil tatsächlich geprüft -- außer bei
# "Grün*" (trivialer Artikel): dort entfällt die Mechanikprüfung komplett.
ARTIKELKATEGORIE_PRUEFUMFANG: dict[str, tuple[str, str]] = {
    "grün*": ("0%", "Trivialer Artikel (Grün*) — laut Vorgabe keine Mechanikprüfung erforderlich"),
    "grün": ("40%", "Prüfumfang lt. Artikelkategorie 'Grün': 40% der Vollprüfung"),
    "gelb": ("50%", "Prüfumfang lt. Artikelkategorie 'Gelb': 50% der Vollprüfung"),
    "rot": ("60–70%", "Prüfumfang lt. Artikelkategorie 'Rot': 60–70% der Vollprüfung"),
}


def pruefumfang_nach_artikelkategorie(artikelkategorie: str) -> tuple[str, str]:
    """(Umfang-Kürzel, Hinweistext) für die im Prüfauftrag angegebene Artikelkategorie.
    Leere/unbekannte Kategorie -> ("", Hinweis zur manuellen Festlegung)."""
    key = (artikelkategorie or "").strip().lower()
    if key in ARTIKELKATEGORIE_PRUEFUMFANG:
        return ARTIKELKATEGORIE_PRUEFUMFANG[key]
    if not key:
        return "", "Keine Artikelkategorie im Prüfauftrag erkannt — Prüfumfang manuell festlegen"
    return "", f"Unbekannte Artikelkategorie '{artikelkategorie}' — Prüfumfang manuell festlegen"


def ist_trivialer_artikel(artikelkategorie: str) -> bool:
    return (artikelkategorie or "").strip().lower() == "grün*"
