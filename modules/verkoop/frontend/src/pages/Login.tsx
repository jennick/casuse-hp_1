// modules/verkoop/frontend/src/pages/Login.tsx

import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { request, setAuthToken } from "../lib/api";
import type { Lang } from "../App";

interface LoginResponse {
  access_token: string;
  token_type: string;
}

// Login-endpoint configurabel maken. Standaard: /auth/login
const LOGIN_PATH =
  (typeof import.meta !== "undefined" &&
    (import.meta as any).env.VITE_API_LOGIN_PATH) || "/admin/login";

interface LocationState {
  from?: string;
}

interface LoginPageProps {
  lang: Lang;
  onLangChange: (lang: Lang) => void;
}

export const LoginPage: React.FC<LoginPageProps> = ({ lang, onLangChange }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const from =
    ((location.state as LocationState | null)?.from as string | undefined) ||
    "/dashboard";

  const [email, setEmail] = useState("admin@verkoop.local");
  const [password, setPassword] = useState("admin");
  const [submitting, setSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setErrorMessage(null);

    try {
      // Let op: JSON body { email, password }.
      // Als je backend "username" verwacht, kan je hier email->username mappen.
      const resp = await request<LoginResponse>(LOGIN_PATH, {
        method: "POST",
        body: {
          email,
          password,
        },
        auth: false,
      });

      if (!resp?.access_token) {
        throw new Error("No access token in response");
      }

      // Token opslaan
      setAuthToken(resp.access_token);

      // Door naar dashboard (of naar oorspronkelijke route)
      navigate(from, { replace: true });
    } catch (err: any) {
      console.error("Login failed", err);
      setErrorMessage(
        err?.message || "Login failed. Please check your credentials."
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#e5e7eb",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "2rem",
      }}
    >
      <div
        style={{
          maxWidth: 480,
          width: "100%",
          backgroundColor: "#ffffff",
          borderRadius: 16,
          padding: "2rem 2.5rem",
          boxShadow: "0 20px 40px rgba(15, 23, 42, 0.15)",
        }}
      >
        <h1
          style={{
            fontSize: "1.5rem",
            fontWeight: 700,
            marginBottom: "1.5rem",
            color: "#0f172a",
            textAlign: "center",
          }}
        >
          Sales Manager login
        </h1>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: "1rem" }}>
            <label
              htmlFor="lang"
              style={{
                display: "block",
                fontSize: "0.875rem",
                fontWeight: 500,
                marginBottom: "0.25rem",
              }}
            >
              Lang
            </label>
            <select
              id="lang"
              value={lang}
              onChange={(e) => onLangChange(e.target.value as Lang)}
              style={{
                width: "100%",
                borderRadius: 8,
                border: "1px solid #cbd5e1",
                padding: "0.5rem 0.75rem",
              }}
            >
              <option value="EN">EN</option>
              <option value="ES">ES</option>
            </select>
          </div>

          <div style={{ marginBottom: "1rem" }}>
            <label
              htmlFor="email"
              style={{
                display: "block",
                fontSize: "0.875rem",
                fontWeight: 500,
                marginBottom: "0.25rem",
              }}
            >
              Email
            </label>
            <input
              id="email"
              type="email"
              autoComplete="username"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={{
                width: "100%",
                borderRadius: 8,
                border: "1px solid #cbd5e1",
                padding: "0.5rem 0.75rem",
              }}
            />
          </div>

          <div style={{ marginBottom: "1rem" }}>
            <label
              htmlFor="password"
              style={{
                display: "block",
                fontSize: "0.875rem",
                fontWeight: 500,
                marginBottom: "0.25rem",
              }}
            >
              Password
            </label>
            <input
              id="password"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{
                width: "100%",
                borderRadius: 8,
                border: "1px solid #cbd5e1",
                padding: "0.5rem 0.75rem",
              }}
            />
          </div>

          {errorMessage && (
            <p
              style={{
                color: "#b91c1c",
                fontSize: "0.875rem",
                marginBottom: "0.75rem",
              }}
            >
              {errorMessage}
            </p>
          )}

          <button
            type="submit"
            disabled={submitting}
            style={{
              width: "100%",
              borderRadius: 8,
              padding: "0.75rem",
              border: "none",
              backgroundColor: submitting ? "#1d4ed8" : "#111827",
              color: "#ffffff",
              fontWeight: 600,
              cursor: submitting ? "default" : "pointer",
              opacity: submitting ? 0.8 : 1,
            }}
          >
            {submitting ? "Signing in..." : "Sign in"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
