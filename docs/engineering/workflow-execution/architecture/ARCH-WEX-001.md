+++
id = "ARCH-WEX-001"
type = "architecture"
title = "Provider-neutral transactional workflow kernel"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
addresses = ["REQ-WEX-001", "REQ-WEX-002", "REQ-WEX-003", "REQ-WEX-004", "REQ-WEX-005"]
conforms_to = ["SPEC-WEX-001"]

[decision_assessment]
outcome = "adr_required"
triggers = ["system-boundary", "responsibility-or-dependency-direction", "public-interface-or-protocol", "data-ownership-or-persistence", "security-privacy-or-trust-boundary", "concurrency-consistency-reliability-or-failure-strategy", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "Moving lifecycle calculation from agent interpretation and manual edits into a shared kernel establishes a new authority-adjacent system boundary, public CLI and JSON interfaces, persistent lifecycle metadata, dependency direction, hostile-input boundary, atomic multi-file failure strategy, and cross-cutting workflow policy. Provider-specific Skills, a shared local kernel, and an external workflow service are material alternatives, while the public state and metadata contracts will be difficult to reverse once distributed."
assessed_by = "technical-owner"
+++

# Architecture: Provider-neutral transactional workflow kernel

## Lifecycle

Approved on 2026-08-20 through the technical owner's explicit acceptance of `ADR-WEX-001` and approval of this architecture. The decision authorizes the structural contract for bounded implementation under a separately approved work order; it grants no commit, assurance, release, or external authority.

## Context and scope

The harness already owns formal artifact parsing, snapshot validation, record preparation, and managed workflow policy, but agents still calculate scope, apply status changes, and compose next-step handoffs independently. This architecture moves those deterministic mechanics behind one local `harnessctl` boundary while keeping accountable decisions in formal artifacts and humans.

The scope begins with a selected formal ID or explicit transition packet and ends with a read-only focus result, a validated mutation plan, an atomically applied repository transaction, or a canonical handoff. It includes VREC/RLS preparation behavior and lifecycle metadata. It excludes trusted-base diff enforcement under rejected `REQ-WEX-006`, provider-specific Skill packaging, external services, commits, pushes, tags, publication, deployment, and human authority evaluation.

## Components and responsibilities

- The existing formal artifact parser and indexed graph own identity, type, status, relations, paths, and snapshot findings.
- The workflow scope projector owns bounded WO/VREC/RLS traversal and selected, repository-blocker, and background classification.
- The lifecycle policy registry owns allowed state edges, type-specific prerequisites, permitted fields, terminal states, and derived assurance/release projections.
- The workflow planner owns explicit packet selection, actor assertions, before/after state, complete in-memory rendering, and proposed-final-graph validation.
- VREC and RLS preparation adapters translate existing command inputs into the same workflow plan without acquiring decision authority.
- The transactional writer owns stale-input detection, repository-contained temporary files, atomic replacement, rollback, and exact-write reporting.
- The lifecycle metadata codec owns preparation fields, decision fields, append-only lifecycle events, legacy reads, and invariant checks.
- The next-step registry owns the closed mapping from final workflow result to one primary recommendation, authority, exact command or suggested response, and bounded alternatives.
- The `WorkflowResult` model is the only input to human and JSON renderers.
- CLI parsers and optional agent/Skill adapters are thin boundary layers; they own no scope, transition, or recommendation rules.

## Dependency direction

```text
CLI or optional agent adapter
  -> workflow application service
     -> formal artifact index + snapshot validator
     -> scope projector
     -> lifecycle policy registry
     -> planner + proposed-final-graph validation
        -> transactional writer only for explicit apply/preparation
     -> next-step registry
     -> WorkflowResult
        -> human renderer
        -> canonical JSON renderer
```

Formal state and managed policy flow into the kernel. The kernel emits plans, mutations, findings, and handoffs. Renderer wording, agent prose, Skill instructions, command success, and external actions never flow back as authority or lifecycle facts.

## Data and control flow

For `focus`, the application service resolves one typed identity, indexes relations, projects the bounded scope, classifies existing findings, calculates the next legal action, and renders one immutable result without invoking the writer.

For `transition`, the planner resolves every explicit `ID=STATUS` and actor assertion, obtains the exact input bytes, evaluates state edges and prerequisites, renders all candidate files in memory, validates the complete proposed graph, and emits a plan. `--apply` repeats the input comparison, stages all output outside discovery locations, replaces the exact planned set, rolls back on failure, validates the final snapshot, and renders the actual final result.

For record preparation, the existing public inputs are normalized into a single-record create plan after Git candidate identity, work scope, verification coverage, evidence, and release prerequisites are checked. Preparation provenance is written; accountable decision provenance is absent until a later explicit transition.

## Trust boundaries

Repository paths, files, formal metadata, IDs, relations, actor and reason text, evidence paths, Git observations, concurrent filesystem activity, and terminal capabilities are untrusted. The repository root and indexed pre-operation bytes form the bounded local input, not a trust claim. Path resolution, TOML rendering, JSON encoding, terminal rendering, and temporary-file promotion remain separate encoding boundaries.

The workflow kernel may record a supplied actor assertion but cannot authenticate the actor or judge whether the decision is substantively correct. Managed decision rights and explicit human instructions remain the authority boundary. The writer is authorized only by an explicit apply/preparation invocation and never performs Git or network side effects.

## Required patterns

- One provider-neutral workflow kernel shared by focus, transition, and record preparation.
- Typed immutable plan and result models between domain logic, writer, and renderers.
- Complete proposed-final-graph validation before mutation, including multi-artifact activation packets.
- Explicit plan/apply separation with stale-input detection and exact mutation reporting.
- Same-filesystem staging, bounded atomic replacement, digest-backed rollback, and no files staged in artifact discovery paths.
- A declarative lifecycle registry with verifier-owned black-box transition expectations.
- Separate preparation provenance, accountable decision provenance, and append-only lifecycle events.
- Derived assurance and release projections without related-status synchronization.
- One versioned semantic result rendered to human and JSON forms.
- Closed next-step mapping and exactly one primary recommendation.
- Legacy-read compatibility without automatic repository-owned migration.

## Prohibited patterns

- Provider-specific prompts, Skills, or conversation text implementing state-machine rules.
- Duplicated transition tables or next-step selection across CLI commands and renderers.
- Sequential writes that temporarily require the repository graph to be invalid.
- Writing before complete prerequisite and proposed-final-graph validation.
- Treating `--actor`, command availability, command success, Git authorship, or output text as proof of authority.
- Implicit WO changes during VREC decisions or implicit VREC/WO changes during RLS decisions.
- Decision timestamps or actors on merely prepared ready records.
- Arbitrary graph reachability as selected workflow scope.
- Trusted-base diff comparison, direct-edit enforcement, or CI transition history under this packet.
- A daemon, database, network API, plugin requirement, new runtime dependency, or installation profile.
- Commit, push, tag, pull-request, publication, deployment, or operational effects from workflow commands.

## Quality attributes

The architecture prioritizes determinism, auditability, atomicity, hostile-input safety, authority separation, repeatability across agent hosts, compatibility with historical records, explainable failure, portable standard-library execution, and concise human operation. It accepts a larger local domain model and new persistent metadata to eliminate provider-specific workflow behavior and partial state.

## Conformance checks

`VER-WEX-001` verifies exact bounded scope, state-edge coverage, whole-packet graph validation, no-partial-write behavior, failure injection, preparation/decision metadata separation, independent lifecycle planes, canonical human/JSON equivalence, hostile-input containment, compatibility, performance, distribution parity, and supported-agent adapter conformance. Architecture review additionally confirms that CLI parsers and renderers remain thin, one workflow kernel owns every rule, and rejected `REQ-WEX-006` has no implementation surface.

## Related ADRs

`ADR-WEX-001` proposes the provider-neutral transactional kernel, plan/apply mutation boundary, declarative lifecycle policy, and canonical result as one coherent significant decision. It must be accepted before this architecture or `WO-WEX-001` can be approved.
