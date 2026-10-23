import { useEffect, useState } from "react";
import { CurrentUser, getCurrentUser, logout } from "./api/auth";
import { AppShell } from "./components/AppShell";
import { Companies } from "./components/Companies";
import { Login } from "./components/Login";
import { Roles } from "./components/Roles";

export type Page = "companies" | "roles";

export default function App() {
  const [user, setUser] = useState<CurrentUser | null | undefined>(undefined);
  const [page, setPage] = useState<Page>("companies");

  useEffect(() => {
    const handleExpiredSession = () => {
      setUser(null);
      setPage("companies");
    };
    window.addEventListener("erp:session-expired", handleExpiredSession);
    return () => window.removeEventListener("erp:session-expired", handleExpiredSession);
  }, []);

  useEffect(() => {
    getCurrentUser()
      .then(setUser)
      .catch(() => setUser(null));
  }, []);

  async function handleLogout() {
    try {
      await logout();
    } finally {
      setUser(null);
      setPage("companies");
    }
  }

  if (user === undefined) {
    return <div className="loading">Loading...</div>;
  }

  if (!user) {
    return <Login onLogin={setUser} />;
  }

  const activePage = user.isAdmin ? page : "companies";

  return (
    <AppShell user={user} page={activePage} onPageChange={setPage} onLogout={handleLogout}>
      {activePage === "roles" ? <Roles /> : <Companies canManage={user.isAdmin} />}
    </AppShell>
  );
}
