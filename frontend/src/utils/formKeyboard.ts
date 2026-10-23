import type { KeyboardEvent } from "react";

export function handleFormEnter(event: KeyboardEvent<HTMLFormElement>) {
  if (event.key !== "Enter" || event.shiftKey || event.ctrlKey || event.altKey ||
      event.metaKey || event.nativeEvent.isComposing) {
    return;
  }

  const target = event.target;
  if (!(target instanceof HTMLInputElement) ||
      ["file", "hidden", "submit", "button"].includes(target.type)) {
    return;
  }

  const form = event.currentTarget;
  const fields = Array.from(
    form.querySelectorAll<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>(
      "input, select, textarea",
    ),
  ).filter((field) =>
    !field.disabled && !field.readOnly &&
    field.type !== "hidden" && field.getClientRects().length > 0,
  );

  const index = fields.indexOf(target);
  if (index < 0) {
    return;
  }

  event.preventDefault();
  if (fields[index + 1]) {
    fields[index + 1].focus();
  } else {
    form.requestSubmit();
  }
}
