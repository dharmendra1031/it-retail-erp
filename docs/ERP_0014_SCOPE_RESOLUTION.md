# ERP-0014 — scope and sequencing resolution

The previous blocker correctly identified missing runtime authorization/audit behavior, but WP01 was the wrong place to require its implementation.

WP01 owns SRS traceability and delivery boundaries. Runtime ownership remains:
- WP06 Permission policies
- WP07 Role/permission assignment
- WP08 User/role membership
- WP09 Branch/warehouse access
- WP46 Security/audit hardening

ERP-0005 already specifies the required restricted-user 403/no-mutation/audit acceptance case. Therefore ERP-0014 is complete as a requirement/ownership/acceptance trace, without pretending the runtime feature exists.

**Still pending:** SRS AT-12 runtime 403/no-mutation/audit proof in the owner/integration packages.
