+++
id = "RISK-HAG-001"
type = "risk"
title = "Cypher lacks a database-enforced read-only boundary in the sandbox"
status = "raised"
owners = ["security-owner"]
created = "2026-10-04"
updated = "2026-10-07"
description = "Cypher remains available by user direction while Memgraph-side read-only enforcement is deferred. A flaw in application query admission or rollback handling could permit an unintended graph write. Application restrictions are not a database authorization boundary, so the POC cannot establish safe authoritative or untrusted-network use."
action = "Security owner: before Phase 3 authority cutover or untrusted-network exposure, qualify a Memgraph-enforced read-only role or an equivalently enforced database boundary for the query connection, including its edition and licensing implications. Retain Cypher in the disposable Phase 2 sandbox with application restrictions, explicit view binding, limits, rollback defense and adversarial refusal tests. Resolve this open item through the existing decision process; do not infer formal risk acceptance from the deferral."
raised_by = "operator"

[relations]
threatens = ["REQ-HAG-006", "WO-HAG-001", "WO-HAG-009", "WO-HAG-010"]

[[lifecycle_events]]
from = "identified"
to = "raised"
decided_at = "2026-10-04T09:47:13Z"
decided_by = "operator"
reason = "Recorded by harnessctl raise-risk."
+++

# Risk: Cypher lacks a database-enforced read-only boundary in the sandbox

## Description

Cypher remains available by user direction while Memgraph-side read-only enforcement is deferred. A flaw in application query admission or rollback handling could permit an unintended graph write. Application restrictions are not a database authorization boundary, so the POC cannot establish safe authoritative or untrusted-network use.

## Next action

Security owner: before Phase 3 authority cutover or untrusted-network exposure, qualify a Memgraph-enforced read-only role or an equivalently enforced database boundary for the query connection, including its edition and licensing implications. Retain Cypher in the disposable Phase 2 sandbox with application restrictions, explicit view binding, limits, rollback defense and adversarial refusal tests. Resolve this open item through the existing decision process; do not infer formal risk acceptance from the deferral.
