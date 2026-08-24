+++
id = "SPEC-WEX-003"
type = "specification"
title = "Semantic-fidelity lifecycle handoff contract"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
specifies = ["REQ-WEX-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T17:31:43Z"
decided_by = "technical-owner"
+++

# Specification: Semantic-fidelity lifecycle handoff contract

## Scope

This specification defines two presentation paths over the existing
`se-harness-workflow-result-v2`:

1. **direct exact rendering**, in which trusted software produces the existing
   canonical human block; and
2. **adaptive human handoff**, in which an agent explains the authoritative
   result while preserving its decision-relevant semantics.

It replaces the verbatim-agent-output rule in the agent-facing portions of
`SPEC-WEX-002`, `ENGINEERING_HARNESS.md`, `WORKFLOW.md`, `AGENTS.md`, and
`CLAUDE.md`. It does not replace schema-2, its restitution object, deterministic
human rendering, workflow selection, quality gates, procedures, lifecycle
rules, or decision rights.

## Actors and external systems

- `harnessctl` computes and validates the workflow result and the one typed next
  step.
- A direct renderer converts that result to deterministic human bytes without a
  model in the path.
- A supported agent adapter receives the structured result and prepares a
  user-facing explanation.
- An application or automation consumer declares whether it needs structured
  JSON, direct exact human rendering, or an adaptive handoff.
- The user or accountable owner makes any required decision; no renderer or
  agent gains that authority.

## Inputs

The input is one validated `se-harness-workflow-result-v2` produced for a
selected workflow operation. Consumers must use the structured value, not parse
a previously rendered human block.

The authoritative semantic projection is:

| Source field | Meaning that must be preserved |
| --- | --- |
| `operation.outcome`, `restitution.outcome` | whether the selected operation completed or blocked |
| `selection` | actual selected artifact identities |
| `restitution.done` | effects observed during this operation |
| `restitution.not_done` | expected effects that remain incomplete |
| procedure and declared non-effects | effects explicitly known not to have occurred |
| `restitution.blocked_by` | exact predicates preventing progress |
| `restitution.current_lifecycle_state` | actual final artifact states |
| `restitution.decision_required` | decision right, role, artifact, decision, and permitted outcomes |
| `restitution.next` | the one recommended typed procedure step |
| `restitution.command_or_response` | canonical argument array or precise suggested response |
| `restitution.alternatives` | complete declared alternatives, never extra recommendations |

## Outputs

### Structured output

JSON output remains the complete authoritative schema-2 result. No field or
cardinality changes are introduced by this specification.

### Direct exact human output

Direct exact output remains the deterministic block produced from schema-2 by
the existing renderer. It retains the current ordered headings and empty-value
rules. Its supported uses include terminal output, snapshots, documentation,
and explicitly format-dependent integrations.

Exactness is a property of the direct renderer path. Copying the text through a
model is not an exact-rendering mechanism.

### Adaptive human handoff

An adaptive handoff may:

- lead with the outcome or the decision the user needs to make;
- use prose, a short list, or compact headings;
- merge fields whose distinct meaning remains clear;
- omit empty blocker and alternative fields;
- omit `Not done` when there is no incomplete expected effect;
- add relevant explanation of the lifecycle result;
- adjust vocabulary to the user's technical level; and
- display complete alternatives separately after the one recommendation.

It must:

- identify the selected artifact when an artifact is selected;
- state the completed or blocked outcome without reversing its meaning;
- distinguish observed effects from incomplete work;
- preserve every blocker and non-effect that changes what the user may safely
  believe or do next;
- preserve the final lifecycle state;
- name the accountable role and required decision when present;
- recommend exactly one next action selected by the workflow result; and
- preserve command argument values and boundaries or the suggested response's
  operative meaning.

It must not:

- claim an unobserved effect or exercised authority;
- conceal a blocker or required decision;
- introduce a second recommendation or undeclared alternative;
- add an unrelated finding as part of the selected result;
- turn a non-effect into a completed effect; or
- claim byte-for-byte compliance.

## State model

| State | Condition | Permitted presentation behavior |
| --- | --- | --- |
| `result-unavailable` | no valid schema-2 result | stop; report that no authoritative handoff can be constructed |
| `result-valid` | schema and semantic validation pass | select one declared presentation path |
| `direct-exact` | consumer requires exact human output | renderer emits deterministic bytes; no model transformation |
| `adaptive` | consumer requests or accepts agent explanation | agent preserves the semantic projection and one next action |
| `handoff-nonconforming` | required semantics differ or are missing | do not treat the presentation as lifecycle authority; retain the source result |

Presentation state does not modify formal lifecycle state.

## Behavioral rules

1. Validate schema-2 before presentation.
2. Retain the structured result as the evidence source for either presentation
   path.
3. Choose direct exact rendering whenever a caller, protocol, snapshot, or test
   requires exact headings or bytes.
4. Never route exact rendering through a language model.
5. Permit adaptive presentation only when the consumer does not require exact
   formatting.
6. Treat artifact IDs, lifecycle states, outcomes, blockers, accountable roles,
   decision rights, command arguments, and the selected next step as closed
   values; paraphrasing must not alter them.
7. Treat observed effects and incomplete expected effects as separate sets.
8. Preserve a non-effect in adaptive output when omitting it could imply that a
   lifecycle transition, approval, verification, release, Git action,
   publication, deployment, or other external effect occurred.
9. Permit omission of a non-effect only when the surrounding output cannot
   reasonably imply that effect and the user did not ask about it.
10. Show no more than one recommended next action. Declared alternatives remain
    alternatives and must not be phrased as additional recommendations.
11. Relevant explanation may describe why the action is next, but it must not
    recompute legality, select another procedure, or resolve an accountable
    decision.
12. Agent-specific instructions remain thin adapters to this contract. They may
    constrain style but may not define lifecycle semantics.
13. A conformance test of agent output compares the semantic projection, not
    exact prose, whitespace, heading names, or field order.
14. A conformance test of direct rendering compares the deterministic renderer
    output and may compare exact bytes.

## Error and recovery behavior

- Invalid or incomplete structured input fails before either presentation path.
- A direct-renderer failure returns a typed rendering error and preserves the
  source result.
- A detected adaptive mismatch reports the differing semantic field and
  retains the source result for retry or direct display.
- Failure must not substitute a generic next action, drop the original blocker,
  or mutate an artifact.
- When an agent host cannot be tested or constrained, documentation must state
  that limitation rather than claim enforcement.

## Data and interface contracts

- `se-harness-workflow-result-v2` remains unchanged.
- Existing restitution validation and `render_human` behavior remain supported.
- Machine consumers must use JSON fields and canonical argument arrays.
- Human exactness means output produced directly by the installed trusted
  renderer from the validated result.
- Adaptive conformance is defined by the matrix in this specification and
  verifier-owned positive and negative cases in `VER-WEX-003`.
- No natural-language parser becomes part of the trusted lifecycle kernel.

## Security and privacy properties

- Treat result text, artifact content, commands, paths, and provider output as
  untrusted display data.
- Preserve argument boundaries; do not convert canonical argv into an
  executable shell string.
- Do not allow injected artifact text to create headings, decisions,
  alternatives, or next actions.
- Do not add repository content unrelated to the selected result.
- Do not expose credentials, host paths, or hidden provider context in either
  presentation path.

## Performance and capacity

The direct renderer must remain linear in the bounded result size. Adaptive
presentation adds no graph traversal, lifecycle evaluation, filesystem write,
or network dependency to `harnessctl`. Semantic fixture checks must operate on
bounded extracted fields rather than unrestricted natural-language inference.

## Observability

Tests and evidence must label the path as `structured`, `direct-exact`, or
`adaptive`. Evidence records the source result digest, the presentation mode,
the fields assessed, mismatches, and the selected next-step identity. It must
not label an agent response byte-exact unless it bypassed the model.

## Compatibility and migration

- Existing schema-2 JSON consumers require no migration.
- Existing direct human output remains deterministic and available.
- Managed agent instructions change from "return verbatim" to "preserve
  semantics and one next action."
- The candidate distribution changes first under a bounded work order. Root
  managed files remain unchanged until a later governed harness release and
  repository upgrade installs the new distribution.
- References to "canonical restitution" must distinguish canonical structured
  semantics from canonical direct human rendering.
- `REQ-WEX-009`, `SPEC-WEX-002`, `ARCH-WEX-002`, `ADR-WEX-002`, and
  `VER-WEX-002` remain historical evidence for the schema-2 implementation;
  this specification replaces only their verbatim-agent presentation rule.

## Examples and counterexamples

Conforming adaptive output may say:

> The draft for `WO-WEX-003` is complete, but it has not been approved and no
> implementation occurred. The repository owner must decide whether to approve
> it. Next, review that work order using the supplied response.

It need not print empty `Blocked by` or `Alternatives` headings.

Nonconforming output includes any response that:

- calls a draft work order approved;
- says tests passed when no test effect is recorded;
- omits a failed gate that blocks progress;
- asks an open-ended question instead of presenting the selected next action;
- recommends approval and implementation as two next actions; or
- changes, concatenates, or shell-interprets command arguments.

## Explicitly unspecified decisions

- Exact prose, heading choice, bullet style, and sentence order for adaptive
  handoffs.
- Provider-specific prompt wording when it remains a thin presentation adapter.
- Whether a host displays the structured source result alongside an adaptive
  explanation.
- Internal helper decomposition for tests that compare semantic fixtures.
