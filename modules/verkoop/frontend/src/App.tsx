import React, { useEffect, useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import { RequireAuth } from "./components/RequireAuth";
import Layout from "./components/Layout";
import LoginPage from "./pages/Login";

export type Lang = "en" | "es";

const LANG_STORAGE_KEY = "verkoop_ui_lang";

const AppRoutes: React.FC = () => {
  const [lang, setLang] = useState<Lang>("en");

  useEffect(() => {
    if (typeof window === "undefined") return;
    const stored = window.localStorage.getItem(LANG_STORAGE_KEY) as Lang | null;
    if (stored === "en" || stored === "es") {
      setLang(stored);
    }
  }, []);

  const handleLangChange = (value: Lang) => {
    setLang(value);
    if (typeof window !== "undefined") {
      window.localStorage.setItem(LANG_STORAGE_KEY, value);
    }
  };

  return (
    <Routes>
      <Route
        path="/login"
        element={<LoginPage lang={lang} onLangChange={handleLangChange} />}
      />
      <Route
        path="/*"
        element={
          <RequireAuth>
            <Layout lang={lang} onLangChange={handleLangChange} />
          </RequireAuth>
        }
      />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
};

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  );
};

export default App;
