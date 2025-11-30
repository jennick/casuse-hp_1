import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

interface LocationState {
  from?: { pathname: string };
}

const LoginPage: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const navigate = useNavigate();
  const location = useLocation();
  const state = location.state as LocationState | null;

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (!email || !password) {
      setError("Vul e-mail en wachtwoord in.");
      return;
    }

    // TODO: hier later echte API-call naar verkoop-backend of Casuse-Core.
    // Voor nu simuleren we een geslaagde login met een dummy token.
    try {
      localStorage.setItem("verkoop_access_token", "dev-token");
    } catch {
      // niets, in dev is dit genoeg
    }

    const destination =
      state?.from?.pathname && state.from.pathname !== "/login"
        ? state.from.pathname
        : "/dashboard";

    navigate(destination, { replace: true });
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-header-title">Casuse · Verkoopmodule</div>
      </header>
      <div className="app-main">
        <main
          className="app-content"
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "flex-start",
            paddingTop: "4rem",
          }}
        >
          <div
            className="card"
            style={{ maxWidth: "420px", width: "100%" }}
          >
            <h1>Inloggen verkoopmodule</h1>
            <p
              style={{
                fontSize: "0.9rem",
                color: "#4b5563",
                marginTop: 0,
                marginBottom: "1rem",
              }}
            >
              Meld je aan met je verkoop-account. Alleen gebruikers met
              toegang tot deze module kunnen door.
            </p>
            <form onSubmit={handleSubmit} className="form-grid">
              <div className="form-field">
                <label>E-mail</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  autoComplete="username"
                />
              </div>
              <div className="form-field">
                <label>Wachtwoord</label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  autoComplete="current-password"
                />
              </div>
              {error && (
                <p
                  style={{
                    color: "#b91c1c",
                    fontSize: "0.9rem",
                    marginTop: "0.25rem",
                    gridColumn: "1 / -1",
                  }}
                >
                  {error}
                </p>
              )}
              <div
                style={{
                  gridColumn: "1 / -1",
                  marginTop: "0.75rem",
                  display: "flex",
                  justifyContent: "flex-end",
                }}
              >
                <button className="button" type="submit">
                  Inloggen
                </button>
              </div>
            </form>
          </div>
        </main>
      </div>
    </div>
  );
};

export default LoginPage;
