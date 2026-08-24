Attribute VB_Name = "Modul1"
' ============================================================================
' Ersetzt den Inhalt von Sub Mec() im vorhandenen VBA-Modul "Modul1" der Datei
' IAN_CHARGE_AB_ARTIKEL...xlsm. Der Button "Mechanik einfügen" auf dem Blatt
' "Inspection Booking" ruft bereits diese Sub auf (siehe FmlaMacro "[0]!Mec")
' - es muss also NUR der Code dieser Sub ersetzt werden, der Button selbst
' bleibt unverändert und funktioniert danach automatisch mit dem neuen Ablauf.
'
' Workflow:
'   1. Im KV-Monitoring-Tool den gewünschten Kostenvoranschlag öffnen und im
'      Block "Mechanische Prüfpositionen" auf "📋 In Zwischenablage kopieren"
'      klicken (die Tabelle ist dort automatisch nach Kategorie sortiert:
'      Sicherheit-/Normprüfung, Produktspezifikation, FFU/Fitting, NGO,
'      Referenzprüfung).
'   2. In dieser Excel-Datei zum passenden Blatt "Inspection Booking"
'      wechseln und auf den Button "Mechanik einfügen" klicken.
'
' Nur AKTIVE Positionen (Spalte "Aktiv" = "Ja") werden übernommen. Jede
' Position wird als NEUE Zeile in die Tabelle "Mechanik_30SER" eingefügt -
' es wird NICHT versucht, Positionen automatisch den vorhandenen
' Standardzeilen (Akkusicherheitskurzcheck, Kennzeichnung GER, Optischer
' Abgleich, Klimawechselprüfung, UV-Beständigkeit, ...) zuzuordnen, da einige
' davon eigene, vom Trivial-/DokCheck-Status abhängige Preisformeln enthielten
' (siehe unten - diese Formeln wurden jetzt allerdings entfernt, die Werte
' bleiben also einfach als zuletzt eingegebene/berechnete Zahl stehen, bis sie
' manuell geändert werden). Diese Zeilen bleiben unangetastet - wer sie
' braucht, aktiviert sie weiterhin wie bisher manuell (Spalte "FILTER" = "x").
'
' Vor jedem Import werden zunächst alle vorbelegten "x"-Markierungen in Spalte F (FILTER) der
' bestehenden Standardzeilen entfernt - AUSGENOMMEN die fünf Kategorie-Überschriften-Zeilen
' ("Sicherheit & Norm ...", "(physikalische-) Produktspezifikation", "FFU/Fitting",
' "Referenzprüfung", "NGO"). So zählen nur noch die Positionen, die tatsächlich aus dem aktuellen
' KV-Monitoring-Export stammen - nicht mehr die als Vorlage vorbelegten Standard-Haken. Am Ende wird
' die Tabelle automatisch auf Spalte F = "x" gefiltert (bisher der separate Button/das separate
' Makro "Spalte_Filter"), sodass nur die aktiven Zeilen sichtbar bleiben. Eine
' Kategorie-Überschriften-Zeile bleibt dabei nur sichtbar, wenn dieser Block auch tatsächlich
' Positionen enthält - für einen Block ohne ausgewählte Prüfungen erscheint gar keine Überschrift
' mehr (früher stand dort eine leere Überschrift mit Summe 0), siehe Mec_KategorieSummeSchreiben.
'
' WICHTIG - Kategorie-Überschriften-Zeilen sind jetzt REINE Überschriften- UND Summenzeilen ohne
' eigene Formel: Die ursprünglichen Formeln in diesen fünf Zeilen (SUMPRODUCT für Sicherheit & Norm/
' Produktspezifikation, die INDEX/MATCH-Preistabellen-Abfrage für Produktspezifikation sowie die
' IF(...)-Summenformeln bei FFU/Fitting, Referenzprüfung, NGO) wurden ENTFERNT. Die komplette Logik
' steckt jetzt in Mec_KategorieSummeSchreiben: nach jedem Import werden für jede der fünf Kategorien
' NUR die tatsächlich ausgewählten, zugehörigen Positionszeilen (Spalte E = Kürzel, Spalte F = "x",
' außer der Überschriften-Zeile selbst) aufsummiert (Kosten × Anzahl) und das Ergebnis als FESTER
' Zahlenwert (keine Formel mehr) in die Kosten-/Summenspalte der jeweiligen Überschriften-Zeile
' geschrieben. Der frühere Pauschal-Aufschlag von 190 € (bzw. 250 € bei "MAK Pilot") aus der Tabelle
' "Kostentabelle" für Produktspezifikation ist hinfällig und wurde komplett entfernt - Produkt-
' spezifikation wird jetzt exakt wie die übrigen vier Kategorien behandelt.
' ACHTUNG: Da es sich um FESTE Werte statt Formeln handelt, aktualisieren sich diese Summen NICHT
' mehr automatisch, wenn z. B. manuell eine Kosten-Zelle geändert oder eine FILTER-Markierung
' nachträglich umgesetzt wird - dafür muss "Mechanik einfügen" erneut ausgeführt werden (aktualisiert
' die Summen auch dann korrekt neu, auch ganz ohne etwas Neues aus der Zwischenablage einzufügen,
' solange die Zwischenablage nicht leer ist).
'
' Da "Mechanik_30SER" eine echte Excel-Tabelle ist (ListObject), erweitert Excel beim Einfügen neuer
' Zeilen automatisch die "ZWISCHENSUMME MECHANIK"-Formel (=SUM(I48:I67), liegt UNTERHALB der Tabelle
' und wurde bewusst NICHT angetastet) sowie die SUMIF-Formeln der Kopfübersicht weiter oben im Blatt
' (FFU/Fitting, Referenzprüfung, NGO) - dafür muss jede neue Zeile innerhalb des bestehenden
' Tabellenbereichs eingefügt werden, nie dahinter. Jede neue Positionszeile landet direkt NACH der
' zugehörigen Kategorie-Überschriften-Zeile (bzw. bei NGO als letzte Zeile ganz am Ende der
' Tabelle, da keine weitere Kategorie mehr folgt) - siehe Mec_ZeileEinfuegen.
'
' Spalte L (bisher komplett ungenutzt) wird für die "Bemerkung" jeder neuen Zeile verwendet - dort
' landet die automatische Teilprüfung-Angabe der Sicherheit-/Normprüfung-Position (Prozentsatz je
' nach Artikelkategorie - Grün 40 %, Gelb 50 %, Rot/unbekannt 60 %, siehe teilpruefungProzentsatz im
' KV-Monitoring-Tool) sowie alle in der Prüfpositionstabelle automatisch aggregierten Bemerkungen
' (siehe positionBemerkungen: frei eingetragene Bemerkung, Bewertungsgrundlage/Grenzwert,
' Norm-Bemerkung, Prüfgrundlage-Kommentar, MAK-Hinweis, Kennzeichnungs-/Bedienungsanleitung-
' Anforderung), damit diese Angaben auch in der Excel-Datei nicht verloren gehen.
' Zusätzlich steht dieselbe Bemerkung nach einem Zeilenumbruch MIT in Spalte D, also in derselben
' Zelle wie der Parameter/die Bezeichnung (Zeilenumbruch-Formatierung wird dafür gesetzt) - so ist
' sie direkt beim Parameter sichtbar, auch wenn Spalte L ausgeblendet ist.
'
' WICHTIG: Bitte zunächst an einer KOPIE der Datei testen und die Summen
' hinterher prüfen, bevor produktiv damit gearbeitet wird - das Makro wurde
' anhand der Formelstruktur analysiert, aber nicht in echtem Excel getestet
' (dieses Tool läuft in einer Linux-Umgebung ohne Excel).
' ============================================================================

Sub Mec()
'
' Mec Makro ("Mechanik einfügen")
' Importiert die per "In Zwischenablage kopieren" aus dem KV-Monitoring-Tool
' kopierte Positionsliste (tabulatorgetrennt: Aktiv / Kategorie / Bezeichnung /
' Kürzel / SAP-Code / Kosten € / Anzahl / Summe € / Bemerkung) in die Tabelle
' "Mechanik_30SER" auf diesem Blatt und aktualisiert anschließend die
' Kategorie-Summen (siehe Kommentarblock oben).
'
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets("Inspection Booking")

    Dim tbl As ListObject
    Set tbl = ws.ListObjects("Mechanik_30SER")

    If Len(Trim(ws.Cells(47, 12).Value & "")) = 0 Then ws.Cells(47, 12).Value = "Bemerkung"   ' L47: Spaltenkopf einmalig ergänzen

    Dim clipText As String
    clipText = Mec_Zwischenablage()
    If Len(Trim(clipText)) = 0 Then
        MsgBox "Zwischenablage ist leer. Bitte zuerst im KV-Monitoring-Tool auf ""📋 In Zwischenablage kopieren"" klicken.", vbExclamation, "Mechanik einfügen"
        Exit Sub
    End If

    Dim zeilen() As String
    zeilen = Split(clipText, vbLf)

    Dim startIdx As Long
    startIdx = 0
    If UBound(zeilen) >= 0 And InStr(1, zeilen(0), "Bezeichnung", vbTextCompare) > 0 Then startIdx = 1

    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual

    Mec_AlteFilterZuruecksetzen tbl

    Dim eingefuegt As Long, uebersprungen As Long, warnungen As String
    Dim i As Long
    For i = startIdx To UBound(zeilen)
        Dim zeile As String
        zeile = Replace(zeilen(i), vbCr, "")
        If Len(Trim(zeile)) > 0 Then
            Dim spalten() As String
            spalten = Split(zeile, vbTab)
            If UBound(spalten) < 8 Then
                warnungen = warnungen & "Zeile " & (i + 1) & " übersprungen (zu wenige Spalten)." & vbCrLf
                uebersprungen = uebersprungen + 1
            Else
                Dim aktiv As String, bezeichnung As String, kuerzel As String, sapCode As String, bemerkung As String
                Dim kosten As Double, anzahl As Double
                aktiv = Trim(spalten(0))
                bezeichnung = Trim(spalten(2))
                kuerzel = UCase(Trim(spalten(3)))
                sapCode = Trim(spalten(4))
                kosten = Mec_Zahl(spalten(5))
                anzahl = Mec_Zahl(spalten(6))
                bemerkung = Trim(spalten(8))
                If anzahl = 0 Then anzahl = 1

                If aktiv <> "Ja" Then
                    uebersprungen = uebersprungen + 1
                ElseIf kuerzel <> "MS" And kuerzel <> "PS" And kuerzel <> "FFU" And kuerzel <> "REF" And kuerzel <> "NGO" Then
                    warnungen = warnungen & "Zeile " & (i + 1) & " (""" & bezeichnung & """) übersprungen - unbekanntes Kürzel """ & kuerzel & """." & vbCrLf
                    uebersprungen = uebersprungen + 1
                Else
                    Mec_ZeileEinfuegen tbl, kuerzel, bezeichnung, kosten, anzahl, sapCode, bemerkung
                    eingefuegt = eingefuegt + 1
                End If
            End If
        End If
    Next i

    Mec_SummenAktualisieren tbl, ws

    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
    ws.Calculate

    tbl.Range.AutoFilter Field:=4, Criteria1:="x"

    Dim meldung As String
    meldung = eingefuegt & " Position(en) eingefügt."
    If uebersprungen > 0 Then meldung = meldung & vbCrLf & uebersprungen & " Position(en) übersprungen (inaktiv oder unbekanntes Kürzel)."
    If Len(warnungen) > 0 Then meldung = meldung & vbCrLf & vbCrLf & warnungen
    MsgBox meldung, vbInformation, "Mechanik einfügen"
End Sub

' Entfernt alle vorbelegten "x"-Markierungen in Spalte F (FILTER) der bestehenden Zeilen der
' Tabelle Mechanik_30SER - AUSSER bei den fünf Kategorie-Überschriften-Zeilen (Spalte C gefüllt).
' Läuft VOR jedem Import, damit nur noch zählt, was tatsächlich aus dem aktuellen
' KV-Monitoring-Export als aktiv markiert wurde - nicht mehr die als Vorlage vorbelegten
' Standard-Haken (z. B. Kennzeichnung GER, Optischer Abgleich, Projektkosten).
Private Sub Mec_AlteFilterZuruecksetzen(tbl As ListObject)
    Dim zeile As ListRow
    For Each zeile In tbl.ListRows
        If Len(Trim(zeile.Range.Cells(1, 1).Value & "")) = 0 Then   ' Spalte C (1. Tabellenspalte) leer -> Detailzeile, keine Kategorie-Überschrift
            zeile.Range.Cells(1, 4).Value = ""                       ' Spalte F ist die 4. Tabellenspalte (C=1, D=2, E=3, F=4)
        End If
    Next zeile
End Sub

' Fügt EINE neue Positionszeile für die Kategorie "kuerzel" in die Tabelle Mechanik_30SER ein -
' direkt NACH der zugehörigen Kategorie-Überschriften-Zeile (bzw. bei NGO als letzte Zeile ganz am
' Ende der Tabelle, da nach NGO keine weitere Kategorie mehr folgt), damit die "ZWISCHENSUMME
' MECHANIK"-Formel unterhalb der Tabelle sowie die SUMIF-Formeln der Kopfübersicht (FFU/Fitting,
' Referenzprüfung, NGO) sich automatisch mit erweitern. Setzt bewusst KEINE Formel mehr in Spalte I
' (Summe) - die Kategorie-Summe wird komplett zentral in Mec_KategorieSummeSchreiben berechnet, die
' dafür direkt Kosten × Anzahl jeder mit "x" markierten Zeile derselben Kategorie liest.
Private Sub Mec_ZeileEinfuegen(tbl As ListObject, kuerzel As String, bezeichnung As String, kosten As Double, anzahl As Double, sapCode As String, bemerkung As String)
    Dim neuePosition As Long

    If kuerzel = "NGO" Then
        neuePosition = tbl.ListRows.Count + 1   ' ans Ende der Tabelle anhängen (keine nachfolgende Kategorie mehr)
    Else
        Dim ankerLabel As String
        Select Case kuerzel
            Case "MS": ankerLabel = "(physikalische-) Produktspezifikation"
            Case "PS": ankerLabel = "FFU/Fitting"
            Case "FFU": ankerLabel = "Referenzprüfung"
            Case "REF": ankerLabel = "NGO"
        End Select

        Dim spalteC As Range
        Set spalteC = tbl.DataBodyRange.Columns(1)   ' Spalte C innerhalb der Tabelle (Kategorie-Label)

        Dim gefunden As Range
        Set gefunden = spalteC.Find(What:=ankerLabel, LookIn:=xlValues, LookAt:=xlWhole, MatchCase:=True)
        If gefunden Is Nothing Then
            MsgBox "Ankerzeile """ & ankerLabel & """ nicht in der Tabelle ""Mechanik_30SER"" gefunden - Vorlage wurde vermutlich verändert. Import abgebrochen.", vbCritical, "Mechanik einfügen"
            End
        End If
        neuePosition = gefunden.Row - tbl.HeaderRowRange.Row   ' 1-basierte Position INNERHALB der Tabellendaten
    End If

    Dim neueZeile As ListRow
    Set neueZeile = tbl.ListRows.Add(Position:=neuePosition, AlwaysInsert:=True)

    Dim ws As Worksheet
    Set ws = tbl.Parent
    Dim r As Long
    r = neueZeile.Range.Row

    ' D: Bezeichnung - die Bemerkung steht nach einem Zeilenumbruch MIT in derselben Zelle, damit sie
    ' im ausgedruckten/versendeten KV direkt beim Parameter steht und nicht nur in der (oft
    ' ausgeblendeten) Spalte L. Dort landet sie zusätzlich unverändert.
    If Len(bemerkung) > 0 Then
        ws.Cells(r, 4).Value = bezeichnung & vbLf & bemerkung
        ws.Cells(r, 4).WrapText = True        ' ohne Zeilenumbruch-Formatierung wäre der Umbruch unsichtbar
    Else
        ws.Cells(r, 4).Value = bezeichnung
    End If
    ws.Cells(r, 5).Value = kuerzel            ' E: Kategorie/Kürzel
    ws.Cells(r, 6).Value = "x"                ' F: aktiv (zählt in der Kategorie-Summe mit, bleibt beim Filter sichtbar)
    ws.Cells(r, 7).Value = kosten             ' G: Kosten
    ws.Cells(r, 8).Value = anzahl             ' H: Anzahl
    ws.Cells(r, 11).Value = sapCode           ' K: SAP Material
    ws.Cells(r, 12).Value = bemerkung         ' L: Bemerkung
End Sub

' Berechnet für jede der fünf Kategorien die Summe aller zugehörigen, mit "x" markierten
' Positionszeilen (Kosten × Anzahl, ohne die Überschriften-Zeile selbst) und schreibt sie als FESTEN
' Zahlenwert in die jeweilige Kategorie-Überschriften-Zeile - ersetzt die ursprünglichen
' SUMPRODUCT-/INDEX-MATCH-/IF(...)-Formeln dieser fünf Zeilen vollständig.
Private Sub Mec_SummenAktualisieren(tbl As ListObject, ws As Worksheet)
    Mec_KategorieSummeSchreiben tbl, ws, "Sicherheit & Norm / Sonder- & Funktionsparameter", "MS"
    Mec_KategorieSummeSchreiben tbl, ws, "(physikalische-) Produktspezifikation", "PS"
    Mec_KategorieSummeSchreiben tbl, ws, "FFU/Fitting", "FFU"
    Mec_KategorieSummeSchreiben tbl, ws, "Referenzprüfung", "REF"
    Mec_KategorieSummeSchreiben tbl, ws, "NGO", "NGO"
End Sub

' Summiert AUSSCHLIESSLICH die tatsächlich ausgewählten Positionszeilen (Kosten × Anzahl) derselben
' Kategorie - keine Pauschale/Basispreis mehr. Der frühere Aufschlag von 190 € (bzw. 250 € bei "MAK
' Pilot") aus der Tabelle "Kostentabelle" für Produktspezifikation ist hinfällig und wurde komplett
' entfernt; Produktspezifikation wird jetzt exakt wie die übrigen vier Kategorien behandelt.
Private Sub Mec_KategorieSummeSchreiben(tbl As ListObject, ws As Worksheet, headerLabel As String, kuerzel As String)
    Dim spalteC As Range
    Set spalteC = tbl.DataBodyRange.Columns(1)

    Dim headerZelle As Range
    Set headerZelle = spalteC.Find(What:=headerLabel, LookIn:=xlValues, LookAt:=xlWhole, MatchCase:=True)
    If headerZelle Is Nothing Then Exit Sub
    Dim headerRow As Long
    headerRow = headerZelle.Row

    Dim summe As Double
    Dim anzahlPositionen As Long
    summe = 0
    anzahlPositionen = 0
    Dim zeile As ListRow
    For Each zeile In tbl.ListRows
        Dim r As Long
        r = zeile.Range.Row
        If r <> headerRow Then
            If CStr(ws.Cells(r, 5).Value) = kuerzel And CStr(ws.Cells(r, 6).Value) = "x" Then
                summe = summe + (Mec_ZahlAusZelle(ws.Cells(r, 7)) * Mec_ZahlAusZelle(ws.Cells(r, 8)))
                anzahlPositionen = anzahlPositionen + 1
            End If
        End If
    Next zeile

    ws.Cells(headerRow, 7).Value = summe  ' G: Kategorie-Summe (fester Wert, keine Formel mehr)
    ws.Cells(headerRow, 8).Value = 1      ' H: Anzahl (Multiplikator, unverändert 1)
    ws.Cells(headerRow, 9).Value = summe  ' I: Summe = G*H (fester Wert, keine Formel mehr)

    ' F: Die Überschriften-Zeile ist nur sichtbar, wenn dieser Block überhaupt Positionen hat.
    ' Sonst blieben im gefilterten KV leere Blocküberschriften mit Summe 0 stehen.
    If anzahlPositionen > 0 Then
        ws.Cells(headerRow, 6).Value = "x"
    Else
        ws.Cells(headerRow, 6).Value = ""
    End If
End Sub

Private Function Mec_ZahlAusZelle(zelle As Range) As Double
    If IsNumeric(zelle.Value) Then
        Mec_ZahlAusZelle = zelle.Value
    Else
        Mec_ZahlAusZelle = 0
    End If
End Function

' Val() erwartet IMMER einen Punkt als Dezimaltrennzeichen (so wie KV-Monitoring exportiert),
' unabhängig vom Gebietsschema/den Ländereinstellungen von Excel - anders als CDbl(), das je nach
' Gebietsschema Komma oder Punkt erwartet und sonst einen Laufzeitfehler wirft.
Private Function Mec_Zahl(ByVal s As String) As Double
    s = Trim(s)
    If s = "" Then
        Mec_Zahl = 0
    Else
        Mec_Zahl = Val(s)
    End If
End Function

' Liest Text aus der Windows-Zwischenablage, ohne dass dafür manuell ein VBA-Verweis (z. B.
' "Microsoft Forms 2.0 Object Library") aktiviert werden muss - funktioniert über die
' clipboardData-Eigenschaft eines unsichtbaren "htmlfile"-COM-Objekts.
Private Function Mec_Zwischenablage() As String
    Dim objHTML As Object
    On Error Resume Next
    Set objHTML = CreateObject("htmlfile")
    Mec_Zwischenablage = objHTML.ParentWindow.ClipboardData.GetData("Text")
    On Error GoTo 0
End Function

' ----------------------------------------------------------------------------
' Unverändert aus der bisherigen Datei übernommen (nicht Teil dieser Änderung) -
' blendet in der Tabelle Mechanik_30SER nur die Zeilen mit FILTER = "x" ein.
' Mec() ruft diesen Filter mittlerweile am Ende automatisch mit auf; dieses
' separate Makro bleibt nur als manuelle Option erhalten (z. B. um den Filter
' nach späteren Handeingaben erneut anzuwenden).
' ----------------------------------------------------------------------------
Sub Spalte_Filter()
'
' Hilfe Makro
'
    Range("Mechanik_30SER[FILTER]").Select
    ActiveSheet.ListObjects("Mechanik_30SER").Range.AutoFilter Field:=4, _
        Criteria1:="x"
    Range("F48").Select
End Sub
