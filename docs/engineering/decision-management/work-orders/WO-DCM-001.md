+++
id = "WO-DCM-001"
type = "work_order"
title = "Implement the decision artifact, its gate, and its disposition command"
status = "implemented"
owners = ["engineering-owner", "technical-owner", "quality-owner"]
created = "2026-09-03"
updated = "2026-09-03"

[assurance]
commit_bound_verification = "required"
rationale = "The change adds an artifact type, a lifecycle family, a gate evaluated at every transition of four families, a command that writes decisions, and validator diagnostics; every later approval, completion, verification and release relies on the gate refusing and admitting correctly."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "se_harness/",
  "templates/repository/standard/docs/engineering/",
  "templates/repository/standard/scripts/",
  "templates/repository/standard/.engineering-harness.toml.tpl",
  "repository_tools/explorer_design/",
  "tests/",
  "docs/engineering/decision-management/",
  "docs/engineering/README.md",
  "docs/notes/",
]

[delegation]
class = "execution"

[relations]
implements = ["REQ-DCM-001", "REQ-DCM-002", "REQ-DCM-003"]
specifications = ["SPEC-DCM-001"]
architecture = ["ARCH-DCM-001", "ADR-DCM-001"]
verification = ["VER-DCM-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-03T19:10:33Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable repository owner on 2026-09-03 with the instruction 'i approve with execution delegation', after reviewing the decision-artifact proposal and the drafted packet. WO-DCM-001 carries the delegation class: this approval delegates DR-WO-START, DR-WO-COMPLETE and DR-VREC-PREPARE to the delegated-executor role under the required validate check, with the class read from the pull request's base."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-03T19:18:57Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-START under [delegation] class 'execution': required check 'validate' success at 2f305c0b4fd5df9101f8efa46d269871d516dab7 (check-run 100781440327, source github-checks)."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-03T20:28:02Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-COMPLETE under [delegation] class 'execution': required check 'validate' success at e644dd06a6852d3ba16234368dbe87be379b9449 (check-run 100804318056, source github-checks). Delegated DR-WO-COMPLETE: the decision artifact is implemented in the candidate per SPEC-DCM-001 (as amended by record); evidence docs/engineering/decision-management/evidence/WO-DCM-001-verification.md with the retained Git-derived handoff result; Windows suite 1206 tests, zero failures, the one baseline error; released 0.14.0 validate PASS. Four disclosures for the assurance decision are in the evidence packet."
+++

# Work Order: Implement the decision artifact, its gate, and its disposition command

## Lifecycle

Drafted on 2026-09-03 after the repository owner reviewed
`docs/notes/decision-artifact-proposal-2026-09-03.md` and instructed the
creation of this packet. Approval authorizes the bounded implementation
below and nothing further. Commit-bound verification is `required`.

This work order carries `[delegation] class = "execution"`. Approving it is
the act of delegating `DR-WO-START`, `DR-WO-COMPLETE` and `DR-VREC-PREPARE`
to the `delegated-executor` role, each act admitted only while the required
`validate` check is `success` for the exact candidate head, with the class
read from the base of the pull request. Approval of the definitions, the
verification decision on the record, merge, release and publication stay
human.

## Objective

Add the decision artifact (`DEC-`) to the candidate harness as
`SPEC-DCM-001` defines it: the type and template, the `decision` lifecycle
family, the `QGP-DECISION-OPEN` gate on every transition of definitions,
work orders, verification records and release records, the
`harnessctl decide` command under `DR-DECISION-DISPOSE`, the validator
diagnostics and the standing-deviation projection, and the Explorer
projection; so that the next release ships it and this repository adopts it
at its next root adoption.

## In scope

- Layout and authoring: `DEC-` prefix and `decisions/` directory in the
  layout registry and `artifact_layout.py`; `DECISION.template.md`; the
  templates index; the threshold paragraph in `ARTIFACT_AUTHORING.md`.
- Contracts: the `decision` lifecycle family in `WORKFLOW.json` and
  `workflow_contract.json` with the disposing procedure step and its
  prose in `WORKFLOW.md`; `QGP-DECISION-OPEN` in `QUALITY_GATES.json`,
  `quality_gates_contract.json` and `QUALITY_GATES.md`, bound to every
  transition checkpoint of the four families; `DR-DECISION-DISPOSE` in
  `DECISION_RIGHTS.md`; `concerns`, `blocks` and `produces` in
  `TRACEABILITY.md`.
- Validator: field rules per kind, relation target types, `E-DCM-001` to
  `E-DCM-004`, `W-DCM-001` and `W-DCM-002`, and the projection of accepted
  deviations onto specifications, work orders and records, in the candidate
  `validate_engineering_artifacts.py`; the inspection command lists open
  decisions.
- Command: `harnessctl decide` with `--option`, `--decision`, `--reason`,
  `--defer --scope --revisit`, `--withdraw`, writing the disposition and the
  lifecycle event through the atomic transition path; the decision right
  check; `capture-verification` listing accepted deviations in the record's
  evidence.
- Explorer: the in-flight tile reads open and deferred decisions; the
  record panel shows the decision trail on concerned artifacts and the
  standing deviations on specifications, work orders and records; the
  summary `metrics` gain decision counts and raise-to-dispose times; the
  designed view sources are patched through the count-asserted build.
- Tests: fixtures per blocked family and per disposition path, taxonomy,
  template and registry tests, lifecycle-contract tests, Explorer tests,
  upgrade test; the generated diagnostic-code index refreshed.
- Documentation: a live note `docs/notes/decision-artifacts.md`, the notes
  index, `harnessctl-reference.md`, the domain index and this domain's
  README.

## Out of scope

- The risk artifact, in any form.
- Any change to the root managed copies, the lock, or the released
  evaluator; the root adopts at the next release adoption.
- Rewriting existing prose decisions or deviations into artifacts.
- Host integration that turns a presented option into a `decide` call; the
  command is the interface.
- Building, releasing, publishing or deploying anything.

## Authorized decision envelope

The implementation agent may choose the module layout, the internal
predicate implementation, the refusal wording within `SPEC-DCM-001` rule 5,
the `--scope` syntax within rule 6, the fixture layout, the Explorer's
visual treatment, and the note's structure. It may not admit a transition
by any field other than a disposition or a scoped deferral, may not let a
role without the right dispose, may not write a disposition outside the
atomic transition path, may not reuse the type for risks, and may not alter
a requirement or specification other than the ones enumerated here.

## Constraints

- Python 3.11+ standard library only.
- Deterministic gate evaluation and Explorer generation.
- Fail closed: a malformed decision blocks like an open one.
- Repository text stays inert in refusals and in the Explorer.
- The designed Explorer views change only through the count-asserted patch
  list of `SPEC-DST-023`.

## Expected change surface

The package `se_harness/` (layout, CLI, workflow, compliance, contracts,
provenance for record evidence); the candidate policies, templates and
scripts under `templates/repository/standard/`; the Explorer design sources
and the rebuilt template; tests; the decision-management packet and its
evidence; the domain index; the notes.

## Required verification

Execute `VER-DCM-001` in full: fixture tests for every blocked family and
every disposition path, taxonomy, template, registry, contract, Explorer
and upgrade tests; the full Windows suite against its known baseline;
formal validation and start/review preflight under the released evaluator;
`git diff --check`; a headless Explorer review of the in-flight tile and one
record panel with a standing deviation.

## Evidence to record

Retain under `docs/engineering/decision-management/evidence/WO-DCM-001-verification.md`:
commands and exit codes, test counts against the baseline, fixture
identities, one refusal text per blocked family, one disposition per path,
the Explorer observations, preflight results, deviations, and the actions
not performed.

## Stop and escalate conditions

Stop if the gate cannot be bound to a family's transition checkpoint
without changing the contract shape; if a disposition would need to be
written outside the atomic transition path; if the decision right cannot be
derived from `DECISION_RIGHTS.md` for a blocked type; if the designed views
need a change outside the patch list; or if the root managed copies would
have to change.

## Completion report format

Report the artifact type and template, the contract changes with their
tests, the command and its refusals, the diagnostics added, the Explorer
changes, the test counts against the baseline, the retained evidence path,
and the statement that root copies, lock, release and publication were not
changed.
