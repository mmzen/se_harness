+++
id = "VER-IAR-016"
type = "verification"
title = "Verify the active plugin and native instruction delivery"
status = "approved"
owners = ["quality-owner", "repository-owner"]
created = "2026-09-28"
updated = "2026-09-28"

[relations]
verifies = ["REQ-IAR-026"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-28T07:51:40Z"
decided_by = "quality-owner"
reason = "Human repository owner mmzen: \"I approve, you can start the work orders\". Approval covers the reviewed instruction-cleanup package and required commit-bound assurance. Legacy evaluator role quality-owner records that human decision; Codex applies it. Reviewed SHA-256 56df632eee3fd599a95f83210a8989207300068edf96264f0b4f975f013e2e92."
+++

# Verify the active plugin and native instruction delivery

## Independence and scope

REQ-IAR-026 and SPEC-IAR-014 IAR-DIS-008/009 define the expected behavior.
This contract verifies the actual host/package selection behind finding F1.
The exposed cache observation is evidence about one location, not proof of the
package loaded by every host. Prior temporary-demo results are not fresh proof
of the active configuration. Source code need not change to correct adoption.

## Requirement-to-evidence matrix

| Requirement | Method | Case | Pass condition |
| --- | --- | --- | --- |
| REQ-IAR-026 | inspection | Active host, marketplace, plugin and evaluator inventory | Record host/version, loaded plugin identity and path, package provenance, hooks and skills hashes, repository path and selected released evaluator. Distinguish a cache from demonstrated active loading. |
| REQ-IAR-026 | demonstration | Startup and compaction in Codex and Claude Code | Each claimed host actually delivers the current repository's full root, including its final heading. Capture root path, release, root hash, event and observed payload. A direct helper invocation is not a native event. |
| REQ-IAR-026 | demonstration, test | Switch repositories; missing root; mismatched release; uncertain previous write | Correct repository selection or explicit gap; no stale success, replayed mutation, restored AGENTS harness block or inferred authority. |

## Procedure and boundaries

Inventory current configuration read-only first. Compare it with a released
plugin package compatible with the repository's selected release. Retain the
exact package identity and digest before proposing any replacement. Do not
install candidate source as the selected evaluator.

Rehearse with isolated host profiles and disposable repositories. Use the
existing native-demo procedure and actual host events; record host commands
as run. Keep credentials and unrelated conversation text out of evidence.
Real profile or marketplace changes require a separately reviewed exact target
and action. Do not edit a managed plugin cache by hand.

After any authorized adoption, repeat the native startup and compaction checks
on the intended configuration. For the new collection, the active skill must
follow its current discovery route and not unconditionally request the old card.
A stale cache that the host does not load is a different finding from a stale
loaded plugin; record which case was observed.

## Evidence and pass boundary

Retain inventory, package hashes, native traces, exact commands, failure cases
and any reviewed adoption/readback under evidence/WO-IAR-020/. Bind the retained
evidence to the candidate commit through supported VREC preparation.
Use selected released lifecycle checks separately from host demonstrations.

Both advertised hosts must have actual evidence. If unavailable, identify the
host and unverified claim; do not mark the complete qualification passed.
A proposed repair, synthetic trace or partial trace does not close F1. An exact
adoption handoff is a useful intermediate output, not completed qualification.
Approval of this contract does not authorize a host update or release.
