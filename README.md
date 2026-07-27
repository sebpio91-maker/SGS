# Poker Range Viewer

Eine kleine Web-App zum Ansehen von Preflop-Ranges an einem 8-Handed-Tisch.

## Positionen

1. UTG
2. UTG+1
3. MP
4. HJ
5. CO
6. BTN
7. SB
8. BB

Auf dem Tisch anklicken, um die Open-Raise-Range der jeweiligen Position als 13x13-Grid
anzuzeigen. Über die Stack-Auswahl (100/60/40/30/20 BB) lässt sich die Range je Stacktiefe
umschalten.

Die Open-Raise-Ranges (UTG bis BTN) stammen aus einer hochgeladenen Excel-Tabelle
("Openraising"-Blatt). Da diese Tabelle nur 5 Eröffner-Gruppen kennt (EP, MP, HJ, CO, BTN),
teilen sich UTG und UTG+1 dieselbe "EP"-Range. Bei 20 BB markiert ein "*" Hände, die die
Tabelle für BTN als All-in statt Raise kennzeichnet.

Für SB und BB liegt in der Quelltabelle kein Hand-für-Hand-Grid vor, sondern nur
Continue-Prozentsätze (Call + 3-Bet zusammen) gegen einzelne Eröffner-Positionen
(Blatt "% Ranges" / "Flat & 3-Bet"). Diese werden dort als Balkendiagramm angezeigt.

Nicht übernommen wurde das Blatt "Gametree" (Postflop-Bet-Sizing-Frequenzen für einzelne
Boardtypen) – das ist inhaltlich ein anderes Thema als Preflop-Positionsranges und würde eine
eigene Ansicht brauchen.

## Starten

Kein Build-Schritt nötig, reines HTML/CSS/JS:

```bash
python3 -m http.server 8000
```

Dann im Browser `http://localhost:8000` öffnen. Alternativ `index.html` direkt öffnen
(funktioniert ebenfalls, da keine externen Requests nötig sind).

## Dateien

- `index.html` – Struktur / Layout
- `style.css` – Tisch-, Grid- und Stats-Design
- `ranges.js` – Grid-Hilfsfunktionen, Positions-Metadaten
- `myranges.js` – aus der Excel-Datei generierte Range-Daten (Open-Raise-Grid je Stacktiefe,
  Continue-Statistiken); bei einer neuen Datei neu generieren, nicht von Hand pflegen
- `app.js` – Rendering des Tisches, der Range-Grid bzw. Continue-Stats, Klick-Interaktion
