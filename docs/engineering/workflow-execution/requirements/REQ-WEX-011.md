+++
id = "REQ-WEX-011"
type = "requirement"
title = "Preserve lifecycle semantics in adaptive human handoffs"
status = "approved"
owners = ["requirements-steward", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN a lifecycle stage completes or reaches a stop condition, THE SYSTEM SHALL make the schema-2 workflow result authoritative and permit an agent to present a clear human handoff only when it preserves every decision-relevant fact and exactly one recommended next action."
verification_method = "automated-test-and-human-review"

[relations]
derives_from = ["CAP-WEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T17:31:43Z"
decided_by = "requirements-steward"
+++

# Requirement: Preserve lifecycle semantics in adaptive human handoffs

## Rationale

`REQ-WEX-009` created a strong structured restitution and a deterministic human
renderer, but it also requires a supported agent to reproduce the rendered
block byte for byte. Repository instructions cannot enforce a model's final
bytes, and the fixed block is often a poor conversational answer even when it
is reproduced correctly. The useful guarantee is preservation of the governed
facts, authority boundary, and next action.

This requirement separates those concerns. The structured
`se-harness-workflow-result-v2` remains authoritative. Software may render an
exact block directly when exact bytes are needed. An agent may instead explain
the same result in clear language without becoming a second workflow engine.

This requirement refines only the agent-presentation portion of
`REQ-WEX-009`. It does not weaken that requirement's schema, observed-effect,
non-effect, blocker, lifecycle-state, decision, or single-next-action rules.

## Preconditions and trigger

- One selected lifecycle operation has completed, blocked, or reached a
  governed decision stop.
- The selected `harnessctl` operation has produced a valid schema-2 result.
- A consumer is preparing either a direct deterministic rendering or an
  agent-mediated human handoff.

## Required response

1. Treat the structured schema-2 result as the sole authority for the outcome,
   selected artifacts, effects, non-effects, blockers, lifecycle state,
   decision requirement, alternatives, and next procedure step.
2. Preserve actual artifact IDs and distinguish completed work from incomplete
   expected work.
3. Preserve every stated non-effect and blocker when either is material to what
   the user may safely believe or do next.
4. State the required accountable role and decision without implying that the
   agent exercised it.
5. Recommend exactly one next action and preserve the command's argument values
   or the suggested response's meaning.
6. Permit an agent to adapt wording, ordering, headings, and explanatory
   context to the user; omit empty fields; and show complete alternatives
   separately.
7. Require applications and automation needing exact bytes to call the
   deterministic renderer directly rather than ask a model to transcribe it.

## Failure and boundary behavior

- If a valid schema-2 result is unavailable, the consumer must stop and report
  that it cannot construct an authoritative lifecycle handoff.
- An agent must not invent an effect, decision, authority, blocker, artifact
  identity, alternative, or next action.
- An agent must not hide a failed predicate, changed lifecycle state, required
  decision, or safety-relevant non-effect to improve fluency.
- An agent must not turn incomplete work into a general backlog or add an
  unrelated repository inspection finding.
- When an exact rendered block is required, model-generated text is
  nonconforming even if it appears identical; the trusted renderer must produce
  the bytes.
- A presentation defect does not change the underlying lifecycle result or
  grant authority to continue.

## Constraints

- `se-harness-workflow-result-v2` and its restitution fields remain compatible.
- `harnessctl` remains the only component that computes lifecycle legality and
  the canonical next action.
- The existing deterministic human renderer remains a supported direct output.
- Semantic preservation does not mean verbatim transcription and does not
  require fixed prose headings in an agent reply.
- Relevant explanation may clarify a result but must not add a second proposed
  action or obscure the selected recommendation.
- Provider-specific prompts or Skills may adapt presentation only; they must
  not redefine result semantics.

## Acceptance examples

### Example: clear adaptive handoff

**Given** schema-2 reports that `WO-WEX-003` remains `draft`, no implementation
occurred, repository-owner approval is required, and one review action is next

**When** an agent responds to a user

**Then** it may say, "The draft packet is ready for repository-owner review;
no policy or implementation changed. Next, review `WO-WEX-003` for approval,"
and include the exact suggested response without reproducing empty headings.

### Example: direct exact rendering

**Given** a terminal integration requires the standard heading block for a
snapshot or parser

**When** it requests human output

**Then** the application invokes the deterministic schema-2 renderer directly
and uses those bytes without model transcription.

### Example: semantic mismatch

**Given** the result says `WO-WEX-003` is `draft` and requires
repository-owner approval

**When** an agent says implementation may start or omits the approval decision

**Then** the handoff fails conformance even if the prose uses the standard
headings.

### Example: harmless presentation change

**Given** `blocked_by` and `alternatives` are empty

**When** an agent omits those empty sections, leads with the outcome, and
combines the state and decision in one sentence

**Then** the handoff remains conforming when all decision-relevant facts and the
single next action are preserved.

## Open decisions

Before approval, the product, technical, and quality owners must confirm the
closed semantic-preservation matrix in `SPEC-WEX-003`, including which
non-effects are material, how exact command arguments are displayed, and the
supported boundary between direct rendering and agent-mediated presentation.
