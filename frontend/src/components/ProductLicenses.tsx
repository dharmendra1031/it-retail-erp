import { FormEvent, useEffect, useState } from "react";
import { Product } from "../api/products";
import {
  ProductLicense, getProductLicenses, revokeProductLicense, saveProductLicense,
} from "../api/productLicenses";
import { languageError, useLanguage } from "../i18n";

export function ProductLicenses({ product, onClose }: {
  product: Product;
  onClose: () => void;
}) {
  const { t } = useLanguage();
  const [rows, setRows] = useState<ProductLicense[]>([]);
  const [number, setNumber] = useState("");
  const [key, setKey] = useState("");
  const [activationDate, setActivationDate] = useState("");
  const [expiryDate, setExpiryDate] = useState("");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    let active = true;
    getProductLicenses(product.id)
      .then(data => { if (active) setRows(data); })
      .catch(() => { if (active) setError(t("unableLoadLicenses")); });
    return () => { active = false; };
  }, [product.id]);

  async function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaving(true);
    setError("");
    try {
      await saveProductLicense({
        productId: product.id, licenseNumber: number, licenseKey: key,
        activationDate: activationDate || null, expiryDate: expiryDate || null,
      });
      setNumber("");
      setKey("");
      setActivationDate("");
      setExpiryDate("");
      setRows(await getProductLicenses(product.id));
    } catch (caught) {
      setError(caught instanceof Error ? languageError(caught.message, t) : t("unableSaveLicense"));
    } finally {
      setSaving(false);
    }
  }

  async function revoke(id: number) {
    if (!window.confirm(t("confirmRevokeLicense"))) return;
    setError("");
    try {
      await revokeProductLicense(id);
      setRows(await getProductLicenses(product.id));
    } catch (caught) {
      setError(caught instanceof Error ? languageError(caught.message, t) : t("unableRevokeLicense"));
    }
  }

  return (
    <section className="panel">
      <div className="panel-heading">
        <h2>{t("productLicenses")}: {product.sku}</h2>
        <button type="button" className="secondary" onClick={onClose}>{t("cancel")}</button>
      </div>
      {error && <div role="alert" className="alert">{error}</div>}
      <form className="company-form" onSubmit={save}>
        <label>{t("licenseNumber")}
          <input maxLength={100} value={number} onChange={event => setNumber(event.target.value)} />
        </label>
        <label>{t("licenseKey")}
          <input type="password" autoComplete="off" maxLength={512} value={key}
            onChange={event => setKey(event.target.value)} />
        </label>
        <label>{t("activationDate")}
          <input type="date" value={activationDate}
            onChange={event => setActivationDate(event.target.value)} />
        </label>
        <label>{t("expiryDate")}
          <input type="date" min={activationDate || undefined} value={expiryDate}
            onChange={event => setExpiryDate(event.target.value)} />
        </label>
        <div className="form-actions full-width">
          <button type="submit" disabled={saving || (!number.trim() && !key.trim())}>
            {t("addLicense")}
          </button>
        </div>
      </form>
      <div className="table-wrap">
        <table>
          <thead><tr>
            <th>ID</th><th>{t("licenseNumber")}</th><th>{t("licenseKey")}</th>
            <th>{t("activationDate")}</th><th>{t("expiryDate")}</th>
            <th>{t("licenseStatus")}</th><th>{t("actions")}</th>
          </tr></thead>
          <tbody>
            {rows.map(row => <tr key={row.id}>
              <td>{row.id}</td><td>{row.licenseNumber || "-"}</td>
              <td>{t(row.hasKey ? "licenseStored" : "licenseNoKey")}</td>
              <td>{row.activationDate || "-"}</td><td>{row.expiryDate || "-"}</td>
              <td>{t(row.isActive ? "active" : "inactive")}</td>
              <td>{row.isActive && <button type="button" className="danger"
                onClick={() => void revoke(row.id)}>{t("revokeLicense")}</button>}</td>
            </tr>)}
          </tbody>
        </table>
      </div>
    </section>
  );
}
