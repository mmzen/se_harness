+++
id = "VER-KIS-007"
type = "verification"
title = "Check: give agents one consistent route with bounded reading"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-19"
updated = "2026-09-20"

[relations]
verifies = ["REQ-KIS-013"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-20T06:27:29Z"
decided_by = "assurance-owner"
reason = "On 2026-09-20 the owner approved the presented recovery artifact package with \"i approve\". Record approval of this reviewed artifact in the named owner role. Reviewed full-byte SHA-256: e2a2112b97108b3dcc529b3c2519d8145b58d2ac6e4e93c4227a47f5464e8d3f. DEC-KIS-001 separately records the explicit owner-review choice. WO approval grants the bounded execution operations in DR-015; this transition records no implementation result, assurance acceptance or external action."
+++

# Check: give agents one consistent route with bounded reading

## Independence

Expected outcomes come from REQ-KIS-013, SPEC-KIS-007 and the retained assessment reproductions.
Do not derive expectations from candidate output or replace failing gates with test
substitutes in the acceptance examples. The responsible assurance owner judges the
result under the chosen repository review policy; this contract records no completed checks.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-KIS-013 | inspection, demonstration | G1, G2, G3, G4, G5 | Every case below meets its expected result and preserves the retained KISS protections. |

## Acceptance cases

### G1: One authority explanation

Read the operating card, workflow guide, decision-rights guide and relevant plugin references together. Each action has one consistent actor and authority meaning, including executor start/completion and reserved assurance/release.

### G2: Fresh agent

Observe an ordinary approved task in the existing acceptance setup. The agent selects the governing released checker, completes covered steps without duplicate permission and requests the genuine missing owner decision.

### G3: Resumed agent

Resume with bounded retained context and a changed relevant input. The agent reads the selected contracts, recognizes the changed input or failed gate and does not reuse obsolete authority or a previous green result.

### G4: Two active tasks

Allocate two different record-number blocks through the coordinator. Both task creators use their allocations. A deliberately duplicated ID is caught before integration; no collision-free guarantee is claimed for uncoordinated writers.

### G5: Result and adoption

Review the short brief against the full structured result. Required facts and command boundaries survive shortening. A normal project upgrade receives candidate policy through the released route and explicitly reconciles preserved editable guides.

## Platforms, evaluator and regression

Use the current project-selected released evaluator for governance (0.18.0 in this
checkout), and clearly label candidate-source or ephemeral-package acceptance. Check
portable CLI/file behavior on Windows and the existing Linux CI route. Host-rule cases
use GitHub; agent walkthroughs use the supported Codex/Claude routes actually claimed
by the changed package. Do not claim a platform or host that was not exercised.

Run the affected existing tests during implementation and the project-required suite
and package checks before acceptance of the combined change. Retain the normal success
case as well as the observed failure case. No performance matrix or speculative test
framework is required.

## Retention and uncertainty

Retain concise observed results and retrievable raw-output references under
`evidence/WO-KIS-013/`. Record unavailable checks as unavailable, not passed. Keep the
original tested candidate and historical evidence. A later commit-bound VREC records
actual assurance; this draft verification contract is only a test plan.
