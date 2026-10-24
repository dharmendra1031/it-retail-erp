import { FormEvent, useEffect, useRef, useState } from "react";
import {
  Partner, PartnerDocument, PartnerKind, PartnerValues, deletePartner,
  getPartnerDocuments, getPartners, savePartner, uploadPartnerDocument,
} from "../api/partners";
import { advanceOnEnter } from "../forms/keyboard";
import { languageError, useLanguage } from "../i18n";

const blank: PartnerValues = {
  code: "", nameEn: "", nameAr: "", addressEn: "", addressAr: "",
  mobile: "", telephone: "", contactPerson: "", remarks: "", companyName: "",
  paymentTermsDays: 0, isActive: true, civilId: "",
  customerType: "retail", creditLimit: "0.000",
  taxNumber: "", email: "", openingBalance: "0.000",
};

export function Partners({ kind }: { kind: PartnerKind }) {
  const { t } = useLanguage();
  const [rows, setRows] = useState<Partner[]>([]);
  const [values, setValues] = useState<PartnerValues>({ ...blank });
  const [editingId, setEditingId] = useState<number | null>(null);
  const [documents, setDocuments] = useState<PartnerDocument[]>([]);
  const [file, setFile] = useState<File | null>(null);
  const [query, setQuery] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const codeInput = useRef<HTMLInputElement>(null);
  const isCustomer = kind === "customers";

  useEffect(() => {
    void load();
  }, [kind]);

  async function load() {
    try {
      setRows(await getPartners(kind));
    } catch {
      setError(t("unableLoadPartners"));
    }
  }

  function change<K extends keyof PartnerValues>(key: K, value: PartnerValues[K]) {
    setValues(current => ({ ...current, [key]: value }));
  }

  function clear() {
    setEditingId(null);
    setValues({ ...blank });
    setDocuments([]);
    setFile(null);
    setError("");
    codeInput.current?.focus();
  }

  async function edit(partner: Partner) {
    setEditingId(partner.id);
    setValues({
      ...blank, ...partner,
      creditLimit: partner.creditLimit ?? "0.000",
      openingBalance: partner.openingBalance ?? "0.000",
      customerType: partner.customerType ?? "retail",
    });
    setError("");
    try {
      setDocuments(await getPartnerDocuments(kind, partner.id));
    } catch {
      setError(t("unableLoadDocuments"));
    }
    codeInput.current?.focus();
  }

  async function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaving(true);
    setError("");
    try {
      await savePartner(kind, values, editingId ?? undefined);
      clear();
      await load();
    } catch (caught) {
      setError(caught instanceof Error ? languageError(caught.message, t) : t("unableSavePartner"));
      codeInput.current?.focus();
    } finally {
      setSaving(false);
    }
  }

  async function remove(partner: Partner) {
    if (!window.confirm(`${t("delete")} ${partner.nameEn}?`)) return;
    try {
      await deletePartner(kind, partner.id);
      await load();
    } catch (caught) {
      setError(caught instanceof Error ? languageError(caught.message, t) : t("unableDeletePartner"));
    }
  }

  async function upload() {
    if (editingId === null || file === null) return;
    setSaving(true);
    setError("");
    try {
      await uploadPartnerDocument(kind, editingId, file);
      setDocuments(await getPartnerDocuments(kind, editingId));
      setFile(null);
    } catch (caught) {
      setError(caught instanceof Error ? languageError(caught.message, t) : t("invalidDocument"));
    } finally {
      setSaving(false);
    }
  }

  const visibleRows = rows.filter(row =>
    (row.code + row.nameEn + row.nameAr).toLowerCase().includes(query.trim().toLowerCase()),
  );

  return (
    <main className="content">
      <div className="page-heading">
        <h1>{t(isCustomer ? "customerMaster" : "supplierMaster")}</h1>
      </div>
      {error && <div className="alert" role="alert">{error}</div>}
      <section className="panel">
        <div className="panel-heading">
          <h2>{t(editingId === null ? "addPartner" : "editPartner")}</h2>
          {editingId !== null &&
            <button type="button" className="secondary" onClick={clear}>{t("cancel")}</button>}
        </div>
        <form className="company-form" onSubmit={save} onKeyDown={advanceOnEnter}>
          <label>{t("code")}
            <input ref={codeInput} dir="ltr" required maxLength={30} value={values.code}
              onChange={event => change("code", event.target.value)} />
          </label>
          <label>{t(isCustomer ? "customerNameEnglish" : "supplierNameEnglish")}
            <input required maxLength={200} value={values.nameEn}
              onChange={event => change("nameEn", event.target.value)} />
          </label>
          <label>{t(isCustomer ? "customerNameArabic" : "supplierNameArabic")}
            <input dir="rtl" required={isCustomer} maxLength={200} value={values.nameAr}
              onChange={event => change("nameAr", event.target.value)} />
          </label>
          <label>{t("addressEnglish")}
            <textarea maxLength={500} value={values.addressEn}
              onChange={event => change("addressEn", event.target.value)} />
          </label>
          <label>{t("addressArabic")}
            <textarea dir="rtl" maxLength={500} value={values.addressAr}
              onChange={event => change("addressAr", event.target.value)} />
          </label>
          <label>{t("mobile")}
            <input required={isCustomer} maxLength={30} value={values.mobile}
              onChange={event => change("mobile", event.target.value)} />
          </label>
          <label>{t("telephone")}
            <input maxLength={30} value={values.telephone}
              onChange={event => change("telephone", event.target.value)} />
          </label>
          <label>{t("contactPerson")}
            <input maxLength={150} value={values.contactPerson}
              onChange={event => change("contactPerson", event.target.value)} />
          </label>
          {isCustomer ? (
            <>
              <label>{t("companyName")}
                <input maxLength={200} value={values.companyName}
                  onChange={event => change("companyName", event.target.value)} />
              </label>
              <label>{t("customerType")}
                <select value={values.customerType} onChange={event => change("customerType", event.target.value)}>
                  <option value="retail">{t("retail")}</option>
                  <option value="wholesale">{t("wholesale")}</option>
                  <option value="corporate">{t("corporate")}</option>
                  <option value="cash">{t("cash")}</option>
                  <option value="credit">{t("credit")}</option>
                  <option value="individual">{t("individual")}</option>
                  <option value="company">{t("company")}</option>
                  <option value="government">{t("government")}</option>
                  <option value="other">{t("other")}</option>
                </select>
              </label>
              <label>{t("civilId")}
                <input maxLength={30} value={values.civilId}
                  onChange={event => change("civilId", event.target.value)} />
              </label>

              <label>{t("email")}
                <input type="email" dir="ltr" maxLength={200} value={values.email}
                  onChange={event => change("email", event.target.value)} />
              </label>
              <label>{t("taxNumber")}
                <input dir="ltr" maxLength={100} value={values.taxNumber}
                  onChange={event => change("taxNumber", event.target.value)} />
              </label>
              <label>{t("openingBalance")}
                <input required dir="ltr" inputMode="decimal" value={values.openingBalance}
                  pattern="[0-9]+(\.[0-9]{1,3})?"
                  onChange={event => change("openingBalance", event.target.value)} />
              </label>
              <label>{t("creditLimit")}
                <input required dir="ltr" inputMode="decimal" value={values.creditLimit}
                  pattern="[0-9]+(\.[0-9]{1,3})?"
                  onChange={event => change("creditLimit", event.target.value)} />
              </label>
            </>
          ) : (
            <>
              <label>{t("email")}
                <input type="email" dir="ltr" maxLength={200} value={values.email}
                  onChange={event => change("email", event.target.value)} />
              </label>
              <label>{t("taxNumber")}
                <input dir="ltr" maxLength={100} value={values.taxNumber}
                  onChange={event => change("taxNumber", event.target.value)} />
              </label>
              <label>{t("openingBalance")}
                <input required dir="ltr" inputMode="decimal" value={values.openingBalance}
                  pattern="[0-9]+(\.[0-9]{1,3})?"
                  onChange={event => change("openingBalance", event.target.value)} />
              </label>
              <label>{t("creditLimit")}
                <input required dir="ltr" inputMode="decimal" value={values.creditLimit}
                  pattern="[0-9]+(\.[0-9]{1,3})?"
                  onChange={event => change("creditLimit", event.target.value)} />
              </label>
            </>
          )}
          <label>{t("remarks")}
            <textarea maxLength={1000} value={values.remarks}
              onChange={event => change("remarks", event.target.value)} />
          </label>
          <label>{t("paymentTermsDays")}
            <input type="number" min={0} max={365} step={1} required
              value={values.paymentTermsDays}
              onChange={event => change("paymentTermsDays", Number(event.target.value))} />
          </label>
          <label className="checkbox full-width">
            <input type="checkbox" checked={values.isActive}
              onChange={event => change("isActive", event.target.checked)} />
            {t("active")}
          </label>
          <div className="form-actions full-width">
            <button type="submit" disabled={saving}>{saving ? t("saving") : t("savePartner")}</button>
          </div>
        </form>
        {editingId !== null && (
          <section className="panel">
            <h3>{t("securedDocuments")}</h3>
            <label>{t("uploadDocument")}
              <input type="file" accept=".pdf,.png,.jpg,.jpeg" onChange={event =>
                setFile(event.target.files?.[0] ?? null)} />
            </label>
            <button type="button" onClick={() => void upload()} disabled={saving || !file}>
              {t("uploadDocument")}
            </button>
            <ul>
              {documents.map(doc => (
                <li key={doc.id}>
                  <a href={`/api/${kind}/${editingId}/documents/${doc.id}`}>
                    {doc.fileName}
                  </a>
                </li>
              ))}
            </ul>
          </section>
        )}
      </section>
      <section className="panel">
        <div className="panel-heading">
          <h2>{t(isCustomer ? "customers" : "suppliers")} ({rows.length})</h2>
          <input className="search" placeholder={t("searchCompanies")}
            value={query} onChange={event => setQuery(event.target.value)} />
        </div>
        <div className="table-wrap">
          <table>
            <thead><tr>
              <th>ID</th><th>{t("code")}</th><th>{t("companyNameEnglish")}</th>
              <th>{t("companyNameArabic")}</th><th>{t("status")}</th><th>{t("actions")}</th>
            </tr></thead>
            <tbody>
              {visibleRows.map(row => (
                <tr key={row.id}>
                  <td>{row.id}</td><td>{row.code}</td><td>{row.nameEn}</td>
                  <td dir="rtl">{row.nameAr}</td>
                  <td>{t(row.isActive ? "active" : "inactive")}</td>
                  <td className="actions">
                    <button type="button" className="secondary" onClick={() => void edit(row)}>{t("edit")}</button>
                    <button type="button" className="danger" onClick={() => void remove(row)}>{t("delete")}</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
