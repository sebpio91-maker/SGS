namespace PokerGrid
{
    /// <summary>Written to PokerGrid.ini on first start.</summary>
    internal static class DefaultConfig
    {
        public const string Text = @"; ============================================================
;  PokerGrid - Konfiguration
;  Kommentare beginnen mit ; oder # (nur am Zeilenanfang).
;  Nach Änderungen: Tray-Menü > Konfiguration neu laden
; ============================================================

[General]
; Wie oft (ms) nach neuen und geschlossenen Tischen gesucht wird
PollIntervalMs=500
; Wartezeit (ms), bevor ein neuer Tisch einsortiert wird
; (manche Clients setzen neue Fenster kurz nach dem Öffnen noch selbst um)
NewWindowDelayMs=500
; Neue Tische automatisch in den nächsten freien Slot setzen
AutoArrange=true
; Tisch mit der Maus auf einen anderen Slot ziehen = Plätze tauschen
; (false = Tisch kommt zusätzlich in den Ziel-Slot, der andere bleibt liegen)
SwapOnDrop=true
; Tisch außerhalb des Grids losgelassen:
;   true  = springt in seinen Slot zurück
;   false = Tisch wird freigegeben, bis 'Jetzt anordnen' gedrückt wird
SnapBack=true
; Minimierte/maximierte Tische beim Anordnen wiederherstellen
RestoreMinimized=true
; Mehr Tische als Slots:  Stack = Tische werden gestapelt,  Wait = warten bis ein Slot frei wird
Overflow=Stack
; Aktives Layout (Name eines [Layout:...]-Abschnitts). Wird beim Umschalten automatisch gespeichert.
ActiveLayout=2x2

; Hotkeys: Ctrl / Alt / Shift / Win + Taste (z.B. A, F5, Right, NumPad1, 1). Leer lassen = aus.
HotkeyArrange=Ctrl+Alt+A
HotkeyCompact=Ctrl+Alt+C
HotkeyPause=Ctrl+Alt+P
HotkeyNextLayout=Ctrl+Alt+L
HotkeyOverlay=Ctrl+Alt+O

; ------------------------------------------------------------
;  Layouts
;  Monitor        : 0 = Hauptmonitor, 1..n = Monitore von links nach rechts
;  Columns / Rows : Anzahl Spalten / Zeilen
;  Margin / Gap   : Rand um das Grid / Abstand zwischen Slots (Pixel)
;  Align          : Center | TopLeft | Top | Left
;                   Position des Tisches im Slot, wenn sein Seitenverhältnis
;                   nicht genau zum Slot passt
;  Order          : RowFirst (Slots zeilenweise nummeriert) | ColumnFirst
;  UseWorkingArea : true = Taskleiste freilassen
; ------------------------------------------------------------

[Layout:2x2]
Monitor=0
Columns=2
Rows=2
Margin=0
Gap=0
Align=Center
UseWorkingArea=true

[Layout:3x2]
Monitor=0
Columns=3
Rows=2
Align=TopLeft

[Layout:3x3]
Monitor=0
Columns=3
Rows=3
Align=TopLeft

; Eigene Slots: SlotN=[Monitor:]X,Y,Breite,Höhe  (Pixel oder Prozent des Monitors)
; Sobald ein Layout Slots hat, werden Columns/Rows ignoriert.
; Slots dürfen auch auf verschiedenen Monitoren liegen (z.B. Slot5=2:0,0,50%,50%).
[Layout:1 groß + 4 klein]
Monitor=0
Slot1=0,0,50%,100%
Slot2=50%,0,25%,50%
Slot3=75%,0,25%,50%
Slot4=50%,50%,25%,50%
Slot5=75%,50%,25%,50%

; ------------------------------------------------------------
;  Pokerseiten - woran PokerGrid einen Tisch erkennt
;  Process           : Prozessname(n), kommagetrennt (z.B. PokerStars.exe)
;  Class             : Regex für die Fensterklasse (optional)
;  TitleRegex        : Regex, der auf den Fenstertitel passen muss (optional)
;  ExcludeTitleRegex : Fenster mit passendem Titel ignorieren (z.B. Lobby)
;  AspectRatio       : auto    = Seitenverhältnis vom Fenster übernehmen
;                      1.45 / 800x557 = festes Verhältnis (Breite/Höhe)
;                      stretch = Slot komplett ausfüllen
;  MinWidth/MinHeight: kleinere Fenster (Popups, Dialoge) ignorieren
;
;  Tipp: Tray-Menü > Fenster-Info zeigt Prozess, Klasse und Titel aller
;        offenen Fenster und kopiert eine fertige Vorlage in die Zwischenablage.
; ------------------------------------------------------------

[Site:PokerStars]
Process=PokerStars.exe
Class=^PokerStarsTableFrameClass$
AspectRatio=auto

[Site:Beispiel]
Enabled=false
Process=MeinPokerClient.exe
TitleRegex=Hold'em|Omaha|Table|Tisch
ExcludeTitleRegex=Lobby
AspectRatio=auto
MinWidth=300
MinHeight=200
";
    }
}
