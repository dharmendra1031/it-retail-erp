import { FormEvent } from "react";
import { CompanyFormValues } from "../api/companies";
import { advanceOnEnter } from "../forms/keyboard";
import { useLanguage } from "../i18n";


interface Props {
  values: CompanyFormValues;
  editing: boolean;
  saving: boolean;
  onChange: <K extends keyof CompanyFormValues>(
    key: K,
    value: CompanyFormValues[K],
  ) => void;
  onSubmit: () => void;
  onCancel: () => void;
}

interface TextFieldProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: "text" | "email" | "url";
  dir?: "ltr" | "rtl";
  required?: boolean;
}

function TextField({
  label,
  value,
  onChange,
  type = "text",
  dir,
  required = false,
}: TextFieldProps) {
  return (
    <label>
      {label}
      <input
        type={type}
        dir={dir}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        required={required}
      />
    </label>
  );
}

function TextArea({
  label,
  value,
  onChange,
  dir,
  fullWidth = false,
}: TextFieldProps & { fullWidth?: boolean }) {
  return (
    <label className={fullWidth ? "full-width" : undefined}>
      {label}
      <textarea
        dir={dir}
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />
    </label>
  );
}

export function CompanyForm({
  values,
  editing,
  saving,
  onChange,
  onSubmit,
  onCancel,
}: Props) {
  const { t } = useLanguage();
  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    onSubmit();
  }

  return (
    <section className="panel">
      <div className="panel-heading">
        <h2>{editing ? t("editCompany") : t("addCompany")}</h2>
        {editing && (
          <button className="secondary" type="button" onClick={onCancel}>
            {t("cancel")}
          </button>
        )}
      </div>

      <form className="company-form" onSubmit={handleSubmit} onKeyDown={advanceOnEnter}>
        <TextField
          label={t("companyNameEnglish")}
          value={values.nameEn}
          onChange={(value) => onChange("nameEn", value)}
          required
        />
        <TextField
          label={t("companyNameArabic")}
          value={values.nameAr}
          onChange={(value) => onChange("nameAr", value)}
          dir="rtl"
        />
        <TextArea
          label={t("addressEnglish")}
          value={values.addressEn}
          onChange={(value) => onChange("addressEn", value)}
        />
        <TextArea
          label={t("addressArabic")}
          value={values.addressAr}
          onChange={(value) => onChange("addressAr", value)}
          dir="rtl"
        />
        <TextField
          label={t("telephone")}
          value={values.telephone}
          onChange={(value) => onChange("telephone", value)}
        />
        <TextField
          label={t("mobile")}
          value={values.mobile}
          onChange={(value) => onChange("mobile", value)}
        />
        <TextField
          label={t("email")}
          value={values.email}
          onChange={(value) => onChange("email", value)}
          type="email"
        />
        <TextField
          label={t("website")}
          value={values.website}
          onChange={(value) => onChange("website", value)}
          type="url"
        />
        <TextField
          label={t("taxNumber")}
          value={values.taxNumber}
          onChange={(value) => onChange("taxNumber", value)}
        />
        <TextField
          label={t("commercialRegistration")}
          value={values.commercialRegistrationNumber}
          onChange={(value) => onChange("commercialRegistrationNumber", value)}
        />

        <label className="full-width">
          {t("companyLogo")}
          <input
            type="file"
            accept=".jpg,.jpeg,.png,.webp"
            onChange={(event) => onChange("logo", event.target.files?.[0] ?? null)}
          />
        </label>

        <TextArea
          label={t("bankDetails")}
          value={values.bankDetails}
          onChange={(value) => onChange("bankDetails", value)}
        />
        <TextArea
          label={t("socialMedia")}
          value={values.socialMedia}
          onChange={(value) => onChange("socialMedia", value)}
        />
        <TextArea
          label={t("invoiceHeader")}
          value={values.invoiceHeader}
          onChange={(value) => onChange("invoiceHeader", value)}
        />
        <TextArea
          label={t("invoiceFooter")}
          value={values.invoiceFooter}
          onChange={(value) => onChange("invoiceFooter", value)}
        />
        <TextArea
          label={t("terms")}
          value={values.termsAndConditions}
          onChange={(value) => onChange("termsAndConditions", value)}
          fullWidth
        />

        <label className="checkbox full-width">
          <input
            type="checkbox"
            checked={values.isActive}
            onChange={(event) => onChange("isActive", event.target.checked)}
          />
          {t("active")}
        </label>

        <div className="form-actions full-width">
          <button type="submit" disabled={saving}>
            {saving ? t("saving") : editing ? t("saveChanges") : t("saveCompany")}
          </button>
        </div>
      </form>
    </section>
  );
}
