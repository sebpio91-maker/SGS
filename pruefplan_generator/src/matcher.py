"""Regel-Engine: primärer Mechanik-Warengruppen-Match + Normenauswahl-Fallback.

Python-Port der Excel-LET/FILTER-Logik aus Normenauswahl.xlsm!Eingabe.
"""

from __future__ import annotations

import sqlite3

from src.models import MechanikTreffer, NormTreffer, ProduktspezifikationTreffer, StandardPruefposition

NORMEN_KRITERIEN_FELDER = ["kategorie", "produktart", "zielgruppe", "einsatzort", "bereich", "produkt"]
SONDERPOSTEN_KRITERIEN_FELDER = ["kategorie", "produktart", "zielgruppe", "einsatzort"]


def find_mechanik(conn: sqlite3.Connection, warengruppe_code: str) -> list[MechanikTreffer]:
    """Primärpfad: alle Mechanik-Regeln für eine (normalisierte) LIDL-Warengruppe."""
    if not warengruppe_code:
        return []
    rows = conn.execute(
        "SELECT * FROM mechanik_regeln WHERE warengruppe_code = ? ORDER BY produkt",
        (warengruppe_code,),
    ).fetchall()
    return [MechanikTreffer(**dict(r)) for r in rows]


def add_mechanik_regel(
    conn: sqlite3.Connection,
    *,
    lidl_bereich: str,
    lidl_warengruppe: str,
    warengruppe_code: str,
    produkt: str,
    norm_ek_ppm: str,
    anzahl_muster: str = "",
    kosten_vp: float | None = None,
    bemerkungen: str = "",
) -> MechanikTreffer:
    """Legt einen neuen Mechanik-Datensatz an, wenn kein bestehender Katalog-
    Eintrag passt (z.B. neue Warengruppe oder neues Produkt). Landet dauerhaft
    in der Datenbank, damit er bei künftigen Prüfaufträgen mit derselben
    Warengruppe als Vorschlag erscheint."""
    cursor = conn.execute(
        """
        INSERT INTO mechanik_regeln (
            lidl_bereich, lidl_warengruppe, warengruppe_code, produkt,
            bemerkungen, trivial, norm_ek_ppm, anzahl_muster, kez_anforderungen,
            kosten_vp, kosten_tp, ffu, kosten_ffu, stiwa, kosten_stiwa, bewertung_uv
        ) VALUES (?, ?, ?, ?, ?, '', ?, ?, '', ?, NULL, '', NULL, '', NULL, '')
        """,
        (lidl_bereich, lidl_warengruppe, warengruppe_code, produkt, bemerkungen, norm_ek_ppm, anzahl_muster, kosten_vp),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM mechanik_regeln WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return MechanikTreffer(**dict(row))


# Reihenfolge der Prüfumfang-Komponenten-Klassifikation. Schlüsselwörter je
# Kategorie sind disjunkt, daher spielt die Reihenfolge hier keine Rolle.
_KOMPONENTEN_KEYWORDS: list[tuple[str, list[str]]] = [
    ("produktspezifikation", ["produktspezifikation"]),
    ("chemie", ["chemie", "lfgb"]),
    ("selbstauskunft", ["selbstauskunft"]),
    ("ngo", ["ngo"]),
    ("ffu", ["ffu"]),
    ("sicherheit_norm", ["sicherheit", "sonder", "funktionsparameter", "norm"]),
]


def klassifiziere_komponente(text: str) -> str:
    """Ordnet einen Prüfumfang-Bestandteil (z.B. 'Chemie / LFGB') einer groben
    Kategorie zu: 'chemie', 'sicherheit_norm', 'produktspezifikation',
    'selbstauskunft', 'ngo', 'ffu' oder 'sonstige' (unbekannt/nicht abgedeckt,
    z.B. Verpackungs-/Logistikprüfungen aus der 100%-PSI-Phase)."""
    text_norm = text.lower()
    for kategorie, keywords in _KOMPONENTEN_KEYWORDS:
        if any(kw in text_norm for kw in keywords):
            return kategorie
    return "sonstige"


def get_standard_pruefpositionen(conn: sqlite3.Connection) -> list[StandardPruefposition]:
    """Feste Teilprüfungen unter 'Sicherheit & Norm / Sonder- & Funktionsparameter'
    (Kennzeichnung, Akkusicherheit, Bedienungsanleitung, optischer Abgleich)."""
    rows = conn.execute("SELECT * FROM standard_pruefpositionen ORDER BY id").fetchall()
    return [StandardPruefposition(**dict(r)) for r in rows]


def get_produktspezifikation_katalog(conn: sqlite3.Connection) -> list[ProduktspezifikationTreffer]:
    """Alle Zeilen des Materialanforderungskatalogs (Blatt 'Produktspezifikationen')."""
    rows = conn.execute(
        "SELECT * FROM produktspezifikationen ORDER BY parameter, mak_paket, laufzeit"
    ).fetchall()
    return [ProduktspezifikationTreffer(**dict(r)) for r in rows]


def find_normen(conn: sqlite3.Connection, kriterien: dict) -> tuple[str, list[NormTreffer]]:
    """Fallback-Pfad (Port von Eingabe!B14): filtert normen_regeln auf alle
    nicht-leeren Kriterien. Rückgabe: ('none'|'unique'|'ambiguous', Treffer)."""
    where_clauses, params = [], []
    for feld in NORMEN_KRITERIEN_FELDER:
        wert = kriterien.get(feld)
        if wert:
            where_clauses.append(f"{feld} = ?")
            params.append(wert)
    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    rows = conn.execute(f"SELECT * FROM normen_regeln WHERE {where_sql}", params).fetchall()
    treffer = [NormTreffer(**dict(r)) for r in rows]
    if not treffer:
        return "none", []
    if len(treffer) == 1:
        return "unique", treffer
    return "ambiguous", treffer


def get_normen_optionen(conn: sqlite3.Connection, kriterien: dict, feld: str) -> list[str]:
    """Port der dynamischen Dropdown-Arrayformeln (F2:N2 in Eingabe): welche
    Werte sind für `feld` noch wählbar, gegeben die bereits gewählten anderen Kriterien?"""
    andere_felder = [f for f in NORMEN_KRITERIEN_FELDER if f != feld]
    where_clauses, params = [], []
    for f in andere_felder:
        wert = kriterien.get(f)
        if wert:
            where_clauses.append(f"{f} = ?")
            params.append(wert)
    where_clauses.append(f"{feld} <> ''")
    where_sql = " AND ".join(where_clauses)
    rows = conn.execute(
        f"SELECT DISTINCT {feld} FROM normen_regeln WHERE {where_sql} ORDER BY {feld}", params
    ).fetchall()
    return [r[0] for r in rows]


def find_zusatzkosten(conn: sqlite3.Connection, kriterien: dict, eigenschaften: list[str]) -> float:
    """Port von Eingabe!B16 (Sonderposten-Summe): für bis zu 3 gewählte Eigenschaften."""
    eigenschaften = [e for e in eigenschaften if e]
    if not eigenschaften:
        return 0.0
    where_clauses, params = [], []
    for feld in SONDERPOSTEN_KRITERIEN_FELDER:
        wert = kriterien.get(feld)
        if wert:
            where_clauses.append(f"({feld} = ? OR {feld} = '')")
            params.append(wert)
    platzhalter = ",".join("?" for _ in eigenschaften)
    where_clauses.append(f"eigenschaft IN ({platzhalter})")
    params.extend(eigenschaften)
    where_sql = " AND ".join(where_clauses)
    row = conn.execute(f"SELECT SUM(zusatzkosten) AS total FROM sonderposten WHERE {where_sql}", params).fetchone()
    return (row["total"] if row and row["total"] is not None else 0.0)
