import { FormEvent, useEffect, useRef, useState } from "react";
import { Role, Permission, createRole, deleteRole, getRoles, updateRole, getPermissionCatalog, getRolePermissions, saveRolePermissions } from "../api/roles";
import { advanceOnEnter } from "../forms/keyboard";
import { languageError, useLanguage } from "../i18n";
import { permissionLabel } from "../locale";


export function Roles() {
  const { t, language } = useLanguage();
  const nameInput = useRef<HTMLInputElement>(null);
  const [roles, setRoles] = useState<Role[]>([]);
  const [name, setName] = useState("");
  const [editingId, setEditingId] = useState<number | null>(null);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);
  const [catalog, setCatalog] = useState<Permission[]>([]);
  const [grants, setGrants] = useState<string[]>([]);
  const [savingPermissions, setSavingPermissions] = useState(false);
  const [notice, setNotice] = useState("");

  useEffect(() => {
    void loadRoles();
    void getPermissionCatalog().then(setCatalog).catch(() => setError(t("unableLoadPermissions")));
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
    setGrants([]);
    setNotice("");
  }

  async function editRole(role: Role) {
    setName(role.name);
    setEditingId(role.id);
    setError("");
    setNotice("");
    try {
      setGrants((await getRolePermissions(role.id)).permissions);
      nameInput.current?.focus();
    } catch {
      setError(t("unableLoadPermissions"));
    }
  }

  async function saveGrants() {
    if (editingId === null) return;
    setSavingPermissions(true);
    setError("");
    try {
      setGrants((await saveRolePermissions(editingId, grants)).permissions);
      setNotice(t("permissionsSaved"));
    } catch (error) {
      setError(error instanceof Error ? languageError(error.message, t) : t("unableSaveRole"));
    } finally {
      setSavingPermissions(false);
    }
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
      setError(error instanceof Error ? languageError(error.message, t) : t("unableSaveRole"));
      nameInput.current?.focus();
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
      setError(error instanceof Error ? languageError(error.message, t) : t("unableDeleteRole"));
    }
  }

  return (
    <main className="content">
      <div className="page-heading">
        <h1>{t("roleMaster")}</h1>
        <p>{t("roleDescription")}</p>
      </div>

      {error && <div className="alert" role="alert">{error}</div>}
      {notice && <div role="status">{notice}</div>}

      <section className="panel">
        <div className="panel-heading">
          <h2>{editingId === null ? t("addRole") : t("editRole")}</h2>
          {editingId !== null && (
            <button className="secondary" type="button" onClick={reset}>{t("cancel")}</button>
          )}
        </div>
        <form className="role-form" onSubmit={save} onKeyDown={advanceOnEnter}>
          <label>
            {t("roleName")}
            <input
              ref={nameInput}
              value={name}
              maxLength={100}
              required
              onChange={(event) => setName(event.target.value)}
              placeholder={t("roleName")}
            />
          </label>
          <button disabled={saving || !name.trim()} type="submit">
            {saving ? t("saving") : editingId === null ? t("addRole") : t("saveChanges")}
          </button>
        </form>
      </section>

      {editingId !== null && (
        <section className="panel">
          <h2>{t("permissionMatrix")}</h2>
          <div className="permission-matrix">
            {catalog.map((item) => (
              <label className="checkbox" key={item.code}>
                <input
                  type="checkbox"
                  checked={grants.includes(item.code)}
                  onChange={(event) => setGrants((current) =>
                    event.target.checked
                      ? [...current, item.code]
                      : current.filter((code) => code !== item.code)
                  )}
                />
                {permissionLabel(item.code, item.name, language)}
              </label>
            ))}
          </div>
          <button type="button" disabled={savingPermissions} onClick={() => void saveGrants()}>
            {savingPermissions ? t("saving") : t("savePermissions")}
          </button>
        </section>
      )}

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
                        <button className="secondary" type="button" onClick={() => void editRole(role)}>{t("edit")}</button>
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
