+++
id = "ARCH-AEX-001"
type = "architecture"
title = "Harness-owned authority with replaceable agent execution planes"
status = "approved"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
addresses = ["REQ-AEX-001", "REQ-AEX-002", "REQ-AEX-003", "REQ-AEX-004", "REQ-AEX-005", "REQ-AEX-006", "REQ-AEX-007"]
conforms_to = ["SPEC-AEX-001", "SPEC-AEX-002"]

[decision_assessment]
outcome = "adr_required"
triggers = ["system-boundary", "responsibility-or-dependency-direction", "public-interface-or-protocol", "security-privacy-or-trust-boundary", "concurrency-consistency-reliability-or-failure-strategy", "technology-framework-vendor-or-external-service", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "The proposal introduces durable boundaries between formal authority, portable skills, agent orchestration, runtime adapters, and retained evidence; it defines public schemas and dependency direction, changes trust and concurrency behavior, and selects among material provider-neutral and provider-specific alternatives. The accountable technical owner accepted this trigger assessment and ADR requirement during Phase 1 content review."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T09:03:54Z"
decided_by = "technical-owner"
+++

# Architecture: Harness-owned authority with replaceable agent execution planes

## Context and scope

SE Harness already provides a repository-native authority and validation plane.
Agent runtimes now provide reusable skills, specialized agents, parallel work,
model selection, permissions, and runtime-specific configuration. The proposed
architecture connects these capabilities without allowing them to become an
alternate source of lifecycle legality or accountable authority.

This architecture covers authority separation, autonomy-envelope validation,
decision packets, execution receipts, portable skills, read-only orientation,
bounded orchestration, and runtime adapter materialization. It does not select
the exact current decision rights that may be pre-delegated; that remains an
accountable policy decision.

The accountable technical owner accepted the trigger set, ADR coverage, and
architecture during Phase 1 content review. That content decision is distinct
from the authoritative lifecycle state recorded in the front matter and its
lifecycle events.

## Components and responsibilities

### Authority plane

Existing formal artifacts, managed workflow, decision rights, quality gates,
traceability, installed lock, mutation guard, and exact released evaluator own:

- product and governance state;
- selected work and relations;
- permitted lifecycle transitions;
- decision-right and gate selection;
- installed integrity and evaluator identity;
- scope and safe mutation enforcement;
- final graph validation.

This plane is authoritative. It does not delegate its rule calculation to a
skill, orchestrator, model, or adapter.

### Procedure plane

Portable skills and machine-readable skill contracts own:

- reusable outcome-oriented instructions;
- trigger and non-trigger descriptions;
- precondition and input discovery;
- invocation of supported harness operations;
- evidence collection and structured handoff;
- declared mutation class, stop conditions, and fallback behavior.

The pilot's portable core has one canonical source under
`templates/repository/standard/.agents/skills/harness-orient/` and one managed
installed location at `.agents/skills/harness-orient/`. The retained
`skill-contract.json` and `se-harness-skill-manifest-v1` digest bind the exact
portable procedure. There is no second authoritative package copy under the
Python module tree.

This plane is managed and integrity-checked when distributed by the harness,
but its procedure text is not product or lifecycle authority.

### Execution plane

The primary agent, logical execution profiles, and optional worker orchestrator
own:

- task decomposition inside selected scope;
- bounded worker assignment;
- read-only parallelism;
- disjoint writer planning and worktree isolation in later phases;
- result aggregation;
- one final integration owner;
- revalidation against the combined repository.

This plane cannot expand the work order, autonomy envelope, decision class, or
runtime permission granted by its parents.

### Adapter plane

Runtime adapters own translation into provider-specific:

- agent definition files;
- model and reasoning defaults;
- tool, sandbox, permission, hook, MCP, memory, and concurrency settings;
- skill discovery metadata;
- capability degradation and single-agent fallback configuration.

Adapter output is derived, ownership-aware, versioned, and replaceable. It does
not change formal state.

### Evidence plane

Decision packets, execution receipts, retained command outputs, test evidence,
skill manifests, and adapter manifests own:

- exact execution observations;
- evidence and digest bindings;
- worker coverage and failure visibility;
- decision-ready summaries;
- reproducibility and conformance observations.

Evidence supports accountable decisions but does not make them.

## Dependency direction

```text
Formal artifacts + managed policy + released evaluator
                         |
                         v
              machine-readable harness result
                         |
                         v
             portable skill procedure contract
                         |
                         v
        primary agent + bounded execution profiles
                         |
                         v
               runtime-specific adapter
                         |
                         v
                 runtime execution
                         |
                         v
       receipts + evidence + combined-state validation
                         |
                         v
              accountable decision packet
```

Lower planes may observe higher-plane results and return evidence. They may not
define or override higher-plane authority. The authority plane has no
dependency on a particular runtime, model, subagent format, or hosted service.

## Data and control flow

1. An operator selects a repository objective or artifact and supplies a
   structured launcher for the target's exact external released evaluator.
2. The authority plane verifies evaluator version and identity, then validates
   installed integrity and current formal state.
3. The harness selects the governing procedure, gates, decision class, and
   scope. The complete current decision-right mapping in `SPEC-AEX-001` fails
   closed to `accountable-decision-required` for unknown future rights.
4. A portable skill validates its retained contract and portable-core digest,
   then invokes only the supported machine contract. Missing optional
   operations use the explicit evaluator capability matrix rather than
   candidate-source fallback.
5. The primary agent executes the single-agent path or plans bounded workers.
6. Workers receive only their task input, execution profile, scope, permitted
   operations, evidence obligation, and result schema.
7. The primary or integration coordinator aggregates results and validates the
   actual combined repository.
8. The evidence plane emits a receipt and, when required, one decision packet.
9. At an accountable decision point, the responsible owner decides through the
   existing managed lifecycle mechanism; generation of the packet has no
   lifecycle effect.

## Trust boundaries

- Formal artifact content is authoritative only according to valid type,
  relations, lifecycle state, and accountable decisions; it remains untrusted
  parser input.
- The exact released evaluator is trusted for the versioned installed contract;
  candidate source and candidate packages remain separately identified.
- Skills and supporting scripts are trusted execution inputs only after their
  integrity and provenance are established; they remain non-authoritative.
- The canonical standard-template skill source and installed managed copy cross
  a packaging and upgrade boundary. Exact managed matches may upgrade;
  customized or ambiguous content blocks before partial replacement.
- Model output, worker summaries, runtime capability reports, and adapter files
  are untrusted observations until validated.
- Runtime sandboxes and permissions constrain technical access but are not
  governance boundaries.
- Filesystem, Git, environment, network, connectors, and external systems remain
  explicit security and side-effect boundaries.

## Required patterns

- Machine-readable, versioned contracts with human renderers over one semantic
  result.
- One canonical portable skill source, one retained strict contract, and one
  deterministic `utf8-text-lf-v1` manifest digest.
- A declared released-evaluator minimum and capability matrix with blocked
  required operations and explicitly degraded optional operations.
- Plan-before-apply for every generated or mutated repository surface.
- Explicit authority, execution profile, skill identity, scope, and decision
  class fields.
- Safe path handling, strict field sets, canonical encoding, stable ordering,
  and content digests.
- Single-agent behavioral baseline before optional orchestration.
- Read-only parallelism before parallel writers.
- Disjoint writer scope, isolated worktrees, and one final integration owner.
- Fresh combined-state validation and evidence after integration.
- Single-agent and command-driven fallback when skill or runtime capabilities
  are unavailable.

## Prohibited patterns

- Encoding lifecycle rules only in `SKILL.md`, prompts, or runtime agents.
- Naming an execution profile as evidence that it holds an accountable role.
- Treating workspace-write, unrestricted tools, model choice, or successful
  execution as authorization.
- Allowing a child agent or adapter to widen parent scope or decision rights.
- Accepting subagent summaries without retained outputs or final validation.
- Concurrent writers in one worktree or overlapping path scope.
- Making a hosted runtime, proprietary agent definition, or provider-specific
  tool mandatory for correctness.
- Keeping a second authoritative skill copy in a Python package or runtime
  adapter, or silently loading candidate commands absent from the exact
  released evaluator.
- Letting adapter generation edit formal artifacts or managed policy.
- Using candidate source as the governing released evaluator.

## Quality attributes

- **Authority clarity:** every requested decision identifies one accountable
  role distinct from execution machinery.
- **Determinism:** identical state and explicit inputs produce equivalent
  scope, decision boundary, receipt, and governed effect.
- **Portability:** the core procedure works across declared runtimes and through
  one agent without provider-specific rules.
- **Safety:** invalid, stale, ambiguous, or out-of-scope execution fails before
  partial writes or external effects.
- **Auditability:** receipts bind skills, workers, commands, changed paths,
  evidence, evaluator, and final validation without retaining hidden reasoning.
- **Recoverability:** interrupted writes restore prior bytes or report exact
  restoration failure.
- **Efficiency:** parallelism is bounded and justified by measured wall-time or
  coverage benefit relative to cost.
- **Evolvability:** skill, receipt, packet, profile, and adapter schemas are
  versioned independently from provider implementations.

## Conformance checks

- Prove that no skill, profile, or adapter defines a lifecycle transition or
  decision role absent from the authority plane.
- Compare command-driven, single-agent skill-driven, and multi-agent outputs for
  semantic equivalence on a shared scenario corpus.
- Exercise missing skills, unsupported runtimes, disabled subagents, permission
  inheritance, stale envelopes, overlapping writers, worker failure, and
  adapter conflict.
- Verify managed integrity, candidate/released identity separation, safe paths,
  transactional writes, rollback, and final graph validation.
- Verify the canonical `.agents/skills/harness-orient/` install and upgrade,
  portable manifest digest, retained skill contract, minimum evaluator 0.5.0,
  and deterministic reduced-capability behavior.
- Confirm packets and receipts contain no secrets, hidden reasoning, or
  unbounded evidence bodies.
- Measure human interruption location, cycle time, worker cost, conflicts, and
  evidence reproducibility.

## Related ADRs

- `ADR-AEX-001` proposes harness-owned authority with non-authoritative skills,
  execution profiles, and runtime adapters.
- `ADR-AEX-002` proposes a single-agent baseline followed by bounded read-heavy
  parallelism and one final integration owner.

Both ADRs remain proposed. This architecture cannot be approved until the
accountable technical owner accepts or revises them and the decision assessment.
