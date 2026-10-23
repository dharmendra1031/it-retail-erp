# WP10 — Company Master / logo lifecycle

Company English and Arabic fields and existing numeric identifiers remain unchanged.

- Max upload 2 MiB, extensions JPG/PNG/WebP, MIME match and actual image signature/decodability.
- ASP.NET writes to a uniquely named logo file using cryptographic randomness; company insert and logo database updates occur in a transaction, and failed transactions remove the newly written file. Old file is removed only after a successful replacement.
- Django uses Pillow verify and `transaction.atomic` on insert/update, deleting newly saved media on transaction failure and old media after successful replacement.
- Both APIs block deleting a Company referenced by Branch (409). Admin/permission authorization and CSRF remain server enforced.
- Full invoice/quotation/report document printing is owned by WP44. A bilingual Company identity browser print preview can be provided in WP10; it must not be called completed invoice printing.
