import React, { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { api } from "../lib/api";

const SellerPasswordResetPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const token = searchParams.get("token") || "";

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [done, setDone] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      setError("De resetlink is ongeldig of ontbreekt.");
    }
  }, [token]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!token) {
      setError("De resetlink is ongeldig of ontbreekt.");
      return;
    }

    if (password.length < 8) {
      setError("Het wachtwoord moet minstens 8 tekens lang zijn.");
      return;
    }

    if (password !== confirmPassword) {
      setError("De wachtwoorden komen niet overeen.");
      return;
    }

    try {
      setSubmitting(true);
      setError(null);

      await api.post("/sellers/reset-password", {
        token,
        new_password: password,
      });

      setDone(true);
    } catch (e: any) {
      console.error(e);
      setError(e?.message ?? "Kon het wachtwoord niet resetten.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="layout-public">
      <div className="card" style={{ maxWidth: 480, margin: "2rem auto" }}>
        <h1>Wachtwoord resetten</h1>

        {!token && (
          <p style={{ color: "#b91c1c" }}>
            De resetlink is ongeldig of ontbreekt.
          </p>
        )}

        {token && !done && (
          <form onSubmit={handleSubmit} className="form-grid">
            <div className="form-field">
              <label>Nieuw wachtwoord</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="new-password"
              />
            </div>
            <div className="form-field">
              <label>Bevestig nieuw wachtwoord</label>
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                autoComplete="new-password"
              />
            </div>

            {error && (
              <p style={{ color: "#b91c1c", gridColumn: "1 / -1" }}>
                {error}
              </p>
            )}

            <div
              style={{
                gridColumn: "1 / -1",
                display: "flex",
                gap: "0.5rem",
                marginTop: "0.5rem",
              }}
            >
              <button
                type="submit"
                className="button"
                disabled={submitting || !token}
              >
                {submitting ? "Bezig…" : "Wachtwoord instellen"}
              </button>

              <button
                type="button"
                className="button secondary"
                onClick={() => navigate("/")}
              >
                Terug naar modules
              </button>
            </div>
          </form>
        )}

        {token && done && (
          <>
            <p>
              Je wachtwoord is succesvol ingesteld. Je kan dit venster sluiten
              en verdergaan naar je verkoopomgeving.
            </p>
            <button
              type="button"
              className="button"
              onClick={() => navigate("/")}
            >
              Terug naar modules
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default SellerPasswordResetPage;
