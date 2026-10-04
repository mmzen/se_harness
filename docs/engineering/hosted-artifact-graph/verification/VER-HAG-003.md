+++
id = "VER-HAG-003"
type = "verification"
title = "Verify explicit human attribution for decision dispositions"
status = "approved"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-04"

[relations]
verifies = ["REQ-HAG-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T16:52:37Z"
decided_by = "mmzen"
reason = "mmzen explicitly approved WO-HAG-003 and required verification in response to the reviewed six-artifact correction package. This applies only to that package: local implementation, checks, commits and commit-bound verification preparation. Human verification acceptance, publication, release, adoption and the live DEC-HAG-001 disposition remain separate. Reviewed file hashes were compared before this transition; approval bindings are retained under docs/engineering/hosted-artifact-graph/evidence/WO-HAG-003/."
+++

# Verify explicit human attribution for decision dispositions

## Independence

Expected results come from REQ-HAG-010 and SPEC-HAG-005, fixed before the
correction. Use disposable synthetic copies of the HAG owner/decision shape;
never use a candidate evaluator to mutate the live DEC-HAG-001. The governing
checker remains released 0.22.0 with its existing archive/payload identity.

## Requirement-to-evidence matrix

| Requirement | Method | Pass condition |
| --- | --- | --- |
| REQ-HAG-010 | CLI, API and installed-package tests | Explicit valid mapping records the actual human and owner label; invalid or inferred mappings refuse atomically; old commands and records retain their behavior. |

## Cases

1. Reproduce WEX201 without mapping for mmzen against engineering-owner.
2. Valid explicit mapping: preview produces no changed bytes; apply records
   mmzen in disposition/event and engineering-owner in authority_owner.
   The blocked work order retains its owners, state and historical events.
3. Reject unrelated/empty/overlong/control-character owner values, empty
   actor, undeclared option, missing reason and disallowed state with no writes.
4. A deviation uses specification owners, not the blocked WO owner. Preserve
   existing multiple-holder semantics without adding new holders.
5. Paired-risk accept/avoid/mitigate/withdraw retains mmzen and existing
   required evidence/revisit rules; a deferral keeps its declared narrow scope.
6. Direct-owner commands and old dispositions without authority_owner still
   pass their existing tests. Malformed optional metadata is rejected.
7. Verify one shared CLI/API path, optional-field serialization and readable
   diagnostics. Command help and instructions distinguish identity, owner
   accountability, actual human consent and lack of authentication.
8. Run focused decision/risk/workflow tests, the full repository suite,
   distribution checks, CLI smoke and installed-wheel tests on Windows and
   Linux. Preserve skipped/unperformed cases as such.

## Evidence and completion

Retain commands, runtime identities, exits, results, refusal observations,
changed-byte comparisons and review findings under the WO-HAG-003 packet
directory. Build candidate packages only in disposable environments. Use the
released capture procedure to allocate the actual commit-bound VREC later.
Its generated destinations must be checked when known. Human verification,
release, adoption and resolution of the live decision remain separate.
