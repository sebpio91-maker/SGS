import { useEffect, useState, type CSSProperties } from "react";
import {
  generateTestPlan,
  listProducts,
  listTestOrders,
  listTestPlans,
  type Product,
  type TestOrder,
  type TestPlan,
} from "../lib/api";

const money = (v: number | null) => (v == null ? "–" : `${v.toFixed(2)} €`);

export default function TestPlansPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [testOrders, setTestOrders] = useState<TestOrder[]>([]);
  const [plans, setPlans] = useState<TestPlan[]>([]);
  const [productId, setProductId] = useState<number | "">("");
  const [testOrderId, setTestOrderId] = useState<number | "">("");
  const [error, setError] = useState<string | null>(null);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    listProducts().then(setProducts).catch(() => setError("Produkte konnten nicht geladen werden"));
  }, []);

  useEffect(() => {
    if (productId === "") {
      setTestOrders([]);
      setPlans([]);
      return;
    }
    listTestOrders().then((orders) =>
      setTestOrders(orders.filter((o) => o.product_id === productId)),
    );
    listTestPlans(productId).then(setPlans).catch(() => setError("Prüfpläne konnten nicht geladen werden"));
    setTestOrderId("");
  }, [productId]);

  async function handleGenerate() {
    if (productId === "") return;
    setGenerating(true);
    setError(null);
    try {
      const plan = await generateTestPlan({
        product_id: productId,
        test_order_id: testOrderId === "" ? null : testOrderId,
      });
      setPlans((prev) => [plan, ...prev]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Generierung fehlgeschlagen");
    } finally {
      setGenerating(false);
    }
  }

  return (
    <section>
      <h2>Prüfpläne</h2>
      {error && <p style={{ color: "crimson" }}>{error}</p>}

      <div style={{ marginBottom: "1rem" }}>
        <select value={productId} onChange={(e) => setProductId(e.target.value === "" ? "" : Number(e.target.value))}>
          <option value="">Produkt wählen...</option>
          {products.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name} ({p.article_number})
            </option>
          ))}
        </select>{" "}
        <select
          value={testOrderId}
          onChange={(e) => setTestOrderId(e.target.value === "" ? "" : Number(e.target.value))}
          disabled={testOrders.length === 0}
        >
          <option value="">Kein Prüfauftrag (manuelle Auswahl)</option>
          {testOrders.map((o) => (
            <option key={o.id} value={o.id}>
              Prüfauftrag #{o.id} ({o.order_number})
            </option>
          ))}
        </select>{" "}
        <button onClick={handleGenerate} disabled={productId === "" || generating}>
          {generating ? "Erzeuge..." : "Prüfplan generieren"}
        </button>
      </div>

      {plans.map((plan) => (
        <div key={plan.id} style={{ marginBottom: "2rem", border: "1px solid #ccc", padding: "1rem" }}>
          <h3>
            Prüfplan #{plan.id} <span style={{ fontWeight: "normal" }}>({plan.status})</span>
          </h3>
          <table style={{ borderCollapse: "collapse", width: "100%" }}>
            <thead>
              <tr>
                <th style={th}>Kategorie</th>
                <th style={th}>Prüfpunkt</th>
                <th style={th}>Norm</th>
                <th style={th}>Laborzeit</th>
                <th style={th}>Laborkosten</th>
                <th style={th}>VK-Preis</th>
              </tr>
            </thead>
            <tbody>
              {plan.items.map((item) => (
                <tr key={item.id}>
                  <td style={td}>{item.category_name}</td>
                  <td style={td}>{item.name}</td>
                  <td style={td}>{item.norm_reference ?? "–"}</td>
                  <td style={td}>{item.lab_minutes != null ? `${item.lab_minutes} min` : "–"}</td>
                  <td style={td}>{money(item.lab_cost)}</td>
                  <td style={td}>{money(item.sale_price)}</td>
                </tr>
              ))}
            </tbody>
            <tfoot>
              <tr>
                <td style={td} colSpan={3}>
                  <strong>Summe</strong>
                </td>
                <td style={td}>
                  <strong>{plan.lab_minutes_total} min</strong>
                </td>
                <td style={td}>
                  <strong>{money(plan.lab_cost_total)}</strong>
                </td>
                <td style={td}>
                  <strong>{money(plan.sale_price_total)}</strong>
                </td>
              </tr>
            </tfoot>
          </table>
        </div>
      ))}
    </section>
  );
}

const th: CSSProperties = { textAlign: "left", borderBottom: "1px solid #ccc", padding: "0.4rem" };
const td: CSSProperties = { borderBottom: "1px solid #eee", padding: "0.4rem" };
