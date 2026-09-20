+++
id = "VER-KIS-005"
type = "verification"
title = "Check: use the full current checks before completion"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-19"
updated = "2026-09-20"

[relations]
verifies = ["REQ-KIS-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-20T06:27:29Z"
decided_by = "assurance-owner"
reason = "On 2026-09-20 the owner approved the presented recovery artifact package with \"i approve\". Record approval of this reviewed artifact in the named owner role. Reviewed full-byte SHA-256: 9ec60539eb38f764638d5397a8ad3fff337d0dd766cb618720fdef2f5f15c7c1. DEC-KIS-001 separately records the explicit owner-review choice. WO approval grants the bounded execution operations in DR-015; this transition records no implementation result, assurance acceptance or external action."
+++

# Check: use the full current checks before completion

## Independence

Expected outcomes come from REQ-KIS-011, SPEC-KIS-005 and the retained assessment reproductions.
Do not derive expectations from candidate output or replace failing gates with test
substitutes in the acceptance examples. The responsible assurance owner judges the
result under the chosen repository review policy; this contract records no completed checks.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-KIS-011 | test, inspection | C1, C2, C3, C4, C5 | Every case below meets its expected result and preserves the retained KISS protections. |

## Acceptance cases

### C1: Direct bypass

Repeat F4 with one admitted and one outside-scope edit. Handoff and direct transition to implemented both refuse, and readback shows unchanged status.

### C2: Changed inputs

Pass handoff, then add a relevant edit, alter the baseline or remove evidence. Completion evaluates the new situation and rejects missing or invalid inputs rather than consuming the old pass.

### C3: Complete diff

Exercise representative rename/deletion and untracked-file changes. A listed-path claim that omits actual task changes cannot pass completion. A later baseline that hides those changes is refused.

### C4: Scope agreement

Repeat F8 with an unrelated incomplete draft: readiness, planning and apply agree. Replace it with a selected dependency error or ambiguous duplicate ID: all relevant paths refuse.

### C5: Valid offline work

An approved normal task with matching evidence completes without network access or a second owner permission request. No verification, release or delivery state is inferred.

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
`evidence/WO-KIS-011/`. Record unavailable checks as unavailable, not passed. Keep the
original tested candidate and historical evidence. A later commit-bound VREC records
actual assurance; this draft verification contract is only a test plan.
