import { ReactNode } from "react";
import { CurrentUser } from "../api/auth";
import { Page } from "../App";
import { useLanguage } from "../i18n";

interface Props {
  user: CurrentUser;
  page: Page;
  onPageChange: (page: Page) => void;
  onLogout: () => void;
  children: ReactNode;
}

export function AppShell({ user, page, onPageChange, onLogout, children }: Props) {
  const { t, language, setLanguage } = useLanguage();
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">{t("title")}</div>
        <nav>
          <span className="nav-section">{t("masters")}</span>
          <button
            type="button"
            className={`nav-link ${page === "companies" ? "active" : ""}`}
            onClick={() => onPageChange("companies")}
          >
            {t("companyMaster")}
          </button>
          {user.isAdmin && (
            <button
              type="button"
              className={`nav-link ${page === "roles" ? "active" : ""}`}
              onClick={() => onPageChange("roles")}
            >
              {t("roleMaster")}
            </button>
          )}
          {user.isAdmin && (
            <button type="button" className={`nav-link ${page === "users" ? "active" : ""}`}
              onClick={() => onPageChange("users")}>{t("userMaster")}</button>
          )}
        </nav>
      </aside>

      <div className="main-area">
        <header className="topbar">
          <label className="language-switch">
            {t("language")}
            <select aria-label={t("language")} value={language} onChange={(event) => setLanguage(event.target.value as "en" | "ar")}>
              <option value="en">English</option>
              <option value="ar">العربية</option>
            </select>
          </label>
          <div><strong>{user.name || user.email}</strong></div>
          <button className="secondary" type="button" onClick={onLogout}>{t("logout")}</button>
        </header>
        {children}
      </div>
    </div>
  );
}
