# WO-AUT-002 implementation evidence

artifact: WO-AUT-002
checkpoint: handoff
formal_snapshot_sha256: 5d0124c6baaea3c89886b250668e9d6472f9e58ca23d0c2f820fe1f08e225539

Retained by the implementation actor on 2026-08-25. This file is evidence. It
does not complete, verify, or release the work order.

## Evaluators

- Governing: released `se-harness 0.6.0` installed outside the checkout from
  the exact wheel `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
  (`C:\Users\mathi\se-harness-eval`, invoked with `-I`).
- Candidate: this checkout, `python -m se_harness` from the repository root.
  The predicates and the migration are exercised against installed targets in
  `tests/test_artifact_authoring_policy.py`; this repository's own root keeps
  the 0.6.0 copies.

## What was built

- **Approval predicates (REQ-AUT-005).** `QGP-G1-AUTHORING` in
  `QG-G1-DEFINITION` and `QGP-G2-AUTHORING` in `QG-G2-ARCHITECTURE`, both on
  the new evaluator `authoring_ready` (`se_harness/workflow_compliance.py`).
  The evaluator fails when the artifact's prose — fenced and inline code and
  the front matter's `#` comment lines removed — still carries a
  `<placeholder>`, or when the first non-empty line under `## Open decisions`
  is not `None`. `ensure_governed_checkpoint` applies it to any definition-type
  artifact moving from `draft` to `approved`; the transition is refused with
  the predicate identifier and the offending text, and no state changes.
  `se_harness/quality_gates_contract.json` and the standard template
  `QUALITY_GATES.json` are byte-identical; `QUALITY_GATES.md` documents the
  evaluator and the two bindings.
- **Migration (REQ-AUT-003), built and not run on this repository.**
  `scripts/migrate_verification_methods.py` (repository-owned) maps every
  string `verification_method` to the closed vocabulary by keyword —
  `test → test`; `review | inspection | walkthrough → inspection`;
  `analysis | assessment | replay → analysis`;
  `demonstration | rehearsal | end-to-end → demonstration` — writes the array
  in front-matter order, keeps the original string as `verification_notes`,
  and reports. Dry run is the default and writes nothing; `--apply` rewrites
  only the `verification_method` line and adds `verification_notes`; a second
  run is a no-op; an unparseable front matter is refused with exit 2 before
  any file is touched; a value matching no rule is reported `unmatched` and
  left for the requirements steward.
- **Dry-run report** retained at
  `docs/engineering/artifact-authoring/evidence/WO-AUT-002/verification-method-mapping.json`:
  252 requirements, 248 mapped, 4 unmatched, 0 skipped. A fresh dry run
  reproduces the counts (asserted by test).

## Commands and results

| Command | Evaluator | Result |
| --- | --- | --- |
| `harnessctl preflight . --work-order WO-AUT-002 --phase review` | released 0.6.0 | `PASS` |
| `harnessctl validate .` | released 0.6.0 | PASS, 902 artifacts, 0 errors, 50 warnings |
| `harnessctl doctor .` | released 0.6.0 | 0 FAIL |
| `python scripts/validate_release_distributions.py --root .` | candidate | PASS (1 distribution-bearing record) |
| `python -m se_harness --help` | candidate | exit 0 |
| `git diff --check` | git | clean |
| `cmp se_harness/quality_gates_contract.json templates/…/QUALITY_GATES.json` | — | identical |
| `python scripts/migrate_verification_methods.py --root . --report …/verification-method-mapping.json` | candidate | dry run: 248 mapped, 4 unmatched, 0 skipped; no file rewritten (`git status` shows no requirement changed) |
| `harnessctl check . --artifact WO-AUT-002 --checkpoint handoff --changed-path … --changes-complete --json` (complete set below) | released 0.6.0 and candidate | before this file existed: blocked only by `QGP-G4I-EVIDENCE`; both report formal snapshot `5d0124c6baaea3c89886b250668e9d6472f9e58ca23d0c2f820fe1f08e225539` |
| `python -m unittest tests.test_artifact_authoring_policy` | candidate | 14 tests, OK (5 from WO-AUT-001, 4 new, plus the shared fixture cases) |
| `python -m unittest` over `test_workflow_documentation_contract`, `test_validation_taxonomy`, `test_artifact_authoring_policy`, `test_workflow_execution.AgentDirectiveSurfaceTests` | candidate | 63 tests, OK, 1 skip (before the four new tests were added) |
| `python -m unittest discover -s tests -p "test_*.py"` | candidate, Windows 11, CPython 3.14 | `Ran 1016 tests in 369.800s` — `OK (skipped=23)`; the 23 skips are the Windows-only guards |
| Linux lane | `.github/workflows/candidate-evidence.yml` | not run locally; the pull-request run is the Linux figure |

## Test coverage added

`tests/test_artifact_authoring_policy.py::ApprovalPredicateAndMigrationTests`:

- the two definition gates carry the authoring predicate in the loaded contract;
- a fresh `REQ-002` from the template is refused approval (`QGP-G1-AUTHORING`,
  the placeholder named, status still `draft`); with every placeholder filled
  and one open decision written it is refused again naming the decision; with
  `None.` it is approved — the `acceptance/<REQ-ID>.feature` mention inside
  inline code does not count as a placeholder;
- the mapping rules on five values including one unmatched; dry run leaves
  the file byte-identical and reports `mapped`; `--apply` writes the array and
  `verification_notes`, the candidate validator then reports no `E-AUT` and no
  `W-AUT-004`; a second `--apply` is a no-op; an unparseable front matter is
  refused with exit 2;
- the retained repository report is a dry run with 0 skipped and matches a
  fresh run, and no requirement in this repository carries the array form.

## Deviations from the specification, recorded for the completion decision

1. **String `verification_method` stays a warning; the migration was built and
   not applied here.** `SPEC-AUT-001` has the string form become `E-AUT-001`
   once the migration has run. This repository's root validator is the
   released 0.6.0 copy, which requires a *string* `verification_method`
   (`scripts/validate_engineering_artifacts.py`, the requirement branch), so
   applying the migration to `docs/engineering/*/requirements/` here would
   make the governing `validate` red for every requirement. Owner decision
   taken interactively before implementation: build the migration, retain the
   dry-run report, and leave the promotion to error and the repository-wide
   application to the governor-upgrade transaction (`WO-HUP-005`), whose
   execution scope must then include `docs/engineering/*/requirements/` and
   `scripts/migrate_verification_methods.py`.
2. **Four values match no rule.** `REQ-REB-004`
   (`automated-active-surface-invariant`), `REQ-REB-011`
   (`automated-release-version-lifecycle-matrix`), `REQ-REB-014`
   (`automated-python311-linux-windows-failure-injection-matrix`) and
   `REQ-REB-018` (`automated-contract-consumer-conformance`). The mapping rules
   are the specification's; adding an `automated → test` rule is a
   specification change. These four are a requirements-steward decision at
   application time; the report lists them as `unmatched`.
3. **Untouched in-scope paths.** `WORKFLOW.json`, `WORKFLOW.md`,
   `se_harness/workflow_contract.json` and the template validator are in the
   execution scope and unchanged: the predicates bind to existing gates and
   need no lifecycle change, and the validator change (promotion to error) is
   deferred with deviation 1.
4. **Predicate scope on the released governor.** The predicates live in the
   candidate contract and the standard template; this repository's root
   `QUALITY_GATES.json` is the 0.6.0 copy, so the released evaluator does not
   yet refuse a placeholder-bearing approval here. `tests/test_validation_taxonomy.py`
   carries a declared exception for the two new predicates until the upgrade.

## Complete changed-path set

```
docs/engineering/artifact-authoring/evidence/WO-AUT-002/WO-AUT-002-verification.md
docs/engineering/artifact-authoring/evidence/WO-AUT-002/verification-method-mapping.json
docs/notes/artifact-authoring.md
scripts/migrate_verification_methods.py
se_harness/quality_gates_contract.json
se_harness/workflow_compliance.py
se_harness/workflow_contract.py
templates/repository/standard/docs/engineering/QUALITY_GATES.json
templates/repository/standard/docs/engineering/QUALITY_GATES.md
tests/test_artifact_authoring_policy.py
tests/test_validation_taxonomy.py
```

## Deviation acceptances

Recorded on 2026-08-25 from the owner's interactive answers, before the
completion decision. These are the owner's statements; the assurance decision
on `VREC-AUT-002` remains separate.

| Deviation | Owner answer |
| --- | --- |
| 1 - string form stays W-AUT-004; migration built, not applied | Accept, defer to WO-HUP-005: promotion to E-AUT-001 and the repository-wide application belong to the governor-upgrade transaction, whose scope amendment is a follow-up item. |
| 2 - four unmatched values (REQ-REB-004, -011, -014, -018) | Steward decides at application time: the report keeps them `unmatched`; no new mapping rule under this work order. |
| 3 - in-scope paths left unchanged | Accept: declared paths that turned out unnecessary. |
| 4 - predicates not enforced by the released governor on this root | Accept: same boundary as every managed change in WO-AUT-001; enforcement arrives with the upgrade. |

## Not done

- Applying the migration to this repository; promoting `W-AUT-004` to
  `E-AUT-001`; the steward decision on the four unmatched values (all deferred
  to `WO-HUP-005`, see deviation 1).
- The completion transition, `VREC-AUT-002`, and the Linux figure.
