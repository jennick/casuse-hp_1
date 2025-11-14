// modules/verkoop/frontend/src/lib/auth.ts
// Centrale helper voor authenticatie in de verkoop-frontend.
// - Beheert access token in localStorage
// - Houdt "laatste activiteit" bij
// - Biedt idle-timeout (bijv. 30 min)

const ACCESS_TOKEN_KEY = "verkoop_admin_access_token";
const LAST_ACTIVE_KEY = "verkoop_admin_last_active";

/** Lees het huidige access token (of null als niet aanwezig). */
export function loadAuthToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(ACCESS_TOKEN_KEY);
}

/** Sla een nieuw access token op en reset de last-active timestamp. */
export function saveAuthToken(token: string): void {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(ACCESS_TOKEN_KEY, token);
  window.localStorage.setItem(LAST_ACTIVE_KEY, Date.now().toString());
}

/** Verwijder token + last-active; effectief uitloggen. */
export function clearSession(): void {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem(ACCESS_TOKEN_KEY);
  window.localStorage.removeItem(LAST_ACTIVE_KEY);
}

/** Registreer activiteit (muisklik, keypress, …). */
export function touchActivity(): void {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(LAST_ACTIVE_KEY, Date.now().toString());
}

/** Lees laatste activiteitstijd (ms sinds epoch) of null. */
export function getLastActive(): number | null {
  if (typeof window === "undefined") return null;
  const raw = window.localStorage.getItem(LAST_ACTIVE_KEY);
  if (!raw) return null;
  const parsed = Number(raw);
  return Number.isFinite(parsed) ? parsed : null;
}

/**
 * Start een idle-timer. Als de gebruiker langer dan `timeoutMs`
 * geen activiteit heeft, wordt `onTimeout()` aangeroepen.
 * Returnt een cleanup-functie om listeners/timer op te ruimen.
 */
export function setupIdleTimer(
  onTimeout: () => void,
  timeoutMs: number = 30 * 60 * 1000 // default 30 min
): () => void {
  if (typeof window === "undefined") {
    // SSR / tests: niks doen
    return () => {};
  }

  const events: Array<keyof WindowEventMap> = [
    "mousemove",
    "keydown",
    "click",
    "scroll",
    "visibilitychange",
  ];

  let timerId: number | null = null;

  const resetTimer = () => {
    if (document.hidden) {
      // Als tab verborgen is, laten we de timer lopen
      return;
    }

    touchActivity();

    if (timerId !== null) {
      window.clearTimeout(timerId);
    }

    timerId = window.setTimeout(() => {
      const lastActive = getLastActive();
      const now = Date.now();

      if (!lastActive || now - lastActive >= timeoutMs) {
        onTimeout();
      } else {
        // Veiligheidsnet: als er net activiteit was, opnieuw planning
        resetTimer();
      }
    }, timeoutMs);
  };

  events.forEach((ev) => window.addEventListener(ev, resetTimer));
  // Initial start
  resetTimer();

  return () => {
    if (timerId !== null) {
      window.clearTimeout(timerId);
    }
    events.forEach((ev) => window.removeEventListener(ev, resetTimer));
  };
}

/** Huidige loginstatus puur op basis van token. */
export function isAuthenticated(): boolean {
  return !!loadAuthToken();
}
