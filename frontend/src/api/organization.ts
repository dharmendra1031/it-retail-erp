import { apiRequest, jsonBody } from "./client";

export interface Branch {
  id: number;
  companyId: number;
  code: string;
  nameEn: string;
  nameAr: string;
  isActive: boolean;
}

export interface Warehouse {
  id: number;
  branchId: number;
  code: string;
  nameEn: string;
  nameAr: string;
  isActive: boolean;
}

export type BranchValues = Omit<Branch, "id">;
export type WarehouseValues = Omit<Warehouse, "id">;

export function getBranches() {
  return apiRequest<Branch[]>("/api/branches");
}

export function getWarehouses() {
  return apiRequest<Warehouse[]>("/api/warehouses");
}

export function saveBranch(values: BranchValues, id?: number) {
  return apiRequest<Branch>(id ? `/api/branches/${id}` : "/api/branches", {
    method: id ? "PUT" : "POST", ...jsonBody(values),
  }, true);
}

export function saveWarehouse(values: WarehouseValues, id?: number) {
  return apiRequest<Warehouse>(id ? `/api/warehouses/${id}` : "/api/warehouses", {
    method: id ? "PUT" : "POST", ...jsonBody(values),
  }, true);
}

export function deleteBranch(id: number) {
  return apiRequest<void>(`/api/branches/${id}`, { method: "DELETE" }, true);
}

export function deleteWarehouse(id: number) {
  return apiRequest<void>(`/api/warehouses/${id}`, { method: "DELETE" }, true);
}
