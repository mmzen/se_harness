+++
id = "VER-IAR-017"
type = "verification"
title = "Verify compatibility-guide retirement and supported upgrades"
status = "draft"
owners = ["quality-owner", "repository-owner"]
created = "2026-09-28"
updated = "2026-09-28"

[relations]
verifies = ["REQ-IAR-028", "REQ-IAR-027"]
+++

# Verify compatibility-guide retirement and supported upgrades

## Independence

Use SPEC-IAR-015's explicit six-path set and independently retained predecessor
fixtures. Use SPEC-IAR-014 for preserved discovery and instruction meaning.
Never copy candidate output into expected hashes or routes. Retain the actual
candidate commit, package hashes, interpreter, platform, command and exit code.

## Requirement-to-evidence matrix

| Requirement | Method | Case | Pass condition |
| --- | --- | --- | --- |
| REQ-IAR-028 | test | Fresh install from built wheel and sdist | None of the six source templates is distributed or generated. Current root, guides, authoring and machine contracts are present; doctor and representative discovery pass. |
| REQ-IAR-028 | test, inspection | Upgrade from 0.19.0 with stock, customized and absent seeds | Existing bytes remain identical, absent seeds stay absent, the new lock and readiness agree, and no owner deletion is automatic. |
| REQ-IAR-028 | test | Supported 0.18.0 migration and refusal | Legacy fingerprints and entry migration still work. Recognized old full guides convert to pointers through the accepted migration contract; customized guides require an explicit owner plan. Unsafe or ambiguous inputs refuse before writes, with no silent success or partial mutation. |
| REQ-IAR-028 | test, demonstration | Authorized cleanup rehearsal, modified pointer and stale consumer | Only reviewed stock pointers are eligible; modified bytes or an active old consumer stop cleanup. Supported reconciliation and retry agree with actual files. |
| REQ-IAR-027 | inspection, test | Consumer inventory and instruction routes | Current consumers no longer need the six pointers. Remaining references have recorded historical or version-conditioned reasons. Canonical destinations resolve and human rights, gates and historical evidence are unchanged. |

## Required checks

Run installer, integrity, preflight, distribution, progressive-discovery and
affected documentation/plugin tests on Windows and Linux. Include negative
controls for a broken replacement route, unsafe destination and a customized
owner guide. Reuse existing transaction/recovery tests when they establish the
same behavior; do not add assertions solely to mirror implementation branches.

Run the full repository test runner, distribution validator and CLI smoke
check. Exercise actual installed candidate wheels in disposable repositories.
Validate supported predecessor paths, including the existing upgrade rehearsal;
do not relax a failing migration assertion just to remove the old filenames.
Run the selected released evaluator's validation and WO start/handoff separately.

## Retained evidence

Keep the six-path disposition, consumer inventory, distribution listings,
owner-byte comparisons, lock/readiness results, migration/refusal/retry traces,
test logs and complete change set under evidence/WO-IAR-022/. Prepare the exact
commit-bound VREC using the supported procedure. Qualification evidence from
WO-IAR-020 is a prerequisite for a real repository cleanup, not replaced by
the synthetic fixtures in this work order.

## Acceptance boundary

Human acceptance confirms this bounded product change. It does not select a
release version, publish a package, upgrade this repository or remove its
installed pointers. Those later actions need an exact released candidate and
their own recorded authority. Unavailable platform evidence remains unverified.
