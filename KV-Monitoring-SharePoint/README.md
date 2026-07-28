# KV-Monitoring – zentrale Version für SharePoint / Excel Online

Eine einzelne Excel-Arbeitsmappe (`KV-Monitoring-SharePoint.xlsx`) mit
denselben Daten wie die Offline-App (`KV-Monitoring-Offline/`), aber als
Excel-Tabellen statt als lokale HTML-Datei — damit sie über SharePoint/
OneDrive gemeinsam und **gleichzeitig** bearbeitet werden kann (Excel-Online-
Co-Authoring), statt Arbeitsstände manuell per JSON zusammenführen zu müssen.

Die genaue Anleitung steht auch **direkt im ersten Tabellenblatt
"Anleitung"** der Datei selbst.

## Kurzfassung

1. Datei in eine SharePoint-Dokumentbibliothek oder einen Teams-/OneDrive-
   Ordner hochladen, auf den alle Zugriff haben.
2. Dort mit "In Excel im Browser öffnen" starten (nicht herunterladen und
   lokal bearbeiten – nur im Browser/mit aktivem AutoSpeichern ist die
   Bearbeitung wirklich gleichzeitig und in Echtzeit sichtbar).
3. Bearbeitungsrechte über die SharePoint-Freigabe vergeben.
4. Danach arbeiten alle in derselben Datei über denselben Link.

## Aufbau (6 Tabellenblätter + Anleitung)

- **Arbeitsvorrat** – 1.230 Zeilen aus dem bestehenden SAP-Export, als
  Excel-Tabelle. Dropdown-Validierung für LFGB?/Trivial?/Mech. erledigt.
- **Pruefauftraege** + **PA_Felder** – ein Kopf-Eintrag pro IAN
  (Pruefauftraege) plus beliebig viele Schlüssel/Wert-Zeilen dazu
  (PA_Felder), verknüpft über die Spalte IAN. Enthält je eine
  Beispielzeile (bitte vor echter Nutzung löschen).
- **KV_Kopf** + **KV_Positionen** – ein Kopf-Eintrag pro Kostenvoranschlag
  (KV_Kopf) plus beliebig viele Prüfpositionen dazu (KV_Positionen),
  verknüpft über IAN. Die Spalte "Summe" in KV_Positionen (`=Kosten*Anzahl`)
  und "Gesamtsumme aktiv (€)" in KV_Kopf (`SUMIFS` über alle aktiven
  Positionen derselben IAN) rechnen automatisch – nichts manuell
  nachpflegen. Enthält je eine Beispielzeile (bitte löschen).
- **Katalog** – die 18 wiederverwendbaren mechanischen Prüfpositionen mit
  Standardkosten/SAP-Code, zum Nachschlagen/Kopieren beim Anlegen neuer
  KV-Positionen.

Alle Formeln wurden geprüft (LibreOffice-Neuberechnung, 0 Fehler) und mit
berechneten Werten gespeichert.

## Was dabei bewusst wegfällt (im Vergleich zur Offline-App)

- **Kein automatischer PDF-Upload/Feld-Erkennung** für Prüfaufträge – das
  müsste separat in der Offline-App erzeugt und die Ergebnisse dann von Hand
  in `Pruefauftraege`/`PA_Felder` übertragen werden (oder komplett manuell
  eingetragen werden).
- **Kein automatisierter Excel-Upload mit Duplikat-Erkennung** für den
  Arbeitsvorrat – neue SAP-Exporte müssen von Hand einkopiert werden
  (Zeilen im Export markieren, kopieren, unten in die Arbeitsvorrat-Tabelle
  einfügen; Excel erweitert die Tabelle automatisch).
- **Keine "Als Vorlage duplizieren"-Schaltfläche** – ähnliche KVs manuell
  suchen (Filter auf `KV_Kopf`/`KV_Positionen`) und Zeilen kopieren.

Das ist der Preis für "schnell und zentral mit Bordmitteln". Falls diese
Automatisierungen später wichtiger werden als Echtzeit-Zusammenarbeit, ist
der in `KV-Monitoring-Offline/` beschriebene Weg 2 (echter Web-Dienst mit
Microsoft-Login) die konsequente Weiterentwicklung.
