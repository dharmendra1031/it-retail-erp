import { apiRequest, jsonBody } from "./client";

export interface Role {
  id: number;
  name: string;
}

export function getRoles() {
  return apiRequest<Role[]>("/api/roles");
}

export function createRole(name: string) {
  return apiRequest<Role>("/api/roles", {
    method: "POST",
    ...jsonBody({ name }),
  }, true);
}

export function updateRole(id: number, name: string) {
  return apiRequest<Role>(`/api/roles/${id}`, {
    method: "PUT",
    ...jsonBody({ name }),
  }, true);
}

export function deleteRole(id: number) {
  return apiRequest<void>(`/api/roles/${id}`, { method: "DELETE" }, true);
}

export interface Permission {
  code: string;
  name: string;
}

export function getPermissionCatalog() {
  return apiRequest<Permission[]>("/api/permissions");
}

export function getRolePermissions(id: number) {
  return apiRequest<{ permissions: string[] }>(`/api/roles/${id}/permissions`);
}

export function saveRolePermissions(id: number, permissions: string[]) {
  return apiRequest<{ permissions: string[] }>(`/api/roles/${id}/permissions`, {
    method: "PUT",
    ...jsonBody({ permissions }),
  }, true);
}
