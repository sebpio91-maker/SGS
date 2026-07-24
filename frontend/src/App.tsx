import { AuthProvider, useAuth } from "./context/AuthContext";
import LoginPage from "./pages/LoginPage";

function Dashboard() {
  const { user, logout } = useAuth();

  return (
    <main style={{ fontFamily: "sans-serif", padding: "2rem" }}>
      <h1>SGS Prüfplan-App</h1>
      <p>
        Angemeldet als {user?.full_name} ({user?.email})
      </p>
      <button onClick={logout} style={{ padding: "0.5rem 1rem" }}>
        Abmelden
      </button>
      <p style={{ marginTop: "2rem" }}>
        Nächste Schritte: Stammdatenverwaltung, Prüfauftrag-Import, Prüfplan-Erstellung.
      </p>
    </main>
  );
}

function AppContent() {
  const { user, loading } = useAuth();

  if (loading) {
    return <p style={{ fontFamily: "sans-serif", padding: "2rem" }}>Lade...</p>;
  }

  return user ? <Dashboard /> : <LoginPage />;
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
