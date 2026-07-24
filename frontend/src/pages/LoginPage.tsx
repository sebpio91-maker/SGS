import { useState, type FormEvent } from "react";
import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await login(email, password);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login fehlgeschlagen");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main style={{ fontFamily: "sans-serif", maxWidth: 360, margin: "4rem auto" }}>
      <h1>SGS Prüfplan-App</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="email">E-Mail</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{ width: "100%", padding: "0.5rem" }}
          />
        </div>
        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="password">Passwort</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ width: "100%", padding: "0.5rem" }}
          />
        </div>
        {error && <p style={{ color: "crimson" }}>{error}</p>}
        <button type="submit" disabled={submitting} style={{ padding: "0.5rem 1rem" }}>
          {submitting ? "Anmelden..." : "Anmelden"}
        </button>
      </form>
    </main>
  );
}
