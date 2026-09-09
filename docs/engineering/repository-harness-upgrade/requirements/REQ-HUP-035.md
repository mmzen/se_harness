+++
id = "REQ-HUP-035"
type = "requirement"
title = "Adopt exact public 0.17.0 as the standard root by the simple upgrade"
status = "draft"
owners = ["repository-owner", "engineering-owner"]
created = "2026-09-09"
updated = "2026-09-09"
statement = "THE INSTALLER SHALL move the root to exact public 0.17.0 in one atomic transaction whose lock names that version and archive pair, with ten updates and one addition."
verification_method = ["test", "inspection"]
priority = "must"
source = "RLS-SEH-026, released 2026-09-09; SPEC-DST-026 rule DST-CFG-015 and SPEC-DST-027 rule DST-MWF-014, which bind the root adoption of the carrying release; the standing practice of adopting each published release as this repository's root (WO-HUP-007 to WO-HUP-017); the rehearsal of 2026-09-09 on a throwaway LF clone of main at e855cc9a"

[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Adopt exact public 0.17.0 as the standard root by the simple upgrade

## In plain words

The published 0.17.0 evaluator, installed outside this checkout, upgrades
the managed files in one transaction and records itself in the lock. Ten
managed files change and one is added; a second upgrade changes nothing.

## Why

Release 0.17.0 rewrites the installed configuration to its five read keys
and hardens the managed workflow. It moves the ignore block to hash markers,
drops two unreachable contract entries and adds the risk template. Every
consumer upgrade takes them; this repository's root takes them here. The
rehearsal showed ten files update, one file added, and a no-op replay.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Exact public 0.17.0, isolated outside the checkout, applies the upgrade | One atomic transaction writes ten updates and one addition and writes a lock naming 0.17.0 with its archive pair. The transaction document is retained. A replay reads every managed file unchanged. | The guard refuses, a managed file reads customized, or nothing is written |

## Examples

### Normal

**Given** the wheel whose digest equals `RLS-SEH-026`'s table, isolated,

**When** it applies the upgrade on main,

**Then** 10 files update, 1 is added and 30 are unchanged. The lock reads
0.17.0 with archive `305c7cbc…` and forty-one files. The replay reads 41
unchanged.

### Failure

**Given** a managed file whose bytes differ from the lock,

**When** the upgrade is planned,

**Then** the path reads customized and nothing is written.

## Open decisions

None.
