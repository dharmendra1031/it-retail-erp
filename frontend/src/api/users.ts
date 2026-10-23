import { apiRequest, jsonBody } from "./client";

export interface ErpUser {
  id: number;
  username: string;
  fullName: string;
  email: string;
  mobile: string;
  isActive: boolean;
  roleIds: number[];
  branchId: number | null;
}

export interface UserValues {
  username: string;
  fullName: string;
  email: string;
  mobile: string;
  isActive: boolean;
  roleIds: number[];
  password?: string;
}

export function getUsers() {
  return apiRequest<ErpUser[]>("/api/users");
}

export function saveUser(values: UserValues, id?: number) {
  return apiRequest<ErpUser>(id ? `/api/users/${id}` : "/api/users", {
    method: id ? "PUT" : "POST",
    ...jsonBody(values),
  }, true);
}

export function resetUserPassword(id: number, password: string) {
  return apiRequest<void>(`/api/users/${id}/password`, {
    method: "PUT", ...jsonBody({ password }),
  }, true);
}
