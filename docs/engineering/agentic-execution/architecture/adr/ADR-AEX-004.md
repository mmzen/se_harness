+++
id = "ADR-AEX-004"
type = "adr"
title = "Thin state-gated skills over existing harness operations"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
decides = ["ARCH-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T13:50:24Z"
decided_by = "technical-owner"
+++

# ADR: Thin state-gated skills over existing harness operations

## Status

Proposed.

## Context

The approved architecture keeps authority in the harness, establishes a
single-agent baseline, and treats skills as portable procedure packages. Phase
1 delivered only `harness-orient`. Phase 2 delivered pure contract validation
but deliberately did not connect autonomy envelopes to effects.

Phase 3 needs three writing skills. The design must decide whether those skills
become a new workflow engine, add a general mutating API, or compose existing
released-evaluator operations and current human decision points. The decision
must also preserve the exact v1 orientation skill and leave stronger delegated
runtime enforcement to Phase 4.

## Decision drivers

- Keep lifecycle legality and accountable roles in one managed authority plane.
- Deliver a usable single-agent MVP against the existing public harness
  procedures.
- Prevent implicit activation from causing writes.
- Preserve exact released-evaluator and candidate-source separation.
- Make helper-controlled boundaries deterministic and adversarially testable.
- Preserve one canonical managed source for each portable skill.
- Avoid adding Phase 4 autonomy, Phase 5 orchestration, or Phase 6 adapters.

## Considered options

### Option A — encode complete workflow logic in each skill

Each skill would describe lifecycle states, roles, gates, transitions, and
recovery in `SKILL.md` and invoke repository tools directly.

This is easy to prototype but creates duplicate authority sources, makes skill
drift likely, and cannot guarantee equivalence with changing managed policy.

### Option B — add one general autonomous skill runner now

A new harness runner would derive autonomy envelopes, admit arbitrary
operations, execute writes, apply eligible lifecycle transitions, and return
receipts.

This could reduce more prompts, but it crosses the explicitly deferred Phase 4
delegation boundary and requires managed decision-right and effect-enforcement
work beyond the Phase 3 MVP.

### Option C — use provider-native agents and permission files

Each supported runtime would receive native agent definitions, tool allowlists,
and hooks for the three outcomes.

This makes one runtime's configuration a hidden semantic dependency, does not
create engineering authority, and begins the runtime-adapter phase before the
single-agent procedure is stable.

### Option D — compose thin state-gated skills over existing harness operations

Each portable skill validates its managed contract, invokes the exact released
evaluator for current structured state and existing preparation operations,
uses an explicit closed effect plan, and stops at current decision points. The
writing skills require explicit activation and never apply lifecycle
transitions. `harness-orient` remains unchanged.

This provides the intended user experience while keeping authority and
decision timing unchanged.

## Decision

Choose Option D, subject to approval of this ADR, `REQ-AEX-008`,
`SPEC-AEX-004`, `VER-AEX-002`, and `WO-AEX-003`.

The Phase 3 architecture uses four outcome-oriented portable skills. The three
new skills use strict `se-harness-skill-contract-v2`; `harness-orient` remains
on its exact v1 contract. Every writing skill is explicit-activation-only and
uses a structured released-evaluator launcher.

The procedure has three control boundaries:

1. **Harness-derived state.** The exact released evaluator supplies current
   integrity, graph, selected lifecycle state, applicable checkpoint, gates,
   role, and next action.
2. **Skill-owned effect plan.** The skill selects only the effect classes and
   path source closed by `SPEC-AEX-004`. The plan is procedural evidence and
   grants no authority.
3. **Repository effect and post-check.** The released evaluator performs draft
   and VREC preparation through existing guarded operations. An implementation
   agent changes only the already-started work order's execution scope. The
   skill compares actual paths and reruns applicable checks before handoff.

No Phase 3 skill applies an existing artifact's lifecycle transition.
`harness-draft-change` stops with drafts. `harness-execute-work-order` requires
`in_progress` and stops before completion. `harness-prepare-assurance` uses the
existing preparation operation to create `ready` and stops before verification.

The canonical source for each skill remains under
`templates/repository/standard/.agents/skills/`. Standard installation manages
the installed `.agents/skills/` bytes. Distribution metadata lists every
canonical core exactly once, and no source copy is added under
`se_harness/skills/`.

This decision does not claim hard enforcement against an agent runtime that
ignores a skill. Phase 3 verifies the portable procedure, managed installed
bytes, command equivalence, and every bundled helper-controlled boundary.
Autonomy-envelope-backed effect admission and runtime permission mapping need
separate Phase 4 authority.

## Consequences

### Positive

- Operators work in outcomes instead of assembling routine command sequences.
- Existing lifecycle and authority semantics remain unchanged.
- Writing skills cannot activate implicitly.
- v1 consumers and the verified orientation skill remain stable.
- Single-agent behavior becomes a deterministic baseline for later delegation
  and orchestration.
- Existing released-evaluator mutation guards remain on formal draft and VREC
  preparation operations.

### Negative

- Phase 3 still pauses for work start, work completion, assurance verification,
  delivery choice, and external actions.
- Arbitrary implementation edits are governed by the work order and skill
  procedure but are not yet mediated by an evaluator-derived autonomy-envelope
  effect API.
- Three additional managed skill packages enlarge installation and distribution
  surfaces.
- Exact pre- and post-checks add runtime cost.

### Operational

- Validate skill contract and digest before any bundled helper.
- Invoke evaluator operations through argument arrays and structured output.
- Recheck state immediately before a controlled effect.
- Retain only declared evidence and deterministic digests.
- Stop on stale state, unexpected paths, failed gates, or missing authority.
- Require a new approved work order before adding lifecycle automation,
  subagents, runtime overlays, or external actions.

### Security

- Treat skill bytes, repository content, paths, JSON, commands, Git facts, and
  evidence as untrusted.
- Deny implicit writes, shell command strings, path escapes, scope widening,
  secret retention, and candidate-as-governor execution.
- Do not present runtime permissions or effect-plan success as authority.
- Make helper effects injectable in tests so rejected cases prove zero callback
  invocation.
- Report unexpected existing changes without deleting user content.

### Migration

- Preserve `harness-orient` v1 byte and semantic identity.
- Introduce v2 parsing alongside v1 rather than changing v1 meaning.
- Add new skill cores through the existing ownership-aware installer and
  managed lock.
- Existing repositories receive the skills only through a later authorized
  harness upgrade.
- Phase 4 extends, rather than reinterprets, this baseline with separately
  approved autonomy-envelope admission.

## Validation

Architecture conformance is checked through `VER-AEX-001` for portable skill,
authority, receipt, decision-point, and evaluator-boundary invariants and
through `VER-AEX-002` for the Phase 3 workflow delta. Verification must prove:

- exact v1 orientation identity and behavior are unchanged;
- all three v2 instances reject implicit activation and invalid scope before a
  helper effect callback;
- command and skill fixtures have equivalent lifecycle effects and stops;
- no skill applies a lifecycle transition or Git/external mutation;
- standard install, safe upgrade, source distribution, and wheel each contain
  one canonical copy of all four skills;
- `harness-execute-work-order` writes only for an `in_progress` selection and
  detects every unexpected changed path;
- assurance preparation produces only one exact-candidate `ready` VREC and
  stops before assurance; and
- the same complete behavior works with one agent and no provider-specific
  files.
