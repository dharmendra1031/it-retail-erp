import { useEffect, useState } from "react";
import { CurrentUser, getCurrentUser, logout } from "./api/auth";
import { AppShell } from "./components/AppShell";
import { Companies } from "./components/Companies";
import { Login } from "./components/Login";

export default function App() {
  const [user, setUser] = useState<CurrentUser | null | undefined>(undefined);

  useEffect(() => {
    getCurrentUser()
      .then(setUser)
      .catch(() => setUser(null));
  }, []);

  async function handleLogout() {
    await logout();
    setUser(null);
  }

  if (user === undefined) {
    return <div className="loading">Loading...</div>;
  }

  if (!user) {
    return <Login onLogin={setUser} />;
  }

  return (
    <AppShell user={user} onLogout={handleLogout}>
      <Companies />
    </AppShell>
  );
}
