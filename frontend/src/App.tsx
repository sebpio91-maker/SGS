import { useEffect, useState } from "react";

type HealthResponse = {
  status: string;
  app: string;
};

export default function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/health")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(setHealth)
      .catch((err) => setError(String(err)));
  }, []);

  return (
    <main style={{ fontFamily: "sans-serif", padding: "2rem" }}>
      <h1>SGS Prüfplan-App</h1>
      <p>Grundgerüst steht. Nächste Schritte: Datenmodell, Login, Stammdaten.</p>
      {error && <p style={{ color: "crimson" }}>Backend nicht erreichbar: {error}</p>}
      {health && (
        <p style={{ color: "green" }}>
          Backend-Status: {health.status} ({health.app})
        </p>
      )}
    </main>
  );
}
