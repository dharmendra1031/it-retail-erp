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
  await page.getByLabel("اسم الشركة (بالإنجليزية)").fill("Arabic Buttons Shop");
  await page.getByRole("button", { name: "حفظ الشركة" }).click();
  const companyRow = page.getByRole("row").filter({ hasText: "Arabic Buttons Shop" });
  await expect(companyRow.getByRole("button", { name: "تعديل" })).toBeVisible();
  page.once("dialog", dialog => dialog.accept());
  await companyRow.getByRole("button", { name: "حذف" }).click();
  await expect(companyRow).toHaveCount(0);
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


test("admin creates and deactivates an employee from keyboard-friendly User Master", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Email").fill(process.env.E2E_ADMIN_EMAIL ?? "");
  await page.getByLabel("Password").fill(password);
  await page.getByRole("button", { name: "Login" }).click();

  await page.getByRole("button", { name: "User Master" }).click();
  await expect(page.getByRole("heading", { name: "User Master" })).toBeVisible();
  const username = page.getByLabel("Username");
  await username.fill("browseremployee");
  await username.press("Enter");
  await expect(page.getByLabel("Full Name")).toBeFocused();
  await page.getByLabel("Full Name").fill("Browser Employee");
  await page.getByLabel("Email").last().fill("browseremployee@example.test");
  await page.getByLabel("Password").last().fill("StrongBrowserPass123!");
  await page.getByRole("button", { name: "Save User" }).click();
  const row = page.getByRole("row").filter({ hasText: "browseremployee" });
  await expect(row).toBeVisible();
  await row.getByRole("button", { name: "Edit" }).click();
  await page.getByRole("checkbox", { name: "Active" }).uncheck();
  await page.getByRole("button", { name: "Save User" }).click();
  await expect(row).toContainText("Inactive");
});


test("admin creates a branch and warehouse for a company", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Email").fill(process.env.E2E_ADMIN_EMAIL ?? "");
  await page.getByLabel("Password").fill(password);
  await page.getByRole("button", { name: "Login" }).click();

  await page.getByLabel("Company Name (English)").fill("Organization Test Company");
  await page.getByRole("button", { name: "Save Company" }).click();
  await page.getByRole("button", { name: "Branches & Warehouses" }).click();
  await expect(page.getByRole("heading", { name: "Branches & Warehouses" })).toBeVisible();
  const forms = page.locator(".company-form");
  await forms.first().locator("select").first().selectOption({ label: "Organization Test Company" });
  await forms.first().getByLabel("Code").fill(`HQ-${Date.now().toString(36)}`);
  await forms.first().getByLabel("Company Name (English)").fill("Head Office");
  await forms.first().getByRole("button", { name: "Save Branch" }).click();

  await forms.nth(1).locator("select").first().selectOption({ label: "Head Office" });
  await forms.nth(1).getByLabel("Code").fill(`MAIN-${Date.now().toString(36)}`);
  await forms.nth(1).getByLabel("Company Name (English)").fill("Main Store");
  await forms.nth(1).getByRole("button", { name: "Save Warehouse" }).click();
  await expect(page.getByRole("row").filter({ hasText: "Main Store" })).toBeVisible();
});

test("admin previews bilingual Company identity for printing", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Email").fill(process.env.E2E_ADMIN_EMAIL ?? "");
  await page.getByLabel("Password").fill(password);
  await page.getByRole("button", { name: "Login" }).click();
  await page.getByLabel("Company Name (English)").fill("Print Company");
  await page.getByLabel("اسم الشركة").fill("شركة للطباعة");
  await page.getByRole("button", { name: "Save Company" }).click();
  await page.evaluate(() => { window.print = () => {}; });
  const row = page.getByRole("row").filter({ hasText: "Print Company" });
  await row.getByRole("button", { name: "Print Identity" }).click();
  await expect(page.getByRole("region", { name: "Print Identity" })).toContainText("شركة للطباعة");
});


test("Arabic permission actions and print date use the selected locale", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Language").selectOption("ar");
  await page.getByLabel("البريد الإلكتروني").fill(process.env.E2E_ADMIN_EMAIL ?? "");
  await page.getByLabel("كلمة المرور").fill(password);
  await page.getByRole("button", { name: "تسجيل الدخول" }).click();

  await page.getByRole("button", { name: "إدارة الأدوار" }).click();
  await page.getByLabel("اسم الدور").fill("Arabic Matrix");
  await page.getByRole("button", { name: "إضافة دور" }).click();
  const row = page.getByRole("row").filter({ hasText: "Arabic Matrix" });
  await row.getByRole("button", { name: "تعديل" }).click();
  await expect(page.getByRole("checkbox", { name: "المبيعات - عرض" })).toBeVisible();
  await expect(page.getByRole("checkbox", { name: "العملاء - عرض" })).toBeVisible();
  await expect(page.getByRole("checkbox", { name: "الموردون - إضافة" })).toBeVisible();
  await expect(page.getByRole("checkbox", { name: "الفئات - تعديل" })).toBeVisible();
  await page.getByRole("button", { name: "إلغاء" }).click();
  page.once("dialog", dialog => dialog.accept());
  await row.getByRole("button", { name: "حذف" }).click();

  await page.getByRole("button", { name: "بيانات الشركة" }).click();
  await page.getByLabel("اسم الشركة (بالإنجليزية)").fill("Locale Preview Company");
  await page.getByRole("textbox", { name: "اسم الشركة", exact: true }).fill("شركة عربية");
  await page.getByRole("button", { name: "حفظ الشركة" }).click();
  const company = page.getByRole("row").filter({ hasText: "Locale Preview Company" });
  await page.evaluate(() => { window.print = () => {}; });
  await company.getByRole("button", { name: "طباعة بيانات الشركة" }).click();
  await expect(page.getByRole("region", { name: "طباعة بيانات الشركة" })).toContainText("تاريخ الطباعة");
});


test("admin uses keyboard to create bilingual credit customer and supplier", async ({ page }) => {
  const suffix = Date.now().toString(36);
  await page.goto("/");
  await page.getByLabel("Email").fill(process.env.E2E_ADMIN_EMAIL ?? "");
  await page.getByLabel("Password").fill(password);
  await page.getByRole("button", { name: "Login" }).click();

  await page.getByRole("button", { name: "Customer Master" }).click();
  await page.getByLabel("Code").fill(`C-${suffix}`);
  await page.getByLabel("Code").press("Enter");
  await expect(page.getByLabel("Customer Name (English)")).toBeFocused();
  await page.getByLabel("Customer Name (English)").fill("Credit Partner");
  await page.getByLabel("Customer Name (Arabic)").fill("عميل تجريبي");
  await page.getByLabel("Credit Limit").fill("2500.750");
  await page.getByLabel("Company Name", { exact: true }).fill("Credit Shop LLC");
  await page.getByLabel("Mobile").fill("96599887766");
  await page.getByLabel("Contact Person").fill("Ali");
  await page.getByLabel("Opening Balance").fill("15.250");
  await page.getByLabel("Payment Terms (days)").fill("30");
  const customerForm = page.locator("form.company-form");
  const invalidFields = await customerForm.evaluate((form: HTMLFormElement) =>
    Array.from(form.elements).filter((element): element is HTMLInputElement =>
      element instanceof HTMLInputElement && !element.checkValidity(),
    ).map(element => ({ name: element.name, value: element.value,
      reason: element.validationMessage })),
  );
  expect(invalidFields, "Customer form has invalid fields").toEqual([]);
  const customerRequest = page.waitForResponse(response =>
    response.url().endsWith("/api/customers") && response.request().method() === "POST",
  );
  await page.getByRole("button", { name: "Save" }).click();
  const customerResponse = await customerRequest;
  expect(customerResponse.status(),
    `Customer payload: ${customerResponse.request().postData()} | Response: ${await customerResponse.text()}`,
  ).toBe(201);
  await expect(page.getByRole("row").filter({ hasText: `C-${suffix}` })).toContainText("عميل تجريبي");

  await page.getByRole("button", { name: "Supplier Master" }).click();
  await expect(page.getByRole("heading", { name: "Supplier Master" })).toBeVisible();
  await page.getByLabel("Code").fill(`S-${suffix}`);
  await page.getByLabel("Supplier Name (English)").fill("First Supplier");
  await page.getByLabel("Opening Balance").fill("135.500");
  await page.getByLabel("Credit Limit").fill("800.500");
  await page.getByLabel("Contact Person").fill("Omar");

  const supplierForm = page.locator("form.company-form");
  expect(await supplierForm.evaluate((form: HTMLFormElement) => form.checkValidity())).toBe(true);
  const supplierRequest = page.waitForResponse(response =>
    response.url().endsWith("/api/suppliers") &&
    response.request().method() === "POST",
  );
  await page.getByRole("button", { name: "Save" }).click();
  const supplierResponse = await supplierRequest;
  expect(supplierResponse.status(), `Supplier payload: ${supplierResponse.request().postData()} | Response: ${await supplierResponse.text()}`).toBe(201);
  await expect(page.getByRole("row").filter({ hasText: `S-${suffix}` })).toContainText("First Supplier");
});


test("admin manages bilingual category hierarchy brand and unit", async ({ page }) => {
  const suffix = Date.now().toString(36);
  await page.goto("/");
  await page.getByLabel("Email").fill(process.env.E2E_ADMIN_EMAIL ?? "");
  await page.getByLabel("Password").fill(password);
  await page.getByRole("button", { name: "Login" }).click();

  await page.getByRole("button", { name: "Category Master" }).click();
  await page.getByLabel("Code").fill(`COMP-${suffix}`);
  await page.getByLabel("Category Name (English)").fill("Computers");
  await page.getByLabel("Category Name (Arabic)").fill("الحواسيب");
  await page.getByRole("button", { name: "Save" }).click();
  await expect(page.getByRole("row").filter({ hasText: `COMP-${suffix}` })).toBeVisible();
  await page.getByLabel("Code").fill(`LAP-${suffix}`);
  await page.getByLabel("Category Name (English)").fill("Laptops");
  await page.getByLabel("Parent Category").selectOption({ label: "Computers" });
  await page.getByRole("button", { name: "Save" }).click();
  await expect(page.getByRole("row").filter({ hasText: `LAP-${suffix}` })).toContainText("Computers");
  await expect(page.getByRole("row").filter({ hasText: `COMP-${suffix}` })).toBeVisible();
  const child = page.getByRole("row").filter({ hasText: `LAP-${suffix}` });
  const childId = await child.locator("td").first().innerText();
  const root = page.getByRole("row").filter({ hasText: `COMP-${suffix}` });
  await root.getByRole("button", { name: "Edit" }).click();
  await expect(page.getByLabel("Parent Category").locator(`option[value="${childId}"]`)).toHaveCount(0);
  await page.getByRole("button", { name: "Cancel" }).click();
  await page.getByRole("button", { name: "Brand Master" }).click();
  await page.getByLabel("Code").fill(`DELL-${suffix}`);
  await page.getByLabel("Brand Name (English)").fill("Dell");
  await page.getByRole("button", { name: "Save" }).click();
  await expect(page.getByRole("row").filter({ hasText: `DELL-${suffix}` })).toBeVisible();

  await page.getByRole("button", { name: "Unit Master" }).click();
  await page.getByLabel("Code").fill(`PCS-${suffix}`);
  await page.getByLabel("Unit Name (English)").fill("Pieces");
  await page.getByLabel("Decimal Places").fill("0");
  await page.getByRole("button", { name: "Save" }).click();
  const unitRow = page.getByRole("row").filter({ hasText: `PCS-${suffix}` });
  await expect(unitRow).toBeVisible();
  await unitRow.getByRole("button", { name: "Edit" }).click();
  await page.getByLabel("Unit Name (English)").fill("Pieces updated");
  await page.getByRole("button", { name: "Save" }).click();
  await expect(unitRow).toContainText("Pieces updated");
});

test("Arabic category hierarchy shows localized parent labels", async ({ page }) => {
  const suffix = Date.now().toString(36);
  await page.goto("/");
  await page.getByLabel("Email").fill(process.env.E2E_ADMIN_EMAIL ?? "");
  await page.getByLabel("Password").fill(password);
  await page.getByRole("button", { name: "Login" }).click();

  await page.getByRole("button", { name: "Category Master" }).click();
  await page.getByLabel("Code").fill(`ROOT-${suffix}`);
  await page.getByLabel("Category Name (English)").fill("Laptops");
  await page.getByLabel("Category Name (Arabic)").fill("أجهزة محمولة");
  await page.getByRole("button", { name: "Save" }).click();
  await expect(page.getByRole("row").filter({ hasText: `ROOT-${suffix}` })).toBeVisible();

  await page.getByLabel("Code").fill(`CHILD-${suffix}`);
  await page.getByLabel("Category Name (English)").fill("Ultrabooks");
  await page.getByLabel("Parent Category").selectOption({ label: "Laptops" });
  await page.getByRole("button", { name: "Save" }).click();
  await expect(page.getByRole("row").filter({ hasText: `CHILD-${suffix}` })).toContainText("Laptops");

  await page.getByLabel("Language").selectOption("ar");
  await expect(page.locator("html")).toHaveAttribute("dir", "rtl");
  await expect(page.getByLabel("الفئة الأساسية").getByRole("option", { name: "أجهزة محمولة" })).toHaveCount(1);
  await expect(page.getByRole("row").filter({ hasText: `CHILD-${suffix}` })).toContainText("أجهزة محمولة");
  await expect(page.getByLabel("اسم الفئة")).toHaveAttribute("dir", "rtl");
  await expect(page.getByLabel("اسم الفئة (بالإنجليزية)")).toHaveAttribute("dir", "ltr");
});

test("Arabic form errors remain localized for field validation failures", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Language").selectOption("ar");
  await page.getByLabel("البريد الإلكتروني").fill(process.env.E2E_ADMIN_EMAIL ?? "");
  await page.getByLabel("كلمة المرور").fill(password);
  await page.getByRole("button", { name: "تسجيل الدخول" }).click();
  await expect(page.getByRole("heading", { name: "بيانات الشركة" })).toBeVisible();

  await page.route("**/api/companies", async route => {
    if (route.request().method() !== "POST") {
      await route.continue();
      return;
    }

    await route.fulfill({
      status: 400,
      contentType: "application/json",
      body: JSON.stringify({ nameEn: ["This field may not be blank."] }),
    });
  });
  await page.getByLabel("اسم الشركة (بالإنجليزية)").fill("Invalid Arabic Entry");
  await page.getByRole("button", { name: "حفظ الشركة" }).click();
  await expect(page.getByRole("alert")).toContainText("البيانات المدخلة غير صحيحة.");
});

test("Arabic master forms preserve LTR codes and RTL names", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Language").selectOption("ar");
  await page.getByLabel("البريد الإلكتروني").fill(process.env.E2E_ADMIN_EMAIL ?? "");
  await page.getByLabel("كلمة المرور").fill(password);
  await page.getByRole("button", { name: "تسجيل الدخول" }).click();
  await expect(page.getByLabel("اسم الشركة (بالإنجليزية)")).toHaveAttribute("dir", "ltr");
  await expect(page.getByLabel("اسم الشركة", { exact: true })).toHaveAttribute("dir", "rtl");

  await page.getByRole("button", { name: "إدارة العملاء" }).click();
  await expect(page.getByLabel("الرمز")).toHaveAttribute("dir", "ltr");
  await expect(page.getByLabel("البريد الإلكتروني")).toHaveAttribute("dir", "ltr");
  await expect(page.getByLabel("اسم العميل", { exact: true })).toHaveAttribute("dir", "rtl");

  await page.getByRole("button", { name: "إدارة الموردين" }).click();
  await expect(page.getByLabel("اسم المورد (بالإنجليزية)")).toHaveAttribute("dir", "ltr");
  await expect(page.getByLabel("اسم المورد", { exact: true })).toHaveAttribute("dir", "rtl");
  await expect(page.getByLabel("الرمز")).toHaveAttribute("dir", "ltr");
  await expect(page.getByLabel("العنوان (بالإنجليزية)")).toHaveAttribute("dir", "ltr");
});

test("RTL tablet layout keeps keyboard fields accessible", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Language").selectOption("ar");
  await page.getByLabel("البريد الإلكتروني").fill(process.env.E2E_ADMIN_EMAIL ?? "");
  await page.getByLabel("كلمة المرور").fill(password);
  await page.getByRole("button", { name: "تسجيل الدخول" }).click();
  await expect(page.getByRole("heading", { name: "بيانات الشركة" })).toBeVisible();

  for (const width of [768, 1024]) {
    await page.setViewportSize({ width, height: 800 });
    await expect(page.locator("html")).toHaveAttribute("dir", "rtl");
    await expect(page.getByLabel("اسم الشركة", { exact: true })).toHaveAttribute("dir", "rtl");
    await expect(page.getByLabel("اسم الشركة (بالإنجليزية)")).toHaveAttribute("dir", "ltr");
    const viewportOverflow = await page.evaluate(() =>
      document.documentElement.scrollWidth > window.innerWidth
    );
    expect(viewportOverflow, `Horizontal clipping at ${width}px`).toBe(false);
  }

  await page.getByLabel("اسم الشركة (بالإنجليزية)").focus();
  await page.keyboard.press("Tab");
  await expect(page.getByLabel("اسم الشركة", { exact: true })).toBeFocused();
});
