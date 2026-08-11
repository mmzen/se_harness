+++
id = "REQ-WLC-005"
type = "requirement"
title = "Distribute identical lifecycle semantics"
status = "implemented"
owners = ["requirements-steward", "engineering-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN the standard harness is initialized or safely upgraded, THE SYSTEM SHALL install lifecycle documentation, templates, validation, and Explorer behavior equivalent to the distribution repository."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-WLC-001"]
+++

# Requirement: Distribute identical lifecycle semantics

## Acceptance criteria

- Canonical and root validator scripts are identical.
- Canonical and root Explorer generator scripts are identical.
- Canonical workflow and work-order template contain the same lifecycle rules as the self-installed repository.
- Managed integrity and fresh-install tests pass.
