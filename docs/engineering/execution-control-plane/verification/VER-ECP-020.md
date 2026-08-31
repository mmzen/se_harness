+++
id = "VER-ECP-020"
type = "verification"
title = "Independent evidence for the .gitattributes tail removal"
status = "approved"
owners = ["assurance-owner"]
created = "2026-08-31"
updated = "2026-08-31"

[relations]
verifies = ["REQ-ECP-029"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-31T14:22:20Z"
decided_by = "assurance-owner"
reason = "Approved by the accountable owner on 2026-08-31 by selecting the presented option 'Approve WO-ECP-024 and delegate': deletion, liveness and delegation-evidence rows."
+++

# Verification: Independent evidence for the .gitattributes tail removal

## Method

| Requirement | Method | Pass condition |
| --- | --- | --- |
| `REQ-ECP-029` deletion | inspection + sweep | `.gitattributes` contains no "Retained from WO-ECP-010" text and no `agent_contract` rule; the managed block bytes unchanged (`doctor` 0 FAIL) |
| `REQ-ECP-029` liveness | test | every non-comment rule matches ≥1 tracked path or a declared byte-exact tree (measured with `git ls-files`); the hash-bound and upgrade-rehearsal suites pass unchanged |
| `SPEC-ECP-018` delegation | the work order's own lifecycle events | the start, implemented and record-preparation events name `delegated-executor` with the class, the check-run id and the head sha; the approval and verification events name humans |

## Independence

The liveness measurement uses Git, not the changed file's own claims; the
delegation evidence is the lifecycle events the evaluator writes, read back
from the artifacts.

## Evidence

`docs/engineering/execution-control-plane/evidence/WO-ECP-024/`.
