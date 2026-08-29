```toml
artifact = "WO-HUP-009"
checkpoint = "handoff"
formal_snapshot_sha256 = "a1bd35eb86942bd29015cf828eb3c333fda7b90f3b7a16d7fe00cc2c9677a054"
rebound_at = "2026-08-29T06:43:22Z"
```

# WO-HUP-009 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The standard root moved from exact public 0.8.0 to exact public 0.9.0 by the
simple upgrade: one command from a wheel-file install outside the checkout,
no packet, no `--work-order`. The transaction document is
`../WO-HUP-009-evaluator-upgrade.json`. This file is the keyed handoff
packet that 0.9.0's `harnessctl evidence` writes (`ECP-EVD-001`); it stands
where `VER-HUP-009` names `WO-HUP-009-verification.md`, the pre-0.9.0
file form, because the packet path is decided by the evaluator, not the
author.

## Evaluators

- Applying and governing after apply: released `se-harness 0.9.0` installed
  into an isolated environment outside the checkout from the wheel file
  downloaded from PyPI (`pip download --no-deps --only-binary=:all:
  se-harness==0.9.0`, then `pip install <wheel>`), invoked with `-I`. The
  wheel file's SHA-256 was measured before the install and again immediately
  before apply:
  `c4b5617585a3cb908a3b3c14b97e1039824ca731b8acce0251888d095927f364`, equal
  to the wheel `RLS-SEH-018` binds and PyPI serves. Identity written by the
  installer: version `0.9.0`, payload
  `e74ad2ae73d7298ebf2ae5125f84068c5f011d96d7c6bb75a105ff45895348f7`,
  archive `se_harness-0.9.0-py3-none-any.whl` with that digest.
- Governing before apply: released 0.8.0 (wheel-file install, archive
  `e08aab8a…`) outside the checkout — packet approvals, start preflight.
- The handoff check and this packet's header were produced by the same
  0.9.0 wheel installed into a second isolated environment on a Linux
  runtime (WSL Ubuntu 24.04, CPython 3.12.3) over the same worktree; see
  "Unassessed observation" for why the Windows environment could not.
- Candidate: this checkout, branch `governance/hup-009-adopt-0-9-0` off
  `main` at `7291602`.

## Plan and transaction

- `upgrade .` before apply: 61 files, 5 `update`, 56 unchanged; zero `add`,
  zero `customized`, zero `conflict`; every path inside the managed set the
  installer declares (`SPEC-HUP-009` rule 3). The five:
  `.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`,
  `ENGINEERING_HARNESS.md`, `docs/engineering/WORKFLOW.json`,
  `docs/engineering/WORKFLOW.md`.
- `upgrade . --apply --evidence-output docs/engineering/repository-harness-upgrade/evidence/WO-HUP-009-evaluator-upgrade.json`:
  `upgraded managed files to se-harness 0.9.0`, evidence retained.
- Replay `upgrade .`: 61 files, 61 unchanged.
- Lock after apply: schema 3, `tool_version 0.9.0`, evaluator
  `{version 0.9.0, payload_manifest se-harness-installed-payload-v1,
  payload_sha256 e74ad2ae…, archive_name se_harness-0.9.0-py3-none-any.whl,
  archive_sha256 c4b56175…}`. Prior lock in the transaction document:
  `174db6dc47a4dbd12d6d695d05bfd2ef44366f788de21a19f714f344043f9770`,
  prior `tool_version 0.8.0`. Postconditions: `lock_matches_target`,
  `no_op_replay`; no external action, no product release.
- After apply the root copies of the five managed files equal the candidate
  templates under `templates/repository/standard/` modulo the installer's
  `{{PROJECT_NAME}}` and `{{HARNESS_VERSION}}` substitutions and line
  endings (the installer writes LF; the checkout is CRLF).

## Readings under the 0.9.0 root, isolated mode

- `validate .`: PASS; structure E0/W0, governance E0/W0, policy E0/W0,
  maintenance E0/W475.
- `doctor .`: 0 FAIL.
- `qualify released-root`: RR001 runtime matches the target root lock;
  RR002 143/143 managed checks; RR003 artifacts=1096, errors=0,
  warnings=475; RR004 target state unchanged.
- `inspect .`: derived observation produced without error; 1096 artifacts,
  4134 relations.
- `dashboard` twice: content directories identical; only
  `generation-summary.json` differs.
- Review preflight for `WO-HUP-009`: PASS, no diagnostics.
- `evaluator_facts derive` (candidate source): `version=0.9.0`,
  `wheel=se_harness-0.9.0-py3-none-any.whl`, `wheel_sha256=c4b56175…`,
  `payload_sha256=e74ad2ae…`, `acceptance_contract_sha256=` (empty),
  `candidate_version=0.10.0`. Measured on the rehearsal with the candidate
  still at 0.9.0: `PRE008: the candidate version 0.9.0 equals the declared
  root version`, which is why the candidate moves in this change.

## Owner content and candidate version

- `AGENTS.md` owner region: the install instruction reads
  `se-harness==0.9.0`.
- `docs/notes/developing-se-harness.md`: the candidate/root paragraph now
  states candidate 0.10.0 and root 0.9.0, and the root-evaluator paragraph
  names `WO-HUP-009`, `RLS-SEH-018` and the wheel-file install.
- Candidate moved to `0.10.0`: `pyproject.toml`, `se_harness/__init__.py`,
  the README install example. No scenario, no legacy map entry.

## Test assumptions replaced

The rehearsal on a throwaway clone of `main` at `7291602` compared the full
suite on the moved root against a control on the unmoved root at the same
commit (1117 tests each, CPython 3.12, this workstation). Exactly four
names differed, none of them present on the control:

| Test | Assumption carried | Resolution |
| --- | --- | --- |
| `test_ci_pipeline.PredecessorDerivationTests.test_facts_come_from_the_lock_and_the_legacy_table`, `…test_null_archive_pair_is_supplied_by_exactly_one_released_record` | candidate version differs from the root's | candidate moved to 0.10.0; no test change |
| `test_ci_pipeline.PredecessorDerivationTests.test_a_version_bump_needs_no_scenario` | the fixture bumped the candidate to a literal `0.9.0` | bumps past the lock's `tool_version` (`major.minor+1.0`) instead |
| `test_instruction_architecture.OwnerInstructionRegionTests.test_owner_region_directs_the_evaluator_outside_the_checkout` | owner region names `se-harness==<lock version>` | no test change; the owner content moved |

One further edit in `tests/test_ci_pipeline.py`: `0.9.0` added to the
forbidden version-literal set that
`test_no_predecessor_literal_remains_in_the_repository_owned_workflows`
asserts, as `WO-HUP-008` added `0.8.0`.

## Suite on the moved root

`python scripts/run_tests.py --scale full` on this branch after every edit:
1117 tests, 34 failures, 30 errors, 27 skips. The control on the unmoved
0.8.0 root at `7291602` reads 35 failures, 30 errors, 27 skips. Set
difference of failing names: none fails on the moved root that does not
fail on the control; the one name that fails on the control only,
`test_instruction_architecture…test_owner_region_stays_within_the_size_bound`,
is the known CRLF-only workstation reading of `AGENTS.md` (`sed -i` left
the file LF in the worktree; Git normalizes it at commit). The 64 shared
failures are workstation-only: 60 of them are the `WEX-ECP-010` refusal
below, plus the identifier-allocation test, and they pass hosted.

## Handoff check

`harnessctl check . --artifact WO-HUP-009 --checkpoint handoff --from-git 7291602`
with released 0.9.0 outside the checkout on the Linux runtime: Completed;
change set of 21 paths, `complete: true`; every predicate of
`QG-G4-IMPLEMENTATION-EVIDENCE` passes (STATUS, GRAPH, INTEGRITY, SCOPE,
COMPLETE, PATHS, PREFLIGHT, EVIDENCE). The packet header's formal snapshot
was measured equal on the CRLF worktree and on an LF export of the same
commit, so the hosted lane binds the same snapshot.

## Complete changed-path set

Every path this work order changed since `main` at `7291602`, packet
included, as Git derived it:

```
.engineering-harness.lock
.engineering-harness.toml
.github/workflows/engineering-harness.yml
AGENTS.md
docs/engineering/repository-harness-upgrade/architecture/ARCH-HUP-007.md
docs/engineering/repository-harness-upgrade/evidence/WO-HUP-009-evaluator-upgrade.json
docs/engineering/repository-harness-upgrade/evidence/WO-HUP-009/WO-HUP-009-handoff.md
docs/engineering/repository-harness-upgrade/README.md
docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-018.md
docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-019.md
docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-009.md
docs/engineering/repository-harness-upgrade/verification/VER-HUP-009.md
docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-009.md
docs/engineering/WORKFLOW.json
docs/engineering/WORKFLOW.md
docs/notes/developing-se-harness.md
ENGINEERING_HARNESS.md
pyproject.toml
README.md
se_harness/__init__.py
tests/test_ci_pipeline.py
```

## Unassessed observation, outside this work order

Released 0.9.0 refuses `harnessctl evidence` and every `harnessctl check`
that builds a checkpoint context on Windows with `WEX-ECP-010: <WO> is not
under a domain directory`, for every work order:
`artifact_layout.artifact_domain_from_relative_path` returns `None` for
any value whose string form contains a backslash, and
`workflow_compliance.evidence_packet_path` passes it
`artifact.path.relative_to(root)`, a `WindowsPath`. Measured on this
workstation with the isolated 0.9.0 evaluator: `check --checkpoint start`
and `--checkpoint handoff` blocked by `WEX210: WEX-ECP-010`; the same call
with a `PurePosixPath` or string returns the domain. The same refusal is
the cause of 60 of the workstation-only suite failures. It is product code,
outside `WO-HUP-009`'s scope, and is recorded here only so that it is
not mistaken for a fact about this root move; it has no artifact ID yet.

## Hosted lanes

Not yet run: the branch has not been pushed. This section is to be
appended with the pull request's lane readings before completion.
