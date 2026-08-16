+++
id = "OPS-DST-001"
type = "operating_contract"
title = "Maintain the standard harness distribution"
status = "approved"
owners = ["service-owner", "engineering-owner"]
created = "2026-08-11"
updated = "2026-08-16"

[relations]
assures = ["REQ-DST-001", "REQ-DST-002", "REQ-DST-003", "REQ-DST-004", "REQ-DST-005", "REQ-DST-006"]
+++

# Operating Contract

Every distribution change must preserve the single-template invariant, schema compatibility or an explicit migration, safe-write boundaries, target customization preservation, deterministic tests, and current verification evidence. Template changes require an upgrade classification test.
