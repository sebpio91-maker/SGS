# -*- coding: utf-8 -*-
"""Baut aus den Stammdaten des KV-Monitorings eine Excel-Arbeitsmappe.
Die Werte stammen 1:1 aus den Funktionen der Anwendung (siehe dump2.py),
die Block- und Verwendungssummen stehen als Formeln in der Datei, damit sie
sich beim Filtern/Ändern wie im Tool neu berechnen."""
import json, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule, FormulaRule

HIER = pathlib.Path(__file__).resolve().parent
D = json.load(open(HIER / "export.json", encoding="utf-8"))

SCHRIFT = "Arial"
KOPF_FUELL = PatternFill("solid", fgColor="1F3864")
KOPF_FONT = Font(name=SCHRIFT, size=10, bold=True, color="FFFFFF")
ZELL_FONT = Font(name=SCHRIFT, size=10)
TITEL_FONT = Font(name=SCHRIFT, size=14, bold=True, color="1F3864")
GRAU = PatternFill("solid", fgColor="F2F2F2")
GELB = PatternFill("solid", fgColor="FFF2CC")
RAHMEN = Border(bottom=Side(style="thin", color="D9D9D9"))
EUR = '#,##0.00 "€"'

wb = Workbook()

def jn(w):
    return "Ja" if w else "Nein"

def blatt(name, spalten, zeilen, hinweis=None, versteckt=()):
    """spalten: Liste (Überschrift, Breite, Ausrichtung|None, Zahlenformat|None)"""
    ws = wb.create_sheet(name)
    kopfzeile = 1
    if hinweis:
        ws.cell(row=1, column=1, value=hinweis).font = Font(name=SCHRIFT, size=9, italic=True, color="595959")
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(spalten))
        kopfzeile = 2
    for i, (titel, breite, ausr, fmt) in enumerate(spalten, start=1):
        z = ws.cell(row=kopfzeile, column=i, value=titel)
        z.font, z.fill = KOPF_FONT, KOPF_FUELL
        z.alignment = Alignment(vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(i)].width = breite
    ws.row_dimensions[kopfzeile].height = 30
    for r, werte in enumerate(zeilen, start=kopfzeile + 1):
        for c, wert in enumerate(werte, start=1):
            z = ws.cell(row=r, column=c, value=wert)
            z.font = ZELL_FONT
            z.border = RAHMEN
            _, _, ausr, fmt = spalten[c - 1]
            if fmt:
                z.number_format = fmt
            z.alignment = Alignment(vertical="top", wrap_text=True,
                                    horizontal=ausr) if ausr else Alignment(vertical="top", wrap_text=True)
    letzte = kopfzeile + len(zeilen)
    ws.auto_filter.ref = f"A{kopfzeile}:{get_column_letter(len(spalten))}{letzte}"
    ws.freeze_panes = ws.cell(row=kopfzeile + 1, column=1)
    for sp in versteckt:
        ws.column_dimensions[sp].hidden = True
    ws.sheet_view.zoomScale = 100
    return ws, kopfzeile, letzte

# ---------------------------------------------------------------- Normen
n_spalten = [
    ("Norm / Prüfprogramm", 26, None, None), ("Titel", 60, None, None), ("Typ", 10, "center", None),
    ("Prüfungsart", 22, None, None), ("SAP-Code", 20, None, None), ("Preis", 13, "right", EUR),
    ("Kennz.", 8, "center", None), ("BDA", 8, "center", None), ("LIDL-Block", 18, None, None),
    ("Anw.-bereiche", 11, "center", None), ("Anwendungsbereiche", 40, None, None),
    ("Bemerkung", 38, None, None), ("PDF-Datei", 26, None, None), ("Hochgeladen", 13, "center", None),
    ("Volltext", 9, "center", None), ("Verwendet in PG", 13, "center", None), ("ID", 10, None, None),
]
n_zeilen = [[n["bezeichnung"], n["titel"], n["typ"], n["pruefungsart"], n["sapCode"], n["kosten"],
             jn(n["kennzeichnung"]), jn(n["bedienungsanleitung"]), n["lidlBlock"],
             n["anzahlAnwendungsbereiche"], n["anwendungsbereiche"], n["bemerkung"],
             n["dateiname"], n["hochgeladenAm"], jn(n["volltextVorhanden"]), None, n["id"]]
            for n in sorted(D["normen"], key=lambda x: (x["pruefungsart"], x["bezeichnung"]))]
ws_n, kn, ln = blatt("Normen", n_spalten, n_zeilen,
    "Alle Normen und Prüfprogramme aus dem Reiter „Normen“. Kopfzeile filtern/sortieren wie gewohnt; "
    "„Verwendet in PG“ zählt live, in wie vielen Prüfgrundlagen die Norm referenziert ist.",
    versteckt=("Q",))
# Die Zählformel folgt erst nach dem Blatt "Prüfanforderungen" (Zeilenbereich steht dann fest).

# -------------------------------------------------- Norm-Anwendungsbereiche
ab_spalten = [("Norm", 26, None, None), ("Titel der Norm", 55, None, None), ("Prüfungsart", 22, None, None),
              ("Anwendungsbereich", 45, None, None), ("Beschreibung", 55, None, None), ("Preis", 13, "right", EUR)]
ab_zeilen = [[b["norm"], b["normTitel"], b["pruefungsart"], b["name"], b["text"], b["preis"]]
             for b in sorted(D["bereiche"], key=lambda x: (x["norm"], x["name"]))]
blatt("Anwendungsbereiche", ab_spalten, ab_zeilen,
      "Anwendungsbereiche einzelner Normen (z. B. „Filigrane Tische“) mit eigenem Preis — "
      "in der Prüfgrundlage wird je Referenz einer davon ausgewählt.")

# ------------------------------------------------------- Prüfanforderungen
p_spalten = [
    ("Bereich", 16, None, None), ("Warengruppe", 30, None, None), ("Produkt", 28, None, None),
    ("Prüfblock", 22, None, None), ("Prüfungsart", 20, None, None), ("SAP-Code", 20, None, None),
    ("Norm / Prüfprogramm", 26, None, None), ("Titel der Norm", 55, None, None),
    ("in Anlehnung an", 13, "center", None), ("Anwendungsbereich", 28, None, None),
    ("Kosten 1. Prüfung", 15, "right", EUR), ("Kosten je weiterem Produkt", 16, "right", EUR),
    ("Kennz.", 8, "center", None), ("BDA", 8, "center", None), ("Bemerkung zur Norm", 38, None, None),
    ("PG-ID", 10, None, None),
]
p_zeilen = [[p["bereich"], p["warengruppeName"], p["produkt"], p["block"], p["pruefungsart"], p["sapCode"],
             p["norm"], p["normTitel"], jn(p["inAnlehnungAn"]), p["anwendungsbereich"],
             p["kosten"], p["kostenWeiteresProdukt"], jn(p["kennzeichnung"]), jn(p["bedienungsanleitung"]),
             p["bemerkung"], p["pgId"]]
            for p in sorted(D["positionen"], key=lambda x: (x["bereich"], x["warengruppeName"], x["produkt"], x["block"]))]
ws_p, kp, lp = blatt("Prüfanforderungen", p_spalten, p_zeilen,
    "Eine Zeile je geforderter Prüfung: welches Produkt braucht welche Norm, in welchem Block, zu welchem Preis. "
    "Das ist die Arbeitsliste — hier nach Bereich, Warengruppe, Produkt oder Norm filtern. "
    "Leere Kosten = „Preis auf Anfrage“ (gelb).",
    versteckt=("P",))
ws_p.conditional_formatting.add(f"K{kp+1}:K{lp}",
    FormulaRule(formula=[f"ISBLANK($K{kp+1})"], fill=GELB, stopIfTrue=False))

# --------------------------------------------------------- Prüfgrundlagen
g_spalten = [
    ("Bereich", 16, None, None), ("Warengruppe", 30, None, None), ("WG-Code", 10, "center", None),
    ("Produkt", 28, None, None), ("Status", 22, None, None), ("Trivial", 8, "center", None), ("Anzahl Muster", 12, "center", None),
    ("Bearbeitungs-dauer (AT)", 12, "center", None), ("Kennz.", 8, "center", None), ("BDA", 8, "center", None),
    ("Normen Sicherheit/Norm", 40, None, None), ("Summe Sicherheit/Norm", 15, "right", EUR),
    ("Kommentar Sicherheit/Norm", 30, None, None), ("Bemerkungen aus den Normen", 40, None, None),
    ("FFU-Normen", 30, None, None), ("Summe FFU", 13, "right", EUR), ("Kommentar FFU", 26, None, None),
    ("NGO/StiWa-Normen", 30, None, None), ("Summe NGO/StiWa", 14, "right", EUR), ("Kommentar NGO/StiWa", 26, None, None),
    ("Kosten TP", 13, "right", EUR), ("Kosten alt", 13, "right", EUR), ("ID", 10, None, None),
]
# Bezüge bewusst auf die tatsächlichen Datenzeilen begrenzt statt auf ganze Spalten -
# ganze Spalten lassen SUMIFS/COUNTIFS beim Neuberechnen unnötig über eine Million Zeilen laufen.
P_PG   = f"Prüfanforderungen!$P${kp+1}:$P${lp}"
P_BLOCK= f"Prüfanforderungen!$D${kp+1}:$D${lp}"
P_KOST = f"Prüfanforderungen!$K${kp+1}:$K${lp}"
P_NORM = f"Prüfanforderungen!$G${kp+1}:$G${lp}"

def summe_formel(zeile, block):
    """Wie normenBlockSumme(): ohne eine einzige bezifferte Norm gilt „Preis auf Anfrage“,
       sonst die Summe der bekannten Beträge."""
    bed = f'{P_PG},$W{zeile},{P_BLOCK},"{block}"'
    return (f'=IF(COUNTIFS({bed},{P_KOST},">=0")=0,"Preis auf Anfrage",'
            f'SUMIFS({P_KOST},{bed}))')
g_zeilen = []
for g in sorted(D["grundlagen"], key=lambda x: (x["bereich"], x["warengruppeName"], x["produkt"])):
    g_zeilen.append([g["bereich"], g["warengruppeName"], g["warengruppeCode"], g["produkt"], None, jn(g["trivial"]),
                     g["anzahlMuster"], g["bearbeitungsdauerTage"], jn(g["kennzeichnung"]), jn(g["bedienungsanleitung"]),
                     g["normenText"], None, g["normenKommentar"], g["normenBemerkungen"],
                     g["ffuText"], None, g["ffuKommentar"],
                     g["stiwaText"], None, g["stiwaKommentar"],
                     g["kostenTp"], g["kostenAlt"], g["id"]])
ws_g, kg, lg = blatt("Prüfgrundlagen", g_spalten, g_zeilen,
    "Eine Zeile je Produkt: welche Prüfungen gefordert sind, wie viele Muster nötig sind und wie lange es dauert. "
    "Die drei Summenspalten sind Formeln über das Blatt „Prüfanforderungen“ und rechnen sich damit wie im Tool. "
    "Die Spalte „Status“ markiert Produkte ohne zugeordnete Norm und solche mit 0 € Kosten.",
    versteckt=("W",))
for r in range(kg + 1, lg + 1):
    # Zwei Lücken, die beim Durchsehen sonst untergehen: gar keine Norm zugeordnet, oder eine
    # Norm ohne Betrag/mit 0 EUR - beides sieht im Tool nach einem fertigen Eintrag aus.
    ws_g.cell(row=r, column=5, value=f'=IF(COUNTIFS({P_PG},$W{r})=0,"keine Norm hinterlegt",IF($L{r}=0,"0 € hinterlegt",""))')
    ws_g.cell(row=r, column=12, value=summe_formel(r, "Sicherheit-/Normprüfung")).number_format = EUR
    ws_g.cell(row=r, column=16, value=summe_formel(r, "FFU/Fitting")).number_format = EUR
    ws_g.cell(row=r, column=19, value=summe_formel(r, "NGO / StiWa")).number_format = EUR
for text in ('"keine Norm hinterlegt"', '"0 € hinterlegt"'):
    ws_g.conditional_formatting.add(f"E{kg+1}:E{lg}",
        CellIsRule(operator="equal", formula=[text], fill=GELB,
                   font=Font(name=SCHRIFT, size=10, bold=True, color="9C5700")))

for r in range(kn + 1, ln + 1):
    ws_n.cell(row=r, column=16, value=f'=COUNTIF({P_NORM},$A{r})')

# ------------------------------------------------------- MAK-Anforderungen
m_spalten = [
    ("SAP-Code", 20, None, None), ("Kategorie", 22, None, None), ("Bereich", 22, None, None),
    ("Parameter", 34, None, None), ("Anforderung", 55, None, None),
    ("Norm/Standard EU", 28, None, None), ("Norm/Standard US", 28, None, None),
    ("Mindest-Prüfnachweis", 34, None, None), ("Kosten", 13, "right", EUR),
    ("Kosten je weiterem Artikel", 15, "right", EUR), ("Abrechnung", 16, None, None),
    ("Bewertungs-grundlage nötig", 12, "center", None), ("Varianten", 30, None, None),
    ("Bemerkung", 34, None, None), ("Schlagworte", 30, None, None),
]
m_zeilen = [[m["sapCode"], m["kategorie"], m["bereich"], m["parameter"], m["anforderung"],
             m["normEu"], m["normUs"], m["pruefnachweis"], m["kosten"], m["kostenWeiteresArtikel"],
             m["abrechnungsmodus"], jn(m["bewertungsgrundlageErforderlich"]), m["varianten"],
             m["bemerkung"], m["schlagworte"]]
            for m in sorted(D["mak"], key=lambda x: (x["kategorie"], x["bereich"], x["parameter"]))]
blatt("MAK-Anforderungen", m_spalten, m_zeilen,
      "Der LIDL-Materialanforderungskatalog: Anforderung und Mindest-Prüfnachweis je Parameter.")

# ---------------------------------------------------------------- Anleitung
ws = wb["Sheet"]; ws.title = "Anleitung"
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 26
ws.column_dimensions["B"].width = 14
ws.column_dimensions["C"].width = 92
ws["A1"] = "KV-Monitoring — Normen und Prüfanforderungen"; ws["A1"].font = TITEL_FONT
ws["A2"] = "Stand: Stammdaten aus KV-Monitoring.html (Commit dd4251e)"
ws["A2"].font = Font(name=SCHRIFT, size=9, italic=True, color="595959")
kopf = ["Blatt", "Zeilen", "Was drinsteht"]
for i, t in enumerate(kopf, start=1):
    z = ws.cell(row=4, column=i, value=t); z.font, z.fill = KOPF_FONT, KOPF_FUELL
inhalt = [
    ("Normen", len(n_zeilen), "Alle Normen und Prüfprogramme mit Typ, Prüfungsart, SAP-Code, Preis, "
        "Kennzeichnungs-/BDA-Kennzeichen und Bemerkung. „Verwendet in PG“ zählt per Formel, in wie vielen "
        "Prüfgrundlagen die Norm steckt — 0 heißt: nirgends referenziert."),
    ("Anwendungsbereiche", len(ab_zeilen), "Untergliederung einzelner Normen (z. B. „Filigrane Tische“) mit eigenem Preis."),
    ("Prüfanforderungen", len(p_zeilen), "Die Arbeitsliste: eine Zeile je geforderter Prüfung — Produkt × Norm × Prüfblock, "
        "mit Kosten für die 1. Prüfung und je weiterem Produkt. Leere Kosten sind gelb hinterlegt "
        "(im Tool „Preis auf Anfrage“)."),
    ("Prüfgrundlagen", len(g_zeilen), "Eine Zeile je Produkt, mit Anzahl Muster, Bearbeitungsdauer und den drei Blöcken "
        "Sicherheit/Norm, FFU und NGO/StiWa. Die Summenspalten sind Formeln über das Blatt „Prüfanforderungen“. "
        "Die Spalte „Status“ markiert gelb, wo noch etwas fehlt: keine Norm zugeordnet oder 0 € hinterlegt."),
    ("MAK-Anforderungen", len(m_zeilen), "Der LIDL-Materialanforderungskatalog mit Anforderung, Norm EU/US und Mindest-Prüfnachweis."),
]
for r, (a, b, c) in enumerate(inhalt, start=5):
    ws.cell(row=r, column=1, value=a).font = Font(name=SCHRIFT, size=10, bold=True)
    ws.cell(row=r, column=2, value=b).font = ZELL_FONT
    ws.cell(row=r, column=2).alignment = Alignment(horizontal="center", vertical="top")
    z = ws.cell(row=r, column=3, value=c); z.font = ZELL_FONT
    z.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 46
ws["A12"] = "Funktionen in dieser Datei"; ws["A12"].font = Font(name=SCHRIFT, size=11, bold=True, color="1F3864")
hinweise = [
    "Jede Kopfzeile hat einen Autofilter samt Suchfeld — das ersetzt die Filterkette Bereich → Warengruppe → Produkt "
    "und die Volltextsuche des Tools.",
    "Die Kopfzeile ist fixiert; beim Scrollen bleiben die Spaltentitel stehen.",
    "Summen und Zählungen stehen als Formeln (SUMIFS/COUNTIFS) in der Datei, nicht als eingefrorene Werte — "
    "wer eine Kostenzeile ändert, sieht die neue Blocksumme sofort.",
    "„Preis auf Anfrage“ entsteht wie im Tool: hat keine einzige Norm eines Blocks einen Betrag, steht dort kein 0 €, "
    "sondern der Text.",
    "Die technischen IDs stehen in ausgeblendeten Spalten (Normen: Q, Prüfanforderungen: P, Prüfgrundlagen: V). "
    "Sie verknüpfen die Blätter — bitte nicht löschen, sonst brechen die Formeln.",
    "Die Datei ist ein Auszug zum Lesen, Filtern und Weitergeben. Gepflegt wird weiterhin im Tool: "
    "Änderungen hier fließen nicht zurück.",
]
for i, t in enumerate(hinweise):
    r = 13 + i
    ws.cell(row=r, column=1, value="•").font = ZELL_FONT
    z = ws.cell(row=r, column=3, value=t); z.font = ZELL_FONT
    ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=3)
    z.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 30

wb.active = 0
ZIEL = str(HIER.parent / "Normen_und_Pruefanforderungen.xlsx")
wb.save(ZIEL)
print("gespeichert:", ZIEL)
