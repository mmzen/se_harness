```toml
artifact = "WO-HUP-011"
checkpoint = "handoff"
formal_snapshot_sha256 = "346a84b9c7da58fa320258a81ec02ae1503db9a633a77616f3d53821ff8b036b"
rebound_at = "2026-08-29T16:49:09Z"
```

# WO-HUP-011 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

This repository's standard root is exact public 0.11.0, installed outside
the checkout from the wheel file whose digest `RLS-SEH-020` binds, by one
`upgrade --apply` transaction with a no-op replay (`REQ-HUP-022`); the
fifteen files the 0.10.0 lock managed and 0.11.0 no longer ships are
removed by this work order (issue #271); exact 0.11.0 validates the
complete graph, passes doctor and released-root qualification, the suite
is at its baseline against a same-bytes control, and the candidate is
0.12.0 (`REQ-HUP-023`). Every reading below is produced natively on this
Windows checkout.

## Identity and transaction (`SPEC-HUP-011` rules 1 to 6)

| Reading | Value |
| --- | --- |
| environment | `C:\Users\mathi\se-harness-eval-0110`, `python -I -m se_harness`, `se-harness==0.11.0` installed from `se_harness-0.11.0-py3-none-any.whl` fetched from PyPI |
| wheel SHA-256 before install | `ba26ab7be14321cdc26b69d59e2b894d544c3e7b529227de1f24ad9cd8f935c0` = `RLS-SEH-020` `wheel_sha256` |
| prior lock | `aeb73cc732474289...`, `tool_version 0.10.0`, 61 files |
| plan (`upgrade .`) | 46 files, 9 `update`, 37 unchanged, 0 `add`, 0 `customized`, 0 `conflict` |
| the nine | `.agents/skills/harness-orient/SKILL.md`, `.agents/skills/harness-orient/scripts/orient.py`, `.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`, `ENGINEERING_HARNESS.md`, `docs/engineering/WORKFLOW.json`, `docs/engineering/WORKFLOW.md`, `docs/engineering/templates/WORK_ORDER.template.md`, `scripts/validate_engineering_artifacts.py` |
| apply | `upgrade . --apply --evidence-output docs/engineering/repository-harness-upgrade/evidence/WO-HUP-011-evaluator-upgrade.json`: "upgraded managed files to se-harness 0.11.0" |
| new lock | `tool_version 0.11.0`, `evaluator.version 0.11.0`, `archive_sha256 ba26ab7b...` (equal to the wheel), `payload_sha256 71b4b5b694111a42785328f4b742f40e5654d7d4c67d88b9939a6c80213dd016`, 46 files (40 managed, 6 fragments) |
| replay (`upgrade .`) | 46 files, 46 unchanged |
| removal (rule 6) | `git rm` of `.agents/skills/{harness-draft-change,harness-execute-work-order,harness-prepare-assurance}/**` (12 files) and `.claude/skills/{same}/SKILL.md` (3); `.agents/skills` now holds `harness-operator-brief`, `harness-orient`; `.claude/skills` holds `harness-orient` |
| root copies vs candidate templates (rule 7) | the six template-backed updated files are byte-equal modulo line endings (`orient.py`, `SKILL.md`, the validator, `WORKFLOW.json`, `WORKFLOW.md`, `WORK_ORDER.template.md`); the toml, the managed workflow and `ENGINEERING_HARNESS.md` carry the installer's substitutions |

## Readings under the 0.11.0 root (rules 7 and 8)

| Check | Reading |
| --- | --- |
| `validate .` | 1,152 artifacts, 0 errors, 484 maintenance warnings |
| `doctor .` | 0 FAIL |
| `qualify released-root .` | PASS: RR001 runtime matches the target root lock; RR002 113/113 managed checks |
| `inspect . --json` | completes |
| `dashboard .` twice | content identical (only `generation-summary.json` differs) |
| `preflight --work-order WO-HUP-011 --phase review` | PASS, no diagnostic |
| `repository_tools.evaluator_facts derive` | 0.11.0 -> 0.12.0, `acceptance_contract_sha256` null |
| candidate identity | `pyproject.toml`, `se_harness/__init__.py` and the README install line read 0.12.0 |

## Owner content (rule 9)

- `AGENTS.md` owner region: the managed-skills line names `SKILL.md`,
  `skill-contract.json`, `orient.py`, `check_brief.py`; the install
  instruction reads `se-harness==0.11.0`. The region is shorter than
  before, so the 6000-byte bound now holds on the CRLF checkout too.
- `docs/notes/developing-se-harness.md`: candidate 0.12.0, root 0.11.0
  adopted by `WO-HUP-011` from the wheel bound in `RLS-SEH-020`;
  `WO-HUP-010`, `WO-HUP-009`, `WO-HUP-008` listed as the earlier
  same-way adoptions.

## Tests (rule 10)

Full-scale suite on the moved root (Windows 11, CPython 3.14, CRLF
checkout, transaction `adaab5e`): 1,128 tests, 26 skipped. Against the
same-bytes control (the suite at `c5dad10`, whose product bytes this root
carries; 1,128 tests, two baseline names), exactly one name moved, in the
direction of the move:
`test_instruction_architecture...test_owner_region_identifies_every_managed_path_from_the_lock`
pinned 55 managed lock entries (the 0.10.0 root); it now reads the count
from the lock's `tool_version` through a declared map (0.10.0: 55, 0.11.0:
40) and fails loudly for an undeclared root. The four owner-content names
the rehearsal moved are resolved by rules 8 and 9 without a test edit. The
baseline `test_owner_region_stays_within_the_size_bound` passes on this
checkout now (the region shrank);
`test_artifact_authoring...test_allocation_refuses_outside_a_checkout...`
remains the one Windows workstation error, present on `main`.

## Deviations, recorded for the completion decision

1. **The installer removed nothing** (`SPEC-ECP-007` `ECP-SKL-004` expected
   `doctor` to report the retired skill files as `remove`; the `WO-ECP-006`
   packet asserted it by construction). Measured: the plan names only the
   new 46-file set, the fifteen files stay on disk unmanaged, `doctor` is
   silent. Removed here under rule 6; issue #271 (P1) records the product
   defect for a later work order.
2. This work order's scope names no `verification-records/` directory
   (rule 11): the record head of its pull request is the first under the
   0.11.0 gate and is the hosted demonstration of `VER-ECP-012`; read in
   the pull request and the record.

## Complete changed-path set

Every path this work order changed since `main` at `896f8fa`, packet
included, as Git derived it; the handoff check completed at its fixed point
with every predicate of `QG-G4-IMPLEMENTATION-EVIDENCE` passing, run by
the released 0.11.0 evaluator - the root this transaction installed - on
this Windows checkout: see `handoff.json` beside this file.
