+++
id = "REQ-HAG-011"
type = "requirement"
title = "Rehearse lifecycle actions without changing Git authority"
status = "draft"
owners = ["mmzen"]
created = "2026-10-06"
updated = "2026-10-06"
statement = "A human or agent can exercise supported lifecycle operations in a private hosted test copy, using the released evaluator, without changing real engineering authority."
verification_method = ["test", "demonstration"]
priority = "must"
source = "INT-HAG-002; DEC-HAG-004; mmzen: Git remains authoritative"

[relations]
derives_from = ["CAP-HAG-002"]
+++

# Rehearse lifecycle actions without changing Git authority

## In plain words

The graph project is a rehearsal. Git remains the authoritative source for real
engineering definitions, approvals, verification and release decisions.

## Why

The owner needs to assess the complete workflow before considering a real
authority switch. DEC-HAG-004 selects this boundary. Authentication and graph
database ACL implementation are deferred; existing sandbox controls remain.

## Behavior and acceptance

1. An explicitly selected test project supports definition acceptance, work
   progression, decision recording, verification preparation and assessment, and
   release-record preparation and assessment through the released evaluator.
2. The installed remote client identifies every lifecycle result as test data.
   Actor labels supplied to a test are not proof of actual human consent.
3. Imported real records remain immutable. The service cannot apply rehearsal
   decisions to a real checkout or invoke publication/deployment actions.
4. Unsupported commands, missing test selection, and evaluator refusals produce
   explicit failures. The affected graph state remains unchanged.

## Examples

**Normal:** Given a disposable project and complete new test definitions, a
supplied test approval advances only the selected records when the evaluator's
gates pass. The response identifies the project as a rehearsal.

**Failure:** A request to approve an imported real work order fails, even if its
supplied actor label matches a recorded owner. Its bytes and state are unchanged.
