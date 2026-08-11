+++
id = "REQ-DST-007"
type = "requirement"
title = "Load one shared contract across supported coding agents"
status = "implemented"
owners = ["product-owner", "engineering-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN the standard harness is installed, adopted, or upgraded, THE SYSTEM SHALL integrate the shared harness contract into AGENTS.md and provide a CLAUDE.md adapter that imports AGENTS.md without replacing repository-owned instructions."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Load one shared contract across supported coding agents

## Rationale

Repositories should not maintain independent copies of the same operating contract for Codex and Claude Code. A thin adapter avoids instruction drift while keeping `AGENTS.md` authoritative for shared rules.

## Required response

- Install a bounded harness fragment in root `AGENTS.md`.
- Install a bounded `CLAUDE.md` fragment containing a root-relative `@AGENTS.md` import.
- Preserve content outside the harness markers in both files.
- Verify that the resulting `CLAUDE.md` loads `AGENTS.md`.

## Boundary behavior

Malformed or duplicated managed markers fail closed. Existing repository content is never replaced as an ordinary managed file.
