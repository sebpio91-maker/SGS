from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ArtikelDaten:
    """Aus einem Prüfauftrag-PDF extrahierte Artikelmerkmale."""

    ian: str = ""
    charge: str = ""
    ian_charge: str = ""  # z.B. "516575_2510"
    artikelbezeichnung: str = ""
    artikelkategorie: str = ""
    ian_vorgaenger: str = ""
    warengruppe: str = ""  # Rohformat aus PDF, z.B. "300.010"
    warengruppe_code: str = ""  # normalisiert, z.B. "300010"
    warenbereich: str = ""
    lieferant: str = ""
    produktklassifizierung: str = ""
    material: str = ""
    materialstaerke: str = ""
    farbe: str = ""
    batterietyp: str = ""
    rf_sicherung: str = ""
    zertifizierungen: str = ""
    herkunftsland: str = ""
    produktionsstaette: str = ""
    qualitaet: str = ""  # Freitext-Block, enthält u.a. die Auslobungen (Style/Set-Angaben)
    pruefumfang: list[str] = field(default_factory=list)
    pruefumfang_komponenten: dict[str, list[str]] = field(default_factory=dict)  # Phase -> ["Chemie / LFGB", ...]
    laender: list[str] = field(default_factory=list)
    quelle_datei: str = ""


@dataclass
class MechanikTreffer:
    """Ein Treffer aus der primären Regel-Tabelle 'mechanik_regeln'."""

    id: int
    lidl_bereich: str
    lidl_warengruppe: str
    warengruppe_code: str
    produkt: str
    bemerkungen: str
    trivial: str
    norm_ek_ppm: str
    anzahl_muster: str
    kez_anforderungen: str
    kosten_vp: float | None
    kosten_tp: float | None
    ffu: str
    kosten_ffu: float | None
    stiwa: str
    kosten_stiwa: float | None
    bewertung_uv: str


@dataclass
class ProduktspezifikationTreffer:
    """Eine Zeile aus dem Materialanforderungskatalog 'produktspezifikationen'."""

    id: int
    parameter: str  # z.B. "Korrosionsbeständigkeit"
    produkt: str  # Kontext/Materialvariante, z.B. "1m³ Kammer"
    mak_paket: str  # Preis-Staffel, z.B. "B1 Paketpreis 1"
    norm: str
    material_code: str
    laufzeit: str
    kosten: float | None
    bewertung: str
    anzahl_proben: str
    gesamtkosten: float | None
    vk_preis: float | None
    pruefstelle: str
    kontakt: str
    bemerkung: str
    materialverkaufstext: str


@dataclass
class StandardPruefposition:
    """Eine feste Teilprüfung unter 'Sicherheit & Norm / Sonder- & Funktionsparameter'
    (Kennzeichnung, Akkusicherheit, Bedienungsanleitung, optischer Abgleich, ...)."""

    id: int
    code: str  # z.B. "1001_PPM"
    bezeichnung: str
    bedingung: str  # 'immer' | 'batterie' | 'spielzeug' | 'elektrisch' | 'lfgb'
    kosten: float | None


@dataclass
class NormTreffer:
    """Ein Treffer aus der Fallback-Regel-Tabelle 'normen_regeln' (Normenauswahl.xlsm)."""

    id: int
    kategorie: str
    produktart: str
    zielgruppe: str
    einsatzort: str
    bereich: str
    produkt: str
    code: str
    lidl_warengruppe: str
    normen: str
    material: str
    verweise: str
    preis: float | None
    laborzeit_min: float | None
    laborkosten: float | None
    bemerkungen: str


@dataclass
class PruefplanPosition:
    """Eine Zeile in der finalen Prüfplan-Positionstabelle."""

    setbestandteil: str  # z.B. "Hauptprodukt", "Teilprodukt 1"
    produkt: str
    pruefung: str  # Norm / EK / PPM-Code bzw. Normen-Text
    anzahl: str
    kosten: float | None
    bemerkung: str = ""
    quelle: str = ""  # "mechanik", "normenauswahl", "produktspezifikation" oder "sonstige"


@dataclass
class PruefplanErgebnis:
    artikel: ArtikelDaten
    positionen: list[PruefplanPosition] = field(default_factory=list)

    @property
    def gesamtkosten(self) -> float:
        return sum(p.kosten for p in self.positionen if p.kosten)
