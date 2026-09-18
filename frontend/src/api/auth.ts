import { apiRequest, jsonBody, refreshCsrfToken } from "./client";

export interface CurrentUser {
  id: number;
  name: string;
  email: string;
}

export async function getCurrentUser() {
  return apiRequest<CurrentUser>("/api/auth/me");
}

export async function login(email: string, password: string, rememberMe: boolean) {
  const user = await apiRequest<CurrentUser>(
    "/api/auth/login",
    {
      method: "POST",
      ...jsonBody({ email, password, rememberMe }),
    },
    true,
  );

  await refreshCsrfToken();
  return user;
}

export async function logout() {
  return apiRequest<void>("/api/auth/logout", { method: "POST" }, true);
}
