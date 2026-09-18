let csrfToken = "";

async function getCsrfToken() {
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
    await getCsrfToken();
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
    throw new Error("UNAUTHORIZED");
  }

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Request failed.");
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
