+++
id = "REQ-IAR-002"
type = "requirement"
title = "Preserve and bound repository-owner instructions"
status = "implemented"
owners = ["requirements-steward", "repository-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN the harness is installed or upgraded in a repository with existing agent instructions, THE SYSTEM SHALL preserve owner-controlled content while retaining a structurally intact, non-waivable managed harness gate."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Preserve and bound repository-owner instructions

## Acceptance criteria

- Existing content outside the managed markers in `AGENTS.md` and `CLAUDE.md` remains unchanged during adoption and safe upgrade.
- Repository owners may add stricter controls, repository commands, review rules, and specialized paths outside managed markers.
- Owner instructions cannot waive an approved work-order boundary, formal validation, retained evidence, decision rights, commit-bound provenance, or release controls.
- Missing, duplicated, reordered, nested, or malformed managed markers fail closed without overwriting the file.
- Because semantic conflict detection is not reliable, the contract requires human escalation when owner prose appears to conflict with the managed gate.
