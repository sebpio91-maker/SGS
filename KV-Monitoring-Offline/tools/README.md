# Stammdaten-Export nach Excel

Erzeugt `../Normen_und_Pruefanforderungen.xlsx` aus den Stammdaten in
`../KV-Monitoring.html`. Beide Schritte lesen die Werte über die Funktionen der
Anwendung selbst (`normenBlockSumme`, `normRefListeText`, …), damit der Export
nicht neben dem Tool herläuft.

```bash
pip install playwright openpyxl && playwright install chromium
python3 stammdaten_auslesen.py      # schreibt export.json
python3 stammdaten_excel_bauen.py   # schreibt die Arbeitsmappe
```

Der Export ist bewusst eine Einbahnstraße: Änderungen in der Excel-Datei fließen
nicht zurück ins Tool.
