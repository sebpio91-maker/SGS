#!/bin/bash
# Läuft automatisch beim ersten Start des Codespace (postCreateCommand).
# Baut Backend + Datenbank, spielt Demo-Daten und einen Login-Benutzer
# ein, und installiert die Frontend-Abhängigkeiten. Danach reicht im
# Terminal: `cd frontend && npm run dev`.
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -f backend/.env ]; then
  cp backend/.env.example backend/.env
fi

docker compose up --build -d

echo "Warte auf Backend/Datenbank..."
for _ in $(seq 1 30); do
  if docker compose exec -T backend python -c "from app.db.session import engine; engine.connect().close()" >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

docker compose exec -T backend python -m app.seed_demo

docker compose exec -T backend python -m app.create_user \
  --email test@sgs.de --name "Test Nutzer" --password geheim123 || true

(cd frontend && npm install)

cat <<'EOF'

==========================================================
Setup fertig!

Noch ein letzter Schritt im Terminal:

    cd frontend && npm run dev

Codespaces öffnet dann automatisch einen Browser-Tab mit der App.
Login: test@sgs.de / geheim123
Auf der Seite "Prüfpläne" das Produkt "Demo-Campingtisch" auswählen.
==========================================================
EOF
