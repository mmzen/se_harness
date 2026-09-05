+++
id = "WO-HUP-016"
type = "work_order"
title = "Adopt exact public 0.15.0 as the standard root, the simple way"
status = "in_progress"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-09-05"
updated = "2026-09-05"

[assurance]
commit_bound_verification = "required"
rationale = "Every later gate, decision and release runs under the evaluator this transaction installs; the moved root, the candidate identity and the test assumptions are trusted engineering state, and this root is the first that reads decision artifacts and the reader-first templates."
decided_by = "repository-owner"

[execution_scope]
paths = [".engineering-harness.lock", ".engineering-harness.toml", ".github/workflows/engineering-harness.yml", "AGENTS.md", "ENGINEERING_HARNESS.md", "README.md", "GLOSSARY.md", "pyproject.toml", "se_harness/__init__.py", "docs/engineering/ARTIFACT_AUTHORING.md", "docs/engineering/DECISION_RIGHTS.md", "docs/engineering/QUALITY_GATES.json", "docs/engineering/QUALITY_GATES.md", "docs/engineering/TRACEABILITY.md", "docs/engineering/WORKFLOW.json", "docs/engineering/WORKFLOW.md", "docs/engineering/templates/", "scripts/", "tests/", "docs/notes/developing-se-harness.md", "docs/engineering/repository-harness-upgrade/README.md", "docs/engineering/repository-harness-upgrade/evidence/", "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-031.md", "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-032.md", "docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-016.md", "docs/engineering/repository-harness-upgrade/architecture/ARCH-HUP-012.md", "docs/engineering/repository-harness-upgrade/verification/VER-HUP-016.md"]

[relations]
implements = ["REQ-HUP-031", "REQ-HUP-032"]
specifications = ["SPEC-HUP-016"]
architecture = ["ARCH-HUP-012"]
verification = ["VER-HUP-016"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-05T08:35:42Z"
decided_by = "repository-owner"
reason = "Approved by the accountable repository owner on 2026-09-05 with the instruction 'i appprove' (approve), after reviewing PR #352 (REQ-HUP-031, REQ-HUP-032, SPEC-HUP-016, VER-HUP-016, WO-HUP-016) and the rehearsal of the 0.15.0 root adoption on a throwaway clone of main at e4192ed. WO-HUP-016 carries no delegation class: its start, completion and record preparation are the owners' explicit decisions."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-05T09:15:29Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-09-05, given with the words 'start, complete on green, prepare record'. Start preflight PASS after ARCH-HUP-012 was amended by record to address REQ-HUP-031 and REQ-HUP-032; the packet was approved and merged as cfd9c4d; the transaction runs from an LF clone whose lock bytes equal the committed blob."
+++

# Work Order: Adopt exact public 0.15.0 as the standard root, the simple way

## Lifecycle

This work order requires the accountable owners' approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `required`.

Its scope names no `verification-records/` directory: the gate admits this
work order's own records by construction on both sides of the move
(`ECP-ADM-001`).

## Objective

Use exact public 0.15.0, installed outside the checkout from the wheel file
whose digest `RLS-SEH-024` binds, to replace the 0.14.0 standard root with
one evidence-bound 0.15.0 root by the simple upgrade, one command and no
packet, and prove the complete graph and the repository suite under the
new root, without changing product, release, publication, deployment,
maintenance or external state. This adoption changes what the gate reads:
after it, this repository can raise `DEC-` artifacts, its new drafts use
the reader-first templates, and the draft-time advisories fire here.

## In scope

- Prove the installed 0.15.0 identity from the isolated environment;
  `SPEC-HUP-016` rules 1 and 2. Rehearsed on 2026-09-05 on a throwaway
  clone of `main` at `e4192ed`: wheel `eb09343f…`, payload `11e4ad03…`.
- Review the plan (rules 3 and 6). Measured: 48 files, 19 `update`, 1
  `add` (`DECISION.template.md`), 1 `adopt` (this repository's own
  `GLOSSARY.md`, kept byte for byte), 27 unchanged; nothing leaves the
  managed set.
- Apply with `harnessctl upgrade . --apply --evidence-output
  docs/engineering/repository-harness-upgrade/evidence/WO-HUP-016-evaluator-upgrade.json`;
  require the no-op replay (rules 4 and 5). Measured: replay 48 unchanged;
  prior lock `0425fccf…` (the committed LF lock), prior `tool_version
  0.14.0`.
- Update owner content only where it must state the new governor (rule 9).
- Move the candidate to `0.16.0` (rule 8).
- Replace the pinned root and candidate assumptions in `tests/` with
  identity-aware assertions (rule 10), each file named in the evidence.
- Run the complete `VER-HUP-016` qualification and the suite, and retain
  the evidence; hand off with the pull request's lanes green.

## Out of scope

Product source and templates other than the version identity; `RLS`, `VREC`
and `REL` records; tags, publication, replay and Pages workflows; the
published 0.15.0 itself; credentials; the workstation-only suite error the
control also reads; any first use of a decision artifact in this repository,
which is a later work order's act.

## Authorized decision envelope

The name of the external environment; the wording of the owner-content
statements; the order of readings; the exact identity-aware form of each
test edit, provided it asserts on the lock's identity and not on a literal.

## Constraints

- The applying runtime is exact public 0.15.0 outside the checkout, in
  isolated mode, installed from the digest-verified wheel file; a refusal
  by the guard is a stop, not a thing to bypass.
- No `customized`, `conflict` or unexpected `remove` action may be waived;
  a `null` archive pair is a stop.
- The complete graph must pass exact 0.15.0 directly after apply.
- Candidate template bytes under `templates/` must remain unchanged.
- The rehearsal clone was created with `core.autocrlf=false`, so the
  transaction document's prior lock digest is the committed LF blob's; the
  real transaction is run from a checkout whose lock bytes are LF as well,
  or the difference is recorded as `WO-HUP-015` recorded it.

## Expected change surface

The 19 reviewed `update` paths, the 1 `add`, the installer-owned lock with
its new seed entry; `AGENTS.md`'s owner region and
`docs/notes/developing-se-harness.md`; `pyproject.toml`,
`se_harness/__init__.py`; the test modules the evidence names; this
packet, the domain index, the transaction JSON and the evidence packet.

## Required verification

Execute `VER-HUP-016` in full; repository-required checks; the pull
request's lanes green; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-016/` and
`WO-HUP-016-evaluator-upgrade.json`.

## Stop and escalate conditions

A guard refusal, a plan path outside the managed set, customization,
conflict, an unexpected removal, a `null` archive pair, a partial
transaction, a failed replay, a failed graph, a suite whose failure set
differs from the control beyond the names the evidence explains, an
unexplained warning or advisory, a product or release byte moved beyond
the version identity, or a need for authority beyond the approved stage.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
