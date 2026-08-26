# WO-DLC-001 Declared Architecture-Generation Exemption Evidence

Date: 2026-08-26

Authority: non-authoritative retained implementation evidence. This file does not approve, verify, release, publish, tag, or deploy anything. It records what was measured on one platform at one commit. Commit-bound assurance for this work order remains a separate `VREC` decision, and this file is not that decision.

artifact: WO-DLC-001
checkpoint: handoff
formal_snapshot_sha256: 0b2a5214010d0600cbe71aed1812fef1fb94f9f9f32866d1951d4f1f5f64e398
platform: Windows 11 Home 10.0.26200, Git Bash
increment: 1 of 3 in the `definition-lifecycle` domain

## 1. Governing packet and authorization

`WO-DLC-001` implements the approved `REQ-DLC-001` and `REQ-DLC-005` under `SPEC-DLC-001`, `ARCH-DLC-001`, `ADR-DLC-001`, `ADR-DLC-002` and `VER-DLC-001`. It adds no requirement and no packet artifact. The repository owner holds the engineering-owner, technical-owner, requirements-steward, assurance-owner, quality-owner, security-owner, release-owner and repository-owner roles here, so every decision below was taken by one person and none was taken by implication.

The owner approved the fourteen definitions of the packet in `1fd82e3` and then approved `WO-DLC-001` alone in `e4b391f`, explicitly declining to approve `WO-DLC-002` and `WO-DLC-003` at the same time. `DR-WO-START` was exercised at `2026-08-26T09:40:33Z`, recorded in `52fd15c`, separately from the implementation commit.

Both transitions were applied by the released 0.6.0 evaluator invoked from outside the checkout, because the in-tree CLI is refused by mutation guard `MG005` on runtime identity.

## 2. Evaluator identity and versions

```text
C:\Users\mathi\se_harness_eval_060\Scripts\python.exe -I -m se_harness --version
0.6.0
```

That evaluator runs on Python `3.14.6` and is installed in a virtual environment outside this checkout. `0.6.0` is the governing version recorded in `.engineering-harness.toml`. The candidate source in this checkout declares `0.7.0` in `pyproject.toml`; the candidate is used for implementation and tests only, never for a governing verdict, and is never invoked with `-I`.

Two distinct code paths are measured throughout and are never conflated:

- the **released lineage** — the 0.6.0 evaluator and the root `scripts/validate_engineering_artifacts.py` that belongs to it;
- the **candidate template** — `templates/repository/standard/scripts/validate_engineering_artifacts.py`, which is where this increment's change lives.

## 3. Paired measurement: base and candidate

The increment's base is `e4b391f`, the branch tip immediately before implementation, checked out in a separate worktree at `C:/Users/mathi/dlc_base_wt`. That base already carries the whole approved artifact packet, so the two ends of the pair differ only by this increment's code and documentation. The main-line merge base is `c189b58`.

Released lineage, both ends:

```text
C:\Users\mathi\se_harness_eval_060\Scripts\python.exe -I -m se_harness validate C:/Users/mathi/dlc_base_wt
Engineering artifact validation: PASS
Artifacts: 907 | Errors: 0 | Warnings: 50
Planes: structure E0/W0 | governance E0/W0 | policy E0/W0 | maintenance E0/W50
exit code 0
```

```text
C:\Users\mathi\se_harness_eval_060\Scripts\python.exe -I -m se_harness validate .
Engineering artifact validation: PASS
Artifacts: 907 | Errors: 0 | Warnings: 50
Planes: structure E0/W0 | governance E0/W0 | policy E0/W0 | maintenance E0/W50
exit code 0
```

Complete identifier sets for all four readings are retained in [`paired_lineage_measurement.json`](paired_lineage_measurement.json), which also records the base template validator run against the base tree and the candidate template validator run against the candidate tree. Set equality, not cardinality, is the recorded comparison:

| Reading | Code | Tree | Artifacts | Errors | `W013` | `W014` | `W015` | Other |
|---|---|---|---|---|---|---|---|---|
| `released_base` | 0.6.0 released | `e4b391f` | 907 | 0 | 21 | 14 | 15 | 0 |
| `released_candidate` | 0.6.0 released | candidate | 907 | 0 | 21 | 14 | 15 | 0 |
| `template_base` | base template | `e4b391f` | 907 | 0 | 21 | 14 | 15 | 6 |
| `template_candidate` | candidate template | candidate | 907 | 0 | 21 | 14 | 15 | 6 |

Both comparisons report `tracked_sets_equal` true for `W013`, `W014` and `W015`, `other_warnings_equal` true, and `zero_errors_at_both_ends` true. The six other warnings are `W024` on `RLS-SEH-001`, `RLS-SEH-002`, `RLS-SEH-004`, `RLS-SEH-005`, `RLS-SEH-006` and `RLS-SEH-007`, identical at both ends. They are the expected governor-versus-candidate gap that `WO-DLC-001`'s constraints name in advance; they are not skew and they did not move.

The candidate `W014` set is exactly:

```text
ARCH-AGR-001 ARCH-DST-001 ARCH-DST-002 ARCH-DST-003 ARCH-DST-004 ARCH-DST-005
ARCH-IAR-001 ARCH-IAR-002 ARCH-IAR-003 ARCH-PMI-001 ARCH-PYP-001 ARCH-REV-001
ARCH-VSP-001 ARCH-WLC-001
```

member for member the base set, and member for member `SELF_HOSTING_COMPATIBILITY_SET`. `W015` still contains `ARCH-IAR-004`. The `W014` count did not fall. No stop condition fired.

## 4. Scenario 1: the status is no longer an input

```text
grep -rn "LEGACY_ARCHITECTURE_STATUSES" --include=*.py --include=*.md --include=*.json .
```

The constant survives in exactly one code file: `scripts/validate_engineering_artifacts.py`, at lines 151, 2414 and 2502. That is the root managed copy, which belongs to released version `0.6.0` and which `WO-DLC-001`'s constraints and `AGENTS.md` both forbid editing. It is absent from `templates/repository/standard/scripts/validate_engineering_artifacts.py` and from `se_harness/definition_generation.py`. Every remaining match is prose in the `definition-lifecycle` artifacts that describe the removal. This is recorded as a material deviation in section 12.

For the reads themselves, `decision_assessment_state` in the candidate template spans lines 3105-3218 and contains exactly one occurrence of the word `status`, in a docstring stating that the lifecycle status is not an input. The self-contained resolver functions `_generation_declaration`, `_generation_unassessed`, `_generation_member_defect`, `resolve_definition_generation`, `_generation_approved` and `definition_generation_state` span lines 1823-1992 and contain one further occurrence, also a docstring sentence. No executable line in either region reads an architecture's status.

The two status reads that remain nearby are unrelated to the exemption and are unchanged: line 3544 reads a deciding ADR's own status when selecting active decisions, and line 3618 reads the architecture's authority to decide whether an assessed `adr_required` architecture must have an ADR. Neither is on the exemption path.

The one status set the candidate template still carries for architectures is `_CONSTRAINS_COMPLETED_STATUSES`, read by `architecture_traceability_state` for the `ARCH.constrains` compatibility classification of `TRC-008`. It is the former proxy constant, renamed to say what its single remaining reader actually uses it for, with behaviour preserved exactly. See section 12.

## 5. Scenarios 2 and 4: ablation and the empty set

[`ablation_matrix.json`](ablation_matrix.json) records fifteen full-graph runs of the candidate template validator over this repository. Fourteen remove one frozen identifier at a time and change nothing else; the fifteenth empties the set.

Unablated: 0 errors, `W014` on all 14.

Every one of the 14 ablations reports `e014_is_exactly_the_ablated_identifier` true and `w014_lost_exactly_the_ablated_identifier` true. Each ablated run has exactly one error, `E014` on the ablated architecture, and no `E015` and no other error. No ablation moved any other architecture. This is what establishes that the declaration and not the lifecycle status suppresses the error in the real run: the statuses of those 14 architectures were identical in all fifteen runs.

Empty frozen set: `E014` on all 14, `error_count` 14, no `E015`, no other error, `run_is_not_green` true. The acceptance criteria cannot be met by a change that merely stops checking.

## 6. Scenario 3: the exempt population did not move

Recorded in section 3. Zero errors at both ends of both pairs; `W013`, `W014` and `W015` identical member for member; `ARCH-IAR-004` still in `W015`.

## 7. Scenario 5: exemption never suppresses the diagnostic

```text
grep -n "W014" templates/repository/standard/scripts/validate_engineering_artifacts.py
3601:                    "W014",
```

One emission site, unconditional inside the `legacy_missing` branch, on the `maintenance` plane. There is no guard on it, no flag, no environment read, no configuration key, and no declaration field that reaches it. The declaration packet has exactly three recognized keys — `schema`, `scope` and the identifier array — and a fourth key is ignored rather than honoured; `test_no_declaration_field_turns_the_warning_off` pins that. `resolve` and `resolve_repository` are pure functions of artifact content, so two runs over the same content emit the same warning; `test_the_exemption_suppresses_the_error_and_never_the_warning` and the repeated readings in section 3 both show the diagnostic on every run.

The message text is:

```text
architecture has no decision_assessment and is exempt through
{exempt_source}; the assessment remains outstanding
```

It names the source of the exemption and no lifecycle status, satisfying `DLC-GEN-010`. `test_the_warning_names_the_declared_source_and_no_lifecycle_status` pins the absence of `implemented`, `verified` and `released` from the emitted text.

## 8. Scenario 16: declaration failure corpus

[`declaration_failure_corpus.json`](declaration_failure_corpus.json) runs both implementations over all 30 committed vectors in `tests/fixtures/definition_generation/resolution_vectors.json`. `every_case_agrees` is true: for every case the package resolver, the self-contained script resolver, and the committed expectation are identical. `unexercised_reasons` is empty — all eight stable reasons are exercised:

| Stable reason | Exercising case |
|---|---|
| `declaration must be an array of strings` | `declaration_must_be_an_array`, `declaration_members_must_all_be_strings`, `a_defective_declaration_does_not_stop_another_work_order_resolving` |
| `declaration exceeds 512 entries` | `declaration_beyond_the_bound_resolves_nothing` |
| `declaring work order has no draft-to-approved lifecycle event` | `declaration_in_an_unapproved_work_order_resolves_nothing` |
| `invalid architecture identifier` | `invalid_identifier_reason` |
| `no artifact has this identifier` | `unknown_architecture_reason`, `unresolved_declaration_leaves_the_architecture_enforced`, `declaration_at_the_bound_is_accepted` |
| `more than one artifact has this identifier` | `ambiguous_architecture_reason` |
| `declared artifact is not an architecture` | `target_is_not_an_architecture_reason` |
| `architecture already carries a decision_assessment` | `already_assessed_reason`, `stale_member_is_reported_beside_a_resolving_member` |

Three corpus obligations are not carried by the fixture and are covered by tests instead:

- **duplicate object keys.** TOML refuses a duplicate key before resolution begins, so the case cannot be expressed as a parsed-view vector. `test_a_duplicate_key_declaration_fails_closed` writes a real work-order file with the declaration field twice and asserts `DefinitionGenerationError`. Resolution fails closed; it does not fall back to the first or last value.
- **two approved 512-entry declarations resolving together.** `test_two_approved_maximal_declarations_resolve_together` resolves 1024 entries across two approved declarers in both implementations. The bound is per declaration, not per repository.
- **not aborting unrelated artifacts.** `a_defective_declaration_does_not_stop_another_work_order_resolving` shows `WO-CON-001` producing a shape defect while `WO-CON-002` still resolves `ARCH-NEW-002`.

One conflict inside the approved packet is recorded rather than resolved. `VER-DLC-001` scenario 16 lists a "`draft` target" among the failure modes that must resolve nothing. `SPEC-DLC-001` rule `DLC-GEN-005` states that the architecture's lifecycle status is not an input, and `DLC-GEN-004` lists exactly four target defects, none of which is a status. The implementation follows the specification: a `draft` declaring **work order** resolves nothing and is a defect (`declaration_in_an_unapproved_work_order_resolves_nothing`), while a `draft` **target architecture** resolves normally (`draft_status_does_not_block_a_declared_exemption`). Both readings are exercised, so a reviewer can see which behaviour was implemented and judge the contract wording separately. Treating a draft target as a defect would reintroduce the status input this increment exists to remove.

## 9. Scenario 17: the frozen set is measured, not asserted

The generating measurement is `tests/definition_generation_measurement.py`. It is read-only, takes no argument beyond a repository root, and derives the population from the graph using the **removed proxy's own criterion** — an architecture with no `decision_assessment` table whose status was `implemented`, `verified` or `released`. That criterion is deliberately historical: it reproduces exactly what the deleted constant exempted, which is the only comparison that can distinguish a measured constant from a transcribed one.

Its committed output is [`frozen_set_measurement.json`](frozen_set_measurement.json): 65 architectures, 51 carrying an assessment, 14 without, and `unassessed_with_an_ongoing_status` empty. That last field is the closure argument. Every unassessed architecture in the graph is already a member, so no architecture in this repository needs an exemption the closed set cannot give, and the set can stay closed.

Measured at the candidate of increment 1. The measurement, the committed evidence file, and the constant are compared in the suite by `test_the_generating_measurement_reproduces_the_committed_constant`, `test_the_committed_evidence_is_the_measurement_output` and `test_no_architecture_is_left_needing_an_exemption_the_set_cannot_give`, so a later edit to any one of the three fails.

The 449-identifier set of increment 3 is not measured here. It belongs to `WO-DLC-003` and, per `VER-DLC-001` scenario 20, must be measured at or after this increment lands.

## 10. Scenario 18: no forgeable exemption input

```text
grep -nE "os\.environ|getenv|datetime|date|time\.|subprocess|git|argv|\.created|\.updated|lock" se_harness/definition_generation.py
```

No match is an executable read. `.git` appears once, inside `EXCLUDED_PARTS`, as a directory name skipped by the artifact walk; no Git command, ref, object or index is consulted. The equivalent scan over lines 1823-1992 of the candidate template returns nothing at all.

Resolution reads governed artifact content only: an artifact's `id`, its `type`, the presence of a `decision_assessment` table, a work order's `lifecycle_events` chain, and the declaration packet. It reads no date, no `created` or `updated` field, no Git reference, no commit, no environment value, no command-line flag, no lock, and no installed evaluator identity. It reads nothing artifact-supplied on the exempted architecture itself beyond its identifier, its type and whether it carries an assessment — in particular not its status, which is what `test_resolution_ignores_a_status_carried_on_the_artifact_view` and `test_a_frozen_member_is_exempt_at_every_status_and_a_stranger_at_none` pin.

## 11. Scenario 19: consumer upgrade across the boundary

[`consumer_upgrade_matrix.json`](consumer_upgrade_matrix.json) records a real isolated consumer repository built at `C:/Users/mathi/dlc_consumer`, holding a complete formal chain plus one architecture that predates the assessment contract and carries a hand-authored `implemented` status. Three variants were each validated twice: once by the released 0.6.0 root validator the consumer already holds, and once by the candidate template validator it would upgrade to.

| Variant | Setup | Released 0.6.0 | Candidate |
|---|---|---|---|
| A | unassessed `implemented` architecture, no declaration | 0 errors, `W014` on `ARCH-CON-001` | **`E014` on `ARCH-CON-001`** |
| B | the same, declared by an approved work order | 0 errors, `W014` on `ARCH-CON-001` | 0 errors, `W014` on `ARCH-CON-001` |
| C | the same, carrying a real decision assessment | 0 errors, no warning | 0 errors, no warning |

This is a material breaking change for a consumer relying on the status proxy: variant A stops validating on upgrade. The remedy is forward-compatible and is proven by variant B — declare first, then upgrade. The `[definition_generation]` table is additive, so the predecessor ignores it entirely; `test_the_declaration_packet_is_additive_for_the_predecessor` asserts that the released root validator's type-specific metadata output is byte-identical with and without the packet. A consumer therefore never has to pass through a non-validating state.

The managed-file half of the scenario is unchanged pre-existing behaviour and was not re-measured: `test_upgrade_plan_is_read_only_and_apply_preserves_customized_file` and `test_upgrade_migrates_unmodified_consumer_workflow_and_blocks_customization` already hold that a customized managed file blocks before any partial replacement. This increment adds no managed file and changes no upgrade path.

The governance-migration scenario the work order asks for could not be written. Section 12 records why.

## 12. Material deviations

Five, all disclosed rather than resolved.

**12.1 The root managed validator still holds the removed constant.** `scripts/validate_engineering_artifacts.py` retains `LEGACY_ARCHITECTURE_STATUSES` and its two reads. `VER-DLC-001` scenario 1 asks for its absence from "both validator copies", but the work order's constraints, `AGENTS.md`, and the hash lock all forbid editing the root copy, which belongs to released `0.6.0`. The constant leaves the root copy when `0.7.0` is released and the templates are reinstalled, not under this work order. Consumers pinning `0.6.0` are unaffected until they upgrade, which is exactly the boundary section 11 measures.

**12.2 No governance-migration scenario could be added.** `WO-DLC-001` lists one in scope. Two independent hard constraints block it, both verified:

- `se_harness/governance_migration_contract.json` pins `implementation_sha256` of `se_harness/governance_migration.py` for all six adapters, and the module's current `sha256` equals that pin exactly. The contract JSON is **not** in `WO-DLC-001`'s `execution_scope.paths`, so touching the module would force an out-of-scope change, which is a stop condition.
- The contract's `capabilities` is a **closed set of eight names**, and `tests/fixtures/governance_migration/candidate-0.6.0-to-0.7.0.json` already lists all eight on both `predecessor` and `successor_required`. There is no capability name for this increment, so the version pair classifies compatible whatever the increment does. `test_lane_scenario_declares_the_version_the_candidate_builds` additionally asserts exactly one lane scenario, referenced from the out-of-scope `.github/workflows/candidate-evidence.yml`, so no second scenario can be added either.

`governance_migration.py`, its contract, and the lane scenario were therefore left untouched. `MigrationSurfaceTests` in `tests/test_definition_generation.py` stands in for the boundary the contract cannot declare: it pins the closed eight-name vocabulary, pins that the pair classifies compatible, and pins the additive property that makes the declare-then-upgrade path in section 11 work. That is the protection a consumer actually gets. Widening the capability vocabulary is an owner decision outside this work order.

**12.3 Three approved artifacts state something false about `W015`.** `SPEC-DLC-001`'s scope section and `VER-DLC-001`'s invariant list both say `W015` "is resolved from relation shape and is independent of status", and `WO-DLC-001`'s out-of-scope section says `E015` and `W015` "are already status-independent". None of that is true. `architecture_traceability_state` reads the architecture's status to classify an `ARCH.constrains` relation, and the managed `TRACEABILITY.md` rule `TRC-008` says so explicitly: a validator "MAY classify an unambiguous **completed** historical relation". The measured impact in this repository is zero — the `W015` set is unchanged and its 15 members are identical at both ends of the pair — and the behaviour is preserved byte-exactly by renaming the constant to `_CONSTRAINS_COMPLETED_STATUSES` rather than removing it. `SPEC-DLC-001` and `VER-DLC-001` are not in `WO-DLC-001`'s scope and so cannot be amended here. Correcting that wording, and deciding whether `TRC-008`'s status read is itself a proxy worth removing, is separate work.

**12.4 `E015`'s message still uses status language.** The `E015` text reads "completed legacy architecture without decision_assessment requires an active deciding ADR". The architecture reaching that branch is now exempt by declaration, not by being completed, so the wording is stale. `WO-DLC-001` puts `E015` out of scope and states it is unchanged, so the message was left exactly as it was. `W019` in `se_harness/preflight.py` and `W014` in the validator, both of which are in scope, do say "generation-exempt".

**12.5 The dashboard sees only frozen-set exemptions.** `scripts/generate_harness_dashboard.py` and its template are not in `WO-DLC-001`'s `execution_scope.paths`, so the dashboard was not taught to resolve a work-order declaration. A repository whose exemptions come from a declaration rather than from the frozen set will see them reflected in `validate`, `inspect` and `preflight` but not in the dashboard. In this repository all 14 exemptions come from the frozen set, so the measured difference here is nil. Extending the dashboard needs a scope amendment or its own work order.

`docs/engineering/definition-lifecycle/README.md` still says `DR-WO-START` "has not been taken, and no implementation has begun". It is not in `execution_scope.paths` and was deliberately left stale rather than edited out of scope.

## 13. Test suite

Windows, candidate source, full suite:

```text
python -m unittest discover -s tests -p "test_*.py"
Ran 1064 tests in 347.297s
OK (skipped=23)
```

The baseline at `e4b391f` is 1021 tests. The increment adds 42 in `tests/test_definition_generation.py` and 1 in `tests/test_adr_applicability.py`, which is 1064 exactly. No existing test was deleted or weakened.

One existing test was extended rather than left red. `tests/test_artifact_catalog.py::test_released_policy_copies_match_with_declared_candidate_exceptions` pins the candidate templates against the root released copies, allowing only exceptions the test itself declares. The `[definition_generation]` block and its guidance paragraph in `WORK_ORDER.template.md`, and the `TRC-007` amendment in the candidate `TRACEABILITY.md`, are now declared there as exact insertions, so the pin still fails on any undeclared divergence. `WO-DLC-001`'s expected change surface names both files, so the divergence is authorized; without the declaration the pin would simply have gone red.

All 23 skips are Windows privilege guards, unrelated to this increment: 21 require creating a symbolic link, which needs a privilege ordinary Windows developer and CI accounts do not hold, and 2 require creating hostile portable filenames Windows refuses. The Linux lane runs these without skipping. Every figure in this section is a Windows reading; a green Windows suite is not evidence about Linux and Linux figures were not obtainable locally.

Repository-required checks, candidate source:

```text
python scripts/validate_release_distributions.py --root .
SE Harness release distribution validation: PASS (1 distribution-bearing record)
exit code 0

python -m se_harness --help
exit code 0
```

## 14. Review preflight

```text
C:\Users\mathi\se_harness_eval_060\Scripts\python.exe -I -m se_harness preflight . --work-order WO-DLC-001 --phase review
Harness preflight: PASS
Phase: review
Work order: WO-DLC-001 (in_progress)

Assurance classification:
- Commit-bound verification: required
- Decided by: engineering-owner
exit code 0
```

## 15. Complete changed-path set

Twenty paths, every one inside `WO-DLC-001`'s `execution_scope.paths`:

```text
docs/engineering/definition-lifecycle/evidence/WO-DLC-001/WO-DLC-001-verification.md
docs/engineering/definition-lifecycle/evidence/WO-DLC-001/ablation_matrix.json
docs/engineering/definition-lifecycle/evidence/WO-DLC-001/consumer_upgrade_matrix.json
docs/engineering/definition-lifecycle/evidence/WO-DLC-001/declaration_failure_corpus.json
docs/engineering/definition-lifecycle/evidence/WO-DLC-001/frozen_set_measurement.json
docs/engineering/definition-lifecycle/evidence/WO-DLC-001/paired_lineage_measurement.json
docs/notes/definition-lifecycle.md
docs/notes/harnessctl-reference.md
se_harness/definition_generation.py
se_harness/preflight.py
templates/repository/standard/docs/engineering/TRACEABILITY.md
templates/repository/standard/docs/engineering/templates/ARCHITECTURE.template.md
templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md
templates/repository/standard/scripts/validate_engineering_artifacts.py
tests/definition_generation_measurement.py
tests/fixtures/definition_generation/resolution_vectors.json
tests/test_adr_applicability.py
tests/test_artifact_catalog.py
tests/test_definition_generation.py
tests/test_revision_provenance.py
```

No artifact file outside the `definition-lifecycle` domain changed. No definition's status, `lifecycle_events`, relations or bytes changed; in particular none of the 28 `implemented` architectures was edited. No root managed copy and not `.engineering-harness.lock` changed. `docs/engineering/definition-lifecycle/work-orders/WO-DLC-001.md` is excluded from the set above because its only change is the `DR-WO-START` transition, committed separately in `52fd15c`; it is not in `execution_scope.paths`, which is correct — a work order does not authorize edits to itself.

## 16. Completion report

Run through the released 0.6.0 evaluator from outside the checkout, with all twenty paths of section 15 repeated as `--changed-path` and `--changes-complete` asserted. The governing `se-harness-workflow-result-v2` restitution block, verbatim:

```text
Outcome
Completed.

Done
- Evaluated handoff compliance for WO-DLC-001.

Not done
None.

Current lifecycle state
- WO-DLC-001 is in_progress.

Decision required
engineering-owner must decide whether the authorized implementation and evidence are complete for WO-DLC-001 under DR-WO-COMPLETE; permitted outcomes: implemented, continue, reject.

Next
whether the authorized implementation and evidence are complete (PROC-WO-IMPLEMENT/STEP-WO-IMPLEMENT-DECIDE).

Command or response
Mark WO-DLC-001 implemented.
```

```text
result_sha256: d4b38b3e6e0b6bcf2bdf792d38c18c7374dc95ebb6fc13ff4396e5437aa3de33
formal_snapshot_sha256: 0b2a5214010d0600cbe71aed1812fef1fb94f9f9f32866d1951d4f1f5f64e398
canonical block: 509 bytes, UTF-8, LF
compliance.status: pass
change_set_complete: true
exit code 0
```

`QGP-G4I-SCOPE` reports 11 normalized scope paths and every changed path resolves inside them; `QGP-G4I-EVIDENCE` resolves this file against formal snapshot `0b2a5214…`. Both `QGP-G4I-PATHS` and `QGP-G4I-COMPLETE` pass. `--changes-complete` is an assertion by the actor, not proof; section 15 is the set asserted.

`formal_snapshot_sha256` is a per-checkout figure, not a per-commit one. It hashes worktree bytes, `core.autocrlf` is `true` on this workstation, and no `.gitattributes` rule pins these documentation paths, so a checkout made differently reads a different digest for the same commit. Both readings above were taken in this checkout. Appending this section did not move it: the snapshot hashes the formal artifact set and retained evidence bytes are outside it, which was confirmed by re-running the check after this section was written and observing the same `0b2a5214…` and the same 509-byte block.

The `result_sha256` figure needs one disclosure. `ADS-DIG-001` added that field under `WO-ADS-001`, so it exists in candidate `0.7.0` and **not** in the released `0.6.0` evaluator, whose schema-2 payload emits `compliance.formal_snapshot_sha256` and no restitution digest. The digest above was therefore obtained from the candidate CLI, and it is quotable only because the two evaluators produce the same block: the released 0.6.0 block and the candidate 0.7.0 block both canonicalize to the identical 509 bytes under `canonical_block_bytes`, and both report the same formal snapshot and the same `pass`. The digest describes the governing block quoted above byte for byte. The governing verdict remains the 0.6.0 run; the candidate run contributed the digest of a block it did not change.

This block is a compliance reading, not a decision. `DR-WO-COMPLETE` belongs to the engineering-owner and has not been exercised; `WO-DLC-001` remains `in_progress`.
