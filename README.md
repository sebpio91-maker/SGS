# SGS – Prüf- und Kostendatenbanken

Mehrere eigenständige Projekte, jeweils als einzelne HTML-Datei ohne
Installation/Server/Berechtigungen nutzbar (siehe jeweiliges Unterverzeichnis).

## Projekt 1: Normen-Datenbank

Werkzeuge zur Pflege einer Datenbank von Normen und ihren Prüfpunkten
(Kapitel, Überschrift, Prüfungsrelevanz, Inhalt), als Grundlage für spätere
Prüfungen. Die Zuordnung/Auswahl "welche Norm gilt für welches Produkt" ist
bewusst noch nicht Teil davon – hier geht es erstmal nur um eine
übersichtliche, gepflegte Datenbasis.

Startdaten (in beiden Varianten): DIN EN 581-1, -2 und -3 (Kapitel +
Prüfungsrelevanz), übernommen aus dem `NORMEN`-Blatt der bestehenden
`Normenauswahl.xlsm`.

### Variante 1 (empfohlen für den Arbeits-PC): `Normen-Datenbank-Offline/`

Eine einzelne HTML-Datei, kein Python, keine Installation, kein Server –
einfach per Doppelklick öffnen. Speichert automatisch im Browser (Local
Storage) und bietet JSON-Export/Import zum Sichern sowie eine
**Zusammenführen-Funktion**, um die Arbeitsstände mehrerer Kolleg:innen zu
einer gemeinsamen Datenbank zu vereinen, plus CSV-Export für Excel.

Details und Arbeitsablauf: siehe `Normen-Datenbank-Offline/README.md`.

### Variante 2 (falls später ein echter Server/geteilte Datenbank gebraucht wird): `app/`

Eine kleine Web-App (Python/FastAPI + SQLite) mit denselben Daten und
zusätzlich einem einfachen, heuristischen PDF-Upload zur Prüfpunkt-Extraktion.
Braucht eine Python-Installation und einen laufenden Prozess (`uvicorn`).

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Danach im Browser: http://127.0.0.1:8000

Die Datenbank liegt als SQLite-Datei unter `data/normen.db` und wird beim
ersten Start automatisch angelegt und mit den Beispiel-Normen befüllt.

### Funktionen

- **Übersicht** aller Normen mit Volltextsuche über Kurzbezeichnung, Titel,
  Kategorie sowie Kapitel/Überschrift/Inhalt der Prüfpunkte.
- **Norm anlegen/bearbeiten/löschen**: Kurzbezeichnung, Vollbezeichnung/Ausgabe,
  Titel, Status (aktiv / in Überarbeitung / zurückgezogen / Entwurf), Kategorie,
  Notiz.
- **Prüfpunkte-Tabelle** je Norm (Kapitel, Überschrift, Prüfungsrelevant,
  Inhalt) – direkt in der Tabelle editierbar, Änderungen werden automatisch
  gespeichert. Zeilen lassen sich hinzufügen, löschen und verschieben.
- **PDF-Upload**: Eine Norm-PDF hochladen, der Text wird ausgelesen und
  heuristisch in Kapitel/Abschnitte zerlegt. Das Ergebnis ist ein *Entwurf*,
  der vor der Übernahme in die Datenbank geprüft und angepasst werden muss
  (die Erkennung ist ein einfacher Best-Effort-Ansatz, kein echtes
  Norm-Parsing).
- **Export**: Alle Normen + Prüfpunkte als Excel-Datei (`/export/excel`).

### Projektstruktur

```
app/
  main.py         FastAPI-Routen (Seiten + JSON-API)
  models.py       SQLAlchemy-Modelle (Norm, Pruefpunkt)
  database.py     SQLite-Setup
  seed.py         Startdaten (EN 581-1/-2/-3)
  extraction.py   Heuristische PDF-Kapitel-Erkennung
  templates/      Jinja2-Templates
  static/         CSS/JS
data/normen.db    SQLite-Datenbankdatei (wird automatisch angelegt)
```

## Projekt 2: KV-Monitoring – `KV-Monitoring-Offline/`

Arbeitsvorrat (aus SAP-Export), Prüfaufträge (PA) und Kostenvoranschläge (KV)
für **mechanische Prüfungen**. Ebenfalls eine einzelne HTML-Datei ohne
Installation. Kernidee: bestehende KVs durchsuchen und als Vorlage für neue,
ähnliche Projekte duplizieren, plus ein wiederverwendbarer
Prüfpositionen-Katalog mit Standardkosten/SAP-Codes zum schnellen Befüllen.

Details und Arbeitsablauf: siehe `KV-Monitoring-Offline/README.md`.
