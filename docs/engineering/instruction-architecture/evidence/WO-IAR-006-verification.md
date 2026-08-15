# WO-IAR-006 implementation and verification evidence

## Scope and authority

This evidence records implementation observations for `WO-IAR-006`. The repository owner approved the complete `IAR-006` packet on 2026-08-15 with `ok go for implementation`. That instruction authorized bounded implementation and evidence only. No commit, push, pull request, VREC preparation or transition, release, tag, publication, or deployment was performed as part of this evidence run.

## Delivered behavior

- Added one authoritative, human-authored artifact applicability catalog to managed `docs/engineering/TRACEABILITY.md`.
- Cataloged exactly the twelve canonical standard artifact types with prefix, objective, required/applicable condition, valid omission or reuse, accountable owner, and primary relations.
- Distinguished formal artifacts from evidence, acceptance scenarios, source, candidate commits, dashboards, tickets, and conversations.
- Routed artifact purpose, applicability, reuse, and relation questions directly from `ENGINEERING_HARNESS.md` to `TRACEABILITY.md`.
- Added concise relative catalog links to the Tier-0 overview and simplified UML/model note without duplicating the normative table.
- Made the work-order template omit architecture by default and explain the exact conditional add/omit rule.
- Changed formal validation so `work_order.architecture` is optional when absent but remains invalid when explicitly empty.
- Changed preflight relation resolution so architecture is conditionally optional; the existing typed applicability scan still reports unselected active applicable architecture as `W022`.
- Added registry/catalog parity, responsibility, managed-copy, documentation, template, validator, and preflight tests plus executable acceptance scenarios.
- Reconciled root managed copies and the schema-2 lock through the supported transactional upgrade. `.engineering-harness.toml` and `.github/workflows/engineering-harness.yml` remained protected.

## Applicability matrix

| Case | Formal validation | Preflight | Result |
| --- | --- | --- | --- |
| No active architecture addresses selected requirements; relation omitted | pass | pass | truthful omission accepted |
| Relation present as an empty list | fail with `E005` | blocked by graph error | malformed placeholder rejected |
| Active architecture addresses an implemented requirement; relation omitted | pass structurally | fail with `W022` | applicable coverage required |
| Applicable architecture and deciding ADR selected | pass | pass | complete typed chain accepted |
| Selected architecture unrelated to selected specification or requirement | pass structurally | fail with `W021` | nominal selection rejected |
| Selected `adr_required` architecture lacks an active deciding ADR | pass structurally | fail with `W018` | decision coverage required |

## Verification results

| Command or check | Result |
| --- | --- |
| Focused catalog, architecture, progressive documentation, instruction architecture, and authoring tests | PASS; 52 tests, 1 expected skip |
| Full suite on Python 3.14.6 | PASS; 168 tests, 3 expected skips |
| Full suite on Python 3.11.9 | PASS; 168 tests, 3 expected skips |
| `python -m se_harness --help` | PASS; current command surface loaded |
| `python -m se_harness doctor .` | PASS; distribution parity, managed integrity, required files, lock, and selected governor checks passed |
| `python scripts/validate_engineering_artifacts.py --root .` | PASS; 309 artifacts, 0 errors, 40 pre-existing compatibility warnings |
| `python -m se_harness preflight . --work-order WO-IAR-006` | PASS while the work order was `in_progress` |
| `python -m se_harness upgrade .` after apply | PASS; 33 managed entries, 31 unchanged and 2 protected, with no pending update |
| `git diff --check` | PASS; line-ending conversion notices only |
| Harness Explorer generation twice | PASS; 309 artifacts, 1138 relations, 0 errors, 49 observations each run |
| Deterministic Explorer snapshot | PASS; both runs produced `3df561b7b3be083814911520731384bbb1cebf18904ec20ce8d9f91b87692b2c` |

The 40 formal warnings are retained historical location and legacy architecture compatibility advisories; no new blocking diagnostic was introduced. Explorer's larger observation count includes derived and review-oriented findings and does not substitute for formal validation.

## Managed transaction

The plan-first upgrade proposed only:

- `ENGINEERING_HARNESS.md`;
- `docs/engineering/TRACEABILITY.md`;
- `docs/engineering/templates/WORK_ORDER.template.md`;
- `scripts/validate_engineering_artifacts.py`;
- matching schema-2 lock entries.

After apply, a second plan contained no updates. Candidate tests proved canonical standard-template copies, rendered root files, package-data declarations, line-ending canonicalization, customized-content protection, and transaction idempotence. Historical formal artifacts were not rewritten.

## Deliberately unperformed package build

No wheel or sdist was built. Repository instructions require explicit authority for distribution builds, and `WO-IAR-006` did not explicitly authorize an ephemeral self-hosting qualification build. Package-data consistency was assessed through canonical-template, installer, upgrade, managed-parity, and full regression tests. A future release qualification work order may build and test the candidate distribution.

## Changed components

- Formal `IAR-006` requirement, specification, architecture, ADR, verification contract, and work order.
- Managed router, traceability policy, work-order template, validator, and schema-2 lock.
- Canonical standard-template copies of those managed files.
- Candidate preflight implementation.
- Human overview and UML/model note.
- Instruction-architecture acceptance scenarios and domain index.
- Focused catalog, architecture traceability, and progressive documentation tests.

## Residual risks and limits

- Structural tests prove catalog membership and required fields, not whether prose is wise or whether reuse claims are honest. Accountable review remains necessary.
- Automation still cannot infer architectural significance from prose or a diff; it enforces declared typed relations.
- The independently released governor continues to enforce the previously released baseline until a later release and separately governed promotion. Candidate source and tests are implementation evidence only.
- Historical compatibility warnings remain outside this work order.

## Candidate and later assurance

The clean candidate commit does not yet exist. A separately authorized commit may contain this implementation and evidence. After that commit, `harnessctl capture-verification` may prepare a later `ready` VREC bound to the exact candidate; accountable verification remains separate.
