# WO-HUP-007 implementation evidence

artifact: WO-HUP-007
checkpoint: handoff
formal_snapshot_sha256: 73c03e91357b0c9290ffdc25c1b1e75da2d2bf1fa45a668d318214af604fe49a

Retained by the implementation actor on 2026-08-27. This file is evidence. It
does not complete, verify, or release the work order.

## Outcome

The standard root moved from exact public 0.6.0 to exact public 0.7.1 by the
simple upgrade: one command from an index install outside the checkout, no
packet, no `--work-order`. The transaction document is
`WO-HUP-007-evaluator-upgrade.json` beside this file.

## Evaluators

- Applying and governing after apply: released `se-harness 0.7.1` installed
  from the index into `C:\Users\mathi\se-harness-eval-071` (`pip install
  --no-cache-dir "se-harness==0.7.1"`), invoked with `-I`. Identity read from
  the installation: version `0.7.1`, payload
  `995ee973b2959af3bcbf7f7cc4388f079ad033e7c68509e71feb142b0691451f`,
  archive pair `null` (index install, `REQ-REB-028`).
- Governing before apply: released 0.6.0 in `C:\Users\mathi\se-harness-eval`
  (start preflight, packet approvals).
- Candidate: this checkout, branch `governance/hup-007-adopt-0-7-1` off
  `main` at `23d5781`.

## Plan and transaction

- `upgrade .` before apply: 61 files, 43 add or update, 18 unchanged; zero
  `customized`, zero `conflict`; every path inside the managed set the
  installer declares (`SPEC-HUP-007` rule 3).
- `upgrade . --apply --evidence-output docs/engineering/repository-harness-upgrade/evidence/WO-HUP-007-evaluator-upgrade.json`:
  `upgraded managed files to se-harness 0.7.1`, evidence retained.
- Replay `upgrade .`: 61 files, 61 unchanged.
- Lock after apply: schema 3, `tool_version 0.7.1`, evaluator
  `{version 0.7.1, payload_manifest se-harness-installed-payload-v1,
  payload_sha256 995ee973…, archive_name null, archive_sha256 null}`.
- A first attempt by the owner from a venv inside the checkout was refused
  by the guard (`MG005`: `RID006`, `RID007`, `RID024`), as rule 1 requires;
  nothing was written by it.

## Owner content and candidate version

- `AGENTS.md` owner region: names `se-harness==0.7.1` and every managed
  path the lock lists (the skills by basename); 5,968 bytes, under the
  6,000-byte bound. The managed block is the 0.7.1 fragment the installer
  wrote.
- `docs/notes/developing-se-harness.md`: the candidate reports 0.8.0; the
  root is exact public 0.7.1 adopted by this work order, archive pair
  `null`, wheel bound in `RLS-SEH-016`.
- `pyproject.toml`, `se_harness/__init__.py`, `README.md`: `0.7.1` → `0.8.0`
  (rule 7); the only product bytes that moved.
- `tests/fixtures/governance_migration/candidate-0.7.1-to-0.8.0.json`:
  written by the canonical writer from the retained
  `candidate-0.6.0-to-0.7.1.json` (sha256
  `d211dc58dd1c47e230332e8519352c34954c3ab1794aa8152d686d34159a26de`,
  3,862 bytes); the 0.7.1 pair stays as the previous candidate.
- `repository_tools/predecessor_facts.py`: `LEGACY_ACCEPTANCE_CONTRACT_SHA256`
  gains `0.7.1` = `a443e93d…` — `CONTRACT_SHA256` read from the installed
  0.7.1 evaluator equals 0.6.0's.

## Scope decision, 2026-08-27: the null archive pair

`predecessor_facts derive` (first step of the candidate-evidence lane)
required the lock's `archive_name`/`archive_sha256` and failed `PRE001`
under the new root, because the simple upgrade from an index install records
`null` for both by design. Put to the owner with two options; the owner
chose (after a mis-click on the first answer, re-asked): **the released
record that binds that version**. `derive` and `write-scenario` now read the
lock's pair when present and otherwise the one `released` release record
whose `version` equals the evaluator version (`RLS-SEH-016` → wheel
`se_harness-0.7.1-py3-none-any.whl`,
`ddd403cde17fc3770460809cbe8f9edb68f47c3aaa0422fe021334279994225d`), failing
closed with `PRE014` on zero or several records and `PRE015` on a record
without a distribution table. `repository_tools/predecessor_facts.py` is in
the declared scope; a test covers the fallback and both fail-closed cases.

## Scope amendment 2, 2026-08-27: the hosted governor transition assessment

The pull request's `Governor transition assessment` lane failed at plan:
`trusted base must contain exactly one released distribution for the target
version`. `scripts/validate_governor_transition.py` still encoded the retired
packet model: a schema-1 distribution table (`RLS-SEH-016` is schema 2), a
`[evaluator_upgrade]` declaration on an implemented work order, evidence
bound to that work order by name, and an exact archive match (null for an
index install). On the owner's answer 'Amend the scope and rework the
assessor', the script was added to the scope and reworked to `SPEC-REB-012`:
a released record of schema 1 or 2 for the target version at the trusted
base; exactly one retained `se-harness-evaluator-upgrade-evidence-v1`
document under `docs/engineering/**/evidence/` whose prior lock digest is one
of the base's materializations and whose `target` equals the head lock's
evaluator (`work_order` may be null); the target's archive pair equal to the
trusted release's when recorded, and taken from the trusted release when
null (`archive_source` in the plan), so the lane installs the exact wheel
`RLS-SEH-016` binds. The plan's `work_order` block became `transition`. The
assess and apply phases are unchanged.

## Tests changed, for root assumptions only

| File | Assumption replaced |
| --- | --- |
| `tests/test_ci_pipeline.py` | root workflow was the unfiltered 0.6.0 copy; scenario paths and versions were literal; the temp root now carries the released records `derive` reads; the lock test accepts a `null` archive pair; new `PRE014` test |
| `tests/test_governance_migration.py` | `CANDIDATE` is `candidate-0.7.1-to-0.8.0.json`, `PREVIOUS_CANDIDATE` the retained 0.6.0→0.7.1 pair; `PUBLIC_PREDECESSOR_ARCHIVES` gains 0.7.1 |
| `tests/test_artifact_catalog.py` | root work-order template and router equal the candidate |
| `tests/test_hash_bound_integrity.py` | the root managed block now carries the promoted patterns |
| `tests/test_instruction_architecture.py` | 55 managed paths; the governor version read from the lock, not literal |
| `tests/test_standard_repository_lifecycle.py` | the root managed block equals the released fragment |
| `tests/test_validation_taxonomy.py` | root `QUALITY_GATES.md` equals the candidate |
| `tests/test_governor_transition.py` | the fixture carried a `[evaluator_upgrade]` packet, a work-order-bound evidence file and a schema-1 record; now the simple model: evidence document alone, `work_order` nullable, null archive pair, schema 1 or 2, plus three new cases |

The first five ports are the changes `WO-HUP-006` measured, re-applied by
patch; the version literals were replaced by lock-derived values.

## Commands and results

| Command | Evaluator | Result |
| --- | --- | --- |
| `harnessctl preflight . --work-order WO-HUP-007 --phase start` | released 0.6.0 | `PASS` (recorded in the start transition) |
| `upgrade .` / `upgrade . --apply --evidence-output …` / `upgrade .` | released 0.7.1 | plan 43 add or update; applied; replay 61 unchanged |
| `harnessctl validate .` | released 0.7.1 | PASS, 986 artifacts, 0 errors, 466 warnings (maintenance plane: `W-AUT-004` 267, `W-AUT-003` 72, `W-AUT-002` 64, `W013` 26, `W015` 15, `W014` 14, `W024` 6, `W-AUT-001` 2; the authoring advisories are the 0.7.x policy reading the pre-policy graph) |
| `harnessctl doctor .` | released 0.7.1 | 0 FAIL |
| `harnessctl qualify released-root .` | released 0.7.1 | passed, RR001–RR004, archive pair `null` |
| `harnessctl inspect .` | released 0.7.1 | completes; derived observation only |
| `harnessctl dashboard .` twice | released 0.7.1 | deterministic; 986 artifacts, 3780 relations, 0 errors, manifest `bbc25756c3eb117b9ceda78d1ab3cdfe2a5b860a902c549a30f297f13e05f939` |
| `harnessctl preflight . --work-order WO-HUP-007 --phase review` | released 0.7.1 | `PASS` |
| `python -m repository_tools.predecessor_facts derive --repository .` | candidate | version 0.7.1, wheel `ddd403cd…` from `RLS-SEH-016`, candidate 0.8.0, scenario `candidate-0.7.1-to-0.8.0.json`, contract `a443e93d…` |
| `python scripts/validate_release_distributions.py --root .` | candidate | PASS (4 distribution-bearing records) |
| `python scripts/check_portable_release_surface.py --repository .` | candidate | PASS |
| `git diff --check` | git | clean |
| `python -m unittest` over the seven root-assumption modules plus `test_progressive_documentation`, `test_public_onboarding` | candidate | OK, 233 tests, 1 skip (the migration rehearsal 0.7.1 to 0.8.0 reads pass, compatible, deterministic) |
| `python scripts/run_tests.py --workers 8 --scale full` | candidate, Windows 11, CPython 3.14 | OK, 987 tests, 24 skipped (Windows-only guards), 0 failures (re-run after the assessor rework; 984 before it) |
| `py -3.11 scripts/run_tests.py --workers 4 --scale full` | candidate, Windows 11, CPython 3.11 | OK, 987 tests, 24 skipped (Windows-only guards), 0 failures (re-run after the assessor rework; 984 before it) |
| `harnessctl check . --artifact WO-HUP-007 --checkpoint handoff --changed-path … --changes-complete --json` | released 0.7.1 and candidate | Completed on both over the 68 paths (the 0.7.1 root governs the check now; the candidate run with python -s); before this file existed the only non-pass predicate was QGP-G4I-EVIDENCE; formal snapshot above |
| Hosted | the pull request's lanes | HOSTED-ROW |

## Deviations from the work order, recorded for the completion decision

1. **`derive` reads released records.** Rule 7 said the writer's legacy map
   gains the 0.7.1 entry, which it did; what the rule did not foresee is
   that the lock carries no archive pair at all. The owner's decision above
   resolves it inside the declared scope; recorded here because it is a
   behaviour of the repository tooling that no requirement stated.
2. **Maintenance warnings rise from 55 to 466 under the new root.** They are
   0.7.1's authoring advisories (`W-AUT-*`) over artifacts written under
   0.6.0's policy, plus the pre-existing `W013`/`W014`/`W015`/`W024`; none is
   an error and none is new content. Left as the owed maintenance backlog.
3. **`.gitattributes` owner copies stay**, as `WO-HUP-006` found: `doctor`
   requires the `governance-migration-protocol` class in the repository
   region.

## Deviation acceptances

Recorded on 2026-08-27 from the owner's interactive answer 'Accept all three',
before the completion decision.

| Deviation | Owner answer |
| --- | --- |
| 1 - derive reads the released record | Accept. |
| 2 - 466 maintenance warnings under the 0.7.1 root | Accept; the W-AUT backlog is owed. |
| 3 - .gitattributes owner copies stay | Accept. |

## Complete changed-path set

Every path this work order changed since `main` at `23d5781`, packet
included (the snapshot above is the one taken after scope amendment 2).

```
.agents/skills/harness-draft-change/SKILL.md
.agents/skills/harness-draft-change/agents/openai.yaml
.agents/skills/harness-draft-change/scripts/guard.py
.agents/skills/harness-draft-change/skill-contract.json
.agents/skills/harness-execute-work-order/SKILL.md
.agents/skills/harness-execute-work-order/agents/openai.yaml
.agents/skills/harness-execute-work-order/scripts/check_scope.py
.agents/skills/harness-execute-work-order/skill-contract.json
.agents/skills/harness-operator-brief/SKILL.md
.agents/skills/harness-operator-brief/scripts/check_brief.py
.agents/skills/harness-operator-brief/skill-contract.json
.agents/skills/harness-orient/SKILL.md
.agents/skills/harness-orient/scripts/orient.py
.agents/skills/harness-orient/skill-contract.json
.agents/skills/harness-prepare-assurance/SKILL.md
.agents/skills/harness-prepare-assurance/agents/openai.yaml
.agents/skills/harness-prepare-assurance/scripts/check_prepare.py
.agents/skills/harness-prepare-assurance/skill-contract.json
.claude/skills/harness-draft-change/SKILL.md
.claude/skills/harness-execute-work-order/SKILL.md
.claude/skills/harness-orient/SKILL.md
.claude/skills/harness-prepare-assurance/SKILL.md
.engineering-harness.lock
.engineering-harness.toml
.gitattributes
.github/workflows/engineering-harness.yml
AGENTS.md
CLAUDE.md
ENGINEERING_HARNESS.md
README.md
docs/engineering/ARTIFACT_AUTHORING.md
docs/engineering/DECISION_RIGHTS.md
docs/engineering/OPERATING_CARD.md
docs/engineering/QUALITY_GATES.json
docs/engineering/QUALITY_GATES.md
docs/engineering/TECHNICAL_COMMUNICATION.md
docs/engineering/WORKFLOW.json
docs/engineering/WORKFLOW.md
docs/engineering/repository-harness-upgrade/README.md
docs/engineering/repository-harness-upgrade/architecture/ARCH-HUP-005.md
docs/engineering/repository-harness-upgrade/evidence/WO-HUP-007-evaluator-upgrade.json
docs/engineering/repository-harness-upgrade/evidence/WO-HUP-007-verification.md
docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-014.md
docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-015.md
docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-007.md
docs/engineering/repository-harness-upgrade/verification/VER-HUP-007.md
docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-007.md
docs/engineering/templates/README.md
docs/engineering/templates/RELEASE_CONTRACT.template.md
docs/engineering/templates/REQUIREMENT.template.md
docs/engineering/templates/VERIFICATION_RECORD.template.md
docs/engineering/templates/WORK_ORDER.template.md
docs/notes/developing-se-harness.md
pyproject.toml
repository_tools/predecessor_facts.py
scripts/select_harness_work_order.py
scripts/validate_engineering_artifacts.py
scripts/validate_governor_transition.py
se_harness/__init__.py
tests/fixtures/governance_migration/candidate-0.7.1-to-0.8.0.json
tests/test_artifact_catalog.py
tests/test_ci_pipeline.py
tests/test_governance_migration.py
tests/test_governor_transition.py
tests/test_hash_bound_integrity.py
tests/test_instruction_architecture.py
tests/test_standard_repository_lifecycle.py
tests/test_validation_taxonomy.py
```

## Not done

- The completion transition; the verification record; anything on `main`.
