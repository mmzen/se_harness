+++
id = "VER-RLO-010"
type = "verification"
title = "Verify formal record selection for release replay"
status = "approved"
owners = ["mmzen"]
created = "2026-10-01"
updated = "2026-10-01"

[relations]
verifies = ["REQ-RLO-014"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T20:30:05Z"
decided_by = "engineering-owner"
reason = "Human mmzen: i approve. Approves the reviewed WO-RLO-013 and VER-RLO-010 with required commit-bound verification, the two-file replay selector correction, ordinary updates to work/release-0-21-0 and draft PR 517, and existing read-only rehearsals. Permits the released 0.20.1 role-label encoding; mmzen remains the human decision-maker. Human verification, merge and exact release-record decision remain separate. Reviewed SHA256 656b04adc65539879d704b367899bac7a5df9df66ae98e8a86995f85e2336e80. Only confirmed work-order assurance metadata was added."
+++

# Verify formal record selection for release replay

## Independence

Derive the selected record and accepted distribution hashes from unchanged
formal RLS inputs and SPEC-RLO-004. Independently place fixture records in the
repository's canonical domain `releases/` location. Do not derive expected paths
from the selector under test. An archived evidence copy remains evidence.

This contract covers WO-RLO-013's bounded correction. It does not replace the
complete recipe qualification in VER-RLO-004 or the v0.21.0 release contracts.

## Requirement-to-evidence matrix

| Requirement | Method | Case or evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-RLO-014 | test | One formal RLS plus an exact evidence copy | Select the formal RLS once; both files stay byte-identical. |
| REQ-RLO-014 | test | Evidence-only RLS copy | Refuse because no formal RLS matches; no input changes. |
| REQ-RLO-014 | test | Two canonical formal RLS files with the same ID | Refuse ambiguity; do not select the first. |
| REQ-RLO-014 | test | Symlink record where supported | Exclude the symlink; never treat its target as a formal match through that link. Record unsupported platform creation as a skip. |
| REQ-RLO-014 | inspection | Diff and preservation hashes | Only approved paths change. Existing status, distribution, candidate, recipe and accepted-hash checks remain active. RLS-SEH-030 and its archived copy retain their original digests. |
| REQ-RLO-014 | demonstration | Existing read-only publication rehearsal, requested RLS-SEH-030 | The corrected selector resolves the formal record; two pinned builds reproduce its bound wheel and sdist hashes. Retain exact correction ref, actual released candidate, run URL and result digests. No lifecycle or publication effect occurs. |

## Procedure and environments

1. Preserve the observed failure from GitHub run 36919403159 and record the
   two input paths and digests before editing.
2. Run `python -m unittest tests.test_release_build` on Windows and Linux.
   Retain exact interpreter versions and any skipped symlink case.
3. Run `python scripts/run_tests.py` and
   `python scripts/validate_release_distributions.py --root .`.
   Retain the actual counts and results. Use released 0.20.1 outside the checkout
   for formal validation, scope, preflight, handoff and VREC preparation.
4. Review the small diff and compare unchanged formal/evidence bytes. Confirm
   the correction introduces no import into portable evaluator or plugin code.
5. At the clean correction commit, update the approved draft PR and dispatch
   the existing publication rehearsal for RLS-SEH-030 with read-only controls.
   Fetch and inspect the actual result; do not infer success from dispatch.
6. Retain passing and failed evidence, then prepare the separate VREC for
   WO-RLO-013 at that commit. Human verification remains a separate decision.

## Evidence retention

Retain evidence in `docs/engineering/release-orchestration/evidence/WO-RLO-013/`:
exact commits, command arrays, directories, runtime identity, exit codes and
outputs, focused and full tests, distribution and scope checks, diff review,
before/after SHA-256 values, original failed run, corrected hosted run and
bounded replay result. Retain VREC-RLO-013's generated evaluator evidence at
`docs/engineering/release-orchestration/evidence/VREC-RLO-013-evaluator.json`.

## Limits

A fixture proves selection behavior, not a hosted build. The historical replay
proves the corrected repository path against fixed RLS-SEH-030 inputs; it does
not approve or verify a v0.21.0 candidate. Final v0.21.0 qualification, desktop
evidence, human verification, release decision and publication remain required.
