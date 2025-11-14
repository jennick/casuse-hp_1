import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import type { Lang } from "../App";
import { Nav } from "./Nav";
import DashboardPage from "../pages/Dashboard";
import SellersPage from "../pages/Sellers";
import AssignmentsPage from "../pages/Assignments";
import QuotesPage from "../pages/Quotes";
import OrdersPage from "../pages/Orders";
import PaymentsPage from "../pages/Payments";
import SettingsPage from "../pages/Settings";
import FeasibilityPage from "../pages/Feasibility";

type LayoutProps = {
  lang: Lang;
  onLangChange: (lang: Lang) => void;
};

const Layout: React.FC<LayoutProps> = ({ lang, onLangChange }) => {
  const handleBackToModules = () => {
    window.location.href = "http://localhost:20020";
  };

  return (
    <div className="min-h-screen bg-slate-100">
      <Nav lang={lang} onLangChange={onLangChange} />
      <main className="max-w-6xl mx-auto px-4 py-6">
        <div className="flex justify-end mb-4">
          <button
            type="button"
            onClick={handleBackToModules}
            className="inline-flex items-center rounded-full border border-slate-300 bg-white px-4 py-1 text-sm font-medium text-slate-700 hover:bg-slate-50"
          >
            ← Terug naar modules
          </button>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-6">
          <Routes>
            <Route path="/dashboard" element={<DashboardPage lang={lang} />} />
            <Route path="/sellers" element={<SellersPage lang={lang} />} />
            <Route
              path="/assignments"
              element={<AssignmentsPage lang={lang} />}
            />
            <Route path="/quotes" element={<QuotesPage lang={lang} />} />
            <Route path="/orders" element={<OrdersPage lang={lang} />} />
            <Route path="/payments" element={<PaymentsPage lang={lang} />} />
            <Route
              path="/feasibility"
              element={<FeasibilityPage lang={lang} />}
            />
            <Route path="/settings" element={<SettingsPage lang={lang} />} />
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </div>
      </main>
    </div>
  );
};

export default Layout;
