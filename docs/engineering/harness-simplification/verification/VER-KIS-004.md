+++
id = "VER-KIS-004"
type = "verification"
title = "Check: keep evidence outcomes truthful"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-19"
updated = "2026-09-20"

[relations]
verifies = ["REQ-KIS-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-20T06:27:29Z"
decided_by = "assurance-owner"
reason = "On 2026-09-20 the owner approved the presented recovery artifact package with \"i approve\". Record approval of this reviewed artifact in the named owner role. Reviewed full-byte SHA-256: eb2655c94ed5e6f6da98f375e63b42e4e1c074e1b44426a3e2864a6fd408dbd6. DEC-KIS-001 separately records the explicit owner-review choice. WO approval grants the bounded execution operations in DR-015; this transition records no implementation result, assurance acceptance or external action."
+++

# Check: keep evidence outcomes truthful

## Independence

Expected outcomes come from REQ-KIS-010, SPEC-KIS-004 and the retained assessment reproductions.
Do not derive expectations from candidate output or replace failing gates with test
substitutes in the acceptance examples. The responsible assurance owner judges the
result under the chosen repository review policy; this contract records no completed checks.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-KIS-010 | test, inspection | E1, E2, E3, E4, E5 | Every case below meets its expected result and preserves the retained KISS protections. |

## Acceptance cases

### E1: Failure and absence

Replay the assessment failure-text file, a missing command run and an unavailable output reference. Required success is refused, with a distinct reason; attachment availability alone is not a pass.

### E2: Stale observation

Run a successful relevant check, change relevant code, then request handoff and explicit attachment rebinding. The old tested version and outcome stay unchanged; affected checks remain required. Also replay the original stale failure-body case.

### E3: Valid capture and reuse

Capture a real successful required command. Keep the relevant code and governing inputs fixed while changing an unrelated note. Evidence remains usable without rerunning the full suite and retains its original observed identity.

### E4: Read versus write

Compare the caller tree before and after projection, scope and handoff checks. They are unchanged. Explicit capture lists its actual writes and does not claim assurance approval.

### E5: Meaning and methods

An irrelevant successful command does not satisfy another required check. A contract-authorized manual inspection can satisfy its own criterion with the responsible assessment. Review structured and human results for the same meaning.

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
`evidence/WO-KIS-010/`. Record unavailable checks as unavailable, not passed. Keep the
original tested candidate and historical evidence. A later commit-bound VREC records
actual assurance; this draft verification contract is only a test plan.
