+++
id = "REQ-ECP-032"
type = "requirement"
title = "Every harnessctl failure follows the stated exit-code and one-code-per-line rules"
status = "approved"
owners = ["repository-owner", "engineering-owner"]
created = "2026-09-07"
updated = "2026-09-07"
statement = "WHEN a harnessctl command cannot complete, THE CLI SHALL report a result with exit 1 or a refusal with exit 2, printing each code once, on every path."
verification_method = ["test", "inspection"]
priority = "must"
source = "issue #375 (code health assessment 2026-09-07, wave 0, docs/notes/code-health-assessment-2026-09-07.md sections 3.1, 3.2 and the wave 0 plan); REQ-ECP-027 and SPEC-ECP-016, whose rules ECP-CLI-004 and ECP-CLI-006 state the two conventions this requirement makes hold everywhere"
measure = "check --checkpoint with an unknown artifact prints WEX210 once; transition refused by the mutation guard exits 2; no handler lets ProcedureError or a coded ValueError escape as a traceback; dashboard --json exits 2 when the engine refuses; pr-body prints a failed result with exit 1 for an unknown artifact; every subprocess launch in the package carries a timeout; each of the four latent defects has a test that fails before the fix"

[relations]
derives_from = ["CAP-ECP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T19:33:14Z"
decided_by = "repository-owner"
reason = "Approved on 2026-09-07 by the accountable owner with the words 'i approve', given after the packet PR #382 and its summary were presented: every harnessctl failure follows the stated exit-code and one-code-per-line rules (issue #375, wave 0 of the code health assessment of 2026-09-07). Approval of a definition authorizes no work."
+++

# Requirement: Every harnessctl failure follows the stated exit-code and one-code-per-line rules

## In plain words

The command reference already says how a failure looks: exit 1 for a
result, exit 2 for a refusal, one code per line. A few command paths break
those rules, and this requirement closes them.

## Why

The code health assessment of 2026-09-07 reproduced a doubled code on the
checkpoint path. It found handlers that exit 1, 2 or with a traceback for
one class of failure. A tool that automates on exit codes cannot tell
"refused" from "failed" without parsing text.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| a command path raises a coded message | the code becomes the result's code, printed once | a doubled code fails the checkpoint-path test |
| the mutation guard refuses a writing command | the refusal reaches standard error with exit 2 | an exit 1 result fails the transition test |
| an error class one handler converts escapes another | the other handler converts it the same way | a traceback fails the test |
| a subprocess hangs | the launch times out and the caller reports a refusal | none new |

## Examples

### Normal

**Given** this repository,

**When** the checkpoint check runs with an unknown artifact identifier,

**Then** the blocked result names the identifier with one code on the line.

### Failure

**Given** a checkout whose evaluator is not the released one,

**When** a transition is applied,

**Then** the guard's refusal goes to standard error with exit 2.
