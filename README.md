# SGS Prüfplan-App

Automatische Erstellung von Prüfplänen für Produktprüfungen – basierend auf
Normen, Prüfprogrammen, gesetzlichen Vorgaben (z. B. Kennzeichnung) sowie
Produktspezifikationen und kundenspezifischen Vorgaben.

Zentrales Ausgangsdokument für den Kunden Lidl ist der Prüfauftrag; für
andere Kunden erfolgt die Auswahl der Prüfungen über ein Menü im Katalog.

## Architektur

- **Backend**: Python / FastAPI, PostgreSQL, SQLAlchemy, Alembic
- **Frontend**: React + TypeScript (Vite)
- **Export**: Prüfpläne als Excel (`.xlsx`) und PDF

## Lokale Entwicklung

### Backend + Datenbank (Docker)

```bash
cp backend/.env.example backend/.env
docker compose up --build
```

Backend läuft danach unter http://localhost:8000, Health-Check unter
http://localhost:8000/api/health.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend läuft unter http://localhost:5173 und proxyt `/api`-Requests an
das Backend.

## Roadmap

1. ✅ Projekt-Grundgerüst (Docker, FastAPI, Vite/React)
2. Datenmodell (Kunden, Produkte, Normen/Gesetzesvorgaben, Prüfkatalog,
   Prüfprogramme, Prüfaufträge, Prüfpläne)
3. Login/Auth (JWT)
4. Stammdatenverwaltung (CRUD) für Kunden, Produkte, Prüfkatalog
5. Lidl-Prüfauftrag-Import (Excel-Parser)
6. Menü-basierte Prüfungsauswahl für andere Kunden
7. Prüfplan-Generierungslogik
8. Export als Excel & PDF
