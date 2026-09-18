import { FormEvent } from "react";
import { CompanyFormValues } from "../api/companies";

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
  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    onSubmit();
  }

  return (
    <section className="panel">
      <div className="panel-heading">
        <h2>{editing ? "Edit Company" : "Add Company"}</h2>
        {editing && (
          <button className="secondary" type="button" onClick={onCancel}>
            Cancel
          </button>
        )}
      </div>

      <form className="company-form" onSubmit={handleSubmit}>
        <TextField
          label="Company Name (English)"
          value={values.nameEn}
          onChange={(value) => onChange("nameEn", value)}
          required
        />
        <TextField
          label="اسم الشركة"
          value={values.nameAr}
          onChange={(value) => onChange("nameAr", value)}
          dir="rtl"
        />
        <TextArea
          label="Address (English)"
          value={values.addressEn}
          onChange={(value) => onChange("addressEn", value)}
        />
        <TextArea
          label="العنوان"
          value={values.addressAr}
          onChange={(value) => onChange("addressAr", value)}
          dir="rtl"
        />
        <TextField
          label="Telephone"
          value={values.telephone}
          onChange={(value) => onChange("telephone", value)}
        />
        <TextField
          label="Mobile"
          value={values.mobile}
          onChange={(value) => onChange("mobile", value)}
        />
        <TextField
          label="Email"
          value={values.email}
          onChange={(value) => onChange("email", value)}
          type="email"
        />
        <TextField
          label="Website"
          value={values.website}
          onChange={(value) => onChange("website", value)}
          type="url"
        />
        <TextField
          label="VAT / Tax Number"
          value={values.taxNumber}
          onChange={(value) => onChange("taxNumber", value)}
        />
        <TextField
          label="Commercial Registration Number"
          value={values.commercialRegistrationNumber}
          onChange={(value) => onChange("commercialRegistrationNumber", value)}
        />

        <label className="full-width">
          Company Logo
          <input
            type="file"
            accept=".jpg,.jpeg,.png,.webp"
            onChange={(event) => onChange("logo", event.target.files?.[0] ?? null)}
          />
        </label>

        <TextArea
          label="Bank Details"
          value={values.bankDetails}
          onChange={(value) => onChange("bankDetails", value)}
        />
        <TextArea
          label="Social Media"
          value={values.socialMedia}
          onChange={(value) => onChange("socialMedia", value)}
        />
        <TextArea
          label="Invoice Header"
          value={values.invoiceHeader}
          onChange={(value) => onChange("invoiceHeader", value)}
        />
        <TextArea
          label="Invoice Footer"
          value={values.invoiceFooter}
          onChange={(value) => onChange("invoiceFooter", value)}
        />
        <TextArea
          label="Terms & Conditions"
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
          Active
        </label>

        <div className="form-actions full-width">
          <button type="submit" disabled={saving}>
            {saving ? "Saving..." : editing ? "Save Changes" : "Save Company"}
          </button>
        </div>
      </form>
    </section>
  );
}
