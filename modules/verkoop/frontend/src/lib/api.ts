export interface ApiError extends Error {
  status?: number;
  details?: unknown;
}

const rawBase =
  (typeof import.meta !== "undefined" &&
    (import.meta as any).env?.VITE_API_BASE_URL) ||
  "http://localhost:20030";

function normalizeApiBase(base: string): string {
  const trimmed = base.replace(/\/+$/, "");
  if (/\/api\/v\d+$/i.test(trimmed)) {
    return trimmed;
  }
  return trimmed + "/api/v1";
}

const API_BASE = normalizeApiBase(rawBase);

async function request<T>(method: string, path: string, body?: any): Promise<T> {
  const url = path.startsWith("http")
    ? path
    : API_BASE + (path.startsWith("/") ? path : "/" + path);

  const init: RequestInit = {
    method,
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
  };

  if (body !== undefined) {
    (init.headers as Record<string, string>)["Content-Type"] =
      "application/json";
    init.body = JSON.stringify(body);
  }

  const res = await fetch(url, init);
  if (!res.ok) {
    const err: ApiError = new Error(
      `API error ${res.status} on ${method} ${url}`
    );
    err.status = res.status;
    try {
      err.details = await res.json();
    } catch {
      err.details = await res.text();
    }
    throw err;
  }
  if (res.status === 204) {
    return undefined as T;
  }
  return (await res.json()) as T;
}

export const api = {
  get: <T>(path: string) => request<T>("GET", path),
  post: <T>(path: string, body?: any) => request<T>("POST", path, body),
  patch: <T>(path: string, body?: any) => request<T>("PATCH", path, body),
  delete: <T>(path: string) => request<T>("DELETE", path),
};
