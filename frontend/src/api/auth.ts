import { apiRequest, jsonBody } from "./client";

export interface CurrentUser {
  id: number;
  name: string;
  email: string;
}

export async function getCurrentUser() {
  return apiRequest<CurrentUser>("/api/auth/me");
}

export async function login(email: string, password: string, rememberMe: boolean) {
  return apiRequest<CurrentUser>(
    "/api/auth/login",
    {
      method: "POST",
      ...jsonBody({ email, password, rememberMe }),
    },
    true,
  );
}

export async function logout() {
  return apiRequest<void>("/api/auth/logout", { method: "POST" }, true);
}
