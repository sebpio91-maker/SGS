# KV-Monitoring (Offline, ohne Installation)

Eine einzelne HTML-Datei zur Verwaltung von Arbeitsvorrat, Prüfaufträgen (PA)
und Kostenvoranschlägen (KV) für mechanische Prüfungen. Läuft komplett im
Browser, ohne Server, ohne Python, ohne Installation, ohne besondere
Berechtigungen — einfach **`KV-Monitoring.html`** doppelklicken.

## Die vier Reiter

- **Arbeitsvorrat** – der Arbeitsvorrat aus dem SAP-Export. Startet leer
  (keine Beispieldaten mehr vorbefüllt). Oben lässt sich zwischen zwei
  **Ansichten** umschalten: **„Arbeitsvorrat (offene Mechanik)"** (Standard)
  zeigt nur Einträge, bei denen „Mech. erledigt" noch nicht gesetzt ist —
  der eigentliche Tagesarbeitsvorrat; **„Gesamtliste (alle jemals
  hochgeladenen)"** zeigt wirklich alle Einträge unabhängig vom
  Mech.-Status, als Archiv/Nachschlagewerk. Beide Ansichten teilen sich alle
  übrigen Filter; „Filter zurücksetzen" leert diese, lässt aber die gewählte
  Ansicht unangetastet. Über
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
    vier Blöcke je Feld). Manche PAs benennen Varianten stattdessen mit einem
    HG-Code (z. B. „HG09747A") direkt am Zeilenanfang statt mit „Style_…:" —
    auch das wird erkannt, unabhängig davon, ob der HG-Code als eigene
    Kopfzeile steht oder direkt gefolgt vom Wert (mit oder ohne Doppelpunkt)
    in derselben Zeile. Bei einstiligen Artikeln erscheint ein einzelner Block.
    Da das Layout nicht in jeder PDF gleich eindeutig ist, bleibt darunter
    weiterhin die vollständige, editierbare Rohliste aller erkannten Felder als
    Korrekturmöglichkeit erhalten — standardmäßig **eingeklappt** hinter „Alle
    ausgelesenen Felder anzeigen/bearbeiten", da sie im Alltag selten gebraucht
    wird.
  - **Vorgänger-Artikel**: steht in der PA-PDF eine „IAN-Vorgänger", erscheint
    eine eigene Karte mit 🔍-Suchlink für diese Vorgänger-IAN. Liegt zu ihr
    bereits ein Prüfauftrag und/oder KV im System vor, gibt es zusätzlich
    Sprung-Buttons direkt dorthin — praktisch bei der KV-Erstellung, da sich
    Daten des Vorgängers oft als Ausgangspunkt übernehmen lassen (vor
    Übernahme aber immer prüfen, ob sich seitdem etwas geändert hat). Gibt es
    keinen Treffer im System, bleibt nur der SharePoint-Suchlink. Liegt der
    Vorgänger-Prüfauftrag im System vor, gibt es zusätzlich **„Vergleich mit
    Vorgänger anzeigen"** — eine eingeklappte Tabelle, die Warengruppe,
    Artikelbezeichnung, Artikelkategorie, Früh. LT, Lieferant, Prüfumfang,
    Anzahl Styles sowie die Style-Blockfelder (Maße, Gewicht, Qualität,
    Material, Markenreferenz, Garantie) aktuell gegen Vorgänger stellt und
    abweichende Zeilen (⚠, gelb hinterlegt) von gleichen (✓) unterscheidet —
    so sieht man auf einen Blick, was sich seit dem Vorgänger geändert hat.
- **Kostenvoranschläge (KV)** – das Herzstück: pro IAN ein KV mit
  Stammdaten und einer Tabelle mechanischer Prüfpositionen (Kategorie,
  Bezeichnung, Kürzel, SAP-Code, Kosten, Anzahl, Summe, aktiv/inaktiv). Auch
  hier erscheint — sofern der verknüpfte Prüfauftrag eine „IAN-Vorgänger"
  enthält — dieselbe Vorgänger-Artikel-Karte wie bei den Prüfaufträgen,
  ergänzt um **„↺ Prüfpositionen aus Vorgänger-KV übernehmen"**: kopiert alle
  aktiven Positionen des Vorgänger-KVs (mit dessen tatsächlichen Kosten/
  Anzahl, nicht den Katalog-Standardwerten) in den aktuellen KV; bereits
  vorhandene Positionen werden dabei übersprungen, ein zweiter Klick legt also
  nichts doppelt an.

  **Warengruppen-Empfehlung (Mechanik)** – die primäre Vorschlagsquelle,
  wie besprochen **zuerst nach Warengruppe, dann nach Produkt**: sobald
  „Warengruppe (neu)" gesetzt ist, wird in einer echten, vom Team gepflegten
  Referenztabelle (205 Zeilen aus der Mechanik-Preisliste) nachgeschlagen.
  Gibt es zu der Warengruppe mehrere Produkte (z. B. „370.030 Grillzubehör"
  → Feuerzeug, Grillbürsten, Anzündkamin, …), erscheint eine Auswahlliste;
  bei genau einem Treffer wird er direkt angezeigt. Für das gewählte Produkt
  zeigt die Karte Norm, Anzahl Muster, Besonderheiten (Bemerkungen,
  Trivial-/KEZ-Kennzeichnung) sowie die **tatsächlich hinterlegten Kosten**
  für Sicherheit & Norm sowie – falls vorhanden – FFU und NGO/StiWa, jeweils
  mit „+ hinzufügen" direkt in die Prüfpositionen-Tabelle. Gibt es zur
  Warengruppe keine Referenzdaten, bleibt nur die manuelle Auswahl unten.

  **Prüfumfang-Übersicht** – ergänzend dazu, automatisch aus dem Prüfumfang
  des verknüpften Prüfauftrags erkannt („im Prüfumfang" bzw. „nicht
  erkannt"):
  - **Chemie / LFGB** und **Selbstauskunft** erscheinen nur informativ —
    beide sind bewusst nicht Teil dieses mechanischen KVs.
  - **Sicherheit & Norm / Sonder- & Funktionsparameter**: die allgemeinen
    Katalog-Positionen (Kennzeichnung, BDA, optischer Abgleich,
    Mustereinlagerung) werden automatisch als „Vorschlag" markiert – ergänzend
    zur produktspezifischen Empfehlung oben. Der **Akkusicherheitskurzcheck**
    wird dabei nur vorgeschlagen, wenn das aus dem Prüfauftrag ausgelesene
    Feld „Batterietyp" auf eine tatsächlich vorhandene Batterie/einen Akku
    hindeutet (nicht „keine"/„nein"/leer).
  - **(Physikalische-) Produktspezifikationen**: durchsuchbare Liste aus dem
    echten, 62 Einträge umfassenden Parameterkatalog (Parameter, Material/
    Kontext, Laufzeit, Norm, SAP-Code, Preis) — Suchfeld oben, „+ hinzufügen"
    trägt die gewählte Zeile mit ihrem tatsächlichen Preis und SAP-Code ein.
    Eine automatische Zuordnung nach Auslobungen ist noch nicht hinterlegt.
  - **FFU/Fitting** und **NGO**: die allgemeinen Katalog-Positionen werden
    vorgeschlagen, sobald im Prüfumfang erkannt — produktspezifische Kosten
    dafür liefert, wenn vorhanden, die Warengruppen-Empfehlung oben.
  - **Referenzprüfung**: zeigt zusätzlich die „Markenreferenz" aus dem
    Prüfauftrag an (das Referenzprodukt, gegen das verglichen wird).

  Bei jeder relevanten Kategorie lässt sich per **„+ hinzufügen"** eine
  einzelne Position oder per **„Alle Vorschläge übernehmen"** alle markierten
  Positionen auf einmal in die Prüfpositionen-Tabelle unten eintragen — dort
  dann wie gewohnt Kosten/Anzahl anpassen, deaktivieren oder entfernen.
  Positionen lassen sich außerdem klassisch aus dem Katalog-Dropdown
  übernehmen (Kosten/SAP-Code werden vorausgefüllt) oder frei anlegen.
  **„⧉ Als Vorlage für neuen KV duplizieren"** kopiert einen bestehenden KV
  (z. B. eines Wiederholartikels) komplett als Ausgangspunkt für einen
  neuen. Über die Suche oben lassen sich bestehende KVs nach
  IAN/Artikel/Warengruppe/Lieferant durchsuchen, um einen passenden zum
  Duplizieren zu finden.
- **Prüfpositionen-Katalog** – die wiederverwendbaren mechanischen
  Prüfpositionen mit Standardkosten und SAP-Code, vorbefüllt aus der
  bestehenden KV-Vorlage. Hier pflegen, wenn sich Preise ändern oder neue
  Prüfarten dazukommen.

## Datenquelle der Warengruppen-Empfehlung und SAP-Codes

Die Warengruppen-Mechanik-Referenz (205 Zeilen) und der Produktspezifikationen-
Parameterkatalog (62 Zeilen) stammen aus `Preisliste_Mechanik_v2.xlsm`
(Blätter „Mechanik" und „Produktspezifikationen"). Es sind feste Referenzdaten,
die beim Bauen der Datei mit eingebettet werden — keine Bearbeitung über die
Oberfläche, kein Autosave. Sollen sich Preise/Normen/Produkte ändern oder neue
Warengruppen dazukommen, bitte die aktualisierte Excel-Datei erneut schicken,
dann wird eine neue Version des Tools damit gebaut. Dabei wurden auch die
SAP-Codes im Prüfpositionen-Katalog gegen die reale SAP-Bestellzeilen-Liste
(Blatt „SAP") korrigiert — u. a. „MECH_SICHERHEIT_TS" statt der zuvor
angenommenen „MECH_S_NORM_TS", und „FFU_TS" als gemeinsamer Code für
Optischer Abgleich/FFU/Referenzprüfung/NGO.

## SharePoint-Suche nach IAN

Neben jeder IAN (in der Arbeitsvorrat-Tabelle sowie auf den Detailseiten von
Prüfaufträgen und Kostenvoranschlägen) steht ein kleines 🔍-Symbol. Ein Klick
öffnet in einem neuen Tab die SharePoint-Suche
(`https://sgs.sharepoint.com/sites/de-cp-hamfiles/_layouts/15/search.aspx/siteall`)
direkt mit dieser IAN als Suchbegriff — praktisch, um schnell vorhandene
Unterlagen zu dieser IAN zu finden. Ohne IAN erscheint kein Symbol.

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
ohne Rückfrage direkt hinzugefügt. Oben in dieser Vergleichsansicht gibt es
**„Alle: Aktuell behalten"** und **„Alle: Aus Datei übernehmen"** — setzt die
Auswahl für alle angezeigten IANs auf einmal; einzelne IANs lassen sich
danach trotzdem noch per Klick anders entscheiden, bevor „Entscheidungen
anwenden" die endgültige Auswahl übernimmt.

**IAN wird beim Abgleich vereinheitlicht:** wie VK Büro wird auch die IAN
unabhängig von führenden Nullen behandelt (z. B. "070123" und "70123" gelten
als dieselbe IAN) — sowohl direkt aus einer IAN-Spalte als auch aus der
führenden Zahl der Bestellnummer abgeleitet. Damit werden Zeilen aus
unterschiedlich formatierten Exporten korrekt demselben Arbeitsvorrat-Eintrag
zugeordnet, statt versehentlich als neue Duplikate angelegt zu werden.

**„Angelegt am" zeigt jetzt immer das korrekte Kalenderdatum**, unabhängig
von der Zeitzone des Rechners. Ursache war ein verbreiteter Excel-Import-Bug:
Datums-Zellen werden als lokale Mitternacht eingelesen, aber bislang über
`toISOString()` (UTC) in Text umgewandelt — das ließ das Datum in Zeitzonen
östlich von UTC (z. B. Europe/Berlin) einen Tag zu früh erscheinen. Betrifft
auch das „Erstellt am"-Datum neuer Kostenvoranschläge.

Nach jedem Upload wechselt die Ansicht automatisch auf **„Gesamtliste"** —
so bleiben frisch importierte Zeilen immer sichtbar, auch wenn einzelne davon
bereits als „Mech. erledigt" markiert sind (die in der Ansicht „Arbeitsvorrat"
sonst ausgeblendet wären).

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
