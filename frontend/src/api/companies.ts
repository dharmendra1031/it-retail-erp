import { apiRequest } from "./client";

export interface Company {
  id: number;
  nameEn: string;
  nameAr: string;
  addressEn: string;
  addressAr: string;
  telephone: string;
  mobile: string;
  email: string;
  website: string;
  taxNumber: string;
  commercialRegistrationNumber: string;
  logoUrl: string;
  bankDetails: string;
  invoiceHeader: string;
  invoiceFooter: string;
  termsAndConditions: string;
  socialMedia: string;
  isActive: boolean;
}

export type CompanyFormValues = Omit<Company, "id" | "logoUrl"> & {
  logo?: File | null;
};

function toFormData(values: CompanyFormValues) {
  const data = new FormData();

  Object.entries(values).forEach(([key, value]) => {
    if (key === "logo") {
      if (value instanceof File) {
        data.append("logo", value);
      }
      return;
    }

    data.append(key, String(value ?? ""));
  });

  return data;
}

export function getCompanies() {
  return apiRequest<Company[]>("/api/companies");
}

export function createCompany(values: CompanyFormValues) {
  return apiRequest<Company>(
    "/api/companies",
    { method: "POST", body: toFormData(values) },
    true,
  );
}

export function updateCompany(id: number, values: CompanyFormValues) {
  return apiRequest<Company>(
    `/api/companies/${id}`,
    { method: "PUT", body: toFormData(values) },
    true,
  );
}

export function deleteCompany(id: number) {
  return apiRequest<void>(`/api/companies/${id}`, { method: "DELETE" }, true);
}
