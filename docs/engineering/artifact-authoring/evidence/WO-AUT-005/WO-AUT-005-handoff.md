```toml
artifact = "WO-AUT-005"
checkpoint = "handoff"
formal_snapshot_sha256 = "e1a25c87b0af11eb0c04b4041d7e899d36513082d22437ca5c0fe1bd46ff1a24"
rebound_at = "2026-09-08T18:15:40Z"
```

# WO-AUT-005 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The corpus no longer holds what the three compatibility windows tolerate.
Fifteen implemented architectures carry `addresses` and `conforms_to` instead
of the retired `constrains`; fourteen of them gained a retroactive
`[decision_assessment]` naming their deciding ADR, and the fifteenth
(`ARCH-IAR-004`) already had one. All 271 requirements that held a string
`verification_method` now hold an array from the closed vocabulary, each
keeping its original string in `verification_notes`: 267 mapped by the rules
of `REQ-AUT-003`, four decided as a steward. The one-shot script left
`scripts/`, retained here, with its two tests and the paragraph of
`docs/notes/artifact-authoring.md` that described it. `SPEC-AUT-001` carries
the amendment record of `AUT-MIG-008`, and `CorpusMigrationTests` in
`tests/test_artifact_authoring_policy.py` holds the corpus invariant.

The released 0.16.0 evaluator reads 0 errors and no `W014` or `W015` on the
candidate, with every other count equal to the baseline. No product module,
managed path or validator branch changed: closing the windows is the
following work order (`AUT-MIG-012`).

## Evaluators

- Governing: released `se-harness 0.16.0` outside the checkout
  (`C:/Users/mathi/se-harness-eval-0160`, installed from the wheel file, run
  with `-I`) for `identity`, `validate`, `doctor`, this packet and the
  handoff check. `identity --role released-evaluator` passed at start with
  `--expected-version 0.16.0`.
- Candidate: this checkout, branch `wo/aut-005-corpus` off `main` at
  `517dc5f6` (the merge of PR #411). `main` had not moved when this packet
  was written, so no merge was needed for the constraint that no concurrent
  requirement keeps a string method unnoticed.
- Commits: `0b99d754` (start), `b5bb8f26` (the architectures), `9684383d`
  (the vocabulary, the retirement, the corpus test, `SPEC-AUT-001` and the
  index), and the commit carrying this packet.

## The fifteen architectures (AUT-MIG-001 to AUT-MIG-004)

Every rewrite was applied by `migrate_architecture_relations.py`, retained
beside this file with its applied report and a second run that finds nothing
left to migrate. Triggers are numbered by the legend below; each rationale
names the deciding ADR and each file gained a `## Amendment record` section
and a bumped `updated`.

| Architecture | `conforms_to` | `addresses` | Deciding ADR | Triggers |
| --- | --- | ---: | --- | --- |
| `ARCH-AGR-001` | `SPEC-AGR-001` | 8 | `ADR-AGR-001` | 3, 4, 11, 12 |
| `ARCH-DST-001` | `SPEC-DST-001` | 6 | `ADR-DST-001` | 1, 4, 11, 12 |
| `ARCH-DST-002` | `SPEC-DST-002` | 1 | `ADR-DST-002` | 2, 3, 11, 12 |
| `ARCH-DST-003` | `SPEC-DST-003` | 5 | `ADR-DST-003` | 3, 8, 12 |
| `ARCH-DST-004` | `SPEC-DST-004` | 1 | `ADR-DST-004` | 3, 8, 12 |
| `ARCH-DST-005` | `SPEC-DST-005` | 4 | `ADR-DST-005` | 2, 10, 11, 12 |
| `ARCH-IAR-001` | `SPEC-IAR-001` | 8 | `ADR-IAR-001` | 1, 2, 10, 12 |
| `ARCH-IAR-002` | `SPEC-IAR-002` | 1 | `ADR-IAR-002` | 2, 10, 12 |
| `ARCH-IAR-003` | `SPEC-IAR-003` | 1 | `ADR-IAR-003` | 2, 10 |
| `ARCH-IAR-004` | `SPEC-IAR-004` | 1 | `ADR-IAR-004` | 10, 11, 12 (pre-existing) |
| `ARCH-PMI-001` | `SPEC-PMI-001` | 7 | `ADR-PMI-001` | 3, 5, 11, 12 |
| `ARCH-PYP-001` | `SPEC-PYP-001` | 5 | `ADR-PYP-001` | 5, 6, 8, 11, 12 |
| `ARCH-REV-001` | `SPEC-REV-001` | 8 | `ADR-REV-001` | 3, 4, 10, 11 |
| `ARCH-VSP-001` | `SPEC-VSP-001` | 7 | `ADR-VSP-001` | 3, 4, 11, 12 |
| `ARCH-WLC-001` | `SPEC-WLC-001` | 6 | `ADR-WLC-001` | 3, 10, 12 |

Every assessment reads `outcome = "adr_required"` and
`assessed_by = "technical-owner"`. `ARCH-IAR-004`'s assessment is the one that
predates this work order: it was left byte-for-byte as it stood, so its
rationale does not name `ADR-IAR-004` the way the fourteen written here name
theirs. `AUT-MIG-003` and `AUT-MIG-004` bind the fourteen. Trigger legend,
this packet's shorthand
for the evaluator's twelve controlled values: 1 `system-boundary`,
2 `responsibility-or-dependency-direction`, 3 `public-interface-or-protocol`,
4 `data-ownership-or-persistence`, 5 `security-privacy-or-trust-boundary`,
6 `deployment-or-operating-model`,
7 `concurrency-consistency-reliability-or-failure-strategy`,
8 `technology-framework-vendor-or-external-service`,
9 `material-performance-scalability-or-cost-tradeoff`, 10 `cross-cutting-policy`,
11 `difficult-to-reverse`, 12 `material-alternatives`.

Two corpus cases fell outside the literal rules; both were measured and
decided by the accountable owner before any file was written.

- Three architectures (`ARCH-AGR-001`, `ARCH-PMI-001`, `ARCH-VSP-001`)
  constrained only their specification, so `addresses` had no legacy source.
  Their `addresses` is the conforming specification's active `specifies` set
  (8, 7 and 7 requirements), which matches the convention of 55 of the 67
  already-typed architectures.
- `REQ-DST-008` and `REQ-IAR-005` are `superseded`. An active architecture
  may not address an inactive requirement, so they are omitted from
  `addresses` on `ARCH-DST-002` and `ARCH-IAR-001`; each amendment record
  states the omission and the surviving `specifies` edge. Neither
  requirement's own file was touched.

## The verification-method vocabulary (AUT-MIG-005 to AUT-MIG-007)

`migrate_verification_methods.py` ran once with `--apply` over the 32
`requirements/` directories of the scope: 267 files mapped, 96 already held
an array, 4 could not be mapped. A second run mapped nothing and wrote
nothing (363 skipped, 4 unmatched); both reports are retained.

| Mapped form | Requirements |
| --- | ---: |
| `["test"]` | 150 |
| `["test", "inspection"]` | 85 |
| `["inspection"]` | 22 |
| `["analysis"]` | 4 |
| `["inspection", "demonstration"]` | 3 |
| `["test", "analysis"]` | 2 |
| `["demonstration"]` | 1 |

The four the rules cannot map are the steward decisions of `AUT-MIG-006`,
applied by `apply_steward_decisions.py` and recorded with their reasons in
`steward-decisions.json`. Each names an automated suite in words the mapping
rules do not recognise, and each reads `["test"]` with the original string in
`verification_notes`.

| Requirement | Original string |
| --- | --- |
| `REQ-REB-004` | `automated-active-surface-invariant` |
| `REQ-REB-011` | `automated-release-version-lifecycle-matrix` |
| `REQ-REB-014` | `automated-python311-linux-windows-failure-injection-matrix` |
| `REQ-REB-018` | `automated-contract-consumer-conformance` |

## Readings

Validator readings are the released evaluator's `validate .`, counted per
code in `validator-readings.json`.

| Reading | Errors | `W013` | `W014` | `W015` | Advisories |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline, `main` at `517dc5f6` | 0 | 44 | 14 | 15 | 0 |
| After the architecture rewrite | 0 | 44 | 0 | 0 | 0 |
| After the vocabulary migration | 0 | 44 | 0 | 0 | 0 |

`doctor .` completed with 97 checks, none failed, and the same 44 `W013`
canonical-location warnings. `python scripts/validate_release_distributions.py
--root .` passed over 13 distribution-bearing records.

`python scripts/run_tests.py` ran 1,056 tests in 157 classes with 22 skipped
and the two known Windows-only failures of this machine, both unrelated to
this work order: `test_instruction_architecture` reads the owner region at
6,024 bytes against a 6,000-byte bound because the worktree is CRLF, and
`test_artifact_authoring`'s allocation test raises `PermissionError` deleting
a temporary `.git`. `tests/test_artifact_authoring_policy.py` alone runs 10
tests green, including the four of `CorpusMigrationTests`.

## Rule by rule (SPEC-AUT-003)

| Rule | Evidence |
| --- | --- |
| `AUT-MIG-001` | 15 architectures hold `addresses` and `conforms_to`; no architecture holds `constrains` (`CorpusMigrationTests`) |
| `AUT-MIG-002` | `conforms_to` also names every active specification specifying an addressed requirement; the script refuses an addressed requirement no conforming specification specifies |
| `AUT-MIG-003` | 14 assessments added, `outcome = "adr_required"`, controlled triggers, `assessed_by = "technical-owner"` |
| `AUT-MIG-004` | each rationale names the deciding ADR; each file gained a `## Amendment record` and a bumped `updated` |
| `AUT-MIG-005` | one applied run of the retained script; the second run maps nothing |
| `AUT-MIG-006` | four steward decisions to `["test"]` with the original in `verification_notes` and a reason each |
| `AUT-MIG-007` | no requirement holds a string method; the script, its tests and the note paragraph are gone |
| `AUT-MIG-008` | `SPEC-AUT-001` amendment record, applied by `amend_spec_aut_001.py` |
| `AUT-MIG-009` | `CorpusMigrationTests` (four tests) in `tests/test_artifact_authoring_policy.py` |
| `AUT-MIG-010` | the readings table: 0 errors, no `W014` or `W015`, `W013` and advisories unchanged |
| `AUT-MIG-011` | the change set below |
| `AUT-MIG-012` | no file under `se_harness/` is in the change set; the windows stay open |

## Change set

- 271 requirement front matters, two lines each (`verification_method`,
  `verification_notes`).
- 15 architecture front matters and amendment records.
- `docs/engineering/artifact-authoring/specifications/SPEC-AUT-001.md`,
  `README.md` and `work-orders/WO-AUT-005.md`.
- `docs/notes/artifact-authoring.md`: the migration paragraph removed, the
  heading now `## Approval predicates`.
- `tests/test_artifact_authoring_policy.py`: two tests removed, four added.
- `scripts/migrate_verification_methods.py` deleted, retained byte-identical
  in this directory.
- This packet: three scripts, five reports and this file.

## Disclosures

1. Deleting the migration test also removed
   `test_repository_dry_run_report_is_retained_and_matches_a_fresh_run`
   beside it. That test is not named in the work order, but it read the same
   deleted script and cannot survive its removal; `tests/` is in scope and
   `AUT-MIG-007` forces the deletion. Nothing else in the module changed
   beyond the class rename to `ApprovalPredicateTests`, the now-dead
   `load_module` import and the appended class.
2. A pre-existing defect found while editing that module, outside this work
   order's change surface and left untouched: a stray top-level
   `if __name__ == "__main__":` at line 188 of
   `tests/test_artifact_authoring_policy.py` on `main` swallows the two
   `REQ-AUT-007` advisory tests
   (`test_advisories_are_raised_only_on_drafts` and
   `test_advisories_are_reported_apart_in_the_summary_the_listing_and_the_json`)
   into its block, so they belong to no class and the loader never collects
   them. It has been so since `479328934` (2026-08-25).
   `WO-TST-004`'s discovered-equals-defined count cannot see them, because
   they are defined in no class namespace. The advisory class of `WO-AUT-004`
   therefore has two written but never-executed tests. It needs a decision
   and a work order of its own.
3. The two owner decisions of the architecture section (the specification's
   `specifies` set as `addresses`; the two `superseded` requirements omitted)
   were taken on the presented options before any file was written.
4. The two Windows-only suite failures above are this machine's, present on
   `main`; the hosted lanes are the governing reading.
5. `updated` moved to `2026-09-08` on the 15 architectures and on
   `SPEC-AUT-001`. No status, statement, title or ADR relation changed, and
   no requirement body was touched.
