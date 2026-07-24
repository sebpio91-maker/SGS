import { NavLink, Route, HashRouter as Router, Routes } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import LoginPage from "./pages/LoginPage";
import CustomersPage from "./pages/CustomersPage";
import ProductsPage from "./pages/ProductsPage";
import LidlImportPage from "./pages/LidlImportPage";

function Home() {
  return <p>Nächste Schritte: Prüfplan-Erstellung.</p>;
}

const navLinkStyle = ({ isActive }: { isActive: boolean }) => ({
  marginRight: "1rem",
  fontWeight: isActive ? "bold" : "normal",
});

function AppShell() {
  const { user, logout } = useAuth();

  return (
    <main style={{ fontFamily: "sans-serif", padding: "2rem" }}>
      <h1>SGS Prüfplan-App</h1>
      <p>
        Angemeldet als {user?.full_name} ({user?.email}){" "}
        <button onClick={logout} style={{ marginLeft: "1rem" }}>
          Abmelden
        </button>
      </p>

      <nav style={{ margin: "1rem 0", borderBottom: "1px solid #ccc", paddingBottom: "0.5rem" }}>
        <NavLink to="/" end style={navLinkStyle}>
          Start
        </NavLink>
        <NavLink to="/kunden" style={navLinkStyle}>
          Kunden
        </NavLink>
        <NavLink to="/produkte" style={navLinkStyle}>
          Produkte
        </NavLink>
        <NavLink to="/lidl-import" style={navLinkStyle}>
          Lidl-Prüfauftrag-Import
        </NavLink>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/kunden" element={<CustomersPage />} />
        <Route path="/produkte" element={<ProductsPage />} />
        <Route path="/lidl-import" element={<LidlImportPage />} />
      </Routes>
    </main>
  );
}

function AppContent() {
  const { user, loading } = useAuth();

  if (loading) {
    return <p style={{ fontFamily: "sans-serif", padding: "2rem" }}>Lade...</p>;
  }

  return user ? <AppShell /> : <LoginPage />;
}

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
}
