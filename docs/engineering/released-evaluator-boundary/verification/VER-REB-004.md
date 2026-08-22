+++
id = "VER-REB-004"
type = "verification"
title = "Predecessor preparation-view and rejected-version succession assurance"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[relations]
verifies = ["REQ-REB-011", "REQ-REB-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T22:17:21Z"
decided_by = "quality-owner"
+++

# Verification Contract: Predecessor preparation-view and rejected-version succession assurance

## Independence

Assurance independently selects lifecycle matrices, Git/object/path mutations, sparse-pattern contamination, runtime-origin substitutions, and rollback faults. It recomputes raw and Git hashes without using adapter-reported values and compares predecessor output to the requested release aggregate.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-REB-011` | Version lifecycle matrix | rejected/ready/released combinations for one version | Any number of valid rejected histories plus at most one active claim pass; every multiple-active combination fails |
| `REQ-REB-011` | Bootstrap history matrix | status-matched and mixed RLS/contract tuples | Exact rejected pairs remain valid; mixed, changed, or reused authority fails |
| `REQ-REB-011` | Preparation API tests | existing rejected versus ready/released versions | Rejected history does not block a successor; an active version does |
| `REQ-REB-012` | Exact-view integration | current rejected pair, successor contract/VREC/work set, external 0.5.0 | Exact predecessor command creates only the expected ready record in the two-path sparse view |
| `REQ-REB-012` | View provenance | commit/tree/blob/raw hashes, sparse spec, command, runtime, output | Canonical evidence independently reproduces every identity and byte |
| `REQ-REB-012` | Omission/path negatives | zero, one, three, unrelated, linked, escaped, changed, or ambiguous paths | Every case fails before durable repository write |
| `REQ-REB-012` | Isolation and TOCTOU | candidate import, PYTHONPATH, user site, executable/wheel/lock drift, record/evidence race | Every contamination or change fails closed with exact rollback |
| Both | Full release rehearsal | import, bootstrap bind, full candidate validation, distribution bind plan | Complete graph passes and historical bytes remain unchanged; no external action occurs |

## Acceptance scenarios

1. Exact 0.5.0 continues failing on the complete rejected-history graph, and the evidence records that boundary without treating it as successor failure.
2. The derived sparse worktree has the same exact governance HEAD and omits only `REL-SEH-008` and `RLS-SEH-009`.
3. Exact isolated 0.5.0 prepares the requested successor record with the exact candidate/VREC/work scope.
4. Candidate validation accepts rejected history plus one ready successor for unpublished `0.6.0`.
5. A second ready/released claim, an arbitrary omission, or a changed historical byte fails with zero durable write.
6. The view/evaluator evidence files remain canonical LF under default Windows and LF checkouts.

## Property and invariant tests

- Active version cardinality depends only on valid lifecycle status, never ID naming.
- Reordering artifact discovery does not change the selected pair, sparse spec, manifest bytes, or diagnostics.
- Omitted hashes match both Git blobs and independently read committed bytes.
- The predecessor output body and core fields are byte-preserved through import and bootstrap binding.
- Plan is read-only; apply is atomic, idempotent where complete, and refuses partial repair.
- Candidate commit, VREC identity, release work set, and old evaluator tuple never change.

## Static and architecture checks

- Trace both requirements through `SPEC-REB-005`, `ARCH-REB-004`, `ADR-REB-004`, and `WO-REB-006`.
- Confirm root managed files and schema-2 lock have zero diff.
- Confirm no validation allowlist, generic ignored path, hand-authored RLS fallback, candidate-root mutation, or automatic lifecycle action exists.

## Security and privacy checks

- Exercise symbolic links, junctions, case aliases, unsafe basenames, alternate Git objects/config, hostile sparse files, duplicate JSON keys, digest substitution, environment contamination, and executable replacement.
- Confirm logs/evidence contain no tokens, credentials, usernames, home paths, or environment dumps.

## Performance and resilience checks

Run focused adversarial tests and full suites on Python 3.11 and the current qualification runtime. Rehearse injected failures before view creation, after predecessor output, during exclusive evidence creation, before RLS replace, before binder apply, and during final validation; prove bounded cleanup and no historical mutation.

## Manual assessments

- Technical/security owners accept the honest split between full candidate validation and predecessor compatibility-view preparation.
- Assurance owner reviews independent hashes, exact omissions, lifecycle matrix, and complete rollback evidence.
- Release owner confirms the version is unpublished and only one active successor is proposed.

## Evidence retention

`WO-REB-006` evidence retains the original failing command/output, approved preflight manifest, complete changed paths, exact manifest schema and example, source/view Git identities, omitted Git/raw hashes, predecessor runtime/wheel/command/output identities, active-version matrix, all negative before/after maps, full test/build/package/bundle/evaluator/checkout/hosted results, and the complete list of actions not performed.

## Residual uncertainty

Sparse-worktree behavior outside supported Git versions and future predecessor formats remains outside this correction. External hosting, protected environments, publication, and root adoption require later observations and authority.
