+++
id = "ADR-WEX-003"
type = "adr"
title = "Semantic fidelity for agents and direct rendering for exact consumers"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
decides = ["ARCH-WEX-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T17:31:43Z"
decided_by = "technical-owner"
+++

# ADR: Semantic fidelity for agents and direct rendering for exact consumers

## Status

Proposed.

## Context

The current policy requires agents to return a canonical human restitution
block verbatim. The schema and renderer are deterministic, but the final answer
is produced by an external model host. Repository instructions can request a
format; they cannot prove or enforce exact final bytes. When followed, the
fixed block also prevents useful explanation and often produces an awkward
answer.

The underlying lifecycle facts must remain strict. Operators still need a
single authoritative state, accountable decision, and next action. Some
software integrations also legitimately need deterministic text.

## Decision drivers

- Preserve lifecycle and authority semantics without relying on model wording.
- Improve clarity for humans at different technical levels.
- Keep deterministic output for terminals and format-dependent consumers.
- Avoid a schema migration or duplicate workflow engine.
- Make the claimed enforcement boundary truthful and testable.
- Keep provider-specific adapters thin and non-authoritative.

## Considered options

### Option A: Continue verbatim model transcription

Keep the existing instruction and exact heading tests. This preserves one
visible format but cannot enforce final host output, judges headings rather
than truth, and blocks concise contextual explanations.

### Option B: Semantic fidelity plus direct exact rendering

Keep schema-2 and its direct deterministic renderer. Require agent adapters to
preserve a closed set of decision-relevant semantics and one next action while
allowing presentation changes. Require exact consumers to invoke the renderer
without a model in the path.

### Option C: Unconstrained agent prose

Let each provider summarize freely. This improves flexibility but makes it too
easy to omit blockers, authority, non-effects, or the selected next action and
would create provider-specific workflow behavior.

### Option D: Add a natural-language conformance judge to the trusted kernel

Use another model or heuristic parser to score every final answer. This adds
non-determinism, cost, privacy and availability concerns, and a circular trust
boundary without proving exact preservation.

## Decision

Select Option B.

`se-harness-workflow-result-v2` remains the semantic authority and the existing
direct renderer remains the exact human-output implementation. Agent-facing
policy will require semantic fidelity rather than verbatim reproduction. The
semantic contract closes identifiers, outcome, effects, material non-effects,
blockers, lifecycle state, accountable decision, alternatives, exact command
arguments or suggested-response meaning, and exactly one recommended next
step.

An application requiring exact text must call the renderer directly. A model's
imitation is not exact-rendering evidence. Agent prose remains explanatory and
never becomes a lifecycle decision or alternative rule engine.

## Consequences

### Positive

- Human answers can be concise, contextual, and easier to understand.
- The strict guarantees attach to structured facts instead of fragile prose.
- Deterministic integrations retain their current output.
- No schema-2 migration or new runtime service is required.
- The policy no longer claims enforcement that the repository cannot provide.

### Negative

- Adaptive output will vary across providers and runs.
- Full natural-language equivalence cannot be mechanically proven for every
  unsupported host.
- Tests must distinguish direct byte rendering from adaptive semantic cases.
- Reviewers must reason about when a non-effect is material to a safe handoff.

### Operational

- Managed candidate templates and their instruction tests must change
  together.
- Existing direct renderer tests remain and are relabeled as renderer
  guarantees, not agent-final-answer guarantees.
- Freshly installed repositories receive the policy only after a released
  distribution and governed upgrade.

### Security

- The structured result remains the only trusted source.
- Command argument arrays must not be flattened into executable shell strings.
- Untrusted artifact text cannot add decisions or next actions.
- No network, model dependency, or natural-language evaluator enters the
  trusted CLI.

### Migration

- Existing machine consumers and direct human consumers remain compatible.
- Agent adapters remove verbatim-output language and adopt the semantic matrix.
- Documentation must distinguish "canonical structured result" from
  "deterministic direct rendering."

## Validation

`VER-WEX-003` will verify schema and renderer compatibility, candidate managed
instruction consistency, positive adaptive transformations, negative semantic
mismatches, fresh-install behavior, unchanged root managed bytes, absence of a
new network or natural-language trusted component, and explicit user review of
representative Claude Code and Codex handoffs.
