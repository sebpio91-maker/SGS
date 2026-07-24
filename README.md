# SGS Prüfplan-App

Automatische Erstellung von Prüfplänen für Produktprüfungen – basierend auf
Normen, Prüfprogrammen, gesetzlichen Vorgaben (z. B. Kennzeichnung) sowie
Produktspezifikationen und kundenspezifischen Vorgaben.

Zentrales Ausgangsdokument für den Kunden Lidl ist der Prüfauftrag (PDF);
für andere Kunden erfolgt die Auswahl der Prüfungen über ein Menü im
Katalog.

## Architektur

- **Backend**: Python / FastAPI, PostgreSQL, SQLAlchemy, Alembic
- **Frontend**: React + TypeScript (Vite)
- **Export**: Prüfpläne als Excel (`.xlsx`) und PDF

## Datenmodell

- **Customer**: Kunde (z. B. Lidl), identifiziert per `code`
- **Product**: zu prüfendes Produkt eines Kunden, inkl. flexibler
  `specification` (JSON) und Flags wie `has_battery`/`has_manual`
- **Norm**: Norm/Gesetz/Kundenvorgabe, auf die sich ein Prüfpunkt bezieht
- **TestCategory** / **TestCatalogItem**: hierarchischer Prüfkatalog
  (Kategorie → Prüfpunkte). Kann kundenspezifisch (z. B. Lidls fester
  Baum) oder generisch (Menü-Auswahl für andere Kunden) sein.
  `applicability_condition` markiert bedingte Prüfpunkte (z. B.
  `has_battery` für den Akkusicherheitskurzcheck)
- **TestProgram** / **TestProgramItem**: wiederverwendbare Vorlage aus
  mehreren Katalog-Prüfpunkten für wiederkehrende, ähnliche Produkte
- **TestOrder**: Prüfauftrag als Ausgangsdokument (bei Lidl importiert,
  sonst manuell)
- **TestPlan** / **TestPlanItem**: der generierte Prüfplan mit seinen
  Prüfpositionen (Snapshot aus dem Katalog zum Erstellungszeitpunkt),
  inkl. Kosten-Snapshot (`lab_minutes`, `lab_cost`, `sale_price`)

Stammdaten-Referenztabellen (befüllt aus den realen Excel-Katalogen):

- **NormLookupRule**: Produktklassifikation (Kategorie → Produktart →
  Zielgruppe → Einsatzort → Bereich → Produkt) → anzuwendende Norm(en),
  Laborzeit/-kosten, Preis (Normenfinder-Logik)
- **NormSpecialItem**: Zusatzkosten/-normen für spezielle
  Produkteigenschaften (z. B. Armlehne, Glas), scoped nach Klassifikation
- **ProductSpecRequirement**: Anforderungskatalog physikalische
  Produktspezifikation (Parameter × Produkt/Material × Paketstufe →
  Norm, Laufzeit, Kosten-/Bewertungsformeln, Prüflabor)
- **LidlWarengruppeRule**: Norm/FFU/StiWa/NGO-Referenzen und Kosten je
  Lidl-Warengruppe

Migrationen liegen in `backend/alembic/versions/`. Der Lidl-Prüfpunkt-Baum
kann per Seed-Skript eingespielt werden (siehe unten), die vier
Referenztabellen per Import-Skript aus den Original-Excel-Dateien.

## Lidl-Prüfauftrag-Import

`backend/app/lidl_pdf_parser.py` extrahiert aus dem PDF-Prüfauftrag
Artikeldaten (IAN/Charge, Bezeichnung, Warenbereich/-gruppe), Lieferant,
den Prüfumfang (welche Prüfkategorien beauftragt sind), sowie die
Signalfelder für Batterie (`Batterietyp`), Anleitung (Erwähnung von
"Montageanleitung"/"Bedienungsanleitung" im Qualitätstext),
Referenzprüfung, NGO- und FFU-Prüfung. Über `POST
/api/test-orders/import-lidl` (Multipart-Upload) wird daraus automatisch
ein `Product` (Kunde "Lidl", identifiziert per Artikelnummer/IAN) und ein
`TestOrder` mit dem vollständigen Rohtext als Audit-Trail angelegt bzw.
aktualisiert. In der Web-App steht dafür die Seite
"Lidl-Prüfauftrag-Import" zur Verfügung.

Da bisher nur ein Beispieldokument vorlag, ist der Parser defensiv
ausgelegt: nicht erkannte Felder bleiben leer, der komplette Rohtext wird
immer mit gespeichert. Ein paar Formularfelder mit mehrzeilig
umgebrochenem Label (z. B. "Sicherheitsdatenblatt Gefahrgut") werden
nicht strukturiert erfasst, da PDF-Textextraktion Label und Wert dort
zeilenweise verschränkt – keines dieser Felder wird für die
Prüfplan-Logik benötigt.

## Lokale Entwicklung

### Backend + Datenbank (Docker)

```bash
cp backend/.env.example backend/.env
docker compose up --build
```

Backend läuft danach unter http://localhost:8000, Health-Check unter
http://localhost:8000/api/health. Datenbankmigrationen (Alembic) werden
beim Start automatisch angewendet.

Optional: Beispieldaten für den Lidl-Prüfpunkt-Baum einspielen
(Kunde "Lidl" inkl. Kategorien und Prüfpunkten unter "Sicherheit & Norm /
Sonder- & Funktionsparameter"):

```bash
docker compose exec backend python -m app.seed
```

Stammdaten aus den Original-Excel-Referenzdateien importieren (Dateien
liegen nicht im Repo – Pfade zeigen auf lokale Kopien):

```bash
docker compose exec backend python -m app.import_master_data \
  --normenauswahl /pfad/zu/Normenauswahl.xlsm \
  --produktspezifikationen /pfad/zu/Produktspezifikationen.xlsx \
  --mechanik /pfad/zu/KV_Monitoring.xlsm
```

Es gibt noch keine öffentliche Registrierung – Benutzer werden über ein
Skript angelegt:

```bash
docker compose exec backend python -m app.create_user \
  --email max.muster@sgs.de --name "Max Muster" --password "einStarkesPasswort"
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend läuft unter http://localhost:5173 und proxyt `/api`-Requests an
das Backend. Nach dem Login stehen die Seiten "Kunden", "Produkte" und
"Lidl-Prüfauftrag-Import" zur Verfügung.

## Roadmap

1. ✅ Projekt-Grundgerüst (Docker, FastAPI, Vite/React)
2. ✅ Datenmodell (Kunden, Produkte, Normen/Gesetzesvorgaben, Prüfkatalog,
   Prüfprogramme, Prüfaufträge, Prüfpläne)
3. ✅ Login/Auth (JWT, eine Rolle für alle Nutzer)
4. ✅ Stammdaten-Datenmodell (Normenfinder, Produktspezifikation,
   Lidl-Warengruppen) + Import der realen Excel-Referenzdaten
5. ✅ Lidl-Prüfauftrag-Import (PDF-Parser)
6. Menü-basierte Prüfungsauswahl für andere Kunden, inkl.
   kaskadierender Normenfinder-Auswahl
7. Prüfplan-Generierungslogik inkl. Kostenberechnung
8. Export als Excel & PDF
9. ✅ CRUD/API für Kunden, Produkte
10. Monitoring-Dashboard
