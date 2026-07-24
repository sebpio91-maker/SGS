from sqlalchemy import Boolean, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class NormLookupRule(Base):
    """Zuordnung Produktklassifikation → Norm (mechanische Sicherheit).

    Entspricht der "Datenbank"-Tabelle aus dem Normenfinder
    (Normenauswahl.xlsm): eine kaskadierende Klassifikation
    (Kategorie → Produktart → Zielgruppe → Einsatzort → Bereich → Produkt)
    liefert die anzuwendende(n) Norm(en) samt Laborzeit/-kosten und Preis.
    Leere Klassifikationsfelder wirken beim Lookup als Platzhalter (passen
    auf jeden Wert), analog zur Excel-Logik.
    """

    __tablename__ = "norm_lookup_rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    kategorie: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    produktart: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    zielgruppe: Mapped[str | None] = mapped_column(String(255), nullable=True)
    einsatzort: Mapped[str | None] = mapped_column(String(255), nullable=True)
    bereich: Mapped[str | None] = mapped_column(String(255), nullable=True)
    produkt: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(500), unique=True, index=True, nullable=False)
    lidl_warengruppe: Mapped[str | None] = mapped_column(String(255), nullable=True)
    normen: Mapped[str] = mapped_column(String(500), nullable=False)
    material: Mapped[str | None] = mapped_column(String(255), nullable=True)
    verweise: Mapped[str | None] = mapped_column(Text, nullable=True)
    preis: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    zeit_labor_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    kosten_labor: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    bemerkungen: Mapped[str | None] = mapped_column(Text, nullable=True)


class NormSpecialItem(Base):
    """Zusatzkosten/-normen für spezielle Produkteigenschaften
    ("Sonderposten" in Normenauswahl.xlsm), z. B. Armlehne, Glas,
    erhöhtes Nutzergewicht. Leere Klassifikationsfelder gelten als
    Platzhalter (passen auf jede Ausprägung).
    """

    __tablename__ = "norm_special_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    kategorie: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    produktart: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    zielgruppe: Mapped[str | None] = mapped_column(String(255), nullable=True)
    einsatzort: Mapped[str | None] = mapped_column(String(255), nullable=True)
    eigenschaft: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    zusatzkosten: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    kommentar: Mapped[str | None] = mapped_column(Text, nullable=True)


class ProductSpecRequirement(Base):
    """Anforderungskatalog für die (physikalische) Produktspezifikation
    (Produktspezifikationen.xlsx). Pro Prüfparameter (z. B.
    Korrosionsbeständigkeit) und Produkt/Material-Kontext samt Paketstufe
    (`mak`) ist Norm, Laufzeit, Kosten-/Bewertungsformel, Prüflabor und ein
    fertiger Verkaufstext hinterlegt.
    """

    __tablename__ = "product_spec_requirements"

    id: Mapped[int] = mapped_column(primary_key=True)
    parameter: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    produkt: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    mak: Mapped[str | None] = mapped_column(String(100), nullable=True)
    norm: Mapped[str | None] = mapped_column(String(255), nullable=True)
    material_code: Mapped[str | None] = mapped_column(String(255), nullable=True)
    laufzeit: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    formel_laufzeit: Mapped[str | None] = mapped_column(String(500), nullable=True)
    kosten: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    bewertung: Mapped[str | None] = mapped_column(Text, nullable=True)
    anzahl_proben: Mapped[str | None] = mapped_column(String(255), nullable=True)
    formel_bewertung: Mapped[str | None] = mapped_column(String(500), nullable=True)
    kosten_bewertung: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    formel_staffelung: Mapped[str | None] = mapped_column(String(500), nullable=True)
    kosten_staffelung: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    gesamtkosten: Mapped[str | None] = mapped_column(String(255), nullable=True)
    vk_preis: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    pruefstelle: Mapped[str | None] = mapped_column(String(255), nullable=True)
    kontakt: Mapped[str | None] = mapped_column(String(255), nullable=True)
    bemerkung: Mapped[str | None] = mapped_column(Text, nullable=True)
    materialverkaufstext: Mapped[str | None] = mapped_column(Text, nullable=True)


class LidlWarengruppeRule(Base):
    """Regeln je Lidl-Warengruppe für Norm/FFU/StiWa/NGO (aus dem
    "Mechanik"-Blatt der KV_Monitoring-Referenzdatei). Dient als
    Nachschlagewerk für Kosten und Testcodes, wenn die Warengruppe eines
    Produkts bekannt ist; FFU/Referenzprüfung/NGO selbst werden aber
    primär direkt aus dem Lidl-Prüfauftrag übernommen.
    """

    __tablename__ = "lidl_warengruppe_rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    lidl_bereich: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    lidl_warengruppe: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    warengruppe_code: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    produkt: Mapped[str | None] = mapped_column(String(255), nullable=True)
    bemerkungen: Mapped[str | None] = mapped_column(Text, nullable=True)
    trivial: Mapped[bool] = mapped_column(Boolean, default=False)
    norm_ek_ppm: Mapped[str | None] = mapped_column(Text, nullable=True)
    anzahl_muster: Mapped[str | None] = mapped_column(String(100), nullable=True)
    kez_anforderung: Mapped[bool] = mapped_column(Boolean, default=False)
    kosten_vp: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    ffu_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    kosten_ffu: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    stiwa_referenz: Mapped[str | None] = mapped_column(Text, nullable=True)
    kosten_stiwa: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    bewertung_uv: Mapped[str | None] = mapped_column(String(255), nullable=True)
