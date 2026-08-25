+++
id = "VREC-TCM-002"
type = "verification_record"
title = "Verification candidate for WO-TCM-001"
status = "verified"
owners = ["engineering-owner"]
created = "2026-08-25"
updated = "2026-08-25"
commit = "f7b69d0ad40321caa0520f9fed137be8e32bcf1f"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-25T10:40:59Z"
prepared_by = "engineering-owner"
artifact_snapshot_sha256 = "bae0e84adf246153abf1c775b0a9413cabe2dc5f54b96b54ff1e3c7b9b04597a"
evidence_paths = ["docs/engineering/technical-communication/evidence/WO-TCM-001/WO-TCM-002-verification.md"]
evaluator_evidence_path = "docs/engineering/technical-communication/evidence/VREC-TCM-002-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

verified_at = "2026-08-25T10:51:11Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-TCM-001"]
conforms_to = ["VER-TCM-001"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-25T10:51:11Z"
decided_by = "assurance-owner"
reason = "The accountable assurance owner accepted this record on 2026-08-25 with \"I accept VREC-TCM-002, you can transition it to verified, commit, push and PR I will merge\". The decision was taken with the record's disclosed limitation in front of it: VER-TCM-001's manual-assessment conditions are NOT evidenced, because the two independent reviewer judgments over rendered corpus output do not exist and no retained manual review form covers them. The owner chose to verify with that gap disclosed rather than record the reviews first or reject. The semantic and operator-comprehension acceptance conditions of VER-TCM-001 are therefore accepted residual risk on this record, not a claim of pass. Every bound field was re-measured immediately before this transition: candidate f7b69d0 is an ancestor of the branch tip and carries WO-TCM-001 as implemented; the bound evidence blob is 07603e0a at 13854 bytes, byte-identical at the candidate and on origin/main; artifact_snapshot_sha256 re-derives to bae0e84a in an independent full clone detached at the candidate with a matching directory basename; the evaluator packet is 873 CR-free bytes at fcfc1447; the graph at the candidate measures 845 artifacts, 0 errors, 50 pre-existing maintenance warnings, with governing doctor exit 0 at 87 PASS and 0 FAIL. This transition grants no release, tag, publication, or deployment authority. The record binds f7b69d0, so its provenance survives only a true merge; a squash or rebase would orphan the bound commit."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-TCM-001` to candidate commit `f7b69d0ad40321caa0520f9fed137be8e32bcf1f`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.

## Why this candidate commit exists

`WO-TCM-001`'s authorized bytes merged into `main` at `1b94c82329e8cfd94ad61601384448c4dc1ed7e3`, but the work order still read `in_progress` there, so no record could bind that commit. The repository owner accepted the work order into the 0.7.0 release unit on 2026-08-25 and authorized its completion transition. The engineering owner applied it with the released 0.6.0 evaluator at 2026-08-25T10:21:06Z, and `f7b69d0` is the governance commit carrying only that transition. `WO-TCM-001` reads `implemented` at the bound commit.

## Bound identity, re-measured before the assurance decision

A verified record cannot be corrected, so every generated figure was re-measured rather than carried forward.

| Field | Measurement |
| --- | --- |
| Candidate commit | `f7b69d0ad40321caa0520f9fed137be8e32bcf1f`, worktree clean at capture, `WO-TCM-001` reads `implemented` |
| Bound evidence blob | `07603e0a60936d0bffa45e5bb3de25663dfdcec0`, 13854 bytes, byte-identical at the candidate and on `origin/main` |
| `artifact_snapshot_sha256` | `bae0e84a` re-derived byte-identically by rerunning capture in an independent full clone detached at the candidate with a matching directory basename; only `prepared_at` differed |
| Evaluator packet | 873 bytes, zero CR, `fcfc1447`, identical to `VREC-TCM-001`'s packet because both came from the same exact public 0.6.0 evaluator venv outside the checkout |
| Graph at the candidate | 845 artifacts, 0 errors, 50 pre-existing maintenance warnings, every plane at E0 |
| Governing `doctor` at the candidate | 87 `PASS`, 0 `FAIL`, exit 0 |
| Windows suite | 943 tests, `OK`, 22 platform-guard skips, measured in the preparation worktree at this commit's content plus the untracked 0.7.0 packet |

## What the bound evidence establishes

The bound file is the combined implementation-phase evidence for both technical-communication work orders. Its directory component keys it to `WO-TCM-001` and its filename keys it to `WO-TCM-002`, so one file serves both. For `WO-TCM-001` it reports passing deterministic results against all four requirements: the single canonical and installed managed policy with its route, lock entry, preflight listing, wheel and sdist payloads, and offline install; exact byte and digest preservation for protected spans with fail-closed rejection of malformed, duplicate, overlapping, unordered, out-of-range, excessive, and digest-mismatched input; profile selection; and the strict v2 read-only skill contract with its effect sentinel, explicit-only activation, missing-current-state refusal, and unchanged baselines for the four pre-existing skills. It also records the static scan finding no positive ASD compliance claim and no retrieval implementation.

## What `VER-TCM-001` requires that this evidence does not establish

This is the material limitation on the record and the reason it is put forward as a candidate rather than as a complete pass.

`VER-TCM-001`'s **Manual assessments** section requires two reviewers to independently record the intended fact, actor, action, condition, qualification, normative force, and result **before seeing candidate output**, and states that pass requires their agreement and that disagreement is an unresolved finding rather than an averaged readability score. Its **Acceptance scenarios** include Scenario 7, which requires giving independent reviewers original and rendered examples containing `MUST`, `SHALL`, `SHOULD`, conditions, exceptions, thresholds, decision roles, and safety qualifications. Its requirement-to-evidence matrix names semantic review as a method for `REQ-TCM-002` and blinded technical review as a method for `REQ-TCM-003`. Its **Evidence retention** list requires a retained manual review form with independent judgments, dispositions, and residual findings.

Those judgments do not exist. The bound evidence states so itself: the versioned corpus of eleven bounded cases is in place and automated tests confirm its structure and exact token presence, but the two independent reviewer judgments over rendered output "are not yet recorded", they remain "required input to assurance under `VER-TCM-001`", and the evidence says directly that this "must be completed before a verification record can claim that the semantic and operator-comprehension acceptance conditions passed." The required manual review form is therefore absent from the retained evidence set.

Deterministic testing cannot substitute. It proves that declared protected spans are preserved byte for byte; it cannot prove that every semantically sensitive span was selected in the first place, nor that an operator reading a rendered brief identifies the intended outcome and one next action. That is precisely the judgment `VER-TCM-001` reserves for human reviewers.

The bound evidence is also the implementer's own handoff report, written at checkpoint `handoff` while both work orders were `in_progress`. `VER-TCM-001`'s **Independence** section does not accept implementation wording, helper output, readability scores, or model confidence as proof. The deterministic results it reports are independent in that they compare bytes, contracts, manifests, locks, and payloads against the requirements; the semantic and comprehension conclusions it does not draw are the ones still owed.

## Deviations and residual uncertainty carried forward

1. The two independent manual reviewer judgments are open, as set out above. This is the one condition that blocks a clean claim of conformance to `VER-TCM-001`.
2. Windows platform-capability skips remain active where the host provides the relevant symlink, case-collision, or optional-tool capability. None hides a failed router or technical-communication assertion, and the hosted Linux lane runs the same suite without them.
3. Both technical-communication work orders' narrative `Lifecycle` sections still describe their original draft preparation while the authoritative front matter and lifecycle events carry the current state. The released evaluator reads the structured state and every gate passes. Revising that historical narrative was outside both implementation scopes.
4. The bound evidence retains a recovered Git incident from implementation: a temporary `.git` pointer let a repository test create an unintended local commit in the source worktree, which was detected before evidence retention, reset away with all working files preserved, and never pushed. It produced no branch, index, remote, or external effect beyond the intended candidate files, and the invalid run was not used as final suite evidence.
5. `VER-TCM-001` states that passing it supports the bounded feature and establishes no ASD-STE100 compliance, endorsement, universal readability, or substantive artifact correctness. Nothing in this record claims otherwise.

## Decision before the assurance owner

Verifying this record accepts an unmet manual-assessment condition on the record. Three routes are available, and the choice belongs to the assurance owner:

- **Complete the reviews first.** Record two independent reviewer judgments over the existing eleven-case corpus, retain the manual review form under `docs/engineering/technical-communication/evidence/`, and verify afterwards. This is the only route that satisfies `VER-TCM-001` as written. A new evidence file would have to be bound, which this ready record cannot absorb; it would need a successor record.
- **Verify with the gap disclosed.** Accept the deterministic evidence as sufficient for release and treat the semantic and comprehension conditions as an accepted residual risk, recorded in the transition reason. The disclosure above then stands permanently in the graph, because a verified record cannot be corrected.
- **Reject.** Reject with a non-empty reason naming the missing judgments, leaving `WO-TCM-001` `implemented` and uncovered. `REL-SEH-012` would then need amendment, because it names `WO-TCM-001` in `gates` and its entry criteria require verified coverage for every member of the release unit.

No route is taken by preparing this record. `WO-TCM-001` was not changed by the capture, and no verification, release, push, tag, publication, or deployment authority follows from it.
