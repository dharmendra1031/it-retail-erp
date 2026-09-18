import { Company } from "../api/companies";

interface Props {
  companies: Company[];
  query: string;
  onQueryChange: (value: string) => void;
  onEdit: (company: Company) => void;
  onDelete: (company: Company) => void;
}

export function CompanyTable({
  companies,
  query,
  onQueryChange,
  onEdit,
  onDelete,
}: Props) {
  return (
    <section className="panel">
      <div className="panel-heading">
        <h2>Companies</h2>
        <input
          className="search"
          placeholder="Search companies..."
          value={query}
          onChange={(event) => onQueryChange(event.target.value)}
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
            {companies.map((company) => (
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
                    onClick={() => onEdit(company)}
                  >
                    Edit
                  </button>
                  <button
                    className="danger"
                    type="button"
                    onClick={() => onDelete(company)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
            {!companies.length && (
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
  );
}
