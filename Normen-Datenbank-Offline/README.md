# Normen-Datenbank (Offline, ohne Installation)

Eine einzelne HTML-Datei zur Pflege einer Datenbank von Normen und ihren
Prüfpunkten (Kapitel, Überschrift, Prüfungsrelevanz, Inhalt). Läuft komplett
im Browser, ohne Server, ohne Python, ohne Installation.

## Benutzen

Einfach **`Normen-Datenbank.html`** doppelklicken – öffnet sich im
Standard-Browser (Chrome, Edge, Firefox). Fertig.

Beim ersten Öffnen sind DIN EN 581-1, -2 und -3 (aus der bestehenden
`Normenauswahl.xlsm`) bereits als Beispiel eingetragen.

Alle Änderungen werden automatisch im Browser (Local Storage) auf diesem PC
gespeichert – ein Neuladen der Seite verliert nichts. Das gilt aber nur für
**diesen** Browser auf **diesem** PC; zum Teilen/Sichern/Zusammenführen die
Export-Funktionen benutzen (siehe unten).

## Funktionen (Toolbar oben)

- **+ Neue Norm** – legt eine leere Norm an.
- **Norm anklicken** (links in der Liste) – Metadaten und Prüfpunkte-Tabelle
  rechts bearbeiten. Jede Änderung wird sofort gespeichert.
- **Zeile hinzufügen / ↑ / ↓ / 🗑** – Prüfpunkte-Zeilen verwalten.
- **⬇ Sichern (JSON)** – lädt den kompletten aktuellen Stand als
  `.json`-Datei herunter. Das ist die "Speichern unter"-Funktion dieser App –
  regelmäßig nutzen, vor allem bevor eine andere Datei geladen wird.
- **⬆ Datei laden (JSON)** – ersetzt den aktuellen Stand komplett durch den
  Inhalt einer zuvor gesicherten `.json`-Datei.
- **🔀 Zusammenführen (JSON)** – **damit lassen sich Arbeitsstände mehrerer
  Personen/Rechner zusammenführen**: Datei einer Kollegin/eines Kollegen
  auswählen, die App zeigt an, was neu ist (neue Normen, neue Prüfpunkte)
  und wo es Konflikte gibt (gleiches Kapitel, aber unterschiedlicher Inhalt).
  Bei Konflikten wählt man je Fall "Aktuell behalten" oder "Aus Datei
  übernehmen". Nichts wird automatisch überschrieben.
- **📄 Excel-Export (CSV)** – exportiert alle Normen/Prüfpunkte als
  `.csv`-Datei, die sich direkt in Excel öffnen lässt (für die spätere
  Zusammenführung in einer zentralen Excel-Datei/Datenbank).

## Typischer Arbeitsablauf mit mehreren Personen

1. Eine Person startet die Datei, pflegt Normen ein, klickt **Sichern (JSON)**
   und schickt die `.json`-Datei an die anderen (z. B. per Mail/Teams).
2. Jede Person öffnet **dieselbe** `.json`-Datei über **Datei laden**, bevor
   sie eigene Änderungen macht (damit alle vom gleichen Stand ausgehen).
3. Jede Person arbeitet lokal weiter und sichert ihren eigenen Stand
   regelmäßig als `.json`.
4. Eine Person sammelt die einzelnen `.json`-Dateien ein und führt sie
   nacheinander über **Zusammenführen** zu einem gemeinsamen Stand zusammen.
5. Der zusammengeführte Stand wird wieder als `.json` gesichert (Master-Datei)
   und bei Bedarf als CSV für Excel exportiert.

## Bewusst nicht enthalten

- Automatischer PDF-Upload zur Prüfpunkt-Extraktion (das war ein
  "vielleicht später" – siehe Hauptrepo, dort gibt es dazu bereits einen
  funktionierenden Prototyp in `app/`, falls das später doch serverbasiert
  gebraucht wird).
- Die Zuordnung "welche Norm gilt für welches Produkt" (Auswahllogik) – laut
  Vorgabe bewusst erstmal zurückgestellt.
