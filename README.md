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

Auf dem Tisch anklicken, um die Open-Raise-Range (Raise-First-In) der jeweiligen Position
als 13x13-Grid anzuzeigen. Für BB wird stattdessen eine beispielhafte Defend-Range
gegen einen Button-Open gezeigt (der BB eröffnet preflop nie selbst).

Alle Ranges sind vereinfachte, aber sinnvolle Trainings-Ranges für ein 100bb-Cash-Game –
keine solver-exakten GTO-Ranges.

## Starten

Kein Build-Schritt nötig, reines HTML/CSS/JS:

```bash
python3 -m http.server 8000
```

Dann im Browser `http://localhost:8000` öffnen. Alternativ `index.html` direkt öffnen
(funktioniert ebenfalls, da keine externen Requests nötig sind).

## Dateien

- `index.html` – Struktur / Layout
- `style.css` – Tisch- und Grid-Design
- `ranges.js` – Range-Notation-Parser (`77+`, `A9s+`, `KTo-KQo`, …) und Range-Daten je Position
- `app.js` – Rendering des Tisches und der Range-Grid, Klick-Interaktion
