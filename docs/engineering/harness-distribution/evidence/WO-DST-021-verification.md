# WO-DST-021 implementation and verification evidence (REQ-DST-065)

## Authority and candidate state

The repository owner approved `REQ-DST-065`, `REQ-IAR-021`, `SPEC-DST-021`, `SPEC-IAR-013`, `VER-DST-021`, `VER-IAR-013`, and `WO-DST-021` as one packet on 2026-08-21 and authorized implementation the same day. This file records the `VER-DST-021` execution for `REQ-DST-065`. The `VER-IAR-013` execution for `REQ-IAR-021` is recorded in `../../instruction-architecture/evidence/WO-DST-021-verification.md`.

At evidence finalization the implementation is an uncommitted working-tree candidate. No commit, push, pull request, verification transition, release, tag, publication, or deployment was performed, and none is authorized by the packet approval. The candidate commit hash cannot be self-recorded here; it belongs in the VREC created after that commit.

## Evaluator identity

The governing evaluator is the released package executed from outside the checkout:

```text
../se-harness-eval-1685/Scripts/python -I -m se_harness
se-harness 0.5.0
C:\Users\mathi\se-harness-eval-1685\Lib\site-packages\se_harness
```

All released-evaluator figures below come from that interpreter. In-tree runs are labelled candidate-source and are drift evidence only.

## Template-tree seed enumeration

Before (three seeds):

```text
templates/repository/standard/.github/PULL_REQUEST_TEMPLATE.md.seed
templates/repository/standard/docs/engineering/README.md.seed
templates/repository/standard/docs/engineering/REPOSITORY_CONTEXT.md.seed
```

After (two seeds):

```text
templates/repository/standard/.github/PULL_REQUEST_TEMPLATE.md.seed
templates/repository/standard/docs/engineering/README.md.seed
```

`pyproject.toml` no longer declares the deleted seed as packaged template data. `docs/engineering/README.md.seed` no longer lists the retired entry.

## Four-row lock convergence

`tests/test_repository_context_retirement.py::test_upgrade_converges_the_four_prior_states_to_one_lock` installs four repositories, drives each to one of the four possible prior states, applies the upgrade, and compares the regenerated locks byte-for-byte:

| Row | Prior file | Prior lock entry |
| --- | --- | --- |
| `absent-absent` | absent | absent |
| `present-present` | present | `seed` / `present` |
| `present-absent` | present | absent |
| `removed-absent` | absent | `seed` / `removed` |

All four regenerate one distinct lock byte-string. No entry and no tombstone for the retired path appears in any of them. `test_repeated_upgrade_is_idempotent` shows a second apply changes nothing.

## Owner content at the retired path

`test_upgrade_never_alters_owner_bytes_at_the_retired_path` writes owner-authored bytes at the retired path in an installed repository, applies the upgrade, and compares SHA-256 before and after for five cases: empty file, CRLF text, `bytes(range(256))`, long LF text, and text with no trailing newline. Every digest is unchanged. `test_upgrade_plans_no_change_for_owner_content_at_the_retired_path` shows the read-only plan proposes no operation on that path at all, so the preservation is a planning property and not a post-hoc restore.

This repository's own owner-authored copy is unchanged by the implementation:

```text
docs/engineering/REPOSITORY_CONTEXT.md  bytes=7385
sha256=67d0f43883faa3ed1f92ae653d7f77cab5ecb8f237924e3c942986e1a6098620
```

It is now ordinary untracked owner content. The absolute stop condition — deleting, moving, or rewriting an owner-authored file at the retired path — was not approached.

## Preflight payload: v1 baseline and v2 result

The independent `v1` baselines were read from the released 0.5.0 install outside this checkout and are retained at `tests/fixtures/repository_context_retirement/released-baseline.json` with their provenance line. They record schema `se-harness-preflight-v1`, the nine payload keys in order (`schema`, `ready`, `phase`, `work_order`, `assurance`, `diagnostics`, `reading_manifest`, `repository_commands`, `authority_boundary`), 12 `REQUIRED_PATHS`, 7 `POLICY_PATHS`, the retired diagnostic family `C001`–`C004`, and the 15 retired context-field labels.

Candidate result, all four runs (`WO-DST-021` and `WO-IAR-012`, `start` and `review`):

```text
schema se-harness-preflight-v2
keys ['assurance', 'authority_boundary', 'diagnostics', 'phase', 'reading_manifest', 'ready', 'schema', 'work_order']
```

Eight keys. `repository_commands` is absent rather than emitted as an empty object, which is the accepted-loss decision recorded at approval. `test_payload_advances_the_schema_and_drops_only_the_command_object` asserts the `v2` key set equals the `v1` key set minus exactly that one name. `test_reading_manifest_keeps_the_baseline_order_without_the_retired_path` asserts the manifest is the baseline order with the retired path removed and nothing reordered.

`test_retired_diagnostic_family_is_absent_from_the_emitted_code_space` writes the retired path back into an installed repository with all fifteen retired field labels left as `TODO[...]` placeholders — the exact input that previously produced `C001`–`C004` — then collects every diagnostic code emitted across four cases: `start`, `review`, an injection-shaped work-order ID, and an unknown work order. The intersection with the retired family is empty and the emitted set is non-empty, so the corpus does exercise the diagnostic path.

## Released-evaluator preflight and doctor

Before the closeout transitions, with both work orders `approved`, all four released-evaluator preflight runs PASS with exit 0:

| Work order | Phase | Result |
| --- | --- | --- |
| `WO-DST-021` | `start` | `Harness preflight: PASS` |
| `WO-DST-021` | `review` | `Harness preflight: PASS` |
| `WO-IAR-012` | `start` | `Harness preflight: PASS` |
| `WO-IAR-012` | `review` | `Harness preflight: PASS` |

After the closeout transitions to `implemented`, `review` still passes for both and `start` reports `FAIL` for both with one diagnostic:

```text
[W005] docs/engineering/harness-distribution/work-orders/WO-DST-021.md: status 'implemented'
       is not eligible for start; expected one of approved, in_progress
```

That is the designed result, not a regression: managed `WORKFLOW.md` states that start preflight accepts `approved` or `in_progress` while review preflight additionally accepts `implemented`, so completed work retains honest lifecycle status. `review` is the phase-appropriate gate from here.

The released evaluator still lists `docs/engineering/REPOSITORY_CONTEXT.md` in its reading manifest and still prints a `Repository commands:` section. That is correct: it is the `v1` product, it reads the repository's own untouched owner file, and the repository lock still carries the `seed` entry. Both are reconciled at publication through the separate upgrade workflow.

`../se-harness-eval-1685/Scripts/python -I -m se_harness doctor .` exits 0 with 81 PASS, 0 FAIL, 15 WARN. Every WARN is a pre-existing `W013` non-canonical-location maintenance warning on historical `VREC-*`/`RLS-*` records. `PASS seed:docs/engineering/REPOSITORY_CONTEXT.md: present` is expected under the released lock.

Candidate-source `preflight` reports `ready False` in-tree with 20 `I001` diagnostics, all candidate-versus-released skew. One is new and intended:

```text
{'code': 'I001', 'message': 'not in standard template', 'path': 'lock-extra:docs/engineering/REPOSITORY_CONTEXT.md'}
```

The candidate template no longer carries the seed while the repository lock, which belongs to released 0.5.0, still does. This is the designed self-hosting lag and resolves when the repository upgrades to the release carrying this change.

## Withdrawn reference-step action form

Released 0.5.0 has no `se_harness.workflow_procedures`, `se_harness.workflow_contract`, or `se_harness.workflow_compliance` module at all. The resolver and the contract validator are candidate-only, so no released consumer can be affected by the withdrawal. This is stronger than the zero-use finding recorded at drafting.

`test_resolver_exposes_no_repository_context_argument` asserts the resolver signature is exactly `(procedures, procedure_id, parameters)`; the removed repository-context argument had no caller.

Rejection precedes resolution, in `se_harness/workflow_contract.py`:

```text
['action_id']                        -> ContractError: procedure PROC-WO-START reference STEP-WO-START-FOCUS
                                        declares action_id, a withdrawn reference form; a reference step
                                        declares procedure_id only
['action_id', 'procedure_id']        -> same diagnostic
['action_id'] (unrecognized value)   -> same diagnostic
```

The withdrawn identifier is a rejected value with an explicit diagnostic rather than a silently dropped field, which is the owner decision recorded at approval: a stale contract stays distinguishable from an unrecognized field.

Resolved-procedure corpus, candidate resolver:

```text
se_harness/workflow_contract.json                              procedures=17 corpus_sha256=014cd526de4aaf88147ad5bcd495ad7803e99a0c8d235a557719bf061e5d39e3
templates/repository/standard/docs/engineering/WORKFLOW.json    procedures=17 corpus_sha256=014cd526de4aaf88147ad5bcd495ad7803e99a0c8d235a557719bf061e5d39e3
resolved step kinds: {'command': 9, 'decision': 14}
contains 'action_id': False   contains 'CTX-ACT': False
```

Both contracts resolve to one identical digest, repeat runs are identical, and no procedure in either declares a `reference` step, so the withdrawn branch was unreachable in both the packaged and template contracts.

## Fragment digests

Computed against `.engineering-harness.lock` before and after the implementation, unchanged in both directions:

| Path | Mode | Digest | Match |
| --- | --- | --- | --- |
| `.gitignore` | fragment | `1b9c8af1917e119817b7160d3afa4e7277226d187b964c318fdbb6072beeaeaa` | yes |
| `AGENTS.md` | fragment | `bcf46d13ceee8c2606834a897eba153a654f0092c1d41c8737723739a1405f1c` | yes |
| `CLAUDE.md` | fragment | `a5d3b02b3200e5dc147578f81f2b80ca4a0f055a0a4a1c94a535352572ade2cd` | yes |

Seed entries before and after: `.github/PULL_REQUEST_TEMPLATE.md` present, `docs/engineering/README.md` present, `docs/engineering/REPOSITORY_CONTEXT.md` present. The repository lock is untouched by this work order.

## Validator

Zero errors before and after the two supersessions:

```text
Engineering artifact validation: PASS
Artifacts: 605 | Errors: 0 | Warnings: 44
Planes: structure E0/W0 | governance E0/W0 | policy E0/W0 | maintenance E0/W44
```

No `E017` on `OPS-IAR-001`. Removing `REQ-IAR-005` from that contract's `assures` relation was the only validator consequence of the supersessions, as the pre-implementation measurement predicted. The warning count matches the recorded baseline of 44; every warning is a pre-existing `W013`/`W014`/`W015` maintenance finding unrelated to this change.

## Unittest suite

```text
Ran 403 tests in 162.005s
FAILED (failures=2, skipped=5)
```

Both failures are the known environment conditions of any Windows clone here, named explicitly rather than reported as regressions:

- `test_standard_repository_lifecycle.test_candidate_source_identity_is_deterministic_and_bounded` — `RID018 distribution_origin: source distribution metadata resolves outside the checkout`. The machine-wide editable `se-harness` install owns the package metadata.
- `test_workflow_documentation_contract.test_fresh_install_contains_managed_machine_contract` — raw byte comparison of `WORKFLOW.json` against a CRLF worktree.

Neither excuses a new failure, and no new failure exists. Per-module results:

| Module | Tests | Result |
| --- | --- | --- |
| `test_repository_context_retirement` (new) | 11 | OK |
| `test_context_routing_retirement` (new) | 11 | OK |
| `test_instruction_architecture` | 26 | OK |
| `test_harnessctl` | 29 | OK, 1 skipped |
| `test_workflow_procedures` | 7 | OK |
| `test_adr_applicability` | 8 | OK |
| `test_architecture_traceability` | 12 | OK |
| `test_progressive_documentation` | 17 | OK |

## Changed baselines and dropped assertions

Three assertions were removed from `test_progressive_documentation.py::test_branching_guide_is_one_explicitly_non_authoritative_model` because they read the retired document, which the harness no longer produces:

- `assertNotIn("feature/<short-description>", context)`
- `assertIn("harness-branching-model.md", context)`
- `assertIn("release/x.y", context)`

Every `branching` assertion in that test is retained, so the "one explicitly non-authoritative model" property is still covered; only the coupling to the retired file is gone.

`tests/test_instruction_architecture.py::add_active_packet` now reactivates requirements that were later superseded when it builds its synthetic active work order. Without that, the newly superseded `REQ-IAR-005` made the fixture's governing chain inactive and preflight `W013` made the report not ready. The real repository is unaffected because preflight is only run for current work orders.

`tests/test_instruction_architecture.py` retains `assertNotIn("REPOSITORY_CONTEXT.md", managed)` deliberately: it asserts the tracked fragment does not name the file.

## Governed artifacts revised

Superseded: `REQ-IAR-005`, `REQ-DST-008`.

Revised: `REQ-IAR-003` (example only, status unchanged), `REQ-WEX-010`, `SPEC-WEX-002`, `VER-WEX-002`, `SPEC-DST-002`, `SPEC-DST-006`, `SPEC-DST-007`, `SPEC-IAR-001`, `ARCH-DST-007`, `ARCH-IAR-001`, `OPS-IAR-001` (`assures` relation and prose).

Domain READMEs and acceptance features: `docs/engineering/harness-distribution/README.md`, `docs/engineering/instruction-architecture/README.md`, `acceptance/distribution.feature`, `acceptance/instruction-architecture.feature`.

## Historical records deliberately left unchanged

The work order states nine such files exist. A literal-path scan finds twelve, and all twelve are unmodified. The count in the work order does not match a literal-string scan; the scan result is recorded here as the measured figure.

```text
docs/engineering/harness-distribution/evidence/WO-DOC-007-verification.md
docs/engineering/harness-distribution/evidence/WO-DOC-009-verification.md
docs/engineering/harness-distribution/evidence/WO-DOC-013-verification.md
docs/engineering/harness-distribution/work-orders/WO-DOC-007.md
docs/engineering/harness-distribution/work-orders/WO-DOC-009.md
docs/engineering/repository-harness-upgrade/evidence/WO-HUP-001-verification.md
docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-001.md
docs/engineering/self-hosting-boundary/work-orders/WO-SHB-001.md
docs/engineering/verification-supersession/engineering-README.md
docs/engineering/work-order-assurance-classification/evidence/WO-WAC-001-verification.md
docs/engineering/workflow-execution/evidence/WO-WEX-002-verification.md
docs/engineering/workflow-execution/work-orders/WO-WEX-002.md
```

`test_only_recorded_files_name_the_retired_path` scans every `.md` file outside `target/`, `tests/`, and `templates/` and asserts the set naming the retired path equals the allowlist exactly, with a stated reason per file, so a new mention and a silently dropped one both fail. `test_historical_records_still_describe_the_retired_obligation` asserts all twelve historical records still describe it, so a silent rewrite of history would fail.

## Residue outside the authorized envelope

The work order's in-scope revision list was derived from a scan for the literal path, so it did not reach active artifacts that describe the same obligation in lowercase prose. Eleven such artifacts were measured and every one is unmodified, because revising them is outside the authorized envelope and outside the enumerated in-scope list.

Factually wrong about the candidate product and needing a follow-on governance packet with its own approval:

| Artifact | Status | Stale claim |
| --- | --- | --- |
| `VER-DST-002` | approved | requires tests proving `init` creates repository context and `doctor` rejects a missing repository-context file |
| `REQ-IAR-006` | implemented | preflight success output lists the repository-context path and the repository commands |
| `ADR-DST-002` | approved | records seeding the document once per installation lineage as the accepted decision |
| `ADR-IAR-001` | approved | records preserving repository context as an owner-owned seed |
| `INT-IAR-001` | approved | readiness blocks when repository context is invalid |
| `SPEC-WEX-002`, `VER-WEX-002` | approved | list unreadable required repository context as a failure category |

Descriptive only, correct once "repository context" is read as the owner-controlled region: `SPEC-DST-002` (title), `SPEC-DST-003`, `ARCH-DST-006`, `ADR-DST-006`.

Assessed and accurate as written, no action needed: `CAP-IAR-001`, `REQ-IAR-001`, `REQ-WEX-007`, `REQ-HUP-002`, `OPS-VSP-001`.

`ADR-DST-002` and `ADR-IAR-001` in particular cannot be touched here: the work order states that reopening an accepted ADR outcome is outside the authorization. `REQ-IAR-006` is an implemented requirement whose acceptance criterion the change now contradicts, which is the same condition that led to superseding `REQ-IAR-005` and `REQ-DST-008`. It is raised rather than resolved.

## Lifecycle transitions at closeout

Set to `implemented`: `REQ-DST-065`, `SPEC-DST-021`, `WO-DST-021`, and, under the instruction-architecture domain, `REQ-IAR-021`, `SPEC-IAR-013`.

Left at `approved`: `VER-DST-021` and `VER-IAR-013`. A verification contract is not advanced by the implementation it governs; a verification transition is a separate accountable decision and none was performed. This follows the recorded precedent of `VER-IAR-011`, which remains `approved` beside an implemented `IAR-011` packet.

Already `superseded` before closeout: `REQ-IAR-005`, `REQ-DST-008`.

After the transitions the validator and the suite were re-run and match the figures above: PASS with 605 artifacts, 0 errors, 44 warnings; 403 tests with only the two named environment conditions and 5 skips. Released-evaluator `doctor .` re-run after the transitions is exit 0 with 81 PASS, 0 FAIL, 15 WARN. All three fragment digests re-measured against the lock still match.

One test change was required at closeout: the three evidence files written under this packet name the retired path, so `PERMITTED_MENTIONS` in `tests/test_context_routing_retirement.py` gained an entry for each with the reason `retained evidence for this retirement` or `retained evidence for the owner-region revision`. Those reasons are outside the historical-record reason set, so `HISTORICAL_RECORDS` remains the same twelve files and `test_historical_records_still_describe_the_retired_obligation` still asserts twelve.

## Change surface

Product: `se_harness/preflight.py`, `se_harness/cli.py`, `se_harness/workflow_contract.py`, `se_harness/workflow_procedures.py`, `pyproject.toml`.

Templates: deleted `templates/repository/standard/docs/engineering/REPOSITORY_CONTEXT.md.seed`; revised `ENGINEERING_HARNESS.md.tpl`, `docs/engineering/WORKFLOW.md`, `docs/engineering/README.md.seed`.

Tests: six revised modules, two new modules, one new fixture.

Documentation: `docs/notes/harness-migration-repository-context-retirement.md` (new), `docs/notes/README.md`, `docs/notes/harness-installation-and-upgrades.md`, `docs/notes/developing-se-harness.md`.

Governance: five artifact status fields and the two domain READMEs at closeout, plus this file and the two companion evidence files.

No repository-root managed copy, tracked fragment block, historical record, or owner file at the retired path was edited.
