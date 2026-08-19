# KV-Monitoring (Offline, ohne Installation)

Eine einzelne HTML-Datei zur Verwaltung von Arbeitsvorrat, Prüfaufträgen (PA)
und Kostenvoranschlägen (KV) für mechanische Prüfungen. Läuft komplett im
Browser, ohne Server, ohne Python, ohne Installation, ohne besondere
Berechtigungen — einfach **`KV-Monitoring.html`** doppelklicken.

## Die sechs Reiter

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
  geraten); **„+ KV" legt einen neuen Kostenvoranschlag für diese IAN an —
  existiert zu dieser IAN aber bereits einer, wird KEIN Duplikat angelegt**,
  sondern direkt zum vorhandenen KV gewechselt (Beschriftung wechselt dann
  entsprechend auf „→ KV"). **VK Büro** wird jetzt als eigene Spalte
  angezeigt. Direkt neben der IAN stehen die Spalten **„Charge"** und
  **„Auftrag"** (die SAP-Auftragsnummer/das Vertriebsbeleg aus dem
  SAP-Export). Die **Charge** wird automatisch aus der SAP-Export-Spalte
  „Bestellnummer" abgeleitet — der Teil hinter dem „_" (z. B. aus
  „538616_2604" wird Charge „2604"). Fehlt dort eine Charge, zeigt die
  Spalte ersatzweise die Charge aus dem verknüpften Prüfauftrag (Feld
  „Initiale Charge" bzw. der Zahlenteil hinter dem „/" im Feld
  „IAN / Charge" der PDF). Die Spalten
  **„PA"** und **„KV"** zeigen auf einen Blick, ob zu
  dieser IAN bereits ein Prüfauftrag bzw. ein Kostenvoranschlag existiert:
  liegt einer vor, erscheint ein anklickbares Feld — bei „PA" mit dem
  **Stand der PA-PDF** (Datum aus dem Dateinamen bzw. ersatzweise aus dem
  Seitenfuß der PDF), bei „KV" mit der **aktuellen Gesamtsumme** — ein Klick
  springt direkt zum jeweiligen Datensatz; fehlt einer, steht dort nur ein
  „–". Die Spalten **„LFGB?"** und **„Trivial?"** zeigen den jeweiligen Wert,
  **sobald er irgendwo vorliegt** — da beide in der Praxis erst bei der
  KV-Erstellung (Karte „Pflichtangaben") gepflegt werden, zählt hier
  automatisch der Wert des verknüpften KVs, falls das Feld am
  Arbeitsvorrat-Eintrag selbst noch leer ist (ein dort manuell eingetragener
  Wert hat weiterhin Vorrang). Unter der Kopfzeile der Tabelle gibt es **Filter**: IAN, Auftrag und
  **Bezeichnung** als Freitextfeld (Teiltreffer); **VK Büro, Lieferant und Warengruppe als
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

  **Warengruppen-Filter zeigt/durchsucht auch die Bezeichnung**: die
  durchsuchbare Mehrfachauswahl für „Warengruppe" schlägt zu jedem Code (sofern
  in den Warengruppen-Stammdaten, siehe Reiter „Verwaltung", bekannt) zusätzlich
  die zugehörige Bezeichnung auf und zeigt sie direkt neben dem Code in der
  Options-Liste an (z. B. „385.030 – Grillbürsten"); die Suche im Filter-Panel
  matcht ebenfalls auf Code **und** Bezeichnung, sodass sich eine Warengruppe
  auch über ihren Namen statt nur über die reine Codenummer finden lässt. Die
  Arbeitsvorrat-**Tabelle selbst** zeigt weiterhin nur den Code, ohne eigene
  Bezeichnungs-Spalte.

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
  Ebenso wird die **Charge** automatisch erkannt (aus dem PDF-Feld „Initiale
  Charge", ersatzweise aus dem Zahlenteil hinter dem „/" im Feld
  „IAN / Charge") und als eigenes Badge „Charge …" oben auf der Detailseite
  sowie in der Prüfauftrag-Liste angezeigt.
  Die Detailseite eines Prüfauftrags ist in drei Bereiche gegliedert:
  - **Kopfdaten**: IAN/Charge (Rohfeld), Charge (eigenes Feld), Warengruppe,
    Artikelbezeichnung, Artikelkategorie,
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
    Ganz unten in der Karte steht die **Ahnentafel**: die komplette
    Vorgänger-Kette, über „IAN-Vorgänger" so weit zurückverfolgt, wie
    Prüfaufträge dafür im System vorliegen — Generation für Generation
    nummeriert, jede mit Sprung-Buttons zum jeweiligen Prüfauftrag/KV
    (fehlt zu einer IAN in der Kette ein Prüfauftrag, endet die Verfolgung
    dort mit einem entsprechenden Hinweis; das erste Projekt der Kette —
    keine weitere „IAN-Vorgänger" mehr hinterlegt — ist als solches markiert).
- **Kostenvoranschläge (KV)** – das Herzstück: pro IAN ein KV mit
  Stammdaten und einer Tabelle mechanischer Prüfpositionen (Kategorie,
  Bezeichnung, Kürzel, SAP-Code, Kosten, Anzahl, Summe, aktiv/inaktiv). Jede
  Position kann zusätzlich eine produktspezifische
  **Bewertungsgrundlage/Grenzwert** tragen (wird nur an der jeweiligen
  KV-Position gespeichert, nicht in einer gemeinsamen Datenbank) — dafür gibt
  es bewusst **keine eigene Spalte** in dieser Tabelle, sondern ein direkt
  editierbares Feld in der Übersicht „Bereits ausgewählte MAK-Parameter" im
  Produktspezifikationen-Block (siehe dort), da die meisten Positionen dieses
  Feld gar nicht brauchen. MAK-Parameter, die im Reiter „MAK" als
  **„Bewertungsgrundlage/Grenzwert erforderlich"** markiert sind, zeigen beim
  Hinzufügen im Produktspezifikationen-Block einen entsprechenden Hinweis
  (siehe MAK unten).

  **SAP-Nummer (Auftrag/Vertriebsbeleg) und Charge sichtbar & automatisch
  übernommen**: die Felder „SAP-Nummer" und „Charge" im KV-Formular werden
  zusätzlich direkt neben der IAN-Kennzeichnung im Detail-Header angezeigt
  (Badges „Auftrag …" bzw. „Charge …", nur sichtbar wenn befüllt) — „Auftrag"
  außerdem als Teil der Unterzeile in der KV-Übersichtsliste links. Beide
  Felder werden automatisch vorbelegt, sobald der KV mit einer IAN verknüpft
  ist (über „+ KV" aus dem Arbeitsvorrat direkt bei der Anlage, oder beim
  Eintragen/Ändern der IAN im KV-Formular): „SAP-Nummer" aus dem Feld
  „Auftrag" (Vertriebsbeleg) des Arbeitsvorrat-Eintrags, „Charge" aus der dort
  angezeigten Charge (inkl. deren eigenem Fallback auf den Prüfauftrag, siehe
  oben). Ein bereits vorhandener Wert wird dabei nie überschrieben.

  **Bemerkungen-Zeile je Position**: sobald zu einer Position irgendwo im
  Tool bereits etwas Relevantes hinterlegt ist, erscheint direkt darunter
  eine schmale, schreibgeschützte Zusatzzeile mit allen gefundenen
  Bemerkungen — ohne dafür extra in andere Reiter wechseln zu müssen. Da
  Positionen selbst keine feste Rückreferenz auf ihre Quelle speichern,
  erfolgt die Zuordnung best-effort über die Bezeichnung: die
  **Norm-Bemerkung** (jede Norm, deren Bezeichnung in der Position vorkommt —
  deckt Sicherheit & Norm, Kennzeichnung, LIDL-spezifisch, FFU/Fitting und
  NGO gleichermaßen ab), der **Prüfgrundlage-Kommentar** (bei
  „Produkt: …"-Bezeichnungen über den Produktnamen plus das zum Kürzel
  passende Kommentarfeld), der **MAK-Hinweis** einer Preisvariante (bei
  „Parameter / Variante"-Bezeichnungen) sowie die an der Position selbst
  gespeicherte **Bewertungsgrundlage/Grenzwert**. Da die Zuordnung über den
  Text läuft, kann sie bei manuell stark umbenannten oder freien Positionen
  auch mal nichts finden — dann bleibt die Zusatzzeile schlicht weg. Die
  **Überschrift zeigt bevorzugt die Artikelbezeichnung aus dem verknüpften
  Prüfauftrag** (aussagekräftiger als die bloße IAN) — ohne verknüpften PA
  fällt sie auf das freie „Artikel"-Feld des KVs zurück, erst danach auf
  „KV <IAN>"; die IAN selbst bleibt daneben immer als Badge sichtbar.
  **Ist zur IAN des KVs noch kein Prüfauftrag vorhanden**, erscheint statt der
  Sprung-Buttons stattdessen **„📄 PA-PDF für dieses Projekt hochladen"** —
  öffnet dieselbe PDF-Auswertung/Review-Ansicht wie beim Hochladen im Reiter
  „Prüfaufträge" (siehe oben), landet aber nach dem Übernehmen direkt wieder
  auf der KV-Detailseite, die sich daraufhin automatisch mit dem neu
  verknüpften Prüfauftrag auffrischt (inkl. automatisch angelegtem
  Arbeitsvorrat-Eintrag, falls noch keiner existierte) — praktisch, wenn zu
  einem bereits angelegten KV der zugehörige PA erst nachträglich vorliegt,
  ohne extra in den Reiter „Prüfaufträge" wechseln zu müssen.
  **Zwischen KV und Prüfauftrag lässt sich in beide Richtungen direkt
  springen**: „→ Verknüpften Prüfauftrag anzeigen" im KV wechselt zum
  passenden Prüfauftrag, „→ Verknüpften Kostenvoranschlag anzeigen" auf der
  Prüfauftrags-Detailseite wieder zurück — praktisch, um bei Bedarf schnell
  genauere Informationen auf der jeweils anderen Seite nachzuschlagen, ohne
  über die Liste suchen zu müssen. **Existiert zur IAN des Prüfauftrags noch
  kein KV**, erscheint stattdessen „+ Kostenvoranschlag für diese IAN
  anlegen" — legt direkt einen neuen, minimalen KV (IAN, Artikelbezeichnung,
  Lieferant, Warengruppe) an und wechselt in den KV-Tab; Warengruppe und
  Styleanzahl übernimmt der KV danach wie gewohnt automatisch aus dem
  verlinkten Prüfauftrag. Bei der **Vorgänger-Artikel-Karte** (siehe oben)
  ist das bewusst anders: dort gibt es ausschließlich Sprung-Buttons zu
  bereits vorhandenen Prüfaufträgen/KVs des Vorgängers, aber **keine
  Möglichkeit, von dort aus einen neuen KV anzulegen** — ein KV soll immer
  nur zum aktuellen Artikel selbst entstehen, nicht versehentlich zu einem
  Vorgänger.

  **Pflichtangaben** (LFGB?, Trivialartikel?) stehen in einer eigenen,
  bewusst hervorgehobenen Karte direkt unter den Kopfdaten — getrennt von
  den übrigen Stammdaten, damit diese beiden Mussfelder nicht in der Menge
  der restlichen Formularfelder untergehen. Eine Änderung von LFGB? oder
  Trivialartikel? aktualisiert die komplette KV-Detailseite **sofort** —
  wird z. B. Trivialartikel? auf „Ja" gesetzt, verschwindet der Haken bei
  „Sicherheit-/Normprüfung" unmittelbar, ganz ohne Tab-Wechsel.

  **Bereits aktive Prüfpositionen erscheinen direkt neben der zugehörigen
  Prüfumfang-Checkbox** (Bezeichnung(en) + Kosten als grünes Häkchen-Badge),
  statt nur ganz unten in der vollständigen, editierbaren
  Prüfpositionen-Tabelle sichtbar zu sein — so ist der Bezug zwischen
  Checkbox und tatsächlich übernommener Position sofort erkennbar, ohne
  scrollen zu müssen. Das Badge aktualisiert sich automatisch bei jeder
  Änderung in der Tabelle ganz unten (hinzufügen, entfernen,
  (de-)aktivieren, Kosten/Anzahl anpassen); Bearbeiten bleibt weiterhin
  Aufgabe der Tabelle selbst.

  **Ist „Sicherheit-/Normprüfung" nicht angehakt, zeigt die Checkliste den
  Grund** dafür an — „Trivialartikel = Ja" oder „Artikelkategorie Grün*" —
  direkt neben der Checkbox, entsprechend der Vorbelegungsregel (siehe
  unten).

  **Reihenfolge der übrigen Karten**: die Vorgänger-Artikel-Karte steht
  **direkt nach den Pflichtangaben und noch vor der Artikelkategorie** — so
  fällt sofort auf, wenn zur IAN ein Vorgänger existiert, bevor man sich in
  die weitere Prüfumfang-Auswahl vertieft. Danach folgen Artikelkategorie,
  die beiden Prüfumfang-Karten (roher Prüfumfang-Text + Checkliste, siehe
  unten) und schließlich **je Prüfung im Prüfumfang ein eigener,
  in sich abgeschlossener Block**: **Sicherheit-/Normprüfung** (immer
  sichtbar), **Kennzeichnung**, **(Physikalische-) Produktspezifikationen**,
  **FFU/Fitting**, **NGO** und **Referenzprüfung** (die letzten fünf jeweils
  nur, solange die zugehörige Prüfumfang-Checkbox angehakt ist — siehe
  unten), zuletzt die Prüfpositionen-Tabelle. Die frühere, alle Kategorien in
  einer einzigen Karte zusammenfassende „Prüfumfang-Details"-Karte gibt es
  nicht mehr — jede Prüfung hat jetzt ihren eigenen Block.

  Sofern der verknüpfte Prüfauftrag eine „IAN-Vorgänger"
  enthält, erscheint dieselbe Vorgänger-Artikel-Karte wie bei den Prüfaufträgen
  (inkl. Ahnentafel, siehe oben), ergänzt um drei zusätzliche Punkte:
  **„↺ Prüfpositionen aus Vorgänger-KV übernehmen"**: kopiert alle
  aktiven Positionen des Vorgänger-KVs (mit dessen tatsächlichen Kosten/
  Anzahl, nicht den ursprünglichen Standardwerten) in den aktuellen KV; bereits
  vorhandene Positionen werden dabei übersprungen, ein zweiter Klick legt also
  nichts doppelt an. **„↺ Gesamten Vorgänger-KV übernehmen"** geht einen
  Schritt weiter (mit Sicherheitsabfrage, da überschreibend statt nur
  ergänzend): übernimmt Artikel, Lieferant, SAP-Nummer, VK Büro,
  Warengruppen (neu/alt), LFGB?/Trivialartikel?, Styleanzahl, Notiz,
  Prüfumfang-Auswahl sowie sämtliche Prüfpositionen 1:1 vom Vorgänger-KV —
  praktisch bei sehr ähnlichen Wiederholartikeln, wenn im Zweifel der
  komplette Vorgänger als Ausgangspunkt taugt; die IAN des aktuellen KVs
  selbst bleibt dabei unangetastet. Und, sofern zum jüngsten Vorgänger ein
  KV im System vorliegt: **„Beim jüngsten Vorgänger geprüft"** — eine
  schreibgeschützte Liste aller dort aktiven Prüfpositionen (Kategorie,
  Bezeichnung, Kosten × Anzahl), direkt zum Nachlesen, was beim letzten
  Projekt tatsächlich geprüft wurde, ohne extra zu dessen KV wechseln zu
  müssen.

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

  **Warengruppe (alt)** bleibt ein Freitextfeld, wird aber automatisch
  befüllt, sobald in der Neu-↔-Alt-Zuordnungstabelle (Reiter „Verwaltung",
  siehe unten) ein passender Eintrag zur gewählten Warengruppe (neu)
  existiert — auch das nur, wenn das Feld noch leer ist. Die Zuordnungsliste
  ist mit der vollständigen offiziellen ADMIN-Blatt-Liste (341 Einträge)
  vorbelegt; einzelne Zeilen lassen sich im Reiter „Verwaltung" jederzeit von
  Hand korrigieren oder ergänzen, „Warengruppe (alt)" bleibt daneben weiter
  manuell pflegbar.

  Im Abschnitt **(Physikalische-) Produktspezifikationen** werden zusätzlich
  die aus dem PA ausgelesenen **„Qualität"** und darunter **„Material"**
  informativ angezeigt (analog zur bereits vorhandenen
  Markenreferenz-Anzeige; „Material" erscheint nur, wenn der PA ein
  entsprechendes Feld enthält) — praktisch als schneller Blick auf die
  Material-/Qualitätsangaben, ohne extra zum Prüfauftrag wechseln zu müssen.

  **Sicherheit-/Normprüfung** (bis vor kurzem „Warengruppen-Empfehlung
  (Mechanik)" genannt, funktional unverändert) – die primäre Vorschlagsquelle
  für diesen Prüfumfang-Abschnitt, wie besprochen **zuerst nach Warengruppe,
  dann nach Produkt**: sobald
  „Warengruppe (neu)" gesetzt ist, wird in einer echten, vom Team gepflegten
  Referenztabelle (185 Zeilen aus der Mechanik-Preisliste) nachgeschlagen.
  Gibt es zu der Warengruppe mehrere Produkte (z. B. „370.030 Grillzubehör"
  → Feuerzeug, Grillbürsten, Anzündkamin, …), erscheint eine Auswahlliste;
  bei genau einem Treffer wird er direkt angezeigt (Hauptprodukt). Für das
  gewählte Produkt zeigt die Karte Norm, Anzahl Muster, Besonderheiten
  (Bemerkungen, Trivial-/Kennzeichnungs-/Bedienungsanleitung-Kennzeichnung)
  sowie – falls vorhanden – FFU
  und NGO/StiWa mit den tatsächlich hinterlegten Kosten, jeweils mit
  „+ hinzufügen" direkt in die Prüfpositionen-Tabelle. Gibt es zur
  Warengruppe keine Referenzdaten, erscheint direkt in der Karte
  **„+ Neue Prüfgrundlage für Warengruppe … anlegen"** — öffnet denselben
  Anlage-Dialog wie im Reiter „Prüfgrundlagen", mit der Warengruppe schon
  vorbelegt; nach dem Speichern zeigt die Karte sofort den neuen Treffer,
  ohne den Tab wechseln zu müssen. Bis dahin bleibt zusätzlich die manuelle
  Auswahl unten verfügbar.

  Die Position **„Sicherheit & Norm"** ist mechanikseitig aus dem
  Auswahl_LIDL-Arbeitsblatt nachgebaut, wird aber **nicht mehr zu einer
  einzigen Summenposition zusammengefasst** — Hauptprodukt und jedes
  Set-Bestandteil erscheinen als **eigener, klar abgegrenzter Block** (eigene
  Umrandung) mit eigenem „+ hinzufügen":
  - **Set-Bestandteile**: über „Weiteren Set-Bestandteil hinzufügen" (bei
    mehrteiligen Produkten, z. B. Messer + Messerblock) lässt sich die
    Referenztabelle **warengruppenübergreifend** nach weiteren
    Produkten durchsuchen (z. B. „Messer" zu einem Hauptprodukt
    „Messerblock") — praktisch für mehrteilige Produkte, bei denen jeder
    Bestandteil eine eigene Norm/eigene Kosten hat. Jedes hinzugefügte
    Set-Bestandteil bekommt einen eigenen Block mit eigenem Norm-Text,
    eigenen (bereits rabattierten) Kosten und eigenem „✕ entfernen" —
    Hauptprodukt und Set-Bestandteile lassen sich dadurch unabhängig
    voneinander in die Prüfpositionen-Tabelle übernehmen, statt zwingend
    gemeinsam als eine Zeile.
  - **Style-Zuordnung**: hat der verknüpfte Prüfauftrag mehrere benannte
    Styles (Style_A, Style_B, …, erkannt aus denselben Style-Blöcken wie bei
    Maße/Gewicht/Qualität), zeigt jeder Block zusätzlich ein Dropdown „Alle
    Styles" / einzelner Style-Name. Damit lässt sich eine Prüfung entweder
    für alle Styles gemeinsam eintragen (Standard) oder gezielt nur für
    einen einzelnen Style — beide Varianten lassen sich auch nebeneinander
    anlegen, da der gewählte Style direkt in die Positionsbezeichnung
    aufgenommen wird (z. B. „… (Style_A)") und damit automatisch eine
    eigenständige, nicht doppelt anlegbare Position ergibt. Bei einstiligen
    Artikeln erscheint kein Style-Dropdown.
  - **Artikelkategorie-Rabattfaktor**: die Kosten jedes einzelnen Blocks
    (Hauptprodukt wie auch jedes Set-Bestandteil) werden automatisch mit
    einem Prozentsatz je nach Artikelkategorie des verknüpften Prüfauftrags
    multipliziert — Standard **Grün/Grün* → 40 %, Gelb → 50 %, sonst/unbekannt
    → 60 %**, im Reiter „Verwaltung" unter „Prüfumfang je Artikelkategorie"
    editierbar (siehe dort) —, in Summe rechnerisch identisch zum „Summe
    zuerst, dann Faktor" (der Faktor ist auf jeden Block gleich,
    Multiplikation ist distributiv). Der verwendete Prozentsatz und die
    erkannte Artikelkategorie werden direkt unter den Blöcken angezeigt.
    „Grün" wird dabei mit und ohne Sternchen („Grün*") gleich behandelt;
    reale Prüfaufträge liefern teils Varianten wie „Grün*", die Erkennung
    vergleicht deshalb bewusst normalisiert (ohne Sonderzeichen,
    Groß-/Kleinschreibung egal) statt exakt, damit der Rabatt auch dort
    korrekt greift. Derselbe Prozentsatz bestimmt außerdem den Hinweistext
    „Teilprüfung: X% der Vollprüfung" (siehe weiter unten) — beide Stellen
    nutzen dieselbe, im Reiter „Verwaltung" gepflegte Einstellung.
  - **Styles-Formel**: ist am Kostenvoranschlag eine **Styleanzahl** hinterlegt
    (Feld „Styleanzahl" in den KV-Stammdaten, meist automatisch aus dem
    Prüfauftrag übernommen), fließt sie in die Kosten jedes Blocks ein:
    **1. Prüfung (Feld „Kosten") + (Styleanzahl − 1) × Kosten je weiterem
    Produkt** (Feld „Kosten je weiterem Produkt" an derselben Norm-Referenz
    der Prüfgrundlage). Ist „Kosten je weiterem Produkt" nicht gesetzt, gilt
    ersatzweise derselbe Betrag wie für die 1. Prüfung. Bei Styleanzahl ≤ 1
    (leer, „1" oder nicht numerisch) ändert sich nichts gegenüber vorher.
    Der Rabattfaktor wird auf den bereits styles-angepassten Betrag
    angewendet; ab 2 Styles zeigt der Vorschlag zusätzlich einen Hinweis
    „(N Styles)". Gilt gleichermaßen für Sicherheit-/Normprüfung,
    FFU/Fitting und NGO/StiWa. Die Prüfgrundlage selbst (Reiter
    „Prüfgrundlagen") ist wiederverwendbar über verschiedene KVs mit
    unterschiedlicher Styleanzahl hinweg und zeigt deshalb weiterhin nur den
    einfachen Basispreis ohne Styles-Formel.

  Dieselbe Hauptprodukt-/Set-Bestandteil-/Style-Mechanik dient seit der
  Aufteilung in eigene Blöcke auch den **FFU/Fitting**- und **NGO**-Blöcken
  (siehe unten) — dort jeweils bezogen auf die für FFU bzw. NGO/StiWa
  hinterlegten Normen der Prüfgrundlage statt auf die Sicherheit &
  Norm-Normen (inkl. Styles-Formel, siehe oben). Der **Artikelkategorie-
  Rabattfaktor gilt bei LIDL ausschließlich für die Sicherheit-/Normprüfung**
  — FFU/Fitting und NGO (wie auch alle übrigen Prüfungskategorien:
  Kennzeichnung, Optischer Abgleich, Produktspezifikation, Referenzprüfung)
  werden dort zum **vollen, unrabattierten Preis** verrechnet, entsprechend
  fehlt der Rabattfaktor-Hinweis in diesen beiden Blöcken. Die zusätzlich
  vorhandenen **festen** FFU/Fitting- und NGO-Positionen (siehe „Innerhalb
  der Blöcke" weiter unten) sind davon unabhängig und bleiben ohne
  Set-Bestandteile/Rabatt/Styles-Formel.

  **Kosten direkt anpassen**: unter jedem Block (Hauptprodukt, Set-Bestandteil,
  FFU, NGO/StiWa) gibt es ein Feld **„Kosten (Prüfgrundlage) €"**, mit dem
  sich der hinterlegte Preis direkt hier ändern lässt, ohne extra in den
  Reiter „Prüfgrundlagen" wechseln zu müssen — die Änderung wird **direkt an
  der Prüfgrundlage gespeichert** und wirkt sich damit auch auf künftige KVs
  mit derselben Warengruppe/demselben Produkt aus (der angezeigte
  Vorschlagspreis daneben bleibt der bereits rabattierte Wert, das Eingabefeld
  zeigt den unrabattierten Rohwert aus der Prüfgrundlage). Referenziert ein
  Block mehrere Normen (in den mitgelieferten Daten aktuell nicht der Fall),
  erscheint dort stattdessen ein Link **„→ Kosten in der Prüfgrundlage
  bearbeiten"**, der direkt zur vollständigen Bearbeitung wechselt.

  **Kommentar direkt bearbeiten**: direkt unter dem Kosten-Feld gibt es je
  Block (Hauptprodukt, Set-Bestandteil, FFU, NGO/StiWa) zusätzlich ein Feld
  **„Kommentar"** — anders als die „Bemerkung" an der Norm selbst (die
  überall geteilt wird, wo diese Norm referenziert ist) gilt dieser Kommentar
  **nur für diese eine Prüfgrundlage/dieses eine Produkt** und wird **nicht
  in der Normdatenbank gespeichert**. Genau wie bei den Kosten wird die
  Änderung direkt an der Prüfgrundlage gespeichert (wirkt sich also auch auf
  künftige KVs mit demselben Produkt aus) und ist ebenso im Reiter
  „Prüfgrundlagen" selbst editierbar (siehe dort) — beide Stellen zeigen
  denselben Wert.

  **Prüfgrundlage komplett aus dem KV heraus pflegen**: im Kopf des
  Sicherheit-/Normprüfung-Blocks gibt es zwei weitere Buttons, unabhängig von
  den beiden oben beschriebenen Einzelfeldern. **„✎ Prüfgrundlage
  bearbeiten"** (erscheint, sobald ein Produkt gewählt ist) öffnet das
  vollständige Bearbeiten-Formular der zugehörigen Prüfgrundlage direkt als
  Dialog — inklusive aller Felder (Normen, Muster, Trivial, Kommentare je
  Block usw.), nicht nur Kosten/Kommentar wie bei den Einzelfeldern; nach dem
  Speichern bleibt der KV-Tab aktiv. **„+ Neue Prüfgrundlage anlegen"** ist
  immer sichtbar (auch wenn für die Warengruppe bereits eine oder mehrere
  Prüfgrundlagen existieren, z. B. um ein weiteres Produkt derselben
  Warengruppe zu ergänzen) und öffnet ein leeres Formular mit bereits
  vorbelegter Warengruppe. Ein Wechsel in den Reiter „Prüfgrundlagen" ist für
  beide Vorgänge nicht mehr nötig.

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
    **Trivial="Ja"** oder die **Artikelkategorie ist Grün\* (mit Stern)**;
    ist die Artikelkategorie Grün\*, aber FFU, NGO oder Referenzprüfung sind
    für denselben Artikel gefordert (deren Checkboxen oben angehakt), bleibt
    sie trotzdem Pflicht. Wichtig: **nur „Grün\*" mit Stern gilt als sicher
    unbedenklich** — ein einfaches „Grün" ohne Stern befreit bewusst
    **nicht**, da dort eine Prüfung ggf. trotzdem notwendig sein kann, und
    bleibt daher ganz normal Pflicht wie jede andere Artikelkategorie auch.
    Für den tatsächlichen Wert (Norm + Kosten) siehe den
    Sicherheit-/Normprüfung-Block weiter oben.
  - **Kennzeichnung (Verpackung & Produkt)** – **immer Pflicht**, unabhängig
    von Prüfumfang, Artikelkategorie oder Trivial, und deshalb immer
    vorbelegt. Es gibt dafür vier feste Positionen mit demselben Zweck,
    aber unterschiedlichem PPM-Code — automatisch als Vorschlag markiert
    wird genau die zum KV passende: **1001_PPM** (Standard/VK Büro 0070),
    **1002_PPM** (VK Büro 0049), **1003_PPM** (VK Büro 0072), **1005_PPM**
    (sobald LFGB="Ja" — hat Vorrang vor der VK-Büro-Zuordnung). Die übrigen
    drei Varianten bleiben im Kennzeichnung-Block sichtbar und bei Bedarf
    manuell hinzufügbar.
  - **Kennzeichnung (Bedienungsanleitung)** – folgt weiterhin der
    Prüfumfang-Text-Erkennung wie bisher. Entspricht immer der festen
    Position „Bedienungsanleitung E&E (1000_PPM)".
  - **Optischer Abgleich** – folgt ebenfalls weiterhin der
    Prüfumfang-Text-Erkennung. Entspricht immer der festen Position
    „Optischer Abgleich (112_PPM)".

  Alle vier lassen sich unabhängig voneinander manuell an- und abhaken,
  unabhängig von ihrer jeweiligen Vorbelegungs-Regel — z. B. wenn im
  Einzelfall nur der optische Abgleich, nicht aber die Kennzeichnungsprüfung
  benötigt wird. Jeder Unterpunkt steuert direkt, ob die zugehörige feste
  Position weiter unten als „Vorschlag" markiert ist. Dateien
  aus einer älteren Tool-Version (ein einzelnes Häkchen für den ganzen
  Abschnitt bzw. nur die eine „1001_PPM"-Kennzeichnungs-Position) werden
  beim Laden automatisch migriert/ergänzt, damit kein bereits gepflegter KV
  plötzlich Positionen verliert.

  **Erst für angehakte Abschnitte/Unterpunkte erscheint darunter der
  jeweils zugehörige, eigenständige Block** — ist nichts angehakt, bleibt nur
  die Checkliste sichtbar. Ohne verknüpften Prüfauftrag startet die
  Checkliste komplett unangehakt (mit Ausnahme der immer aktiven
  Sicherheit-/Normprüfung- und Kennzeichnung(Verpackung & Produkt)-Regel,
  siehe oben), lässt sich aber jederzeit manuell aktivieren (z. B. um
  Positionen schon vor dem PA-Upload grob vorzubereiten). Jede einzelne
  Position steht dabei in einer eigenen, klar umrandeten Zeile statt nur
  durch eine dünne Trennlinie abgesetzt zu sein — Vorschläge zusätzlich grün
  hinterlegt. Die einzelnen Blöcke:
  - **Sicherheit-/Normprüfung** (siehe oben, immer sichtbar sobald eine
    Warengruppe hinterlegt ist) — der Abschnitt „Weitere Positionen" enthält
    hier (im Standardfall) alle **Normen mit Prüfungsart „LIDL-spezifisch"**
    (Reiter „Normen"/„Verwaltung" → Prüfungsarten, analog zu „Kennzeichnung"
    oben). Jede solche Norm hat im Reiter „Normen" zusätzlich ein Dropdown
    **„KV-Block"**, das festlegt, in welchem der vier Blöcke Sicherheit-/
    Normprüfung (Standard), (Physikalische-) Produktspezifikationen,
    FFU/Fitting oder NGO sie als addierbare Position erscheint — dort dann
    jeweils per „+ hinzufügen" direkt übernehmbar, mit ihrem hinterlegten
    Preis (sofern gepflegt) und ohne Vorschlags-Markierung, da es dafür
    (anders als bei den vier festen Kennzeichnung-GER-Varianten) kein
    vergleichbares, aus dem Prüfauftrag ableitbares Signal gibt. Bei
    Produktspezifikationen, FFU/Fitting und NGO erscheint der Abschnitt
    „Weitere Positionen" jeweils **nur**, wenn dort tatsächlich mindestens
    eine LIDL-spezifische Norm zugeordnet ist — dort gibt es (anders als bei
    Sicherheit-/Normprüfung) keine feste Katalogposition mehr, die den
    Abschnitt ohnehin sichtbar hielte. Bei Sicherheit-/Normprüfung selbst
    bleibt der Abschnitt weiterhin an die dortige Checkbox-Auswahl gekoppelt
    (siehe „Prüfumfang" oben), unabhängig davon, ob LIDL-spezifische Normen
    zugeordnet sind. Die früher hier fest verankerten Katalogpositionen
    **Akkusicherheitskurzcheck** und **Optischer Abgleich** wurden entfernt;
    **Mustereinlagerung** wird im Prüfumfang ebenfalls nicht mehr angezeigt
    (weder als Vorschlag noch manuell hinzufügbar).
  - **Kennzeichnung** – eigener Block, erscheint sobald „Kennzeichnung
    (Verpackung & Produkt)" oder „Kennzeichnung (Bedienungsanleitung)"
    angehakt ist. Die zum Hinzufügen angebotenen Positionen sind **direkt die
    Normen mit Prüfungsart „Kennzeichnung"** (Reiter „Normen"/„Verwaltung" →
    Prüfungsarten) statt eines separaten, festen Katalogs — jede Norm lässt
    sich per „+ hinzufügen" direkt als Position in den KV übernehmen. Beim
    ersten Start werden dafür automatisch die vier bisherigen
    Kennzeichnung-Varianten (1001/1002/1003/1005_PPM) sowie
    „Bedienungsanleitung E&E (1000_PPM)" mit dieser Prüfungsart vorbelegt (nur
    beim ersten Mal, eine später manuell geänderte Prüfungsart wird nie
    überschrieben) — die zum KV passende Variante (je VK Büro/LFGB, siehe
    unten) ist weiterhin automatisch als „Vorschlag" markiert. Weitere echte
    Kennzeichnung-Normen lassen sich jederzeit im Reiter „Normen" ergänzen
    (Prüfungsart auf „Kennzeichnung" setzen) und erscheinen dann automatisch
    mit in dieser Liste. Ein an einer Kennzeichnung-Norm eingetragener
    **Kosten-Wert** (siehe „Kosten direkt an der Norm" weiter unten) wird für
    diesen Block bewusst **nicht** angezeigt oder übernommen — der
    Kennzeichnung-Block hat einen fest vorgegebenen Gesamtpreis (siehe „VP &
    Kennzeichnung"-Hinweis weiter unten), der die einzelnen Norm-Kosten
    immer überschreibt. Dieser Gesamtpreis wird automatisch auf die gerade
    **aktiven** Kennzeichnung-Positionen im KV verteilt — **löscht** oder
    **deaktiviert** man eine davon in der Prüfpositionstabelle, verteilt sich
    der Preis sofort neu auf die verbleibenden aktiven Positionen, und die
    gelöschte/deaktivierte Norm erscheint hier wieder als „+ hinzufügen"
    statt „bereits im KV".

    Trägt die im Sicherheit-/Normprüfung-Block für
    dieses Produkt gewählte Norm selbst Kennzeichnungs- und/oder
    Bedienungsanleitung-Anforderungen (siehe „Kennzeichnung/Bedienungsanleitung
    je Norm" unten), erscheint dazu oben im Block ein entsprechendes Badge.
  - **(Physikalische-) Produktspezifikationen**: direkt oben im Block, noch
    vor Qualität/Material, erscheint sobald mindestens eine Position
    hinzugefügt wurde die Übersicht **„Bereits ausgewählte MAK-Parameter"**
    (mit Anzahl) — eine Liste aller in dieser Kategorie bereits im KV
    vorhandenen Positionen samt Kosten, damit auf einen Blick sichtbar ist,
    was für dieses Produkt schon ausgewählt wurde, ohne dafür erst in der
    großen Positionstabelle weiter unten suchen zu müssen. Deaktivierte
    Positionen werden ebenfalls aufgeführt, aber als „– inaktiv" markiert,
    damit nichts versteckt bleibt. Je Position gibt es hier außerdem ein
    direkt editierbares Feld **„Bewertungsgrundlage/Grenzwert"** (produkt-
    spezifisch, wird an der Position gespeichert — dafür gibt es bewusst
    keine eigene Spalte in der großen Positionstabelle, da die meisten
    Positionen dieses Feld nicht brauchen); alle übrigen Eigenschaften
    (SAP-Code, Kosten, Anzahl, Aktiv-Status, Entfernen) bleiben weiterhin
    Sache der Positionstabelle. Enthält direkt
    übereinander die aus dem Prüfauftrag ausgelesenen **„Qualität"** und
    **„Material"** (jeweils als eigene Style-Blöcke aufgeteilt wie auf der
    Prüfauftrags-Detailseite; „Material" erscheint nur, wenn der PA ein
    entsprechendes Feld enthält). Kommt darin der Wortlaut eines **MAK-
    Schlagworts** (siehe Reiter „MAK" unten) vor, wird die Fundstelle direkt
    im Text **fett hervorgehoben** — und der zugehörige MAK-Parameter
    erscheint zusätzlich als klickbarer **Vorschlag** direkt über dem
    MAK-Dropdown (mit dem gefundenen Schlagwort in Klammern); ein Klick
    wählt den Parameter im Dropdown aus. Das **Dropdown „MAK-Parameter
    nachschlagen"** selbst bietet alle Einträge des Materialanforderungskatalogs
    nach Kategorie gruppiert zur Auswahl an; ein **Textfeld direkt darüber**
    durchsucht dabei live alle Felder (Parameter, Kategorie, Bereich,
    Anforderung, Norm EU/US, Mindest-Prüfnachweis, Schlagworte — dieselbe
    breite Suche wie im Reiter „MAK" selbst) und grenzt die
    Dropdown-Optionen entsprechend ein (Kategorien ohne Treffer verschwinden
    automatisch) — praktisch bei der langen, nach Kategorie sortierten
    Liste, um einen Parameter nicht erst durchscrollen zu müssen. Eine noch
    passende Auswahl bleibt beim Weitertippen erhalten, eine nicht mehr
    passende wird zurückgesetzt. Nach Auswahl eines Parameters erscheinen
    darunter dessen Anforderung, Norm/Standard EU, Norm/Standard US und
    Mindest-Prüfnachweis, ohne in den MAK-Tab wechseln zu müssen. Der
    Parameter ist dabei **kein reines Nachschlagewerk**: je nach seiner
    **Abrechnung** (siehe „MAK" unten) sieht die Darstellung unterschiedlich
    aus. Im Modus **„Pro Laufzeit"** (z. B. Korrosionsbeständigkeit nach
    Laufzeit/Paketpreis-Gruppe) erscheint statt eines einzelnen Buttons je
    hinterlegter Laufzeit eine eigene Zeile **„Laufzeiten/Preise"** mit ihrem
    tatsächlichen Preis und SAP-Code zum Hinzufügen. Im Modus **„Pro
    Artikel"** bleibt es beim einzelnen **„+ hinzufügen"** für den Parameter
    selbst — trägt der Parameter dort einen eigenen **Preis**, erscheint
    dieser direkt neben dem Titel und wird beim Hinzufügen automatisch als
    Kosten der Position übernommen (SAP-Code bleibt frei nachtragbar); ohne
    hinterlegten Preis landet die Position wie bisher mit 0 €. Ist zusätzlich
    eine **Staffelung je weiterem Artikel** hinterlegt, erscheint sie hier
    als reiner Hinweis (wird nicht automatisch verrechnet). Beide Modi landen
    als Position mit Kategorie Produktspezifikationen im KV. Direkt darunter
    lassen sich außerdem die **Schlagworte** des gewählten Parameters
    bearbeiten (Chips hinzufügen/entfernen, identisch zum Reiter „MAK" selbst
    — beide Ansichten teilen sich dieselben Daten, eine Änderung hier ist
    also sofort auch dort sichtbar), ohne dafür extra in den MAK-Tab wechseln
    zu müssen. Der frühere, separate 62-Zeilen-Parameterkatalog (feste
    „Projektkosten"-Pauschale + durchsuchbare Katalog-Suche) ist entfallen —
    seine LIDL-Preise stecken jetzt, soweit einem MAK-Parameter eindeutig
    zuordenbar, direkt an den passenden MAK-Einträgen als Preisvarianten.
  - **FFU/Fitting** und **NGO**: je ein eigener Block, funktional analog zu
    Sicherheit-/Normprüfung — dasselbe im Sicherheit-/Normprüfung-Block
    gewählte Hauptprodukt (Warengruppe → Produkt) wird hier übernommen (zum
    Ändern zurück in den Sicherheit-/Normprüfung-Block wechseln, es gibt nur
    eine Produktauswahl), die Prüfgrundlage liefert aber die für **FFU**
    bzw. **NGO/StiWa** hinterlegten Normen samt Kosten (inkl.
    Set-Bestandteile, Style-Zuordnung — **kein** Artikelkategorie-
    Rabattfaktor, siehe oben — und „Kosten (Prüfgrundlage) €"-Bearbeitung)
    statt der Sicherheit & Norm-Normen. Die früher hier fest verankerte
    Katalogposition („FFU/Fitting" bzw. „NGO") wurde entfernt; der Abschnitt
    „Weitere Positionen" erscheint deshalb nur noch, wenn für diesen Block
    mindestens eine Norm mit Prüfungsart „LIDL-spezifisch" zugeordnet ist
    (siehe oben).
  - **Referenzprüfung**: eigener Block mit der festen Position
    „Referenzprüfung" sowie zusätzlich der „Markenreferenz" aus dem
    Prüfauftrag (das Referenzprodukt, gegen das verglichen wird).

  Bei jedem Block lässt sich per **„+ hinzufügen"** eine
  einzelne Position oder per **„Alle Vorschläge übernehmen"** alle markierten
  Positionen auf einmal in die Prüfpositionen-Tabelle unten eintragen — dort
  dann wie gewohnt Kosten/Anzahl anpassen, deaktivieren oder entfernen.
  Positionen lassen sich außerdem frei anlegen („+ Freie Position").

  **Die Tabelle „Mechanische Prüfpositionen" ist immer nach Kategorie
  sortiert** (Sicherheit-/Normprüfung inkl. Kennzeichnung, dann
  Produktspezifikation, FFU/Fitting, NGO, Referenzprüfung — passend zur
  Reihenfolge im offiziellen LIDL/OWIM-Kostenvoranschlag), unabhängig von der
  Reihenfolge, in der Positionen hinzugefügt wurden. **„📋 In Zwischenablage
  kopieren"** kopiert die komplette Tabelle tabulatorgetrennt (Aktiv,
  Kategorie, Bezeichnung, Kürzel, SAP-Code, Kosten, Anzahl, Summe, Bemerkung)
  — direkt in Excel einfügbar. In der Datei `IAN_CHARGE_AB_ARTIKEL...xlsm`
  liegt dafür ein vorbereitetes VBA-Makro bereit (`Mechanik_Import.bas`,
  ersetzt den Code der vorhandenen `Sub Mec()` hinter dem Button **„Mechanik
  einfügen"**): Klick darauf übernimmt alle aktiven Positionen automatisch als
  neue Zeilen in die Tabelle „Mechanik_30SER" auf dem Blatt „Inspection
  Booking", direkt hinter der jeweiligen Kategorie-Überschriften-Zeile
  (Sicherheit & Norm, Produktspezifikation, FFU/Fitting, Referenzprüfung,
  NGO); die Spalte „Bemerkung" landet in der bisher ungenutzten Spalte L. Vor
  jedem Import setzt das Makro außerdem alle vorbelegten „x"-Haken in der
  „FILTER"-Spalte der bestehenden Standardzeilen zurück (außer bei den fünf
  Kategorie-Überschriften-Zeilen) und filtert am Ende automatisch auf
  „FILTER" = „x", sodass nur noch die Zeilen zählen/sichtbar sind, die
  tatsächlich aus dem aktuellen KV-Monitoring-Export stammen.

  Die fünf Kategorie-Überschriften-Zeilen sind dabei **reine Überschriften-
  und Summenzeilen ohne eigene Excel-Formel** — die ursprünglichen
  SUMPRODUCT-/INDEX-MATCH-/IF(...)-Formeln wurden entfernt, das Makro
  berechnet die Summe je Kategorie **ausschließlich aus den tatsächlich
  ausgewählten Positionszeilen** (Kosten × Anzahl aller zugehörigen, mit „x"
  markierten Zeilen) und schreibt sie als festen Wert in die jeweilige Zeile
  — auch bei Produktspezifikation, ohne den früheren Pauschal-Aufschlag aus
  der Tabelle „Kostentabelle" (190 €/250 €), der nicht mehr zutrifft. Dadurch
  aktualisieren sich die Summen **nicht mehr automatisch** bei manuellen
  Änderungen — dafür
  einfach „Mechanik einfügen" erneut ausführen (funktioniert auch ganz ohne
  neue Positionen aus der Zwischenablage, solange diese nicht leer ist).
  Details und Einbau-Anleitung stehen als Kommentar am Anfang von
  `Mechanik_Import.bas`.

  Bei der Sicherheit-/Normprüfung-Position, die **aus der Prüfgrundlage**
  ausgewählt wurde (Hauptprodukt/Set-Bestandteil, „+ hinzufügen" in der
  Warengruppen-Empfehlung), erscheint darunter automatisch **„Teilprüfung"**
  mit dem Prozentsatz der Vollprüfung — ganz ohne Ankreuzen, da eine
  Teilprüfung der mechanischen Sicherheit laut Fachvorgabe **immer** gefordert
  ist. Für alle anderen Positionen im selben Block (Kennzeichnung, Akku,
  Bedienungsanleitung, Optischer Abgleich, Mustereinlagerung sowie über
  „Weitere Positionen" manuell hinzugefügte LIDL-spezifische Normen — auch
  wenn diese dieselbe Kategorie/dasselbe Kürzel „MS" teilen) erscheint sie
  bewusst **nicht**. Der Prozentsatz ergibt sich dabei
  **automatisch aus der Artikelkategorie des verknüpften Prüfauftrags**, auf
  Basis derselben, im Reiter „Verwaltung" unter „Prüfumfang je
  Artikelkategorie" editierbaren Einstellung, die auch den
  Artikelkategorie-Rabattfaktor bestimmt (Standard Grün/Grün* 40 %, Gelb
  50 %, Rot bzw. keine Artikelkategorie hinterlegt 60 %, siehe oben) und
  aktualisiert sich sofort, wenn sich die Artikelkategorie oder die
  Verwaltungs-Einstellung ändert. Die Angabe
  fließt beim Kopieren in die Zwischenablage automatisch in die neue
  „Bemerkung"-Spalte ein (z. B. „Teilprüfung: 40% der Vollprüfung
  (Artikelkategorie Grün)"), zusammen mit allen anderen automatisch
  aggregierten Bemerkungen zur Position (Bewertungsgrundlage/Grenzwert,
  Norm-Bemerkung, Prüfgrundlage-Kommentar, MAK-Hinweis) — damit sie auch beim
  Excel-/VBA-Import ankommen. Im CSV-Export (Reiter „Kostenvoranschläge")
  gibt es dafür eigene Spalten „Teilprüfung"/„Teilprüfung %".
  **„⧉ Als Vorlage für neuen KV duplizieren"** kopiert einen bestehenden KV
  (z. B. eines Wiederholartikels) komplett als Ausgangspunkt für einen
  neuen. Über die Suche oben lassen sich bestehende KVs nach
  IAN/Artikel/Warengruppe/Lieferant durchsuchen, um einen passenden zum
  Duplizieren zu finden.
- **Prüfgrundlagen** – die Datenquelle der Warengruppen-Empfehlung im KV
  (siehe oben) ist **direkt in der Oberfläche bearbeitbar und neu anlegbar**,
  nicht mehr nur fest eingebettet. **Zwei umschaltbare Ansichten** (Pillen
  oben im Reiter): **„Nach Warengruppe (LIDL)"** (Standard) gruppiert nach
  **Warengruppe** — die LIDL-spezifische Sicht, wie bisher. **„Nach Bereich
  (andere Kunden)"** gruppiert stattdessen ausschließlich nach **Bereich**
  (siehe Reiter „Verwaltung" → Warengruppen → Feld „Bereich"), ohne weitere
  Unterteilung nach Warengruppe — gedacht für Kunden, bei denen die
  Zuordnung nach Warengruppen-Code keine Rolle spielt, aber die
  übergeordnete Produktkategorie schon. Einträge ohne zugeordneten Bereich
  landen in „(ohne Bereich)". Innerhalb jeder Gruppe (in beiden Ansichten)
  sind die Produkte alphabetisch (A–Z) sortiert. Die Übersichtszeile je
  Produkt zeigt nur das Nötigste (Produkt, Normen, Kosten Sicherheit & Norm,
  Anzahl Muster, Kennzeichnung-/Bedienungsanleitung-Badges, ob FFU/StiWa
  hinterlegt sind) — der
  Warengruppen-Code selbst wird hier bewusst **nicht** als eigene Spalte
  angezeigt (steht ja schon im Gruppenkopf), ist aber weiterhin die Basis für
  die Zuordnung. **Auf eine Zeile klicken** (oder ✏️) öffnet die
  Detailansicht zum Bearbeiten; **„+ Neue Prüfgrundlage"** öffnet sie leer.
  Änderungen werden erst mit „Speichern" übernommen — „Abbrechen" verwirft
  sie wieder vollständig, inklusive aller Normen-Referenzen. Sobald die
  Warengruppe gespeichert wird, wandert der Eintrag automatisch in die
  passende (neue oder bestehende) Gruppe (in beiden Ansichten).

  **Warengruppe wird nur noch per durchsuchbarem Dropdown gewählt**, kein
  Freitext mehr — Klick öffnet die vollständige Liste, Tippen filtert nach
  Code oder Name (Code wird nicht mehr doppelt angezeigt, da er im Namen
  bereits enthalten ist). Die Liste ist mit der vollständigen offiziellen
  Warengruppen-Stammdaten-Tabelle (730 Codes über alle Warenbereiche)
  vorbelegt und wie Bereich (siehe unten) über den Reiter **„Verwaltung"**
  frei pflegbar — neue Warengruppen anlegen, Code/Name/Bereich bestehender
  ändern oder welche löschen.

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
  **„→ bearbeiten"** neben jeder ausgewählten Norm/PPM springt direkt in
  deren Bearbeitung im Reiter „Normen" (schließt dafür das
  Prüfgrundlage-Fenster wie „Abbrechen", verwirft also ungespeicherte
  Änderungen an der Prüfgrundlage) — praktisch, um z. B. schnell den
  SAP-Code oder eine Bemerkung der referenzierten Norm zu prüfen/anzupassen,
  ohne die Prüfgrundlage separat wiederzufinden. Bei einer inzwischen
  gelöschten Norm-Referenz fehlt der Button entsprechend.
  Diese Normen-Auswahl gibt es jetzt für alle drei Prüfblöcke — **Sicherheit
  & Norm, FFU/Fitting und NGO/StiWa** —, die vorherigen reinen
  Freitext-Hinweise bei FFU/StiWa sind entsprechend entfallen.

  **Kennzeichnung/Bedienungsanleitung stehen nicht mehr an der Prüfgrundlage,
  sondern an der jeweiligen Norm selbst** (Reiter „Normen", siehe unten) und
  werden automatisch übernommen, sobald diese Norm hier referenziert wird —
  die frühere manuelle „KEZ-Anforderungen"-Checkbox an der Prüfgrundlage
  entfällt dadurch komplett. Referenziert eine Prüfgrundlage (in einem der
  drei Blöcke) eine Norm, die an Kennzeichnung und/oder Bedienungsanleitung
  hinterlegt hat, erscheint das in der Prüfgrundlagen-Liste als Badge
  („Kennz."/„BDA") und — sofern diese Norm im KV für Sicherheit-/Normprüfung
  gewählt ist — im Kennzeichnung-Block als eigenes Badge
  („Kennzeichnungsanforderungen"/„Bedienungsanleitung-Anforderungen") —
  ganz ohne manuelles Ankreuzen.
  Ist die Referenz zusätzlich **„in Anlehnung an"** angekreuzt, entfällt die
  automatische Übernahme zunächst (die Norm wird ja nicht vollständig
  angewendet); je Norm-Referenz lässt sich dann aber pro Flag gezielt
  **„… trotzdem übernehmen"** ankreuzen, falls die Kennzeichnungs- bzw.
  Bedienungsanleitung-Anforderungen im Einzelfall trotzdem gelten sollen.

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

  Neben „Kosten €" steht je Norm-Referenz jetzt auch **„Kosten je weiterem
  Produkt €"** — gedacht für den Fall, dass mehrere Produkte parallel unter
  derselben Norm geprüft werden und sich dabei Rüstzeiten einsparen lassen:
  „Kosten €" bildet die Kosten für das erste Produkt ab, „Kosten je weiterem
  Produkt €" die reduzierten Kosten für jedes zusätzliche, parallel geprüfte
  Produkt (ohne erneute Rüstzeit). Das Feld ist aktuell reine Datenpflege —
  wird schreibgeschützt auch in der „Verwendet in Prüfgrundlagen"-Übersicht
  im Reiter „Normen" mit angezeigt (siehe unten), fließt aber noch nicht
  automatisch in die KV-Kalkulation ein.

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
  Hinweise, die sich nicht auf die Norm im Allgemeinen, sondern auf ein
  konkretes Produkt/diese eine Prüfgrundlage beziehen (z. B. „Der Artikel ist
  in Bezug auf [Schnittleistung] mindestens gleichwertig mit
  [Vergleichsprodukt]" bei einer StiWa-Prüfung), gehören dagegen nicht in
  dieses normübergreifend geteilte Feld, sondern in den separaten
  **„Kommentar"** je Block (siehe direkt darunter). Dateien aus einer
  älteren Tool-Version
  (eine einzelne Bemerkung pro Prüfgrundlage, zwischenzeitlich auch eine
  Bemerkung je Referenz) werden automatisch auf die Norm migriert: der Text
  landet auf der ersten referenzierten Norm (bevorzugt aus Sicherheit & Norm,
  sonst FFU, sonst StiWa); treffen für dieselbe Norm mehrere unterschiedliche
  Alttexte zusammen, werden sie durch „ | " getrennt zusammengeführt statt
  einander zu überschreiben.

  **Kommentar je Block, Prüfgrundlage-spezifisch statt norm-übergreifend** —
  unter jedem der drei Normen-Felder (Sicherheit & Norm, FFU/Fitting,
  NGO/StiWa) gibt es ein zusätzliches, frei editierbares Textfeld
  **„Kommentar"**. Anders als die Bemerkung oben (siehe dort) gilt dieser
  Kommentar **nur für diese eine Prüfgrundlage** und wird **nicht in der
  Normendatenbank gespeichert** — verschiedene Prüfgrundlagen, die dieselbe
  Norm referenzieren, können also unterschiedliche Kommentare tragen, ohne
  sich gegenseitig zu beeinflussen. Bearbeitbar sowohl hier im
  Prüfgrundlage-Formular als auch direkt im KV-Vorschlag (Sicherheit-/
  Normprüfung, FFU/Fitting, NGO — siehe oben „Kommentar direkt bearbeiten"),
  beide Stellen zeigen und ändern denselben Wert.

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
  Prüfgrundlagen verknüpft (siehe oben). Die **Auswahlleiste (Liste) zeigt
  neben der Bezeichnung jetzt auch den Titel** der Norm (sofern hinterlegt) —
  praktisch, um Normen mit kryptischer Bezeichnung (z. B. reine Normnummern)
  auf einen Blick zu erkennen, ohne jede einzeln öffnen zu müssen. Über der
  Liste steht ein eigenes **Suchfeld** (Bezeichnung, Titel, Dateiname,
  Bemerkung, Anwendungsbereiche) —
  synchron mit der allgemeinen Suche oben im Header, beide filtern dieselbe
  Liste, welches der beiden Felder benutzt wird ist egal. Darunter der
  **Typ-Filter** (Alle/Normen/PPM/PPM_FFU/StiWa) als eigenständige, frei
  umbrechende Pillen-Gruppe statt eines starren Segment-Balkens — bleibt auch
  bei allen fünf Optionen in der schmalen Listen-Spalte sauber lesbar, egal
  ob ein-, zwei- oder mehrzeilig. Suche und Typ-Filter lassen sich
  kombinieren. Über **„📄 Norm(en)/Prüfprogramm(e)
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

  Jede Norm hat außerdem ein eigenes, frei editierbares **SAP-Code**-Feld
  (SAP-Material). Wird diese Norm in einer Prüfgrundlage referenziert, fließt
  ihr SAP-Code automatisch in die daraus im KV erzeugte mechanische
  Prüfposition ein (Hauptprodukt/Set-Bestandteile bei Sicherheit & Norm sowie
  FFU/NGO) — referenziert ein Block mehrere Normen, zählt der SAP-Code der
  ersten Norm mit hinterlegtem Wert.

  Zwei weitere Checkboxen legen fest, ob die Norm **Kennzeichnungsanforderungen**
  bzw. **Anforderungen an die Bedienungsanleitung** enthält — diese Angabe
  wird nur noch hier an der Norm gepflegt, nicht mehr manuell an jeder
  einzelnen Prüfgrundlage (siehe Reiter „Prüfgrundlagen" oben: die
  Übernahme erfolgt automatisch, sobald die Norm dort referenziert wird,
  außer bei „in Anlehnung an" — dort nur auf ausdrücklichen Wunsch je
  Referenz).

  Jede Norm lässt sich außerdem einer **Prüfungsart** zuordnen (Dropdown,
  Startbestand „Sicherheit-/Normprüfung", „Kennzeichnung",
  „Produktspezifikation") — die Auswahlmöglichkeiten selbst sind frei
  editierbar im Reiter „Verwaltung" → Ansicht „Prüfungsarten" (anlegen,
  umbenennen, löschen; Umbenennen aktualisiert automatisch alle Normen, die
  die bisherige Prüfungsart verwenden, analog zu „Bereiche"). Alle Normen mit
  Prüfungsart „Kennzeichnung" werden im KV-Reiter direkt im
  Kennzeichnung-Block aufgelistet (siehe oben).

  **Kosten direkt an der Norm**: für alle Normen mit einer Prüfungsart
  außer „Sicherheit-/Normprüfung" (also z. B. Kennzeichnung,
  Produktspezifikation oder frei angelegte weitere Arten wie „Sonstige")
  erscheint zusätzlich ein Feld **„Kosten €"**, mit dem sich ein fester
  Preis direkt an der Norm/dem PPM selbst hinterlegen lässt. Das ist bewusst
  anders als bei der Sicherheit-/Normprüfung: dort kommen die Kosten
  weiterhin ausschließlich aus der jeweiligen Prüfgrundlage (siehe
  „Kosten (Prüfgrundlage) €" oben), weil dieselbe Norm dort je Produkt
  unterschiedlich bepreist sein kann — bei den übrigen Prüfungsarten ist der
  Preis dagegen üblicherweise für alle Produkte gleich. Aktuell wird dieser
  Wert im Kennzeichnung-Block als Preis der Position übernommen, sobald sie
  einem KV hinzugefügt wird (siehe oben); für andere Prüfungsarten ist er
  vorerst reine Datenerfassung ohne automatische Auswirkung im KV.

  **Anwendungsbereiche**: manche Normen stellen je nach Verwendungszweck des
  Produkts unterschiedliche Anforderungen — z. B. hat DIN EN 581-2
  unterschiedliche Anforderungen für Camping-, Wohn- und Objektbereich. Über
  „+ Anwendungsbereich hinzufügen" lässt sich pro Norm eine beliebige Anzahl
  solcher Bereiche anlegen (freier Name, z. B. „Campingbereich", plus
  Freitext für die dort geltenden Anforderungen) — frei bearbeitbar,
  zusammenführbar, löschbar, unabhängig von einer festen Klausel-Nummerierung
  der Norm. **Welcher Anwendungsbereich gilt, lässt sich an zwei Stellen
  wählen**: optional schon **beim Referenzieren der Norm in einer
  Prüfgrundlage** (dort als Vorbelegung für alle KVs mit dieser
  Prüfgrundlage gedacht — praktisch, wenn derselbe Bereich für die meisten
  Projekte passt) und **spätestens beim tatsächlichen Hinzufügen der
  Norm-Position zu einem konkreten Kostenvoranschlag** (Warengruppen-
  Empfehlung, neben „+ hinzufügen" — analog zur Style-Zuordnung): das
  Dropdown dort startet mit der Vorbelegung aus der Prüfgrundlage (falls
  gesetzt), lässt sich aber **projektspezifisch überschreiben** — zwei KVs
  mit derselben Prüfgrundlage können also trotzdem unterschiedliche
  Anwendungsbereiche wählen, ohne die gemeinsame Prüfgrundlage zu verändern.
  Wurde an der Prüfgrundlage gar kein Bereich vorbelegt, startet die Auswahl
  im KV bei „kein bestimmter Bereich" und muss dort bei Bedarf getroffen
  werden, da es sonst keinen anderen Ort mehr dafür gibt. Die Auswahl im KV
  fließt direkt in die Bezeichnung der neu angelegten Position ein (z. B.
  „…DIN EN 581-2 [Campingbereich]"). Normen ohne Anwendungsbereiche zeigen
  kein Dropdown. Kosten werden bewusst **nicht** zentral an der Norm
  hinterlegt, sondern wie gehabt individuell **je Prüfgrundlage-Referenz**
  gepflegt (siehe „Kosten je Norm" oben, im Reiter Prüfgrundlagen) — dort
  findet die Kostenangabe bereits statt.

  Die Detailansicht einer Norm zeigt außerdem eine schreibgeschützte
  **„Verwendet in Prüfgrundlagen"-Übersicht**: für jede Prüfgrundlage, die
  diese Norm in einem ihrer drei Prüfblöcke referenziert, eine Zeile mit
  Produkt, Warengruppe, Block (Sicherheit & Norm/FFU/StiWa), dem dort
  **vorbelegten Anwendungsbereich** (Spalte erscheint nur, wenn die Norm
  welche definiert hat) und den dort **je Produkt hinterlegten Kosten** —
  Kosten hängen ja an der jeweiligen Prüfgrundlage, nicht an der Norm selbst
  (siehe „Kosten je Norm" oben). Klick auf eine Zeile springt direkt zur
  Detailansicht der jeweiligen Prüfgrundlage.

  **Sortierung der Normen-Liste**: alphabetisch, aber Bezeichnungen, die mit
  einem Buchstaben beginnen, immer vor solchen, die mit einer Ziffer beginnen
  (z. B. „DIN EN 581-2" vor „102_PPM") — eine reine Sprach-Sortierung würde
  Ziffern meist vor Buchstaben einordnen, was hier bewusst umgangen wird.
  Innerhalb der beiden Gruppen gilt normale alphabetische bzw. numerische
  Sortierung (z. B. „102_PPM" vor „163_PPM" vor „2_PPM").

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
- **MAK (Materialanforderungskatalog)** – Referenzliste, beginnend mit den
  193 offiziellen Zeilen (Spalten ID/Kategorie/Bereich/Parameter/Anforderung/
  Norm-EU/Norm-US/Mindest-Prüfnachweis), im gleichen Listen-/Detail-Layout
  wie der Reiter „Normen" — **vollständig editierbar und um eigene
  Positionen erweiterbar**, nicht mehr schreibgeschützt: **„+ Neue
  MAK-Position (manuell)"** legt einen leeren Entwurf an (mit provisorischer,
  aber eindeutiger ID zum sofortigen Umbenennen), alle Felder der
  Detailansicht (ID, Parameter, Kategorie, Bereich, Anforderung, Norm/
  Standard EU, Norm/Standard US, Mindest-Prüfnachweis) sind direkt editierbar
  und speichern bei jeder Änderung sofort; **„MAK-Eintrag löschen"** entfernt
  einen Eintrag dauerhaft (mit Sicherheitsabfrage). Die **ID lässt sich
  umbenennen**, wird dabei aber auf Eindeutigkeit geprüft — ein Duplikat wird
  abgelehnt (Hinweis + Zurücksetzen auf den vorherigen Wert). Die
  **Parameter-Bezeichnung ist das Hauptattribut**: sie steht fett in der
  Liste und als Überschrift in der Detailansicht, die ID erscheint nur noch
  als Zusatzangabe im Formular; die Liste ist entsprechend primär nach
  Parameter alphabetisch sortiert (a-z), nicht nach ID. Eine
  **übergeordnete Textsuche** (durchsucht alle Felder inkl. Schlagworte,
  synchron mit der allgemeinen Suche oben im Header wie beim Normen-Tab)
  lässt sich mit zwei weiteren Filtern kombinieren: einem
  **Kategorie-Dropdown** (die Kategorien der Liste, z. B. „Akku",
  „Textilphysik") und einem **ID-Textfilter** (Teilstring-Suche, z. B. „TX00"
  oder „BA"). Alle drei Filter wirken gemeinsam. Bei den offiziellen
  Einträgen wurde in „Kategorie" und „Mindest-Prüfnachweis" die englische
  Übersetzung aus der Original-Vorlage (jeweils nach einem „/") entfernt; in
  den übrigen Spalten ist „/" auch regulärer Bestandteil des deutschen Texts
  bzw. Trennzeichen zwischen mehreren Normen/Werten (z. B. „2100 mAh / 2400
  mAh", „DIN EN ISO 105/X12") und bleibt daher unverändert. CSV-Export wie
  bei den anderen Reitern verfügbar (exportiert die aktuell gefilterte
  Liste, inkl. Schlagworte-Spalte).

  **Abrechnung: Pro Artikel oder pro Laufzeit** – jeder MAK-Parameter hat ein
  eigenes Dropdown **„Abrechnung"**, das festlegt, wie er bepreist wird:
  - **„Pro Artikel (mit Staffelung)"** (Standard) – der Parameter trägt einen
    einzelnen **„Preis €"**, der beim Hinzufügen einer Position automatisch
    als Kosten übernommen wird und in der Detailansicht wie im KV-Reiter
    neben dem Parameter-Titel erscheint. Zusätzlich lässt sich eine
    **„Staffelung je weiterem Artikel €"** hinterlegen (analog zu „Kosten je
    weiterem Produkt" bei Normen) — ein reduzierter Preis für jeden weiteren
    gleichzeitig geprüften Artikel. Das ist eine reine Referenzangabe: sie
    wird **nicht automatisch verrechnet**, sondern dient als Orientierung
    beim manuellen Anpassen von Kosten/Anzahl der Position.
  - **„Pro Laufzeit (feste Preise)"** – für Parameter mit LIDL-seitig fest
    verhandelten Preisen je Laufzeit (z. B. Korrosionsbeständigkeit: 24h,
    48h, 72h, 96h, 120h, 240h …, teils zusätzlich nach Kammergröße oder
    Paketpreis-Gruppe gestaffelt). Statt eines einzelnen Preisfelds gibt es
    hier eine frei editierbare Liste **„Laufzeiten/Preise"** — jede Zeile mit
    eigener Bezeichnung, Preis, optionalem SAP-Code und Hinweis, per **„+
    Laufzeit/Preis hinzufügen"** beliebig erweiterbar und einzeln löschbar
    (identisches Editier-Muster wie bei den Anwendungsbereichen im
    Normen-Tab). Im KV-Reiter erscheint dann statt eines einzelnen **„+
    hinzufügen"** je Laufzeit eine eigene Zeile mit ihrem tatsächlichen
    Preis/SAP-Code zum Hinzufügen, darunter jeweils sichtbar der hinterlegte
    **Hinweis** (nicht nur als Hover-Tooltip), sowie darunter immer eine
    Eingabe **„Freie Laufzeit (nicht in der Liste)"** (Bezeichnung + Preis),
    für Laufzeiten außerhalb der festen Liste — landet als eigene Position
    mit demselben Bezeichnungsschema wie die festen Varianten, aber frei
    eingebbarem Preis (siehe Produktspezifikationen oben). Ein Umschalten
    zwischen beiden Modi ist jederzeit möglich, die jeweils nicht
    aktiven Felder bleiben dabei im Hintergrund erhalten.

  Die 24 Parameter mit bereits migrierten LIDL-Preisen aus dem früheren,
  eigenständigen Parameterkatalog (u. a. Korrosionsbeständigkeit) starten
  automatisch im Modus „Pro Laufzeit"; alle übrigen starten bei „Pro
  Artikel".

  **Bewertungsgrundlage/Grenzwert erforderlich** – eine eigene Checkbox in
  der Detailansicht markiert Parameter, bei denen im KV zusätzlich eine
  konkrete, produktspezifische Bewertungsgrundlage oder ein Grenzwert
  angegeben werden muss (z. B. eine bestimmte Norm-Grenze oder ein
  Toleranzwert) — unabhängig vom Abrechnungsmodus. Die Markierung selbst
  gilt für den Parameter allgemein; der tatsächliche Wert ist **rein
  produktspezifisch** und wird deshalb **nicht** hier am MAK-Eintrag
  gespeichert, sondern erst beim Hinzufügen zu einem KV direkt an der
  jeweiligen Position (siehe Kostenvoranschläge oben).

  **Schlagworte je Eintrag** – in der Detailansicht lassen sich beliebig
  viele Schlagworte als Chips hinzufügen (Eingabefeld + „+ Hinzufügen" oder
  Enter-Taste) und über das „×" am jeweiligen Chip wieder entfernen;
  Duplikate (unabhängig von Groß-/Kleinschreibung) werden automatisch
  abgefangen. Sie tragen die Signalwörter, die in den Abschnitten „Qualität"
  oder „Material" eines Prüfauftrags stehen müssen, damit dieser Parameter
  relevant ist: im KV-Reiter (Block Produktspezifikationen) werden
  Fundstellen dieser Schlagworte im Qualität-/Material-Text automatisch fett
  hervorgehoben, und der zugehörige Parameter erscheint dort zusätzlich als
  klickbarer Vorschlag (siehe oben). Schlagworte fließen außerdem in die
  übergeordnete Textsuche mit ein und werden dauerhaft in der lokalen
  Datenablage gespeichert. Dieselbe Detailansicht (Felder, Schlagworte) ist
  auch direkt im KV-Reiter über das MAK-Dropdown erreichbar (siehe oben) —
  beide teilen sich dieselben Daten.
- **Verwaltung** – **sechs umschaltbare Ansichten** (Pillen oben im Reiter:
  „Bereiche" / „Warengruppen" / „Prüfungsarten" / „Trivialartikel-Preisliste" /
  „Prüfumfang je Artikelkategorie" / „Gefahrenzone"), von denen jeweils nur
  eine gleichzeitig sichtbar ist —
  analog zum Ansicht-Umschalter im Reiter „Prüfgrundlagen" (siehe oben),
  statt einer langen Scroll-Seite mit allen Blöcken untereinander. Die
  Stammdaten-Listen sind zusätzlich bei mehr als einer Bildschirmseite an
  Einträgen paginiert (Standardgröße 25 Bereiche/Prüfungsarten bzw. 50
  Warengruppen/Trivialartikel-Zeilen pro Seite, „‹ Zurück"/„Weiter ›"
  darunter):
  - **Bereiche** – Dropdown-Quelle im Reiter „Prüfgrundlagen". Neue Werte
    anlegen, bestehende umbenennen (aktualisiert automatisch alle
    Prüfgrundlagen, die den bisherigen Wert verwenden) oder löschen (mit
    Warnhinweis, falls der Wert noch verwendet wird). Neben den ursprünglich
    aus den Prüfgrundlagen-Startdaten abgeleiteten Werten sind hier
    zusätzlich die offiziellen „EK-Säulen" aus der
    Warengruppenzuordnung-Tabelle (Stand 01.03.2026) vorbelegt (z. B.
    „Baumarkt", „Küche & Haushalt", „Wohnen & Einrichten", diverse
    Bekleidungs-Säulen) — der Wert „keine Zuordnung" einzelner Warengruppen
    wurde bewusst nicht als Bereich übernommen. Bereiche, deren Name nur
    durch eine angehängte einzelne Zahl unterschieden wird (z. B. ursprünglich
    „Baumarkt 1"/„Baumarkt 2"), werden automatisch zu einem gemeinsamen
    Bereich ohne Zahl zusammengefasst (inkl. Kaskade auf betroffene
    Prüfgrundlagen) — das gilt auch für künftig von Hand angelegte, ähnlich
    benannte Bereiche.
  - **Warengruppen** – eine gemeinsame Liste aus Warengruppen-Stammdaten
    (Code + Bezeichnung + Bereich) und der Neu-↔-Alt-Zuordnung (viertes Feld
    „Warengruppe alt"), damit die Verlinkung zwischen neuer und alter
    Warengruppe direkt hier sichtbar und editierbar ist, statt in zwei
    getrennten Listen. Code + Bezeichnung speisen die Dropdowns im Reiter
    „Prüfgrundlagen" und bei „Warengruppe (neu)" im Kostenvoranschlag;
    Ändern von Code oder Bezeichnung aktualisiert automatisch alle
    Prüfgrundlagen und Kostenvoranschläge mit dem bisherigen Code. Ändern
    von „Warengruppe alt" befüllt automatisch „Warengruppe (alt)" im
    Kostenvoranschlag (nur wenn dort noch leer). Das Feld **Bereich**
    (Dropdown aus der Bereiche-Liste, siehe oben) ordnet die Warengruppe
    einem Bereich zu — diese Zuordnung speist die Bereich-Ansicht im Reiter
    „Prüfgrundlagen" (siehe dort). Ein Code kann auch nur in einer der
    beiden Quellen (Stammdaten/Zuordnung) vorkommen; solche Zeilen zeigen
    die Bezeichnung als „– noch keine Bezeichnung –" statt den Code doppelt
    (einmal als Code, einmal als Platzhalter-Bezeichnung) anzuzeigen. Wird
    im PA eine noch unbekannte Warengruppe gelesen und automatisch in einen
    KV übernommen, landet sie ebenfalls automatisch hier als Zeile
    (zunächst ohne eigene Bezeichnung/Bereich), statt das Dropdown mit einem
    unbekannten Wert leer zu lassen. Löschen entfernt sowohl den Stammdaten-
    als auch den Zuordnungs-Eintrag für diesen Code und warnt bei noch
    bestehender Verwendung in Prüfgrundlagen.

    Code+Bezeichnung+Bereich sind mit der vollständigen offiziellen
    Warengruppen-Stammdaten-Tabelle (Stand 01.03.2026, 730 eindeutige Codes
    über alle Warenbereiche) vorbelegt — bei bereits vorhandenen Codes wird
    die Bezeichnung dabei einmalig auf den offiziellen Wortlaut
    aktualisiert (kaskadiert wie eine manuelle Umbenennung auf verknüpfte
    Prüfgrundlagen) und der Bereich ergänzt, fehlende Codes werden neu
    angelegt. Diese Aktualisierung läuft nur **einmal** je Installation
    (intern über einen Merker gesteuert) — spätere manuelle Umbenennungen im
    Reiter „Verwaltung" werden bei künftigen Ladevorgängen nicht wieder
    überschrieben. Die Neu-↔-Alt-Zuordnung selbst ist mit der vollständigen
    offiziellen ADMIN-Blatt-Zuordnungstabelle vorbelegt (341 eindeutige
    Neu-Codes; eine Handvoll Codes kam in der Rohliste mit mehreren
    unterschiedlichen Alt-Codes vor — dort zählt der jeweils zuerst
    genannte, von Hand hier korrigierbar; ein Eintrag ohne gültigen Alt-Code
    wurde beim Einlesen übersprungen). Die beiden Quellen (730
    Stammdaten-Codes, 341 Zuordnungs-Codes) überschneiden sich
    größtenteils, aber nicht vollständig, daher zeigt die vereinigte Liste
    geringfügig mehr als 730 Zeilen.
  - **Prüfungsarten** – Dropdown-Quelle für das Prüfungsart-Feld je Norm im
    Reiter „Normen" (siehe dort). Startbestand: „Sicherheit-/Normprüfung",
    „Kennzeichnung", „Produktspezifikation" — neue Werte anlegen, bestehende
    umbenennen (aktualisiert automatisch alle Normen, die die bisherige
    Prüfungsart verwenden) oder löschen (mit Warnhinweis, falls der Wert
    noch verwendet wird; bereits zugeordnete Normen behalten dabei den
    alten Textwert, analog zum Löschen eines Bereichs).
  - **Trivialartikel-Preisliste** – Preisliste für triviale Artikel je
    **alter** Warengruppe (Code wie im Feld „Warengruppe (alt)" im
    Kostenvoranschlag), mit der offiziellen Preisliste (69 Zeilen) als
    Startbestand: Bezeichnung, Preis „Chemie ≥4 Risikoparameter", Preis
    „VP & Kennzeichnung", Preis „LFGB Stichprobe" (nur bei relevanten
    Warengruppen befüllt), Gesamtpreis (inkl. 3 Sortierungen/Varianten) und
    Preis „Add Sortierung/Variante (ab der 4.)" — alle Felder direkt in der
    Zeile editierbar, neue Zeilen über das Formular darunter anlegen.
    **Angewendet wird davon aktuell nur der Preis „VP & Kennzeichnung"** (die
    übrigen Preise betreffen den chemischen Teil der Prüfung und sind noch
    nicht verdrahtet): sobald **Trivial = Ja** ODER die **Artikelkategorie
    des verknüpften Prüfauftrags „Grün*" (mit Stern)** ist — derselbe
    Artikelkreis, der auch von der Sicherheit-/Normprüfung-Pflicht befreit
    ist — UND sich zur „Warengruppe (alt)" des KVs ein Eintrag mit
    VP&Kennzeichnung-Preis in der Trivialartikel-Preisliste findet, gilt
    dieser Preis als Gesamtsumme für den Kennzeichnung-Block.

    **In allen anderen Fällen gilt stattdessen ein fester Standardpreis von
    360 €** für den gesamten Kennzeichnung-Block — der Kennzeichnung-Block
    kostet also **immer** entweder den Trivialartikel-Paketpreis oder
    pauschal 360 €, **nie** die Summe der an den einzelnen Kennzeichnung-
    Normen hinterlegten Kosten (diese werden für den Kennzeichnung-Block
    komplett ignoriert; die eigentlichen Norm-Kosten spielen nur außerhalb
    davon eine Rolle, z. B. bei „LIDL-spezifisch"-Normen). Der jeweils
    geltende Gesamtpreis wird **automatisch** gleichmäßig auf die im
    Kennzeichnung-Block bereits hinzugefügten, aktiven Positionen verteilt
    (nur eine aktiv → volle Summe dort) und läuft jedes Mal neu, sobald im
    Kennzeichnung-Block eine weitere Norm hinzugefügt wird; ein manueller
    Button ist dafür nicht mehr nötig. Ein Hinweis-Banner im Kennzeichnung-
    Block zeigt dabei immer, welcher der beiden Preise gerade greift.
    Stimmt die aktuelle Summe schon mit dem Gesamtpreis überein, zeigt das
    Banner „✓ verteilt", bei einer später manuell geänderten Summe „Summe
    weicht ab (manuell geändert?)". Ohne bereits hinzugefügte Kennzeichnung-
    Position bleibt der Hinweis reine Information ohne Verteilung.
  - **Prüfumfang je Artikelkategorie** – drei editierbare Prozentfelder
    (Grün/Grün*, Gelb, Rot/sonstige — Standard 40 %/50 %/60 %), sofort beim
    Verlassen des Felds gespeichert. Steuert zentral **beides zugleich**: den
    Artikelkategorie-Rabattfaktor auf die aus der Prüfgrundlage berechneten
    Kosten in der Sicherheit-/Normprüfung-Warengruppen-Empfehlung im Reiter
    „Kostenvoranschläge" sowie den Hinweistext „Teilprüfung: X% der
    Vollprüfung" an der jeweiligen Position (siehe dort) — beide bezogen
    dieselbe Artikelkategorie-Erkennung, „Grün" gilt mit und ohne Sternchen
    gleich.
  - **Gefahrenzone** – löscht **Arbeitsvorrat, Prüfaufträge und
    Kostenvoranschläge** unwiderruflich (zwei Sicherheitsabfragen), z. B. um
    nach dem Testen sauber mit echten Daten neu zu starten.
    **Prüfgrundlagen und Normen sowie die Bereiche-/Warengruppen-Stammdaten,
    die Warengruppen-Zuordnung, die Prüfungsarten und die
    Trivialartikel-Preisliste bleiben dabei erhalten** — die mühsam gepflegte
    Referenzdatenbank geht also
    nicht verloren. Vorher empfiehlt sich ein „⬇ Sichern (JSON)" oben. Da
    alle Daten ausschließlich lokal im Browser (Local Storage) liegen, lässt
    sich dieser Schritt nur über diesen Button hier im Tool selbst auslösen
    — von außen kann niemand auf diese Daten zugreifen.

## Datenquelle der Warengruppen-Empfehlung und SAP-Codes

Die Warengruppen-Mechanik-Referenz (185 Zeilen, jetzt der Reiter
„Prüfgrundlagen") und der Produktspezifikationen-Parameterkatalog (62 Zeilen)
stammen ursprünglich aus `Preisliste_Mechanik_v2.xlsm` (Blätter „Mechanik" und
„Produktspezifikationen") und sind der **Startbestand** beim allerersten
Öffnen des Tools. Die Prüfgrundlagen sind seitdem über den gleichnamigen
Reiter bearbeit- und erweiterbar (siehe oben); der Produktspezifikationen-
Katalog ist weiterhin nur durchsuchbar, nicht editierbar — bei Bedarf bitte
Bescheid geben, dann wird das analog nachgerüstet.

Den früheren eigenständigen Reiter „Prüfpositionen-Katalog" gibt es nicht
mehr. Positionen, die an einer Norm/Prüfgrundlage hängen (Hauptprodukt und
Set-Bestandteile bei Sicherheit & Norm, FFU, NGO/StiWa), holen ihren
**SAP-Code jetzt direkt von der referenzierten Norm** — im Reiter „Normen"
gibt es dafür ein eigenes, editierbares **SAP-Code-Feld** je Norm/PPM (analog
zu Bezeichnung, Typ und Bemerkung); referenziert eine Prüfgrundlage mehrere
Normen in einem Block, zählt der SAP-Code der ersten Norm mit hinterlegtem
Wert. Die übrigen festen Positionen ohne direkten Prüfgrundlage-Bezug (die
vier Kennzeichnung-Varianten, Bedienungsanleitung, Optischer Abgleich,
Akkusicherheitskurzcheck sowie die generischen FFU/NGO/Referenzprüfung-
Einträge) bekommen beim ersten Start automatisch **je eine gleichnamige
Norm im Reiter „Normen"** (Typ „PPM"), damit auch ihr SAP-Code dort zentral
auffindbar und editierbar ist, statt nur „irgendwo im Code" zu stecken —
wird eine solche Norm dort umbenannt, verliert sie diese Verknüpfung
allerdings (der Abgleich läuft über die Bezeichnung); besser nur den
SAP-Code ändern, nicht die Bezeichnung. Nur „Projektkosten" (Produktspezi-
fikationen-Pauschale) hat mangels SAP-Code keine solche Norm. Die
ursprünglichen SAP-Codes wurden gegen die reale SAP-Bestellzeilen-Liste
(Blatt „SAP") korrigiert — u. a. „MECH_SICHERHEIT_TS" statt der zuvor
angenommenen „MECH_S_NORM_TS", und „FFU_TS" als gemeinsamer Code für
Optischer Abgleich/FFU/Referenzprüfung/NGO — und dienen jetzt als
Startwert dieser Normen bzw. als Fallback, solange eine referenzierte Norm
noch keinen eigenen SAP-Code hat. Das freie Dropdown „Position aus Katalog
wählen" im KV ist entsprechend entfallen — für Einzelfälle bleibt
„+ Freie Position".

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

Die vollständige, offizielle **Warengruppen-Liste** (Code+Bezeichnung, 730
Zeilen über alle Warenbereiche) liegt inzwischen als Startbestand vor (siehe
oben) und lässt sich bei Bedarf weiterhin frei im Reiter „Verwaltung"
pflegen. Die reine **Neu→Alt-Zuordnung** (das Feld „Warengruppe alt" in
derselben Verwaltungsliste, unabhängig von Code/Bezeichnung, separate Quelle
vom ADMIN-Blatt) liegt ebenfalls bereits als Startbestand vor (siehe oben)
und befüllt „Warengruppe (alt)" im Kostenvoranschlag automatisch.

## SharePoint-Suche nach IAN

Neben jeder IAN (in der Arbeitsvorrat-Tabelle sowie auf den Detailseiten von
Prüfaufträgen und Kostenvoranschlägen) steht ein kleines 🔍-Symbol. Ein Klick
öffnet in einem neuen Tab die SharePoint-Suche
(`https://sgs.sharepoint.com/sites/de-cp-hamfiles/_layouts/15/search.aspx/siteall`)
direkt mit dieser IAN als Suchbegriff — praktisch, um schnell vorhandene
Unterlagen zu dieser IAN zu finden. Ohne IAN erscheint kein Symbol.

## Toolbar (oben, bereichsübergreifend)

- **⬇ Sichern (JSON)** / **⬆ Datei laden (JSON)** – kompletter Stand
  (Arbeitsvorrat + PA + KV + Prüfgrundlagen + Normen) als Datei sichern bzw.
  laden.
- **🔀 Zusammenführen (JSON)** – Arbeitsstände mehrerer Personen/Rechner
  zusammenführen, mit Konfliktanzeige ("Aktuell behalten" / "Aus Datei
  übernehmen") — deckt inzwischen **alle** Datenbereiche ab: Arbeitsvorrat,
  Prüfaufträge, Kostenvoranschläge, Prüfgrundlagen, Normen, MAK,
  Warengruppen, Warengruppen-Zuordnung, Trivialpreisliste sowie Bereiche und
  Prüfungsarten (letztere beide als reine Werte-Listen ohne Unterfelder,
  daher dort nur "neu hinzufügen", kein Feld-Konflikt möglich). Bei
  Warengruppen/Bereichen sortiert sich die Liste nach neu hinzugefügten
  Einträgen automatisch neu ein (wie beim manuellen Anlegen im Reiter
  „Verwaltung"). Erkennung läuft je Bereich über einen fachlichen Schlüssel
  (z. B. IAN bei Arbeitsvorrat/PA, Warengruppe+Produkt bei Prüfgrundlagen,
  Bezeichnung bei Normen, ID bei MAK, Code bei Warengruppen/Trivialpreisliste)
  statt über interne, pro Rechner zufällig vergebene IDs — zwei unabhängig
  voneinander angelegte, aber inhaltlich gleiche Einträge werden so trotzdem
  korrekt als derselbe erkannt.

  **Löschungen werden beim Zusammenführen mitgenommen:** wird ein Eintrag
  (Arbeitsvorrat, Prüfauftrag, KV, Prüfgrundlage, Norm, MAK oder
  Trivialpreisliste-Eintrag) gelöscht, merkt sich das Tool das im Hintergrund
  ("Tombstone"). Beim Zusammenführen zweier Arbeitsstände gilt dadurch: ein
  hier bereits gelöschter Eintrag taucht nicht wieder als "neu" auf, nur weil
  die eingespielte Datei ihn noch enthält. Umgekehrt zeigt das Tool, wenn ein
  Eintrag auf dem *anderen* Gerät gelöscht wurde, hier lokal aber noch
  vorhanden ist, einen eigenen Abschnitt „🗑 Auf einem anderen Gerät gelöscht"
  mit Checkbox (per Default angehakt) — erst nach „Zusammenführung
  übernehmen" wird er auch hier tatsächlich entfernt, sodass sich Löschungen
  zuverlässig über mehrere Geräte durchsetzen, auch wenn mehr als zwei Geräte
  im Umlauf sind.
- **📄 CSV-Export** – exportiert die Tabelle des gerade offenen Reiters als
  `.csv`, direkt in Excel öffenbar.

Alle Änderungen werden automatisch im Browser (Local Storage) auf diesem PC
gespeichert. Der Speicher ist an die jeweilige Datei/den Dateipfad gebunden —
eine **neue Version dieser Datei startet deshalb mit einem eigenen, leeren
Speicher** und übernimmt Änderungen aus einer älteren Version nicht
automatisch. Vor dem Wechsel auf eine neue Version deshalb erst **⬇ Sichern
(JSON)** in der alten Datei, danach in der neuen Datei **🔀 Zusammenführen
(JSON)** (empfohlen, zeigt Konflikte Feld für Feld) oder **⬆ Datei laden
(JSON)** (ersetzt den kompletten Stand). Für Backup/Weitergabe/Zusammenführen
über mehrere Rechner ebenfalls die JSON-Funktionen benutzen.

**Warnung bei vollem Browser-Speicher:** der Local Storage jeder Datei hat ein
festes Größenlimit (browserabhängig, i. d. R. wenige MB). Wird dieses Limit
erreicht, kann nicht mehr automatisch gespeichert werden — früher blieb das
fast unbemerkt (nur eine unauffällige Statuszeile), sodass der zuletzt
eingegebene Stand zwar noch auf dem Bildschirm sichtbar war, beim Schließen
oder Neuladen der Datei aber verloren ging. Jetzt wird ein solcher Fehler
laut gemeldet: die Statuszeile zeigt „⚠ NICHT gespeichert - Speicher voll!",
zusätzlich erscheint ein Hinweisfenster und es wird automatisch eine
Notsicherungs-Datei heruntergeladen (`kv-monitoring_NOTSICHERUNG_…json`, im
selben Format wie „⬇ Sichern (JSON)"). Diese Datei aufbewahren und in einer
neuen/leeren Version dieses Tools über **🔀 Zusammenführen (JSON)** wieder
einspielen. Das Hinweisfenster erscheint nur einmal pro Fehler-Serie (kein
Alert bei jedem Tastendruck), sobald wieder erfolgreich gespeichert werden
konnte, wird bei einem erneuten Fehler wieder gewarnt.

**Reiter „Normen" startet nicht mehr leer:** anders als früher enthält eine
frische Datei jetzt einen mitgelieferten **Startbestand** an Normen (Stand
eines Datenexports), genau wie die übrigen Stammdaten (Prüfgrundlagen, MAK,
Warengruppen …) das schon immer taten. Eigene, im Browser bereits vorhandene
Normen werden dadurch nie überschrieben — der Startbestand greift nur, wenn
der lokale Speicher für Normen leer ist.

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
