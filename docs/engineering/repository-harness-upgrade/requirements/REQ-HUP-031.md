+++
id = "REQ-HUP-031"
type = "requirement"
title = "Adopt exact public 0.15.0 as the standard root by the simple upgrade"
status = "approved"
owners = ["repository-owner", "engineering-owner"]
created = "2026-09-05"
updated = "2026-09-05"
statement = "WHEN exact public se-harness 0.15.0 installed outside the checkout runs harnessctl upgrade --apply on this 0.14.0 root, THE INSTALLER SHALL replace the managed root with 0.15.0's plan in one atomic transaction whose lock names 0.15.0 by version, payload digest and the published wheel's archive pair."
verification_method = ["test", "inspection"]
priority = "must"
source = "RLS-SEH-024, released 2026-09-05; the standing practice of adopting each published release as this repository's root (WO-HUP-007 to WO-HUP-015); the rehearsal of 2026-09-05 on a throwaway clone of main at e4192ed"

[relations]
derives_from = ["CAP-HUP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-05T08:35:42Z"
decided_by = "repository-owner"
reason = "Approved by the accountable repository owner on 2026-09-05 with the instruction 'i appprove' (approve), after reviewing PR #352 (REQ-HUP-031, REQ-HUP-032, SPEC-HUP-016, VER-HUP-016, WO-HUP-016) and the rehearsal of the 0.15.0 root adoption on a throwaway clone of main at e4192ed."
+++

# Requirement: Adopt exact public 0.15.0 as the standard root by the simple upgrade

## In plain words

The published 0.15.0 evaluator, installed outside this checkout from the
wheel whose digest the release record binds, upgrades this repository's
managed files in one transaction and records itself in the lock. A second
upgrade then changes nothing.

## Why

`RLS-SEH-024` released 0.15.0 on 2026-09-05. Unlike 0.14.0 it is a content
release: the decision artifact, the reader-first definition templates, the
glossary seed and the new validator rules live in it. Nothing of that
applies to this repository until its own root moves, so a `DEC-` file still
fails the managed check here and new drafts still end with `Open
decisions`. The rehearsal showed 19 managed files update, one template
added, the root glossary adopted as owner content, and a no-op replay.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Exact public 0.15.0, isolated outside the checkout, runs `harnessctl upgrade . --apply` on the 0.14.0 root | One atomic transaction writes the reviewed plan and a lock naming 0.15.0 by version, installed-payload digest and archive pair; the transaction document is retained; a second `upgrade .` reads every file unchanged | The guard refuses, or the transaction writes nothing |

## Examples

### Normal

**Given** the wheel file whose SHA-256 equals `RLS-SEH-024`'s distribution
table, installed in an isolated environment,

**When** it plans and applies the upgrade on `main`,

**Then** the plan is 48 files with 19 `update`, 1 `add`, 1 `adopt` and no
`customized`, `conflict` or `remove`; the lock reads `tool_version 0.15.0`
with archive `eb09343f…`; the replay reads 48 unchanged.

### Failure

**Given** a candidate runtime resolving inside the checkout,

**When** it attempts the same upgrade,

**Then** the mutation guard refuses and no file changes.

## Open decisions

None.
