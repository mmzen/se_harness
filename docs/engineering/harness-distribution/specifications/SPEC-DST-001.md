+++
id = "SPEC-DST-001"
type = "specification"
title = "Single-profile harness distribution"
status = "implemented"
owners = ["technical-owner", "quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
specifies = ["REQ-DST-001", "REQ-DST-002", "REQ-DST-003", "REQ-DST-004", "REQ-DST-005", "REQ-DST-006"]
+++

# Specification

## Interface

`harnessctl` provides `init`, `adopt`, `validate`, `dashboard`, `doctor`, and `upgrade`. `init` and `adopt` accept a target and optional project name; `upgrade` plans by default and requires `--apply` to mutate safe managed content. No command accepts a profile.

## Installation contract

Canonical files live at `templates/repository/standard/`. UTF-8 `.tpl` files have their suffix removed and bounded tokens rendered. `AGENTS.md.fragment` and `gitignore.fragment` are placed between unique markers in their target files. Other files are fully managed.

The planner resolves every destination below the target, rejects symlink traversal, classifies all files, and rejects init/adopt if an ordinary destination differs. Only after a non-conflicting plan may application write atomically and create `.engineering-harness.lock`.

## Upgrade contract

The lock schema records the distribution version, management mode, and SHA-256 of each managed file or managed fragment. Upgrade classifies paths as add, integrate, update, unchanged, or customized. It applies only add, integrate, and update; customized content is untouched and produces a manual-review outcome.

## Adoption contract

Adoption generates `docs/engineering/ADOPTION_REPORT.md` from bounded filename checks. The report calls all findings observations and requires accountable humans to create and approve the first formal chain.

## Operations

`validate` and `dashboard` run target-local managed scripts and preserve their exit codes. `doctor` checks Python, configuration, lock, required files, and ordinary managed hashes. All errors are bounded messages without target file bodies.

## Amendment record

**The upgrade action vocabulary gains `remove`, proposed 2026-08-29 under
`WO-DST-022` (issue #271; `SPEC-DST-022`).** The upgrade contract above
classified paths as add, integrate, update, unchanged, or customized, all
derived from the new managed set, so a prior-lock managed path the new set
no longer names appeared in no plan: the 0.10.0-to-0.11.0 upgrade left the
fifteen files of three retired skills on disk while the rewritten lock
stopped naming them. The amendment adds `remove` for a leaving-set path
whose bytes still match the locked digest; apply deletes it in the same
transaction and the entry leaves the lock, while a differing copy is
reported as `customized` and blocks apply as today. The retirement rules
are `SPEC-DST-022`'s `DST-UPR-001` to `DST-UPR-008`. Nothing else in this
specification changes.

