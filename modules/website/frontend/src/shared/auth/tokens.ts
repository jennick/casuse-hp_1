const ADMIN_TOKEN_KEY = "website_admin_token";

export function getWebsiteAdminToken(): string | null {
  return localStorage.getItem(ADMIN_TOKEN_KEY);
}

export function setWebsiteAdminToken(token: string): void {
  localStorage.setItem(ADMIN_TOKEN_KEY, token);
}

export function clearWebsiteAdminToken(): void {
  localStorage.removeItem(ADMIN_TOKEN_KEY);
}
