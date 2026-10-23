export type Locale = "en" | "ar";

const arabicModules: Record<string, string> = {
  companies: "الشركات", roles: "الأدوار", users: "المستخدمون",
  branches: "الفروع", warehouses: "المستودعات",
  quotations: "عروض الأسعار", sales: "المبيعات", purchases: "المشتريات",
  inventory: "المخزون", services: "الخدمات", reports: "التقارير",
};
const arabicActions: Record<string, string> = {
  view: "عرض", add: "إضافة", edit: "تعديل", delete: "حذف",
  print: "طباعة", export: "تصدير", approve: "اعتماد", cancel: "إلغاء",
  post: "ترحيل", reverse: "عكس القيد",
};

export function permissionLabel(code: string, fallback: string, language: Locale) {
  if (language === "en") return fallback;
  const [module, action] = code.split(".");
  const moduleLabel = arabicModules[module];
  const actionLabel = arabicActions[action];
  return moduleLabel && actionLabel ? `${moduleLabel} - ${actionLabel}` : fallback;
}

export function formatLocalDate(value: Date, language: Locale) {
  return new Intl.DateTimeFormat(language === "ar" ? "ar-KW" : "en-GB", {
    year: "numeric", month: "short", day: "numeric",
  }).format(value);
}

export function formatMoney(value: number, currency: string, language: Locale) {
  if (!Number.isFinite(value)) throw new RangeError("Amount must be finite.");
  return new Intl.NumberFormat(language === "ar" ? "ar-KW" : "en-GB", {
    style: "currency", currency,
  }).format(value);
}
