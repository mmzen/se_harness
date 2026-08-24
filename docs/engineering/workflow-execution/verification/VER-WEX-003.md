+++
id = "VER-WEX-003"
type = "verification"
title = "Verify semantic-fidelity lifecycle handoffs"
status = "approved"
owners = ["quality-owner", "assurance-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
verifies = ["REQ-WEX-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T17:31:43Z"
decided_by = "assurance-owner"
+++

# Verification Contract: Verify semantic-fidelity lifecycle handoffs

## Independence

Verifier-owned fixtures will begin with structured schema-2 results and closed
expected semantic projections, not strings copied from implementation tests.
The assurance reviewer will compare implementation evidence with this contract
and independently review representative agent handoffs. Direct-renderer exact
tests and adaptive semantic tests remain separate so one cannot substitute for
the other.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-WEX-011` structured authority | automated contract test | valid and invalid schema-2 corpus | every presentation starts from one valid result; invalid input fails closed |
| `REQ-WEX-011` direct exact rendering | automated byte snapshot | completed, blocked, decision, command, response, and alternatives vectors | existing deterministic bytes and argument values remain stable |
| `REQ-WEX-011` allowed adaptation | verifier-owned positive corpus | paraphrase, reorder, merge, empty-field omission, technical-level adjustment | each output preserves the closed semantic projection and one next action |
| `REQ-WEX-011` forbidden mismatch | verifier-owned negative corpus | changed ID/state/outcome/effect/non-effect/blocker/role/decision/command/next/alternative | every mismatch is rejected or identified by its differing semantic field |
| `REQ-WEX-011` truthful enforcement boundary | static instruction check | candidate router, workflow, AGENTS, and CLAUDE templates | no instruction requires or claims model byte-for-byte transcription; exact mode names direct rendering |
| `REQ-WEX-011` authority boundary | architecture and negative test | adaptive output requesting or claiming approval, verification, or release | presentation never creates a lifecycle or external effect |
| `REQ-WEX-011` upgrade boundary | installation and managed-integrity test | candidate fresh install and current root | candidate installs consistent new instructions; root managed bytes remain unchanged before governed upgrade |

## Acceptance scenarios

### Scenario 1: concise completed handoff

Given a result with one observed draft-authoring effect, no blocker, one material
non-effect, a draft work order, one accountable review decision, and one
suggested response, an adaptive answer may use two sentences and omit empty
sections. It passes only when all those facts and the single next action remain
clear.

### Scenario 2: blocked handoff

Given a failed gate and unchanged state, the answer may explain the failure in
plain language. It must preserve the exact blocker, unchanged artifact state,
absence of the prohibited effect, and the selected retry or escalation.

### Scenario 3: command handoff

Given a command as an argument array, direct rendering preserves its values and
adaptive display preserves each argument boundary. The verifier rejects a
display that adds a flag, removes a target, or turns untrusted data into shell
syntax.

### Scenario 4: alternatives

Given one recommendation and two complete alternatives, the answer leads with
only the recommendation. Alternatives may appear separately but cannot be
phrased as two additional next actions.

### Scenario 5: exact consumer

Given a consumer that declares exact output, the implementation calls the
deterministic renderer directly. A model-produced visually identical block does
not satisfy the scenario.

### Scenario 6: misleading standard headings

Given prose with every historical heading but the wrong lifecycle state or
accountable role, the adaptive case fails. Formatting cannot compensate for a
semantic mismatch.

## Property and invariant tests

- For every schema-2 fixture, direct exact rendering is deterministic across
  repeated runs.
- Reordering or paraphrasing adaptive output cannot change closed identifiers,
  enums, decisions, or command arguments.
- Empty optional fields may be omitted; non-empty blockers and decisions may
  not.
- The number of recommended next actions is exactly one for every valid
  handoff.
- Alternatives are a set of workflow-declared complete procedures and never
  enlarge the primary recommendation.
- No presentation changes the source result, repository bytes, Git state,
  lifecycle state, credentials, or an external system.
- Every material non-effect remains visible when omission could imply that the
  effect occurred.

## Static and architecture checks

- Candidate `ENGINEERING_HARNESS.md`, `WORKFLOW.md`, `AGENTS.md`, and
  `CLAUDE.md` templates use one consistent semantic-fidelity rule.
- The router points to the workflow owner without duplicating a conflicting
  field-order rule.
- `WORKFLOW.json`, schema-2 restitution fields, workflow selection, gate IDs,
  decision rights, and procedure registry remain unchanged unless separately
  approved.
- The direct renderer continues to depend on schema-2 validation.
- Adaptive presentation does not become a dependency of workflow computation.
- No model SDK, network client, heuristic prose parser, provider-specific rule
  engine, or runtime dependency is introduced.
- Public notes distinguish structured authority, direct exact rendering, and
  adaptive presentation.
- Managed distribution parity, package-data, lock, and fresh-install checks
  pass.

## Security and privacy checks

- Inject headings, prompt text, command delimiters, control characters,
  terminal escapes, paths, and decision-like language into result strings.
- Confirm injected content cannot add an artifact, decision, alternative, or
  next action.
- Confirm canonical argv values remain data and are never executed or joined
  into a shell expression.
- Confirm handoffs expose no credentials, hidden prompt content, evaluator host
  path, or unrelated artifact body.
- Confirm invalid, oversized, or malformed schema-2 inputs fail before
  presentation without partial repository effects.

## Performance and resilience checks

- Repeat direct rendering at the schema's bounded list and string sizes and
  confirm linear behavior.
- Confirm the change adds no network call, graph traversal, model invocation,
  or filesystem write to direct rendering.
- Exercise interrupted display, invalid UTF-8 fixture input, read-only
  repository, and Windows/POSIX display cases while preserving the structured
  result and argument boundaries.
- Run the full repository suite on supported Python versions and the candidate
  package/fresh-install boundary selected by the work order.

## Manual assessments

- Requirements and product owners confirm the adaptive examples communicate
  outcome, work done, work remaining, authority, and one next action more
  clearly than the fixed block without weakening meaning.
- Technical and quality owners classify each non-effect fixture as material or
  safely omittable and record the rationale.
- Assurance reviews representative Claude Code and Codex answers for completed,
  blocked, and decision-required cases. This is supported-adapter evidence, not
  a claim that all future host output is enforceable.
- Repository owner confirms exact-output consumers still use direct rendering
  and that managed root files were not edited in the candidate checkout.

## Evidence retention

Retain under
`docs/engineering/workflow-execution/evidence/WO-WEX-003-verification.md`:

- evaluator identities and exact candidate commit when assurance is prepared;
- structured fixture and expected-projection digests;
- direct-renderer byte snapshots and repeatability results;
- adaptive positive and negative case results by semantic field;
- changed-path and execution-scope comparison;
- candidate instruction consistency and root managed non-change proof;
- focused, full-suite, package-data, installation, and distribution-parity
  commands with exit status and runtime;
- dependency and network-absence checks;
- manual owner and supported-adapter assessments;
- deviations, residual uncertainty, and intentionally unperformed lifecycle,
  Git, release, publication, deployment, and external actions.

## Residual uncertainty

No repository can guarantee every future answer emitted by an external model
host. Fixture and manual reviews establish conformance for supported adapters
and representative cases, while the structured result remains the auditable
authority. Natural-language nuance may still make a fact ambiguous; exact or
high-stakes consumers must display structured data or direct renderer output.

This uncertainty does not permit an agent to recompute lifecycle legality,
omit a material blocker or non-effect, invent authority, or recommend a second
next action.
