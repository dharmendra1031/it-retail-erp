let csrfToken = "";
let onUnauthorized: (() => void) | undefined;

export function setUnauthorizedHandler(handler?: () => void) {
  onUnauthorized = handler;
}

export async function refreshCsrfToken() {
  const response = await fetch("/api/auth/csrf", { credentials: "same-origin" });

  if (!response.ok) {
    throw new Error("Unable to initialize security token.");
  }

  const data = (await response.json()) as { csrfToken: string };
  csrfToken = data.csrfToken;
}

export async function apiRequest<T>(
  path: string,
  options: RequestInit = {},
  requiresCsrf = false,
): Promise<T> {
  if (requiresCsrf && !csrfToken) {
    await refreshCsrfToken();
  }

  const headers = new Headers(options.headers);

  if (requiresCsrf) {
    headers.set("X-CSRF-TOKEN", csrfToken);
  }

  const response = await fetch(path, {
    ...options,
    headers,
    credentials: "same-origin",
  });

  if (response.status === 401) {
    csrfToken = "";
    if (path !== "/api/auth/me" && path !== "/api/auth/login") {
      window.dispatchEvent(new Event("erp:session-expired"));
    }
    throw new Error("UNAUTHORIZED");
  }

  if (!response.ok) {
    const contentType = response.headers.get("content-type") ?? "";
    if (contentType.includes("application/json")) {
      const data = (await response.json()) as { detail?: string };
      throw new Error(data.detail || "Request failed.");
    }

    throw new Error("Request failed.");
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export function jsonBody(value: unknown) {
  return {
    body: JSON.stringify(value),
    headers: { "Content-Type": "application/json" },
  };
}
