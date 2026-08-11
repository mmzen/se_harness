+++
id = "REQ-IAR-001"
type = "requirement"
title = "Provide one canonical managed instruction route"
status = "implemented"
owners = ["requirements-steward", "repository-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN an engineering agent starts repository work, THE SYSTEM SHALL route the agent through one canonical managed entry contract without duplicating mandatory harness navigation across adapter files."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Provide one canonical managed instruction route

## Acceptance criteria

- The managed fragment in `AGENTS.md` names `ENGINEERING_HARNESS.md` as its only next harness document.
- The managed fragment in `CLAUDE.md` contains the standalone `@AGENTS.md` import and does not restate harness policy.
- `ENGINEERING_HARNESS.md` is the single fully managed contract and router for repository context, formal authority, workflow policy, validation, verification, and release guidance.
- The route is identical for a fresh install and an adopted repository.
- Repository-specific instructions outside the managed fragments may contain additional navigation without creating a second harness-controlled entry route.
