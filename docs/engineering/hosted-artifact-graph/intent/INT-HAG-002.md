+++
id = "INT-HAG-002"
type = "intent"
title = "Exercise the engineering lifecycle in a hosted test copy"
status = "approved"
owners = ["mmzen"]
created = "2026-10-06"
updated = "2026-10-06"
outcome = "A human and agent can complete and inspect the engineering lifecycle on a private hosted test copy while Git remains authoritative for real work."

[relations]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-06T18:40:36Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"I approve\" to the Phase 3 package published in PR #542 at 689dee3b1929e5c58338df1331a0eb9df484ce25. Approves the nine governing definitions and WO-HAG-008, including required commit-bound verification under VER-HAG-006 and its bounded local execution. Git remains authoritative; this is a private test-copy lifecycle rehearsal. Authentication and database ACL implementation remain deferred; existing controls stay. Includes the reviewed bounded publication grant to mmzen/se_harness, source codex/hosted-artifact-phase3, target main, draft PR #542, including the ready record and a later separately supplied verification-decision push. No risk acceptance, actual assurance decision, merge, real authority cutover, release, deployment or host-plugin update is granted."
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
