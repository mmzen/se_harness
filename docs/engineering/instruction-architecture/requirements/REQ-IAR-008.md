+++
id = "REQ-IAR-008"
type = "requirement"
title = "Migrate new and existing repositories safely"
status = "implemented"
owners = ["requirements-steward", "engineering-owner", "repository-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN the instruction architecture is installed or upgraded, THE SYSTEM SHALL apply deterministic ownership-mode migrations without overwriting customized, ambiguous, or repository-owned content."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Migrate new and existing repositories safely

## Acceptance criteria

- Fresh installation and adoption use the same single standard installation contract; no instruction profile is introduced.
- Existing `AGENTS.md` and `CLAUDE.md` content is preserved while a missing well-formed managed fragment is added once.
- An exact or canonical old managed `docs/engineering/README.md` may be replaced with the new seed and then relinquished to owner control in one recorded mode transition.
- A customized, missing, malformed, or ambiguous file is preserved and reported for manual reconciliation; its lock mode is not silently changed.
- Self-hosting files and lock entries are reconciled through the supported upgrade mechanism, not by hand-editing digests.
- Dry-run and apply produce deterministic plans, and repeated successful application is idempotent.
- A failed plan leaves the repository unchanged.
