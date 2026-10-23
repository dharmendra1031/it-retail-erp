import { FormEvent, useEffect, useRef, useState } from "react";
import { getRoles, Role } from "../api/roles";
import { ErpUser, getUsers, saveUser, resetUserPassword, UserValues } from "../api/users";
import { advanceOnEnter } from "../forms/keyboard";
import { useLanguage } from "../i18n";

const empty: UserValues = {
  username: "", fullName: "", email: "", mobile: "", password: "",
  isActive: true, roleIds: [],
};

export function Users() {
  const { t } = useLanguage();
  const usernameInput = useRef<HTMLInputElement>(null);
  const [users, setUsers] = useState<ErpUser[]>([]);
  const [roles, setRoles] = useState<Role[]>([]);
  const [values, setValues] = useState<UserValues>(empty);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  async function load() {
    try {
      const [accounts, availableRoles] = await Promise.all([getUsers(), getRoles()]);
      setUsers(accounts);
      setRoles(availableRoles);
    } catch {
      setError(t("unableLoadUsers"));
    }
  }

  useEffect(() => { void load(); }, []);

  function change<K extends keyof UserValues>(key: K, value: UserValues[K]) {
    setValues((current) => ({ ...current, [key]: value }));
  }

  function clear() {
    setEditingId(null);
    setValues(empty);
    setError("");
  }

  function edit(user: ErpUser) {
    setEditingId(user.id);
    setValues({
      username: user.username, fullName: user.fullName, email: user.email,
      mobile: user.mobile, isActive: user.isActive, roleIds: user.roleIds,
      password: "",
    });
    usernameInput.current?.focus();
  }

  async function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setSaving(true);
    try {
      const payload = { ...values, password: editingId === null ? values.password : undefined };
      await saveUser(payload, editingId ?? undefined);
      clear();
      await load();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : t("unableSaveUser"));
      usernameInput.current?.focus();
    } finally {
      setSaving(false);
    }
  }

  async function resetPassword() {
    if (editingId === null || !values.password) return;
    setSaving(true);
    setError("");
    try {
      await resetUserPassword(editingId, values.password);
      change("password", "");
    } catch {
      setError(t("unableSaveUser"));
    } finally {
      setSaving(false);
    }
  }

  return (
    <main className="content">
      <div className="page-heading">
        <h1>{t("userMaster")}</h1>
        <p>{t("userDescription")}</p>
      </div>
      {error && <div className="alert" role="alert">{error}</div>}
      <section className="panel">
        <div className="panel-heading">
          <h2>{editingId === null ? t("addUser") : t("editUser")}</h2>
          {editingId !== null && <button type="button" className="secondary" onClick={clear}>{t("cancel")}</button>}
        </div>
        <form className="company-form" onSubmit={save} onKeyDown={advanceOnEnter}>
          <label>{t("username")}
            <input ref={usernameInput} required maxLength={150} value={values.username}
              onChange={(event) => change("username", event.target.value)} />
          </label>
          <label>{t("fullName")}
            <input maxLength={150} value={values.fullName}
              onChange={(event) => change("fullName", event.target.value)} />
          </label>
          <label>{t("email")}
            <input type="email" required maxLength={254} value={values.email}
              onChange={(event) => change("email", event.target.value)} />
          </label>
          <label>{t("mobile")}
            <input maxLength={30} value={values.mobile}
              onChange={(event) => change("mobile", event.target.value)} />
          </label>
          <label>{t("password")}
            <input type="password" autoComplete="new-password"
              required={editingId === null} value={values.password ?? ""}
              onChange={(event) => change("password", event.target.value)} />
          </label>
          <fieldset className="full-width">
            <legend>{t("roles")}</legend>
            {roles.map((role) => (
              <label className="checkbox" key={role.id}>
                <input type="checkbox" checked={values.roleIds.includes(role.id)}
                  onChange={(event) => change("roleIds", event.target.checked
                    ? [...values.roleIds, role.id]
                    : values.roleIds.filter((id) => id !== role.id))} />
                {role.name}
              </label>
            ))}
          </fieldset>
          <label className="checkbox full-width">
            <input type="checkbox" checked={values.isActive}
              onChange={(event) => change("isActive", event.target.checked)} />
            {t("active")}
          </label>
          <div className="form-actions full-width">
            <button type="submit" disabled={saving}>{saving ? t("saving") : t("saveUser")}</button>
            {editingId !== null && (
              <button type="button" className="secondary" disabled={saving || !values.password}
                onClick={() => void resetPassword()}>{t("resetPassword")}</button>
            )}
          </div>
        </form>
      </section>
      <section className="panel">
        <h2>{t("users")} ({users.length})</h2>
        <div className="table-wrap">
          <table>
            <thead><tr>
              <th>ID</th><th>{t("username")}</th><th>{t("fullName")}</th>
              <th>{t("email")}</th><th>{t("status")}</th><th>{t("actions")}</th>
            </tr></thead>
            <tbody>{users.map((user) => (
              <tr key={user.id}>
                <td>{user.id}</td><td>{user.username}</td><td>{user.fullName}</td>
                <td>{user.email}</td><td>{user.isActive ? t("active") : t("inactive")}</td>
                <td><button className="secondary" type="button" onClick={() => edit(user)}>{t("edit")}</button></td>
              </tr>
            ))}</tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
