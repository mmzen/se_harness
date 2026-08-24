+++
id = "REQ-AEX-006"
type = "requirement"
title = "Orient an operator through a read-only portable skill"
status = "approved"
owners = ["product-owner", "requirements-steward", "technical-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN an operator asks a supported agent to understand an installed repository or one selected formal artifact, THE SYSTEM SHALL provide a read-only `harness-orient` skill that verifies installed integrity, validates and inspects the repository, focuses selected scope when supported, reports lifecycle state and blockers, identifies the next accountable decision point and required role, emits an execution receipt, and performs no repository, Git, lifecycle, or external mutation."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T09:03:54Z"
decided_by = "requirements-steward"
+++

# Requirement: Orient an operator through a read-only portable skill

## Rationale

Read-only orientation is a low-risk way to prove the skill boundary before
introducing delegated mutation or multi-agent writers. It also replaces a
common sequence of manual repository discovery, doctor, validation, inspection,
focus, and handoff interpretation with one outcome-oriented interaction.

## Preconditions and trigger

An operator explicitly invokes `harness-orient` or asks a supported agent for an
orientation task that unambiguously matches the skill description. The target
repository or selected artifact is supplied or safely discoverable.

## Required response

- Load applicable repository instructions and the complete skill procedure.
- Identify the repository root without resolving outside the supplied target.
- Run the exact released evaluator required for installed integrity when the
  repository declares one, and keep candidate-source observations separately
  labeled.
- Run supported read-only validation and inspection commands.
- When an artifact is selected and the evaluator supports it, project only the
  selected governing scope while retaining repository-wide blockers.
- Report current lifecycle state, selected scope, blockers, background
  observations, required accountable role, and one recommended next step.
- Emit a deterministic read-only execution receipt with no changed paths.

## Failure and boundary behavior

- Stop when managed integrity fails, repository context is incomplete, the
  graph is invalid, evaluator identity is unavailable, selection is ambiguous,
  or owner instructions materially conflict.
- Distinguish expected candidate-versus-released skew from authorization to
  repair or overwrite managed files.
- Do not scaffold, edit, transition, commit, fetch, push, tag, publish, deploy,
  operate, install an unapproved evaluator, or invoke credential-bearing tools.
- Do not recommend unrelated background maintenance as the selected task.

## Constraints

- The skill operates correctly without subagents, connectors, network access,
  or a hosted service.
- Optional parallel read-only exploration may be added later only if the final
  output and receipt remain equivalent.
- Human output is written for a technical expertise level appropriate to the
  repository audience; machine output remains canonical.
- The skill does not claim that reading occurred merely because a file appeared
  in a manifest.

## Acceptance examples

### Example: healthy installed consumer repository

**Given** a repository with intact managed content and a valid formal graph

**When** the operator invokes `harness-orient`

**Then** the skill reports the repository state and next decision, emits a
read-only receipt, and leaves all repository and Git bytes unchanged.

### Example: candidate source is not the evaluator

**Given** a source checkout whose candidate package is ahead of its locked
released evaluator

**When** the skill performs orientation

**Then** it uses or requests the exact external released evaluator for installed
integrity, labels candidate observations separately, and does not copy candidate
managed files into the root installation.

## Open decisions

Before approval, the specification must define the minimum command set for an
older supported evaluator that lacks newer focus or workflow-result interfaces,
and whether reduced orientation is supported or reported as an explicit
capability limitation.
