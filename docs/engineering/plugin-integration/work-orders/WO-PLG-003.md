+++
id = "WO-PLG-003"
type = "work_order"
title = "Probe Codex plugin activation in isolated fixtures"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-09"

[assurance]
commit_bound_verification = "required"
rationale = "The later Codex support and adapter decisions depend on the correctness of the activation findings and their retained evidence."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "tests/plugin_integration/codex_probe/",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-003.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-003/",
  "docs/engineering/plugin-integration/verification-records/VREC-PLG-001.md",
  "docs/engineering/plugin-integration/evidence/VREC-PLG-001-evaluator.json",
  "GLOSSARY.md",
  "docs/notes/plugin-definition-delivery-2026-09-08.md",
  "docs/engineering/README.md",
  "docs/engineering/plugin-integration/README.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-006.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-003.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-003.md",
]

[relations]
implements = ["REQ-PLG-006"]
specifications = ["SPEC-PLG-003"]
verification = ["VER-PLG-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T21:39:49Z"
decided_by = "engineering-owner"
reason = "Operator explicitly approved the Codex probe packet reviewed at be8b4126 and authorized its work in this Codex task. Scope and required commit-bound assurance are unchanged; start is recorded separately."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-08T21:41:01Z"
decided_by = "engineering-owner"
reason = "Operator explicitly authorized starting the Codex probe work after approving its packet in this Codex task. Current start checks passed. No completion, assurance or external integration decision is inferred."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-09T17:23:27Z"
decided_by = "engineering-owner"
reason = "Operator explicitly approved marking WO-PLG-003 and WO-PLG-004 implemented in this Codex task on 2026-09-09, after reviewing the completion handoff and its documented C02 and platform coverage limits. This records completion only; independent commit-bound verification and integration remain separate decisions."
+++

# Work Order: Probe Codex plugin activation in isolated fixtures

## Lifecycle

The lifecycle events above record the engineering owner's approval, start,
and explicit completion decision. The work order is implemented.
VREC-PLG-001 is prepared; the independent assurance decision remains pending.

## Objective

Produce observed Codex activation evidence and a compatibility report before selecting a production adapter design.

## In scope

Disposable manifest and logging fixtures, isolated host profiles, activation attempts, missing-prerequisite cases, and a versioned compatibility table.


Definition introduction D01 selects this WO and the exact records listed in the [definition-delivery plan](../../../notes/plugin-definition-delivery-2026-09-08.md). Those paths cover draft introduction and separately authorized decisions, not implementation of another WO.

## Out of scope

Core evaluator changes, managed repository controls, approved definition amendments, public release or publication, and installation outside disposable host fixtures.

## Authorized decision envelope

After approval, choose minimal observation fixtures and repeatable local probe commands. A specific observed incompatibility is an acceptable result; production integration is unnecessary.

## Constraints

This investigation has no dependency on production adapters or unresolved DEC-PLG-001. Attempt available host/platform combinations; mark unavailable combinations honestly. The technical owner separately selects a supported route or host exclusion through DEC-PLG-001.
An evidenced incompatibility can complete this investigation. It does not require a synthetic positive result or authorize a production adapter.
The proposal source is PR #360 at `9e894e99`; this work order's approved relations and scope govern implementation.

## Expected change surface

Codex probe fixtures and their retained report only.
Definition delivery may also change its exact declared records and assigned index files.

## Required verification

Execute VER-PLG-003 against the exact candidate.
Record real host, operating-system, Python, and released-evaluator versions; no unrun case counts as passing.

## Evidence to record

Retain commands, independent expectations, observed results, candidate identity, and limitations under `evidence/WO-PLG-003/`.
Prepare the later verification record through the existing evaluator when authorized.

## Approved delivery-scope amendment — 2026-09-09

After the two exact generated paths were presented, the operator replied
"i approve" in this Codex task. As engineering owner, the operator approves
adding VREC-PLG-001 and its evaluator sidecar to this work order's delivery
scope under DR-REMEDIATION-SCOPE. As repository owner, the operator authorizes
committing and pushing them for review in PR #421.

This amendment permits publication of the prepared record in that PR only.
It is recorded after the bound candidate
`a8c880a11e0cece6932695b7951cfa047a9f691c`; it does not change that candidate,
the retained evidence, or the record's provenance. The work order remains
implemented and VREC-PLG-001 remains ready. Verification, PR merge, production
support selection, and package release or publication remain separate decisions.

## Stop and escalate conditions

Stop for missing approval, unmet prerequisites, failed required checks, unsafe interpreter identity, or changes outside the selected scope.
New host permissions or unsupported API assumptions require a concrete decision.

## Completion report format

Report changed paths, requirement coverage, checks and failures, exact candidate, retained evidence paths, and unresolved limits.
Do not infer approval, verification, release, or publication from successful tests.
