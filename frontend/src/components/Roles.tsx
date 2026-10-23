import { FormEvent, useEffect, useState } from "react";
import { Role, createRole, deleteRole, getRoles, updateRole } from "../api/roles";

export function Roles() {
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
      setError("Unable to load roles.");
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
      setError(error instanceof Error ? error.message : "Unable to save role.");
    } finally {
      setSaving(false);
    }
  }

  async function remove(role: Role) {
    if (!window.confirm(`Delete role "${role.name}"?`)) {
      return;
    }

    setError("");
    try {
      await deleteRole(role.id);
      await loadRoles();
    } catch (error) {
      setError(error instanceof Error ? error.message : "Unable to delete role.");
    }
  }

  return (
    <main className="content">
      <div className="page-heading">
        <h1>Role Master</h1>
        <p>Manage user roles. Assigned roles cannot be deleted.</p>
      </div>

      {error && <div className="alert" role="alert">{error}</div>}

      <section className="panel">
        <div className="panel-heading">
          <h2>{editingId === null ? "Add Role" : "Edit Role"}</h2>
          {editingId !== null && (
            <button className="secondary" type="button" onClick={reset}>Cancel</button>
          )}
        </div>
        <form className="role-form" onSubmit={save}>
          <label>
            Role Name
            <input
              value={name}
              maxLength={100}
              required
              onChange={(event) => setName(event.target.value)}
              placeholder="e.g. Sales Manager"
            />
          </label>
          <button disabled={saving || !name.trim()} type="submit">
            {saving ? "Saving..." : editingId === null ? "Add Role" : "Save Changes"}
          </button>
        </form>
      </section>

      <section className="panel">
        <div className="panel-heading"><h2>Roles ({roles.length})</h2></div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr><th>ID</th><th>Role Name</th><th>Actions</th></tr>
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
                        }}>Edit</button>
                        <button className="danger" type="button" onClick={() => void remove(role)}>
                          Delete
                        </button>
                      </div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {roles.length === 0 && <p className="empty">No roles available.</p>}
        </div>
      </section>
    </main>
  );
}
