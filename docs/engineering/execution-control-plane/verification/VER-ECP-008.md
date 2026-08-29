+++
id = "VER-ECP-008"
type = "verification"
title = "Independent evidence for host-independent evaluator paths and the check reference"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
verifies = ["REQ-ECP-019"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T07:45:09Z"
decided_by = "assurance-owner"
reason = "Approved on 2026-08-29 by the accountable owner, 'i approve the artifact packet', for the repair of issue #254: render the evaluator's own artifact path as POSIX before the domain resolver's text guard, prove it with PureWindowsPath tests on the Linux lane, and add the plain-English reference for harnessctl check. Measured before this transition over branch state 88d1a1f carrying unmoved main aa99773: validate PASS at 0 errors under the governing 0.9.0 root; start preflight reads only the draft signature. Approval of a definition authorizes no work; the work order is approved separately."
+++

# Verification Contract: Independent evidence for host-independent evaluator paths and the check reference

## Independence

Expected behaviour derives from `REQ-ECP-019` and the `ECP-HST-` rules of
`SPEC-ECP-008`. The regression tests build their paths from
`PureWindowsPath` literals written from the requirement, not from the host,
so the Linux lane exercises the Windows form; the Windows reading is a
before-and-after count of the existing suite on a Windows host, retained in
the evidence with the host named.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-019` evaluator-derived paths resolve on every host | test: resolver with `PureWindowsPath` and with a backslash `str`; `evidence_packet_path` with a `PureWindowsPath` root and artifact | `tests/test_artifact_authoring.py`, `tests/test_workflow_compliance.py` | the `PureWindowsPath` resolves to its domain and the packet path ends in `evidence/WO-ID/WO-ID-handoff.md`; the backslash `str` still resolves to `None` |
| `REQ-ECP-019` on a Windows host | test: the full suite on a Windows workstation before and after the change | `run_tests.py --scale full`, host named | the `WEX-ECP-010: ... is not under a domain directory` errors are absent after; the remaining failure set is named and unrelated |
| `SPEC-ECP-008` ECP-HST-005 the check reference | inspection and test: the note exists, is indexed, is linked, and its command forms exist in the CLI | `docs/notes/harnessctl-check.md`; `tests/test_progressive_documentation.py` | every section the rule lists is present; every rule of `WORKFLOW.json` and every gate of `QUALITY_GATES.json` named in its tables exists in the contract |

## Acceptance scenarios

### Scenario 1: the resolver takes a Windows path

Call `artifact_domain_from_relative_path(PureWindowsPath("docs/engineering/d/work-orders/WO-D-001.md"))`.
Assert `"d"`. Call it with the `str` `"docs\\engineering\\d\\work-orders\\WO-D-001.md"`.
Assert `None`.

### Scenario 2: the packet path on a Windows root

With `root = PureWindowsPath("C:/repo")` and an artifact whose `path` is
`root / "docs/engineering/d/work-orders/WO-D-001.md"`, call
`evidence_packet_path(root, artifact, "handoff")`. Assert the result equals
`root / "docs/engineering/d/evidence/WO-D-001/WO-D-001-handoff.md"`.

### Scenario 3: failure path, an artifact outside a domain

With an artifact whose `path` is `root / "docs/engineering/WO-D-001.md"`,
assert `evidence_packet_path` raises `WEX-ECP-010` naming `WO-D-001`.

### Scenario 4: the Windows host reading

On a Windows workstation, run the full suite at the base commit and at the
candidate. Record both failure sets by name. Assert no name after the change
carries `WEX-ECP-010: ... is not under a domain directory`.

### Scenario 5: the reference is complete and current

Read `docs/notes/harnessctl-check.md` against `SPEC-ECP-008` ECP-HST-005.
Assert each listed section exists; assert every `WFL-*`, `PROC-*`, `QG-*`
and `QGP-*` identifier in its tables exists in the template contracts.

## Static and architecture checks

- `templates/repository/standard/scripts/artifact_layout_registry.py` is
  byte-identical before and after the change (`ECP-HST-003`).
- No other caller of `artifact_domain_from_relative_path` passes a
  `PurePath` (grep over `se_harness/` and the template scripts).

## Evidence retention

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-012/`: the
handoff packet with the test figures per host, the Windows before-and-after
failure sets, and the grep inventory.

## Pass criteria

Every deterministic test passes on the Linux lane. The Windows reading
shows the `WEX-ECP-010` errors gone. Graph and integrity readings come from
the exact released evaluator, se-harness 0.9.0, installed outside the
checkout.

## Residual uncertainty

The suite runs hosted on Linux only; the Windows reading is a workstation
reading until a Windows test lane exists, which is outside this contract.
