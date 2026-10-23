import { Company } from "../api/companies";
import { useLanguage } from "../i18n";

interface Props {
  companies: Company[];
  canManage: boolean;
  query: string;
  onQueryChange: (value: string) => void;
  onEdit: (company: Company) => void;
  onDelete: (company: Company) => void;
  onPrint: (company: Company) => void;
}

export function CompanyTable({
  companies,
  canManage,
  query,
  onQueryChange,
  onEdit,
  onDelete,
  onPrint,
}: Props) {
  const { t } = useLanguage();
  return (
    <section className="panel">
      <div className="panel-heading">
        <h2>{t("companies")}</h2>
        <input
          className="search"
          placeholder={t("searchCompanies")}
          value={query}
          onChange={(event) => onQueryChange(event.target.value)}
        />
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>{t("company")}</th>
              <th>{t("arabicName")}</th>
              <th>{t("mobile")}</th>
              <th>{t("taxNo")}</th>
              <th>{t("status")}</th>
              <th>{t("actions")}</th>
            </tr>
          </thead>
          <tbody>
            {companies.map((company) => (
              <tr key={company.id}>
                <td>{company.id}</td>
                <td>{company.nameEn}</td>
                <td dir="rtl">{company.nameAr}</td>
                <td>{company.mobile}</td>
                <td>{company.taxNumber}</td>
                <td>{company.isActive ? t("active") : t("inactive")}</td>
                <td className="actions">
                  <button className="secondary" type="button" onClick={() => onPrint(company)}>{t("printIdentity")}</button>
                  {canManage && (
                    <>
                    <button className="secondary" type="button" onClick={() => onEdit(company)}>
                      {t("edit")}
                    </button>
                    <button className="danger" type="button" onClick={() => onDelete(company)}>
                      {t("delete")}
                    </button>
                    </>
                  )}
                </td>
              </tr>
            ))}
            {!companies.length && (
              <tr>
                <td colSpan={7} className="empty">
                  {t("noCompanies")}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
