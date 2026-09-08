# WO-CIP-007: retired-name grep before and after

`SPEC-CIP-003` `CIP-ONE-011` and `CIP-ONE-012`; `VER-CIP-003`'s "retired names"
row. A retired name is `governor`, `governor-transition` or
`governance-migration` — mechanisms removed under `WO-ECP-010`, `WO-ECP-011`
and `WO-REB-028`.

    git grep -niE "governor|governance.migration" <ref> -- .github/workflows | grep -v engineering-harness

## Before, at `fae52e1b6c570bf1cdba892728029fa38416c947`: 28 lines

The same 28 lines stand at `560973cf12452d1c91b5a198c6a74d11af383d49`, the
`main` this branch later merged in: `git diff fae52e1b 560973cf -- .github/`
is empty.

### `candidate-evidence.yml` — 9

| Line | Text | Disposition |
| --- | --- | --- |
| 160 | `"se_harness/governor_reconciliation.py",` in the inline forbidden-member tuple | removed with the assertion (`CIP-ONE-003`) |
| 252, 253 | the `--help` grep for `reconcile-governor` and its message | removed (`CIP-ONE-004`) |
| 268 | `governance-migration:` — the job id | renamed `upgrade-rehearsal` (`CIP-ONE-012`) |
| 269 | `name: Governance migration (${{ matrix.platform }})` | renamed |
| 375 | `name: governance-migration-${{ matrix.platform }}` — the artifact | renamed |
| 391 | `- governance-migration` in `integration-package-build`'s `needs` | renamed |
| 399, 400 | `needs.governance-migration.outputs.Linux` and `.Windows` | renamed |

### `predecessor-evaluator-assessment.yml` — 19

Sixteen are renamed after the predecessor evaluator assessment
(`CIP-ONE-011`): lines 7 (workflow name), 18 (concurrency group), 25 (job id),
26 (job name), 47 and 109 (step titles), and 59, 60, 61, 122, 133, 154, 157,
158, 159, 160 (temporary file and artifact names).

Two occurrences cannot move under this work order and are named as exemptions:

| Line | Text | Why it stays |
| --- | --- | --- |
| 55, 132 | `scripts/validate_governor_transition.py` | `WO-CIP-007`, Out of scope: "Renaming `scripts/validate_governor_transition.py` or any script, module or test file; only workflow-level names change." |
| 67 | `assert value["schema"] == "se-harness-governor-transition-v1"` | the schema string that unrenamed script emits; changing the assertion without changing the script would break the lane |

The retired-name test therefore excludes exactly those two literals, naming the
out-of-scope clause. Retiring them needs a separate work order over the script,
its module-level names and its own tests.

## Required status checks before the renames

`GET /repos/mmzen/se_harness/rulesets/20693381` (ruleset "main basic
protection", branch target, active) declares one required status check context:
`validate`. `release protection` (id 22326279) is disabled. No renamed workflow
or job is a required check, so `WO-CIP-007`'s stop condition "a renamed job
missing as a required check on the pull request" does not arise and the owner
has no ruleset to update.

## Documents outside this work order's scope that name the renamed job

`ARCH-CIP-001` line 43 and `REQ-CIP-002` lines 27, 29, 41 and 49 describe the
job as `governance-migration`. Neither file is in `WO-CIP-007`'s
`[execution_scope]`, which admits `specifications/`, `REQ-CIP-008` and
`REQ-CIP-009` only, so both keep the old name and are owed an amendment under a
later work order. `SPEC-CIP-001` is amended here, as `CIP-ONE-015` requires.
Historical evidence packets and verification records state what was true when
they were written and are never rewritten.

## After, on the branch `wo/cip-007-pipeline-hygiene`: 4 lines, all exempt

    git grep -niE "governor|governance.migration" -- .github/workflows \
      | grep -v engineering-harness

| File | Line | Text |
| --- | --- | --- |
| `predecessor-evaluator-assessment.yml` | 5 | `# scripts/validate_governor_transition.py, and the schema string that script` |
| `predecessor-evaluator-assessment.yml` | 59 | `python -S scripts/validate_governor_transition.py plan \` |
| `predecessor-evaluator-assessment.yml` | 71 | `assert value["schema"] == "se-harness-governor-transition-v1"` |
| `predecessor-evaluator-assessment.yml` | 136 | `python -S scripts/validate_governor_transition.py assess "${args[@]}" \` |

28 to 4. Every remaining line is one of the two exempt literals: the path of
the unrenamed script (three lines, one of them the header sentence that
discloses the exemption) and the schema string that script emits. Line 5 is
new: `CIP-ONE-017` obliges the header to describe the file, and the header
names both exemptions and the out-of-scope clause that keeps them.

`candidate-evidence.yml` holds none. Its job is `upgrade-rehearsal`, with
`name: Upgrade rehearsal (${{ matrix.platform }})`, the artifact
`upgrade-rehearsal-${{ matrix.platform }}`, the `needs` entry
`- upgrade-rehearsal` in `integration-package-build`, and the outputs
`needs.upgrade-rehearsal.outputs.Linux` and `.Windows`. The two lines that
restated a script's definition are gone with their steps' inline checks.

`predecessor-evaluator-assessment.yml`'s renames: workflow name
`Predecessor Evaluator Assessment`, concurrency group
`predecessor-evaluator-assessment-${{ github.ref }}`, job id and job name
`predecessor-evaluator-assessment` / `Predecessor evaluator assessment`, step
titles "Plan the exact root evaluator transition" and "Assess the current root
with the exact target evaluator", temporary files
`evaluator-transition-plan[-result].json` and
`evaluator-transition-assessment[-result].json`, and the artifact
`predecessor-evaluator-assessment`.

`test_no_retired_name_survives_in_a_repository_owned_workflow` strips exactly
the two exempt literals before searching, so a third occurrence of a retired
name — including a re-added one inside a comment — fails the suite. That the
guard bites was measured: adding the literal `reconcile-governor` to a comment
in `candidate-evidence.yml` while drafting this change made the test fail, and
the comment was reworded to name `FORBIDDEN_CLI` instead.

The concurrency group changed name, so the first run on this branch cannot
cancel a run of the old group. No run of the old group can exist for these
commits, since the branch is new.
