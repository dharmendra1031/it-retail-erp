# ERP-0016 — bilingual/RTL/formatting/accessibility/responsive verification

**Reviewed development HEAD:** `4ad84ef415b48fdf0c7e8c2c8a60b3b1c80a53ca`

## Current WP01-owned/available surface

Source inspection confirms the current Company Master carries separate English/Arabic company name and address fields through React, ASP.NET and Django. ASP.NET's SQL Server migration uses `nvarchar` for those bilingual fields. React marks the Arabic name/address inputs `dir="rtl"`. The current stylesheet collapses the two-column Company form to one column below 900px and makes tables horizontally scrollable.

These are source-level capabilities, not a browser or SQL round-trip pass.

## Deferred integration contracts

Full application language switching and page-level RTL are owned by **WP11 Localization/RTL**. Bilingual/A4/A5/thermal document rendering is owned by **WP44**. Currency/date formatting becomes testable on the transactional surfaces that introduce dates/money; WP01 traceability itself has no date/currency UI. WP49 owns full acceptance execution, including AT-10.

Required downstream contract:
- English and Arabic are first-class and Arabic data survives SQL Server round-trip unchanged.
- Arabic UI uses correct RTL layout, focus/order and readable mixed-direction values.
- Dates/currency use approved locale/KWD conventions without changing stored business values.
- Keyboard/focus/labels/error feedback remain accessible in both directions.
- Supported responsive widths do not hide required actions/data.
- Printed English, Arabic and bilingual documents preserve approved layout and Arabic shaping.

## Findings

1. PASS by source inspection — separate Company English/Arabic fields exist end-to-end.
2. PASS by source inspection — ASP.NET Company bilingual SQL columns are NVARCHAR.
3. PASS by source inspection — Arabic Company form inputs explicitly use RTL.
4. PASS by source inspection — current Company layout has a responsive breakpoint and horizontal table overflow handling.
5. DEFERRED to WP11 — global language switch, page-level RTL and localized labels/messages.
6. DEFERRED to transactional owners/WP11 — date/KWD display and parsing tests.
7. DEFERRED to WP44 — bilingual document/printing layout.
8. DEFERRED to WP49 — full browser/E2E acceptance.
9. UNVERIFIED — live SQL Server Arabic round-trip, keyboard/accessibility tooling and real-device responsive behavior; no runtime environment was executed in this step.

## Step decision

ERP-0016 is satisfied as a dependency-aware verification/specification gate. No temporary localization framework, print engine or placeholder money/date formatter is added to WP01.
