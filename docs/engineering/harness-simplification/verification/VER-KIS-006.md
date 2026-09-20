+++
id = "VER-KIS-006"
type = "verification"
title = "Check: match repository protection to the stated approval policy"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-19"
updated = "2026-09-20"

[relations]
verifies = ["REQ-KIS-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-20T06:27:29Z"
decided_by = "assurance-owner"
reason = "On 2026-09-20 the owner approved the presented recovery artifact package with \"i approve\". Record approval of this reviewed artifact in the named owner role. Reviewed full-byte SHA-256: 5f08e85051a6d4f618ed670ad77842256dca82384f3f7558e62998581180a713. DEC-KIS-001 separately records the explicit owner-review choice. WO approval grants the bounded execution operations in DR-015; this transition records no implementation result, assurance acceptance or external action."
+++

# Check: match repository protection to the stated approval policy

## Independence

Expected outcomes come from REQ-KIS-012, SPEC-KIS-006 and the retained assessment reproductions.
Do not derive expectations from candidate output or replace failing gates with test
substitutes in the acceptance examples. The responsible assurance owner judges the
result under the chosen repository review policy; this contract records no completed checks.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-KIS-012 | inspection, demonstration | P1, P2, P3, P4, P5 | Every case below meets its expected result and preserves the retained KISS protections. |

## Acceptance cases

### P1: Settings and actual statuses

Read effective rules and enumerate current acceptance jobs. Map each required acceptance result to its actual status and candidate. Record which routes and bypasses were assessed and which were not.

### P2: Normal merge refusal

In an explicitly authorized disposable host target or non-merging test PR, show that missing/failed required checks and missing required current review block the normal merge route. A workflow that only prints pass cannot be accepted as proof that the expected tests ran.

### P3: Scope and identity

Compare a changed work description with its recorded reviewed version while keeping paths unchanged. Review requires an amendment. A supplied owner label or edited approval event cannot substitute for the actual decision reference.

### P4: Control and publication boundary

Inspect review protection for workflow/owner/checker changes and each used publication route. Demonstrate independent controls only if that option was selected and a real second reviewer exists. Enumerate remaining bypasses without claiming a real publish occurred.

### P5: Preserved local workflow

Demonstrate ordinary approved local execution and evidence preparation with GitHub unavailable. No local step gains a new live-CI, preliminary-merge or repeated-approval dependency.

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
`evidence/WO-KIS-012/`. Record unavailable checks as unavailable, not passed. Keep the
original tested candidate and historical evidence. A later commit-bound VREC records
actual assurance; this draft verification contract is only a test plan.

Live demonstrations need an exact authorized target and action. Until those checks
are observed, host enforcement remains unassessed. Owner-controlled review cannot
be reported as independent or tamper-proof enforcement. DEC-KIS-001 must be resolved.
