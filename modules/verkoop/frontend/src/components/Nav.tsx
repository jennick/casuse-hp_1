import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import type { Lang } from "../App";
import { setAuthToken } from "../lib/api";

type NavProps = {
  lang: Lang;
  onLangChange: (lang: Lang) => void;
};

const Nav: React.FC<NavProps> = ({ lang, onLangChange }) => {
  const navigate = useNavigate();

  const handleSignOut = () => {
    setAuthToken(null);
    // Terug naar modules-pagina in core-frontend
    window.location.href = "http://localhost:20020";
  };

  return (
    <header className="bg-slate-900 text-white">
      <nav className="max-w-6xl mx-auto flex items-center justify-between px-4 py-3">
        <div className="font-semibold text-lg">Sales Manager</div>
        <div className="flex items-center gap-6 text-sm">
          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              isActive ? "font-semibold underline" : "hover:underline"
            }
          >
            Dashboard
          </NavLink>
          <NavLink
            to="/sellers"
            className={({ isActive }) =>
              isActive ? "font-semibold underline" : "hover:underline"
            }
          >
            Sellers
          </NavLink>
          <NavLink
            to="/assignments"
            className={({ isActive }) =>
              isActive ? "font-semibold underline" : "hover:underline"
            }
          >
            Assignments
          </NavLink>
          <NavLink
            to="/quotes"
            className={({ isActive }) =>
              isActive ? "font-semibold underline" : "hover:underline"
            }
          >
            Quotes
          </NavLink>
          <NavLink
            to="/orders"
            className={({ isActive }) =>
              isActive ? "font-semibold underline" : "hover:underline"
            }
          >
            Orders
          </NavLink>
          <NavLink
            to="/payments"
            className={({ isActive }) =>
              isActive ? "font-semibold underline" : "hover:underline"
            }
          >
            Payments
          </NavLink>
          <NavLink
            to="/settings"
            className={({ isActive }) =>
              isActive ? "font-semibold underline" : "hover:underline"
            }
          >
            Settings
          </NavLink>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={lang}
            onChange={(e) => onLangChange(e.target.value as Lang)}
            className="rounded-md bg-slate-800 border border-slate-600 px-2 py-1 text-sm"
          >
            <option value="en">EN</option>
            <option value="es">ES</option>
          </select>
          <button
            type="button"
            onClick={handleSignOut}
            className="rounded-md bg-red-600 px-3 py-1 text-sm font-medium hover:bg-red-500"
          >
            Sign out
          </button>
        </div>
      </nav>
    </header>
  );
};

export { Nav };
