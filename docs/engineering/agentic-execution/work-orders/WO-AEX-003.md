+++
id = "WO-AEX-003"
type = "work_order"
title = "Implement the single-agent outcome skills MVP"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "technical-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[assurance]
commit_bound_verification = "required"
rationale = "The work will change managed installed skills, trusted helper scripts, strict portable contracts, installer behavior, and distribution surfaces that later operators will rely on at governance and assurance boundaries."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "MANIFEST.in",
  "README.md",
  "pyproject.toml",
  "se_harness/installer.py",
  "se_harness/skill_contract.py",
  "templates/repository/standard/.agents/skills/harness-draft-change/",
  "templates/repository/standard/.agents/skills/harness-execute-work-order/",
  "templates/repository/standard/.agents/skills/harness-prepare-assurance/",
  "tests/fixtures/agentic_execution/phase3/",
  "tests/test_agentic_execution.py",
  "tests/test_instruction_architecture.py",
  "tests/test_public_onboarding.py",
  "tests/test_release_build.py",
  "tests/test_standard_repository_lifecycle.py",
  "docs/engineering/agentic-execution/README.md",
  "docs/engineering/agentic-execution/evidence/WO-AEX-003-verification.md",
  "docs/notes/agentic-execution-skills-mvp.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/notes/README.md",
]

[relations]
implements = ["REQ-AEX-005", "REQ-AEX-008"]
specifications = ["SPEC-AEX-001", "SPEC-AEX-002", "SPEC-AEX-003", "SPEC-AEX-004"]
architecture = ["ARCH-AEX-001", "ADR-AEX-001", "ADR-AEX-002", "ADR-AEX-003", "ADR-AEX-004"]
verification = ["VER-AEX-001", "VER-AEX-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T13:50:24Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-24T13:51:11Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-24T14:23:12Z"
decided_by = "engineering-owner"
+++

# Work Order: Implement the single-agent outcome skills MVP

## Lifecycle and readiness

This work order is `draft`. It authorizes no implementation, lifecycle
transition, evidence claim, Git operation, package build, installation,
verification record, release, network access, credential use, or external
action.

Before approval, accountable owners must approve `REQ-AEX-008`,
`SPEC-AEX-004`, `ADR-AEX-004`, `VER-AEX-002`, and this work order through the
managed lifecycle procedure. Approval still does not start implementation.
After a separate engineering-owner start decision, the exact released
evaluator must pass the current start checkpoint and preflight for
`WO-AEX-003` before any implementation path changes.

Commit-bound verification is classified `required` because the resulting
managed skills, scripts, strict contracts, installer, and packaged bytes become
trusted execution inputs for later operator workflows.

## Objective

Implement and distribute the three Phase 3 portable skills
`harness-draft-change`, `harness-execute-work-order`, and
`harness-prepare-assurance` as a deterministic single-agent MVP over the
existing harness control plane. Preserve the exact `harness-orient` v1 identity,
keep writing activation explicit, prove command/skill governed equivalence, and
stop before every current accountable completion, assurance, delivery, release,
Git, credential, network, or external-action boundary.

## In scope

- Extend the strict portable skill parser with
  `se-harness-skill-contract-v2` exactly as specified by `SPEC-AEX-004`, while
  preserving all v1 behavior and canonical vectors.
- Add one canonical managed portable core for each of the three new skills.
  Each core contains `SKILL.md`, `skill-contract.json`, and only the bounded
  standard-library scripts required for its declared outcome.
- Implement explicit-activation and precondition checks, structured evaluator
  launchers, current-state checkpoints, closed effect plans, portable path
  admission, immediate pre-effect rechecks, post-effect path comparison,
  structured results, and receipt generation or validation.
- Implement draft preparation through existing released-evaluator draft
  creation operations. Permit one declared planning note and complete new
  formal drafts; permit revision only for explicitly selected current drafts.
  Apply no lifecycle transition.
- Implement work-order execution guidance and bounded helpers for one already
  `in_progress` work order: read the complete current manifest, admit proposed
  paths, execute repository-owned checks, retain declared evidence, compare
  actual changed paths, and stop at the managed handoff decision.
- Implement assurance preparation through the existing released-evaluator
  verification-record preparation operation. Require the exact clean
  candidate, selected work and verification contracts, retained evidence,
  passing preparation checks, unused ID, and explicit preparation actor. Create
  only one `ready` VREC and stop before assurance.
- Extend the ownership-aware standard installer and explicit distribution
  metadata so fresh install and safe upgrade manage and package all four skills
  exactly once.
- Add verifier-owned Phase 3 fixtures and deterministic tests for strict
  contracts, hostile input, explicit activation, lifecycle states,
  command/skill equivalence, path admission, effect sentinels, receipts,
  install, upgrade, source and wheel inventory, and one representative
  end-to-end workflow.
- Add concise operator documentation, update the domain and note indexes, and
  retain exact work-order-keyed evidence.

## Out of scope

- Editing managed `ENGINEERING_HARNESS.md`, workflow, decision-right,
  quality-gate, traceability, template, lock, CI, or managed root files.
- Adding a lifecycle state, transition, decision right, gate, workflow policy,
  or general autonomous workflow command.
- Applying an approval, work-start, work-completion, verification, rejection,
  supersession, delivery, release, or exception decision through a skill.
- Deriving or using an autonomy envelope to admit a real effect, connecting the
  Phase 2 pure contract layer to a general mutation interface, or claiming
  Phase 4 delegated execution.
- Spawning or coordinating subagents, workers, parallel readers, parallel
  writers, worktrees, writer leases, or an integration coordinator.
- Creating Codex, Claude, ChatGPT, IDE, CI, MCP, hosted-service, or other
  runtime-specific profiles, overlays, adapters, hooks, permissions, or model
  defaults.
- Committing, pushing, merging, tagging, publishing, deploying, operating,
  accessing credentials, using the network, or performing another external
  action.
- Building promotable release distributions or changing release/publication
  behavior. An explicitly non-promotable ephemeral wheel may be built outside
  the checkout only as candidate acceptance evidence after implementation has
  separately started.
- Changing the exact v1 `harness-orient` core, behavior, digest, activation, or
  output contract.
- Claiming enforcement against a runtime that ignores the skill procedure or
  authenticating a real-world accountable actor.

## Authorized decision envelope

After separate approval and start authorization, the implementation actor may
choose private helper names, internal immutable data structures, stable bounded
diagnostic wording, fixture subdivisions inside the declared prefix, and
documentation examples that preserve the approved semantics. Scripts and
implementation code must use Python 3.11+ standard-library facilities only.

The actor may not change a public v2 field, enum, effect class, path source,
checkpoint, activation rule, lifecycle stop, output, schema identifier,
canonical encoding, v1 behavior, installer ownership mode, or authority
boundary. It may not add a dependency, CLI or workflow operation, execution
path, skill, adapter, provider file, subagent behavior, Git mutation, credential
access, network behavior, or external effect. Ambiguity is a stop condition,
not implementation discretion.

## Constraints

- Preserve Python 3.11+ compatibility and use only the standard library.
- Keep the exact released evaluator external to the target checkout and pass
  its launcher as a structured argument array.
- Preserve the `se-harness-skill-contract-v1`,
  `se-harness-skill-manifest-v1`, `se-harness-canonical-json-v1`,
  `se-harness-execution-receipt-v1`, decision-packet, and repository-state
  contracts already approved.
- Treat skill bytes, contracts, JSON, artifact IDs, paths, repository content,
  commands, evaluator output, Git observations, evidence, and runtime metadata
  as untrusted.
- Reject duplicate and unknown fields, malformed UTF-8, unsupported schemas,
  excessive inputs, invalid paths, stale state, scope widening, unexpected
  effects, secrets, and authority claims.
- Writing skills require exact explicit activation and delegation remains
  disabled.
- Every controlled effect requires a current identity, integrity, selected
  state, checkpoint, operation, and path recheck immediately before its callback.
- Receipts and packets remain non-authoritative. Conversation history and
  hidden reasoning are not required evidence.
- Preserve unrelated user changes. Do not automatically delete or overwrite an
  unexpected path to manufacture a passing handoff.
- Keep canonical sources under the standard template and create no
  `se_harness/skills/` duplicate.

## Expected change surface

The exact authorized paths are declared in `[execution_scope]`.
`se_harness/skill_contract.py` contains the strict portable v2 parsing and
canonical validation. `se_harness/installer.py`, `MANIFEST.in`, and
`pyproject.toml` change only as required to install and distribute the three new
canonical skill cores. The three skill directories contain all new portable
procedures and bounded scripts.

Tests may change only in the declared files and fixture prefix. Documentation
may change only at the declared paths. If implementation discovers that
`se_harness/cli.py`, `se_harness/workflow.py`, `se_harness/mutation_guard.py`,
managed policy, another package module, or any undeclared path must change,
stop and revise the applicable approved definitions and work order before
continuing.

## Required verification

- Execute every applicable `VER-AEX-001` method for `REQ-AEX-005` plus every
  `VER-AEX-002` method for `REQ-AEX-008`.
- Prove v1 orientation source, contract, helper, canonical vectors, manifest
  digest, installed result, and public behavior are unchanged.
- Use independent canonical vectors for every v2 field, enum, ordering,
  activation, input, precondition, checkpoint, effect, evidence, stop, output,
  and digest rule.
- Prove duplicate keys, unknown fields, invalid UTF-8, floats, excessive input,
  unsupported schema, invalid ID, invalid path, provider metadata, authority
  claims, and secret-bearing values fail closed.
- Run the full explicit-activation matrix and prove every implicit or ambiguous
  writing invocation changes no repository or Git state.
- Run work-order state matrices for `draft`, `approved`, `in_progress`,
  `implemented`, `verified`, and inapplicable states. Only `in_progress` may
  reach an implementation callback.
- Wrap draft, implementation-plan, and assurance helpers with verifier-owned
  effect sentinels. Prove every invalid, stale, failed-gate, scope-expanding, or
  unauthorized case returns before the controlled callback.
- Exercise portable path attacks, component-prefix boundaries, case collisions,
  symlink and junction escapes, staged and unstaged paths, renamed/deleted files,
  untracked files, and repository changes between plan and recheck.
- Compare actual command-driven and skill-driven formal effects, lifecycle
  state, gates, evidence, decision packet, and next action for every common
  fixture.
- Prove valid assurance preparation creates one exact-candidate `ready` VREC
  and performs no assurance, delivery, release, Git, network, credential, or
  external effect.
- Prove complete single-agent behavior when subagents and provider features are
  unavailable and confirm no provider-native files are distributed.
- Prove fresh install, no-op replay, safe upgrade, customization conflict,
  source distribution, non-promotable ephemeral wheel, and fresh wheel install
  contain one complete managed copy of all four canonical skill cores.
- Run the complete repository test suite, source and package validation, exact
  released-evaluator doctor and formal validation, `git diff --check`, and exact
  changed-path comparison against this work order.

## Evidence to record

Retain the source candidate, exact released evaluator, candidate package, and
candidate commit identities; four skill manifests and digests; v1 regression
and v2 canonical vectors; strict parser matrix; explicit-activation matrix;
work-order state matrix; command/skill equivalence results; effect-sentinel
counts; before/after repository and Git manifests; path attack and drift
results; command outputs and digests; receipt and packet equivalence; prepared
VREC fixtures; install, upgrade, source, wheel, and fresh-install inventories;
full-suite counts and duration; exact changed paths; manual assessments;
deviations; and residual uncertainty at
`docs/engineering/agentic-execution/evidence/WO-AEX-003-verification.md`.

## Stop and escalate conditions

Stop while this artifact is `draft`. After separate approval and start, stop
before changing any public contract, v1 behavior, authority source, decision
class, managed policy, lifecycle operation, path source, verification
obligation, dependency, undeclared path, evaluator boundary, installer
ownership mode, or distribution identity. Stop before introducing envelope-
admitted effects, subagents, runtime adapters, Git mutation, credentials,
network activity, publication, deployment, or another external action.

Stop on any required check failure that cannot be corrected within the exact
approved contract and path scope. An unexpected changed path, ambiguous owner
content, or need to alter another package module requires a revised work order;
it is not implementation discretion.

## Completion report format

Report `Outcome`, `Done`, `Not done`, conditional `Blocked by`, `Current
lifecycle state`, `Decision required`, `Next`, `Command or response`, and
conditional `Alternatives`. Name `WO-AEX-003`, implemented requirements, all
four skill identities, evaluator identity, exact changed paths, verification
results, evidence path, deviations, residual uncertainty, and intentionally
unperformed lifecycle, envelope-delegation, subagent, adapter, Git, credential,
network, release, and external actions. Recommend exactly one next authorized
step.
