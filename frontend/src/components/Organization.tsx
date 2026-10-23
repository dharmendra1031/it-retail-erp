import { FormEvent, useEffect, useState } from "react";
import { getCompanies, Company } from "../api/companies";
import {
  Branch, BranchValues, Warehouse, WarehouseValues, getBranches, getWarehouses,
  saveBranch, saveWarehouse, deleteBranch, deleteWarehouse,
} from "../api/organization";
import { advanceOnEnter } from "../forms/keyboard";
import { useLanguage } from "../i18n";

const initialBranch: BranchValues = { companyId: 0, code: "", nameEn: "", nameAr: "", isActive: true };
const initialWarehouse: WarehouseValues = { branchId: 0, code: "", nameEn: "", nameAr: "", isActive: true };

export function Organization() {
  const { t } = useLanguage();
  const [companies, setCompanies] = useState<Company[]>([]);
  const [branches, setBranches] = useState<Branch[]>([]);
  const [warehouses, setWarehouses] = useState<Warehouse[]>([]);
  const [branch, setBranch] = useState<BranchValues>(initialBranch);
  const [warehouse, setWarehouse] = useState<WarehouseValues>(initialWarehouse);
  const [branchId, setBranchId] = useState<number | null>(null);
  const [warehouseId, setWarehouseId] = useState<number | null>(null);
  const [error, setError] = useState("");

  async function load() {
    try {
      const [companiesResponse, branchesResponse, warehousesResponse] = await Promise.all([
        getCompanies(), getBranches(), getWarehouses(),
      ]);
      setCompanies(companiesResponse);
      setBranches(branchesResponse);
      setWarehouses(warehousesResponse);
    } catch {
      setError(t("invalidRequest"));
    }
  }

  useEffect(() => { void load(); }, []);

  async function submitBranch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    try {
      await saveBranch(branch, branchId ?? undefined);
      setBranch(initialBranch);
      setBranchId(null);
      await load();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : t("invalidRequest"));
    }
  }

  async function submitWarehouse(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    try {
      await saveWarehouse(warehouse, warehouseId ?? undefined);
      setWarehouse(initialWarehouse);
      setWarehouseId(null);
      await load();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : t("invalidRequest"));
    }
  }

  async function removeBranch(id: number) {
    if (!window.confirm(t("confirmDeleteBranch"))) return;
    try { await deleteBranch(id); await load(); }
    catch (caught) { setError(caught instanceof Error ? caught.message : t("invalidRequest")); }
  }

  async function removeWarehouse(id: number) {
    if (!window.confirm(t("confirmDeleteWarehouse"))) return;
    try { await deleteWarehouse(id); await load(); }
    catch (caught) { setError(caught instanceof Error ? caught.message : t("invalidRequest")); }
  }

  return (
    <main className="content">
      <div className="page-heading"><h1>{t("organizationMaster")}</h1></div>
      {error && <div className="alert" role="alert">{error}</div>}
      <section className="panel">
        <h2>{t("branchMaster")}</h2>
        <form className="company-form" onKeyDown={advanceOnEnter} onSubmit={submitBranch}>
          <label>{t("company")}
            <select required value={branch.companyId || ""}
              onChange={(event) => setBranch({ ...branch, companyId: Number(event.target.value) })}>
              <option value="">{t("selectCompany")}</option>
              {companies.map((company) => <option key={company.id} value={company.id}>{company.nameEn}</option>)}
            </select>
          </label>
          <label>{t("code")}
            <input required maxLength={30} value={branch.code}
              onChange={(event) => setBranch({ ...branch, code: event.target.value })} />
          </label>
          <label>{t("companyNameEnglish")}
            <input required maxLength={200} value={branch.nameEn}
              onChange={(event) => setBranch({ ...branch, nameEn: event.target.value })} />
          </label>
          <label>{t("companyNameArabic")}
            <input dir="rtl" maxLength={200} value={branch.nameAr}
              onChange={(event) => setBranch({ ...branch, nameAr: event.target.value })} />
          </label>
          <button type="submit">{t("saveBranch")}</button>
        </form>
        <div className="table-wrap">
          <table><thead><tr><th>ID</th><th>{t("code")}</th><th>{t("branchMaster")}</th><th>{t("actions")}</th></tr></thead>
            <tbody>{branches.map((item) => (
              <tr key={item.id}><td>{item.id}</td><td>{item.code}</td><td>{item.nameEn}</td>
                <td>
                  <button className="secondary" type="button" onClick={() => {
                    setBranchId(item.id); setBranch({ companyId: item.companyId, code: item.code,
                      nameEn: item.nameEn, nameAr: item.nameAr, isActive: item.isActive });
                  }}>{t("edit")}</button>
                  <button className="danger" type="button" onClick={() => void removeBranch(item.id)}>{t("delete")}</button>
                </td>
              </tr>
            ))}</tbody>
          </table>
        </div>
      </section>
      <section className="panel">
        <h2>{t("warehouseMaster")}</h2>
        <form className="company-form" onKeyDown={advanceOnEnter} onSubmit={submitWarehouse}>
          <label>{t("branchMaster")}
            <select required value={warehouse.branchId || ""}
              onChange={(event) => setWarehouse({ ...warehouse, branchId: Number(event.target.value) })}>
              <option value="">{t("selectBranch")}</option>
              {branches.map((item) => <option key={item.id} value={item.id}>{item.nameEn}</option>)}
            </select>
          </label>
          <label>{t("code")}
            <input required maxLength={30} value={warehouse.code}
              onChange={(event) => setWarehouse({ ...warehouse, code: event.target.value })} />
          </label>
          <label>{t("companyNameEnglish")}
            <input required maxLength={200} value={warehouse.nameEn}
              onChange={(event) => setWarehouse({ ...warehouse, nameEn: event.target.value })} />
          </label>
          <label>{t("companyNameArabic")}
            <input dir="rtl" maxLength={200} value={warehouse.nameAr}
              onChange={(event) => setWarehouse({ ...warehouse, nameAr: event.target.value })} />
          </label>
          <button type="submit">{t("saveWarehouse")}</button>
        </form>
        <div className="table-wrap">
          <table><thead><tr><th>ID</th><th>{t("code")}</th><th>{t("warehouseMaster")}</th><th>{t("actions")}</th></tr></thead>
            <tbody>{warehouses.map((item) => (
              <tr key={item.id}><td>{item.id}</td><td>{item.code}</td><td>{item.nameEn}</td>
                <td>
                  <button className="secondary" type="button" onClick={() => {
                    setWarehouseId(item.id); setWarehouse({ branchId: item.branchId, code: item.code,
                      nameEn: item.nameEn, nameAr: item.nameAr, isActive: item.isActive });
                  }}>{t("edit")}</button>
                  <button className="danger" type="button" onClick={() => void removeWarehouse(item.id)}>{t("delete")}</button>
                </td>
              </tr>
            ))}</tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
