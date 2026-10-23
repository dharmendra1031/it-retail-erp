import { apiRequest, jsonBody } from "./client";

export type PartnerKind = "customers" | "suppliers";

export interface Partner {
  id: number;
  code: string;
  nameEn: string;
  nameAr: string;
  addressEn: string;
  addressAr: string;
  mobile: string;
  contactPerson: string;
  telephone: string;
  remarks: string;
  paymentTermsDays: number;
  isActive: boolean;
  companyName?: string;
  civilId?: string;
  customerType?: string;
  creditLimit?: string;
  taxNumber?: string;
  email?: string;
  openingBalance?: string;
}

export interface PartnerDocument {
  id: number;
  fileName: string;
  contentType: string;
  size: number;
}

export interface PartnerValues {
  code: string;
  nameEn: string;
  nameAr: string;
  addressEn: string;
  addressAr: string;
  mobile: string;
  paymentTermsDays: number;
  isActive: boolean;
  companyName: string;
  civilId: string;
  customerType: string;
  creditLimit: string;
  taxNumber: string;
  email: string;
  openingBalance: string;
}

export function getPartners(kind: PartnerKind) {
  return apiRequest<Partner[]>(`/api/${kind}`);
}

export function savePartner(kind: PartnerKind, values: PartnerValues, id?: number) {
  const common = {
    code: values.code,
    nameEn: values.nameEn,
    nameAr: values.nameAr,
    addressEn: values.addressEn,
    addressAr: values.addressAr,
    mobile: values.mobile,
    contactPerson: values.contactPerson,
    telephone: values.telephone,
    remarks: values.remarks,
    paymentTermsDays: values.paymentTermsDays,
    isActive: values.isActive,
  };
  const details = kind === "customers"
    ? { companyName: values.companyName, civilId: values.civilId, customerType: values.customerType,
        creditLimit: values.creditLimit, email: values.email, taxNumber: values.taxNumber,
        openingBalance: values.openingBalance }
    : { taxNumber: values.taxNumber, email: values.email, openingBalance: values.openingBalance,
        creditLimit: values.creditLimit };

  return apiRequest<Partner>(`/api/${kind}${id ? `/${id}` : ""}`, {
    method: id ? "PUT" : "POST",
    ...jsonBody({ ...common, ...details }),
  }, true);
}

export function deletePartner(kind: PartnerKind, id: number) {
  return apiRequest<void>(`/api/${kind}/${id}`, { method: "DELETE" }, true);
}

export function getPartnerDocuments(kind: PartnerKind, id: number) {
  return apiRequest<PartnerDocument[]>(`/api/${kind}/${id}/documents`);
}

export function uploadPartnerDocument(kind: PartnerKind, id: number, file: File) {
  const form = new FormData();
  form.append("file", file);
  return apiRequest<PartnerDocument>(`/api/${kind}/${id}/documents`, {
    method: "POST", body: form,
  }, true);
}
