import { ReactNode } from "react";
import { CurrentUser } from "../api/auth";
import { Page } from "../App";

interface Props {
  user: CurrentUser;
  page: Page;
  onPageChange: (page: Page) => void;
  onLogout: () => void;
  children: ReactNode;
}

export function AppShell({ user, page, onPageChange, onLogout, children }: Props) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">IT Retail ERP</div>
        <nav>
          <span className="nav-section">Masters</span>
          <button
            type="button"
            className={`nav-link ${page === "companies" ? "active" : ""}`}
            onClick={() => onPageChange("companies")}
          >
            Company Master
          </button>
          {user.isAdmin && (
            <button
              type="button"
              className={`nav-link ${page === "roles" ? "active" : ""}`}
              onClick={() => onPageChange("roles")}
            >
              Role Master
            </button>
          )}
        </nav>
      </aside>

      <div className="main-area">
        <header className="topbar">
          <div><strong>{user.name || user.email}</strong></div>
          <button className="secondary" type="button" onClick={onLogout}>Logout</button>
        </header>
        {children}
      </div>
    </div>
  );
}
