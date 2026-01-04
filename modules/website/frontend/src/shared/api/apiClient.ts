const API_BASE_URL =
  import.meta.env.VITE_WEBSITE_API_BASE_URL ?? "";

type ApiFetchOptions = RequestInit & {
  skipAuth?: boolean;
  json?: unknown;
};

function getAdminToken(): string | null {
  return localStorage.getItem("website_admin_token");
}

export async function apiFetch<T = any>(
  path: string,
  options: ApiFetchOptions = {}
): Promise<T> {
  const { skipAuth, headers, body, json, ...rest } = options;

  const token = getAdminToken();

  const finalBody =
    json !== undefined
      ? JSON.stringify(json)
      : body !== undefined
      ? typeof body === "string"
        ? body
        : JSON.stringify(body)
      : undefined;

  const finalHeaders: HeadersInit = {
    ...(finalBody ? { "Content-Type": "application/json" } : {}),
    ...(token && !skipAuth
      ? { Authorization: `Bearer ${token}` }
      : {}),
    ...headers,
  };

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...rest,
    headers: finalHeaders,
    body: finalBody,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`API ${response.status}: ${text}`);
  }

  if (response.status === 204) {
    return null as T;
  }

  return (await response.json()) as T;
}
