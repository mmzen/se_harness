+++
id = "WO-ECP-017"
type = "work_order"
title = "Remove the focus alias and move harness-orient to check"
status = "draft"
owners = ["engineering-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[assurance]
commit_bound_verification = "required"
rationale = "The change removes a public CLI command and changes the digest of a shipped skill core whose identity is retained history; both are trusted engineering state later decisions rely on, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/cli.py",
  "se_harness/workflow.py",
  "se_harness/workflow_compliance.py",
  "tests/test_workflow_execution.py",
  "tests/test_agentic_execution.py",
  "tests/fixtures/focus_alias/",
  "tests/fixtures/agentic_execution/fake_evaluator.py",
  "tests/fixtures/agentic_execution/phase5/",
  "templates/repository/standard/.agents/skills/harness-orient/",
  "templates/repository/standard/docs/engineering/README.md.seed",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/harnessctl-check.md",
  "docs/notes/harness-orient.md",
  "AGENTS.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/verification-records/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-024.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-013.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-013.md",
]

[relations]
implements = ["REQ-ECP-024", "REQ-ECP-022"]
specifications = ["SPEC-ECP-013", "SPEC-ECP-011"]
architecture = ["ARCH-ECP-001", "ADR-ECP-007"]
verification = ["VER-ECP-013", "VER-ECP-011"]
+++

# Work Order: Remove the focus alias and move harness-orient to check

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above.

Commit-bound verification is `required`.

## Objective

Close the alias window: delete the `focus` subcommand behind a guard that
names `check` (`ECP-RMV-001` to `ECP-RMV-003`), move the shipped
`harness-orient` core to `check` — the `ECP-ONE-007` rule of
`SPEC-ECP-011` deferred at `WO-ECP-015`'s completion — with a phase-5
vector row that keeps every earlier identity as history (`ECP-RMV-004`,
`ECP-RMV-005`), retire the alias tests and fixture (`ECP-RMV-006`), and
make the notes and the owner instructions say `check` (`ECP-RMV-007`).
Audit item P1 of 2026-08-29.

## Why now

The alias window `ECP-ONE-004` opened is one release; 0.10.0 shipped the
alias, so the next candidate is where it goes. Doing it now also performs
the one vector re-baseline the audit's P2 (`next`) will reuse.

## In scope

- `se_harness/cli.py`: parser and handler removal; the pre-parse guard.
- `se_harness/workflow.py`, `se_harness/workflow_compliance.py`: the
  projection under one name.
- `templates/repository/standard/.agents/skills/harness-orient/`:
  `scripts/orient.py`, `SKILL.md` (`skill-contract.json` unchanged).
- `tests/fixtures/agentic_execution/phase5/portable-vectors.json` (new),
  `fake_evaluator.py`; `tests/fixtures/focus_alias/` (deleted);
  `tests/test_workflow_execution.py`, `tests/test_agentic_execution.py`.
- `docs/notes/harnessctl-reference.md`, `harnessctl-check.md`,
  `harness-orient.md`; the template `README.md.seed`; this repository's
  `AGENTS.md` owner region (outside the managed block).
- The packet, this domain's index and its `verification-records/` (the
  hosted lane runs the released 0.10.0 evaluator, which lacks
  `ECP-ADM-001`).

## Out of scope

Any change to `focus-json` as an operation identifier or to any
skill-contract.json, profile or retained receipt; the `next` command
(audit P2); the root `.agents/skills/` copies (hash-locked, moved by the
next root adoption); any contract file; the release carrying this change.

## Authorized decision envelope

The wording of the guard's message and of the notes; the phase-5 fixture's
layout, provided it carries `previous` and `current`; test names.

## Constraints

- The phase-1, phase-3 and phase-4 vector fixtures are byte-unchanged.
- No hash-locked root file moves; the root `harness-orient` stays at its
  0.10.0 bytes.
- `check`'s stdout and `--json` bytes are unchanged (`ECP-ONE-002`).

## Expected change surface

Three product modules, two test modules, two fixture trees (one added, one
removed), one skill core (two files), four notes, one owner region, the
packet and the index.

## Required verification

Execute `VER-ECP-013` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-017/`.

## Stop and escalate conditions

Any test that can only pass by editing a retained vector row; any need to
touch a skill contract, a profile in `skill_contract.py` or the
`focus-json` identifier; any hash-locked file in the change set.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's, and it
closes the `ECP-ONE-007` deferral recorded on `WO-ECP-015`.
