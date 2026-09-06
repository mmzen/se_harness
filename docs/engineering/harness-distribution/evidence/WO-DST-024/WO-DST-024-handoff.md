```toml
artifact = "WO-DST-024"
checkpoint = "handoff"
formal_snapshot_sha256 = "d5ce28c121ea3c9a06758bfcef6578a47da8bf8b1e504a52eef0a37a111ad089"
rebound_at = "2026-09-06T15:14:58Z"
```

# WO-DST-024 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## What the candidate does

The five evaluator files that the standard template carried under
`scripts/` now live in `se_harness/engine/` and ship inside the wheel as
modules and package data (`SPEC-DST-025` DST-ENG-001 to DST-ENG-003). The two
shell wrappers and the unused `select_harness_work_order.py` are deleted
(DST-ENG-008, DST-ENG-009). The evaluator resolves its scripts through
`se_harness.installer.engine_script` and `ENGINE_ROOT` (DST-ENG-004,
DST-ENG-005); the subprocess invocation is unchanged (DST-ENG-006,
DST-ENG-007). The validator reads the package's own `workflow_contract.json`,
byte-identical to the template's `docs/engineering/WORKFLOW.json`. The
required-path list in `preflight.py` names no `scripts/` path (DST-ENG-010).
The Explorer build tool's default output and the diagnostic-code index's
scan roots follow the move, under the scope amendment the owner selected.

## What was measured

Full detail, with command output, is retained in
`docs/engineering/harness-distribution/evidence/WO-DST-024-verification.md`.

- Released 0.15.0 evaluator from its venv outside the checkout: `validate`
  0 errors, warning count unchanged; `preflight --phase review` no
  diagnostics; scope checkpoint `completed` against the merge-base before and
  after `main` was merged in.
- Candidate wheel built into a directory outside the checkout: engine members
  present once under `se_harness/engine/`, no `share/.../scripts/` member,
  no retired name. Scenario A (fresh `init`): 40 files, no `scripts/` path,
  no `scripts/` lock entry, `doctor`, `validate`, `dashboard` pass. Scenario
  B (0.15.0 installation upgraded): eight `remove` actions, applied,
  `scripts/` gone, lock clean, `doctor` exit 0, file set identical to a fresh
  init. Scenario C (one edited retired copy): `customized`, nothing written.
- Local Windows suite as control: 1265 tests, 0 failures, 1 error that is
  the known temporary-directory teardown flake, 26 Windows-only skips.
- This repository's root `scripts/` files, lock and AGENTS.md are byte-identical
  to `main` (DST-ENG-014).

## What did not happen

No transition beyond `in_progress` was applied. No verification record was
prepared. Nothing was built for promotion, released, published or adopted.
The root footprint, the lock and AGENTS.md are unchanged; DST-ENG-015 and
DST-ENG-016 bind the root-adoption work order that adopts the carrying release.

## Decision that remains

`DR-WO-COMPLETE`, engineering owner: mark WO-DST-024 `implemented` once the
hosted Linux lane is green on the final head, or stop.
