+++
id = "DEC-PLG-004"
type = "decision"
title = "Repository and plugin skill discovery"
status = "open"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"

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

Pending. Only the evaluator records a disposition after the accountable owner's explicit decision.

Keeping the repository route does not satisfy plugin migration. The technical owner must amend or reject incompatible proposed scope before it can proceed.
