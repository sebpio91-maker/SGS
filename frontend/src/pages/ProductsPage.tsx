import { useEffect, useState, type CSSProperties, type FormEvent } from "react";
import {
  createProduct,
  deleteProduct,
  listCustomers,
  listProducts,
  updateProduct,
  type Customer,
  type Product,
} from "../lib/api";

export default function ProductsPage() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [filterCustomerId, setFilterCustomerId] = useState<number | "">("");

  const [customerId, setCustomerId] = useState<number | "">("");
  const [articleNumber, setArticleNumber] = useState("");
  const [name, setName] = useState("");
  const [category, setCategory] = useState("");
  const [hasBattery, setHasBattery] = useState(false);
  const [hasManual, setHasManual] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);

  async function reload(customerFilter: number | "") {
    try {
      setProducts(await listProducts(customerFilter === "" ? undefined : customerFilter));
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Fehler beim Laden");
    }
  }

  useEffect(() => {
    listCustomers().then(setCustomers).catch(() => setError("Kunden konnten nicht geladen werden"));
    reload("");
  }, []);

  useEffect(() => {
    reload(filterCustomerId);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filterCustomerId]);

  function resetForm() {
    setEditingId(null);
    setCustomerId("");
    setArticleNumber("");
    setName("");
    setCategory("");
    setHasBattery(false);
    setHasManual(false);
  }

  function startEdit(product: Product) {
    setEditingId(product.id);
    setCustomerId(product.customer_id);
    setArticleNumber(product.article_number);
    setName(product.name);
    setCategory(product.category ?? "");
    setHasBattery(product.has_battery);
    setHasManual(product.has_manual);
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    if (customerId === "") {
      setError("Bitte einen Kunden auswählen");
      return;
    }
    try {
      const payload = {
        customer_id: customerId,
        article_number: articleNumber,
        name,
        category: category || null,
        has_battery: hasBattery,
        has_manual: hasManual,
      };
      if (editingId !== null) {
        await updateProduct(editingId, payload);
      } else {
        await createProduct(payload);
      }
      resetForm();
      await reload(filterCustomerId);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Speichern fehlgeschlagen");
    }
  }

  async function handleDelete(id: number) {
    setError(null);
    try {
      await deleteProduct(id);
      await reload(filterCustomerId);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Löschen fehlgeschlagen");
    }
  }

  function customerName(id: number): string {
    return customers.find((c) => c.id === id)?.name ?? `#${id}`;
  }

  return (
    <section>
      <h2>Produkte</h2>
      {error && <p style={{ color: "crimson" }}>{error}</p>}

      <div style={{ marginBottom: "1rem" }}>
        <label>
          Filter nach Kunde:{" "}
          <select
            value={filterCustomerId}
            onChange={(e) => setFilterCustomerId(e.target.value === "" ? "" : Number(e.target.value))}
          >
            <option value="">Alle</option>
            {customers.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </label>
      </div>

      <form onSubmit={handleSubmit} style={{ marginBottom: "1.5rem" }}>
        <select
          value={customerId}
          onChange={(e) => setCustomerId(e.target.value === "" ? "" : Number(e.target.value))}
          required
          style={{ marginRight: "0.5rem", padding: "0.4rem" }}
        >
          <option value="">Kunde wählen...</option>
          {customers.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
        <input
          placeholder="Artikelnummer"
          value={articleNumber}
          onChange={(e) => setArticleNumber(e.target.value)}
          required
          style={{ marginRight: "0.5rem", padding: "0.4rem" }}
        />
        <input
          placeholder="Produktname"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          style={{ marginRight: "0.5rem", padding: "0.4rem" }}
        />
        <input
          placeholder="Kategorie"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          style={{ marginRight: "0.5rem", padding: "0.4rem" }}
        />
        <label style={{ marginRight: "0.5rem" }}>
          <input
            type="checkbox"
            checked={hasBattery}
            onChange={(e) => setHasBattery(e.target.checked)}
          />{" "}
          Akku/Batterie
        </label>
        <label style={{ marginRight: "0.5rem" }}>
          <input
            type="checkbox"
            checked={hasManual}
            onChange={(e) => setHasManual(e.target.checked)}
          />{" "}
          Anleitung
        </label>
        <button type="submit" style={{ padding: "0.4rem 0.8rem" }}>
          {editingId !== null ? "Speichern" : "Anlegen"}
        </button>
        {editingId !== null && (
          <button type="button" onClick={resetForm} style={{ marginLeft: "0.5rem" }}>
            Abbrechen
          </button>
        )}
      </form>

      <table style={{ borderCollapse: "collapse", width: "100%" }}>
        <thead>
          <tr>
            <th style={thStyle}>Kunde</th>
            <th style={thStyle}>Artikelnummer</th>
            <th style={thStyle}>Name</th>
            <th style={thStyle}>Kategorie</th>
            <th style={thStyle}>Akku</th>
            <th style={thStyle}>Anleitung</th>
            <th style={thStyle}></th>
          </tr>
        </thead>
        <tbody>
          {products.map((p) => (
            <tr key={p.id}>
              <td style={tdStyle}>{customerName(p.customer_id)}</td>
              <td style={tdStyle}>{p.article_number}</td>
              <td style={tdStyle}>{p.name}</td>
              <td style={tdStyle}>{p.category}</td>
              <td style={tdStyle}>{p.has_battery ? "Ja" : "Nein"}</td>
              <td style={tdStyle}>{p.has_manual ? "Ja" : "Nein"}</td>
              <td style={tdStyle}>
                <button onClick={() => startEdit(p)} style={{ marginRight: "0.5rem" }}>
                  Bearbeiten
                </button>
                <button onClick={() => handleDelete(p.id)}>Löschen</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

const thStyle: CSSProperties = {
  textAlign: "left",
  borderBottom: "1px solid #ccc",
  padding: "0.4rem",
};
const tdStyle: CSSProperties = { borderBottom: "1px solid #eee", padding: "0.4rem" };
