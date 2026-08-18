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
' davon eigene, vom Trivial-/DokCheck-Status abhängige Preisformeln enthalten,
' die dabei NIE überschrieben werden sollen. Diese Zeilen bleiben unangetastet
' - wer sie braucht, aktiviert sie weiterhin wie bisher manuell (Spalte
' "FILTER" = "x").
'
' Vor jedem Import werden zunächst alle vorbelegten "x"-Markierungen in Spalte F (FILTER) der
' bestehenden Standardzeilen entfernt - AUSGENOMMEN die Kategorie-Überschriften-Zeilen (Spalte C
' gefüllt, z. B. "Sicherheit & Norm ...", "(physikalische-) Produktspezifikation", "FFU/Fitting",
' "Referenzprüfung", "NGO"), deren "x" für die SUMPRODUCT-Formeln (G48/G55) benötigt wird. So
' zählen nur noch die Positionen, die tatsächlich aus dem aktuellen KV-Monitoring-Export stammen -
' nicht mehr die als Vorlage vorbelegten Standard-Haken. Am Ende wird die Tabelle automatisch auf
' Spalte F = "x" gefiltert (bisher der separate Button/das separate Makro "Spalte_Filter"), sodass
' nur die aktiven Zeilen sichtbar bleiben.
'
' Da "Mechanik_30SER" eine echte Excel-Tabelle ist (ListObject), erweitert
' Excel beim Einfügen neuer Zeilen automatisch alle betroffenen Formeln
' (SUMPRODUCT in G48/G55, SUMIF für FFU/REF/NGO in der Kopfübersicht,
' "ZWISCHENSUMME MECHANIK" = SUM(I48:I67)) - dafür muss jede neue Zeile
' innerhalb des bestehenden Tabellenbereichs eingefügt werden, nie dahinter.
' Deshalb sucht Mec_ZeileEinfuegen die passende "Ankerzeile" (Beginn des
' jeweils nächsten Kategorie-Blocks) und fügt dort ein.
'
' Die bisher ungenutzte Spalte J (Kopf ein einzelnes Leerzeichen) wird für die
' "Bemerkung" jeder neuen Zeile verwendet - dort landet die automatische
' Teilprüfung-Angabe der Sicherheit-/Normprüfung-Position (Prozentsatz je nach
' Artikelkategorie - Grün 40 %, Gelb 50 %, Rot/unbekannt 70 %, siehe
' teilpruefungProzentsatz im KV-Monitoring-Tool) sowie alle in der
' Prüfpositionstabelle automatisch aggregierten Bemerkungen (siehe
' positionBemerkungen: Bewertungsgrundlage/Grenzwert, Norm-Bemerkung,
' Prüfgrundlage-Kommentar, MAK-Hinweis), damit diese Angaben auch in der
' Excel-Datei nicht verloren gehen.
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
' "Mechanik_30SER" auf diesem Blatt. Die Bemerkung-Spalte (Teilprüfung/
' Prozentsatz, Bewertungsgrundlage, Norm-Bemerkung, Prüfgrundlage-Kommentar,
' MAK-Hinweis - siehe positionBemerkungen im KV-Monitoring-Tool) landet dabei
' in der bisher ungenutzten Spalte J der Tabelle.
'
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets("Inspection Booking")

    Dim tbl As ListObject
    Set tbl = ws.ListObjects("Mechanik_30SER")

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
' Tabelle Mechanik_30SER - AUSSER bei den Kategorie-Überschriften-Zeilen (Spalte C gefüllt), deren
' "x" die SUMPRODUCT-Formeln in G48/G55 braucht. Läuft VOR jedem Import, damit nur noch zählt, was
' tatsächlich aus dem aktuellen KV-Monitoring-Export als aktiv markiert wurde - nicht mehr die als
' Vorlage vorbelegten Standard-Haken (z. B. Kennzeichnung GER, Optischer Abgleich, Projektkosten).
Private Sub Mec_AlteFilterZuruecksetzen(tbl As ListObject)
    Dim zeile As ListRow
    For Each zeile In tbl.ListRows
        If Len(Trim(zeile.Range.Cells(1, 1).Value & "")) = 0 Then   ' Spalte C (1. Tabellenspalte) leer -> Detailzeile, keine Kategorie-Überschrift
            zeile.Range.Cells(1, 4).Value = ""                       ' Spalte F ist die 4. Tabellenspalte (C=1, D=2, E=3, F=4)
        End If
    Next zeile
End Sub

' Fügt EINE neue Zeile für die Kategorie "kuerzel" in die Tabelle Mechanik_30SER ein - direkt vor
' dem Beginn des jeweils nächsten Kategorie-Blocks (bzw. bei NGO direkt vor der bestehenden
' NGO-Zeile), damit alle Summenformeln (SUMPRODUCT/SUMIF/SUM), die den Tabellenbereich
' referenzieren, sich automatisch mit erweitern.
Private Sub Mec_ZeileEinfuegen(tbl As ListObject, kuerzel As String, bezeichnung As String, kosten As Double, anzahl As Double, sapCode As String, bemerkung As String)
    Dim ankerLabel As String
    Select Case kuerzel
        Case "MS": ankerLabel = "(physikalische-) Produktspezifikation"
        Case "PS": ankerLabel = "FFU/Fitting"
        Case "FFU": ankerLabel = "Referenzprüfung"
        Case "REF", "NGO": ankerLabel = "NGO"
    End Select

    Dim spalteC As Range
    Set spalteC = tbl.DataBodyRange.Columns(1)   ' Spalte C innerhalb der Tabelle (Kategorie-Label)

    Dim gefunden As Range
    Set gefunden = spalteC.Find(What:=ankerLabel, LookIn:=xlValues, LookAt:=xlWhole, MatchCase:=True)
    If gefunden Is Nothing Then
        MsgBox "Ankerzeile """ & ankerLabel & """ nicht in der Tabelle ""Mechanik_30SER"" gefunden - Vorlage wurde vermutlich verändert. Import abgebrochen.", vbCritical, "Mechanik einfügen"
        End
    End If

    Dim neuePosition As Long
    neuePosition = gefunden.Row - tbl.HeaderRowRange.Row   ' 1-basierte Position INNERHALB der Tabellendaten

    Dim neueZeile As ListRow
    Set neueZeile = tbl.ListRows.Add(Position:=neuePosition, AlwaysInsert:=True)

    Dim ws As Worksheet
    Set ws = tbl.Parent
    Dim r As Long
    r = neueZeile.Range.Row

    ws.Cells(r, 4).Value = bezeichnung        ' D: Bezeichnung
    ws.Cells(r, 5).Value = kuerzel            ' E: Kategorie/Kürzel
    ws.Cells(r, 7).Value = kosten             ' G: Kosten
    ws.Cells(r, 8).Value = anzahl             ' H: Anzahl
    ws.Cells(r, 10).Value = bemerkung         ' J: Bemerkung (Teilprüfung/Prozentsatz, Bewertungsgrundlage, Norm-/Prüfgrundlage-/MAK-Hinweise)
    ws.Cells(r, 11).Value = sapCode           ' K: SAP Material

    If kuerzel = "MS" Or kuerzel = "PS" Then
        ws.Cells(r, 6).Value = "x"            ' F: aktiviert die Zeile in der SUMPRODUCT-Summe (G48/G55)
    Else
        ws.Cells(r, 9).Formula = "=IF(D" & r & "="""","""",G" & r & "*H" & r & ")"   ' I: eigene Summe (FFU/REF/NGO haben keine SUMPRODUCT-Sammelzeile)
    End If
End Sub

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
