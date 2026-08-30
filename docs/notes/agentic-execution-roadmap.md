# Agentic execution roadmap

<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This is a non-authoritative planning note. It does not approve product changes,
> authorize implementation, delegate a decision right, verify a candidate, or
> authorize a release or external action. Formal authority comes from
> `ENGINEERING_HARNESS.md`, its managed policies, and approved artifacts under
> `docs/engineering/`.

## Purpose

This roadmap describes a staged transformation of SE Harness from a primarily
command-driven operating model into a skill-driven, agent-executed model. The
target is to delegate routine engineering execution as far as safely possible
while retaining accountable humans at the decisions that require judgment,
risk acceptance, assurance, or external authority.

The operating objective is:

> Move from human-in-the-loop at routine procedural steps to
> human-at-the-decision-point, without weakening explicit authority,
> deterministic gates, exact provenance, or recovery boundaries.

The sequence is dependency-based, not a calendar commitment. Each phase needs
its own approved governing artifacts and bounded work orders before
implementation begins.

## Target model

The target model separates six concepts that must not be conflated:

| Concept | Meaning |
| --- | --- |
| Accountable role | The human role that owns a defined engineering decision |
| Agent execution profile | The type of worker assigned to a bounded task |
| Skill | A reusable procedure that explains how to achieve an engineering outcome |
| Work order and autonomy envelope | The exact scope and operations authorized now |
| Harness control plane | The authoritative state, gates, procedures, and permitted transitions |
| Runtime permission | What the executing process can technically access or modify |

The intended control flow is:

```text
Accountable human approves definition, work, and delegation boundary
                              |
                              v
          Harness selects the permitted procedure and gates
                              |
                              v
            Orchestrator assigns bounded agent execution
                              |
                   +----------+----------+
                   |                     |
                   v                     v
             Execution profile         Skill
                 "worker"          "procedure"
                   |                     |
                   +----------+----------+
                              |
                              v
                   Runtime-specific agent
                              |
                              v
              Changes, checks, and retained evidence
                              |
                              v
                 Harness revalidation and receipt
                              |
                              v
             Decision packet for accountable human
```

Agent profiles and runtime configuration are execution machinery. They do not
create engineering authority. A separate context, model, or sandbox can improve
analytical independence, but it does not create an accountable assurance or
release decision.

## Design principles

1. **Authority remains in the harness model.** Skills and agent definitions do
   not replace formal artifacts, decision rights, quality gates, or lifecycle
   rules.
2. **Skills remain thin over a thick control plane.** Skills ask `harnessctl`
   for current state and the selected procedure instead of duplicating managed
   workflow rules.
3. **Delegation is explicit and bounded.** An agent does not infer an autonomy
   envelope from tool permissions, a prompt, silence, or a previous action.
4. **Preparation remains distinct from decision.** Agents may analyze and
   prepare decision candidates; reserved accountable decisions remain explicit.
5. **Structured outputs precede orchestration.** Single-agent execution must be
   deterministic before multi-agent coordination is introduced.
6. **Parallelism is selective.** Read-heavy work may run concurrently. Parallel
   writers require disjoint scope and isolation, followed by integration and
   final revalidation.
7. **Runtime adapters are replaceable.** Vendor-specific formats remain derived
   configuration and do not become product or governance authority.
8. **The released-evaluator boundary remains intact.** Candidate source, skills,
   adapters, and subagents cannot substitute for the exact released evaluator
   required by the target repository.

## Decision classification

The transformation requires an explicit classification of actions and
decisions. Adding skills without changing the underlying decision model would
improve usability but would not materially reduce human interruptions.

| Class | Typical examples | Expected handling |
| --- | --- | --- |
| `routine-read-only` | Inspect, focus, preflight, run tests, render evidence | Autonomous when scope and runtime permissions allow it |
| `advance-delegation-required` | Start approved work, mark bounded execution complete, prepare a ready VREC | Autonomous only inside a previously approved delegation boundary |
| `accountable-decision-required` | Approve definitions, accept significant architecture, accept exceptions or risk, verify a VREC, release an RLS | Explicit human decision |
| `action-time-authorization-required` | Merge, tag, publish, deploy, operate, or use privileged credentials | Exact action-time authorization by the accountable owner |

The formal design work must review every current decision right and classify it
deliberately. No existing decision becomes delegatable merely because an agent
can perform the associated command.

## Workstreams

The program contains six related workstreams.

### Authority and lifecycle

- distinguish accountable roles from agent execution profiles;
- define `routine-read-only`, `advance-delegation-required`,
  `accountable-decision-required`, and
  `action-time-authorization-required` classes;
- define the autonomy-envelope contract;
- review current work-start, work-completion, verification-preparation,
  delivery-selection, release-preparation, and external-action boundaries;
- retain explicit assurance, release, exception, and external-action decisions.

### Harness control plane

- expose stable machine-readable next-action and decision information;
- validate delegation scope before mutation;
- bind agent execution to selected artifacts and exact repository state;
- produce decision packets and execution receipts;
- preserve mutation guard, installed integrity, and runtime identity;
- make retries bounded and failure behavior deterministic.

### Skills

- define an SE Harness portable skill profile;
- implement outcome-oriented lifecycle skills;
- consume harness JSON rather than parse human prose;
- declare mutation class, evidence obligations, stop conditions, and decision
  boundaries;
- version and digest skill content used during governed execution.

### Execution profiles and orchestration

- define narrow non-accountable worker profiles;
- specify task inputs, allowed operations, prohibited actions, and return schema;
- support read-only parallel analysis first;
- introduce isolated concurrent writers only for disjoint scopes;
- designate one integration owner for the combined candidate;
- revalidate the real combined repository after orchestration.

### Runtime adapters

- translate logical execution profiles into runtime-native configuration;
- support one runtime before claiming portability;
- preserve user-owned runtime configuration and customizations;
- generate derived manifests and detect adapter drift;
- provide a single-agent fallback when subagents are unavailable.

### Evidence, evaluation, and distribution

- retain structured execution receipts without treating conversation history as
  authority;
- test single-agent and multi-agent behavioral equivalence;
- test cross-runtime conformance;
- distribute skills and adapters through safe, versioned installation and
  upgrade paths;
- measure human interruptions, reliability, scope control, reproducibility,
  cost, and cycle time.

## Phase 1 - Govern the target operating model

### Current progress

The complete 16-artifact `agentic-execution` packet has passed accountable
content review and exact released-evaluator 0.6.0 validation. The accountable
owner approved the complete atomic `draft -> approved` transaction under all
required role assertions, and the isolated exact-wheel evaluator applied all 16
transitions atomically after current `main` supplied the governed schema-3 root
lock. All selected artifacts are `approved`; Phase 1 exit criteria are met. The
decision and transition result are recorded in
[`agentic-execution-phase-1-approval-decision.md`](history/agentic-execution-phase-1-approval-decision.md).

### Objective

Establish the authoritative product intent and architecture before creating
runtime configuration or executable skills.

### Planned outputs

- a new formal engineering domain, for example `agentic-execution`;
- approved intent and capability definitions;
- requirements for authority separation, delegation, skills, evidence,
  portability, and failure behavior;
- specifications for autonomy envelopes, decision packets, execution receipts,
  and the portable skill profile;
- architecture and significant ADRs;
- verification contracts and bounded implementation work orders.

Artifact identifiers must be allocated only after checking every repository ref.
This roadmap does not reserve identifiers.

### Exit criteria

- accountable roles and agent execution profiles are unambiguous;
- every current lifecycle decision has a proposed classification;
- the `accountable-decision-required` human decision set is explicit;
- the candidate design explains how existing authority and evaluator boundaries
  remain intact;
- the first implementation work is approved and bounded.

### Human decision point

Accountable owners approve or reject the proposed intent, definitions,
architecture decisions, verification approach, and initial work order.

## Phase 2 - Define the core contracts

### Objective

Create runtime-neutral contracts that skills and adapters can rely on.

### Autonomy envelope

The envelope should identify:

- the selected work order and repository;
- permitted operations and lifecycle effects;
- permitted files or component prefixes;
- evidence obligations;
- allowed execution profiles;
- concurrency and writer limits;
- bounded retry rules;
- explicit stop conditions;
- reserved decisions that cannot be delegated.

The exact representation remains an architecture decision. The harness must
validate it; a skill or runtime must not interpret a free-form approximation as
authority.

### Decision packet

A decision packet should contain:

- decision type and required accountable role;
- selected artifact and exact candidate identity;
- the exact decision being requested;
- applicable gate results;
- recommendation and complete alternatives;
- evidence paths and digests;
- unresolved findings and assumptions;
- expected effects and explicit non-effects;
- transition preview or exact external action;
- safe deferral and remediation information.

### Execution receipt

An execution receipt should contain:

- execution profile and runtime observation;
- skill name, version, and digest;
- selected artifact and authorized scope;
- commands and normalized results;
- changed paths;
- retained evidence paths and hashes;
- subagent contribution summaries;
- final validation result and repository identity.

The receipt is retained evidence. It does not prove that the work is correct and
does not make an accountable decision.

### Portable skill profile

The profile should define:

- mandatory `SKILL.md` metadata and procedure sections;
- required inputs and structured outputs;
- preconditions and supported lifecycle states;
- mutation classification;
- required harness checkpoints;
- evidence obligations;
- escalation and stop conditions;
- optional runtime overlays;
- deterministic fallback behavior.

### Exit criteria

- all four contracts have machine-testable schemas or equivalent deterministic
  representations;
- security and authority threat models cover malformed, ambiguous, stale, and
  adversarial inputs;
- failure tests prove that invalid scope cannot reach a write;
- the contracts do not depend on a particular agent runtime.

## Phase 3 - Build the single-agent skills MVP

### Objective

Prove that a skill-driven interface can operate the existing harness without
changing authority or weakening checks.

### Initial skill set

| Skill | Outcome | Mutation boundary |
| --- | --- | --- |
| `harness-orient` | Explain repository state, focused scope, readiness, and the next decision | Read-only |
| `harness-draft-change` | Prepare a reviewable definition and work-order proposal | Draft creation only; no approval |
| `harness-execute-work-order` | Preflight, implement, test, review, and retain evidence within approved scope | Work-order-bounded implementation |
| `harness-prepare-assurance` | Revalidate the exact candidate, prepare a ready VREC, and emit the assurance packet | Ready preparation only; no verification |

Small command wrappers such as `run-harness-check` should normally be internal
skill steps or scripts, not separately discoverable top-level skills.

### Implementation rules

- query the harness for current state and the selected procedure;
- consume stable JSON outputs;
- do not duplicate `WORKFLOW.json`, quality gates, or decision rights in skill
  prose;
- recheck repository state immediately before mutation;
- stop at missing authority, invalid scope, failed gates, or conflicting policy;
- emit a structured handoff or decision packet.

### Exit criteria

- the skill-driven path produces the same formal effects as the documented
  command-driven path;
- it introduces no new authority source;
- adversarial input and mutation-boundary tests pass;
- the same skill procedure works without spawning subagents;
- the user can complete a representative bounded workflow with fewer procedural
  prompts and no loss of evidence.

### Repository host activation follow-through

The four canonical cores remain under `.agents/skills`. Codex discovers them
directly. Claude Code receives same-named repository-local adapters under
`.claude/skills` that load the canonical core without copying its procedure.
Writing skills remain user-explicit-only in both hosts; orientation remains
read-only and matchable. `WO-AEX-004` implements this bounded availability
layer before Phase 4 changes delegation or mutation admission.

## Phase 4 - Enable governed delegated execution

### Current approved packet and implementation

The formal Phase 4 definition and implementation packet is approved:
`REQ-AEX-010` through `REQ-AEX-012`, `SPEC-AEX-006` through
`SPEC-AEX-008`, `ARCH-AEX-002`, `ADR-AEX-006` through `ADR-AEX-007`,
`VER-AEX-004`, and `WO-AEX-005` through `WO-AEX-008`.

The packet selects one exact-evaluator-owned path: stable live observation,
formal maximum delegation, one ephemeral envelope per effect, isolated worker
proposals, canonical content-addressed change bundles, a journaled target effect
broker, receipt-linked state, delegated work-order start/completion, and VREC
preparation. It stops at independent assurance. `WO-AEX-005` and `WO-AEX-006`
are implemented and covered by verified VRECs. Their commits remain the exact
stacked dependency while the `WO-AEX-006` pull request awaits integration.
`WO-AEX-007` is implemented with verified `VREC-AEX-007`; `WO-AEX-008` is
separately `in_progress` on that exact stacked candidate. This note does not
complete, verify, release, or activate the current candidate.

The verified `WO-AEX-007` candidate composes the observer, delegation,
nonce/session, bundle broker, lifecycle engine, provenance writer, execution
receipts, and lossless packet projector. It registers only the closed four-
operation catalog, proves complete lifecycle documents rather than a receipt
alone, stops before Git when a commit is required, and prepares only an
undecided ready VREC after a separately created clean candidate. Real-Git tests
exercise success, proof gaps, failed gates, direct unreceipted writes, and
recovery blocking. `WO-AEX-008` integrates v3 writing-skill evaluator clients,
host parity, and complete package qualification; commit-bound independent
assurance remains required.

### Objective

Change the harness and managed policies so approved autonomous execution can
continue through steps that do not require a current accountable decision
without repeated human confirmation.

### Planned changes

- validate and bind autonomy envelopes;
- separate `accountable_role` from `execution_profile` in relevant outputs;
- emit canonical decision packets;
- emit and validate execution receipts;
- activate advance delegation for work start, work completion, and VREC
  preparation; retain `DR-RLS-PREPARE` as a later separately governed step;
- allow only `advance-delegation-required` steps to use an approved delegation
  boundary;
- retain human decisions for definition approval, exceptions, assurance,
  release, and external action;
- ensure lifecycle mutations still require the locked released evaluator.

### Target lifecycle

```text
Human approves definition + bounded work + autonomy envelope
                              |
                              v
Agent starts and completes approved execution, checks, and evidence
                              |
                              v
Agent prepares exact-commit assurance material and a ready VREC
                              |
                              v
Human assurance owner verifies, rejects, or requests remediation
```

Release preparation, release decisions, delivery, Git mutation, and external
actions remain outside the Phase 4 packet and require later formal work.

### Exit criteria

- an approved envelope cannot expand itself or survive stale repository state;
- autonomous operations stop exactly at `accountable-decision-required` and
  `action-time-authorization-required` boundaries;
- every mutation remains attributable and recoverable;
- lifecycle validation and evaluator identity pass before and after execution;
- the number of procedural human interruptions is measurably lower.

## Phase 5 - Add multi-agent orchestration

### Objective

Improve speed and analytical coverage without changing the authority or result
of the single-agent procedure.

### Initial execution profiles

| Profile | Responsibility | Default write policy |
| --- | --- | --- |
| `repository-explorer` | Map scope, dependencies, and relevant implementation | Read-only |
| `implementation-worker` | Implement one bounded and assigned change | Scoped write |
| `test-evidence-runner` | Execute checks and retain normalized evidence | Read-only except declared evidence output |
| `verification-evidence-analyst` | Independently assess candidate evidence and findings | Read-only |
| `integration-coordinator` | Combine authorized results and own the final candidate | Sole final writer |

These profiles do not correspond to accountable product, technical, assurance,
release, or service-owner roles.

### Coordination rules

- parallelize exploration, testing, log analysis, and review first;
- allow only one writer for a given path or artifact set;
- use separate worktrees for concurrent writers;
- require explicit disjoint scopes for parallel mutations;
- return structured claims and evidence rather than raw transcripts;
- integrate through one coordinator;
- run final gates against the combined repository, not individual worker views;
- degrade to the single-agent procedure when orchestration is unavailable.

### Exit criteria

- single-agent and multi-agent runs have equivalent governed effects;
- coordination cannot bypass path scope or mutation authority;
- conflicts and partial results fail safely;
- the combined candidate has fresh evidence and exact provenance;
- parallel execution provides a measured benefit that justifies its cost.

## Phase 6 - Add runtime adapters

### Objective

Materialize logical execution profiles and skills for supported agent runtimes
without making runtime formats authoritative.

### Adapter behavior

A future command such as `harnessctl agents materialize --runtime <runtime>`
should:

- produce a read-only plan by default;
- identify every derived file and its logical source;
- preserve unrelated and customized runtime configuration;
- fail on ambiguous ownership or drift;
- apply transactionally under an approved work order;
- write a deterministic adapter manifest;
- support safe replay and no-op detection;
- avoid changing formal artifacts or decision rights.

One runtime should be implemented and tested first. A second runtime is the
first meaningful portability test. Similar-looking generated files are not
proof of equivalent behavior.

### Exit criteria

- adapter conformance tests cover discovery, invocation, permissions,
  delegation, and fallback;
- generated configurations remain derived and replaceable;
- unsupported runtime features produce explicit degradation rather than bypass;
- upgrades preserve user customization and repository integrity.

## Phase 7 - Distribute, pilot, and self-host

### Objective

Prove the model in consumer repositories before relying on it for SE Harness's
own governed development and release.

### Rollout order

1. disposable fixture repositories;
2. controlled non-critical consumer repositories;
3. representative repositories with custom instructions and policies;
4. cross-runtime conformance pilots;
5. SE Harness self-hosting under the released-evaluator boundary;
6. documented installation, safe upgrade, and rollback paths.

Self-hosting is the final proof because this repository has additional
candidate-versus-released evaluator, distribution, bootstrap, and publication
constraints. It should not be the first experiment.

### Exit criteria

- installation and upgrade are safe, deterministic, and recoverable;
- pilot evidence meets the defined reliability and autonomy targets;
- no runtime becomes a hidden authority source;
- self-hosted execution passes the governing released evaluator;
- accountable owners approve general availability separately from technical
  completion.

## Measures of success

The program should measure outcomes rather than count skills or agents.

| Measure | Intended direction |
| --- | --- |
| Human interactions occurring at accountable decision points | Increase |
| Procedural interruptions per work order | Decrease |
| Time from approved work to ready assurance material | Decrease |
| Unauthorized lifecycle transitions | Remain zero |
| Out-of-scope writes | Remain zero |
| Reproducible evidence and exact candidate binding | Remain complete |
| Failed or ambiguous escalations | Decrease |
| Single-agent versus multi-agent result equivalence | Remain high |
| Cross-runtime conformance | Increase as adapters mature |
| Token and execution cost per completed workflow | Measured against saved human time and cycle time |

An initial product-level target to validate during Phase 1 is:

> At least 80 percent of human interactions occur at accountable decision points,
> with zero unauthorized lifecycle transitions and reproducible evidence for
> every autonomous stage.

The target is a planning hypothesis until approved through formal artifacts.

## Principal risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Agent profile is mistaken for an accountable role | Separate namespaces and prohibit accountable decision claims in execution profiles |
| Skill prose drifts from managed workflow | Query machine-readable harness contracts; add conformance tests and content digests |
| Runtime permission is mistaken for authorization | Require a valid work order and autonomy envelope before mutation |
| Implicit skill activation starts sensitive work | Make mutation preconditions executable and require explicit bounded authority |
| Parallel writers corrupt or conflict | Disjoint scopes, separate worktrees, one integration owner, final revalidation |
| Subagent summary is accepted without evidence | Require structured receipts, retained outputs, and independent harness checks |
| Runtime adapter becomes authoritative | Mark output as derived; retain harness authority and single-agent fallback |
| Candidate code substitutes for the evaluator | Preserve external released-evaluator identity checks for every governed mutation |
| Too many small skills create routing ambiguity | Use outcome-oriented skills aligned with lifecycle and decision boundaries |
| Automation hides cost or correlated failure | Measure tokens, time, retries, failure modes, and multi-agent equivalence |

## Immediate next step

`WO-AEX-005` through `WO-AEX-007` are independently verified, and
`WO-AEX-008` is in progress on their exact stacked commits. The immediate next
step is to finish the v3 skill, host, source, wheel, installation, and upgrade
qualification, then prepare the governed implementation handoff. Later
independent assurance must bind an exact candidate commit.

Do not use candidate Phase 4 code to govern its own construction, start
create a promotable successor distribution, install it, or run a target pilot
without the applicable later decisions and release/pilot packet.

## Roadmap maintenance

Update this roadmap when an approved formal decision changes sequencing,
scope, terminology, measures, or runtime support. The corresponding formal
artifacts remain authoritative. This note should link to them once they exist
without copying their normative rules or implying that roadmap completion
constitutes verification or release.
