import { useEffect, useState, type CSSProperties, type FormEvent } from "react";
import {
  createCustomer,
  deleteCustomer,
  listCustomers,
  updateCustomer,
  type Customer,
} from "../lib/api";

export default function CustomersPage() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [name, setName] = useState("");
  const [code, setCode] = useState("");
  const [notes, setNotes] = useState("");
  const [editingId, setEditingId] = useState<number | null>(null);

  async function reload() {
    try {
      setCustomers(await listCustomers());
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Fehler beim Laden");
    }
  }

  useEffect(() => {
    reload();
  }, []);

  function startEdit(customer: Customer) {
    setEditingId(customer.id);
    setName(customer.name);
    setCode(customer.code);
    setNotes(customer.notes ?? "");
  }

  function resetForm() {
    setEditingId(null);
    setName("");
    setCode("");
    setNotes("");
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      if (editingId !== null) {
        await updateCustomer(editingId, { name, code, notes: notes || null });
      } else {
        await createCustomer({ name, code, notes: notes || null });
      }
      resetForm();
      await reload();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Speichern fehlgeschlagen");
    }
  }

  async function handleDelete(id: number) {
    setError(null);
    try {
      await deleteCustomer(id);
      await reload();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Löschen fehlgeschlagen");
    }
  }

  return (
    <section>
      <h2>Kunden</h2>
      {error && <p style={{ color: "crimson" }}>{error}</p>}

      <form onSubmit={handleSubmit} style={{ marginBottom: "1.5rem" }}>
        <input
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          style={{ marginRight: "0.5rem", padding: "0.4rem" }}
        />
        <input
          placeholder="Code (z.B. LIDL)"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          required
          style={{ marginRight: "0.5rem", padding: "0.4rem" }}
        />
        <input
          placeholder="Notizen"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          style={{ marginRight: "0.5rem", padding: "0.4rem" }}
        />
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
            <th style={thStyle}>Name</th>
            <th style={thStyle}>Code</th>
            <th style={thStyle}>Notizen</th>
            <th style={thStyle}></th>
          </tr>
        </thead>
        <tbody>
          {customers.map((c) => (
            <tr key={c.id}>
              <td style={tdStyle}>{c.name}</td>
              <td style={tdStyle}>{c.code}</td>
              <td style={tdStyle}>{c.notes}</td>
              <td style={tdStyle}>
                <button onClick={() => startEdit(c)} style={{ marginRight: "0.5rem" }}>
                  Bearbeiten
                </button>
                <button onClick={() => handleDelete(c.id)}>Löschen</button>
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
