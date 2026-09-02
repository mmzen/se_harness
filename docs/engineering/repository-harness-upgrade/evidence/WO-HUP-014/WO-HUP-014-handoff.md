```toml
artifact = "WO-HUP-014"
checkpoint = "handoff"
formal_snapshot_sha256 = "e07cf7f553d53fb621e6b336ab86b0ca15ad3b92b2caf74463c3482e6a6f2165"
rebound_at = "2026-09-02T08:34:02Z"
```

# WO-HUP-014 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The standard root is exact public 0.13.0: lock schema 3, `tool_version
0.13.0`, archive `1bbf3b74…` equal to the wheel `RLS-SEH-022` binds,
payload `9b4cdb5f…`, written by the simple upgrade from the isolated
wheel-file environment in one atomic transaction (46 managed files, 5
updated, replay 46 unchanged; nothing left the managed set). The candidate
moved to 0.14.0. The 0.13.0 gate reads its own numbers over this graph:
0 errors, 67 warnings, 0 advisories. This repository's own generated
Explorer is now the designed self-contained page, 431,388 bytes with no
remote origin; after the merge the Pages deployment regenerates the public
demonstration from it, the observation `REL-SEH-024` names.

## Evaluators

- Predecessor (approval, start): released `se-harness 0.12.0` outside the
  checkout (`C:/Users/hok/se-harness-eval-0120`), wheel-installed.
- Governor from the transaction onward: released `se-harness 0.13.0`
  outside the checkout (`C:/Users/hok/se-harness-eval-0130`), installed
  from the wheel file verified against `RLS-SEH-022` before install; every
  later reading, this packet and the handoff check included.
- Candidate: this checkout, branch `governance/hup-014-adopt-0-13-0` off
  `main` at `09aa69f`; `pyproject.toml` reads 0.14.0 after rule 8.

## Readings (VER-HUP-014)

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| wheel SHA-256 before install | workstation | `1bbf3b74…` equal to `RLS-SEH-022`'s distribution table |
| `upgrade .` plan | exact 0.13.0 | 46 files, 5 `update` (the five of SPEC-HUP-014 rule 3), 41 unchanged, no `customized`/`conflict`/`remove` |
| `upgrade . --apply --evidence-output …` | exact 0.13.0 | transaction complete; `WO-HUP-014-evaluator-upgrade.json` retained: prior lock `4d8f9d37…`, prior `tool_version 0.12.0`, target identity equal to the new lock |
| `upgrade .` replay | exact 0.13.0 | 46 unchanged |
| `validate --advisories` | exact 0.13.0 | 1,241 artifacts, 0 errors, 67 warnings, 0 advisories |
| `doctor` | exact 0.13.0 | 113 PASS, 0 FAIL |
| `qualify released-root .` | exact 0.13.0 | RR001 to RR004 PASS, 113/113 managed checks |
| `inspect` | exact 0.13.0 | exit 0 |
| `dashboard` twice | exact 0.13.0 | content digest `6300559b0b301f5d` identical across both runs (only `generation-summary.json` excluded); `index.html` 431,388 bytes, zero remote origins |
| root copies vs candidate templates | workstation | `scripts/generate_harness_dashboard.py` and `scripts/harness_explorer/index.template.html` equal to `templates/repository/standard/` modulo line endings |
| review preflight `--work-order WO-HUP-014` | exact 0.13.0 | PASS |
| `evaluator_facts derive` | candidate | 0.13.0 -> 0.14.0, payload `9b4cdb5f…`, wheel `1bbf3b74…`; `PRE008` with the candidate still at 0.13.0, as rehearsed |
| `run_tests.py --scale full` | candidate, Windows 11 (CPython 3.13), `PYTHONUTF8=1` | section below |

### The Windows suite

`PYTHONUTF8=1 python scripts/run_tests.py --scale full` on the moved root
at this commit, Windows 11 (CPython 3.13), LF checkout: 1,176 tests, 26
skipped, 1 error, the known baseline name present on `main` and outside
this work order
(`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
a Windows `PermissionError` on a temporary Git object during teardown),
equal to the same-commit control on the 0.12.0 root measured at
`aa14628` during `WO-RLS-019` and to the rehearsal after the same edits.
No other name differs.

## Identity-aware edits (rules 8, 9, 10)

- `pyproject.toml`, `se_harness/__init__.py`, README install line: 0.14.0.
- `AGENTS.md` owner region: the evaluator instruction reads
  `se-harness==0.13.0`.
- `docs/notes/developing-se-harness.md`: the candidate/root identity
  paragraph and the "Advancing the root evaluator" paragraph state 0.13.0
  adopted by this work order and the 0.14.0 candidate.
- `tests/test_instruction_architecture.py`: `managed_count_by_root` gains
  `"0.13.0": 40`.
- `tests/test_dashboard_webui.py`: eight tests that asserted the 0.12.0
  page's markers against the root copy of the Explorer template
  (`overview`, `lineage board`, `search and revision`, `semantic routes`,
  `graph analysis colours`, `progressive browser contract`, `rich detail`,
  `accepted runtime URL`) gain a guard: under a root of 0.13.0 or later
  they assert the root copy equals the canonical designed template modulo
  line endings; the previous markers apply only to an older root. Two
  helpers carry the rule with this work order's identifier.
- Rehearsal on a throwaway clone of `main` at `09aa69f` on 2026-09-02
  predicted exactly this set; a `source_url` failure seen only there came
  from the clone's local-path origin and does not occur in this checkout.
  The runner's report needs `PYTHONUTF8=1` on a Windows console because a
  failing assertion may print the designed page's non-cp1252 characters.

## Material non-effects

No product byte beyond the version identity; no template byte; no release,
tag, publication, Pages or maintenance-line change; the published 0.13.0
did not move. `RLS-SEH-022` and `VREC-SEH-022` are unchanged.

## Hosted lanes

All thirteen lanes of pull request #314 pass at its head `a2f4677`,
including the governor-transition lane assessing the real 0.12.0 to 0.13.0
root move with exactly one transaction document and the released
`RLS-SEH-022` supplying the wheel, the managed lane running the 0.13.0
gate the transaction installed over the live pull-request body, the
candidate-evidence lanes with the 0.13.0 to 0.14.0 upgrade rehearsal on
both platforms, and the Publication Rehearsal in both modes. Runs: Governor Transition Assessment (pull_request, 33609997670, success); Engineering Harness (pull_request, 33609997735, success); Publication Rehearsal (pull_request, 33609997885, success); SE Harness Candidate Evidence (pull_request, 33609997668, success).
