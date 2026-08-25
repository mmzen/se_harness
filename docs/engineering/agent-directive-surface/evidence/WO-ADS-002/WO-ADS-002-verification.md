# WO-ADS-002 implementation evidence

artifact: WO-ADS-002
checkpoint: handoff
formal_snapshot_sha256: 222ee6436eefb8d7992603196fc40ae71dd83a99b1050594dbcb3e1a20218cc7

Retained by the implementation actor on 2026-08-25. This file is evidence. It
does not complete, verify, or release the work order.

## Evaluators

- Governing: released `se-harness 0.6.0` installed outside the checkout from
  the exact wheel `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
  (`C:\Users\mathi\se-harness-eval`, invoked with `-I`).
- Candidate: this checkout, `python -m se_harness` from the repository root.

## Commands and results

| Command | Evaluator | Result |
| --- | --- | --- |
| `harnessctl preflight . --work-order WO-ADS-002 --phase review` | released 0.6.0 | `PASS` |
| `harnessctl validate .` | released 0.6.0 | PASS, 863 artifacts, 0 errors, 50 warnings (unchanged count; `REQ-IAR-020` superseded adds no error) |
| `harnessctl doctor .` | released 0.6.0 | 0 FAIL |
| `python scripts/validate_engineering_artifacts.py --root .` | candidate | PASS, 863 artifacts, 0 errors, 50 warnings |
| `python scripts/validate_release_distributions.py --root .` | candidate | PASS (1 distribution-bearing record) |
| `python -m se_harness --help` | candidate | exit 0 |
| `git diff --check` | git | clean |
| `harnessctl check . --artifact WO-ADS-002 --checkpoint handoff --changed-path … --changes-complete --json` (complete set below) | released 0.6.0 and candidate | before this file existed: blocked only by `QGP-G4I-EVIDENCE`; both report formal snapshot `222ee6436eefb8d7992603196fc40ae71dd83a99b1050594dbcb3e1a20218cc7` |
| `python -m unittest discover -s tests -p "test_*.py"` | candidate, Windows 11, CPython 3.14 | `Ran 991 tests in 326.768s` — `OK (skipped=23)`; the 23 skips are the Windows-only guards. Run on the tree before this evidence file and its inventory line were added; `tests.test_context_routing_retirement` was re-run green afterwards |
| Linux lane | `.github/workflows/candidate-evidence.yml` | not run locally; the pull-request run is the Linux figure |

## Measurements

- Operating card: 1006 bytes (bound 1024); sections `## Stop when`, `## Traps` only.
- Owner region of `AGENTS.md`: 5727 bytes (bound 6000); names
  `docs/notes/developing-se-harness.md#release-sequences`; does not name the
  retired path.
- Reading manifest for `WO-ADS-002`, both phases (candidate preflight):

```
- ENGINEERING_HARNESS.md
- docs/engineering/OPERATING_CARD.md
- AGENTS.md
- docs/engineering/agent-directive-surface/intent/INT-ADS-001.md
- docs/engineering/agent-directive-surface/capabilities/CAP-ADS-001.md
- docs/engineering/agent-directive-surface/requirements/REQ-ADS-007.md
- docs/engineering/agent-directive-surface/specifications/SPEC-ADS-002.md
- docs/engineering/agent-directive-surface/verification/VER-ADS-002.md
- docs/engineering/agent-directive-surface/work-orders/WO-ADS-002.md
```

No routed policy is listed. `POLICY_PATHS` is unchanged and still drives the
installation checks.

## Complete changed-path set

```
AGENTS.md
docs/engineering/README.md
docs/engineering/REPOSITORY_CONTEXT.md
docs/engineering/agent-directive-surface/evidence/WO-ADS-002/WO-ADS-002-verification.md
docs/engineering/instruction-architecture/requirements/REQ-IAR-020.md
docs/notes/developing-se-harness.md
se_harness/preflight.py
se_harness/workflow_contract.py
templates/repository/standard/ENGINEERING_HARNESS.md.tpl
templates/repository/standard/docs/engineering/OPERATING_CARD.md
tests/test_context_routing_retirement.py
tests/test_instruction_architecture.py
tests/test_repository_context_retirement.py
tests/test_workflow_execution.py
```

`docs/engineering/REPOSITORY_CONTEXT.md` is a staged deletion (`git rm`).
Every path is admitted by `[execution_scope].paths` of `WO-ADS-002`. Scoped
paths left untouched: `docs/notes/harnessctl-reference.md`,
`tests/fixtures/repository_context_retirement/` (the baseline fixture records
the released 0.5.0 payload and needed no change: the manifest-prefix test
now compares against `READING_PATHS`).

## Rule coverage

| Rule | Implemented by | Test evidence |
| --- | --- | --- |
| `ADS-RDS-001` | `READING_PATHS` in `preflight.py`; manifest prefix | `test_preflight_returns_deterministic_reading_manifest_without_writes`, `test_reading_manifest_keeps_the_baseline_order_without_the_retired_path`, `AgentDirectiveSurfaceTests.test_operating_card_template_equals_its_contract_rendering_and_stays_bounded` |
| `ADS-RDS-002` | `render_operating_card`: header, stop conditions, traps; `OPERATING_CARD_LIMIT = 1024`; regenerated template | `…test_operating_card_template_equals_its_contract_rendering_and_stays_bounded` (sections, mutation), `AgentDirectiveSurfaceRouterTests.test_router_states_the_scope_of_its_obligations_after_the_invariants` (installed size) |
| `ADS-RDS-003` | router template sentence | `…test_router_states_the_scope_of_its_obligations_after_the_invariants` |
| `ADS-RDS-004` | `AGENTS.md` owner region | `OwnerInstructionRegionTests` (required facts now name the note anchor; size bound) |
| `ADS-RDS-005` | `## Release sequences` in `docs/notes/developing-se-harness.md`; file and index line removed | `test_only_recorded_files_name_the_retired_path` (inventory shrinks by three files) |
| `ADS-RDS-006` | `REQ-IAR-020` status `superseded`, `updated` date, supersession section; body otherwise unchanged | released and candidate validators: 0 errors |
| `ADS-RDS-007` | four test modules updated | the modules themselves |

## Material deviations from SPEC-ADS-002

1. `ADS-RDS-002` describes a "two-line header naming the contracts and
   `harnessctl` as the only legality oracle". The header is two lines but
   drops the sentence "Read this, the phase manifest, and the selected chain"
   to fit the 1,024-byte bound (1077 bytes with it). The router carries that
   instruction.
2. `ADS-RDS-006` says the body of `REQ-IAR-020` is unchanged. A `## Supersession`
   section is inserted before the original body, following the exact form of
   `REQ-DST-008`; the original sections are byte-identical.
3. `ADS-RDS-007` lists the retirement fixture baseline among the updates; it
   needed none, because the assertion that pinned the manifest prefix lives in
   the test module, not in the fixture.

## Not done

Linux figure pending the pull-request lane. `harnessctl-reference.md` was
not edited: its only manifest mention is a one-line command description that
remains true.
