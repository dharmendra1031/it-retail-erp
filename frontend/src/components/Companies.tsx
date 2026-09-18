import { FormEvent, useEffect, useMemo, useState } from "react";
import {
  Company,
  CompanyFormValues,
  createCompany,
  deleteCompany,
  getCompanies,
  updateCompany,
} from "../api/companies";

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

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
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

  async function handleDelete(company: Company) {
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
        <div>
          <h1>Company Master</h1>
          <p>Manage company identity, tax and invoice information.</p>
        </div>
      </div>

      {error && <div className="alert">{error}</div>}

      <section className="panel">
        <div className="panel-heading">
          <h2>{editingId ? "Edit Company" : "Add Company"}</h2>
          {editingId && (
            <button className="secondary" type="button" onClick={resetForm}>
              Cancel
            </button>
          )}
        </div>

        <form className="company-form" onSubmit={handleSubmit}>
          <label>
            Company Name (English)
            <input
              value={form.nameEn}
              onChange={(event) => setValue("nameEn", event.target.value)}
              required
            />
          </label>

          <label>
            اسم الشركة
            <input
              dir="rtl"
              value={form.nameAr}
              onChange={(event) => setValue("nameAr", event.target.value)}
            />
          </label>

          <label>
            Address (English)
            <textarea
              value={form.addressEn}
              onChange={(event) => setValue("addressEn", event.target.value)}
            />
          </label>

          <label>
            العنوان
            <textarea
              dir="rtl"
              value={form.addressAr}
              onChange={(event) => setValue("addressAr", event.target.value)}
            />
          </label>

          <label>
            Telephone
            <input
              value={form.telephone}
              onChange={(event) => setValue("telephone", event.target.value)}
            />
          </label>

          <label>
            Mobile
            <input
              value={form.mobile}
              onChange={(event) => setValue("mobile", event.target.value)}
            />
          </label>

          <label>
            Email
            <input
              type="email"
              value={form.email}
              onChange={(event) => setValue("email", event.target.value)}
            />
          </label>

          <label>
            Website
            <input
              type="url"
              value={form.website}
              onChange={(event) => setValue("website", event.target.value)}
            />
          </label>

          <label>
            VAT / Tax Number
            <input
              value={form.taxNumber}
              onChange={(event) => setValue("taxNumber", event.target.value)}
            />
          </label>

          <label>
            Commercial Registration Number
            <input
              value={form.commercialRegistrationNumber}
              onChange={(event) =>
                setValue("commercialRegistrationNumber", event.target.value)
              }
            />
          </label>

          <label className="full-width">
            Company Logo
            <input
              type="file"
              accept=".jpg,.jpeg,.png,.webp"
              onChange={(event) => setValue("logo", event.target.files?.[0] ?? null)}
            />
          </label>

          <label>
            Bank Details
            <textarea
              value={form.bankDetails}
              onChange={(event) => setValue("bankDetails", event.target.value)}
            />
          </label>

          <label>
            Social Media
            <textarea
              value={form.socialMedia}
              onChange={(event) => setValue("socialMedia", event.target.value)}
            />
          </label>

          <label>
            Invoice Header
            <textarea
              value={form.invoiceHeader}
              onChange={(event) => setValue("invoiceHeader", event.target.value)}
            />
          </label>

          <label>
            Invoice Footer
            <textarea
              value={form.invoiceFooter}
              onChange={(event) => setValue("invoiceFooter", event.target.value)}
            />
          </label>

          <label className="full-width">
            Terms & Conditions
            <textarea
              value={form.termsAndConditions}
              onChange={(event) => setValue("termsAndConditions", event.target.value)}
            />
          </label>

          <label className="checkbox full-width">
            <input
              type="checkbox"
              checked={form.isActive}
              onChange={(event) => setValue("isActive", event.target.checked)}
            />
            Active
          </label>

          <div className="form-actions full-width">
            <button type="submit" disabled={saving}>
              {saving ? "Saving..." : editingId ? "Save Changes" : "Save Company"}
            </button>
          </div>
        </form>
      </section>

      <section className="panel">
        <div className="panel-heading">
          <h2>Companies</h2>
          <input
            className="search"
            placeholder="Search companies..."
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
        </div>

        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Company</th>
                <th>Arabic Name</th>
                <th>Mobile</th>
                <th>Tax No.</th>
                <th>Status</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {filteredCompanies.map((company) => (
                <tr key={company.id}>
                  <td>{company.id}</td>
                  <td>{company.nameEn}</td>
                  <td dir="rtl">{company.nameAr}</td>
                  <td>{company.mobile}</td>
                  <td>{company.taxNumber}</td>
                  <td>{company.isActive ? "Active" : "Inactive"}</td>
                  <td className="actions">
                    <button
                      className="secondary"
                      type="button"
                      onClick={() => startEdit(company)}
                    >
                      Edit
                    </button>
                    <button
                      className="danger"
                      type="button"
                      onClick={() => handleDelete(company)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
              {!filteredCompanies.length && (
                <tr>
                  <td colSpan={7} className="empty">
                    No companies found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
