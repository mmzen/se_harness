+++
id = "SPEC-ECP-008"
type = "specification"
title = "Host-independent resolution of evaluator-derived paths, and the check command's reference"
status = "approved"
owners = ["technical-owner", "quality-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
specifies = ["REQ-ECP-019"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T07:45:09Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-29 by the accountable owner, 'i approve the artifact packet', for the repair of issue #254: render the evaluator's own artifact path as POSIX before the domain resolver's text guard, prove it with PureWindowsPath tests on the Linux lane, and add the plain-English reference for harnessctl check. Measured before this transition over branch state 88d1a1f carrying unmoved main aa99773: validate PASS at 0 errors under the governing 0.9.0 root; start preflight reads only the draft signature. Approval of a definition authorizes no work; the work order is approved separately."
+++

# Specification: Host-independent resolution of evaluator-derived paths, and the check command's reference

## Scope

The one code path that hands the evaluator's own `PurePath` to a resolver
written for untrusted text (`evidence_packet_path`, issue #254), the
resolver's treatment of `PurePath` values, the regression tests that make
the defect visible on the Linux lane, and the human reference for
`harnessctl check` that the same defect showed to be missing: an operator
who met `WEX-ECP-010` had no page saying what `check` does, at which
checkpoints, for which states, under which gates, and why it refuses.

## Terms

- **Evaluator-derived path:** a `PurePath` the evaluator computed from its
  own catalog (`artifact.path.relative_to(root)`), as opposed to text
  received from an argument, a manifest, a lock, or a pull-request body.
- **Text guard:** the rule that a relative path containing a backslash is
  not a normalized repository path and resolves to no domain.

## Rules

**ECP-HST-001:** `evidence_packet_path` passes
`artifact.path.relative_to(root).as_posix()` to
`artifact_domain_from_relative_path`; the packet path it returns is
`root / "docs" / "engineering" / DOMAIN / "evidence" / WO-ID /
"WO-ID-CHECKPOINT.md"` on every host.

**ECP-HST-002:** `se_harness.artifact_layout.artifact_domain_from_relative_path`
renders a `PurePath` argument with `.as_posix()` before applying the text
guard; a `str` argument keeps the text guard unchanged, so
`"docs\\engineering\\d\\work-orders\\WO-D-001.md"` still resolves to no
domain while `PureWindowsPath` of the same value resolves to `d`.

**ECP-HST-003:** The managed template copy
`templates/repository/standard/scripts/artifact_layout_registry.py` is not
changed: it is hash-locked in every installed root, is only ever called with
display strings, and the two copies already differ in their domain check.

**ECP-HST-004:** Regression tests construct the artifact path as
`PureWindowsPath` so that both the resolver rule and the packet-path rule
are asserted on the Linux lane; on a Windows host the existing
`test_workflow_compliance`, `test_workflow_execution` and
`test_delegated_workflow` cases become the same assertion against real
`WindowsPath` values, and the work order's evidence records their count
before and after on that host.

**ECP-HST-005:** `docs/notes/harnessctl-check.md` is the reference for
`harnessctl check`. It states, in this order and in plain English: what the
command does and does not do; the four checkpoints and when each is used;
how the selected artifact's type, state and related records choose the
workflow rule, its procedure and its gates, as a table over every rule of
`WORKFLOW.json`; the gates and predicates each checkpoint evaluates, from
`QUALITY_GATES.json`; how the change set is supplied and how the scope
predicates read it; the two outcomes and what `Blocked by` names; every
refusal code the command can emit with its cause; and the worked sequence of
one work order from `approved` to `implemented`. It is indexed in
`docs/notes/README.md` and linked from `docs/notes/harnessctl-reference.md`.
Its tables are derived from the contracts, never restated as policy.

## Error and recovery

A `PurePath` that is absolute, or outside `docs/engineering/`, still resolves
to no domain and `evidence_packet_path` still raises `WEX-ECP-010` naming the
artifact; nothing else about the refusal changes.

## Verification

`VER-ECP-008`.
