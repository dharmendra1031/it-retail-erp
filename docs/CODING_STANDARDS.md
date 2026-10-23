# IT Retail ERP — Mandatory coding standards

- Write minimal, conventional, developer-style Django, ASP.NET Core and React code; meaningful naming, reusable helpers, no unnecessary abstractions/CSS.
- The same React UI must work with Django and ASP.NET Core APIs backed by SQL Server. All application database primary keys are numeric auto-increment BIGINT. Do not introduce UUID-based application IDs.
- **Every form must be keyboard-first:** Enter moves focus to the next editable field; Enter in the last field submits; Tab/Shift+Tab remain native; arrow navigation stays native in selectable controls; Enter in textarea adds a newline. On validation failure the invalid field receives focus. All actions also work with mouse.
- Use the shared `frontend/src/utils/formKeyboard.ts` handler rather than duplicating event logic. Do not intercept IME composition or modifier shortcuts.
- **English and Arabic are mandatory languages:** shared language switcher, `lang` / `dir` on the document (English LTR; Arabic RTL), translated labels, navigation and errors, Unicode in SQL Server and appropriate direction for Arabic content. New features must add both translations; later languages should be addable through the dictionary without rewriting screens. Bilingual report/print acceptance remains owned by localization/report packages.
- Form keyboard behavior and both language modes require Playwright regression tests.
- Enforce authorization and CSRF server-side; do not trust client-side hiding. Use safe migrations and verify with real SQL Server CI. Never claim unexecuted tests passed.
