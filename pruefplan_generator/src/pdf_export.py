"""PDF-Export des Prüfplans: lesbarer Report mit Kopfdaten, Positionstabelle
und Gesamtsumme (reportlab)."""

from __future__ import annotations

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from src.models import PruefplanErgebnis


def build_pdf(ergebnis: PruefplanErgebnis) -> bytes:
    artikel = ergebnis.artikel
    styles = getSampleStyleSheet()
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.5 * cm, bottomMargin=1.5 * cm
    )
    story = []

    story.append(Paragraph("Prüfplan", styles["Title"]))
    story.append(Spacer(1, 10))

    kopf_felder = [
        ("IAN_Charge", artikel.ian_charge),
        ("Artikelbezeichnung", artikel.artikelbezeichnung),
        ("Bereich", artikel.warenbereich),
        ("Warengruppe", artikel.warengruppe),
        ("Artikelkategorie", artikel.artikelkategorie),
        ("Lieferant", artikel.lieferant),
        ("Herkunftsland", artikel.herkunftsland),
        ("Prüfumfang (Prüfauftrag)", ", ".join(artikel.pruefumfang)),
    ]
    kopf_data = [[Paragraph(f"<b>{label}</b>", styles["Normal"]), Paragraph(str(value), styles["Normal"])] for label, value in kopf_felder]
    kopf_table = Table(kopf_data, colWidths=[5 * cm, 11 * cm])
    kopf_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(kopf_table)
    story.append(Spacer(1, 16))

    story.append(Paragraph("Prüfpositionen", styles["Heading2"]))
    header = ["Setbestandteil", "Produkt", "Prüfung", "Anzahl", "Kosten [EUR]"]
    pos_data = [header]
    for pos in ergebnis.positionen:
        pos_data.append(
            [
                pos.setbestandteil,
                pos.produkt,
                Paragraph(pos.pruefung or "", styles["Normal"]),
                pos.anzahl,
                f"{pos.kosten:.2f}" if pos.kosten is not None else "",
            ]
        )
    pos_data.append(["", "", "", "Gesamtkosten", f"{ergebnis.gesamtkosten:.2f}"])

    pos_table = Table(pos_data, colWidths=[3 * cm, 3.5 * cm, 6.5 * cm, 1.8 * cm, 2.2 * cm], repeatRows=1)
    pos_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dddddd")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
            ]
        )
    )
    story.append(pos_table)

    doc.build(story)
    return buf.getvalue()


def export_file(ergebnis: PruefplanErgebnis, path: str) -> None:
    data = build_pdf(ergebnis)
    with open(path, "wb") as f:
        f.write(data)
