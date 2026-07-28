# KV-Monitoring (Offline, ohne Installation)

Eine einzelne HTML-Datei zur Verwaltung von Arbeitsvorrat, Prüfaufträgen (PA)
und Kostenvoranschlägen (KV) für mechanische Prüfungen. Läuft komplett im
Browser, ohne Server, ohne Python, ohne Installation, ohne besondere
Berechtigungen — einfach **`KV-Monitoring.html`** doppelklicken.

## Die vier Reiter

- **Arbeitsvorrat** – der Arbeitsvorrat aus dem SAP-Export. Startet leer
  (keine Beispieldaten mehr vorbefüllt) — über
  **„📥 SAP-Export hochladen"** lässt sich der Arbeitsvorrat mit einem neuen
  Excel-Export weiter füllen (unterstützt sowohl den bereits angereicherten
  Export als auch den rohen SAP-Export mit den Spalten Vertriebsbeleg/
  Verkaufsbüro/Bestellnummer/Bezeichnung/Importeur/Angelegt am/
  Sachbearbeiter — die IAN wird in dem Fall automatisch aus der führenden
  Zahl der Bestellnummer abgeleitet). Eine Zeile anklicken (✏️) öffnet sie
  zum Bearbeiten; **„📄" lädt direkt eine PA-PDF für genau dieses Projekt
  hoch** (die IAN steht dabei schon fest und wird nicht erst aus der PDF
  geraten); „+ KV" legt direkt einen neuen Kostenvoranschlag für diese IAN
  an. **VK Büro** wird jetzt als eigene Spalte angezeigt. Die Spalte **„PA"**
  zeigt auf einen Blick, ob zu dieser IAN bereits ein Prüfauftrag hochgeladen
  wurde: liegt einer vor, erscheint ein anklickbares Feld mit dem **Stand der
  PA-PDF** (Datum aus dem Dateinamen bzw. ersatzweise aus dem Seitenfuß der
  PDF), ein Klick springt direkt zum Prüfauftrag; fehlt einer, steht dort nur
  ein „–". Unter der Kopfzeile der Tabelle gibt es **Filter**: IAN als
  Freitextfeld (Teiltreffer); **VK Büro, Lieferant und Warengruppe als
  durchsuchbare Mehrfachauswahl** — anklicken öffnet ein Panel mit Suchfeld
  und Checkbox-Liste, mehrere Werte gleichzeitig ankreuzbar (inkl.
  „Alle"/„Keine" für die gerade sichtbare/gefilterte Liste); Sachbearbeiter,
  LFGB?, Trivial? und Mech. erledigt als einfaches Dropdown. Alles
  kombinierbar, zusätzlich zur Volltextsuche oben. „Filter zurücksetzen"
  setzt alles wieder auf „Alle" zurück.

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
  Sachbearbeiter kommen aus dem SAP-Export. Warengruppe und Anzahl Styles
  kommen bewusst **nicht** aus SAP, sondern — wenn im verknüpften
  Prüfauftrag (PA) vorhanden — von dort; ein SAP-Excel-Upload lässt diese
  Felder daher unangetastet. Sobald zu einer IAN ein PA hochgeladen wird,
  werden sie automatisch befüllt (nur wenn noch leer); über „↺ … aus PA
  übernehmen" (im Bearbeiten-Dialog bzw. auf der PA-Detailseite) lässt sich
  das auch nachträglich/erzwungen anstoßen. **Anzahl Styles** steht in
  keiner PA-PDF als eigenes Feld — sie wird aus der Anzahl unterschiedlicher
  „Style_X"-Blöcke in den Style-Feldern (Maße, Gewicht, …) abgeleitet; ohne
  erkennbare Style-Kennzeichnung wird von einem einzigen Style ausgegangen.
  **LFGB? und Trivial? lassen sich aus der PA-PDF nicht auslesen** (dort
  gibt es dafür kein Feld) und müssen bei der KV-Erstellung manuell gewählt
  werden. „Mech. erledigt" ist nur ein anklickbarer Haken direkt in der
  Tabelle — reiner Status, ob der KV von mechanischer Seite fertig ist. Die
  Muster-Anzahl-Felder und „KV CU" aus der ursprünglichen Excel wurden
  entfernt, da die Musteranzahl erst bei der KV-Erstellung festgelegt wird
  und „KV CU" hier nicht gebraucht wird.
- **Prüfaufträge (PA)** – ein Eintrag pro IAN mit den aus der PA-PDF
  ausgelesenen Feldern. Über **„📄 PA-PDF hochladen"** wird eine Prüfauftrag-PDF
  eingelesen und automatisch (heuristisch) in Schlüssel/Wert-Paare zerlegt;
  vor der Übernahme gibt es eine Prüf-/Korrekturseite. Über **„📄📄 Mehrere
  PA-PDFs hochladen"** lassen sich stattdessen mehrere PDFs auf einmal
  auswählen — hier gibt es *keine* Feld-für-Feld-Prüfseite je Datei, jede
  PDF wird automatisch anhand der erkannten IAN mit dem passenden
  Arbeitsvorrat-Eintrag verknüpft (fehlt ein Treffer, wird trotzdem ein
  Prüfauftrag angelegt). Am Ende erscheint eine Zusammenfassung mit Status
  je Datei (verknüpft/aktualisiert/keine IAN erkannt/Fehler); einzelne
  Prüfaufträge lassen sich danach wie gewohnt in der Liste prüfen und
  korrigieren. Der Rohtext bleibt zum Nachschlagen erhalten. Der **Stand der PDF** (aus dem Dateinamen, z. B.
  „…_Stand_16.07.2026.pdf", ersatzweise aus dem Seitenfuß der PDF) wird
  automatisch erkannt, als Badge oben auf der Detailseite sowie in der
  Prüfauftrag-Liste angezeigt und ist bei Bedarf im Kopf-Formular korrigierbar.
  Die Detailseite eines Prüfauftrags ist in drei Bereiche gegliedert:
  - **Kopfdaten**: IAN/Charge, Warengruppe, Artikelbezeichnung, Artikelkategorie,
    IAN-Vorgänger, Früh. LT, Lieferant, Stand der PDF – direkt editierbar.
  - **Prüfumfang**: der Fließtext-Absatz aus der PDF (30% SPU/QSP, ALT, 100% PSI
    usw.), die **ALT-Zeile ist hervorgehoben**, da sie meist am relevantesten ist.
    Das Institut/Datum-Klammerelement (z. B. „(18.06.2026: SGS Hamburg)") und der
    „bestehend aus"-Verbinder werden für die Anzeige automatisch entfernt, da
    Institut und Datum bereits im Kopf des Prüfauftrags stehen.
  - **Maße, Gewicht, Qualität, Material, Markenreferenz, Garantie**: werden
    **blockweise statt zeilenweise dargestellt** – enthält die PDF
    „Style_A, …:"/„Style_B, …:"-Kennzeichnungen, wird automatisch pro Style ein
    eigener Block gezeigt (z. B. bei einem Artikel mit vier Farb-/Gewichtsvarianten
    vier Blöcke je Feld). Bei einstiligen Artikeln erscheint ein einzelner Block.
    Da das Layout nicht in jeder PDF gleich eindeutig ist, bleibt darunter
    weiterhin die vollständige, editierbare Rohliste aller erkannten Felder als
    Korrekturmöglichkeit erhalten — standardmäßig **eingeklappt** hinter „Alle
    ausgelesenen Felder anzeigen/bearbeiten", da sie im Alltag selten gebraucht
    wird.
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
