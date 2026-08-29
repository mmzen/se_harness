```toml
artifact = "WO-HUP-010"
checkpoint = "handoff"
formal_snapshot_sha256 = "f21c7493b0257c6bd85279a37c882c0c54ef70e79dc8203ec7d558b3b5ed84c8"
rebound_at = "2026-08-29T10:44:33Z"
```

# WO-HUP-010 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The standard root moved from exact public 0.9.0 to exact public 0.10.0 by
the simple upgrade: one command from a wheel-file install outside the
checkout, no packet, no `--work-order`. The transaction document is
`../WO-HUP-010-evaluator-upgrade.json`. This is the first root move whose
evidence packet and handoff check were produced by the released evaluator
on this Windows checkout itself: the three defects the 0.9.0 adoption
exposed (issues #254, #255, #256) are repaired in the root this transaction
installs.

## Evaluators

- Applying and governing after apply: released `se-harness 0.10.0`
  installed into an isolated environment outside the checkout from the
  wheel file downloaded from PyPI (`pip download --no-deps
  --only-binary=:all: se-harness==0.10.0`, then `pip install <wheel>`),
  invoked with `-I`, on Windows. The wheel file's SHA-256 was measured
  before the install and again immediately before apply:
  `e2f8077264ee2c8ad39d6ac33f726030627f0f70de5579e80bcc159d971f93c3`,
  equal to the wheel `RLS-SEH-019` binds and PyPI serves. Identity written
  by the installer: version `0.10.0`, payload
  `723c98ecf21a853441ead771956af7aed6564fcffb97389c0468b9376214235d`,
  archive `se_harness-0.10.0-py3-none-any.whl` with that digest.
- Governing before apply: released 0.9.0 (wheel-file install, archive
  `c4b56175…`) outside the checkout — packet approvals, start preflight.
- Candidate: this checkout, branch `governance/hup-010-adopt-0-10-0` off
  `main` at `47f67de`.

## Plan and transaction

- `upgrade .` before apply: 61 files, 6 `update`, 55 unchanged; zero `add`,
  zero `customized`, zero `conflict`; every path inside the managed set the
  installer declares (`SPEC-HUP-010` rule 3). The six:
  `.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`,
  `ENGINEERING_HARNESS.md`, `docs/engineering/QUALITY_GATES.json`,
  `docs/engineering/QUALITY_GATES.md`, `docs/engineering/WORKFLOW.md` —
  the `scope` checkpoint's contract and the state-independent managed
  workflow (`WO-ECP-013`).
- `upgrade . --apply --evidence-output docs/engineering/repository-harness-upgrade/evidence/WO-HUP-010-evaluator-upgrade.json`:
  `upgraded managed files to se-harness 0.10.0`, evidence retained.
- Replay `upgrade .`: 61 files, 61 unchanged.
- Lock after apply: schema 3, `tool_version 0.10.0`, evaluator
  `{version 0.10.0, payload_manifest se-harness-installed-payload-v1,
  payload_sha256 723c98ec…, archive_name se_harness-0.10.0-py3-none-any.whl,
  archive_sha256 e2f80772…}`. Prior lock in the transaction document:
  `fb61f1fee6a6d79692495954cc2952b547313c66a6d6a4a84556bdae60482356`,
  prior `tool_version 0.9.0`. Postconditions: `lock_matches_target`,
  `no_op_replay`; no external action, no product release.
- After apply the root copies of the six managed files equal the candidate
  templates under `templates/repository/standard/` modulo the installer's
  substitutions and line endings.

## Readings under the 0.10.0 root, isolated mode

- `validate .`: PASS; structure E0/W0, governance E0/W0, policy E0/W0,
  maintenance E0/W477.
- `doctor .`: 0 FAIL.
- `qualify released-root`: RR001 runtime matches the target root lock;
  RR002 143/143 managed checks; RR003 artifacts=1123, errors=0,
  warnings=477; RR004 target state unchanged.
- `inspect .`: derived observation produced without error; 1123 artifacts,
  4209 relations.
- `dashboard` twice: content directories identical; only
  `generation-summary.json` differs.
- Review preflight for `WO-HUP-010`: PASS, no diagnostics.
- `evaluator_facts derive` (candidate source): `version=0.10.0`,
  `wheel=se_harness-0.10.0-py3-none-any.whl`, `wheel_sha256=e2f80772…`,
  `payload_sha256=723c98ec…`, `acceptance_contract_sha256=` (empty),
  `candidate_version=0.11.0`. Measured on the rehearsal with the candidate
  still at 0.10.0: `PRE008: the candidate version 0.10.0 equals the
  declared root version`, which is why the candidate moves in this change.

## Owner content and candidate version

- `AGENTS.md` owner region: the install instruction reads
  `se-harness==0.10.0`.
- `docs/notes/developing-se-harness.md`: the candidate/root paragraph now
  states candidate 0.11.0 and root 0.10.0, and the root-evaluator paragraph
  names `WO-HUP-010`, `RLS-SEH-019` and the wheel-file install.
- Candidate moved to `0.11.0`: `pyproject.toml`, `se_harness/__init__.py`,
  the README install example. No scenario, no legacy map entry.

## Test assumptions replaced

The rehearsal on a throwaway clone of `main` at `47f67de` compared the full
suite on the moved root against a control on the unmoved root at the same
commit (1117 tests each, CPython 3.12, this workstation). Exactly three
names differed, none of them present on the control:

| Test | Assumption carried | Resolution |
| --- | --- | --- |
| `test_ci_pipeline.PredecessorDerivationTests.test_facts_come_from_the_lock_and_the_legacy_table`, `…test_null_archive_pair_is_supplied_by_exactly_one_released_record` | candidate version differs from the root's | candidate moved to 0.11.0; no test change |
| `test_instruction_architecture.OwnerInstructionRegionTests.test_owner_region_directs_the_evaluator_outside_the_checkout` | owner region names `se-harness==<lock version>` | no test change; the owner content moved |

One edit in `tests/test_ci_pipeline.py`: `0.10.0` added to the forbidden
version-literal set that
`test_no_predecessor_literal_remains_in_the_repository_owned_workflows`
asserts, as `WO-HUP-009` added `0.9.0`. The version-bump fixture that
`WO-HUP-009` made identity-aware did not move.

## Suite on the moved root

`python scripts/run_tests.py --scale full` on this branch after every edit,
Windows 11 workstation (CPython 3.12, CRLF checkout): 1117 tests, 1 error,
27 skips —
`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
present on the control and unrelated to the root. The control's other
failure, the CRLF-only owner-region size bound, clears on this branch
because `AGENTS.md` was rewritten LF by the owner-content edit. No name
fails on the moved root that does not fail on the control. The Linux
reading at the transaction commit follows in the ledger section.

## Handoff check

`harnessctl check . --artifact WO-HUP-010 --checkpoint handoff --from-git 47f67de`
with released 0.10.0 outside the checkout, on this Windows checkout, run to
its fixed point on the committed packet: see the retained `handoff.json`
beside this file. The packet header was written by the same evaluator on
the same checkout; under 0.10.0 the formal snapshot is line-ending
canonical, so no Linux clone was needed for any reading of this work order.

## Observation outside this work order

A packet file that Git checks out with CRLF (the `.gitattributes`
`evaluator-evidence` rule forces LF for `*.json` only) reads to 0.10.0's
`evidence` as carrying no header at byte offset 0
(`WEX-ECP-010`), measured on the rehearsal clone against the checked-out
`WO-RLS-016` packet. A one-line attribute for `docs/engineering/**/evidence/**/*.md`
would close it; it is not part of this adoption.
