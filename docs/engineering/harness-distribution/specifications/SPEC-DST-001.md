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

