+++
id = "VER-ECP-027"
type = "verification"
title = "Verify supported ownership in upgrade rehearsal"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-16"
updated = "2026-09-16"

[relations]
verifies = ["REQ-ECP-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-16T16:55:52Z"
decided_by = "assurance-owner"
reason = "The owner approved the presented SPEC-ECP-025, VER-ECP-027 and WO-ECP-039 package with \"i apprive\" on 2026-09-16, exercising the assurance-owner decision for VER-ECP-027. Reviewed SHA-256 13b9827b2ca1db801ff1eae828693aae4ecb20ccee75eeceb19e6fb6179a5d1e. This records definition and bounded execution approval, not assurance or external delivery."
+++

# Verify supported ownership in upgrade rehearsal

## Independence and acceptance

Expected behavior comes from SPEC-ECP-025 and the existing real-handover
contract. Extend tests/test_upgrade_rehearsal.py's existing fixtures with
explicit initial and resulting ownership values. Its current fake evaluators
default to schema 3, leaving the successful schema-4 path untested.

| Requirement | Method | Evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-ECP-012 | test, demonstration, inspection | Focused regressions, real upgrade replay, existing CI | Both supported ownership modes pass; malformed or changed ownership and evaluator errors fail; each real handover step retains its meaning. |

Cover schema-3 and schema-4 success, supported extra plugin metadata, missing
or invalid providers, unsupported/non-integer schemas and accidental ownership
changes in either direction. Reuse the existing failure tests for doctor,
validation, version, payload, dirty input/export and credential isolation.
Exercise version and payload refusals on the plugin path as well. Assertions
must check outcomes rather than mirror the implementation's helper structure.

## Required checks

Run the focused module and repository-required full source suite after the
final implementation. Retain counts, skips, commands and actual interpreter.
Run release-distribution validation and candidate CLI help; separate the known
source 0.19.0/selected 0.18.0 candidate-doctor skew from governing integrity.
The isolated released 0.18.0 evaluator must pass doctor, graph validation,
review preflight and the selected scope/handoff checks.

Run the real existing upgrade rehearsal twice locally on Windows using the
released predecessor and installed candidate wheel outside the operational
checkout. Prefer the checksum-verified non-promotable wheel already retained
by CI if its relevant product inputs are unchanged; record those comparisons.
Otherwise an explicitly non-promotable ephemeral local wheel may be built.
Both results must pass, give the same canonical lock digest, preserve plugin
ownership, and leave the operational checkout clean. Retain original failed
Linux/Windows evidence; do not substitute fixture results for real execution.

After authorized delivery, the existing Linux and Windows rehearsal jobs and
their dependent integration-package checks must pass before merge. Local
evidence does not claim a hosted result. No workflow change or extra CI job is
needed. Additional failures require diagnosis against this bounded scope.

## Evidence and assurance

Keep commands, exit codes, results, review findings and file digests under
evidence/WO-ECP-039/. Preserve the original failure and note that it predates
WO-HUP-020; its fix addressed the separate predecessor assessor only.

Prepare VREC-ECP-041 at the corrected clean candidate for WO-ECP-039,
WO-HUP-020 and WO-PLG-025, conforming to this contract, VER-HUP-020 and
VER-PLG-025. Reuse the 29 earlier evidence files only after confirming relevant
inputs and hashes are unchanged. This contract prospectively permits this
aggregate record and its ECP location in place of the earlier contracts'
VREC-HUP-019/VREC-PLG-022-specific preparation instructions. Their substantive
acceptance conditions remain; new rehearsal behavior belongs to this contract.
Earlier verified records remain unchanged. Preparation, owner assurance,
external delivery and merge remain separate decisions.
