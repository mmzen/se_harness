+++
id = "ADR-AEX-001"
type = "adr"
title = "Harness-owned authority with non-authoritative skills and runtime adapters"
status = "approved"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
decides = ["ARCH-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T09:03:54Z"
decided_by = "technical-owner"
+++

# ADR: Harness-owned authority with non-authoritative skills and runtime adapters

## Status

Option D was accepted during accountable technical-owner content review. The
authoritative lifecycle state remains the front-matter `status` and lifecycle
events.

## Context

SE Harness needs a more direct, outcome-oriented way for agents to operate its
workflow. Skills can package reusable procedures and subagents can provide
specialized contexts or parallel execution. Provider-specific agent
configuration can select models, tools, permissions, and integrations.

If any of those layers becomes authoritative, lifecycle legality and decision
rights would vary by runtime and could drift from managed policy. If the harness
ignores them entirely, operators continue supervising procedural command
sequences and lose the main benefit of agentic execution.

## Decision drivers

- Preserve explicit accountable decision rights.
- Keep the released evaluator and formal artifact graph authoritative.
- Make common workflows usable as outcome-oriented skills.
- Support more than one runtime and a deterministic single-agent fallback.
- Prevent runtime permissions or agent names from being mistaken for authority.
- Version and verify trusted execution inputs without treating them as product
  intent.
- Allow runtime formats to evolve without rewriting formal engineering state.

## Considered options

### Option A: encode workflow and authority in skills

Skills would contain complete lifecycle rules and decide which transitions an
agent may perform. This is easy to prototype but creates a second rule source,
drifts from the evaluator, and makes natural-language procedure text an
authority boundary.

### Option B: encode authority in runtime agent definitions

Specialized runtime agents would be configured as implementer, verifier, or
release roles. This uses strong runtime controls but conflates job description,
technical permission, and accountable decision right, while binding the product
to vendor-specific formats.

### Option C: use a hosted orchestration authority

A service would own agent routing, workflow state, and authorization. This could
centralize operations but adds a service, trust boundary, dependency, identity
model, and availability requirement contrary to the repository-native and
standard-library product boundary.

### Option D: retain authority in the harness and make skills and adapters thin

The formal graph, managed policy, machine-readable workflow, gates, mutation
guard, and released evaluator remain authoritative. Skills package procedures;
profiles describe workers; adapters translate provider-specific execution
configuration; receipts and packets return evidence and decisions to the
harness boundary.

## Decision

Choose Option D.

- The authority plane remains the only source of lifecycle legality and managed
  decision-right requirements.
- Portable skills query the harness and cannot override it.
- Logical execution profiles describe worker behavior but hold no accountable
  authority by themselves.
- Runtime adapters produce derived configuration with explicit ownership and
  provenance.
- Managed integrity may protect skill and adapter inputs without making their
  content product authority.
- Command-driven and single-agent execution remain correctness-preserving
  fallbacks.
- The pilot has one canonical portable source at
  `templates/repository/standard/.agents/skills/harness-orient/`, installed as
  managed content at `.agents/skills/harness-orient/`; it is not duplicated
  under `se_harness/skills/`.
- The retained `skill-contract.json` and canonical portable-core manifest bind
  skill identity. Provider-specific overlays remain outside that digest and
  bind it separately.
- Decision packets remain a separate lossless projection of the canonical
  workflow result, while execution receipts use their own canonical evidence
  schema. Neither can change formal state.

## Consequences

### Positive

- Authority remains provider-neutral and consistent with existing SE Harness
  guarantees.
- Skills can improve usability without becoming a second state machine.
- Runtime integrations can evolve independently and degrade safely.
- The distinction between accountable owner, worker, procedure, scope, and
  permission becomes testable.

### Negative

- Skills depend on stable machine-readable harness interfaces.
- Adapter development requires explicit conformance testing per runtime.
- Some runtime-native convenience features cannot be treated as reliable across
  all supported environments.
- Managed skill distribution expands installer, package-data, integrity, and
  upgrade surfaces.
- The selected `.agents/skills/` location is a portable repository convention,
  but runtimes that do not discover it require an explicit later adapter or
  direct invocation; this does not weaken the single-agent procedure.

### Operational

- Repositories need safe skill installation and upgrades separate from package
  installation.
- Package and source distributions must carry the nested canonical skill files
  exactly once, and the standard installer must treat the target copy as
  managed content with customization conflict detection.
- Operators need clear diagnostics when the exact evaluator or runtime feature
  is unavailable.
- Adapter manifests and skill digests add retained provenance data.

### Security

- Supporting scripts and generated runtime configuration become supply-chain
  inputs requiring strict integrity, path, permission, and hostile-input tests.
- Runtime permissions remain defense-in-depth; the harness must still deny
  unauthorized governed operations.

### Migration

- Existing repositories remain command-driven until an explicit supported
  installation or upgrade adds skills.
- A managed upgrade may add the canonical skill only after its exact plan is
  reviewed; customized content at the target location blocks rather than being
  adopted or overwritten.
- Existing formal artifacts are not rewritten automatically.
- Provider-specific configurations remain owner-controlled unless a later
  approved adapter transaction establishes bounded ownership.

## Validation

- Inspect every skill, profile, and adapter for duplicated lifecycle rules or
  accountable-role claims.
- Run a common conformance corpus through command-driven and skill-driven paths.
- Prove that modified skill prose cannot make a prohibited transition pass.
- Prove that runtime workspace-write permission cannot bypass work-order,
  envelope, evaluator, or gate checks.
- Verify safe install, replay, upgrade, customization conflict, and rollback for
  managed skill and adapter inputs.
