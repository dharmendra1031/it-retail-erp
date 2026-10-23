import { FormEvent, useEffect, useRef, useState } from "react";
import {
  CatalogItem, CatalogKind, CatalogValues, deleteCatalog, getCatalog, saveCatalog,
} from "../api/catalog";
import { advanceOnEnter } from "../forms/keyboard";
import { languageError, useLanguage } from "../i18n";

const empty: CatalogValues = {
  code: "", nameEn: "", nameAr: "", isActive: true,
  parentId: null, decimalPlaces: 0,
};

const titles = {
  categories: "categoryMaster",
  brands: "brandMaster",
  units: "unitMaster",
} as const;

export function Catalog({ kind }: { kind: CatalogKind }) {
  const { t } = useLanguage();
  const [rows, setRows] = useState<CatalogItem[]>([]);
  const [values, setValues] = useState<CatalogValues>({ ...empty });
  const [editingId, setEditingId] = useState<number | null>(null);
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);
  const codeRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    clear();
    void load();
  }, [kind]);

  async function load() {
    try {
      setRows(await getCatalog(kind));
    } catch {
      setError(t("unableLoadCatalog"));
    }
  }

  function clear() {
    setValues({ ...empty });
    setEditingId(null);
    setError("");
  }

  function change<K extends keyof CatalogValues>(name: K, value: CatalogValues[K]) {
    setValues(current => ({ ...current, [name]: value }));
  }

  function edit(row: CatalogItem) {
    setValues({
      ...empty, ...row,
      parentId: row.parentId ?? null,
      decimalPlaces: row.decimalPlaces ?? 0,
    });
    setEditingId(row.id);
    setError("");
    codeRef.current?.focus();
  }

  async function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaving(true);
    setError("");
    try {
      await saveCatalog(kind, values, editingId ?? undefined);
      clear();
      await load();
    } catch (caught) {
      setError(caught instanceof Error ? languageError(caught.message, t) : t("unableSaveCatalog"));
      codeRef.current?.focus();
    } finally {
      setSaving(false);
    }
  }

  async function remove(row: CatalogItem) {
    if (!window.confirm(`${t("delete")} ${row.nameEn}?`)) return;
    try {
      await deleteCatalog(kind, row.id);
      await load();
    } catch (caught) {
      setError(caught instanceof Error ? languageError(caught.message, t) : t("unableDeleteCatalog"));
    }
  }

  const visibleRows = rows.filter(row =>
    (row.code + row.nameEn + row.nameAr).toLowerCase().includes(query.trim().toLowerCase()),
  );

  return (
    <main className="content">
      <div className="page-heading"><h1>{t(titles[kind])}</h1></div>
      {error && <div className="alert" role="alert">{error}</div>}
      <section className="panel">
        <div className="panel-heading">
          <h2>{t(editingId === null ? "addPartner" : "editPartner")}</h2>
          {editingId !== null && <button className="secondary" type="button" onClick={clear}>{t("cancel")}</button>}
        </div>
        <form className="company-form" onSubmit={save} onKeyDown={advanceOnEnter}>
          <label>{t("code")}
            <input ref={codeRef} required maxLength={30} value={values.code}
              onChange={event => change("code", event.target.value)} />
          </label>
          <label>{t("companyNameEnglish")}
            <input required maxLength={200} value={values.nameEn}
              onChange={event => change("nameEn", event.target.value)} />
          </label>
          <label>{t("companyNameArabic")}
            <input maxLength={200} dir="rtl" value={values.nameAr}
              onChange={event => change("nameAr", event.target.value)} />
          </label>
          {kind === "categories" && (
            <label>{t("parentCategory")}
              <select value={values.parentId ?? ""} onChange={event =>
                change("parentId", event.target.value ? Number(event.target.value) : null)}>
                <option value="">{t("noParentCategory")}</option>
                {rows.filter(row => row.id !== editingId).map(row => (
                  <option key={row.id} value={row.id}>{row.nameEn}</option>
                ))}
              </select>
            </label>
          )}
          {kind === "units" && (
            <label>{t("decimalPlaces")}
              <input required type="number" min={0} max={6} step={1}
                value={values.decimalPlaces}
                onChange={event => change("decimalPlaces", Number(event.target.value))} />
            </label>
          )}
          <label className="checkbox full-width">
            <input type="checkbox" checked={values.isActive}
              onChange={event => change("isActive", event.target.checked)} />
            {t("active")}
          </label>
          <div className="form-actions full-width">
            <button type="submit" disabled={saving}>{saving ? t("saving") : t("savePartner")}</button>
          </div>
        </form>
      </section>
      <section className="panel">
        <div className="panel-heading">
          <h2>{t(titles[kind])} ({rows.length})</h2>
          <input className="search" placeholder={t("searchCompanies")} value={query}
            onChange={event => setQuery(event.target.value)} />
        </div>
        <div className="table-wrap">
          <table>
            <thead><tr>
              <th>ID</th><th>{t("code")}</th><th>{t("companyNameEnglish")}</th>
              <th>{t("companyNameArabic")}</th>
              {kind === "categories" && <th>{t("parentCategory")}</th>}
              {kind === "units" && <th>{t("decimalPlaces")}</th>}
              <th>{t("status")}</th><th>{t("actions")}</th>
            </tr></thead>
            <tbody>
              {visibleRows.map(row => (
                <tr key={row.id}>
                  <td>{row.id}</td><td>{row.code}</td><td>{row.nameEn}</td>
                  <td dir="rtl">{row.nameAr}</td>
                  {kind === "categories" && <td>{rows.find(item => item.id === row.parentId)?.nameEn ?? "-"}</td>}
                  {kind === "units" && <td>{row.decimalPlaces}</td>}
                  <td>{t(row.isActive ? "active" : "inactive")}</td>
                  <td className="actions">
                    <button type="button" className="secondary" onClick={() => edit(row)}>{t("edit")}</button>
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
