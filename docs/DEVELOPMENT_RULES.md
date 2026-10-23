# IT Retail ERP — Development rules

Apply these to **every existing and new form/module**.

- Write minimal, idiomatic Django, ASP.NET Core and React code. Use descriptive names, reusable small utilities and framework conventions. Avoid duplicate abstractions, unnecessary CSS or speculative features.
- Keep Django and ASP.NET Core business/API behavior equivalent and backed by SQL Server. Application keys are numeric auto-increment `BIGINT`/`BigAutoField`; never introduce UUID identifiers.
- **Keyboard first:** Enter moves from a single-line input to the next enabled, visible field; Enter on the last field submits using the browser's native form validation. Native textarea Enter inserts a newline; file/select inputs retain their native Enter behavior. Tab and Shift+Tab always work; Space/arrow keys retain standard control semantics. Validations must focus the invalid control. Preserve mouse usability.
- **Languages:** English (`en`, LTR) and Arabic (`ar`, RTL) must be available at launch, with an accessible language switcher and translated form labels, navigation, validation messages and other UI text. Store bilingual business fields separately and preserve Unicode. Future languages extend the shared dictionary; do not hardcode user-facing text across components.
- Keep forms accessible: associated labels, visible focus indicators, native HTML field validation, correct direction for Arabic values and responsive layout.
- Every new/changed form requires keyboard and language-specific Playwright coverage, plus backend/API validation and security tests where appropriate.
- For production: never hardcode passwords, commit secrets, bypass CSRF, guess a SQL migration result or claim unexecuted tests PASS.
