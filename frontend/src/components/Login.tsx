import { FormEvent, useState } from "react";
import { CurrentUser, login } from "../api/auth";
import { advanceOnEnter } from "../forms/keyboard";
import { useLanguage } from "../i18n";


interface Props {
  onLogin: (user: CurrentUser) => void;
}

export function Login({ onLogin }: Props) {
  const { language, setLanguage, t } = useLanguage();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setSubmitting(true);
    setError("");

    try {
      onLogin(await login(email, password, rememberMe));
    } catch {
      setError(t("invalidLogin"));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="login-page">
      <form className="login-card" onSubmit={handleSubmit} onKeyDown={advanceOnEnter}>
        <h1>IT Retail ERP</h1>
        <p>{t("signIn")}</p>
        <label>
          {t("language")}
          <select aria-label="Language" value={language} onChange={(event) => setLanguage(event.target.value as "en" | "ar")}>
            <option value="en">English</option>
            <option value="ar">العربية</option>
          </select>
        </label>

        {error && <div className="alert" role="alert">{error}</div>}

        <label>
          {t("email")}
          <input
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            autoComplete="username"
            required
          />
        </label>

        <label>
          {t("password")}
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            autoComplete="current-password"
            required
          />
        </label>

        <label className="checkbox">
          <input
            type="checkbox"
            checked={rememberMe}
            onChange={(event) => setRememberMe(event.target.checked)}
          />
          {t("rememberMe")}
        </label>

        <button type="submit" disabled={submitting}>
          {submitting ? t("signingIn") : t("login")}
        </button>
      </form>
    </main>
  );
}
