import { apiRequest, jsonBody } from "./client";

export interface ProductLicense {
  id: number;
  productId: number;
  licenseNumber: string;
  hasKey: boolean;
  activationDate: string | null;
  expiryDate: string | null;
  isActive: boolean;
}

export interface ProductLicenseValues {
  productId: number;
  licenseNumber: string;
  licenseKey: string;
  activationDate: string | null;
  expiryDate: string | null;
}

export function getProductLicenses(productId: number) {
  return apiRequest<ProductLicense[]>(
    `/api/product-licenses?productId=${encodeURIComponent(productId)}`
  );
}

export function saveProductLicense(values: ProductLicenseValues) {
  return apiRequest<ProductLicense>("/api/product-licenses", {
    method: "POST", ...jsonBody(values),
  }, true);
}

export function revokeProductLicense(id: number) {
  return apiRequest<ProductLicense>(`/api/product-licenses/${id}`, {
    method: "DELETE",
  }, true);
}
