import { apiRequest, jsonBody } from "./client";

export interface ProductValues {
  sku: string;
  barcode: string | null;
  nameEn: string;
  nameAr: string;
  descriptionEn: string;
  descriptionAr: string;
  categoryId: number;
  brandId: number | null;
  unitId: number;
  productType: "stock" | "nonstock" | "digital";
  serialTracked: boolean;
  costPrice: string;
  basePrice: string;
  minPrice: string;
  reorderLevel: string;
  isActive: boolean;
}

export interface Product extends ProductValues {
  id: number;
}

interface ProductPage {
  items: Product[];
  total: number;
  page: number;
  pageSize: number;
}

export async function getProducts(search: string, page: number): Promise<ProductPage> {
  const query = new URLSearchParams({ page: String(page), pageSize: "25" });
  if (search.trim()) query.set("search", search.trim());
  const result = await apiRequest<ProductPage>("/api/products?" + query);
  if (!result.items.every(item => Number.isSafeInteger(item.id) && item.id > 0)) {
    throw new Error("Invalid or unsafe numeric ID.");
  }
  return result;
}

export function saveProduct(values: ProductValues, id?: number) {
  const path = "/api/products" + (id ? "/" + id : "");
  return apiRequest<Product>(path, {
    method: id ? "PUT" : "POST",
    ...jsonBody(values),
  }, true);
}

export function deleteProduct(id: number) {
  return apiRequest<void>("/api/products/" + id, { method: "DELETE" }, true);
}
