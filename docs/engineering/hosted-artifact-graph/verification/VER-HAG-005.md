+++
id = "VER-HAG-005"
type = "verification"
title = "Verify stacked-branch adoption assessment and evidence preservation"
status = "approved"
owners = ["mmzen"]
created = "2026-10-05"
updated = "2026-10-05"

[relations]
verifies = ["REQ-HUP-008", "REQ-HAG-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-05T13:25:58Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"I approve\" to SPEC-HAG-006, VER-HAG-005 and WO-HAG-006, required commit-bound verification, DEC-HAG-003 bounded-manual-revision of the exact VER-HAG-004 proposal, and ordinary draft PR #535 updates in mmzen/se_harness from codex/hosted-artifact-phase1 to codex/hosted-artifact-graph-inputs. Review binding SHA-256 c9d4d84326b0e26d39519a1eadb91e216e4a6f01700213ec3c76a6854e55a649. This covers local implementation, checks, aggregate ready-record publication and later separately given verification-decision push. No verification acceptance, risk acceptance, retargeting, base-branch update, force push, merge, release or deployment. The exact manual amendment grants no general revision mechanism or gate waiver."
+++

# Verify stacked-branch adoption assessment and evidence preservation

## Independence

Derive expected behavior from SPEC-HAG-006. Use released evaluator 0.22.1 in
its separate installation; candidate code is only the repository-owned CI
assessor under test. Test synthetic Git histories and the exact HAG/main
commits independently of the implementation's reported result.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-HUP-008 | test, inspection | CI-01 through CI-04 | Independent adopted-history proof works without changing B or weakening direct adoption, identity or refusal checks. |
| REQ-HAG-008 | test, inspection | CI-03 through CI-06 | Original scope is fully checked, historical bytes survive, current handoff binds correctly and actual CI passes. |

## Cases

1. CI-01: Existing direct adoption and same-version cases keep their verdicts.
   A synthetic older stacked branch passes only with one matching, independently
   integrated adoption. Use another version pair to catch HAG-specific constants.
2. CI-02: Refuse target-only releases; malformed or multiple base releases;
   missing, unrelated or ambiguous default-branch history; changed release or
   transaction bytes; different root or evaluator identities; duplicate or
   nonmatching transactions; dirty checkout and existing runtime-origin failures.
   Check actual nonzero exits and absence of evaluator execution where required.
3. CI-03: Run plan and complete assess at the exact HAG candidate with original
   PR base be1812e7042081014cc7682da8b9cd3822d9071f. Independently compare the
   declared default-history anchor and byte hashes. Install/acquire no candidate
   governor. Prove no checkout writes and preserve the original failed result.
4. CI-04: Run focused assessor tests on Windows and Linux, the canonical full
   source suite, distribution checks and CLI smoke check. Retain actual commands,
   platforms, exits and skips. Run the existing actual PR CI after publication;
   its predecessor, harness and other applicable checks must pass before merge.
5. CI-05: Compare the preserved WO-HAG-001 handoff bytes against the full original
   Git blob. Rebind the live packet using released evidence and keep old test
   claims unchanged. Prove VREC-HAG-001/002 and their complete bound evidence are
   unchanged. Compare VER-HAG-004's before/after hashes and identical lifecycle
   events with the explicit DEC-HAG-003 amendment. Zero hosted scenarios remain.
6. CI-06: Run complete combined PR scope from the original base using
   WO-HAG-001/003/004/005/006. Run applicable scope and handoff gates, complete
   only the finished corrective/reconciliation work, and capture one ready
   commit-bound VREC covering WO-HAG-005/006 and VER-HAG-004/005. WO-HAG-001
   remains in_progress. Human verification remains separate.

## Evidence retention and limits

Retain commands, failures, Git identities, independent comparisons and assessment
under evidence/WO-HAG-006/. Keep old WO-HAG-005 observations as historical evidence.
Use released capture for the final record and inspect its generated destinations.
Do not rewrite older verified records or their evidence. This establishes no
hosted-service readiness, deployment, release, risk acceptance or merge decision.
