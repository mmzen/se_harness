+++
id = "VER-HUP-019"
type = "verification"
title = "Verify adoption of the public 0.18.0 evaluator"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-09-15"
updated = "2026-09-15"
[relations]
verifies = ["REQ-HUP-037", "REQ-HUP-038"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-15T11:01:51Z"
decided_by = "assurance-owner"
reason = "The owner replied \"i approve evaluator upgrade\" to the reviewed WO-HUP-019 scope and its five governing drafts on 2026-09-15. This records approval of the selected artifact, including the proposed architecture assessment and required assurance classification where applicable. The accepted scope authorizes start, completion only after passing checks, and ready verification-record preparation; independent verification and external integration remain separate."
+++

# Verify adoption of the public 0.18.0 evaluator

## Independence

Expected package identity comes from released RLS-SEH-027 and the public package index. Required behavior comes from the two requirements and SPEC-HUP-019.

The disposable rehearsal is preparation evidence. It does not verify the final repository candidate or exercise an assurance decision.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-HUP-037 | Test and inspection | Public wheel checksum, baseline doctor, plan, transaction document, resulting lock, replay | Exact release checksum; passing prior integrity; reviewed actions only; prior and target identities retained; repeat reports 41 unchanged paths |
| REQ-HUP-038 | Test and inspection | Released 0.18.0 doctor, validation, released-root qualification, review preflight, candidate identity derivation, source suite, owner-content diff | Zero failed integrity checks or graph errors; no unexplained new warnings; 0.18.0/0.19.0 pair; required gates pass; all suite failures explained against the unchanged control |

## Acceptance scenarios

1. Compare the wheel checksum with the release record before installing outside the repository.
2. Check baseline 0.17.0 integrity and review all selected replacement paths.
3. Apply once with transaction evidence, then confirm a no-op replay and the release-bound archive identity.
4. Check owner content preservation and unchanged historical records.
5. Run the repository-required source checks and the selected review preflight.
6. Confirm that a wrong checksum, unexpected plan or equal candidate/root versions prevents continuation.

## Required checks

Use released 0.18.0 outside the checkout for doctor, validate, qualify released-root and review preflight.
Run `python scripts/run_tests.py`, `python scripts/validate_release_distributions.py --root .`, candidate `--help`, candidate doctor, and `python -m repository_tools.evaluator_facts derive --repository . --json`.

## Platforms and pass criteria

The local qualification uses Windows and the recorded Python version. Linux CI remains pending until a separately selected remote integration action.

The full source suite must have no new failures relative to the same-commit 0.17.0 control. Any correction must satisfy HUP-NEW-012.

## Evidence retention

Retain a short result summary under the work order's evidence directory and the single upgrade transaction beside it. Retain raw local logs outside the checkout.

## Assurance boundary

Completion and a ready verification record do not constitute independent verification. The assurance owner's decision remains separate.
