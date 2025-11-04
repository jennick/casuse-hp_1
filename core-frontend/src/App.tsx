import React, { useEffect, useState } from "react";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import { getModules } from "./api";
import AIHelper from "./components/AIHelper";

const App: React.FC = () => {
  const [token, setToken] = useState<string | null>(null);
  const [modules, setModules] = useState<any[]>([]);

  useEffect(() => {
    if (token) {
      getModules(token)
        .then(setModules)
        .catch(() => setModules([]));
    } else {
      // bij uitloggen modules leegmaken
      setModules([]);
    }
  }, [token]);

  const handleLogout = () => {
    setToken(null);

    // Als je in Login of elders een token in localStorage zet,
    // kun je die hier ook weghalen:
    // localStorage.removeItem("token");
  };

  return (
    <div className="app">
      <header className="topbar">
        <h1>casuse-hp</h1>
        {token && (
          <button className="logout-button" onClick={handleLogout}>
            Log uit
          </button>
        )}
      </header>

      <div className="content">
        {!token ? (
          <Login onSuccess={setToken} />
        ) : (
          <>
            <Dashboard modules={modules} />
            <AIHelper />
          </>
        )}
      </div>
    </div>
  );
};

export default App;
