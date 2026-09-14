+++
id = "VER-PLG-009"
type = "verification"
title = "Check the project connection and repair outcomes"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-14"
updated = "2026-09-14"

[relations]
verifies = ["REQ-PLG-015", "REQ-PLG-016"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T22:05:14Z"
decided_by = "assurance-owner"
reason = "The owner reviewed and approved completion of the KISS backlog amendment and explicitly said \"you can start WO-PLG-009 and WO-PLG-016\" on 2026-09-15. This accepts the selected rewritten definition chain and authorizes its bounded routine execution, checks and evidence under the installed evaluator. No result-specific assurance, merge, release or live host/project installation is inferred."
+++

# Check the project connection and repair outcomes

## Checks

| Outcome | Check | Pass condition |
| --- | --- | --- |
| Connection: REQ-PLG-015/016 | Follow the instructions on small disposable new and existing projects. Reuse current init/ownership integration tests for unchanged behavior. | Expected provider/skills and successful explicit check; unrelated files remain. |
| Maintenance: REQ-PLG-015 | Repeat setup, then repair the environment; exercise the documented explicit upgrade path with an available compatible release or labeled development fixture. | One environment is usable; routine repair/plugin update preserves the selected project version. |
| Actual failure boundaries: REQ-PLG-015/016 | Reuse tests for missing prerequisites/replacement, escaped destination and interrupted replacement. Add a small test only for a newly changed uncovered behavior. | Failure is clear; no outside write or premature deletion; rerun finishes when the cause is fixed. |

Review the instructions for retired hook, receipt, ownership-conflict and environment
switching requirements. Keep one result summary with commands, versions and outcomes,
linking existing evidence where it still applies. Do not require per-case archives,
internal-call inventories, full repository snapshots or a host permutation matrix.
Run the repository's required checks for the actual diff. Native discovery and
public-install claims are assessed once under VER-PLG-016. No live project is changed
by fixture acceptance and an unavailable released feature is not reported as tested.
