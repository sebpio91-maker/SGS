# Normen-Datenbank (Offline, ohne Installation)

Eine einzelne HTML-Datei zur Pflege einer Datenbank von Normen (mit ihren
Prüfpunkten) **und** der Zuordnung zu Produkten inkl. besonderer
Ausprägungen. Läuft komplett im Browser, ohne Server, ohne Python, ohne
Installation.

## Benutzen

Einfach **`Normen-Datenbank.html`** doppelklicken – öffnet sich im
Standard-Browser (Chrome, Edge, Firefox). Fertig.

Beim ersten Öffnen sind bereits eingetragen (übernommen aus der bestehenden
`Normenauswahl.xlsm`):
- **Normen**: DIN EN 581-1, -2 und -3 (Blatt „NORMEN")
- **Produkte**: alle 133 Zeilen aus dem Blatt „Datenbank" (Produkt-Norm-Zuordnung)
- **Sonderposten**: alle 17 Zeilen aus dem Blatt „Sonderposten" (Produktmerkmale
  mit besonderen Prüfungen/Zusatzkosten)

Alle Änderungen werden automatisch im Browser (Local Storage) auf diesem PC
gespeichert – ein Neuladen der Seite verliert nichts. Das gilt aber nur für
**diesen** Browser auf **diesem** PC; zum Teilen/Sichern/Zusammenführen die
Export-Funktionen benutzen (siehe unten).

## Die vier Reiter

- **Normen** – wie bisher: Norm anklicken (links), Metadaten und
  Prüfpunkte-Tabelle (Kapitel/Überschrift/Prüfungsrelevant/Inhalt) rechts
  bearbeiten.
- **Produkte** – die Produkt-Norm-Zuordnung als eine große, direkt editierbare
  Tabelle: Kategorie → Produktart → Zielgruppe → Einsatzort → Bereich →
  Produkt, dazu Normen (Freitext, wie im Original), Verweise/Prüfmethoden,
  Material, Preis, Labor-Zeit/-Kosten, Bemerkungen. Suche filtert über alle
  Spalten. „+ Neues Produkt" legt eine leere Zeile an.
- **Sonderposten** – Produktmerkmale, die besondere/zusätzliche Prüfungen oder
  Kosten auslösen (z. B. „Armlehne", „Glas", „Level 2"), zugeordnet über
  Kategorie/Produktart und optional Zielgruppe/Einsatzort. Leer lassen, wenn
  das Merkmal unabhängig davon gilt.
- **Übersicht** – nur lesend: pro Produkt werden die hinterlegten Normen,
  Verweise/Prüfmethoden und die **passenden Sonderposten** (automatisch nach
  Kategorie/Produktart/Zielgruppe/Einsatzort abgeglichen) in einer Zeile
  zusammengeführt. Das ist die gewünschte Gesamtübersicht "Produkt +
  zugehörige Normen + besondere Ausprägungen".

## Toolbar (oben, gilt bereichsübergreifend)

- **⬇ Sichern (JSON)** – lädt den kompletten aktuellen Stand (Normen +
  Produkte + Sonderposten) als `.json`-Datei herunter. Das ist die "Speichern
  unter"-Funktion dieser App – regelmäßig nutzen, vor allem bevor eine andere
  Datei geladen wird.
- **⬆ Datei laden (JSON)** – ersetzt den aktuellen Stand komplett durch den
  Inhalt einer zuvor gesicherten `.json`-Datei.
- **🔀 Zusammenführen (JSON)** – **damit lassen sich Arbeitsstände mehrerer
  Personen/Rechner zusammenführen**, für Normen, Produkte und Sonderposten
  gemeinsam: Datei einer Kollegin/eines Kollegen auswählen, die App zeigt an,
  was neu ist und wo es Konflikte gibt (gleicher Eintrag, aber
  unterschiedliche Angaben). Bei Konflikten wählt man je Fall "Aktuell
  behalten" oder "Aus Datei übernehmen". Nichts wird automatisch
  überschrieben.
- **📄 CSV-Export (aktueller Bereich)** – exportiert die Tabelle des gerade
  geöffneten Reiters (Normen / Produkte / Sonderposten / Übersicht) als
  `.csv`-Datei, direkt in Excel öffenbar.

## Typischer Arbeitsablauf mit mehreren Personen

1. Eine Person pflegt Normen/Produkte/Sonderposten ein, klickt
   **Sichern (JSON)** und schickt die `.json`-Datei an die anderen (z. B. per
   Mail/Teams).
2. Jede Person öffnet **dieselbe** `.json`-Datei über **Datei laden**, bevor
   sie eigene Änderungen macht (damit alle vom gleichen Stand ausgehen).
3. Jede Person arbeitet lokal weiter und sichert ihren eigenen Stand
   regelmäßig als `.json`.
4. Eine Person sammelt die einzelnen `.json`-Dateien ein und führt sie
   nacheinander über **Zusammenführen** zu einem gemeinsamen Stand zusammen.
5. Der zusammengeführte Stand wird wieder als `.json` gesichert (Master-Datei)
   und bei Bedarf pro Reiter als CSV für Excel exportiert.

## Bewusst nicht enthalten

- Automatischer PDF-Upload zur Prüfpunkt-Extraktion (das war ein
  "vielleicht später" – siehe Hauptrepo, dort gibt es dazu bereits einen
  funktionierenden Prototyp in `app/`, falls das später doch serverbasiert
  gebraucht wird).
- Der interaktive Auswahl-Assistent ("Normenfinder" mit Dropdowns, wie im
  Blatt „Eingabe") – die Übersicht deckt das Kernbedürfnis (welche Normen +
  Ausprägungen gehören zu welchem Produkt) bereits ab; ein geführter
  Auswahl-Dialog kann bei Bedarf ergänzt werden.
- Strikte Verknüpfung zwischen dem Normen-Reiter und dem Freitext-Feld
  "Normen" in den Produkten (z. B. per Verweis auf die Norm-ID). Das Original
  enthält dort uneinheitliche/teils fehlerhafte Bezeichnungen (z. B.
  „DIN EN 518-3" statt „581-3"), daher bewusst als Freitext belassen statt
  automatisch (und ggf. falsch) verknüpft.
