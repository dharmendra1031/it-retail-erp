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
