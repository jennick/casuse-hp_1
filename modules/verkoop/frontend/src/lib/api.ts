// modules/verkoop/frontend/src/lib/api.ts
// Centrale API helper voor de verkoop-frontend.
// - Regelt basis-URL (voegt automatisch /api/v1 toe indien nodig)
// - Beheert auth-token in localStorage
// - Biedt get/post/put/patch/delete helpers
// - Gooit duidelijke fouten met HTTP-status + backend detail

const STORAGE_KEY = "verkoop_admin_token";

// Token helpers --------------------------------------------------------------

export function loadAuthToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(STORAGE_KEY);
}

export function setAuthToken(token: string | null): void {
  if (typeof window === "undefined") return;
  if (token) {
    window.localStorage.setItem(STORAGE_KEY, token);
  } else {
    window.localStorage.removeItem(STORAGE_KEY);
  }
}

// Request options ------------------------------------------------------------

export type RequestOptions = {
  method: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  body?: unknown;
  signal?: AbortSignal;
  /** Als auth = false -> géén Bearer token meesturen. Default: true. */
  auth?: boolean;
};

// Basis-URL robuust opbouwen -------------------------------------------------
//
// Scenario's die we willen afdekken:
// 1) VITE_API_BASE_URL = "http://localhost:20030"
//      -> we maken er "http://localhost:20030/api/v1" van
// 2) VITE_API_BASE_URL = "http://localhost:20030/api/v1"
//      -> we laten dit zo (geen dubbele /api/v1)
// 3) Geen env var gezet
//      -> fallback naar "http://localhost:20030/api/v1"

const rawBase =
  (typeof import.meta !== "undefined" &&
    (import.meta as any).env?.VITE_API_BASE_URL) ||
  "http://localhost:20030";

function normalizeApiBase(base: string): string {
  let trimmed = base.trim().replace(/\/+$/, ""); // trailing / weg

  if (!/\/api\/v\d+$/i.test(trimmed)) {
    // bevat nog geen /api/v1, /api/v2, ...
    trimmed = `${trimmed}/api/v1`;
  }

  return trimmed;
}

const API_BASE = normalizeApiBase(rawBase);

// Low-level request helper ---------------------------------------------------

export async function request<T>(
  path: string,
  opts: RequestOptions
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  const token = loadAuthToken();

  if (opts.auth !== false && token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  // path robuust samenstellen
  const normalizedPath = path.startsWith("http")
    ? path
    : `${API_BASE}${path.startsWith("/") ? "" : "/"}${path}`;

  const response = await fetch(normalizedPath, {
    method: opts.method,
    headers,
    body: opts.body ? JSON.stringify(opts.body) : undefined,
    signal: opts.signal,
  });

  if (!response.ok) {
    let detail: string | undefined;

    try {
      const data = await response.json();
      // FastAPI gebruikt vaak "detail"
      detail = (data as any)?.detail ?? JSON.stringify(data);
    } catch {
      try {
        detail = await response.text();
      } catch {
        detail = undefined;
      }
    }

    // Geef expliciet de URL in de error message mee → helpt debuggen
    throw new Error(
      `API request failed (${response.status} ${
        response.statusText
      }) [${normalizedPath}]${detail ? `: ${detail}` : ""}`
    );
  }

  if (response.status === 204) {
    // No content
    return undefined as T;
  }

  return (await response.json()) as T;
}

// Convenience wrapper met HTTP-method helpers --------------------------------

const api = {
  get<T>(
    path: string,
    opts: Omit<RequestOptions, "method" | "body"> = {}
  ): Promise<T> {
    return request<T>(path, { ...opts, method: "GET" });
  },

  post<T>(
    path: string,
    body?: unknown,
    opts: Omit<RequestOptions, "method" | "body"> = {}
  ): Promise<T> {
    return request<T>(path, { ...opts, method: "POST", body });
  },

  put<T>(
    path: string,
    body?: unknown,
    opts: Omit<RequestOptions, "method" | "body"> = {}
  ): Promise<T> {
    return request<T>(path, { ...opts, method: "PUT", body });
  },

  patch<T>(
    path: string,
    body?: unknown,
    opts: Omit<RequestOptions, "method" | "body"> = {}
  ): Promise<T> {
    return request<T>(path, { ...opts, method: "PATCH", body });
  },

  delete<T>(
    path: string,
    opts: Omit<RequestOptions, "method" | "body"> = {}
  ): Promise<T> {
    return request<T>(path, { ...opts, method: "DELETE" });
  },
};

export default api;
export { api };
