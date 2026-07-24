import re
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "normenfinder.db"

SCHEMA = """
-- primäre Regel-Tabelle, aus HL_KV_Monitoring...xlsm Blatt "Mechanik"
CREATE TABLE IF NOT EXISTS mechanik_regeln (
    id INTEGER PRIMARY KEY,
    lidl_bereich TEXT,
    lidl_warengruppe TEXT,
    warengruppe_code TEXT,
    produkt TEXT,
    bemerkungen TEXT,
    trivial TEXT,
    norm_ek_ppm TEXT,
    anzahl_muster TEXT,
    kez_anforderungen TEXT,
    kosten_vp REAL,
    kosten_tp REAL,
    ffu TEXT,
    kosten_ffu REAL,
    stiwa TEXT,
    kosten_stiwa REAL,
    bewertung_uv TEXT
);
CREATE INDEX IF NOT EXISTS idx_mechanik_warengruppe_code ON mechanik_regeln(warengruppe_code);

-- Katalog konkreter Prüfparameter ("Materialanforderungskatalog"), aus
-- Preisliste_Mechanik_v2.xlsm Blatt "Produktspezifikationen". Keine feste
-- Warengruppe-Zuordnung -- Auswahl erfolgt über Abgleich mit den Auslobungen
-- im Feld "Qualität" des Prüfauftrags (siehe suggest.rank_produktspezifikationen).
CREATE TABLE IF NOT EXISTS produktspezifikationen (
    id INTEGER PRIMARY KEY,
    parameter TEXT,
    produkt TEXT,
    mak_paket TEXT,
    norm TEXT,
    material_code TEXT,
    laufzeit TEXT,
    kosten REAL,
    bewertung TEXT,
    anzahl_proben TEXT,
    gesamtkosten REAL,
    vk_preis REAL,
    pruefstelle TEXT,
    kontakt TEXT,
    bemerkung TEXT,
    materialverkaufstext TEXT
);
CREATE INDEX IF NOT EXISTS idx_produktspezifikationen_parameter ON produktspezifikationen(parameter);

-- sekundäre Regel-Tabelle (Fallback Möbel/Spielzeug), aus Normenauswahl.xlsm Blatt "Datenbank"
CREATE TABLE IF NOT EXISTS normen_regeln (
    id INTEGER PRIMARY KEY,
    kategorie TEXT,
    produktart TEXT,
    zielgruppe TEXT,
    einsatzort TEXT,
    bereich TEXT,
    produkt TEXT,
    code TEXT UNIQUE,
    lidl_warengruppe TEXT,
    normen TEXT,
    material TEXT,
    verweise TEXT,
    preis REAL,
    laborzeit_min REAL,
    laborkosten REAL,
    bemerkungen TEXT
);

CREATE TABLE IF NOT EXISTS sonderposten (
    id INTEGER PRIMARY KEY,
    kategorie TEXT,
    produktart TEXT,
    zielgruppe TEXT,
    einsatzort TEXT,
    eigenschaft TEXT,
    zusatzkosten REAL,
    kommentar TEXT
);

CREATE TABLE IF NOT EXISTS normen_texte (
    id INTEGER PRIMARY KEY,
    norm_name TEXT,
    kapitel TEXT,
    ueberschrift TEXT,
    pruefungsrelevant TEXT,
    inhalt TEXT
);

CREATE TABLE IF NOT EXISTS warengruppe_mapping (
    warengruppe_code TEXT PRIMARY KEY,
    alte_warengruppe TEXT
);

-- Testkorpus aus Blatt "PA_Database" zur Parser-Validierung
CREATE TABLE IF NOT EXISTS pa_referenzdaten (
    id INTEGER PRIMARY KEY,
    ian_charge TEXT,
    artikelbezeichnung TEXT,
    artikelkategorie TEXT,
    ian_vorgaenger TEXT,
    warengruppe TEXT,
    lieferant TEXT,
    pruefumfang TEXT,
    qualitaet TEXT,
    material TEXT,
    markenreferenz TEXT,
    referenzpruefung TEXT
);

-- Feste Liste an Standard-Teilprüfungen, die laut Nutzer immer unter
-- "Sicherheit & Norm / Sonder- & Funktionsparameter" mitlaufen (Kennzeichnung,
-- Akkusicherheit, Bedienungsanleitung, optischer Abgleich). Nicht aus einer
-- Excel-Quelle migriert, sondern direktes Fachwissen -- Preise noch nicht
-- gepflegt (kosten bleibt NULL, bis der Nutzer sie nachreicht).
CREATE TABLE IF NOT EXISTS standard_pruefpositionen (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    bezeichnung TEXT,
    bedingung TEXT,  -- 'immer' | 'allgemein' | 'batterie' | 'spielzeug' | 'elektrisch' | 'lfgb'
    kosten REAL
);
INSERT OR IGNORE INTO standard_pruefpositionen (code, bezeichnung, bedingung, kosten) VALUES
    ('163_PPM', 'Akkusicherheits-Kurzcheck', 'batterie', NULL),
    ('1001_PPM', 'Verpackung & Produktkennzeichnung (allgemein)', 'allgemein', NULL),
    ('1002_PPM', 'Verpackung & Produktkennzeichnung von Spielzeugen', 'spielzeug', NULL),
    ('1003_PPM', 'Verpackung & Produktkennzeichnung von elektrischen Produkten', 'elektrisch', NULL),
    ('1005_PPM', 'Verpackung & Produktkennzeichnung von Produkten mit Lebensmittelkontakt (LFGB)', 'lfgb', NULL),
    ('1000_PPM', 'Prüfung der Bedienungsanleitung', 'immer', NULL),
    ('112_PPM', 'Optischer Abgleich', 'immer', NULL);
-- Korrektur (nachträglich): 1001_PPM ist der allgemeine Fall, nicht immer --
-- greift nur, wenn keine der spezifischeren Kennzeichnungsprüfungen zutrifft.
-- UPDATE statt erneutem INSERT, da 'code' UNIQUE ist und die Zeile schon
-- existieren kann (idempotent, unabhängig vom Ausführungszeitpunkt).
UPDATE standard_pruefpositionen SET bedingung = 'allgemein' WHERE code = '1001_PPM';
"""


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    conn.commit()


def clear_table(conn: sqlite3.Connection, table: str) -> None:
    conn.execute(f"DELETE FROM {table}")
    conn.commit()


_WARENGRUPPE_RE = re.compile(r"\d[\d.\s]*\d|\d")


def normalize_warengruppe(raw: str) -> str:
    """'300.010' / '300 010' / '370.020 Kohlegrills' / '300010' -> '300010'.

    Nimmt nur die führende Zifferngruppe (inkl. Trennzeichen), damit Text nach
    dem Code (z.B. Produktbezeichnung in der Mechanik-Tabelle) nicht versehentlich
    mit-digitalisiert wird.
    """
    if not raw:
        return ""
    match = _WARENGRUPPE_RE.match(str(raw).strip())
    if not match:
        return ""
    return "".join(ch for ch in match.group(0) if ch.isdigit())
