+++
id = "WO-HUP-013"
type = "work_order"
title = "Adopt exact public 0.12.0 as the standard root, the simple way"
status = "draft"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-31"
updated = "2026-08-31"

[assurance]
commit_bound_verification = "required"
rationale = "Every later gate, decision and release runs under the evaluator this transaction installs; the moved root, the candidate identity and the test assumptions are trusted engineering state."
decided_by = "repository-owner"

[execution_scope]
paths = [".engineering-harness.lock", ".engineering-harness.toml", ".github/workflows/engineering-harness.yml", "AGENTS.md", "ENGINEERING_HARNESS.md", "README.md", "docs/engineering/DECISION_RIGHTS.md", "docs/engineering/WORKFLOW.json", "docs/engineering/WORKFLOW.md", "docs/engineering/templates/WORK_ORDER.template.md", "scripts/validate_engineering_artifacts.py", "pyproject.toml", "se_harness/__init__.py", "tests/", "docs/notes/developing-se-harness.md", "docs/engineering/repository-harness-upgrade/README.md", "docs/engineering/repository-harness-upgrade/evidence/", "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-025.md", "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-026.md", "docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-013.md", "docs/engineering/repository-harness-upgrade/architecture/ARCH-HUP-010.md", "docs/engineering/repository-harness-upgrade/verification/VER-HUP-013.md"]

[relations]
implements = ["REQ-HUP-025", "REQ-HUP-026"]
specifications = ["SPEC-HUP-013"]
architecture = ["ARCH-HUP-010"]
verification = ["VER-HUP-013"]
+++

# Work Order: Adopt exact public 0.12.0 as the standard root, the simple way

## Lifecycle

This work order requires the accountable owners' approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `required`.

Its scope names no `verification-records/` directory: the gate admits this
work order's own records by construction on both sides of the move
(`ECP-ADM-001`).

## Objective

Use exact public 0.12.0, installed outside the checkout from the wheel file
whose digest `RLS-SEH-021` binds, to replace the 0.11.0 standard root with
one evidence-bound 0.12.0 root by the simple upgrade — one command, no
packet — and prove the complete graph and the repository suite under the
new root, without changing product, release, publication, deployment,
maintenance or external state.

## In scope

- Prove the installed 0.12.0 identity (version, payload digest, archive
  pair equal to the published wheel) from the isolated environment;
  `SPEC-HUP-013` rules 1 and 2. Rehearsed on 2026-08-31 on a throwaway
  clone of `main` at `63889f7`: wheel `se_harness-0.12.0-py3-none-any.whl`
  `639edbeed4bdca7c9e21a5eb2afc3b9fc993ddb3f66177eec962f1646a545811`,
  payload `0df83ce9c9bb6d456f3244f517031753daee740bb22180a492f835d25831ee0d`.
- Review the plan against the installer's managed set: `add` or `update`
  only, no `customized`, no `conflict`, no unexpected `remove` (rules 3
  and 6). Measured: 46 files, 8 `update`, 38 unchanged; nothing leaves the
  managed set.
- Apply with `harnessctl upgrade . --apply --evidence-output
  docs/engineering/repository-harness-upgrade/evidence/WO-HUP-013-evaluator-upgrade.json`;
  require the no-op replay (rules 4 and 5). Measured at rehearsal: replay
  46 unchanged; prior lock `e3f7039416fd…`, prior `tool_version 0.11.0`.
- Update owner content only where it must state the new governor: the
  `se-harness==0.11.0` instruction and the stored-payload pull-request trap
  in `AGENTS.md`'s owner region, and the candidate/root statements in
  `docs/notes/developing-se-harness.md` (rule 9).
- Move the candidate to `0.13.0` (`pyproject.toml`,
  `se_harness/__init__.py`, the README install example); no scenario and
  no legacy table exist (rule 8).
- Replace pinned root and candidate assumptions in `tests/` with
  identity-aware assertions, each named in the evidence (rule 10); the
  rehearsal names exactly one test module
  (`tests/test_instruction_architecture.py`: the managed count of root
  0.12.0 and the live-body operational fact) beyond the owner-content
  files.
- Run the complete `VER-HUP-013` qualification and the suite, and retain
  the evidence; hand off with the pull request's lanes green.

## Out of scope

Product source and templates other than the version identity; `RLS`, `VREC`
and `REL` records; tags, publication, replay and Pages workflows; the
`release/0.12` line and the latest markers (they follow `REL-SEH-023`'s
promotion policy after this observation window); branch protection and the
delegation demonstration (issue #284's later stages); credentials; the
published 0.12.0 itself, which does not move; the workstation-only suite
error the control also reads.

## Authorized decision envelope

The name of the external environment; the wording of the owner-content
statements; which assertion form replaces each pinned test assumption,
provided the released-root identity and the candidate templates are both
still asserted; the order of readings.

## Constraints

- The applying runtime is exact public 0.12.0 outside the checkout, in
  isolated mode, installed from the digest-verified wheel file; a refusal
  by the guard is a stop, not a thing to bypass.
- No `customized`, `conflict` or unexpected `remove` action may be waived;
  a `null` archive pair is a stop.
- The complete graph must pass exact 0.12.0 directly after apply.
- Candidate template bytes must remain unchanged.

## Expected change surface

The 8 reviewed `update` paths and the installer-owned lock; `AGENTS.md`'s
owner region and `docs/notes/developing-se-harness.md`; `pyproject.toml`,
`se_harness/__init__.py`, `README.md`; the one test module the evidence
names; this packet, the domain index, the transaction JSON and the
evidence packet.

## Required verification

Execute `VER-HUP-013` in full; repository-required checks; the pull
request's lanes green; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-013/` and
`WO-HUP-013-evaluator-upgrade.json`.

## Stop and escalate conditions

A guard refusal, a plan path outside the managed set, customization,
conflict, an unexpected removal, a `null` archive pair, a partial
transaction, a failed replay, a failed graph, a suite whose failure set
differs from the control beyond the names the evidence explains, an
unexplained warning, a product or release byte moved beyond the version
identity, or a need for authority beyond the approved stage.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
