import { FormEvent, useEffect, useRef, useState } from "react";
import { CatalogItem, getCatalog } from "../api/catalog";
import { Product, ProductValues, deleteProduct, getProducts, saveProduct } from "../api/products";
import { advanceOnEnter } from "../forms/keyboard";
import { languageError, useLanguage } from "../i18n";
import { ProductLicenses } from "./ProductLicenses";

const blank: ProductValues = {
  sku: "", barcode: "", nameEn: "", nameAr: "",
  descriptionEn: "", descriptionAr: "",
  categoryId: 0, brandId: null, unitId: 0, productType: "stock",
  serialTracked: false, costPrice: "0.000", basePrice: "0.000",
  minPrice: "0.000", reorderLevel: "0.000000", isActive: true,
};

export function Products() {
  const { t, language } = useLanguage();
  const [rows, setRows] = useState<Product[]>([]);
  const [categories, setCategories] = useState<CatalogItem[]>([]);
  const [brands, setBrands] = useState<CatalogItem[]>([]);
  const [units, setUnits] = useState<CatalogItem[]>([]);
  const [values, setValues] = useState<ProductValues>({ ...blank });
  const [editingId, setEditingId] = useState<number | null>(null);
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [saving, setSaving] = useState(false);
  const [licenseProduct, setLicenseProduct] = useState<Product | null>(null);
  const [error, setError] = useState("");
  const skuInput = useRef<HTMLInputElement>(null);

  useEffect(() => {
    Promise.all([getCatalog("categories"), getCatalog("brands"), getCatalog("units")])
      .then(([allCategories, allBrands, allUnits]) => {
        setCategories(allCategories);
        setBrands(allBrands);
        setUnits(allUnits);
      })
      .catch(() => setError(t("unableLoadProducts")));
  }, []);

  useEffect(() => {
    let current = true;
    getProducts(query, page)
      .then(data => {
        if (!current) return;
        setRows(data.items);
        setTotal(data.total);
      })
      .catch(() => { if (current) setError(t("unableLoadProducts")); });
    return () => { current = false; };
  }, [query, page]);

  async function reload(selectedPage = page) {
    const result = await getProducts(query, selectedPage);
    setRows(result.items);
    setTotal(result.total);
  }

  function change<K extends keyof ProductValues>(key: K, value: ProductValues[K]) {
    setValues(current => ({ ...current, [key]: value }));
  }

  function clear() {
    setEditingId(null);
    setValues({ ...blank });
    setError("");
  }

  function edit(product: Product) {
    setEditingId(product.id);
    setValues({ ...product });
    setError("");
    skuInput.current?.focus();
  }

  async function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaving(true);
    setError("");
    try {
      await saveProduct(values, editingId ?? undefined);
      clear();
      setPage(1);
      await reload(1);
    } catch (caught) {
      setError(caught instanceof Error ? languageError(caught.message, t) : t("unableSaveProduct"));
      skuInput.current?.focus();
    } finally {
      setSaving(false);
    }
  }

  async function remove(product: Product) {
    if (!window.confirm(t("confirmDeleteProduct") + " " + product.nameEn + "?")) return;
    try {
      await deleteProduct(product.id);
      await reload();
    } catch (caught) {
      setError(caught instanceof Error ? languageError(caught.message, t) : t("unableDeleteProduct"));
    }
  }

  function label(item: CatalogItem) {
    return language === "ar" && item.nameAr ? item.nameAr : item.nameEn;
  }

  const activeCategories = categories.filter(item => item.isActive || item.id === values.categoryId);
  const activeBrands = brands.filter(item => item.isActive || item.id === values.brandId);
  const activeUnits = units.filter(item => item.isActive || item.id === values.unitId);
  const maxPage = Math.max(1, Math.ceil(total / 25));

  return (
    <main className="content">
      <div className="page-heading"><h1>{t("productMaster")}</h1></div>
      {error && <div role="alert" className="alert">{error}</div>}
      <section className="panel">
        <div className="panel-heading">
          <h2>{t(editingId === null ? "addProduct" : "editProduct")}</h2>
          {editingId !== null && <button className="secondary" type="button" onClick={clear}>{t("cancel")}</button>}
        </div>
        <form className="company-form" onSubmit={save} onKeyDown={advanceOnEnter}>
          <label>{t("productSku")}
            <input ref={skuInput} dir="ltr" required maxLength={40} pattern="[A-Za-z0-9_-]+"
              value={values.sku} onChange={event => change("sku", event.target.value)} />
          </label>
          <label>{t("productBarcode")}
            <input dir="ltr" maxLength={64} value={values.barcode ?? ""}
              onChange={event => change("barcode", event.target.value)} />
          </label>
          <label>{t("productNameEnglish")}
            <input dir="ltr" required maxLength={200} value={values.nameEn}
              onChange={event => change("nameEn", event.target.value)} />
          </label>
          <label>{t("productNameArabic")}
            <input dir="rtl" maxLength={200} value={values.nameAr}
              onChange={event => change("nameAr", event.target.value)} />
          </label>
          <label>{t("productDescriptionEnglish")}
            <textarea dir="ltr" maxLength={1000} value={values.descriptionEn}
              onChange={event => change("descriptionEn", event.target.value)} />
          </label>
          <label>{t("productDescriptionArabic")}
            <textarea dir="rtl" maxLength={1000} value={values.descriptionAr}
              onChange={event => change("descriptionAr", event.target.value)} />
          </label>
          <label>{t("productCategory")}
            <select aria-label={t("productCategory")} required value={values.categoryId || ""}
              onChange={event => change("categoryId", Number(event.target.value))}>
              <option value="">{t("selectProductCategory")}</option>
              {activeCategories.map(item =>
                <option key={item.id} value={item.id}>{label(item)}</option>)}
            </select>
          </label>
          <label>{t("productBrand")}
            <select aria-label={t("productBrand")} value={values.brandId ?? ""}
              onChange={event => change("brandId", event.target.value ? Number(event.target.value) : null)}>
              <option value="">{t("noProductBrand")}</option>
              {activeBrands.map(item =>
                <option key={item.id} value={item.id}>{label(item)}</option>)}
            </select>
          </label>
          <label>{t("productUnit")}
            <select aria-label={t("productUnit")} required value={values.unitId || ""}
              onChange={event => change("unitId", Number(event.target.value))}>
              <option value="">{t("selectProductUnit")}</option>
              {activeUnits.map(item =>
                <option key={item.id} value={item.id}>{label(item)}</option>)}
            </select>
          </label>
          <label>{t("productType")}
            <select aria-label={t("productType")} value={values.productType} onChange={event => {
              const type = event.target.value as ProductValues["productType"];
              setValues(current => ({
                ...current, productType: type,
                serialTracked: type === "stock" ? current.serialTracked : false,
                reorderLevel: type === "stock" ? current.reorderLevel : "0.000000",
              }));
            }}>
              <option value="stock">{t("stockProduct")}</option>
              <option value="nonstock">{t("nonstockProduct")}</option>
              <option value="digital">{t("digitalProduct")}</option>
            </select>
          </label>
          <label>{t("productCostPrice")}
            <input required dir="ltr" inputMode="decimal" pattern="[0-9]+(\.[0-9]{1,3})?"
              value={values.costPrice} onChange={event => change("costPrice", event.target.value)} />
          </label>
          <label>{t("productSellingPrice")}
            <input required dir="ltr" inputMode="decimal" pattern="[0-9]+(\.[0-9]{1,3})?"
              value={values.basePrice} onChange={event => change("basePrice", event.target.value)} />
          </label>
          <label>{t("productMinimumPrice")}
            <input required dir="ltr" inputMode="decimal" pattern="[0-9]+(\.[0-9]{1,3})?"
              value={values.minPrice} onChange={event => change("minPrice", event.target.value)} />
          </label>
          {values.productType === "stock" && (
            <>
              <label>{t("productReorderLevel")}
                <input required dir="ltr" inputMode="decimal" pattern="[0-9]+(\.[0-9]{1,6})?"
                  value={values.reorderLevel} onChange={event => change("reorderLevel", event.target.value)} />
              </label>
              <label className="checkbox">
                <input type="checkbox" checked={values.serialTracked}
                  onChange={event => change("serialTracked", event.target.checked)} />
                {t("serialTracked")}
              </label>
            </>
          )}
          <label className="checkbox">
            <input type="checkbox" checked={values.isActive}
              onChange={event => change("isActive", event.target.checked)} />
            {t("active")}
          </label>
          <div className="form-actions full-width">
            <button type="submit" disabled={saving}>{saving ? t("saving") : t("saveProduct")}</button>
          </div>
        </form>
      </section>
      <section className="panel">
        <div className="panel-heading">
          <h2>{t("productMaster")} ({total})</h2>
          <input className="search" aria-label={t("searchProducts")}
            placeholder={t("searchProducts")} value={query}
            onChange={event => { setQuery(event.target.value); setPage(1); }} />
        </div>
        <div className="table-wrap">
          <table>
            <thead><tr>
              <th>ID</th><th>{t("productSku")}</th><th>{t("productBarcode")}</th>
              <th>{t("productNameEnglish")}</th><th>{t("productNameArabic")}</th>
              <th>{t("productSellingPrice")}</th><th>{t("status")}</th><th>{t("actions")}</th>
            </tr></thead>
            <tbody>
              {rows.map(product => (
                <tr key={product.id}>
                  <td>{product.id}</td><td>{product.sku}</td><td>{product.barcode ?? "-"}</td>
                  <td>{language === "ar" && product.nameAr ? product.nameAr : product.nameEn}</td>
                  <td dir="rtl">{product.nameAr}</td><td>{product.basePrice}</td>
                  <td>{t(product.isActive ? "active" : "inactive")}</td>
                  <td className="actions">
                    <button type="button" className="secondary" onClick={() => edit(product)}>{t("edit")}</button>
                    {product.productType === "digital" &&
                      <button type="button" className="secondary"
                        onClick={() => setLicenseProduct(product)}>{t("productLicenses")}</button>}
                    <button type="button" className="danger" onClick={() => void remove(product)}>{t("delete")}</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {!rows.length && <p>{t("noProducts")}</p>}
        </div>
        <div className="form-actions">
          <button type="button" className="secondary" disabled={page <= 1}
            onClick={() => setPage(value => value - 1)}>{t("previousProductsPage")}</button>
          <span>{t("productsPage")} {page} / {maxPage}</span>
          <button type="button" className="secondary" disabled={page >= maxPage}
            onClick={() => setPage(value => value + 1)}>{t("nextProductsPage")}</button>
        </div>
      </section>
      {licenseProduct && <ProductLicenses key={licenseProduct.id} product={licenseProduct}
        onClose={() => setLicenseProduct(null)} />}
    </main>
  );
}
