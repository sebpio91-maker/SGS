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

## Ranges vergleichen

Über "Ranges vergleichen" lassen sich zwei Ranges nebeneinander im Grid darstellen – entweder
zwei Positionen beim gleichen Stack, oder eine Position bei zwei unterschiedlichen Stacktiefen.
Die verglichenen Sitze werden am Tisch farblich markiert.

## Spot analysieren

Über "Spot analysieren" lässt sich ein Spot als Freitext beschreiben (z.B. "UTG, 100bb, ich habe
AKo, alle folden zu mir"). Ein lokaler Parser (`spotparser.js`) erkennt daraus Position, Stack,
Hand und Situation – **ohne KI-Aufruf, ohne Internetverbindung, ohne Kosten**. Die erkannten
Felder werden vor der Auswertung angezeigt und lassen sich korrigieren.

Ausgewertet wird nur, wofür echte Daten aus der Excel-Tabelle vorliegen:
- **Unopened-Spots** bei UTG–BTN: hand-genaue Ja/Nein-Antwort aus dem Open-Raise-Grid.
- **Spots gegen einen Open**: aggregierter Continue-Prozentsatz (keine Hand-für-Hand-Antwort,
  da die Tabelle das nicht hergibt).
- **Alles andere** (3-Bet-Pots, Squeeze, 4-Bet, Rejam, Postflop): explizite Meldung, dass dafür
  keine Daten vorliegen, statt einer erfundenen Antwort.

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
- `spotparser.js` – Freitext-Parser für die Spot-Analyse (Position/Stack/Hand/Situation
  erkennen), rein lokal, keine externen Aufrufe
