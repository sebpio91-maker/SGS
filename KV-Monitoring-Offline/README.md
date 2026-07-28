# KV-Monitoring (Offline, ohne Installation)

Eine einzelne HTML-Datei zur Verwaltung von Arbeitsvorrat, Prüfaufträgen (PA)
und Kostenvoranschlägen (KV) für mechanische Prüfungen. Läuft komplett im
Browser, ohne Server, ohne Python, ohne Installation, ohne besondere
Berechtigungen — einfach **`KV-Monitoring.html`** doppelklicken.

## Die vier Reiter

- **Arbeitsvorrat** – der Arbeitsvorrat aus dem SAP-Export. Beim ersten
  Öffnen bereits mit allen 1.230 Zeilen aus der bestehenden
  `HL_KV_Monitoring_PA_ab_SeptMAK.xlsx` (Blatt „Tabelle1") gefüllt. Über
  **„📥 SAP-Export hochladen"** lässt sich der Arbeitsvorrat mit einem neuen
  Excel-Export weiter füllen (unterstützt sowohl den bereits angereicherten
  Export als auch den rohen SAP-Export mit den Spalten Vertriebsbeleg/
  Verkaufsbüro/Bestellnummer/Bezeichnung/Importeur/Angelegt am/
  Sachbearbeiter — die IAN wird in dem Fall automatisch aus der führenden
  Zahl der Bestellnummer abgeleitet). Eine Zeile anklicken (✏️) öffnet sie
  zum Bearbeiten; **„📄" lädt direkt eine PA-PDF für genau dieses Projekt
  hoch** (die IAN steht dabei schon fest und wird nicht erst aus der PDF
  geraten); „+ KV" legt direkt einen neuen Kostenvoranschlag für diese IAN
  an. **VK Büro** wird jetzt als eigene Spalte angezeigt. Unter der
  Kopfzeile der Tabelle gibt es **Filter**: IAN als Freitextfeld
  (Teiltreffer); **VK Büro, Lieferant und Warengruppe als durchsuchbare
  Mehrfachauswahl** — anklicken öffnet ein Panel mit Suchfeld und
  Checkbox-Liste, mehrere Werte gleichzeitig ankreuzbar (inkl. „Alle"/„Keine"
  für die gerade sichtbare/gefilterte Liste); Sachbearbeiter, LFGB?,
  Trivial? und Mech. erledigt als einfaches Dropdown. Alles kombinierbar,
  zusätzlich zur Volltextsuche oben. „Filter zurücksetzen" setzt alles
  wieder auf „Alle" zurück.

  **VK Büro wird vereinheitlicht:** „0070", „070" und „70" gelten als
  derselbe Wert (führende Nullen werden ignoriert) — sowohl bei der Anzeige
  und im Filter als auch beim Excel-Upload und beim Duplikat-Abgleich. Der
  rohe SAP-Export liefert das Verkaufsbüro z. B. als „0070", die bereits
  angereicherte Monitoring-Tabelle als „70" — beide landen als „70" im
  Arbeitsvorrat.

  **Warengruppe wird immer als „###.###" dargestellt** (z. B. „385030" oder
  „385.030" → „385.030"), egal wie sie ursprünglich eingetragen/aus dem PA
  übernommen wurde — in der Tabelle, im Filter und im CSV-Export. Werte, die
  nicht aus genau 6 Ziffern bestehen, werden unverändert gelassen statt
  geraten.

  **Datenherkunft je Feld:** Bezeichnung, Lieferant, Angelegt am und
  Sachbearbeiter kommen aus dem SAP-Export. Warengruppe, Anzahl Styles,
  LFGB? und Trivial? kommen bewusst **nicht** aus SAP, sondern — wenn im
  verknüpften Prüfauftrag (PA) vorhanden — von dort; ein SAP-Excel-Upload
  lässt diese vier Felder daher unangetastet. Sobald zu einer IAN ein PA
  hochgeladen wird, werden sie automatisch befüllt (nur wenn noch leer);
  über „↺ … aus PA übernehmen" (im Bearbeiten-Dialog bzw. auf der
  PA-Detailseite) lässt sich das auch nachträglich/erzwungen anstoßen.
  „Mech. erledigt" ist nur ein anklickbarer Haken direkt in der Tabelle —
  reiner Status, ob der KV von mechanischer Seite fertig ist. Die
  Muster-Anzahl-Felder und „KV CU" aus der ursprünglichen Excel wurden
  entfernt, da die Musteranzahl erst bei der KV-Erstellung festgelegt wird
  und „KV CU" hier nicht gebraucht wird.
- **Prüfaufträge (PA)** – ein Eintrag pro IAN mit den aus der PA-PDF
  ausgelesenen Feldern. Über **„📄 PA-PDF hochladen"** wird eine Prüfauftrag-PDF
  eingelesen und automatisch (heuristisch) in Schlüssel/Wert-Paare zerlegt;
  vor der Übernahme gibt es eine Prüf-/Korrekturseite. Der Rohtext bleibt zum
  Nachschlagen erhalten.
- **Kostenvoranschläge (KV)** – das Herzstück: pro IAN ein KV mit
  Stammdaten und einer Tabelle mechanischer Prüfpositionen (Kategorie,
  Bezeichnung, Kürzel, SAP-Code, Kosten, Anzahl, Summe, aktiv/inaktiv).
  Positionen lassen sich aus dem Katalog übernehmen (Kosten/SAP-Code werden
  vorausgefüllt) oder frei anlegen. **„⧉ Als Vorlage für neuen KV
  duplizieren"** kopiert einen bestehenden KV (z. B. eines Wiederholartikels)
  als Ausgangspunkt für einen neuen. Über die Suche oben lassen sich
  bestehende KVs nach IAN/Artikel/Warengruppe/Lieferant durchsuchen, um einen
  passenden zum Duplizieren zu finden.
- **Prüfpositionen-Katalog** – die wiederverwendbaren mechanischen
  Prüfpositionen mit Standardkosten und SAP-Code, vorbefüllt aus der
  bestehenden KV-Vorlage. Hier pflegen, wenn sich Preise ändern oder neue
  Prüfarten dazukommen.

## Toolbar (oben, bereichsübergreifend)

- **⬇ Sichern (JSON)** / **⬆ Datei laden (JSON)** – kompletter Stand
  (Arbeitsvorrat + PA + KV + Katalog) als Datei sichern bzw. laden.
- **🔀 Zusammenführen (JSON)** – Arbeitsstände mehrerer Personen/Rechner
  zusammenführen, mit Konfliktanzeige ("Aktuell behalten" / "Aus Datei
  übernehmen") für alle vier Bereiche.
- **📄 CSV-Export** – exportiert die Tabelle des gerade offenen Reiters als
  `.csv`, direkt in Excel öffenbar.

Alle Änderungen werden automatisch im Browser (Local Storage) auf diesem PC
gespeichert. Für Backup/Weitergabe/Zusammenführen über mehrere Rechner die
JSON-Funktionen benutzen.

## Wichtig: Excel-Upload und Duplikate

Der Arbeitsvorrat-Upload prüft neue Zeilen gegen bestehende IANs. Kommt eine
IAN bereits vor und die Werte unterscheiden sich, erscheint pro betroffener
IAN eine Vergleichsansicht ("Aktuell behalten" / "Aus Datei übernehmen") —
das sollte laut Beschreibung normalerweise nicht vorkommen, ist aber als
Sicherheitsnetz eingebaut. Gibt es keine Abweichungen, werden neue Zeilen
ohne Rückfrage direkt hinzugefügt.

## Bewusst so gelöst / nicht enthalten

- **Nur mechanische Prüfungen.** Chemie/LFGB, PSI, Verpackung etc. aus der
  ursprünglichen KV-Vorlage sind bewusst nicht abgebildet — das war die
  ausdrückliche Vorgabe für diesen ersten Schritt.
- **Wiederverwendung ist manuell.** Es gibt (noch) keine automatische
  "ähnliche Projekte"-Vorschlagsfunktion — über Suche + "Als Vorlage
  duplizieren" hat man volle Kontrolle, welcher alte KV als Basis dient.
- **PA-Erkennung ist Best-Effort.** Die PDF-Struktur ist nicht 100 %
  einheitlich (z. B. bei mehreren Styles); erkannte Felder deshalb vor dem
  Übernehmen prüfen. Nicht erkannte/falsch zugeordnete Informationen lassen
  sich in der Review-Ansicht oder danach direkt in der Felder-Tabelle
  korrigieren.
- **Verknüpfung PA ↔ KV** läuft ausschließlich über die IAN (Freitext-Feld,
  keine feste ID-Kopplung), damit auch KVs ohne (noch) vorhandene PA
  funktionieren.

## Technisch

Eine einzelne Datei, keine Internetverbindung nötig. Enthält eingebettet:
[SheetJS/xlsx](https://github.com/SheetJS/sheetjs) (Excel-Import) und
[pdf.js](https://mozilla.github.io/pdf.js/) (PDF-Text-Extraktion) — beide
komplett offline, keine Daten verlassen den Rechner.
