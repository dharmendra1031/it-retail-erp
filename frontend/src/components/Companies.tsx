import { useEffect, useMemo, useState } from "react";
import {
  Company,
  CompanyFormValues,
  createCompany,
  deleteCompany,
  getCompanies,
  updateCompany,
} from "../api/companies";
import { CompanyForm } from "./CompanyForm";
import { CompanyTable } from "./CompanyTable";

const emptyForm: CompanyFormValues = {
  nameEn: "",
  nameAr: "",
  addressEn: "",
  addressAr: "",
  telephone: "",
  mobile: "",
  email: "",
  website: "",
  taxNumber: "",
  commercialRegistrationNumber: "",
  bankDetails: "",
  invoiceHeader: "",
  invoiceFooter: "",
  termsAndConditions: "",
  socialMedia: "",
  isActive: true,
  logo: null,
};

export function Companies() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [form, setForm] = useState<CompanyFormValues>(emptyForm);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadCompanies();
  }, []);

  const filteredCompanies = useMemo(() => {
    const term = query.trim().toLowerCase();
    if (!term) {
      return companies;
    }

    return companies.filter((company) =>
      [company.nameEn, company.nameAr, company.mobile, company.taxNumber]
        .join(" ")
        .toLowerCase()
        .includes(term),
    );
  }, [companies, query]);

  async function loadCompanies() {
    try {
      setCompanies(await getCompanies());
    } catch {
      setError("Unable to load companies.");
    }
  }

  function startEdit(company: Company) {
    setEditingId(company.id);
    setForm({
      nameEn: company.nameEn,
      nameAr: company.nameAr,
      addressEn: company.addressEn,
      addressAr: company.addressAr,
      telephone: company.telephone,
      mobile: company.mobile,
      email: company.email,
      website: company.website,
      taxNumber: company.taxNumber,
      commercialRegistrationNumber: company.commercialRegistrationNumber,
      bankDetails: company.bankDetails,
      invoiceHeader: company.invoiceHeader,
      invoiceFooter: company.invoiceFooter,
      termsAndConditions: company.termsAndConditions,
      socialMedia: company.socialMedia,
      isActive: company.isActive,
      logo: null,
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function resetForm() {
    setEditingId(null);
    setForm(emptyForm);
    setError("");
  }

  async function saveCompany() {
    setSaving(true);
    setError("");

    try {
      if (editingId) {
        await updateCompany(editingId, form);
      } else {
        await createCompany(form);
      }

      resetForm();
      await loadCompanies();
    } catch {
      setError("Unable to save company.");
    } finally {
      setSaving(false);
    }
  }

  async function removeCompany(company: Company) {
    if (!window.confirm(`Delete ${company.nameEn}?`)) {
      return;
    }

    try {
      await deleteCompany(company.id);
      await loadCompanies();
    } catch {
      setError("Unable to delete company.");
    }
  }

  function setValue<K extends keyof CompanyFormValues>(
    key: K,
    value: CompanyFormValues[K],
  ) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  return (
    <main className="content">
      <div className="page-heading">
        <h1>Company Master</h1>
        <p>Manage company identity, tax and invoice information.</p>
      </div>

      {error && <div className="alert">{error}</div>}

      <CompanyForm
        values={form}
        editing={editingId !== null}
        saving={saving}
        onChange={setValue}
        onSubmit={saveCompany}
        onCancel={resetForm}
      />

      <CompanyTable
        companies={filteredCompanies}
        query={query}
        onQueryChange={setQuery}
        onEdit={startEdit}
        onDelete={removeCompany}
      />
    </main>
  );
}
