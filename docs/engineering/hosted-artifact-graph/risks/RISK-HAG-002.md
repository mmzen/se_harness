+++
id = "RISK-HAG-002"
type = "risk"
title = "Rehearsal decisions mistaken for real authority"
status = "raised"
owners = ["mmzen"]
created = "2026-10-06"
updated = "2026-10-07"
description = "Hosted test-copy records can reach approved, verified or released states using supplied test actor labels. If a user imports or cites them as real engineering authority, genuine human decisions and assurance could be bypassed. Git remains authoritative; authentication and database ACL implementation are deferred."
action = "mmzen reviews the explicit test boundary and VER-HAG-006 refusal/export evidence before accepting WO-HAG-008. Revisit before any proposal for real authority cutover; do not import rehearsal decisions as real approvals."
raised_by = "operator"

[relations]
threatens = ["REQ-HAG-011", "REQ-HAG-013", "WO-HAG-008", "WO-HAG-009", "WO-HAG-010"]

[[lifecycle_events]]
from = "identified"
to = "raised"
decided_at = "2026-10-06T06:46:04Z"
decided_by = "operator"
reason = "Recorded by harnessctl raise-risk."
+++

# Risk: Rehearsal decisions mistaken for real authority

## Description

Hosted test-copy records can reach approved, verified or released states using supplied test actor labels. If a user imports or cites them as real engineering authority, genuine human decisions and assurance could be bypassed. Git remains authoritative; authentication and database ACL implementation are deferred.

## Next action

mmzen reviews the explicit test boundary and VER-HAG-006 refusal/export evidence before accepting WO-HAG-008. Revisit before any proposal for real authority cutover; do not import rehearsal decisions as real approvals.
