# WO-PLG-020 supplemental CI and command-contract reconciliation

Revision 2 replaces both earlier supplemental approval proposals. The final independent contract review added REQ-CIP-009, VER-CIP-003, and the two CI documents mandated by CIP-DOC. No earlier proposal has been applied. No approval, scope, lifecycle, or implementation effect is recorded by this proposal. The approved ownership operation and verification matrix stay as selected; this reconciles additional prior contracts and adds the exact paths needed by the full regression suite.

## Observed conflict

Approved `docs/engineering/ci-pipeline/specifications/SPEC-CIP-003.md`, rule CIP-ONE-005 (technical-owner), says:

> Every `python-version` in a repository-owned workflow MUST be the one string `"3.11"`; `publish-pypi.yml` MAY keep it in its `PYTHON_VERSION` env.

Approved VER-PLG-020 requires the full ownership and fault matrix with Python 3.13 on Ubuntu and Windows, in addition to Python 3.11 interface and compatibility smoke. Both instructions cannot be followed by the current setup-python rule.

CIP-ONE-002 also reserves the complete candidate qualification and test suite to `candidate-source`. The amendment below expressly distinguishes the additional bounded ownership acceptance runs.

## Exact proposed applicability text

Append to SPEC-CIP-003 without rewriting its historical rule or approval:

### Applicability amendment — WO-PLG-020 ownership acceptance

For the ownership acceptance required by VER-PLG-020, CIP-ONE-005 permits one additional pinned major/minor interpreter selection, `"3.13"`, in the existing `upgrade-rehearsal` job of `.github/workflows/candidate-evidence.yml`. The additional interpreter runs only the complete WO-PLG-020 source and isolated installed-candidate ownership and fault matrix on Ubuntu and Windows. Existing qualification, the canonical complete candidate-source regression, candidate wheel production, integration packaging, and predecessor-to-successor upgrade rehearsals retain Python `"3.11"`; ownership interface and compatibility smoke also runs on `"3.11"`. Every acceptance consumer uses the same verified non-promotable candidate wheel built once by `candidate-source`; this exception authorizes no additional release build, qualification duplicate, new job, publication, or adoption. As a bounded exception to CIP-ONE-002, the same `upgrade-rehearsal` job may run only these WO-PLG-020 ownership acceptance subsets; complete-candidate qualification and the canonical full repository test suite still run once in `candidate-source`. Every other application of CIP-ONE-002 and CIP-ONE-005, and all other SPEC-CIP-003 rules, remain unchanged.

## Exact execution-scope additions

Add only these paths to WO-PLG-020 `[execution_scope].paths`:

- `docs/engineering/ci-pipeline/specifications/SPEC-CIP-003.md`
- `tests/test_ci_pipeline.py`
- `docs/engineering/execution-control-plane/requirements/REQ-ECP-027.md`
- `docs/engineering/execution-control-plane/specifications/SPEC-ECP-016.md`
- `docs/notes/harnessctl-reference.md`
- `tests/test_cli_shape.py`
- `docs/engineering/ci-pipeline/requirements/REQ-CIP-009.md`
- `docs/engineering/ci-pipeline/verification/VER-CIP-003.md`
- `docs/notes/ci-pipeline.md`
- `docs/notes/developing-se-harness.md`

The workflow itself is already in approved scope. The bounded implementation and current work-order state remain unchanged by scope definition approval.

## Scoped test adjustment

In `tests/test_ci_pipeline.py`, `PipelineHygieneTests.test_one_python_version_string` (locate by method name; current definition around line 621) currently permits only `"3.11"` in every non-publication workflow. Preserve that check outside the exact named ownership acceptance setup step. Permit `"3.13"` only in the `upgrade-rehearsal` job's named `Select Python 3.13 for full ownership acceptance` setup-python step. Assert that the step uses the existing full action SHA, all other job steps retain the existing selection, and both source and isolated package acceptance are invoked through the shared runner with explicit `full` selection. Keep the existing exact-six-jobs assertion, one-wheel build assertion, released qualification assertions, action digest assertions, and predecessor-to-successor double-rehearsal assertions unchanged.

## Resulting execution evidence

Each Ubuntu/Windows upgrade-rehearsal job first performs its existing required predecessor-to-successor rehearsals, then ownership source and installed-package smoke on Python 3.11, and only then switches to Python 3.13 for full ownership acceptance. The 3.13 leg uses separately named external candidate and predecessor virtual environments. Evidence artifact `skill-ownership-Linux` or `skill-ownership-Windows` retains per-case JSON, recursive snapshots, raw recovery metadata, subprocess and fault logs, exact platform/interpreter/runner identity, Git candidate identities, input wheel SHA-256 and installed evaluator identity. Test failure still fails the existing job and downstream integration retention.

## Command-contract conflict found by the full regression suite

REQ-ECP-027's repository-target rule and SPEC-ECP-016 ECP-CLI-001 require an optional positional target defaulting to `.`. The already approved SPEC-PLG-020 deliberately requires an explicit target for skill ownership. SPEC-ECP-016 ECP-CLI-003 also lists only `completed` and `failed` outcomes in the common envelope; approved PLG-OWN-027 and ADR-PLG-003 require distinct ownership transaction outcomes.

The existing CLI census and command-reference tests fail because `skill-ownership` is absent from their enumerations. Their assertions remain intact; the new command is added explicitly.

## Exact REQ-ECP-027 applicability amendment

Append this text without rewriting historical requirements or approvals:

### Applicability amendment — WO-PLG-020 explicit ownership selection

For the ownership operation selected by REQ-PLG-028 and SPEC-PLG-020, `skill-ownership` is a repository command whose positional `target` is required and has no implicit default. This is the sole exception to this requirement's optional-target rule: the repository argument keeps the same positional name and no alternate repository option is introduced. The operation keeps the standard JSON envelope and exit-code convention; its bounded transaction outcomes are the distinct observations required by PLG-OWN-027. Every other command and every other rule of REQ-ECP-027 remain unchanged.

## Exact SPEC-ECP-016 applicability amendment

Append this text without rewriting historical rules or approvals:

### Applicability amendment — WO-PLG-020 ownership command

ECP-CLI-001 includes `skill-ownership` in the repository-command set. As selected by SPEC-PLG-020 and the corresponding REQ-ECP-027 amendment, only this command requires an explicit positional `target`; it has no implicit `.` default and no alternate repository-target option. ECP-CLI-003 includes this command in the existing `se-harness-command-result-v1` envelope. Its transaction outcome is one of `planned`, `applied`, `rolled-back`, `recovery-required`, or `unchanged`; a bounded input refusal uses `failed`. Its result retains the source identity, selected and resulting provider as applicable, reviewed plan digest, exact ownership changes, actual effects, conflicts, recovery state, and explicitly unobserved external availability/native discovery as specified by SPEC-PLG-020 and ADR-PLG-003. Planning is read-only; applying requires `--apply --expected-plan-sha256 HASH`. ECP-CLI-004's 0/1/2 convention and all other rules remain unchanged. This amendment grants no lifecycle, verification, release, or external-action authority.

## Exact command-reference and classification changes

In `tests/test_cli_shape.py`, add `skill-ownership` to `REPOSITORY_COMMANDS`. Keep exact parser/census equality and existing target-name/JSON assertions. Add a focused assertion that this one command's target is required and that provider and reviewed apply selection follow the approved parser contract. Keep every other command's classification and behavior unchanged.

In `docs/notes/harnessctl-reference.md`:

- Clarify the optional-target rule with this sentence: `skill-ownership` requires an explicit positional `TARGET` under SPEC-PLG-020; it has no implicit repository selection.
- Add `skill-ownership` to the plan-by-default command examples.
- Add this command-table row:

| `skill-ownership` | repository owner or explicitly authorized agent | plan is read-only; reviewed application changes only the selected repository ownership transaction and its bounded recovery data | migrate the seven retained repository skill files to a validated portable plugin binding, restore repository ownership, or review and complete pending recovery; external availability and native loading remain unobserved |

- Add these two syntax forms and the explanatory sentence below:

```text
harnessctl skill-ownership TARGET --provider plugin --binding-input FILE [--apply --expected-plan-sha256 HASH] [--json]
harnessctl skill-ownership TARGET --provider repository [--apply --expected-plan-sha256 HASH] [--json]
```

This candidate operation is unavailable in released 0.17.0. It requires a migration-capable installed evaluator governing the selected repository, and does not install or activate a plugin. A recovery plan distinguishes restoring prior state from finalizing cleanup of an already committed state.

## Exact REQ-CIP-009 applicability amendment

Append this text without rewriting historical requirements or approvals:

### Applicability amendment — WO-PLG-020 ownership acceptance

For VER-PLG-020 ownership acceptance only, the one-Python-version clauses in this requirement's statement, measure, and behavior permit the additional `"3.13"` selection bounded by SPEC-CIP-003's WO-PLG-020 applicability amendment. It is used only for the full ownership and fault matrix in the existing Ubuntu and Windows `upgrade-rehearsal` job; the general workflow selection, ownership compatibility smoke, candidate wheel production, complete-candidate qualification, canonical full repository suite, integration packaging, and predecessor upgrade rehearsals remain on `"3.11"`. All action-pin, duplicate-check, tool-inventory, queue, probe, and retired-name requirements remain unchanged. This exception introduces no second full repository-suite run or complete-candidate qualification.

## Exact VER-CIP-003 applicability amendment

Append this text without rewriting historical verification results or approvals:

### Applicability amendment — WO-PLG-020 ownership acceptance

For WO-PLG-020, the versions-and-pins row expects `"3.11"` everywhere except the single named `Select Python 3.13 for full ownership acceptance` setup-python step in the existing `upgrade-rehearsal` job of `candidate-evidence.yml`, as bounded by the corresponding REQ-CIP-009 and SPEC-CIP-003 amendments. Verify that the additional selection uses the existing full action SHA and that both Ubuntu and Windows run the complete source and isolated installed-candidate ownership/fault matrix on `"3.13"`, while interface and compatibility smoke and the pre-existing rehearsals use `"3.11"`. The one-run and run-observation rows continue to require exactly one complete-candidate qualification and one canonical full repository suite in `candidate-source`; the separately identified ownership subsets are the sole permitted additional test executions under this amendment. Every ownership package consumer verifies and uses the same non-promotable candidate wheel. Retain per-platform/interpreter observations and unavailable cases explicitly under WO-PLG-020; its VER-PLG-020 acceptance and every other applicable pin, duplication, graph, regression, and lifecycle criterion remain unchanged. This amendment records no pass result and does not rewrite WO-CIP-007's historical evidence.

REQ-CIP-008 already states the uniqueness of the **full** repository test suite and complete-candidate qualification; neither is duplicated. No amendment to that requirement is needed.

## Bounded CI documentation changes

SPEC-CIP-001 CIP-DOC requires documentation in the same workflow-changing increment. Its rule remains unchanged.

- In `docs/notes/ci-pipeline.md`, preserve the historical baseline and prior increments. Add an `After WO-PLG-020` comparison showing six job definitions, one complete-candidate qualification, one canonical full repository suite, one shared non-promotable candidate wheel, the added non-promotable sdist inventory check, and the ownership smoke/full subsets by platform and interpreter. Report hosted observations only after they exist; distinguish planned execution shape from observed counts and timings.
- In the affected `Ordinary development checks` and `Evaluator and candidate evidence` sections of `docs/notes/developing-se-harness.md`, document the shared ownership acceptance runner, Python 3.11 smoke and Python 3.13 full coverage, outside-checkout package environments, one verified wheel, retained case evidence, and explicit unavailable mechanisms. Clarify that this is candidate acceptance; the release sequences and root-evaluator adoption procedure remain unchanged.

## Accountable approval

Approve revision 2 as requirements steward for REQ-ECP-027 and REQ-CIP-009, technical owner for SPEC-ECP-016 and SPEC-CIP-003, assurance owner for the VER-CIP-003 applicability amendment, and engineering owner for the ten listed WO-PLG-020 scope additions. VER-PLG-020's approved acceptance criteria remain unchanged. Record these definition decisions only; WO-PLG-020 remains in progress and no verification result or release decision is taken.

The installed DECISION_RIGHTS.md DR-015 states: "The class MUST NOT activate verification, release, delivery, Git, credential, network or external authority, or any definition decision". This is why the additional prior-contract reconciliation and exact scope additions need owner approval. The earlier packet and delegated start approvals remain recorded and are not being requested again.
