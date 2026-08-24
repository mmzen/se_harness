+++
id = "REQ-AEX-005"
type = "requirement"
title = "Expose governed workflows through portable outcome-oriented skills"
status = "approved"
owners = ["product-owner", "requirements-steward", "technical-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN a supported agent invokes an SE Harness workflow through a skill, THE SYSTEM SHALL provide a portable outcome-oriented skill contract that declares trigger scope, preconditions, required inputs, harness checkpoints, mutation class, evidence obligations, structured outputs, escalation conditions, and fallback behavior; and SHALL derive lifecycle legality from machine-readable harness contracts rather than skill prose or runtime-specific configuration."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T09:03:54Z"
decided_by = "requirements-steward"
+++

# Requirement: Expose governed workflows through portable outcome-oriented skills

## Rationale

Skills can make the harness easier to use and allow agents to execute complete
outcomes instead of requiring operators to remember individual commands.
Portability is limited, however, if the core skill depends on one runtime's tool
names, permission syntax, subagent representation, or implicit behavior.

## Preconditions and trigger

A supported agent discovers or explicitly invokes an SE Harness skill for a
repository workflow.

## Required response

- Use a versioned portable core with a `SKILL.md` and only explicitly declared
  supporting scripts, references, and assets.
- Describe one recognizable engineering outcome rather than expose every CLI
  command as an independent top-level skill.
- Declare when the skill must and must not activate.
- Declare read-only, draft-writing, governed-mutation, or external-action
  behavior before execution.
- Query current harness state and procedure contracts through supported
  machine-readable interfaces.
- Preserve the harness's selected scope, gate, decision-right, and stop
  semantics.
- Produce a structured result and single-agent fallback independent of optional
  subagent support.

## Failure and boundary behavior

- A missing, damaged, ambiguous, disabled, unsupported, or digest-mismatched
  skill fails explicitly or falls back to the documented command-driven
  procedure; it does not bypass a gate.
- Implicit activation cannot authorize a governed mutation.
- A skill cannot add a permitted transition, reinterpret a decision role, or
  weaken a failed gate.
- Runtime-specific metadata may narrow tools or improve discovery but cannot
  change the portable procedure's governed effects.

## Constraints

- Managed skill integrity does not make skill prose a source of product
  authority.
- Supporting scripts are executable supply-chain inputs and require the same
  safe-path, integrity, hostile-input, and deterministic-failure treatment as
  other trusted tooling.
- Large skill catalogs must avoid ambiguous names and overlapping trigger
  descriptions.
- Distribution and upgrades preserve repository-owned customization and fail on
  ambiguous ownership.

## Acceptance examples

### Example: runtime lacks subagents

**Given** a supported runtime that can load the portable skill but cannot spawn
subagents

**When** the skill is invoked

**Then** it executes the same governed procedure through one agent and produces
the same authority boundary and structured outcome.

### Example: skill prose conflicts with workflow

**Given** a skill instruction that recommends a transition prohibited by the
current machine-readable workflow contract

**When** the skill attempts the transition

**Then** the harness rejects it and reports the conflict; the skill does not
become an alternate rule source.

## Open decisions

Before approval, the technical design must define the portable core, canonical
repository location, distribution ownership mode, content digest binding, and
the minimum supported runtime conformance profile.
