import { Outlet } from "react-router-dom";

const CORE_HOME_URL =
  import.meta.env.VITE_CORE_HOME_URL || "http://localhost:20020";

export default function AdminLayout() {
  /**
   * Logout:
   * - token verwijderen
   * - admin SPA verlaten
   * - DIRECT naar core (geen loginpagina)
   */
  const handleLogout = () => {
    localStorage.removeItem("website_admin_token");
    window.location.replace(CORE_HOME_URL);
  };

  /**
   * Terug naar modules:
   * - extern
   * - zelfde tab
   */
  const handleBackToModules = () => {
    window.location.replace(CORE_HOME_URL);
  };

  return (
    <div className="admin-layout">
      <header
        style={{
          background: "#0b1a33",
          color: "#fff",
          padding: "0.75rem 1.25rem",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <strong>Casuse Website Admin</strong>

        <div style={{ display: "flex", gap: "0.5rem" }}>
          <button onClick={handleBackToModules}>Terug naar modules</button>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </header>

      <main style={{ padding: "1.5rem" }}>
        <Outlet />
      </main>
    </div>
  );
}
