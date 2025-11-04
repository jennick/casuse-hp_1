import React, { useState } from "react";
import { login } from "../api";

const Login: React.FC<{ onSuccess: (t: string) => void }> = ({ onSuccess }) => {
  const [email, setEmail] = useState("admin@casuse-hp.local");
  const [password, setPassword] = useState("Casuse!2025");
  const [totp, setTotp] = useState("");
  const [error, setError] = useState("");

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await login(email, password, totp || undefined);
      onSuccess(res.access_token);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Login mislukt");
    }
  };

  return (
    <div className="login-container">
      <h2>Inloggen</h2>
      <form onSubmit={submit}>
        <label>E-mail</label>
        <input value={email} onChange={(e) => setEmail(e.target.value)} />
        <label>Wachtwoord</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <label>2FA (optioneel)</label>
        <input value={totp} onChange={(e) => setTotp(e.target.value)} />
        <button type="submit">Login</button>
        {error && <p className="error">{error}</p>}
      </form>
    </div>
  );
};

export default Login;
