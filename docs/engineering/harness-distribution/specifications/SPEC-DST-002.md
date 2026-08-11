+++
id = "SPEC-DST-002"
type = "specification"
title = "Cross-agent instructions and repository context"
status = "implemented"
owners = ["technical-owner", "quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
specifies = ["REQ-DST-007", "REQ-DST-008"]
+++

# Specification

## Instruction integration

`CLAUDE.md.fragment` maps to root `CLAUDE.md` using the same unique harness markers and hash-based fragment ownership as `AGENTS.md.fragment`. Its managed body is the single import line `@AGENTS.md`. Existing content outside the block is preserved by init, adopt, and upgrade.

The root `AGENTS.md` managed fragment directs agents to read `ENGINEERING_HARNESS.md` and `docs/engineering/REPOSITORY_CONTEXT.md` before implementation.

## Repository-context seed

`docs/engineering/REPOSITORY_CONTEXT.md.seed` maps to `docs/engineering/REPOSITORY_CONTEXT.md` with management mode `seed`. A seed is written only when the path is absent and the lock has no prior seed entry. Existing content is accepted without comparison. The lock records seed presence or removal without a content hash so later upgrades preserve repository edits and intentional deletion.

The scaffold contains the selected project name plus explicit human-owned fields for purpose, setup, build, test, lint, architecture, generated paths, restricted paths, and verification constraints. It states that it is context, not approved intent or requirements.

## Diagnostics

`doctor` requires `AGENTS.md`, `CLAUDE.md`, and the repository-context file. It verifies a standalone `@AGENTS.md` import in `CLAUDE.md`, skips seed content hashing, and continues to validate ordinary managed hashes.

## Packaging and upgrade

The source distribution includes both new template sources. Upgrade adds them to older installations, preserves customized shared-root content, and never restores a repository-context file once its seed entry records intentional removal.
