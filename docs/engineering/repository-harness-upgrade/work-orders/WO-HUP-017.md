+++
id = "WO-HUP-017"
type = "work_order"
title = "Adopt exact public 0.16.0 as the standard root, the simple way, and let the retired scripts leave"
status = "draft"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-09-07"
updated = "2026-09-07"

[assurance]
commit_bound_verification = "required"
rationale = "Every later gate, decision and release runs under the evaluator this transaction installs; the moved root, the candidate identity, the three release workflows switched to evaluator commands and the test assumptions are trusted engineering state, and this is the first root that installs no script copy."
decided_by = "repository-owner"

[execution_scope]
paths = [".engineering-harness.lock", ".engineering-harness.toml", ".github/workflows/engineering-harness.yml", ".github/workflows/release-qualification.yml", ".github/workflows/release-candidate-replay.yml", ".github/workflows/pages-publication.yml", "AGENTS.md", "ENGINEERING_HARNESS.md", "pyproject.toml", "se_harness/__init__.py", "docs/engineering/ARTIFACT_AUTHORING.md", "docs/engineering/templates/", "scripts/", "tests/", "docs/notes/developing-se-harness.md", "docs/engineering/instruction-architecture/specifications/SPEC-IAR-012.md", "docs/engineering/repository-harness-upgrade/README.md", "docs/engineering/repository-harness-upgrade/evidence/", "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-033.md", "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-034.md", "docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-017.md", "docs/engineering/repository-harness-upgrade/architecture/ARCH-HUP-012.md", "docs/engineering/repository-harness-upgrade/verification/VER-HUP-017.md"]

[relations]
implements = ["REQ-HUP-033", "REQ-HUP-034"]
specifications = ["SPEC-HUP-017"]
architecture = ["ARCH-HUP-012"]
verification = ["VER-HUP-017"]
+++

# Work Order: Adopt exact public 0.16.0 as the standard root, the simple way, and let the retired scripts leave

## Lifecycle

This work order requires the accountable owners' approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `required`.

Its scope names no `verification-records/` directory: the gate admits this
work order's own records by construction on both sides of the move
(`ECP-ADM-001`).

## Objective

Use exact public 0.16.0, installed outside the checkout from the wheel file
whose digest `RLS-SEH-025` binds, to replace the 0.15.0 standard root with
one evidence-bound 0.16.0 root by the simple upgrade, one command and no
packet; let the eight retired script copies leave the tree and the lock
through the installer's leaving-set rule; switch the three release workflows,
the owner region, one specification's count and the tests that read those
copies to the evaluator, as `SPEC-DST-025` binds this work order to do; and
prove the complete graph and the repository suite under the new root,
without changing product, release, publication, deployment, maintenance or
external state. After it, the in-tree `doctor` reports no `lock-extra`
finding and `WO-TCM-011` may start.

## In scope

- Prove the installed 0.16.0 identity from the isolated environment;
  `SPEC-HUP-017` rules 1 and 2. Rehearsed on 2026-09-07 on a throwaway LF
  clone of `main` at `5df10aa9`: wheel `a969d6ab…`, payload `51712fcf…`.
- Review the plan (rules 3 and 6). Measured: 48 files, 6 `update`, 8
  `remove` (the eight retired copies, byte-identical to their lock
  entries), 34 unchanged; no `add`, `adopt`, `customized` or `conflict`.
- Apply with `harnessctl upgrade . --apply --evidence-output
  docs/engineering/repository-harness-upgrade/evidence/WO-HUP-017-evaluator-upgrade.json`;
  require the no-op replay (rules 4 and 5). Measured: replay 40 unchanged;
  prior lock `f617ff0b…` (the committed LF lock), prior `tool_version
  0.15.0`; forty lock entries, none under `scripts/`.
- Update owner content where it must state the new governor and where
  `DST-ENG-015` binds this work order (rule 9): `AGENTS.md`'s owner region,
  `docs/notes/developing-se-harness.md`, the amendment record on
  `SPEC-IAR-012`.
- Move the candidate to `0.17.0` (rule 8).
- Switch `release-qualification.yml`, `release-candidate-replay.yml` and
  `pages-publication.yml` from root scripts to evaluator commands (rule 11,
  `DST-ENG-016`).
- Replace the pinned root and candidate assumptions in `tests/` with
  identity-aware assertions (rule 10), each file named in the evidence.
- Run the complete `VER-HUP-017` qualification and the suite, and retain
  the evidence; hand off with the pull request's lanes green.

## Out of scope

Product source and templates other than the version identity; `RLS`, `VREC`
and `REL` records; tags, publication, replay and Pages runs; the published
0.16.0 itself; credentials; the workstation-only suite error the control
also reads; the start of `WO-TCM-011`, which is its delegated executor's
act after this adoption merges; the removal of the `adopt` alias
(`REQ-ECP-030`).

## Authorized decision envelope

The name of the external environment; the wording of the owner-content
statements and the amendment record; the order of readings; the exact
identity-aware form of each test edit, provided it asserts on the lock's
identity and not on a literal; the exact form of each workflow line,
provided it invokes the evaluator's `validate` or `dashboard` and changes
nothing else in the step.

## Constraints

- The applying runtime is exact public 0.16.0 outside the checkout, in
  isolated mode, installed from the digest-verified wheel file; a refusal
  by the guard is a stop, not a thing to bypass.
- No `customized`, `conflict`, `add`, `adopt` or `remove` beyond the eight
  named copies may be waived; a `null` archive pair is a stop.
- The complete graph must pass exact 0.16.0 directly after apply.
- Candidate template bytes under `templates/` must remain unchanged; no
  byte under `se_harness/` moves beyond `__init__.py`'s version.
- The transaction runs from a checkout whose lock bytes are LF, so the
  transaction document's prior lock digest is the committed blob's.

## Expected change surface

The 6 reviewed `update` paths, the 8 removals, the installer-owned lock;
`AGENTS.md`'s owner region, `docs/notes/developing-se-harness.md`,
`SPEC-IAR-012`'s amendment record; the three workflows; `pyproject.toml`,
`se_harness/__init__.py`; the test modules the evidence names; this
packet, the domain index, the transaction JSON and the evidence packet.

## Required verification

Execute `VER-HUP-017` in full; repository-required checks; the pull
request's lanes green; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-017/` and
`WO-HUP-017-evaluator-upgrade.json`.

## Stop and escalate conditions

A guard refusal, a plan path outside the measured shape, customization,
conflict, a removal beyond the eight, a `null` archive pair, a partial
transaction, a failed replay, a failed graph, a suite whose failure set
differs from the control beyond the names the evidence explains, an
unexplained warning or advisory, a product or release byte moved beyond
the version identity, a workflow step changed beyond its script invocation,
or a need for authority beyond the approved stage.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
