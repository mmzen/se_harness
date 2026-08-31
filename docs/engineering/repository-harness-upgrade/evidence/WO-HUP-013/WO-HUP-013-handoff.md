```toml
artifact = "WO-HUP-013"
checkpoint = "handoff"
formal_snapshot_sha256 = "05fc20f9eba875fe6788e81dd08ce924c3a2c0459caf78d45158a964ec4333b9"
rebound_at = "2026-08-31T13:18:46Z"
```

# WO-HUP-013 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The standard root is exact public 0.12.0: lock schema 3, `tool_version
0.12.0`, archive `639edbee…` equal to the wheel `RLS-SEH-021` binds,
payload `0df83ce9…`, written by the simple upgrade from the isolated
wheel-file environment in one atomic transaction (46 managed files, 8
updated, replay 46 unchanged; nothing left the managed set). The candidate
moved to 0.13.0. The 0.12.0 gate reads its own numbers over this graph:
0 errors, 65 warnings, 0 advisories.

## Evaluators

- Predecessor (approval, start): released `se-harness 0.11.0` outside the
  checkout, wheel-installed.
- Governor from the transaction onward: released `se-harness 0.12.0`
  outside the checkout (`C:/Users/mathi/se-harness-eval-0120`), installed
  from the wheel file verified against `RLS-SEH-021` before install; every
  later reading, the packet and the handoff check included.
- Candidate: this checkout, branch `governance/hup-013-adopt-0-12-0` off
  `main` at `63889f7`; `pyproject.toml` reads 0.13.0 after rule 8.

## Readings (VER-HUP-013)

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| wheel SHA-256 before install | workstation | `639edbee…` equal to `RLS-SEH-021`'s distribution table |
| `upgrade .` plan | exact 0.12.0 | 46 files, 8 `update` (the eight of SPEC-HUP-013 rule 3), 38 unchanged, no `customized`/`conflict`/`remove` |
| `upgrade . --apply --evidence-output …` | exact 0.12.0 | transaction complete; `WO-HUP-013-evaluator-upgrade.json` retained: prior lock `e3f70394…`, prior `tool_version 0.11.0`, target identity equal to the new lock |
| `upgrade .` replay | exact 0.12.0 | 46 unchanged |
| `validate` | exact 0.12.0 | 1,218 artifacts, 0 errors, 65 warnings, 0 advisories |
| `doctor` | exact 0.12.0 | 0 FAIL |
| `qualify released-root .` | exact 0.12.0 | RR001 to RR004 PASS, 113/113 managed checks |
| `inspect` | exact 0.12.0 | exit 0 |
| `dashboard` twice | exact 0.12.0 | content digest `0eb2b37a3c744490` identical across both runs (only `generation-summary.json` excluded) |
| review preflight `--work-order WO-HUP-013` | exact 0.12.0 | PASS |
| `evaluator_facts derive` | candidate | 0.12.0 -> 0.13.0, no legacy fact |
| `run_tests.py --scale full` | candidate, Windows 11, CRLF checkout | 1,171 tests, 26 skipped, 1 failing name, the known baseline (`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`), equal to the same-commit control on the 0.11.0 root measured at the 2026-08-31 rehearsal |

## Identity-aware edits (rule 10)

- `AGENTS.md` owner region: the evaluator instruction reads
  `se-harness==0.12.0`; the pull-request trap states the live-body lane
  the 0.12.0 root installs.
- `tests/test_instruction_architecture.py`: `managed_count_by_root` gains
  `"0.12.0": 40`; the operational-fact pin moves from the stored-payload
  sentence to the live-body sentence, commented with this work order.
- `docs/notes/developing-se-harness.md`: the candidate/root identity
  paragraph and the "Advancing the root evaluator" paragraph state 0.12.0
  adopted by this work order and the 0.13.0 candidate.
- No other test name differs from the control; the rehearsal predicted
  exactly this set.

## Material non-effects

No product byte beyond the version identity; no template byte; no release,
tag, publication, Pages or maintenance-line change; the published 0.12.0
did not move. The latest markers wait for this observation window per
`REL-SEH-023`.

## Hosted lanes

All thirteen lanes of pull request #306 pass at its head `7d7e626`,
including the governor-transition lane assessing the real 0.11.0 to 0.12.0
root move with exactly one transaction document and the released
`RLS-SEH-021` supplying the wheel, and the managed lane running the
0.12.0 gate the transaction installed. The owner merged the pull request
on 2026-08-31 as `c8206cb`, the tip of `main`; the push-event check
runs on `main` for that commit all thirteen completed with success.
