+++
id = "REQ-DST-063"
type = "requirement"
title = "Exercise topology capacity on integration history"
status = "approved"
owners = ["quality-owner", "engineering-owner"]
created = "2026-08-20"
updated = "2026-10-03"
statement = "WHEN topology capacity is qualified, THE SYSTEM SHALL exercise the exact branch and pull-request merge histories that contribute revision provenance and SHALL apply the same declared target on supported platforms."
verification_method = ["test"]
verification_notes = "automated-cross-platform-and-hosted-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Exercise topology capacity on integration history

## Rationale

Topology contains valid revision-provenance observations. A branch push may therefore remain below the target while GitHub's pull-request merge ref, and later merged `main`, add legitimate history and cross the same target. Qualification that observes only the feature branch misses the integrated product state.

## Preconditions and trigger

A candidate changes the topology acceptance contract or adds formal artifacts and is evaluated locally, on a branch push, or through a pull-request merge ref.

## Required response

- Assert the declared target directly rather than deriving it from the current output size.
- Retain the current-repository acceptance test on the candidate source tree.
- Run hosted candidate-source evidence on the pull-request merge ref before merge.
- Record branch, merge-ref, and resulting merged-main topology bytes when they differ because their valid revision histories differ.
- Apply the same 4,194,304-byte target on Windows and Linux; platform path or line-ending behavior must not select another target.

## Failure and boundary behavior

A branch-only pass does not override a merge-ref failure. A size difference caused by different valid Git history is recorded and assessed against the same target. Unexplained nondeterminism for the same bytes and history remains a failure.

## Constraints

- Verification does not fabricate or rewrite Git history merely to reduce output.
- Revision provenance remains complete and authoritative only to its existing derived-observation boundary.
- Hosted workflow success does not itself approve, verify, or merge a candidate.

## Acceptance examples

### Example: push and merge-ref differ

**Given** a branch push and pull-request merge ref contain the same formal files but different valid merge history,

**When** topology is generated for each,

**Then** both observed byte counts are retained and each is compared with the same 4 MiB target.

### Example: unexplained repeat difference

**Given** identical repository bytes and Git history,

**When** generation runs twice,

**Then** any topology byte or digest difference fails deterministic qualification.

## Open decisions

None when approved.

## Manual capacity revision — 2026-10-03

mmzen authorized the 4 MiB target and the bounded manual amendment after reviewing
the two-file correction and the affected definitions. This records the human's
exception to the selected 0.21.0 amendment procedure's unsupported-command stop;
it is not a revision operation performed by harnessctl. Lifecycle states,
original decision history and all noncapacity rules are preserved.

The exact accepted predecessor is the member `docs/engineering/harness-distribution/requirements/REQ-DST-063.md` of
[accepted-predecessors.zip](../evidence/WO-DST-028/accepted-predecessors.zip),
SHA-256 `1bb8e913d0cde489c0e571216074e9a9247ae2f996545f44666d4d9747b8ceef`. The
[amendment manifest](../evidence/WO-DST-028/amendment.json) links both versions
and retains the owner's instruction. Earlier work keeps its original Git-bound
definitions and evidence.

The current target is 4,194,304 uncompressed UTF-8 bytes. Measurements and
0.5.0/0.5.1 rollout statements from the earlier amendment describe its historical
context. New work uses selected released 0.21.0 and the checks in VER-DST-030
under WO-DST-028. All other payload budgets, complete topology data, integrity
checks and publication boundaries remain unchanged. RLS-SEH-032's approved
candidate and archives are not amended.
