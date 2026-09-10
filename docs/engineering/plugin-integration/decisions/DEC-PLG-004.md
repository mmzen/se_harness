+++
id = "DEC-PLG-004"
type = "decision"
title = "Repository and plugin skill discovery"
status = "decided"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-10"

kind = "question"
question = "Which supported ownership mechanism makes one skill route active when repository-managed and plugin skills coexist?"
raised_by = "implementation-planner"
recommendation = "supported-migration"

[[options]]
id = "supported-migration"
label = "Use an ownership-aware evaluator migration before activating the plugin route."

[[options]]
id = "retain-repository-route"
label = "Keep repository skills active and defer conflicting plugin discovery."

[relations]
concerns = ["REQ-PLG-016", "SPEC-PLG-009", "WO-PLG-009", "WO-PLG-012", "SPEC-AEX-005"]
blocks = ["SPEC-PLG-009"]

[disposition]
option = "supported-migration"
label = "Use an ownership-aware evaluator migration before activating the plugin route."
decided_by = "technical-owner"
decided_at = "2026-09-10T18:06:34Z"
reason = "On 2026-09-10 the technical owner confirmed \"OK then\" after asking whether supported-migration means existing SE Harness skills are replaced by the plugin versions. The accepted objective is: plugin setup for a repository automatically replaces existing SE Harness skill implementations with the plugin implementations, updates ownership records and integrity checks, and confirms one active implementation per overlapping skill, without manual cleanup. Unrelated skills remain untouched. The supported released evaluator migration may remove obsolete managed repository copies because plugin copies live elsewhere; ad hoc deletion or lock rewriting is not the route. Inspection of released evaluator 0.17.0 found no exposed ownership-migration operation. The decision selects the target and requires separate evaluator implementation, release and adoption before affected live repository connection; it does not claim that migration exists. Isolated implementation and testing of WO-PLG-010, WO-PLG-011 and WO-PLG-012 can proceed within their own approved scopes. Blocked definitions remain unchanged by this disposition; no verification, merge or release decision is supplied."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-09-10T18:06:34Z"
decided_by = "technical-owner"
reason = "On 2026-09-10 the technical owner confirmed \"OK then\" after asking whether supported-migration means existing SE Harness skills are replaced by the plugin versions. The accepted objective is: plugin setup for a repository automatically replaces existing SE Harness skill implementations with the plugin implementations, updates ownership records and integrity checks, and confirms one active implementation per overlapping skill, without manual cleanup. Unrelated skills remain untouched. The supported released evaluator migration may remove obsolete managed repository copies because plugin copies live elsewhere; ad hoc deletion or lock rewriting is not the route. Inspection of released evaluator 0.17.0 found no exposed ownership-migration operation. The decision selects the target and requires separate evaluator implementation, release and adoption before affected live repository connection; it does not claim that migration exists. Isolated implementation and testing of WO-PLG-010, WO-PLG-011 and WO-PLG-012 can proceed within their own approved scopes. Blocked definitions remain unchanged by this disposition; no verification, merge or release decision is supplied."
+++

# Decision: Repository and plugin skill discovery

## Question

Which supported ownership mechanism makes one skill route active when repository-managed and plugin skills coexist?

Existing skill locations and managed digests are contract-bound. A plugin cannot delete those copies, edit their locks, or assume namespacing suppresses duplicate discovery.

## Options

**supported-migration.** Use an ownership-aware evaluator migration before activating the plugin route.

**retain-repository-route.** Keep repository skills active and defer conflicting plugin discovery.

## Recommendation

Inspect the selected released evaluator before choosing. If it lacks the necessary migration operation, define and approve separate evaluator work, release it, then resume plugin connection.

## Disposition

The technical owner selected **supported-migration** on 2026-09-10. The released evaluator recorded the decision in the disposition above.

During repository setup, the supported migration automatically replaces existing SE Harness skills with the plugin implementations, updates ownership and integrity records, and confirms one active implementation per overlapping skill. No manual cleanup is required. Unrelated skills remain untouched.

The selected target still needs a supported evaluator migration, its release and adoption. Until it is available, affected live discovery remains unready under SPEC-PLG-009. Isolated work on WO-PLG-010, WO-PLG-011 and WO-PLG-012 remains possible within its own authority. This decision does not approve or implement the blocked specification.
