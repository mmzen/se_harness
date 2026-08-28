+++
id = "WO-ECP-001"
type = "work_order"
title = "Ship `harnessctl next` and Git-derived change sets"
status = "approved"
owners = ["engineering-owner"]
created = "2026-08-27"
updated = "2026-08-28"

[assurance]
commit_bound_verification = "required"
rationale = "The work adds a product command every agent will call first, changes how `check` derives the change set that `QGP-G4I-PATHS` evaluates, and edits the managed workflow contract. Every later scope, handoff, and release decision relies on exact candidate behaviour, so commit-bound assurance is required."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/cli.py",
  "se_harness/workflow.py",
  "se_harness/workflow_compliance.py",
  "se_harness/workflow_procedures.py",
  "se_harness/preflight.py",
  "se_harness/workflow_contract.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "docs/notes/harnessctl-reference.md",
  "tests/test_workflow_execution.py",
  "tests/test_workflow_compliance.py",
  "docs/engineering/execution-control-plane/evidence/",
]

[relations]
implements = ["REQ-ECP-001", "REQ-ECP-002"]
specifications = ["SPEC-ECP-001"]
architecture = ["ARCH-ECP-001", "ADR-ECP-001"]
verification = ["VER-ECP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T20:35:00Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-28 with the words 'Approve and start', as the first work order of the execution-control-plane plan recorded in ADR-AEX-008 and the agentic-execution README. Its definitions REQ-ECP-001, REQ-ECP-002, SPEC-ECP-001, ARCH-ECP-001, ADR-ECP-001 and VER-ECP-001 were approved separately on 2026-08-28. Authorizes start preflight and then only the declared scope: harnessctl next as a projection of focus, preflight and select_current_step; check --from-git deriving the change set from Git; the WEX210 corrective; the contract JSON, template WORKFLOW renderings, reference note, the two test modules and evidence. Two deviations from the packet text are accepted in advance and to be recorded in the evidence: readings are taken with the governing exact public 0.8.0 root, not 0.7.1 as written on 2026-08-27; and the root managed WORKFLOW copies, now byte-identical to the templates, stay unedited while the templates move. Measured before this transition over main 233bc92: validate PASS at 0 errors under 0.8.0. It authorizes no verification record, no release and no publication."
+++

# Work Order: Ship `harnessctl next` and Git-derived change sets

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification, the assurance-owner decision, integration, and release are
separate decisions by the roles that own them. Approval of `REQ-ECP-001`,
`REQ-ECP-002`, `SPEC-ECP-001`, `ARCH-ECP-001`, `ADR-ECP-001`, and
`VER-ECP-001` are separate acts by their owners and precede approval of
this work order. This is the first work order of the packet and depends on
no other; `WO-ECP-002`, `WO-ECP-003`, and `WO-ECP-008` depend on it.

## Objective

Give an agent one call that returns its complete execution context, and
make `check` derive the changed-path set from Git instead of from paths the
agent types. Today the next step is emitted only after an operation, `focus`
gives the decision step rather than the `check` command, and no `next`
command exists (the 2026-08 agentic execution review,
`docs/notes/agentic-execution-review-2026-08.md:304-306`); scope paths are
agent-typed and never compared to `git diff`
(`se_harness/workflow_compliance.py:156-165`, `:316-322`; review section 3).

## In scope

- `harnessctl next <repo> [--artifact ID] --json` composing `focus_schema2`,
  `run_preflight`, and `select_current_step` into one schema-2 result per
  `ECP-NXT-*`, with `decision_required` and a concrete next argv.
- `check --from-git <base>` deriving the change set from
  `git diff --name-only <base>` plus untracked, minus ignored, per
  `ECP-CHG-*`; refusal when combined with `--changed-path`; fail-closed
  `not_assessable` on an unresolvable base.
- The `QGP-G4I-COMPLETE` corrective in `se_harness/workflow_contract.json`
  and the template `WORKFLOW.json` and `WORKFLOW.md` updated to name
  `--from-git`; the "rerun the same command" compatibility corrective
  removed (`WORKFLOW.json:83`, review section 3).
- Reference note section for `next` and `--from-git`.
- Tests in the two named modules; work-order-keyed evidence.

## Out of scope

- The trimmed manifest and chain-scoped snapshot (`WO-ECP-008`); evidence
  authoring, identifier allocation, and body generation (`WO-ECP-002`); the
  CI gate and digest (`WO-ECP-003`); any change to lifecycle states, gate
  predicates, decision rights, or root managed copies; any lifecycle
  transition of any artifact.

## Authorized decision envelope

The implementation agent may decide the internal field order of the `next`
result within schema 2, the diagnostic code numbers within the `WEX`
prefix, test names, and the note's wording. It may not add a second rule
table, change any predicate identifier, change the meaning of
`--changes-complete`, or write outside the listed paths.

## Constraints

- Use the exact released evaluator, se-harness 0.7.1, installed outside the
  checkout, for identity, integrity, graph, focus, and preflight readings.
- Root managed copies (`docs/engineering/WORKFLOW.json`, `WORKFLOW.md`,
  `AGENTS.md`, `CLAUDE.md`, `ENGINEERING_HARNESS.md`, the root scripts, and
  the lock) are not edited; the template copies are, and the root follows
  on the next managed upgrade.
- LF line endings; assert bytes against blobs.
- Stage every deletion before any preflight or check run;
  `hash_bound.assess` reads index-tracked paths.

## Expected change surface

CLI parser and dispatch, the workflow kernel's projection helpers, the
compliance module's change-set builder, one contract JSON and its two
template renderings, one note, two test modules, evidence.

## Required verification

Execute `VER-ECP-001` completely for `REQ-ECP-001` and `REQ-ECP-002`
(Scenarios 1 to 5 and the corresponding property, static, and security
checks) plus the repository-required checks; run the complete suite on
Linux and Windows with figures labelled per platform.

## Evidence to record

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-001/`:
commands and results, the `next` JSON per state, the fixture tree listings
and derived change sets, the refusal diagnostics, per-platform test
figures, and the complete changed-path set.

## Stop and escalate conditions

Stop if `next` cannot be expressed as a projection of existing kernel
functions without a second selector, if deriving the change set requires a
Git version newer than the one CI runs, if any predicate identifier must
change, or if any path outside scope must change.

## Completion report format

Return the `harnessctl check . --artifact WO-ECP-001 --checkpoint handoff`
schema-2 block verbatim with the complete changed-path set asserted, and
its `result_sha256`.
