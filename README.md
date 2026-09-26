# PokerGrid

Ordnet Pokertische unter Windows 10/11 in einem festen Grid an – ähnlich wie Table Ninja.
Tische verschiedener Pokerseiten mit unterschiedlichen Seitenverhältnissen werden jeweils so groß
wie möglich in ihren Slot eingepasst, ohne verzerrt zu werden.

## Funktionen

- **Automatisches Einsortieren**: Neue Tische landen im nächsten freien Slot, geschlossene Tische geben ihren Slot frei.
- **Verschiedene Seitenverhältnisse**: Jeder Tisch behält sein eigenes Seitenverhältnis (automatisch erkannt oder fest
  eingestellt) und wird im Slot zentriert bzw. oben links ausgerichtet.
- **Drag & Drop**: Tisch mit der Maus auf einen anderen Slot ziehen → die Tische tauschen die Plätze.
  Außerhalb des Grids losgelassen → springt zurück (oder wird freigegeben, einstellbar).
- **Mehrere Layouts** (2x2, 3x2, 3x3, eigene Slots in Pixel oder Prozent, auch über mehrere Monitore),
  per Tray-Menü oder Hotkey umschaltbar.
- **Automatische Layoutwahl**: Standardmäßig 3x2 bei bis zu 6 Tischen, 3x3 ab 7 Tischen (`AutoLayout=3x2,3x3`).
  Zurück auf 3x2 geht es erst, wenn die Tischanzahl 5 Sekunden lang niedrig bleibt.
- **Überlauf**: Mehr Tische als Slots → stapeln oder warten, bis ein Slot frei wird.
- **Slot-Overlay**: zeigt die Slots des aktiven Layouts kurz auf dem Bildschirm an.
- **Fenster-Info**: listet Prozess, Fensterklasse und Titel aller Fenster und erzeugt per Klick eine
  Konfigurationsvorlage für eine neue Pokerseite.
- Berücksichtigt die unsichtbaren Fensterränder von Windows 10 und hohe DPI-Einstellungen.

## Programm bekommen

**Variante A – fertige EXE:** Unter *Actions → Build* den letzten erfolgreichen Lauf öffnen und das Artefakt
`PokerGrid` herunterladen (enthält `PokerGrid.exe`).

**Variante B – selbst bauen (nichts zu installieren):** Repository herunterladen und `build.bat` doppelklicken.
Das Skript nutzt den C#-Compiler, der bei Windows 10 schon dabei ist. Ergebnis: `dist\PokerGrid.exe`.

## Benutzung

1. `PokerGrid.exe` starten – es erscheint ein grünes Grid-Symbol im Infobereich der Taskleiste.
   Beim ersten Start wird neben der EXE die Datei `PokerGrid.ini` angelegt.
2. Rechtsklick auf das Symbol → *Fenster-Info …*: Pokertisch öffnen, *Aktualisieren*, Zeile des Tisches wählen,
   *Als Site-Vorlage kopieren*.
3. *Konfiguration bearbeiten* → Vorlage unten einfügen, ggf. `TitleRegex`/`ExcludeTitleRegex` anpassen
   (damit z. B. die Lobby nicht mit einsortiert wird), speichern.
4. *Konfiguration neu laden* – ab jetzt werden die Tische automatisch angeordnet.

Für PokerStars, GGPoker, partypoker und CoinPoker sind bereits Einträge vorhanden. Bei GGPoker, partypoker und
CoinPoker sind Prozessnamen und Lobby-Titel noch nicht am echten Client geprüft – kontrolliere sie beim ersten Start
in der Fenster-Info (siehe unten).

Hast du PokerGrid schon einmal gestartet, lösche die alte `PokerGrid.ini`, damit die neuen Standardwerte angelegt werden. In der Fenster-Info sind erkannte Tische grün markiert.

### Hotkeys (Standard, in der INI änderbar)

| Hotkey         | Aktion                                               |
|----------------|------------------------------------------------------|
| `Ctrl+Alt+A`   | Jetzt anordnen (holt auch freigegebene Tische zurück) |
| `Ctrl+Alt+C`   | Lücken schließen (Tische nach vorne aufrücken)        |
| `Ctrl+Alt+P`   | Pause an/aus                                          |
| `Ctrl+Alt+L`   | Nächstes Layout                                       |
| `Ctrl+Alt+O`   | Slots anzeigen                                        |

Doppelklick auf das Tray-Symbol zeigt ebenfalls die Slots.

## Konfiguration (`PokerGrid.ini`)

Die Datei ist ausführlich kommentiert. Die wichtigsten Stellen:

```ini
[Layout:3x2]
Monitor=0          ; 0 = Hauptmonitor, 1..n = Monitore von links nach rechts
Columns=3
Rows=2
Gap=0
Align=TopLeft      ; Center | TopLeft | Top | Left

[Layout:1 groß + 4 klein]
Slot1=0,0,50%,100%          ; X,Y,Breite,Höhe – Pixel oder Prozent
Slot2=50%,0,25%,50%
Slot3=2:0,0,50%,50%         ; optional Monitor davor (hier Monitor 2)

[Site:PokerStars]
Process=PokerStars.exe
Class=^PokerStarsTableFrameClass$
AspectRatio=auto   ; auto | 1.45 | 800x557 | stretch
```

`AspectRatio=auto` übernimmt das Seitenverhältnis, das der Tisch beim Öffnen hat. Wenn ein Client beim Verkleinern
Balken bekommt oder das Verhältnis leicht ändert, trägst du das exakte Verhältnis fest ein (z. B. `800x557`).

## Hinweise

- **Adminrechte**: Läuft ein Pokerclient als Administrator, kann Windows ihn nur von einem Programm verschieben
  lassen, das ebenfalls als Administrator läuft. Dann PokerGrid per Rechtsklick → *Als Administrator ausführen*.
- **Mindestgrößen**: Manche Clients haben eine Mindestgröße. Ist ein Slot kleiner, bleibt der Tisch größer als der Slot.
- **Regeln der Pokerseiten**: PokerGrid verschiebt nur Fenster und liest keine Spieldaten. Prüfe trotzdem die Liste
  erlaubter Software deiner Pokerseite – einige Seiten (z. B. GGPoker) schränken Drittprogramme stark ein.
