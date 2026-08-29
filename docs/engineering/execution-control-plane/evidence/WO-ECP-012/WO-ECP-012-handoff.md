```toml
artifact = "WO-ECP-012"
checkpoint = "handoff"
formal_snapshot_sha256 = "f48f104e9d28ec7e176003778c877f09c101121e0fc5b8237ed251da9ea8835c"
rebound_at = "2026-08-29T07:57:06Z"
```

# WO-ECP-012 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

`harnessctl evidence` and `harnessctl check` work on Windows again. The
evaluator's own artifact path is rendered POSIX before the domain resolver's
text guard sees it (`ECP-HST-001`), the resolver renders any `PurePath` the
same way while a `str` keeps the guard (`ECP-HST-002`), and
`docs/notes/harnessctl-check.md` is the plain-English reference for the
command (`ECP-HST-005`). Issue #254.

## Evaluators

- Governing: released `se-harness 0.9.0` outside the checkout, `-I`, on
  Windows for `validate`, `doctor`, `preflight` and the packet approvals'
  readings, and the same wheel installed into a second isolated environment
  on a Linux runtime (WSL Ubuntu 24.04, CPython 3.12.3) for `evidence`,
  `transition --apply` and the handoff check, because the released 0.9.0
  cannot run those on Windows — the defect this work order repairs.
- Candidate: this checkout, branch `wo/ecp-012-windows-evidence-path` off
  `main` at `aa99773`; the suite runs candidate source.

## Change

- `se_harness/workflow_compliance.py::evidence_packet_path` passes
  `artifact.path.relative_to(root).as_posix()` to the resolver.
- `se_harness/artifact_layout.py::artifact_domain_from_relative_path`
  accepts `str | PurePath`; a `PurePath` is rendered with `.as_posix()`
  before the backslash guard, a `str` is guarded unchanged.
- Caller inventory after the change (`grep artifact_domain_from_relative_path(`
  over `se_harness/` and the template scripts): `workflow_compliance.py:374`
  passes the POSIX string; `artifact_layout.py:168` and the template
  registry's `common_artifact_domain` pass display strings; the template
  validator passes a display string. No caller passes a `PurePath`.
- `templates/repository/standard/scripts/artifact_layout_registry.py` and
  every other file under `templates/` and `scripts/` are byte-identical to
  `main` (`ECP-HST-003`; `git diff --stat aa99773 -- templates/ scripts/`
  is empty).

## Tests

- `tests/test_artifact_authoring.py::EvaluatorDerivedPathTests`: a
  `PureWindowsPath`, a `PurePosixPath` and a `str` of the same relative
  path resolve to the domain; a backslash `str`, an absolute
  `PureWindowsPath` and a path outside a domain resolve to `None`.
- `tests/test_workflow_compliance.py::EvaluatorDerivedPacketPathTests`:
  `evidence_packet_path` on a `PureWindowsPath` root and on a
  `PurePosixPath` root returns `DOMAIN/evidence/WO-ID/WO-ID-handoff.md`
  under that root; an artifact outside a domain still raises
  `WEX-ECP-010: WO-D-001 is not under a domain directory`.
- `tests/test_progressive_documentation.py::test_check_note_is_indexed_linked_and_names_only_contract_identifiers`:
  the note is indexed and linked, carries the eight sections
  `ECP-HST-005` lists, names every `WFL-*` rule and every `QG-*` gate of
  the template contracts, and names no `WFL`, `PROC`, `QG`, `QGP` or `QGS`
  identifier that the contracts do not define.

## Suite readings

- Linux (WSL Ubuntu 24.04, CPython 3.12.3, LF clone at `44d9a04`):
  `python3 scripts/run_tests.py --scale full` OK, 4 skips.
- Windows 11 workstation (CPython 3.12, CRLF checkout), `run_tests.py
  --scale full`, 1117 tests: before the change, at `5957139` under the same
  0.9.0 root, 64 failing names, 60 of them the `WEX-ECP-010: ... is not
  under a domain directory` error in `test_workflow_compliance`,
  `test_workflow_execution` and `test_delegated_workflow`; after, at
  `44d9a04`, 2 failing names and zero occurrences of that message:
  `test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`
  (present before, unrelated to paths) and
  `test_instruction_architecture.OwnerInstructionRegionTests.test_owner_region_stays_within_the_size_bound`
  (the CRLF-only owner-region reading, which comes and goes with the
  line endings of `AGENTS.md` in the worktree). Both are outside this work
  order.

## Readings under the 0.9.0 root

- `validate .`: PASS; maintenance E0/W475.
- `doctor .`: 0 FAIL.
- Review preflight for `WO-ECP-012`: PASS.

## Handoff check

`harnessctl check . --artifact WO-ECP-012 --checkpoint handoff --from-git aa99773`
from the Linux 0.9.0 environment over an LF clone (issue #256 makes a
CRLF-bound packet unusable hosted): see the retained `handoff.json` beside
this file.

## Complete changed-path set

Every path this work order changed since `main` at `aa99773`, packet
included, as Git derived it:

```
docs/engineering/execution-control-plane/README.md
docs/engineering/execution-control-plane/evidence/WO-ECP-012/WO-ECP-012-handoff.md
docs/engineering/execution-control-plane/evidence/WO-ECP-012/handoff.json
docs/engineering/execution-control-plane/requirements/REQ-ECP-019.md
docs/engineering/execution-control-plane/specifications/SPEC-ECP-008.md
docs/engineering/execution-control-plane/verification/VER-ECP-008.md
docs/engineering/execution-control-plane/work-orders/WO-ECP-012.md
docs/notes/README.md
docs/notes/harnessctl-check.md
docs/notes/harnessctl-reference.md
se_harness/artifact_layout.py
se_harness/workflow_compliance.py
tests/test_artifact_authoring.py
tests/test_progressive_documentation.py
tests/test_workflow_compliance.py
```

## Hosted lanes

Pull request #257 at `bafc534`: every lane passes (13 pass). The managed
Engineering Harness lane (https://github.com/mmzen/se_harness/actions/runs/33242110343/job/99073099746) ran the handoff check over the pull
request's diff inside the declared scope and the declared
`Harness-Restitution` `26cda39e…` equalled the recomputed `result_sha256`;
the Governor Transition Assessment (https://github.com/mmzen/se_harness/actions/runs/33242110353/job/99073099856) and every candidate-evidence,
migration, qualification-rehearsal and integration-package lane pass.

At `35ce28d`, the first push, the managed lane alone was red: the declared
digest `f69deeb0…` came from a check run before its own `handoff.json`
existed, so its change set lacked that file; `bafc534` retained the
fixed-point result (two consecutive runs reading `26cda39e…`) and the pull
request body was corrected before the push. The managed lane is expected
red once the work order leaves `in_progress` (issue #255).
