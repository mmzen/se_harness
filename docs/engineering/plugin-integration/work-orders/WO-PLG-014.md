+++
id = "WO-PLG-014"
type = "work_order"
title = "Optional helpers with enforced read-only boundaries"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"
[assurance]
commit_bound_verification = "required"
rationale = "Later decisions rely on changed plugin behavior or trusted guidance; assurance must bind the exact candidate."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "plugins/verity-plane/common/agents/",
  "plugins/verity-plane/claude-code/agents/",
  "plugins/verity-plane/codex/agents/",
  "tests/plugin_integration/helpers/",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-014.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-014/",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-024.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-014.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-014.md",
]

[relations]
implements = ["REQ-PLG-024"]
specifications = ["SPEC-PLG-014"]
verification = ["VER-PLG-014"]
architecture = ["ARCH-PLG-002", "ADR-PLG-002"]
+++

# Work Order: Optional helpers with enforced read-only boundaries

## Lifecycle

Draft proposal; classification and scope await approval. Start, completion, preparation, assurance and integration remain separate accountable decisions. No delegation is proposed.

## Objective

Provide optional investigator and evidence-reviewer definitions with demonstrated host restrictions and a main-agent fallback.

## In scope

Shared roles, supported host registrations, and permission/refusal/fallback tests. Retain this work order's evidence; definition delivery uses only the exact declared artifact paths.


The [definition-delivery plan](../../../notes/plugin-definition-delivery-2026-09-08.md) introduces this packet in D04 under WO-PLG-007. This WO's definition paths support its own introduction and separately authorized decisions.

## Out of scope

Mandatory helpers, privileged tools, autonomous implementation, decision delegation, or changed retained-skill contracts. No other packet's implementation or managed root changes.

## Authorized decision envelope

After approval, choose names, fixtures and wording within SPEC-PLG-014. Scope, acceptance criteria and decision ownership remain accountable-owner decisions.

## Constraints

Follow approved ARCH-PLG-002 and ADR-PLG-002. Demonstrate Codex registration and restrictions; unsupported combinations use the main agent.

## Expected change surface

Only declared exact files and component directories. Inspect before editing; coordinate overlapping setup changes.

## Required verification

Execute VER-PLG-014, repository-required checks and Git-derived scope/handoff checks using the governing released evaluator. Record candidate and host versions.

## Evidence to record

Retain inputs, outputs, changed paths, refusals and limitations under `evidence/WO-PLG-014/`. No VREC or RLS is prepared while this work remains draft.

## Stop and escalate conditions

Stop on failed identity, undeclared effects, unsupported required host behavior, unresolved blocking decisions, or scope expansion. Passing checks cannot approve work.

## Completion report format

Report implemented behavior, evidence, material non-effects, limitations and the evaluator's next accountable step. Completion does not decide assurance, merge or publication.
