import { createContext, ReactNode, useContext, useEffect, useState } from "react";

const en = {
  language: "Language", login: "Login", logout: "Logout", email: "Email",
  password: "Password", remember: "Remember me", signingIn: "Signing in...",
  signInPrompt: "Sign in to continue", invalidLogin: "Invalid email or password.",
  companyMaster: "Company Master", roleMaster: "Role Master", masters: "Masters",
  companyDescription: "Manage company identity, tax and invoice information.",
  addCompany: "Add Company", editCompany: "Edit Company", saveCompany: "Save Company",
  saveChanges: "Save Changes", saving: "Saving...", cancel: "Cancel",
  nameEn: "Company Name (English)", nameAr: "اسم الشركة",
  addressEn: "Address (English)", addressAr: "العنوان",
  telephone: "Telephone", mobile: "Mobile", website: "Website",
  taxNumber: "VAT / Tax Number", registration: "Commercial Registration Number",
  logo: "Company Logo", bank: "Bank Details", social: "Social Media",
  invoiceHeader: "Invoice Header", invoiceFooter: "Invoice Footer",
  terms: "Terms & Conditions", active: "Active", inactive: "Inactive",
  companies: "Companies", company: "Company", arabicName: "Arabic Name",
  taxNo: "Tax No.", status: "Status", actions: "Actions",
  searchCompanies: "Search companies...", noCompanies: "No companies found.",
  edit: "Edit", delete: "Delete", unableLoadCompanies: "Unable to load companies.",
  unableSaveCompany: "Unable to save company.", unableDeleteCompany: "Unable to delete company.",
  roleDescription: "Manage user roles. Assigned roles cannot be deleted.",
  addRole: "Add Role", editRole: "Edit Role", roleName: "Role Name",
  rolePlaceholder: "e.g. Sales Manager", roles: "Roles",
  noRoles: "No roles available.", unableLoadRoles: "Unable to load roles.",
  unableSaveRole: "Unable to save role.", unableDeleteRole: "Unable to delete role.",
  duplicateRole: "Role name already exists.", invalidRequest: "Invalid request.",
  assignedRole: "Role is assigned to users.", confirmDelete: "Delete",
} as const;

type Key = keyof typeof en;
const ar: Record<Key, string> = {
  language: "اللغة", login: "تسجيل الدخول", logout: "تسجيل الخروج",
  email: "البريد الإلكتروني", password: "كلمة المرور", remember: "تذكرني",
  signingIn: "جارٍ تسجيل الدخول...", signInPrompt: "سجّل الدخول للمتابعة",
  invalidLogin: "البريد الإلكتروني أو كلمة المرور غير صحيحة.",
  companyMaster: "بيانات الشركة", roleMaster: "إدارة الأدوار", masters: "البيانات الأساسية",
  companyDescription: "إدارة بيانات الشركة والضرائب والفواتير.",
  addCompany: "إضافة شركة", editCompany: "تعديل الشركة", saveCompany: "حفظ الشركة",
  saveChanges: "حفظ التغييرات", saving: "جارٍ الحفظ...", cancel: "إلغاء",
  nameEn: "اسم الشركة (بالإنجليزية)", nameAr: "اسم الشركة",
  addressEn: "العنوان (بالإنجليزية)", addressAr: "العنوان",
  telephone: "الهاتف", mobile: "الجوال", website: "الموقع الإلكتروني",
  taxNumber: "الرقم الضريبي", registration: "رقم السجل التجاري",
  logo: "شعار الشركة", bank: "البيانات البنكية", social: "وسائل التواصل",
  invoiceHeader: "ترويسة الفاتورة", invoiceFooter: "تذييل الفاتورة",
  terms: "الشروط والأحكام", active: "نشط", inactive: "غير نشط",
  companies: "الشركات", company: "الشركة", arabicName: "الاسم العربي",
  taxNo: "الرقم الضريبي", status: "الحالة", actions: "الإجراءات",
  searchCompanies: "البحث عن الشركات...", noCompanies: "لا توجد شركات.",
  edit: "تعديل", delete: "حذف", unableLoadCompanies: "تعذر تحميل الشركات.",
  unableSaveCompany: "تعذر حفظ الشركة.", unableDeleteCompany: "تعذر حذف الشركة.",
  roleDescription: "إدارة أدوار المستخدمين. لا يمكن حذف الأدوار المرتبطة بمستخدمين.",
  addRole: "إضافة دور", editRole: "تعديل الدور", roleName: "اسم الدور",
  rolePlaceholder: "مثلاً: مدير المبيعات", roles: "الأدوار",
  noRoles: "لا توجد أدوار.", unableLoadRoles: "تعذر تحميل الأدوار.",
  unableSaveRole: "تعذر حفظ الدور.", unableDeleteRole: "تعذر حذف الدور.",
  duplicateRole: "اسم الدور موجود بالفعل.", invalidRequest: "طلب غير صالح.",
  assignedRole: "الدور مرتبط بمستخدمين.", confirmDelete: "حذف",
};

type Language = "en" | "ar";
interface Locale {
  language: Language;
  setLanguage: (language: Language) => void;
  t: (key: Key) => string;
  error: (value: unknown, fallback: Key) => string;
}

const Context = createContext<Locale | null>(null);
const errorKeys: Record<string, Key> = {
  "Role name already exists.": "duplicateRole",
  "Invalid request.": "invalidRequest",
  "Role is assigned to users.": "assignedRole",
};

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguage] = useState<Language>(
    () => localStorage.getItem("erp.language") === "ar" ? "ar" : "en",
  );

  useEffect(() => {
    document.documentElement.lang = language;
    document.documentElement.dir = language === "ar" ? "rtl" : "ltr";
    localStorage.setItem("erp.language", language);
  }, [language]);

  const t = (key: Key) => (language === "ar" ? ar[key] : en[key]);
  const error = (value: unknown, fallback: Key) => {
    const text = value instanceof Error ? value.message : "";
    return t(errorKeys[text] ?? fallback);
  };

  return (
    <Context.Provider value={{ language, setLanguage, t, error }}>
      {children}
    </Context.Provider>
  );
}

export function useLanguage() {
  const context = useContext(Context);
  if (!context) {
    throw new Error("LanguageProvider is missing.");
  }
  return context;
}
