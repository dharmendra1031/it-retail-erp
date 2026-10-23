import { apiRequest, jsonBody } from "./client";

export type CatalogKind = "categories" | "brands" | "units";

export interface CatalogItem {
  id: number;
  code: string;
  nameEn: string;
  nameAr: string;
  isActive: boolean;
  parentId?: number | null;
  decimalPlaces?: number;
}

export interface CatalogValues {
  code: string;
  nameEn: string;
  nameAr: string;
  isActive: boolean;
  parentId: number | null;
  decimalPlaces: number;
}

export function getCatalog(kind: CatalogKind) {
  return apiRequest<CatalogItem[]>(`/api/${kind}`);
}

export function saveCatalog(kind: CatalogKind, values: CatalogValues, id?: number) {
  const base = { code: values.code, nameEn: values.nameEn, nameAr: values.nameAr, isActive: values.isActive };
  const extra = kind === "categories" ? { parentId: values.parentId } :
    kind === "units" ? { decimalPlaces: values.decimalPlaces } : {};

  return apiRequest<CatalogItem>(`/api/${kind}${id ? `/${id}` : ""}`, {
    method: id ? "PUT" : "POST", ...jsonBody({ ...base, ...extra }),
  }, true);
}

export function deleteCatalog(kind: CatalogKind, id: number) {
  return apiRequest<void>(`/api/${kind}/${id}`, { method: "DELETE" }, true);
}
