import React from "react";
import { NavLink, Outlet } from "react-router-dom";

function getModulesBaseUrl(): string {
  if (typeof import.meta !== "undefined") {
    const env: any = (import.meta as any).env || {};
    return env.VITE_MODULES_BASE_URL || "";
  }
  return "";
}

const Layout: React.FC = () => {
  const modulesBase = getModulesBaseUrl();

  function goToModules() {
    if (modulesBase) {
      window.location.href = modulesBase;
    } else {
      // Fallback: als er geen URL is ingesteld, ga naar root
      window.location.href = "/";
    }
  }

  function handleLogout() {
    try {
      // Hier later JWT / refresh-tokens / localStorage keys van de verkoopmodule wissen
      localStorage.removeItem("verkoop_access_token");
      localStorage.removeItem("verkoop_refresh_token");
    } catch {
      // stil falen, is geen ramp
    }

    // Na logout altijd terug naar de modulespagina van casuse-hp
    goToModules();
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-header-title">Casuse · Verkoopmodule</div>
        <div className="app-header-right">
          <button
            type="button"
            className="button secondary"
            style={{ marginRight: "0.5rem" }}
            onClick={goToModules}
          >
            ← Terug naar modules
          </button>
          <button
            type="button"
            className="button"
            onClick={handleLogout}
          >
            Logout
          </button>
        </div>
      </header>
      <div className="app-main">
        <nav className="app-nav">
          <NavLink
            to="/dashboard"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Dashboard
          </NavLink>
          <NavLink
            to="/sellers"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Verkopers
          </NavLink>
          <NavLink
            to="/customers"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Klanten
          </NavLink>
          <NavLink
            to="/quotes"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Offertes
          </NavLink>
          <NavLink
            to="/orders"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Orders
          </NavLink>
          <NavLink
            to="/assignments"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Toewijzingen
          </NavLink>
          <NavLink
            to="/payments"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Betalingen
          </NavLink>
          <NavLink
            to="/settings"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Instellingen
          </NavLink>
        </nav>
        <main className="app-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
