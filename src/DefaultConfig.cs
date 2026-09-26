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
; Aktives Layout (Name eines [Layout:...]-Abschnitts). Wird beim manuellen Umschalten gespeichert.
ActiveLayout=Dynamisch
; Alternative zum dynamischen Layout: zwischen festen Layouts nach Tischanzahl umschalten.
; Liste von klein nach groß, es wird das erste Layout mit genug Slots genommen
; (z.B. AutoLayout=3x2,3x3 = bis 6 Tische 3x2, ab 7 Tischen 3x3).
; Leer lassen = aus. Manuelles Umschalten im Tray-Menü schaltet die Automatik ab (dort wieder einschaltbar).
AutoLayout=
; Auf ein kleineres Layout/Grid erst wechseln, wenn die Tischanzahl so lange (ms) niedrig bleibt
; (verhindert Hin- und Herspringen bei Tischwechseln im Turnier)
AutoLayoutShrinkDelayMs=5000

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
;  Align          : Center | TopLeft | Top | Left | Spread
;                   Position des Tisches im Slot, wenn sein Seitenverhältnis
;                   nicht genau zum Slot passt.
;                   Spread = äußere Tische bündig am Bildschirmrand, die übrigen
;                   gleichmäßig dazwischen (freier Platz/Überlappung wird gleich verteilt)
;  Overlap        : Tische dürfen um so viel Prozent größer als ihr Slot werden
;                   und sich dafür etwas überlappen (0 = keine Überlappung).
;                   Die oberen Reihen liegen dann über den unteren, damit Karten
;                   und Aktionsbuttons unten im Tisch sichtbar bleiben.
;  Order          : RowFirst (Slots zeilenweise nummeriert) | ColumnFirst
;  UseWorkingArea : true = Taskleiste freilassen
;  Mode           : Grid (feste Columns/Rows) | Dynamic
;                   Dynamic = Spalten und Zeilen werden laufend aus der Anzahl der
;                   offenen Tische und ihren Seitenverhältnissen berechnet, sodass
;                   alle Tische so groß wie möglich werden (Columns/Rows werden ignoriert)
;  MaxColumns / MaxRows : Grenzen für Mode=Dynamic
; ------------------------------------------------------------

[Layout:Dynamisch]
Monitor=0
Mode=Dynamic
MaxColumns=5
MaxRows=4
Align=Spread
Overlap=10

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
Align=Spread
Overlap=0

[Layout:3x3]
Monitor=0
Columns=3
Rows=3
Align=Spread
Overlap=12

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

; Bei GGPoker, partypoker und CoinPoker liegen Lobby und Tische im selben Prozess.
; Die Lobby wird über den Titel ausgeschlossen. Falls sie trotzdem einsortiert wird:
; Fenster-Info öffnen, Titel/Klasse der Lobby ablesen und ExcludeTitleRegex bzw. Class anpassen.
; TitleRegex=. bedeutet: Fenster muss einen Titel haben (blendet unsichtbare Hilfsfenster aus).

[Site:PokerStars]
Process=PokerStars.exe
; GLFW30 = neuer Client, PokerStarsTableFrameClass = alter Client
Class=^(GLFW30|PokerStarsTableFrameClass)$
ExcludeTitleRegex=Lobby
AspectRatio=auto

[Site:GGPoker]
Process=GGnet.exe,GGPoker.exe
TitleRegex=.
ExcludeTitleRegex=Lobby|^GG ?Poker$|^GGnet$
AspectRatio=auto
MinWidth=400
MinHeight=300

[Site:partypoker]
Process=PartyPokerde.exe,PartyGaming.exe,partypoker.exe
Class=^#32770$
TitleRegex=.
ExcludeTitleRegex=Lobby|^partypoker$
AspectRatio=auto
MinWidth=400
MinHeight=300

[Site:CoinPoker]
Process=CoinPoker.exe
Class=^UnityWndClass$
TitleRegex=.
ExcludeTitleRegex=Lobby|^CoinPoker$
AspectRatio=auto
MinWidth=400
MinHeight=300
";
    }
}
