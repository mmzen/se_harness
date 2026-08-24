+++
id = "INT-AEX-001"
type = "intent"
title = "Make governed agent execution autonomous between accountable decisions"
status = "approved"
owners = ["product-owner", "repository-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T09:03:54Z"
decided_by = "product-owner"
+++

# Intent: Make governed agent execution autonomous between accountable decisions

## Problem

SE Harness already separates formal authority from automation, validates a
selected engineering graph, and emits bounded workflow guidance. In practice,
operators and coding agents still interact mainly through individual commands
and conversational handoffs. A human may therefore be asked to confirm routine
procedural steps, while agent runtimes provide increasingly capable skills,
subagents, background execution, and runtime-specific permissions that the
harness does not yet model directly.

Moving orchestration into prompts or vendor-specific agent definitions would
reduce visible friction but create a new risk: execution configuration could be
mistaken for engineering authority. It would also make governed behavior depend
on one runtime's discovery, permission, delegation, or configuration semantics.

The product problem is to delegate routine execution without delegating the
accountable decisions that make product intent, architecture, assurance,
release, risk acceptance, and external action legitimate.

## Desired outcomes

- An accountable owner can approve one bounded work scope and explicit
  delegation boundary, after which agents perform permitted procedural work
  without repeated confirmation until an accountable decision point or stop
  condition is reached.
- A human arriving at an accountable decision point receives one compact,
  evidence-backed decision packet tied to the exact artifact and repository
  state.
- Skills provide reusable outcome-oriented procedures while the harness remains
  the source of lifecycle legality, gates, authority, and mutation constraints.
- Agent execution profiles remain visibly distinct from accountable human roles
  and runtime permissions.
- Single-agent and multi-agent execution produce equivalent governed effects;
  parallelism changes throughput or analytical coverage, not authority.
- Runtime-specific agent definitions remain replaceable adapters with a safe
  single-agent fallback.
- Every governed mutation preserves installed integrity, exact released-
  evaluator identity, scope confinement, attributable evidence, and recoverable
  failure behavior.

## Actors and stakeholders

- Product and domain owners decide the desired outcomes and requirement
  obligations.
- Technical owners decide significant architecture and accept its risks and
  tradeoffs.
- Engineering owners approve bounded work and any pre-delegated execution
  envelope permitted by policy.
- Assurance owners define verification contracts and decide exact candidate
  evidence.
- Release and external-action owners retain release, publication, deployment,
  operational, and credential-bearing decisions.
- Repository contributors and coding agents execute approved work and prepare
  evidence or decision candidates.
- Agent runtime providers supply execution contexts, permissions, discovery,
  and optional orchestration without becoming an authority source.
- Repository adopters bear compatibility, customization, cost, and operational
  risk when enabling agentic execution.

## Success measures

| Measure | Baseline | Target | Observation window |
| --- | ---: | ---: | --- |
| Human interactions occurring at accountable decision points | Not yet measured | At least 80% | Each representative governed workflow |
| Unauthorized lifecycle transitions or out-of-scope writes | 0 required | 0 | Every automated and pilot run |
| Autonomous stages with reproducible retained evidence | No agentic receipt contract | 100% | Every autonomous governed stage |
| Single-agent and multi-agent governed-effect equivalence | Not defined | 100% for supported scenarios | Each orchestration conformance run |
| Supported-runtime conformance for authority and stop behavior | Not defined | 100% for the declared portable profile | Each adapter release |
| Time from approved work to an assurance-ready decision packet | Not yet measured | Measurable reduction without weaker gates | Each pilot cohort |

## Non-goals

- Grant product, requirements, architecture, assurance, release, exception,
  publication, deployment, or operational decision rights to a model merely
  because it is configured as a specialized agent.
- Treat a skill, prompt, conversation, model choice, sandbox, permission mode,
  hook, runtime configuration, or adapter manifest as formal authority.
- Replace `harnessctl`, formal artifacts, managed policies, or the exact
  released evaluator with agent reasoning.
- Require subagents for correctness; the governed procedure must retain a
  deterministic single-agent path.
- Make conversation transcripts authoritative evidence or require retention of
  private chain-of-thought material.
- Implement every lifecycle skill, runtime adapter, or external integration in
  the first work order.
- Automatically commit, push, open or merge a pull request, tag, publish,
  deploy, operate, or use privileged credentials.
- Use SE Harness's self-hosting repository as the first uncontrolled pilot.

## Principles and immutable constraints

- Accountable authority, delegated scope, executable procedure, runtime
  permission, and model capability remain separately represented.
- Automation may prepare a decision candidate but cannot claim that an
  accountable owner made the decision.
- Skills remain thin clients over machine-readable harness contracts and never
  calculate lifecycle legality independently.
- Delegation is explicit, bounded, stale-state-sensitive, and unable to expand
  itself.
- An `accountable-decision-required` decision or failed gate stops autonomous
  execution before the associated mutation or external action.
- Every governed write is attributable, path-confined, evaluator-authorized,
  transactionally safe, and followed by validation of the real combined state.
- Runtime-specific formats and provider capabilities remain replaceable.
- Python 3.11+ standard-library runtime behavior and the single standard
  installation remain supported.

## Risks and assumptions

- **Fact:** current managed workflow already separates preparation from
  accountable verification and release decisions.
- **Fact:** current agent runtimes differ in skill discovery, subagent
  configuration, permission inheritance, orchestration, and isolation.
- **Assumption:** a small portable skill core can invoke stable harness JSON and
  degrade safely when runtime-specific orchestration is absent.
- **Assumption:** fewer procedural interruptions improve operator throughput
  only if decision packets remain concise, complete, and trustworthy.
- **Risk:** an execution profile named after an accountable role may be mistaken
  for that role; the model requires distinct terminology and fields.
- **Risk:** skill prose may drift from managed workflow; conformance must be
  executable and skill content versioned.
- **Risk:** implicit skill activation or inherited runtime permissions may start
  work outside the intended boundary; every mutation requires harness-side
  authority checks.
- **Risk:** parallel writers can create stale evidence, conflicts, or partial
  integration; one final integration owner and fresh combined-state validation
  are required.
- **Risk:** additional agents increase token, latency, and coordination cost;
  delegation must demonstrate a measured benefit.
- **Open decision:** accountable owners must decide which current decision
  rights, if any, may be pre-delegated inside an approved autonomy envelope.
