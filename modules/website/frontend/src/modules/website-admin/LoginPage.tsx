import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { apiFetch } from "@/shared/api/apiClient";
import { setWebsiteAdminToken } from "@/shared/auth/tokens";

export default function LoginPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    try {
      setLoading(true);
      setError(null);

      const response = await apiFetch<{ access_token: string }>(
        "/api/admin/login",
        {
          method: "POST",
          body: JSON.stringify({ email, password }),
        }
      );

      // ✅ TOKEN OPSLAAN
      setWebsiteAdminToken(response.access_token);


      navigate("/customers", { replace: true });
    } catch (err) {
      console.error("Login failed", err);
      setError("Ongeldige logingegevens.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h1>Inloggen – Website Admin</h1>

      {error && <div style={{ color: "red" }}>{error}</div>}

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />

      <input
        type="password"
        placeholder="Wachtwoord"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />

      <button type="submit" disabled={loading}>
        Inloggen
      </button>
    </form>
  );
}
