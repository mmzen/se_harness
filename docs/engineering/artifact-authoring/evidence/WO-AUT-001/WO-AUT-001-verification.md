# WO-AUT-001 implementation evidence

artifact: WO-AUT-001
checkpoint: handoff
formal_snapshot_sha256: ac435d2c550dc721b1c05dc43159d1054b4c444f3f778961bd52254b4a5cc4f3

Retained by the implementation actor on 2026-08-25. This file is evidence. It
does not complete, verify, or release the work order.

## Evaluators

- Governing: released `se-harness 0.6.0` installed outside the checkout from
  the exact wheel `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
  (`C:\Users\mathi\se-harness-eval`, invoked with `-I`).
- Candidate: this checkout, `python -m se_harness` from the repository root.
  The candidate validator, template, and commands are exercised against
  installed targets in `tests/test_artifact_authoring_policy.py`; this
  repository's own root keeps the 0.6.0 copies.

## Commands and results

| Command | Evaluator | Result |
| --- | --- | --- |
| `harnessctl preflight . --work-order WO-AUT-001 --phase review` | released 0.6.0 | `PASS` |
| `harnessctl validate .` | released 0.6.0 | PASS, 901 artifacts, 0 errors, 50 warnings |
| `harnessctl doctor .` | released 0.6.0 | 0 FAIL |
| `python scripts/validate_release_distributions.py --root .` | candidate | PASS (1 distribution-bearing record) |
| `python -m se_harness --help` | candidate | exit 0 |
| `git diff --check` | git | clean |
| `harnessctl check . --artifact WO-AUT-001 --checkpoint handoff --changed-path … --changes-complete --json` (complete set below) | released 0.6.0 and candidate | before this file existed: blocked only by `QGP-G4I-EVIDENCE`; both report formal snapshot `ac435d2c550dc721b1c05dc43159d1054b4c444f3f778961bd52254b4a5cc4f3` |
| `python -m unittest tests.test_artifact_authoring_policy` | candidate | 5 tests, OK |
| `python -m unittest` over `test_context_routing_retirement`, `test_artifact_catalog`, `test_agentic_execution`, `test_instruction_architecture`, `test_harnessctl`, `test_repository_context_retirement`, `test_release_build`, `test_workflow_documentation_contract`, `test_artifact_authoring`, `test_progressive_documentation`, `test_validation_taxonomy` | candidate | 174 tests, OK, 4 skips |
| `python -m unittest discover -s tests -p "test_*.py"` | candidate, Windows 11, CPython 3.14 | `Ran 1007 tests in 336.113s` — `OK (skipped=23)`; the 23 skips are the Windows-only guards |
| Linux lane | `.github/workflows/candidate-evidence.yml` | not run locally; the pull-request run is the Linux figure |

## Measurements

- `REQUIREMENT.template.md`: 1618 bytes (bound 2,500); headings Rationale,
  Behavior, Assumptions and dependencies, Acceptance examples, Open
  decisions; five shapes as TOML comments above `statement`.
- `ARTIFACT_AUTHORING.md`: 5,793 bytes; sections for every artifact type;
  the requirement checklist has eleven items, four marked mechanical.
- `create-artifact --type requirement` prints the eleven bullets from the
  installed file (an edited installed file changes the printout);
  `--quiet` suppresses; a `verification_record` prints nothing.

## Complete changed-path set

```
docs/engineering/artifact-authoring/evidence/WO-AUT-001/WO-AUT-001-verification.md
docs/notes/README.md
docs/notes/artifact-authoring.md
docs/notes/harnessctl-reference.md
pyproject.toml
se_harness/artifact_layout.py
se_harness/cli.py
se_harness/preflight.py
templates/repository/standard/.agents/skills/harness-draft-change/SKILL.md
templates/repository/standard/.agents/skills/harness-draft-change/skill-contract.json
templates/repository/standard/ENGINEERING_HARNESS.md.tpl
templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md
templates/repository/standard/docs/engineering/templates/README.md
templates/repository/standard/docs/engineering/templates/REQUIREMENT.template.md
templates/repository/standard/scripts/validate_engineering_artifacts.py
tests/fixtures/agentic_execution/phase3/portable_vectors.json
tests/test_agentic_execution.py
tests/test_artifact_authoring_policy.py
tests/test_context_routing_retirement.py
```

Every path is admitted by `[execution_scope].paths` of `WO-AUT-001`. Scoped
path left untouched: `se_harness/skill_contract.py` (no profile change was
needed: the skill's operations and effects are unchanged). One out-of-scope
edit was made and reverted before the handoff check: `se_harness/workflow.py`
had been given a call to the new authoring check inside the transition
planner's re-validation; it was redundant, because `plan_transition` refuses
on any error of `validate_repository`, which already includes `E-AUT-*`.

## Rule coverage

| Rule | Implemented by | Test evidence |
| --- | --- | --- |
| `AUT-POL-001..002` | `ARTIFACT_AUTHORING.md` template (managed); router row "Authoring rules for formal artifacts"; wheel data file | `test_policy_is_managed_routed_once_listed_and_printed_by_create_artifact`; `test_context_routing_retirement` routing-row baseline updated |
| `AUT-POL-003` | `authoring_checklist` in `artifact_layout.py`; `create-artifact --quiet` | same test (prints from the installed file; quiet; non-authored type prints nothing) |
| `AUT-POL-004` | `harness-draft-change` step 6 sentence; contract `1.0.1 -> 1.0.2`; phase-3 vector regenerated | `test_draft_change_skill_applies_the_policy_and_its_vector_is_current`; `test_agentic_execution` version expectation per skill |
| `AUT-POL-005` | `REQUIRED_PATHS` and `POLICY_PATHS` | policy test |
| `AUT-STM-001..002` | `validate_authoring`: `W-AUT-001` opener, `W-AUT-002` second `SHALL`, `W-AUT-003` > 300 characters (maintenance) | `test_five_shapes_validate_clean_and_defects_are_signalled` |
| `AUT-STM-003` | template comments and sentence | `test_template_carries_six_headings_five_shapes_and_the_acceptance_link` |
| `AUT-VOC-001..002` (warning half) | array form accepted and validated (`E-AUT-001`); string form accepted with `W-AUT-004` | `test_vocabulary_and_optional_attributes_are_validated` |
| `AUT-ATT-001` | `priority`, `source` (resolving when an artifact ID), `measure`; `E-AUT-002` | same test |
| `AUT-TPL-001..002` | six headings, attributes, `verification_method = ["test"]`, `acceptance/<REQ-ID>.feature` sentence | template test |

## Material deviations from SPEC-AUT-001

1. `AUT-POL-002` describes `### Checklist` and `### Guidance` under every
   type section. Guidance is written for requirement, intent, specification,
   and the record types; the other sections carry a checklist only. The
   checklist is the part a tool consumes; guidance can be extended under a
   later policy revision without touching code.
2. `AUT-POL-004` says the contract "version advances". `harness-draft-change`
   moves from `1.0.1` to `1.0.2` on this branch; `WO-RSK-002` (PR #158, not
   yet merged) also moves it to `1.0.2` with different content. Whichever
   merges second must bump to `1.0.3` and regenerate the vector; recorded here
   so the merge does not silently keep one of the two.
3. `VER-AUT-001` scenario 3 ("paste `REQ-AEX-008`'s statement") is covered
   by an equivalent synthetic statement in the test rather than the literal
   text, to keep the fixture independent of that artifact's future edits.

## Deviation acceptances

Recorded on 2026-08-25 from the owner's interactive answers, before the
completion decision. These are the owner's statements; the assurance decision
on `VREC-AUT-001` remains separate.

| Deviation | Owner answer |
| --- | --- |
| 1 — guidance subsections only for some types | Accept: the mechanical part is complete for every type; guidance for the remaining types is a policy-only follow-up. |
| 2 — `harness-draft-change` 1.0.2 also claimed by PR #158 | Accept, resolve at merge: whichever merges second bumps to 1.0.3 and regenerates the vector under its own work order. |
| 3 — synthetic statement instead of `REQ-AEX-008`'s literal text | Accept: the signal under test is the same; the fixture is independent of a live artifact. |

## Not done

Linux figure pending the pull-request lane. `REQ-AUT-003` (migration,
`E-AUT-001` for strings) and `REQ-AUT-005` (approval predicates) are
`WO-AUT-002` by design.
