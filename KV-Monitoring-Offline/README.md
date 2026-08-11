# KV-Monitoring (Offline, ohne Installation)

Eine einzelne HTML-Datei zur Verwaltung von Arbeitsvorrat, Prüfaufträgen (PA)
und Kostenvoranschlägen (KV) für mechanische Prüfungen. Läuft komplett im
Browser, ohne Server, ohne Python, ohne Installation, ohne besondere
Berechtigungen — einfach **`KV-Monitoring.html`** doppelklicken.

## Die sieben Reiter

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
  werden — dort jeweils als einfaches **Ja/Nein-Dropdown** statt Freitext.
  „Mech. erledigt" ist nur ein anklickbarer Haken direkt in der
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
  Arbeitsvorrat-Eintrag verknüpft. **Existiert zu der erkannten IAN noch kein
  Arbeitsvorrat-Eintrag, wird automatisch ein neuer angelegt** (befüllt mit
  IAN, Bezeichnung, Lieferant und „Angelegt am" aus der PA-PDF; alles
  Weitere bleibt leer und ist im Reiter „Arbeitsvorrat" wie gewohnt
  nachpflegbar, z. B. sobald der SAP-Export nachgeliefert wird) — so
  „verwaisen" hochgeladene PAs nie ohne zugehörigen Arbeitsvorrat. Das gilt
  sowohl für den Mehrfach-Upload als auch für den Einzel-Upload mit
  Prüf-/Korrekturseite. Am Ende erscheint eine Zusammenfassung mit Status
  je Datei (verknüpft/automatisch neu angelegter Arbeitsvorrat/aktualisiert/
  keine IAN erkannt/Fehler); einzelne Prüfaufträge lassen sich danach wie
  gewohnt in der Liste prüfen und korrigieren. Der Rohtext bleibt zum
  Nachschlagen erhalten. Der **Stand der PDF** (aus dem Dateinamen, z. B.
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
  Bezeichnung, Kürzel, SAP-Code, Kosten, Anzahl, Summe, aktiv/inaktiv). Die
  **Überschrift zeigt bevorzugt die Artikelbezeichnung aus dem verknüpften
  Prüfauftrag** (aussagekräftiger als die bloße IAN) — ohne verknüpften PA
  fällt sie auf das freie „Artikel"-Feld des KVs zurück, erst danach auf
  „KV <IAN>"; die IAN selbst bleibt daneben immer als Badge sichtbar.
  **Zwischen KV und Prüfauftrag lässt sich in beide Richtungen direkt
  springen**: „→ Verknüpften Prüfauftrag anzeigen" im KV wechselt zum
  passenden Prüfauftrag, „→ Verknüpften Kostenvoranschlag anzeigen" auf der
  Prüfauftrags-Detailseite wieder zurück — praktisch, um bei Bedarf schnell
  genauere Informationen auf der jeweils anderen Seite nachzuschlagen, ohne
  über die Liste suchen zu müssen. Beide Buttons erscheinen nur, wenn zur
  IAN tatsächlich ein Gegenstück existiert. Auch
  hier erscheint — sofern der verknüpfte Prüfauftrag eine „IAN-Vorgänger"
  enthält — dieselbe Vorgänger-Artikel-Karte wie bei den Prüfaufträgen,
  ergänzt um **„↺ Prüfpositionen aus Vorgänger-KV übernehmen"**: kopiert alle
  aktiven Positionen des Vorgänger-KVs (mit dessen tatsächlichen Kosten/
  Anzahl, nicht den Katalog-Standardwerten) in den aktuellen KV; bereits
  vorhandene Positionen werden dabei übersprungen, ein zweiter Klick legt also
  nichts doppelt an.

  **Warengruppe (neu) ist ein durchsuchbares Dropdown** (dieselbe Liste wie
  im Reiter „Prüfgrundlagen"/„Verwaltung") und wird **automatisch aus dem
  verknüpften Prüfauftrag übernommen**, sobald zur IAN ein PA vorliegt (nur
  wenn im KV noch leer — eine bewusste manuelle Auswahl wird nie ohne
  Nachfrage überschrieben). Taucht der aus dem PA gelesene Code noch nicht in
  der Warengruppen-Liste auf, wird er automatisch als neuer Platzhalter-
  Eintrag ergänzt, damit das Dropdown nie einen unbekannten Wert „stumm"
  anzeigt. **„↺ Warengruppe/Styleanzahl aus PA übernehmen"** erzwingt bei
  Bedarf die Neu-Übernahme, auch wenn bereits manuell etwas anderes gewählt
  wurde. **Styleanzahl** wird nach demselben Prinzip automatisch aus der
  Anzahl der im PA erkannten „Style_X"-Blöcke übernommen (fällt kein Style
  auf, wird von einem einzigen ausgegangen).

  **Warengruppe (alt)** bleibt vorerst ein Freitextfeld, wird aber
  automatisch befüllt, sobald in der Neu-↔-Alt-Zuordnungstabelle (Reiter
  „Verwaltung", siehe unten) ein passender Eintrag zur gewählten Warengruppe
  (neu) existiert — auch das nur, wenn das Feld noch leer ist. Die
  Zuordnungsliste selbst startet leer, bis die offizielle Zuordnung
  (ADMIN-Blatt) vorliegt; bis dahin bleibt „Warengruppe (alt)" manuell
  pflegbar.

  Im Abschnitt **(Physikalische-) Produktspezifikationen** wird zusätzlich
  die aus dem PA ausgelesene **„Qualität"** informativ angezeigt (analog zur
  bereits vorhandenen Markenreferenz-Anzeige) — praktisch als schneller
  Blick auf die Materialangaben, ohne extra zum Prüfauftrag wechseln zu
  müssen.

  **Warengruppen-Empfehlung (Mechanik)** – die primäre Vorschlagsquelle,
  wie besprochen **zuerst nach Warengruppe, dann nach Produkt**: sobald
  „Warengruppe (neu)" gesetzt ist, wird in einer echten, vom Team gepflegten
  Referenztabelle (185 Zeilen aus der Mechanik-Preisliste) nachgeschlagen.
  Gibt es zu der Warengruppe mehrere Produkte (z. B. „370.030 Grillzubehör"
  → Feuerzeug, Grillbürsten, Anzündkamin, …), erscheint eine Auswahlliste;
  bei genau einem Treffer wird er direkt angezeigt (Hauptprodukt). Für das
  gewählte Produkt zeigt die Karte Norm, Anzahl Muster, Besonderheiten
  (Bemerkungen, Trivial-/KEZ-Kennzeichnung) sowie – falls vorhanden – FFU
  und NGO/StiWa mit den tatsächlich hinterlegten Kosten, jeweils mit
  „+ hinzufügen" direkt in die Prüfpositionen-Tabelle. Gibt es zur
  Warengruppe keine Referenzdaten, erscheint direkt in der Karte
  **„+ Neue Prüfgrundlage für Warengruppe … anlegen"** — öffnet denselben
  Anlage-Dialog wie im Reiter „Prüfgrundlagen", mit der Warengruppe schon
  vorbelegt; nach dem Speichern zeigt die Karte sofort den neuen Treffer,
  ohne den Tab wechseln zu müssen. Bis dahin bleibt zusätzlich die manuelle
  Auswahl unten verfügbar.

  Die Position **„Sicherheit & Norm"** wird als eine **kombinierte Position**
  gebildet, nachgebaut aus dem Auswahl_LIDL-Arbeitsblatt (siehe unten):
  - **Set-Bestandteile**: über „Weiteren Set-Bestandteil hinzufügen" (bei
    mehrteiligen Produkten, z. B. Messer + Messerblock) lässt sich die
    Referenztabelle **warengruppenübergreifend** nach weiteren
    Produkten durchsuchen (z. B. „Messer" zu einem Hauptprodukt
    „Messerblock") — praktisch für mehrteilige Produkte, bei denen jeder
    Bestandteil eine eigene Norm/eigene Kosten hat. Jeder hinzugefügte
    Bestandteil erscheint als entfernbarer Chip; Norm-Text und Kosten aller
    Bestandteile (Hauptprodukt + Set-Bestandteile) werden zu einer einzigen
    Position zusammengefasst.
  - **Artikelkategorie-Rabattfaktor**: die Summe der Sicherheit & Norm-Kosten
    wird automatisch mit einem Faktor je nach Artikelkategorie des
    verknüpften Prüfauftrags multipliziert — **Grün → 0,3, Gelb → 0,5,
    sonst/unbekannt → 0,7**. Der verwendete Faktor und die erkannte
    Artikelkategorie werden direkt unter der Position angezeigt. Hinweis:
    das Original vergleicht die Artikelkategorie exakt (nur „Grün"); da
    reale Prüfaufträge auch Werte wie „Grün*" liefern, wird hier bewusst
    normalisiert verglichen (ohne Sonderzeichen, Groß-/Kleinschreibung
    egal), damit der Rabatt auch bei solchen Varianten korrekt greift.

  FFU- und NGO/StiWa-Kosten sind vom Rabattfaktor **nicht** betroffen (im
  Original eigenständige Positionen ohne Set-Bestandteile/Rabatt).

  **Artikelkategorie** – direkt oberhalb des Prüfumfangs zeigt eine eigene
  Karte die Artikelkategorie aus dem verknüpften Prüfauftrag (dieselbe, die
  auch den Rabattfaktor der Sicherheit & Norm-Position bestimmt, siehe
  unten) — auf einen Blick sichtbar statt nur beiläufig im
  Rabattfaktor-Hinweis erwähnt. Ohne hinterlegte Artikelkategorie im
  Prüfauftrag erscheint stattdessen ein entsprechender Hinweis.

  **Prüfumfang** – der rohe Prüfumfang-Text aus dem verknüpften Prüfauftrag
  wird jetzt auch im KV angezeigt, in derselben Darstellung wie auf der
  Prüfauftrags-Detailseite (ALT-Zeile hervorgehoben, Institut/Datum-Klammer
  entfernt) — kein Wechsel zum Prüfauftrag mehr nötig, um nachzusehen, was
  dort genau drinsteht. Direkt darunter folgt die Checkliste der fünf
  mechanisch relevanten Prüfumfang-Abschnitte. Jede Checkbox ist so lange
  automatisch aus dem Prüfumfang des verknüpften Prüfauftrags vorbelegt
  (Badge „im Prüfumfang erkannt"/„nicht erkannt"), bis sie einmal manuell
  angeklickt wird — danach bleibt genau diese manuelle Wahl dauerhaft für
  den KV gespeichert, auch über einen Prüfauftrags-Wechsel hinweg.
  Chemie/LFGB und Selbstauskunft tauchen hier gar nicht erst auf, da beide
  nicht Teil dieses mechanischen KVs sind. Die fünf Abschnitte sind
  bewusst **genauso benannt, wie sie im Prüfauftrag stehen**:
  - **Sicherheit & Norm / Sonder- & Funktionsparameter**
  - **(Physikalische-) Produktspezifikationen**
  - **FFU/Fitting**
  - **NGO**
  - **Referenzprüfung**

  **„Sicherheit & Norm / Sonder- & Funktionsparameter" ist zusätzlich in
  vier eigene Unterpunkte gegliedert**, jeder mit eigener Checkbox statt
  einer einzigen für den ganzen Abschnitt — und jeder mit eigener
  Vorbelegungs-Regel statt der reinen Prüfumfang-Text-Erkennung:
  - **Sicherheit-/Normprüfung** – Pflicht, außer der Artikel ist
    **Trivial="Ja"** oder die **Artikelkategorie ist Grün\***; ist die
    Artikelkategorie Grün\*, aber FFU, NGO oder Referenzprüfung sind für
    denselben Artikel gefordert (deren Checkboxen oben angehakt), bleibt
    sie trotzdem Pflicht. Entspricht dem Katalog-Eintrag „Sicherheit-/
    Normprüfung Teilprüfung EK5/AK5 06-01.3:2011".
  - **Kennzeichnung (Verpackung & Produkt)** – **immer Pflicht**, unabhängig
    von Prüfumfang, Artikelkategorie oder Trivial, und deshalb immer
    vorbelegt. Es gibt dafür vier Katalog-Varianten mit demselben Zweck,
    aber unterschiedlichem PPM-Code — automatisch als Vorschlag markiert
    wird genau die zum KV passende: **1001_PPM** (Standard/VK Büro 0070),
    **1002_PPM** (VK Büro 0049), **1003_PPM** (VK Büro 0072), **1005_PPM**
    (sobald LFGB="Ja" — hat Vorrang vor der VK-Büro-Zuordnung). Die übrigen
    drei Varianten bleiben in der Detail-Karte sichtbar und bei Bedarf
    manuell hinzufügbar.
  - **Kennzeichnung (Bedienungsanleitung)** – folgt weiterhin der
    Prüfumfang-Text-Erkennung wie bisher. Entspricht immer dem
    Katalog-Eintrag „Bedienungsanleitung E&E (1000_PPM)".
  - **Optischer Abgleich** – folgt ebenfalls weiterhin der
    Prüfumfang-Text-Erkennung. Entspricht immer dem Katalog-Eintrag
    „Optischer Abgleich (112_PPM)".

  Alle vier lassen sich unabhängig voneinander manuell an- und abhaken,
  unabhängig von ihrer jeweiligen Vorbelegungs-Regel — z. B. wenn im
  Einzelfall nur der optische Abgleich, nicht aber die Kennzeichnungsprüfung
  benötigt wird. Jeder Unterpunkt steuert direkt, ob die zugehörige
  Katalog-Position in der Detail-Karte unten als „Vorschlag" markiert ist.
  Dateien aus einer älteren Tool-Version (ein einzelnes Häkchen für den
  ganzen Abschnitt bzw. nur die eine „1001_PPM"-Kennzeichnungs-Position)
  werden beim Laden automatisch migriert/ergänzt, damit kein bereits
  gepflegter KV plötzlich Positionen verliert.

  **Erst für angehakte Abschnitte/Unterpunkte erscheinen darunter die
  einzelnen Prüfpositionen** zur Auswahl (Karte „Prüfumfang-Details") — ist
  nichts angehakt, bleibt nur die Checkliste sichtbar. Ohne verknüpften
  Prüfauftrag startet die Checkliste komplett unangehakt, lässt sich aber
  jederzeit manuell aktivieren (z. B. um Positionen schon vor dem
  PA-Upload grob vorzubereiten). Innerhalb der Detail-Karten:
  - **Sicherheit & Norm / Sonder- & Funktionsparameter**: die allgemeinen
    Katalog-Positionen zu den vier Unterpunkten oben werden automatisch als
    „Vorschlag" markiert, ergänzend zur produktspezifischen Empfehlung
    oben. Der **Akkusicherheitskurzcheck** wird davon unabhängig nur
    vorgeschlagen, wenn das aus dem Prüfauftrag ausgelesene Feld
    „Batterietyp" auf eine tatsächlich vorhandene Batterie/einen Akku
    hindeutet (nicht „keine"/„nein"/leer). **Mustereinlagerung (18
    Monate)** wird im Prüfumfang nicht mehr angezeigt (weder als Vorschlag
    noch manuell hinzufügbar) — bleibt aber im Reiter
    „Prüfpositionen-Katalog" erhalten und ist dort weiterhin klassisch über
    das Katalog-Dropdown im KV auswählbar, falls im Einzelfall doch
    gebraucht.
  - **(Physikalische-) Produktspezifikationen**: durchsuchbare Liste aus dem
    echten, 62 Einträge umfassenden Parameterkatalog (Parameter, Material/
    Kontext, Laufzeit, Norm, SAP-Code, Preis) — Suchfeld oben, „+ hinzufügen"
    trägt die gewählte Zeile mit ihrem tatsächlichen Preis und SAP-Code ein.
    Eine automatische Zuordnung nach Auslobungen ist noch nicht hinterlegt.
    Die **Qualität** aus dem Prüfauftrag wird hier direkt darüber angezeigt
    — genauso als eigene Style-Blöcke aufgeteilt wie auf der
    Prüfauftrags-Detailseite (siehe unten), statt als ein zusammenhängender
    Text.
  - **FFU/Fitting** und **NGO**: die allgemeinen Katalog-Positionen werden
    vorgeschlagen, sobald im Prüfumfang erkannt — produktspezifische Kosten
    dafür liefert, wenn vorhanden, die Warengruppen-Empfehlung oben.
  - **Referenzprüfung**: zeigt zusätzlich die „Markenreferenz" aus dem
    Prüfauftrag an (das Referenzprodukt, gegen das verglichen wird).

  Bei jeder Detail-Karte lässt sich per **„+ hinzufügen"** eine
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
- **Prüfgrundlagen** – die Datenquelle der Warengruppen-Empfehlung im KV
  (siehe oben) ist **direkt in der Oberfläche bearbeitbar und neu anlegbar**,
  nicht mehr nur fest eingebettet. Zuerst nach **Warengruppe** gruppiert
  (auf-/zuklappbar), darunter nach **Produkt** sortiert. Die Übersichtszeile
  je Produkt zeigt nur das Nötigste (Produkt, Normen, Kosten Sicherheit &
  Norm, Anzahl Muster, KEZ-Badge, ob FFU/StiWa hinterlegt sind) — der
  Warengruppen-Code selbst wird hier bewusst **nicht** als eigene Spalte
  angezeigt (steht ja schon im Gruppenkopf), ist aber weiterhin die Basis für
  die Zuordnung. **Auf eine Zeile klicken** (oder ✏️) öffnet die
  Detailansicht zum Bearbeiten; **„+ Neue Prüfgrundlage"** öffnet sie leer.
  Änderungen werden erst mit „Speichern" übernommen — „Abbrechen" verwirft
  sie wieder vollständig, inklusive aller Normen-Referenzen. Sobald die
  Warengruppe gespeichert wird, wandert der Eintrag automatisch in die
  passende (neue oder bestehende) Gruppe.

  **Warengruppe wird nur noch per durchsuchbarem Dropdown gewählt**, kein
  Freitext mehr — Klick öffnet die vollständige Liste, Tippen filtert nach
  Code oder Name (Code wird nicht mehr doppelt angezeigt, da er im Namen
  bereits enthalten ist). Die Liste ist anfangs aus den 64 in den
  Prüfgrundlagen-Startdaten vorkommenden Warengruppen abgeleitet, aber wie
  Bereich (siehe unten) über den Reiter **„Verwaltung"** frei pflegbar —
  neue Warengruppen anlegen, Code/Name bestehender ändern oder welche
  löschen, bis die offizielle Warengruppen-Liste geliefert wird.

  **Bereich ist ebenfalls ein durchsuchbares Dropdown**, kein Freitext mehr
  — genau wie Warengruppe gibt es hier **kein "+ Neue anlegen" direkt aus
  der Prüfgrundlage heraus**; beide Listen werden ausschließlich im neuen
  Reiter **„Verwaltung"** gepflegt (anlegen, umbenennen, löschen), damit sie
  nicht durch beiläufige Freitext-Varianten wuchern. Dateien aus einer
  älteren Tool-Version (Bereich als Freitext) werden migriert: jeder
  bislang verwendete Wert, der noch nicht in der gepflegten Liste steht,
  wird beim Laden automatisch ergänzt.

  **Normen sind jetzt eine durchsuchbare Dropdown-Mehrfachauswahl, die auf
  echte Norm-Datensätze verweist** (Reiter „Normen", siehe unten) statt auf
  Freitext — der Button „+ Norm hinzufügen" öffnet die Normendatenbank zum
  Durchblättern, Tippen filtert; „+ Neue Norm „…" anlegen" legt bei Bedarf
  sofort eine neue Norm an (auch schon vor dem Speichern der
  Prüfgrundlage). Je ausgewählter Norm lässt sich zusätzlich
  **„in Anlehnung an"** ankreuzen, falls sie nicht vollständig anwendbar ist.
  Diese Normen-Auswahl gibt es jetzt für alle drei Prüfblöcke — **Sicherheit
  & Norm, FFU/Fitting und NGO/StiWa** —, die vorherigen reinen
  Freitext-Hinweise bei FFU/StiWa sind entsprechend entfallen. Das frühere,
  separate „Kennzeichnung über GPSR hinaus"-Feld war inhaltlich dasselbe wie
  **KEZ-Anforderungen** und wurde deshalb zu einem einzigen Kästchen
  zusammengeführt (Tooltip erklärt die GPSR-Bedeutung).

  Jedes der drei Dropdowns ist auf den jeweils passenden Normen-**Typ**
  eingeschränkt, damit man nicht versehentlich eine Norm im falschen Block
  auswählt: **Sicherheit & Norm** zeigt nur externe Normen und interne
  Prüfprogramme (Typ „Norm" und „PPM"), **FFU/Fitting** nur
  FFU-Prüfprogramme (Typ „PPM_FFU") und **NGO/StiWa** nur StiWa-Programme
  (Typ „StiWa"). Legt man über „+ Neue Norm „…" anlegen" direkt aus einem
  dieser Blöcke heraus eine neue Norm an, bekommt sie automatisch einen zum
  jeweiligen Block passenden Typ (z. B. immer „PPM_FFU" im FFU-Block),
  unabhängig davon, wie die Bezeichnung geschätzt worden wäre. Bereits
  ausgewählte Normen (Chips) bleiben unabhängig vom Typ immer sichtbar —
  die Einschränkung gilt nur für die Such-/Browse-Liste beim Hinzufügen.

  **Die Kosten werden jetzt je Norm hinterlegt statt einmal pauschal pro
  Block**, jeweils in **ganzen Euro-Schritten** (Feld „Kosten €" mit
  Schrittweite 1). Direkt darunter zeigt jeder der drei Blöcke (Sicherheit &
  Norm, FFU/Fitting, NGO/StiWa) live die **Summe** der eingetragenen
  Einzelkosten. Ist für keine der ausgewählten Normen ein Betrag hinterlegt,
  zeigt die Summe „Preis auf Anfrage" (genau wie zuvor beim einzelnen
  Blockfeld); einzelne unbezifferte Normen neben bezifferten tragen einfach 0
  zur Summe bei. Diese Summe ist es auch, die in der Warengruppen-Empfehlung
  im KV-Reiter (inkl. Set-Bestandteile und Rabattfaktor) sowie im CSV-Export
  verwendet wird. Dateien aus einer älteren Tool-Version (ein einzelner
  Kostenbetrag pro Block) werden beim Laden/Zusammenführen automatisch
  migriert: der alte Gesamtbetrag landet vollständig auf der ersten Norm der
  jeweiligen Liste, damit die Summe exakt erhalten bleibt — eine feinere
  Aufteilung auf mehrere Normen ist danach manuell in der Detailansicht
  möglich.

  **Bemerkungen hängen an der Norm/dem PPM selbst statt pauschal am ganzen
  Produkt.** Die Bemerkung ist ein Feld der Norm in der Normendatenbank
  (Reiter „Normen", siehe unten) — nicht der Prüfgrundlage und nicht der
  einzelnen Referenz. Dadurch bleibt sie konsistent, egal in wie vielen
  Prüfgrundlagen dieselbe Norm verwendet wird: einmal gepflegt (z. B.
  „Gasgeräteverordnung! CE-Zeichen! KE nötig." bei einer bestimmten Norm),
  überall sichtbar. Bearbeiten geht an **beiden Stellen** — direkt am
  Normen-Eintrag in einer Prüfgrundlage (schreibt sofort in die
  Normendatenbank, ohne dass die Prüfgrundlage gespeichert werden muss) oder
  im Reiter „Normen" selbst; beide zeigen denselben, gemeinsamen Text.
  Projektspezifische Hinweise, die sich nicht auf die Norm im Allgemeinen,
  sondern auf ein konkretes Projekt beziehen (z. B. „Der Artikel ist in Bezug
  auf [Schnittleistung] mindestens gleichwertig mit [Vergleichsprodukt]" bei
  einer StiWa-Prüfung), gehören dagegen ins bereits vorhandene freie
  Notizfeld des jeweiligen Kostenvoranschlags, nicht in dieses
  normübergreifend geteilte Feld. Dateien aus einer älteren Tool-Version
  (eine einzelne Bemerkung pro Prüfgrundlage, zwischenzeitlich auch eine
  Bemerkung je Referenz) werden automatisch auf die Norm migriert: der Text
  landet auf der ersten referenzierten Norm (bevorzugt aus Sicherheit & Norm,
  sonst FFU, sonst StiWa); treffen für dieselbe Norm mehrere unterschiedliche
  Alttexte zusammen, werden sie durch „ | " getrennt zusammengeführt statt
  einander zu überschreiben.

  **Materialien sind aus den Prüfgrundlagen entfernt** — sie hängen vom
  jeweiligen Projekt ab und gehören nicht in diese produktübergreifende
  Referenztabelle. Stattdessen zeigt die Detailansicht jetzt eine
  schreibgeschützte **„Verwendet in Projekten"-Übersicht**: alle
  Kostenvoranschläge, die diese Prüfgrundlage als Hauptprodukt oder
  Set-Bestandteil verwenden, mit Klick-Sprung zum jeweiligen KV. **Normen-/
  Prüfprogramm-Dokumente werden nicht mehr hier, sondern ausschließlich im
  Reiter „Normen" hochgeladen** (siehe unten).

  Über die Suche oben lässt sich nach Warengruppe, Produkt, Norm oder
  Bemerkung filtern. Änderungen wirken sich sofort auf die
  Warengruppen-Empfehlung im KV-Reiter aus. Auch bei **⬇ Sichern/⬆ Laden
  (JSON)**, **🔀 Zusammenführen** und **📄 CSV-Export** wie die übrigen
  Reiter behandelt (Zusammenführen erkennt gleiche Einträge an
  Warengruppen-Code + Produkt). Dateien aus einer älteren Tool-Version
  (einzeiliges Norm-Feld, separates Kennzeichnung-Feld, Materialien,
  Freitext-FFU/StiWa-Hinweise) werden beim Laden/Zusammenführen automatisch
  auf die neue Form migriert — dabei wird für jeden bisherigen Freitext-Wert
  automatisch eine passende Norm im Reiter „Normen" angelegt (bzw.
  wiederverwendet, falls schon vorhanden), damit keine Information verloren
  geht.
- **Normen** – eigenständige Verwaltung einzelner Normen, im Listen-/
  Detail-Layout wie bei Prüfaufträgen/KVs, und jetzt direkt mit den
  Prüfgrundlagen verknüpft (siehe oben). Über **„📄 Norm(en)/Prüfprogramm(e)
  hochladen"** lassen sich eine oder mehrere **.docx**-Dateien auf einmal
  hochladen — jede Datei legt eine eigene Norm an (Bezeichnung anfangs aus
  dem Dateinamen abgeleitet, danach frei editierbar). Wie überall beim
  Datei-Upload in diesem Tool wird nur der ausgelesene Text gespeichert,
  nicht die Datei selbst. **PDF-Upload wurde entfernt** — Normen werden
  entweder manuell angelegt oder per .docx hochgeladen. Der komplette
  Rohtext der Datei bleibt einsehbar (durchsuchbar per Strg+F wie jeder
  andere Text auf der Seite); „.docx erneut hochladen" ersetzt nur den
  Rohtext, vorhandene Anwendungsbereiche (siehe unten) bleiben unangetastet.
  Alte **.doc-Dateien** (Format vor Office 2007) werden nicht unterstützt —
  hierfür bitte eine .docx-Version hochladen.

  **Anwendungsbereiche**: manche Normen stellen je nach Verwendungszweck des
  Produkts unterschiedliche Anforderungen — z. B. hat DIN EN 581-2
  unterschiedliche Anforderungen für Camping-, Wohn- und Objektbereich. Über
  „+ Anwendungsbereich hinzufügen" lässt sich pro Norm eine beliebige Anzahl
  solcher Bereiche anlegen (freier Name, z. B. „Campingbereich", plus
  Freitext für die dort geltenden Anforderungen) — frei bearbeitbar,
  zusammenführbar, löschbar, unabhängig von einer festen Klausel-Nummerierung
  der Norm. Diese Anwendungsbereiche lassen sich dann **direkt bei der
  jeweiligen Norm-Referenz in den Prüfgrundlagen auswählen**: hat eine
  referenzierte Norm Anwendungsbereiche definiert, erscheint dort automatisch
  ein zusätzliches Dropdown („— kein bestimmter Bereich —" oder einer der
  definierten Bereiche); Normen ohne Anwendungsbereiche zeigen kein Dropdown.

  Die Detailansicht einer Norm zeigt außerdem eine schreibgeschützte
  **„Verwendet in Prüfgrundlagen"-Übersicht**: für jede Prüfgrundlage, die
  diese Norm in einem ihrer drei Prüfblöcke referenziert, eine Zeile mit
  Produkt, Warengruppe, Block (Sicherheit & Norm/FFU/StiWa), dem dort
  **ausgewählten Anwendungsbereich** (Spalte erscheint nur, wenn die Norm
  welche definiert hat) und den dort **je Produkt hinterlegten Kosten** —
  Kosten hängen ja an der jeweiligen Prüfgrundlage, nicht an der Norm selbst
  (siehe „Kosten je Norm" oben), so ist auf einen Blick sichtbar, wie sich
  Anwendungsbereich und Kosten für dieselbe Norm über verschiedene Produkte
  unterscheiden. Klick auf eine Zeile springt direkt zur Detailansicht der
  jeweiligen Prüfgrundlage.

  Jede Norm hat einen **Typ** — „Norm (extern)" für echte Regelwerke
  (DIN/EN/ISO) oder eine von drei internen Kategorien: **Prüfprogramm
  (PPM)**, **FFU-Prüfprogramm (PPM_FFU)** oder **StiWa-Programm** — als
  eigene Sammlung der jeweiligen internen Prüfprogramm-Kürzel, getrennt von
  den externen Normen. Der Typ wird beim Anlegen automatisch anhand der
  Bezeichnung geschätzt (z. B. „163_PPM_FFU" → FFU-Prüfprogramm, „StiWa
  06/2014" → StiWa-Programm, alles andere → Norm) und lässt sich in der
  Detailansicht per Dropdown korrigieren. Über der Normen-Liste lässt sich
  per Umschalter („Alle" / „Normen" / „PPM" / „PPM_FFU" / „StiWa") gezielt
  nach Typ filtern; jeder Eintrag zeigt sein Kürzel als Badge, auch in der
  Normen-Auswahl bei den Prüfgrundlagen.

  Jede Norm hat außerdem ein eigenes **Bemerkungsfeld** — bearbeitbar sowohl
  hier in der Detailansicht als auch direkt am jeweiligen Normen-Eintrag in
  jeder Prüfgrundlage, die diese Norm verwendet (siehe oben); beide Stellen
  zeigen und ändern denselben Text.

  Wird eine Norm gelöscht, auf die eine Prüfgrundlage noch verweist,
  erscheint dort „(gelöschte Norm)" statt der Bezeichnung — die Referenz
  bleibt technisch bestehen, sollte aber in der Prüfgrundlage entfernt oder
  ersetzt werden.
- **Verwaltung** – Pflege von drei Stammdaten-Listen:
  - **Bereiche** – Dropdown-Quelle im Reiter „Prüfgrundlagen". Neue Werte
    anlegen, bestehende umbenennen (aktualisiert automatisch alle
    Prüfgrundlagen, die den bisherigen Wert verwenden) oder löschen (mit
    Warnhinweis, falls der Wert noch verwendet wird); die Anzahl der
    Verwendungen steht neben jedem Eintrag.
  - **Warengruppen** – Dropdown-Quelle sowohl im Reiter „Prüfgrundlagen" als
    auch bei „Warengruppe (neu)" im Kostenvoranschlag, mit zwei Feldern je
    Eintrag (Code und Name). Ändern von Code oder Name aktualisiert
    automatisch alle Prüfgrundlagen und Kostenvoranschläge mit dem
    bisherigen Code; Löschen warnt ebenfalls bei noch bestehender
    Verwendung. Ersetzt die bisher rein aus den Prüfgrundlagen-Startdaten
    abgeleitete, nicht editierbare Liste (siehe unten) — die 64 Startwerte
    sind hier jetzt frei pflegbar, bis die offizielle Warengruppen-Liste
    geliefert wird. Wird im PA eine noch unbekannte Warengruppe gelesen und
    automatisch in einen KV übernommen, landet sie ebenfalls automatisch
    hier als Platzhalter-Eintrag (Code = Name), statt das Dropdown mit
    einem unbekannten Wert leer zu lassen.
  - **Warengruppen-Zuordnung (Neu → Alt)** – ordnet einer neuen Warengruppe
    (Code) den passenden Alt-Wert zu; sobald hier ein Eintrag existiert,
    befüllt er automatisch „Warengruppe (alt)" im Kostenvoranschlag (nur
    wenn dort noch leer). Startet leer — die vollständige, offizielle
    Zuordnungstabelle (ADMIN-Blatt, 347 Zeilen) lässt sich hier nach und
    nach eintragen, sobald sie vorliegt (siehe auch unten).

## Datenquelle der Warengruppen-Empfehlung und SAP-Codes

Die Warengruppen-Mechanik-Referenz (185 Zeilen, jetzt der Reiter
„Prüfgrundlagen") und der Produktspezifikationen-Parameterkatalog (62 Zeilen)
stammen ursprünglich aus `Preisliste_Mechanik_v2.xlsm` (Blätter „Mechanik" und
„Produktspezifikationen") und sind der **Startbestand** beim allerersten
Öffnen des Tools. Die Prüfgrundlagen sind seitdem über den gleichnamigen
Reiter bearbeit- und erweiterbar (siehe oben); der Produktspezifikationen-
Katalog ist weiterhin nur durchsuchbar, nicht editierbar — bei Bedarf bitte
Bescheid geben, dann wird das analog nachgerüstet. Dabei wurden auch die
SAP-Codes im Prüfpositionen-Katalog gegen die reale SAP-Bestellzeilen-Liste
(Blatt „SAP") korrigiert — u. a. „MECH_SICHERHEIT_TS" statt der zuvor
angenommenen „MECH_S_NORM_TS", und „FFU_TS" als gemeinsamer Code für
Optischer Abgleich/FFU/Referenzprüfung/NGO.

Die **Set-Bestandteile- und Rabattfaktor-Logik** der Sicherheit & Norm-Position
ist aus `Preisliste_Hilfe_claude.xlsm` (Blatt „Auswahl_LIDL", dort die
Formeln/Verknüpfungen rund um die Tabelle „Setbestandteile" sowie die
Gesamtkosten-Formel `SUMME(Kosten VP) × (Grün:0,3 | Gelb:0,5 | sonst:0,7)`)
nachgebaut — bewusst vereinfacht auf eine dynamische Liste statt der starren
5 Zeilen (1 Hauptprodukt + 4 Teilprodukte) im Original. Die dortige
„Mechanik"-Tabelle selbst (206 Zeilen) hatte keine befüllte Kosten-Spalte und
diente nur zur Absicherung der Warengruppen-/Produktstruktur — Kostenquelle
bleibt `Preisliste_Mechanik_v2.xlsm`. Noch nicht übernommen: eine Lockerung
der Prüfumfang-Schlüsselwort-Erkennung auf das dort verwendete, einfachere
Teilstring-Prinzip.

Die Neue-↔-Alte-Warengruppe-Zuordnungstabelle vom ADMIN-Blatt (347 Zeilen)
wäre die naheliegende Quelle für die vollständige, offizielle
Warengruppen-Liste im Dropdown bei Prüfgrundlagen/Kostenvoranschlag (aktuell
ein 64-Einträge-Startbestand aus den bereits genutzten Warengruppen) —
bislang aber noch nicht dafür verwendet, da unklar war, welche der beiden
Spalten (Neu/Alt) als Code+Name-Paar für die Auswahl taugt. Anders als
früher braucht das aber keine neue Tool-Version mehr: die Warengruppen-Liste
selbst lässt sich direkt im Reiter „Verwaltung" pflegen (siehe oben) — die
offizielle Liste könnte dort bei Bedarf auch komplett von Hand nachgetragen
werden. Für die reine **Neu→Alt-Zuordnung** (unabhängig von der
Warengruppen-Liste) gibt es dort inzwischen eine eigene, noch leere Tabelle
(„Warengruppen-Zuordnung (Neu → Alt)"), die „Warengruppe (alt)" im
Kostenvoranschlag automatisch befüllt, sobald ein passender Eintrag vorliegt
— auch hier wartet die vollständige ADMIN-Blatt-Liste noch auf manuelles
Eintragen.

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
