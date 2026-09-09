+++
id = "WO-HUP-018"
type = "work_order"
title = "Adopt exact public 0.17.0 as the standard root, the simple way, and take the carried obligations into the root"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-09-09"
updated = "2026-09-09"

[assurance]
commit_bound_verification = "required"
rationale = "Every later gate, decision and release runs under the evaluator this transaction installs; the moved root, the candidate identity, the reduced configuration, the hardened managed workflow and the test assumptions are trusted engineering state."
decided_by = "repository-owner"

[execution_scope]
paths = [".engineering-harness.lock", ".engineering-harness.toml", ".github/workflows/engineering-harness.yml", ".gitignore", "AGENTS.md", "ENGINEERING_HARNESS.md", "pyproject.toml", "se_harness/__init__.py", "docs/engineering/QUALITY_GATES.json", "docs/engineering/QUALITY_GATES.md", "docs/engineering/TRACEABILITY.md", "docs/engineering/WORKFLOW.json", "docs/engineering/WORKFLOW.md", "docs/engineering/templates/", "tests/", "docs/notes/developing-se-harness.md", "docs/engineering/instruction-architecture/specifications/SPEC-IAR-012.md", "docs/engineering/repository-harness-upgrade/README.md", "docs/engineering/repository-harness-upgrade/evidence/", "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-035.md", "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-036.md", "docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-018.md", "docs/engineering/repository-harness-upgrade/architecture/ARCH-HUP-012.md", "docs/engineering/repository-harness-upgrade/verification/VER-HUP-018.md"]

[relations]
implements = ["REQ-HUP-035", "REQ-HUP-036"]
specifications = ["SPEC-HUP-018"]
architecture = ["ARCH-HUP-012"]
verification = ["VER-HUP-018"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-09T09:04:33Z"
decided_by = "repository-owner"
reason = "Approved by the accountable repository owner on 2026-09-09 by selecting the presented option 'Approve all five (Recommended)', after reviewing PR #426 (REQ-HUP-035, REQ-HUP-036, SPEC-HUP-018, VER-HUP-018, WO-HUP-018) and the rehearsal of the 0.17.0 root adoption on a throwaway LF clone of main at e855cc9a. WO-HUP-018 carries no delegation class: its start, completion and record preparation are the owners' explicit decisions."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-09T09:37:09Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-09-09, given with the words 'merged => start' after the approved packet #426 merged to main at b172f42a. Start preflight PASS with no diagnostics over the reading manifest after ARCH-HUP-012 was amended by record on the packet branch; the transaction runs from an LF checkout whose lock bytes equal the committed blob."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-09T10:03:00Z"
decided_by = "engineering-owner"
reason = "Completed by the accountable engineering owner on 2026-09-09 under DR-WO-COMPLETE, by selecting the presented option 'Complete and prepare the record (Recommended)' for WO-HUP-018 (PR #427). The standard root is exact public 0.17.0 by the simple upgrade from the isolated wheel-file environment (transaction d8ba7a23: 41 managed files, 10 updated, RISK.template.md added, replay 41 unchanged; prior lock 69d0fb9f under 0.16.0, target archive 305c7cbc, payload dd48b16b, document WO-HUP-018-evaluator-upgrade.json); the root configuration holds its five keys and the root workflow and ignore block take the release's template (DST-CFG-015, DST-MWF-014 discharged). VER-HUP-018 executed in full under exact 0.17.0: validate 1442 artifacts, 0 errors, 46 warnings, 0 advisories; doctor 99/0; released-root qualification RR001-RR004 PASS; inspect 0; identical Explorer digests twice; review preflight PASS; identity passed; derive PRE008 then 0.17.0 to 0.18.0; the Windows suite's failure set equals the same-commit 0.16.0 control's (1098 tests, the one workstation baseline error, 23 skips). HUP-ADS-011 to HUP-ADS-015 applied: the candidate 0.18.0, the owner region, the developing note, the SPEC-IAR-012 amendment record, the duplicated ignore lines dropped; no test needed an identity-aware edit. All four lanes green at the evidence head 39fc1352, the governor-transition lane assessing the real 0.16.0 to 0.17.0 move with one transaction document and RLS-SEH-026 supplying the wheel. Evidence: docs/engineering/repository-harness-upgrade/evidence/WO-HUP-018/WO-HUP-018-handoff.md, bound at handoff."
+++

# Work Order: Adopt exact public 0.17.0 as the standard root, the simple way, and take the carried obligations into the root

## Lifecycle

This work order requires the accountable owners' approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `required`.

Its scope names no `verification-records/` directory: the gate admits this
work order's own records by construction on both sides of the move
(`ECP-ADM-001`).

## Objective

Use exact public 0.17.0, installed outside the checkout from the wheel file
whose digest `RLS-SEH-026` binds, to replace the 0.16.0 standard root with
one evidence-bound 0.17.0 root by the simple upgrade, one command and no
packet; take the reduced configuration (`DST-CFG-015`), the hardened
managed workflow and the hash-marked ignore block (`DST-MWF-014`) and the
risk template into the root; move the candidate to 0.18.0; keep the owner
region, the developing note, one specification's count and the tests that
pin the root's shape truthful; and prove the complete graph and the
repository suite under the new root, without changing product, release,
publication, deployment, maintenance or external state.

## In scope

- Prove the installed 0.17.0 identity from the isolated environment;
  `SPEC-HUP-018` `HUP-ADS-001` to `HUP-ADS-003`. Rehearsed on 2026-09-09 on
  a throwaway LF clone of `main` at `e855cc9a`: wheel `305c7cbc…`, payload
  `dd48b16b…`.
- Review the plan (`HUP-ADS-004`, `HUP-ADS-005`). Measured: 41 files, 10
  `update` (`.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`,
  `.gitignore`, `ENGINEERING_HARNESS.md`, `QUALITY_GATES.json`,
  `QUALITY_GATES.md`, `TRACEABILITY.md`, `WORKFLOW.json`, `WORKFLOW.md`,
  `templates/README.md`), 1 `add` (`templates/RISK.template.md`), 30
  unchanged; no `remove`, `adopt`, `customized` or `conflict`.
- Apply with `harnessctl upgrade . --apply --evidence-output
  docs/engineering/repository-harness-upgrade/evidence/WO-HUP-018-evaluator-upgrade.json`;
  require the no-op replay (`HUP-ADS-006` to `HUP-ADS-008`). Measured:
  replay 41 unchanged; prior lock `69d0fb9f…` (the committed LF lock), prior
  `tool_version 0.16.0`; forty-one lock entries.
- Record the carried obligations discharged (`HUP-ADS-014`, `HUP-ADS-015`):
  the root configuration in its five-key form with its new digest, the root
  workflow equal to the release's template, the ignore block between hash
  markers; drop the two root ignore lines the fragment duplicates, which
  `DST-MWF-014` allows.
- Update owner content where it must state the new governor (`HUP-ADS-012`,
  `HUP-ADS-013`): `AGENTS.md`'s owner region, `docs/notes/developing-se-harness.md`,
  the amendment record on `SPEC-IAR-012`.
- Move the candidate to `0.18.0` (`HUP-ADS-011`).
- Replace the pinned root assumptions in `tests/` with identity-aware
  assertions or fixtures (`HUP-ADS-016`, `HUP-ADS-017`), each file named in
  the evidence.
- Run the complete `VER-HUP-018` qualification and the suite, and retain
  the evidence; hand off with the pull request's lanes green.

## Out of scope

Product source and templates other than the version identity; `RLS`, `VREC`
and `REL` records; tags, publication, replay and Pages runs; the published
0.17.0 itself; credentials; the workstation-only suite error the control
also reads; the start of `WO-TCM-011`, which is its delegated executor's
act after this adoption merges.

## Authorized decision envelope

The name of the external environment; the wording of the owner-content
statements and the amendment record; the order of readings; the exact
identity-aware form of each test edit, provided it asserts on the lock's
identity and not on a literal; whether the duplicated root ignore lines are
dropped.

## Constraints

- The applying runtime is exact public 0.17.0 outside the checkout, in
  isolated mode, installed from the digest-verified wheel file; a refusal
  by the guard is a stop, not a thing to bypass.
- No `customized`, `conflict`, `adopt` or `remove`, and no `add` beyond the
  risk template, may be waived; a `null` archive pair is a stop.
- The complete graph must pass exact 0.17.0 directly after apply.
- Candidate template bytes under `templates/` must remain unchanged; no
  byte under `se_harness/` moves beyond `__init__.py`'s version.
- The transaction runs from a checkout whose lock bytes are LF, so the
  transaction document's prior lock digest is the committed blob's.
- Every commit carries the `Harness-Work-Order: WO-HUP-018` trailer in one
  trailer block.

## Expected change surface

The 10 reviewed `update` paths, the added risk template, the installer-owned
lock; `AGENTS.md`'s owner region, `docs/notes/developing-se-harness.md`,
`SPEC-IAR-012`'s amendment record; `pyproject.toml`,
`se_harness/__init__.py`; the test modules the evidence names; this packet,
the domain index, the transaction JSON and the evidence packet.

## Required verification

Execute `VER-HUP-018` in full; repository-required checks; the pull
request's lanes green; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-018/` and
`WO-HUP-018-evaluator-upgrade.json`.

## Stop and escalate conditions

A guard refusal, a plan path outside the measured shape, customization,
conflict, a removal, an addition beyond the risk template, a `null` archive
pair, a partial transaction, a failed replay, a failed graph, a suite whose
failure set differs from the control beyond the names the evidence explains,
an unexplained warning or advisory, a product or release byte moved beyond
the version identity, or a need for authority beyond the approved stage.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
