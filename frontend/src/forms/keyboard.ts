import { KeyboardEvent } from "react";

export function advanceOnEnter(event: KeyboardEvent<HTMLFormElement>) {
  if (event.key !== "Enter" || event.nativeEvent.isComposing ||
      event.shiftKey || event.ctrlKey || event.altKey || event.metaKey) {
    return;
  }

  const target = event.target;
  if (!(target instanceof HTMLInputElement || target instanceof HTMLSelectElement)) {
    return;
  }
  if (target instanceof HTMLInputElement &&
      ["file", "submit", "button", "reset"].includes(target.type)) {
    return;
  }

  const form = event.currentTarget;
  const fields = Array.from(form.querySelectorAll<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>(
    "input, textarea, select",
  )).filter((field) =>
    !field.disabled && !("readOnly" in field && field.readOnly) &&
    !["hidden", "file", "submit", "button", "reset"].includes(field.type) &&
    field.getClientRects().length > 0,
  );
  const index = fields.indexOf(target);
  if (index < 0) return;

  event.preventDefault();
  if (fields[index + 1]) {
    fields[index + 1].focus();
  } else {
    form.requestSubmit();
  }
}
