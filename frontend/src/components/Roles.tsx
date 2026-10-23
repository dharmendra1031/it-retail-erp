import { FormEvent, useEffect, useState } from "react";
import { Role, createRole, deleteRole, getRoles, updateRole } from "../api/roles";
import { advanceOnEnter } from "../forms/keyboard";
import { languageError, useLanguage } from "../i18n";
import { useLanguage } from "../i18n";
import { handleFormEnter } from "../utils/formKeyboard";

export function Roles() {
  const { t } = useLanguage();
  const { t, error: translateError } = useLanguage();
  const [roles, setRoles] = useState<Role[]>([]);
  const [name, setName] = useState("");
  const [editingId, setEditingId] = useState<number | null>(null);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    void loadRoles();
  }, []);

  async function loadRoles() {
    try {
      setRoles(await getRoles());
    } catch {
      setError(t("unableLoadRoles"));
    }
  }

  function reset() {
    setName("");
    setEditingId(null);
  }

  async function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaving(true);
    setError("");
    try {
      if (editingId === null) {
        await createRole(name.trim());
      } else {
        await updateRole(editingId, name.trim());
      }
      reset();
      await loadRoles();
    } catch (error) {
      setError(translateError(error, "unableSaveRole"));
    } finally {
      setSaving(false);
    }
  }

  async function remove(role: Role) {
    if (!window.confirm(`${t("confirmDeleteRole")} "${role.name}"?`)) {
      return;
    }

    setError("");
    try {
      await deleteRole(role.id);
      await loadRoles();
    } catch (error) {
      setError(translateError(error, "unableDeleteRole"));
    }
  }

  return (
    <main className="content">
      <div className="page-heading">
        <h1>{t("roleMaster")}</h1>
        <p>{t("roleDescription")}</p>
      </div>

      {error && <div className="alert" role="alert">{error}</div>}

      <section className="panel">
        <div className="panel-heading">
          <h2>{editingId === null ? t("addRole") : t("editRole")}</h2>
          {editingId !== null && (
            <button className="secondary" type="button" onClick={reset}>{t("cancel")}</button>
          )}
        </div>
        <form className="role-form" onSubmit={save} onKeyDown={handleFormEnter}>
          <label>
            {t("roleName")}
            <input
              value={name}
              maxLength={100}
              required
              onChange={(event) => setName(event.target.value)}
              placeholder={t("rolePlaceholder")}
            />
          </label>
          <button disabled={saving || !name.trim()} type="submit">
            {saving ? t("saving") : editingId === null ? t("addRole") : t("saveChanges")}
          </button>
        </form>
      </section>

      <section className="panel">
        <div className="panel-heading"><h2>{t("roles")} ({roles.length})</h2></div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr><th>ID</th><th>{t("roleName")}</th><th>{t("actions")}</th></tr>
            </thead>
            <tbody>
              {roles.map((role) => (
                <tr key={role.id}>
                  <td>{role.id}</td>
                  <td>{role.name}</td>
                  <td>
                    {role.name.toLowerCase() !== "admin" && (
                      <div className="actions">
                        <button className="secondary" type="button" onClick={() => {
                          setName(role.name);
                          setEditingId(role.id);
                          setError("");
                        }}>{t("edit")}</button>
                        <button className="danger" type="button" onClick={() => void remove(role)}>
                          {t("delete")}
                        </button>
                      </div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {roles.length === 0 && <p className="empty">{t("noRoles")}</p>}
        </div>
      </section>
    </main>
  );
}
