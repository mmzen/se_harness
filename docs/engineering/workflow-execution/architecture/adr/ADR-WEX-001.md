+++
id = "ADR-WEX-001"
type = "adr"
title = "Provider-neutral transactional workflow kernel"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
decides = ["ARCH-WEX-001"]
+++

# ADR: Provider-neutral transactional workflow kernel

## Status

Accepted on 2026-08-20 through the technical owner's explicit instruction `I accept ADR-WEX-001`. Acceptance decides `ARCH-WEX-001`; it does not itself authorize implementation or any Git, assurance, release, or external action.

## Context

The harness supplies common prose, artifact schemas, snapshot validation, and preparation commands, yet coding agents still interpret lifecycle preconditions, edit statuses, decide related mutations, choose working scope, and compose handoffs themselves. That produces materially different behavior across ChatGPT, Claude, Codex, and future hosts. It also makes mutually dependent approvals awkward because sequential edits can create an invalid intermediate graph.

`SPEC-WEX-001` requires a selected-scope projection, atomic multi-artifact lifecycle operation, independent WO/VREC/RLS planes, honest preparation and decision metadata, and one canonical human/machine handoff. These responsibilities need a stable ownership and dependency boundary before implementation.

## Decision drivers

- The same repository state and explicit decision must yield the same scope, plan, result, and next action across supported agents.
- Formal artifacts and human decisions must remain authoritative; automation must not infer or acquire accountability.
- Whole-packet activation must validate without transient invalid graph states or partial writes.
- VREC and RLS preparation and later decisions must use the same lifecycle rules without coupled related-record mutation.
- Human and JSON output must express one semantic result.
- Repository content and paths are untrusted, and runtime behavior must remain Python 3.11+ standard-library only.
- Historical repository-owned records must remain readable without automatic rewrite.
- Skills may improve discovery and presentation but cannot be the enforcement layer.

## Considered options

### Option A — Keep prose-driven agent workflow and snapshot validation

Continue documenting transitions and allow each agent to edit artifacts directly, then run whole-graph validation. This is the smallest implementation but retains the observed provider divergence, approval sequencing failures, inconsistent handoffs, and partial-write risk.

### Option B — Encode workflow separately in provider-specific Skills and prompts

Give each supported agent a detailed Skill or instruction package. This improves ergonomics but duplicates state rules across hosts, depends on activation and model compliance, makes parity difficult to prove, and lets presentation layers drift into authority-adjacent behavior.

### Option C — Add one local transactional workflow kernel to `harnessctl`

Centralize scope projection, lifecycle policy, planning, proposed-final-graph validation, atomic application, metadata rules, and next-step selection in a provider-neutral standard-library domain layer. Keep CLI commands, renderers, and optional Skills thin. This adds a substantive local API and metadata contract but gives every host the same executable semantics.

### Option D — Introduce an external workflow service or governance database

Move state and transitions behind a hosted service. This could provide identity and concurrency controls, but it replaces repository-native authority, adds deployment and network dependencies, complicates offline use and adoption, and conflicts with the single portable installation.

## Decision

Choose Option C.

Implement one local provider-neutral workflow kernel inside the `se_harness` package. The kernel consumes the existing formal artifact index and snapshot validator; owns bounded scope projection, a declarative transition/precondition registry, preparation rules, complete in-memory packet planning, stale-state checks, transaction application and rollback, lifecycle metadata invariants, derived assurance/release projections, and the closed next-step registry; and produces one immutable versioned `WorkflowResult`.

Expose the kernel through additive `focus` and `transition` CLI commands and route existing VREC/RLS preparation commands through the same planning boundary. Transition is plan-only by default and mutates only with explicit `--apply`. A transaction may select several artifacts so the final graph can be validated and applied atomically; every artifact, target state, and actor assertion remains explicit.

Render human and JSON forms only from `WorkflowResult`. Agent entry files and future Skills may call the CLI and render or summarize its fields, but they must not contain an independent transition table, scope algorithm, or recommendation policy.

Retain repository-native formal artifacts as authoritative state. Record preparation and decision provenance as defined by `SPEC-WEX-001`, preserve unchanged legacy records, and make no automatic migration. Do not implement trusted-base diff enforcement from rejected `REQ-WEX-006` in this decision.

## Consequences

### Positive

- Supported agents converge on one scope, transition plan, mutation set, validation result, and primary next action.
- Multi-artifact approvals and completion can be validated against one proposed final graph and applied without invalid intermediate states.
- VREC/RLS preparation and decisions share enforceable preconditions and independent lifecycle-plane behavior.
- Canonical JSON supports deterministic adapter and regression testing while the human form remains concise.
- Skills become small optional UX adapters rather than duplicated governance engines.

### Negative and operational

- The package gains a nontrivial state-machine, transaction writer, public CLI, JSON schema, and persistent metadata surface that must remain compatible.
- Existing preparation behavior becomes stricter and can reject repositories that relied on states broader than managed workflow policy.
- Atomic multi-file behavior and rollback require extensive cross-platform failure testing and careful concurrent-change handling.
- Definition and record templates, validator rules, managed copies, documentation, and public examples must change together.

### Security and trust

- Centralization reduces prompt-driven mutation risk but makes the kernel and writer a high-value boundary for traversal, injection, symlink, concurrency, and rollback defects.
- Actor assertions remain unauthenticated repository facts; callers and accountable owners must not treat command success as proof of authority.
- No network, service, plugin, Git write, or external side effect is added.

### Migration

- Unchanged legacy artifacts remain readable without lifecycle events or separated preparation fields.
- A later governed transition can add the new metadata required for that target while preserving captured facts.
- No installer or upgrade operation rewrites repository-owned historical artifacts.
- Trusted-base direct-edit enforcement, if later needed, requires a separate requirement and architecture reassessment.

## Validation

- Run all independent cases in `VER-WEX-001`, including black-box public CLI scenarios and verifier-owned lifecycle expectations.
- Prove CLI parsers, preparation adapters, and renderers delegate to one kernel and contain no duplicate transition or next-step tables.
- Prove complete packet planning and final-graph validation occur before writes.
- Inject failure and concurrent change at every transaction boundary and compare complete repository digests with the pre-operation state.
- Verify exact WO/VREC/RLS scope projections, status independence, metadata timing, immutable provenance, and legacy behavior.
- Compare canonical JSON and human semantics across supported runtimes and agent adapters.
- Confirm fresh-install, upgrade, managed integrity, package data, root/template parity, preflight, and full repository tests.
- Confirm no source, tests, help, templates, or work-order scope implement rejected `REQ-WEX-006`.
