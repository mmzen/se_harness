+++
id = "REQ-HUP-033"
type = "requirement"
title = "Adopt exact public 0.16.0 as the standard root by the simple upgrade"
status = "draft"
owners = ["repository-owner", "engineering-owner"]
created = "2026-09-07"
updated = "2026-09-07"
statement = "THE INSTALLER SHALL move the root to exact public 0.16.0 in one atomic transaction whose lock names that version, payload and archive pair and no scripts path."
verification_method = ["test", "inspection"]
priority = "must"
source = "RLS-SEH-025, released 2026-09-07; SPEC-DST-025 rules DST-ENG-011 and DST-ENG-013; the standing practice of adopting each published release as this repository's root (WO-HUP-007 to WO-HUP-016); the rehearsal of 2026-09-07 on a throwaway LF clone of main at 5df10aa9"

[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Adopt exact public 0.16.0 as the standard root by the simple upgrade

## In plain words

The published 0.16.0 evaluator, installed outside this checkout, upgrades
the managed files in one transaction and records itself in the lock. For
the first time files leave: the eight script copies the evaluator used to
install are removed, and a second upgrade changes nothing.

## Why

Release 0.16.0 ships the evaluator's scripts inside the wheel, and the
installer writes none of them into a repository. This repository still
carries the 0.15.0 evaluator's eight hash-locked copies. The rehearsal
showed six files update, the eight copies leave, and a no-op replay.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Exact public 0.16.0, isolated outside the checkout, applies the upgrade | One atomic transaction writes six updates, removes the eight retired copies and writes a lock with no scripts entry. The transaction document is retained. A replay reads every remaining file unchanged. | The guard refuses, a retired copy reads customized, or nothing is written |

## Examples

### Normal

**Given** the wheel whose digest equals `RLS-SEH-025`'s table, isolated,

**When** it applies the upgrade on main,

**Then** 6 files update, 8 leave, 34 are unchanged; the lock reads 0.16.0
with archive `a969d6ab…` and forty files; the replay reads 40 unchanged.

### Failure

**Given** a root script copy whose bytes differ from the lock,

**When** the upgrade is planned,

**Then** the path reads customized and nothing is written.

## Open decisions

None.
