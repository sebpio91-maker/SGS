import { useState, type ChangeEvent, type CSSProperties } from "react";
import { importLidlPruefauftrag, type LidlImportResult } from "../lib/api";

const CATEGORY_LABELS: Record<string, string> = {
  chemie_lfgb: "Chemie / LFGB",
  sicherheit_norm: "Sicherheit & Norm / Sonder- & Funktionsparameter",
  produktspezifikation: "(Physikalische-) Produktspezifikationen",
  verpackung: "Verpackung / Transportverpackung",
  verarbeitung_aql: "Verarbeitung (AQL)",
  on_site_testing: "On-Site Testing",
  standsicherheit: "SLT (Standsicherheit)",
  selbstauskunft: "Selbstauskunft",
};

export default function LidlImportPage() {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<LidlImportResult | null>(null);

  async function handleFileChange(e: ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setError(null);
    setResult(null);
    try {
      setResult(await importLidlPruefauftrag(file));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Import fehlgeschlagen");
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  }

  return (
    <section>
      <h2>Lidl-Prüfauftrag importieren</h2>
      <p>Lade den Prüfauftrag als PDF hoch. IAN/Charge, Artikeldaten und Prüfumfang werden automatisch erkannt.</p>

      <input type="file" accept="application/pdf" onChange={handleFileChange} disabled={uploading} />
      {uploading && <p>Wird verarbeitet...</p>}
      {error && <p style={{ color: "crimson" }}>{error}</p>}

      {result && (
        <div style={{ marginTop: "1.5rem" }}>
          <h3>Erkannt: {result.product.name}</h3>
          <table style={{ borderCollapse: "collapse" }}>
            <tbody>
              <tr>
                <td style={tdLabel}>IAN / Charge</td>
                <td style={tdValue}>{result.product.article_number}</td>
              </tr>
              <tr>
                <td style={tdLabel}>Warenbereich</td>
                <td style={tdValue}>{result.product.category}</td>
              </tr>
              <tr>
                <td style={tdLabel}>Akku/Batterie</td>
                <td style={tdValue}>{result.product.has_battery ? "Ja" : "Nein"}</td>
              </tr>
              <tr>
                <td style={tdLabel}>Anleitung</td>
                <td style={tdValue}>{result.product.has_manual ? "Ja" : "Nein"}</td>
              </tr>
              <tr>
                <td style={tdLabel}>Referenzprüfung</td>
                <td style={tdValue}>{result.referenzpruefung ? "Ja" : "Nein"}</td>
              </tr>
              <tr>
                <td style={tdLabel}>NGO-Prüfung</td>
                <td style={tdValue}>{result.ngo_pruefung ? "Ja" : "Nein"}</td>
              </tr>
              <tr>
                <td style={tdLabel}>FFU-Prüfung</td>
                <td style={tdValue}>{result.ffu_pruefung ? "Ja" : "Nein"}</td>
              </tr>
            </tbody>
          </table>

          <h4 style={{ marginTop: "1rem" }}>Erkannter Prüfumfang</h4>
          <ul>
            {result.pruefumfang_kategorien.length === 0 && <li>Keine Kategorien erkannt</li>}
            {result.pruefumfang_kategorien.map((key) => (
              <li key={key}>{CATEGORY_LABELS[key] ?? key}</li>
            ))}
          </ul>

          <p style={{ color: "green" }}>
            Produkt und Prüfauftrag wurden gespeichert (Prüfauftrag-ID: {result.test_order.id}).
          </p>
        </div>
      )}
    </section>
  );
}

const tdLabel: CSSProperties = { fontWeight: "bold", padding: "0.2rem 1rem 0.2rem 0" };
const tdValue: CSSProperties = { padding: "0.2rem 0" };
