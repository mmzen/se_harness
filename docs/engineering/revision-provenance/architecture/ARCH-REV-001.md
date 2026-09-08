+++
id = "ARCH-REV-001"
type = "architecture"
title = "Revision provenance architecture"
status = "implemented"
owners = ["technical-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-09-08"

[relations]
addresses = ["REQ-REV-001", "REQ-REV-002", "REQ-REV-003", "REQ-REV-004", "REQ-REV-005", "REQ-REV-006", "REQ-REV-007", "REQ-REV-008"]
conforms_to = ["SPEC-REV-001"]

[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "data-ownership-or-persistence", "cross-cutting-policy", "difficult-to-reverse"]
rationale = "ADR-REV-001 added the verification record and release record artifact types, separating reusable contracts from records that bind one clean candidate commit to evidence. Every later governance commit reads that schema and provenance boundary."
assessed_by = "technical-owner"
+++

# Architecture

Formal Markdown metadata remains the authoritative graph. Git supplies only bounded observed values through explicit CLI operations. Verification and release records are later governance artifacts referencing a prior candidate commit, avoiding self-reference.

The standard-library validator owns structural and cross-record consistency. The CLI owns safe Git observation and record preparation. The dashboard owns derived comparison and presentation. No layer creates approval, tags, commits, or release state.

## Amendment record

**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-REV-001`).** The eight
requirements of the legacy relation become `addresses`; `conforms_to` names
`SPEC-REV-001`, the active specification that specifies them. The assessment
reads the decision and consequences of `ADR-REV-001`, the one active ADR that
decides this architecture; that ADR records no enumerated alternatives, so no
alternatives trigger is claimed. Title, status, statement and ADR relations
are unchanged.
