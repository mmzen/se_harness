+++
id = "INT-HAG-002"
type = "intent"
title = "Exercise the engineering lifecycle in a hosted test copy"
status = "draft"
owners = ["mmzen"]
created = "2026-10-06"
updated = "2026-10-06"
outcome = "A human and agent can complete and inspect the engineering lifecycle on a private hosted test copy while Git remains authoritative for real work."

[relations]
+++

# Exercise the engineering lifecycle in a hosted test copy

## Intended outcome

A human and agent can exercise the engineering lifecycle in one private hosted
test project, inspect each result, recover uncertain writes and export the exact
records. Git remains authoritative for real engineering work and decisions.
DEC-HAG-004 records mmzen's scope choice: "Git remains authoritative."

## Problem

Phase 2 supports context reads and draft authoring. It does not support the
workflow operations that approve definitions, advance work, record decisions,
or prepare verification and release records. Those missing paths prevent a
complete functional pilot of the graph-backed workflow.

## Smallest useful result

One guided change runs from draft definitions to a test release decision through
the installed remote client. The same released evaluator determines legality
in the graph service and an independent file-based reference run. Exported test
records retain their exact bytes, evidence and Git identities. No service result
is imported into the real repository as a human approval or assurance decision.

The pilot remains one service, one Memgraph store, one project and explicit
synchronous requests. Authentication and database ACL implementation are
deferred by the requester. Existing sandbox access restrictions remain in place;
this package neither strengthens nor removes them.

## Success measures

| Measure | Today | When reached | Observed |
| --- | --- | --- | --- |
| Operator can complete a change in the hosted test copy | Only reads and draft edits are supported | One documented run reaches a test release decision and an inspectable export | Operator records outcome and interventions after each pilot run |
| Operator can recover a lost operation result | Qualified for Phase 2 draft operations | The same recovery procedure works for lifecycle and record operations | Operator retains the recovered receipt when a response is uncertain |

The verification contract defines acceptance tests; this draft claims no new
observed operational result.

## Exclusions

- Real artifact-authority cutover or synchronization back into authoritative Git.
- New authentication, identity providers, database roles or ACL qualification.
- Public access, production operation, multi-tenancy, a UI or background jobs.
- Publication, tagging, host-plugin installation, deployment or a real release decision.
- Rewriting accepted Phase 2 definitions, historical records or bound evidence.

## Relationship to the earlier roadmap

This is the functional test-copy portion of Phase 3. The authority switch and
its security prerequisites in SPEC-HAG-003 remain future work. The original
definitions continue to govern the delivered Phase 2 behavior; this new intent
does not replace them. RISK-HAG-001 remains raised.
