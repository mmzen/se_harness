+++
id = "VREC-DLC-001"
type = "verification_record"
title = "Verification candidate for WO-DLC-001"
status = "ready"
owners = ["engineering-owner"]
created = "2026-08-26"
updated = "2026-08-26"
commit = "f5dd99f27b6a3fe9647bc366baf12ce52c95604d"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-26T14:53:09Z"
prepared_by = "engineering-owner"
artifact_snapshot_sha256 = "9c29c0bb9c3e26fbf6a5532aa740b7ed93d7d6280d18173182abb4f77a7e5758"
evidence_paths = ["docs/engineering/definition-lifecycle/evidence/WO-DLC-001/WO-DLC-001-verification.md", "docs/engineering/definition-lifecycle/evidence/WO-DLC-001/ablation_matrix.json", "docs/engineering/definition-lifecycle/evidence/WO-DLC-001/consumer_upgrade_matrix.json", "docs/engineering/definition-lifecycle/evidence/WO-DLC-001/declaration_failure_corpus.json", "docs/engineering/definition-lifecycle/evidence/WO-DLC-001/frozen_set_measurement.json", "docs/engineering/definition-lifecycle/evidence/WO-DLC-001/paired_lineage_measurement.json"]
evaluator_evidence_path = "docs/engineering/definition-lifecycle/evidence/VREC-DLC-001-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

[relations]
verifies_work_order = ["WO-DLC-001"]
conforms_to = ["VER-DLC-001"]
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-DLC-001` to candidate commit `f5dd99f27b6a3fe9647bc366baf12ce52c95604d`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.

## Why this candidate commit exists

`WO-DLC-001`'s authorized bytes are in `5e25388`, the implementation commit. No record can bind that commit, because `WEX301` refuses capture while the work order is not `implemented` and it still read `in_progress` there. The engineering-owner exercised `DR-WO-COMPLETE` on 2026-08-26 after the handoff checkpoint passed, and `f5dd99f` is the governance commit carrying only that transition. `WO-DLC-001` reads `implemented` at the bound commit. The implementation bytes are identical in both commits; `f5dd99f` differs from `5e25388` only by the work order's own status line and its new lifecycle event.

Nothing in this domain is merged. This record therefore binds a branch commit, and its provenance survives only a true merge. A squash or a rebase would orphan `f5dd99f`, and a verified record can never be re-pointed at a later commit — the only remedy would be supersession with every field measured afresh.

## Bound identity, re-measured before the assurance decision

A verified record cannot be corrected, so every generated figure was re-measured rather than carried forward from the capture run or from the implementation session.

| Field | Measurement |
| --- | --- |
| Candidate commit | `f5dd99f27b6a3fe9647bc366baf12ce52c95604d`, worktree clean at capture and in an independent clone, `WO-DLC-001` reads `implemented` |
| `artifact_snapshot_sha256` | `9c29c0bb` re-derived byte-identically by rerunning capture in an independent full clone detached at the candidate with a matching directory basename; only `prepared_at` differed |
| Evaluator packet | 873 bytes, zero CR, `fcfc1447`, identical to earlier records' packets because it came from the same exact public 0.6.0 evaluator venv outside the checkout |
| Graph at the candidate | 907 artifacts, 0 errors, 50 maintenance warnings, every other plane at E0/W0 |
| Diagnostic sets at the candidate | `W013` 21, `W014` 14, `W015` 15 |
| Graph at the merge base `c189b58` | 890 artifacts, 0 errors, 50 maintenance warnings; `W013` 21, `W014` 14, `W015` 15, and the `W014` members identical to the candidate's |
| Governing `doctor` at the candidate | 87 `PASS`, 0 `FAIL`, exit 0 |
| Windows suite at the candidate | 1064 tests, `OK`, 23 platform-guard skips |

Bound evidence blobs at the candidate, each CR-free:

| File | Blob | Bytes |
| --- | --- | --- |
| `WO-DLC-001-verification.md` | `b34a1b59` | 29250 |
| `ablation_matrix.json` | `9913a064` | 9554 |
| `consumer_upgrade_matrix.json` | `c8b6d876` | 1773 |
| `declaration_failure_corpus.json` | `2b2fd450` | 17000 |
| `frozen_set_measurement.json` | `e9ad4789` | 765 |
| `paired_lineage_measurement.json` | `4df48453` | 7526 |

Those byte figures are the LF blobs as committed. The implementation session quoted larger numbers for five of the six files; those were pre-normalization CRLF readings taken before the files were converted, and they are superseded here rather than carried forward.

The merge-base reading is the stronger of the two population measurements and was taken for this record. `VER-DLC-001` asks for validation at the merge base and the candidate; `890` artifacts against `907` is the packet's own seventeen artifacts and nothing else, the warning total is `50` at both, and the fourteen `W014` members are identical. The exempt population did not move from `main` through to the candidate.

## What the bound evidence establishes

The bound set is one verification document and five machine-readable measurement records, all retained under `docs/engineering/definition-lifecycle/evidence/WO-DLC-001/`.

For the increment-1 subset of `VER-DLC-001` it reports passing deterministic results: the lifecycle status is no longer read on the exemption path in either candidate surface; the exempt population is unchanged at both ends of a paired lineage measurement; all fourteen single-identifier ablations isolate exactly one `E014` with no other error and no `E015`; the empty frozen set fails loudly with fourteen errors rather than passing quietly; the maintenance warning is emitted unconditionally from a single site with no flag, field, environment value, or declaration key able to reach it; all eight stable declaration-defect reasons are exercised and both implementations agree with the committed expectation on all thirty vectors; the frozen constant is reproduced from a committed generating measurement using the removed proxy's own criterion, with no architecture left needing an exemption the closed set cannot give; resolution reads no date, Git reference, environment value, argument, subprocess, or lock; and a real consumer repository built against released 0.6.0 code shows the breaking change and the forward-compatible declare-then-upgrade remedy.

## What `VER-DLC-001` requires that this evidence does not establish

This record covers **increment 1 only**. `VER-DLC-001` is the single verification contract for all three increments of the domain, and it is not established by this record.

Scenarios 6 to 13 belong to `WO-DLC-002` and scenarios 14, 15 and 20 to `WO-DLC-003`. Neither work order is approved. No part of this record claims the contract passes as a whole, and a later record for those increments is required before it can.

Three obligations inside the increment-1 subset are open and are the reason this is a candidate rather than a complete pass.

**The applicable manual assessment does not exist.** `VER-DLC-001`'s **Manual assessments** section requires assurance reviewers to confirm, without reading the implementation, that the `W014` diagnostic text asserts only that a fact is declared and never that a decision was taken, by whom, or when. That independent judgment is not recorded and no manual review form covers it. The retained evidence pins the mechanical half — the emitted text contains no lifecycle status word and names the exemption's source — and a deterministic test cannot settle the semantic half. The section states that reviewer disagreement is an unresolved finding rather than an averaged judgment, so this is a condition owed, not a condition met. The remaining five bullets of that section concern `DR-DEFINITION-DECIDE`, the `WORKFLOW.md` state table, `W025`, the derived coverage output, and the increment-3 449-entry constant; all belong to later increments.

**Two performance-and-resilience conditions are only partly evidenced.** The paired measurement was repeated and every figure is labelled by platform, and the static scan establishes no network and no subprocess. Resolution linearity was reasoned from the code shape and pinned by a maximal two-declaration case rather than measured as a timing curve, and the interrupted-validation condition — interrupt a run and confirm no repository byte changed — was not exercised at all.

**Every figure in this record is a Windows reading.** No Linux measurement was obtainable locally. `VER-DLC-001` states directly that a green Windows reading is not evidence about Linux and the reverse. The hosted lanes have not run this branch, because nothing is pushed.

## Deviations and residual uncertainty carried forward

Seven deviations were disclosed to the owner before `DR-WO-COMPLETE` and accepted as residuals. Two carry an explicit owner decision of 2026-08-26, recorded in the work order's transition reason.

1. **The root managed validator still holds the removed proxy constant.** `LEGACY_ARCHITECTURE_STATUSES` survives in `scripts/validate_engineering_artifacts.py` at three lines. Scenario 1 asks for its absence from both validator copies; the root copy belongs to released `0.6.0` and this work order, `AGENTS.md`, and the hash lock all forbid editing it. Satisfied for the candidate surfaces only. It leaves the root copy when `0.7.0` is released.
2. **Three approved artifacts state something false.** `SPEC-DLC-001`, `VER-DLC-001` and `WO-DLC-001` all assert that `W015` and `E015` are already status-independent. They are not: `architecture_traceability_state` reads the architecture's status to classify an `ARCH.constrains` relation, and the managed `TRC-008` speaks explicitly of an unambiguous **completed** historical relation. Measured impact is zero — `W015` holds fifteen identical members at the merge base, the branch base and the candidate — and behaviour is preserved byte-exactly by renaming the constant to `_CONSTRAINS_COMPLETED_STATUSES`. **Owner decision:** recorded as a residual for correction under a later dedicated work order. Neither artifact is in this work order's scope, and `WO-DLC-002`'s draft scope contains neither the specifications nor the verification directory and puts `W015` and `E015` out of scope explicitly.
3. **`VER-DLC-001` scenario 16 contradicts `SPEC-DLC-001` rule `DLC-GEN-005`.** The scenario lists a `draft` target among the failure modes that must resolve nothing; the rule states the architecture's lifecycle status is not an input, and `DLC-GEN-004` lists four target defects, none of them a status. The specification governs and was implemented. Both readings are exercised by committed vectors so a reviewer can see which behaviour exists and judge the wording separately. Carried under the same owner decision as item 2.
4. **A listed deliverable was not delivered.** Line 86 of the work order asks for a governance-migration scenario for the version pair this increment lands in. `governance_migration_contract.json` byte-pins the module for all six adapters and is not in `execution_scope.paths`, and the contract's `capabilities` is a closed set of eight names that the candidate fixture already lists in full on both sides, so the pair classifies compatible whatever this increment does. Producing the scenario would have required changing a path outside scope, which is one of this work order's own stop conditions. **Owner decision:** accepted as an authorized stop. `MigrationSurfaceTests` stands in, pinning the closed vocabulary, the compatible classification, and the additive property the upgrade remedy depends on. The contract cannot express a post-0.6.0 boundary at all; widening it is separate work and has not been scoped.
5. **`E015`'s message still uses status language.** It reads "completed legacy architecture without decision_assessment requires an active deciding ADR", but an architecture reaching that branch is now exempt by declaration rather than by being completed. `E015` is out of scope and its behaviour is unchanged, so the text was left exactly as it was. `W014` and preflight's `W019`, both in scope, say "generation-exempt".
6. **The dashboard sees only frozen-set exemptions.** `scripts/generate_harness_dashboard.py` is not in scope, so it was not taught to resolve a work-order declaration. A repository whose exemptions come from a declaration will see them in `validate`, `inspect` and `preflight` but not in the dashboard. All fourteen exemptions in this repository come from the frozen set, so the measured difference here is nil. This compounds the dashboard limit `VER-DLC-001` already records under **Residual uncertainty**.
7. **A consumer relying on the status proxy breaks on upgrade.** Measured against real released code: an unassessed `implemented` architecture with no declaration validates under `0.6.0` and raises `E014` under the candidate. The remedy is declare-then-upgrade, proven end to end, and the declaration packet is additive so the predecessor ignores it and the repository never has to pass through a non-validating state. This is a behaviour change, not a defect, and it is the intended effect of the requirement.

Two further limits are inherited from the contract rather than introduced here. The frozen set is correct only as of the commit at which it was measured, and nothing but the recorded measurement commit and its comparison test stands behind that. And an operator reading one of the exempt architectures still sees a lifecycle status that no longer carries the meaning the proxy gave it; the domain declines to close that by editing the records.

`docs/engineering/definition-lifecycle/README.md` still states that `DR-WO-START` has not been taken and no implementation has begun. It is not in `execution_scope.paths` and was left stale rather than edited out of scope.

Nothing in this record grants release, tag, publication, or deployment authority.
