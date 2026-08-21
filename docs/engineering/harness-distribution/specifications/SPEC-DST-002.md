+++
id = "SPEC-DST-002"
type = "specification"
title = "Cross-agent instructions and repository context"
status = "implemented"
owners = ["technical-owner", "quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-21"

[relations]
specifies = ["REQ-DST-007", "REQ-DST-008"]
+++

# Specification

## Instruction integration

`CLAUDE.md.fragment` maps to root `CLAUDE.md` using the same unique harness markers and hash-based fragment ownership as `AGENTS.md.fragment`. Its managed body is the single import line `@AGENTS.md`. Existing content outside the block is preserved by init, adopt, and upgrade.

The root `AGENTS.md` managed fragment directs agents to read `ENGINEERING_HARNESS.md` before implementation. It names exactly one harness destination.

## Repository-context seed

Withdrawn on 2026-08-21 by `REQ-DST-065` and `SPEC-DST-021` under `WO-DST-021`. The harness ships no repository-context seed and no successor scaffold under any name. Repository-local operational facts belong in the owner-controlled region of `AGENTS.md`, which the harness does not scaffold, track, or require. An existing owner-authored file at the retired path is ordinary untracked owner content and is never written, moved, truncated, or deleted; the regenerated lock carries no entry and no tombstone for it.

The seed mechanism itself is unchanged and continues to govern the remaining seeds. `docs/engineering/README.md.seed` maps to `docs/engineering/README.md` with management mode `seed`. A seed is written only when the path is absent and the lock has no prior seed entry. Existing content is accepted without comparison. The lock records seed presence or removal without a content hash so later upgrades preserve repository edits and intentional deletion.

## Diagnostics

`doctor` requires `AGENTS.md` and `CLAUDE.md`. It verifies a standalone `@AGENTS.md` import in `CLAUDE.md`, skips seed content hashing, and continues to validate ordinary managed hashes. It makes no presence check for the retired repository-context path.

## Packaging and upgrade

The source distribution includes both new template sources. Upgrade adds them to older installations, preserves customized shared-root content, and never restores a repository-context file once its seed entry records intentional removal.
