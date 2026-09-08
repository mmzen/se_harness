+++
id = "ARCH-DST-001"
type = "architecture"
title = "Repository-native distribution architecture"
status = "implemented"
owners = ["technical-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-09-08"

[relations]
addresses = ["REQ-DST-001", "REQ-DST-002", "REQ-DST-003", "REQ-DST-004", "REQ-DST-005", "REQ-DST-006"]
conforms_to = ["SPEC-DST-001"]

[decision_assessment]
outcome = "adr_required"
triggers = ["system-boundary", "data-ownership-or-persistence", "difficult-to-reverse", "material-alternatives"]
rationale = "ADR-DST-001 chose one canonical template with hash-based ownership over minimal and offline installation modes. It fixed the distribution boundary, what the lock persists about tool-owned content, and an ownership model installed repositories cannot cheaply leave."
assessed_by = "technical-owner"
+++

# Architecture

The system has three boundaries: a standard-library Python control plane in `se_harness/`, an immutable canonical template in `templates/repository/standard/`, and repository-local installed files owned by each target. The lock records provenance but never makes the distribution repository authoritative for target product intent.

Writes are contained below an explicitly resolved target and use same-directory temporary replacement. External services, credentials, code execution inferred from repository content, and installation profiles are outside the architecture.

## Amendment record

**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-DST-001`).** The six
requirements of the legacy relation become `addresses`; `conforms_to` names
`SPEC-DST-001`, the active specification that specifies them. The assessment
reads the decision and consequences of `ADR-DST-001`, the one active ADR that
decides this architecture. Title, status, statement and ADR relations are
unchanged.
