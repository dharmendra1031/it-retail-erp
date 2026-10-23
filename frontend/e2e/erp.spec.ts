import { expect, test } from "@playwright/test";

const password = process.env.E2E_PASSWORD ?? "";

test("admin can manage roles from the browser", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Email").fill(process.env.E2E_ADMIN_EMAIL ?? "");
  await page.getByLabel("Password").fill(password);
  await page.getByRole("button", { name: "Login" }).click();

  await expect(page.getByRole("heading", { name: "Company Master" })).toBeVisible();
  await page.getByRole("button", { name: "Role Master" }).click();
  await expect(page.getByRole("heading", { name: "Role Master" })).toBeVisible();

  await page.getByLabel("Role Name").fill("E2E Cashier");
  await page.getByRole("button", { name: "Add Role" }).click();
  const row = page.getByRole("row").filter({ hasText: "E2E Cashier" });
  await expect(row).toBeVisible();

  await row.getByRole("button", { name: "Edit" }).click();
  await page.getByLabel("Role Name").fill("E2E Senior Cashier");
  await page.getByRole("button", { name: "Save Changes" }).click();
  const renamed = page.getByRole("row").filter({ hasText: "E2E Senior Cashier" });
  await expect(renamed).toBeVisible();

  page.once("dialog", (dialog) => dialog.accept());
  await renamed.getByRole("button", { name: "Delete" }).click();
  await expect(renamed).toHaveCount(0);

  await page.getByRole("button", { name: "Logout" }).click();
  await expect(page.getByRole("button", { name: "Login" })).toBeVisible();
});

test("ordinary employee cannot access management screens", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Email").fill(process.env.E2E_EMPLOYEE_EMAIL ?? "");
  await page.getByLabel("Password").fill(password);
  await page.getByRole("button", { name: "Login" }).click();

  await expect(page.getByRole("heading", { name: "Company Master" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Role Master" })).toHaveCount(0);
  await expect(page.getByRole("button", { name: "Save Company" })).toHaveCount(0);
});


test("admin company bilingual create/delete and role duplicate validation", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Email").fill(process.env.E2E_ADMIN_EMAIL ?? "");
  await page.getByLabel("Password").fill(password);
  await page.getByRole("button", { name: "Login" }).click();

  await page.getByLabel("Company Name (English)").fill("ERP Browser Shop");
  await page.getByLabel("اسم الشركة").fill("شركة اختبار");
  await page.getByRole("button", { name: "Save Company" }).click();

  const company = page.getByRole("row").filter({ hasText: "ERP Browser Shop" });
  await expect(company).toContainText("شركة اختبار");

  page.once("dialog", (dialog) => dialog.accept());
  await company.getByRole("button", { name: "Delete" }).click();
  await expect(company).toHaveCount(0);

  await page.getByRole("button", { name: "Role Master" }).click();
  await page.getByLabel("Role Name").fill("Browser Duplicate Check");
  await page.getByRole("button", { name: "Add Role" }).click();
  const row = page.getByRole("row").filter({ hasText: "Browser Duplicate Check" });
  await expect(row).toBeVisible();

  await page.getByLabel("Role Name").fill("browser duplicate check");
  await page.getByRole("button", { name: "Add Role" }).click();
  await expect(page.getByRole("alert")).toHaveText("Role name already exists.");

  page.once("dialog", (dialog) => dialog.accept());
  await row.getByRole("button", { name: "Delete" }).click();
  await expect(row).toHaveCount(0);
});

test("admin navigation remains available on a narrow screen", async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto("/");
  await page.getByLabel("Email").fill(process.env.E2E_ADMIN_EMAIL ?? "");
  await page.getByLabel("Password").fill(password);
  await page.getByRole("button", { name: "Login" }).click();

  await expect(page.getByRole("button", { name: "Role Master" })).toBeVisible();
  await page.getByRole("button", { name: "Role Master" }).click();
  await expect(page.getByRole("heading", { name: "Role Master" })).toBeVisible();
});

test("admin can use Enter to navigate Login and Company forms", async ({ page }) => {
  await page.goto("/");
  const email = page.getByLabel("Email");
  const passwordField = page.getByLabel("Password");

  await email.fill(process.env.E2E_ADMIN_EMAIL ?? "");
  await email.press("Enter");
  await expect(passwordField).toBeFocused();

  await passwordField.fill(password);
  await passwordField.press("Enter");
  await expect(page.getByRole("checkbox", { name: "Remember me" })).toBeFocused();
  await page.getByRole("checkbox", { name: "Remember me" }).press("Enter");

  await expect(page.getByRole("heading", { name: "Company Master" })).toBeVisible();
  const english = page.getByLabel("Company Name (English)");
  const arabic = page.getByLabel("اسم الشركة");
  await english.fill("Keyboard Shop");
  await english.press("Enter");
  await expect(arabic).toBeFocused();

  await arabic.fill("متجر لوحة المفاتيح");
  await arabic.press("Enter");
  const address = page.getByLabel("Address (English)");
  await expect(address).toBeFocused();
  await address.press("Enter");
  await expect(address).toHaveValue("\n");

  await page.getByRole("button", { name: "Save Company" }).click();
  const row = page.getByRole("row").filter({ hasText: "Keyboard Shop" });
  await expect(row).toBeVisible();
  page.once("dialog", dialog => dialog.accept());
  await row.getByRole("button", { name: "Delete" }).click();
  await expect(row).toHaveCount(0);
});

test("admin can switch to Arabic with RTL navigation", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Language").selectOption("ar");
  await expect(page.locator("html")).toHaveAttribute("lang", "ar");
  await expect(page.locator("html")).toHaveAttribute("dir", "rtl");

  await page.getByLabel("البريد الإلكتروني").fill(process.env.E2E_ADMIN_EMAIL ?? "");
  await page.getByLabel("كلمة المرور").fill(password);
  await page.getByRole("button", { name: "تسجيل الدخول" }).click();
  await expect(page.getByRole("heading", { name: "بيانات الشركة" })).toBeVisible();
  await page.getByRole("button", { name: "إدارة الأدوار" }).click();
  await expect(page.getByRole("heading", { name: "إدارة الأدوار" })).toBeVisible();

  await page.getByLabel("اللغة").selectOption("en");
  await expect(page.locator("html")).toHaveAttribute("dir", "ltr");
  await expect(page.getByRole("heading", { name: "Role Master" })).toBeVisible();
});


test("admin is returned to login when the session expires", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Email").fill(process.env.E2E_ADMIN_EMAIL ?? "");
  await page.getByLabel("Password").fill(password);
  await page.getByRole("button", { name: "Login" }).click();

  await expect(page.getByRole("heading", { name: "Company Master" })).toBeVisible();
  await page.context().clearCookies();
  await page.getByRole("button", { name: "Role Master" }).click();
  await expect(page.getByRole("button", { name: "Login" })).toBeVisible();
});


test("admin is returned to login when a session expires", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Email").fill(process.env.E2E_ADMIN_EMAIL ?? "");
  await page.getByLabel("Password").fill(password);
  await page.getByRole("button", { name: "Login" }).click();
  await expect(page.getByRole("heading", { name: "Company Master" })).toBeVisible();

  await page.route("**/api/roles", (route) => route.fulfill({ status: 401, body: "" }));
  await page.getByRole("button", { name: "Role Master" }).click();
  await expect(page.getByRole("button", { name: "Login" })).toBeVisible();
});


test("admin rejects unsafe large numeric IDs from an API", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Email").fill(process.env.E2E_ADMIN_EMAIL ?? "");
  await page.getByLabel("Password").fill(password);
  await page.getByRole("button", { name: "Login" }).click();
  await expect(page.getByRole("heading", { name: "Company Master" })).toBeVisible();

  await page.route("**/api/roles", (route) => {
    if (route.request().method() !== "GET") return route.continue();
    return route.fulfill({
      status: 200,
      contentType: "application/json",
      body: '[{"id":9007199254740992,"name":"Unsafe ID"}]',
    });
  });
  await page.getByRole("button", { name: "Role Master" }).click();

  await expect(page.getByRole("alert")).toContainText("Unable to load roles.");
  await expect(page.getByRole("row").filter({ hasText: "Unsafe ID" })).toHaveCount(0);
});


test("admin assigns role permission matrix with keyboard-accessible checkboxes", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Email").fill(process.env.E2E_ADMIN_EMAIL ?? "");
  await page.getByLabel("Password").fill(password);
  await page.getByRole("button", { name: "Login" }).click();
  await page.getByRole("button", { name: "Role Master" }).click();

  await page.getByLabel("Role Name").fill("Matrix Sales");
  await page.getByRole("button", { name: "Add Role" }).click();
  const row = page.getByRole("row").filter({ hasText: "Matrix Sales" });
  await expect(row).toBeVisible();
  await row.getByRole("button", { name: "Edit" }).click();

  const grant = page.getByRole("checkbox", { name: "Sales - View" });
  await expect(grant).toBeVisible();
  await grant.focus();
  await page.keyboard.press("Space");
  await expect(grant).toBeChecked();
  await page.getByRole("button", { name: "Save Permissions" }).click();
  await expect(page.getByRole("status")).toHaveText("Permissions saved.");
  await page.getByRole("button", { name: "Cancel" }).click();
  await row.getByRole("button", { name: "Edit" }).click();
  await expect(grant).toBeChecked();

  page.once("dialog", (dialog) => dialog.accept());
  await row.getByRole("button", { name: "Delete" }).click();
  await expect(row).toHaveCount(0);
});
