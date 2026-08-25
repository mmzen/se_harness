+++
id = "ADR-AUT-001"
type = "adr"
title = "Put authoring rules in a managed policy and the validator, not in per-type skills"
status = "draft"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
decides = ["ARCH-AUT-001"]
+++

# ADR: Put authoring rules in a managed policy and the validator, not in per-type skills

## Status

Proposed.

## Context

The owner asked whether a dedicated skill should write requirements, and
the same for other artifact types. The repository already decided the
analogous question for communication rules (`ADR-TCM-001`).

## Decision drivers

- Rules must apply on every route, not only when a skill is invoked.
- Mechanical rules must be predicates; the directive-surface review showed
  prose rules are unmeasured.
- Reading surface must not grow; `WO-ADS-002` bounded it.
- One owner per subject; skills are non-authoritative consumers.

## Considered options

### Option A: managed policy + validator + existing skill (chosen)
One policy file, checklists printed by `create-artifact`, mechanical rules in
the validator and two gate predicates, one sentence in `harness-draft-change`.

### Option B: a skill per artifact type
Five to twelve new cores, contracts, digests, adapters, and tests, each
restating a procedure that already exists and differing only in content
advice; rules unenforced outside the skill.

### Option C: rules only in templates
Discoverable at creation, invisible afterwards, unenforced, and silently
outdated in every existing artifact.

### Option D: an elicitation skill
Deferred: a different procedure (dialogue to candidates), justified only if
elicitation proves to be a recurring distinct activity.

## Decision

Option A. Revisit D on evidence.

## Consequences

- `verification_method` changes type; a migration work order follows.
- Two new warning families and one evaluator key.
- The policy joins the managed set and reaches this repository's root at the
  next released-evaluator upgrade.
