+++
id = "ARCH-WEX-003"
type = "architecture"
title = "Separate lifecycle semantics from human presentation"
status = "approved"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
addresses = ["REQ-WEX-011"]
conforms_to = ["SPEC-WEX-003"]

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "public-interface-or-protocol", "cross-cutting-policy", "material-alternatives"]
rationale = "The change moves exactness from model behavior to a direct renderer, defines two public presentation paths over one authoritative result, and alters cross-cutting instructions for every supported agent adapter."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T17:31:43Z"
decided_by = "technical-owner"
+++

# Architecture: Separate lifecycle semantics from human presentation

## Context and scope

The workflow kernel already emits a typed schema-2 result and has a
deterministic human renderer. Managed instructions currently collapse three
responsibilities into one rule: compute lifecycle facts, render exact bytes,
and make a model repeat those bytes. The first two are software-enforceable;
the third is neither reliably enforceable nor consistently useful to a human.

This architecture keeps one authoritative result and separates presentation
into a deterministic software path and an adaptive agent path. It applies to
selected lifecycle handoffs only. It does not change lifecycle computation,
formal state, gate evaluation, or authority.

## Components and responsibilities

### Workflow result producer

- Computes the selected workflow result, effects, non-effects, blockers,
  lifecycle state, decision, and one next procedure step.
- Emits and validates `se-harness-workflow-result-v2`.
- Does not optimize wording for a provider or user.

### Direct exact renderer

- Accepts only a validated schema-2 result.
- Produces the deterministic existing heading block.
- Serves terminals, snapshots, documentation, and format-dependent consumers.
- Does not call a model or parse agent prose.

### Adaptive presentation adapter

- Consumes the structured result, not rendered prose.
- Selects wording and layout appropriate to the interaction.
- Preserves the semantic-fidelity matrix and one recommended next action.
- Does not compute legality, choose another procedure, or exercise authority.

### Conformance fixtures

- Bind a structured source result to required semantic facts.
- Include allowed paraphrase and omission examples plus forbidden mismatches.
- Test direct rendering by exact output and adaptive presentation by semantic
  preservation.

### Managed instruction distribution

- Describes the two paths consistently in the candidate standard templates.
- Avoids claims that repository text enforces unsupported host behavior.
- Leaves root managed files unchanged until a governed release and upgrade.

## Dependency direction

```text
workflow policy + formal graph
            |
            v
validated schema-2 result
       /                 \
      v                   v
direct exact renderer   adaptive presentation adapter
      |                   |
      v                   v
exact human bytes       clear semantic-fidelity handoff
```

Both presentation paths depend on the structured result. Neither path feeds
facts, decisions, or recommendations back into the workflow kernel. The
adaptive path must not depend on parsing the direct human rendering.

## Data and control flow

1. A selected `harnessctl` operation computes and validates schema-2.
2. The consumer selects a presentation mode.
3. For `direct-exact`, trusted code calls the deterministic renderer and emits
   its bytes unchanged.
4. For `adaptive`, the adapter supplies the structured semantic projection to
   the agent with the preservation constraints.
5. The resulting presentation has no lifecycle effect. Accountable decisions
   still enter through existing transition procedures.

## Trust boundaries

- The structured workflow result and trusted direct renderer are inside the
  lifecycle presentation trust boundary.
- Agent prose is outside the lifecycle authority boundary, even when it is a
  conforming explanation.
- Repository and artifact text embedded in fields is untrusted display data.
- Provider-specific prompts, Skills, and UI transformations are adapters, not
  policy owners.
- A format-dependent consumer trusts only direct renderer output, never a
  visual imitation returned by a model.

## Required patterns

- One validated semantic source for both presentation paths.
- Explicit mode selection by the consuming application or interaction.
- Closed comparison of identifiers, states, decisions, blockers, argument
  arrays, and next-step identity.
- Exact tests for direct rendering and semantic positive/negative fixtures for
  adaptive handoffs.
- Managed template changes before any root managed upgrade.
- Clear non-effect language when omission could imply approval, transition,
  verification, release, Git, publication, deployment, or external action.

## Prohibited patterns

- Parsing rendered prose to recover lifecycle authority.
- Asking a language model to provide byte-for-byte enforcement.
- Letting an adaptive adapter compute or replace the selected next action.
- Using fixed headings as evidence that semantics are correct.
- Treating fluent prose as an approval or lifecycle event.
- Adding a network model call or natural-language verifier to `harnessctl`.
- Editing the installed root managed policy during candidate implementation.

## Quality attributes

- **Correctness:** identifiers, lifecycle facts, authority, and next action
  remain traceable to schema-2.
- **Clarity:** human replies can lead with the outcome and omit empty ceremony.
- **Determinism:** exact consumers retain direct deterministic rendering.
- **Provider neutrality:** no provider becomes the workflow rule engine.
- **Auditability:** source result and presentation mode are separately labeled.
- **Compatibility:** schema-2 and current direct renderer remain stable.
- **Safety:** presentation cannot grant authority or hide a blocking condition.

## Conformance checks

- Validate that every candidate managed instruction names schema-2 as
  authoritative and does not require model transcription.
- Confirm direct renderer snapshots remain deterministic.
- Confirm positive adaptive cases may reorder, paraphrase, merge, and omit empty
  fields.
- Confirm negative cases fail on changed IDs, states, outcomes, blockers,
  decision roles, commands, non-effects, or next actions.
- Confirm no adaptive component is imported by the workflow kernel and no
  network or natural-language parser is added.
- Confirm fresh installations contain the candidate instructions while the
  current root managed bytes remain untouched.

## Related ADRs

`ADR-WEX-003` decides the responsibility boundary and selects semantic fidelity
plus direct exact rendering over both verbatim model transcription and
unconstrained prose.
