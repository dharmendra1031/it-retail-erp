import { ReactNode } from "react";
import { CurrentUser } from "../api/auth";

interface Props {
  user: CurrentUser;
  onLogout: () => void;
  children: ReactNode;
}

export function AppShell({ user, onLogout, children }: Props) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">IT Retail ERP</div>
        <nav>
          <span className="nav-section">Masters</span>
          <a className="nav-link active" href="#companies">
            Company Master
          </a>
        </nav>
      </aside>

      <div className="main-area">
        <header className="topbar">
          <div>
            <strong>{user.name || user.email}</strong>
          </div>
          <button className="secondary" type="button" onClick={onLogout}>
            Logout
          </button>
        </header>

        {children}
      </div>
    </div>
  );
}
