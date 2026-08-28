+++
id = "SPEC-WEX-002"
type = "specification"
title = "Scoped compliance, procedure, and restitution contract"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
specifies = ["REQ-WEX-007", "REQ-WEX-008", "REQ-WEX-009", "REQ-WEX-010"]
+++

# Specification: Scoped compliance, procedure, and restitution contract

## Scope

This specification extends `SPEC-WEX-001` with four provider-neutral controls:

1. selected execution and restitution scope;
2. executable quality-gate evaluation at fixed checkpoints;
3. one concise canonical iteration restitution; and
4. typed workflow procedures bound to exact commands or decisions.

`SPEC-WEX-001` remains authoritative for focus projection, lifecycle edges,
atomic transition planning and application, preparation provenance, independent
lifecycle records, and the version-1 workflow result. This specification does
not add trusted-base lifecycle-diff validation, intercept arbitrary editor
writes, authenticate a claimed actor, or authorize external action.

A bounded iteration starts when an operator selects one `WO-*`, `VREC-*`, or
`RLS-*`, or explicitly selects a definition transition packet. It ends when the
selected procedure completes, blocks, or reaches a decision step and emits its
final restitution.

## Actors and external systems

- Operators and coding agents select scope, declare the complete change set
  visible to them, invoke checkpoint evaluation, and return the canonical
  restitution without additions.
- Product, technical, engineering, assurance, repository, release, and service
  owners exercise only the decision rights assigned by
  `DECISION_RIGHTS.md`.
- `harnessctl` resolves scope, procedures, gates, and restitution. Prompts,
  Skills, agent adapters, and dashboards are consumers, never alternative rule
  engines.
- The filesystem and repository contain untrusted paths, artifacts, evidence,
  and procedure parameters.
- Git MAY supply candidate identity to existing provenance commands. It is not
  used as a trusted change baseline by this contract.

## Inputs

### Work-order execution scope

Every new work order that authorizes implementation declares:

```toml
[execution_scope]
paths = ["se_harness/workflow.py", "tests/workflow/", "templates/repository/standard/docs/engineering/"]
```

An entry ending in `/` admits that repository-relative directory and every
descendant. Any other entry admits exactly one repository-relative path. Entries
use `/`, must be normalized, must not be absolute or empty, and must not contain
`.` or `..` components, backslashes, wildcards, drive prefixes, URI syntax, or
NUL/control characters. Duplicate and case-ambiguous entries are invalid.

Lifecycle writes planned by `harnessctl transition`, new records prepared by
governed preparation commands, and work-order-keyed evidence writes are checked
against their command-specific mutation contracts from `SPEC-WEX-001`; they are
not made legal merely by adding their paths to `execution_scope`.

### Checkpoint command

```text
harnessctl check [TARGET] --artifact ID --checkpoint start|pre-action|handoff
  [--procedure PROC-ID] [--changed-path PATH ...] [--changes-complete]
  [--change-manifest PATH] [--json]
```

- `--artifact` selects exactly one `WO-*`, `VREC-*`, or `RLS-*`.
- `--procedure` is required for `pre-action` and must equal the procedure
  selected by the active workflow rule or one of its declared alternatives.
- `--changed-path` may repeat. `--changes-complete` is the caller's explicit
  assertion that the supplied list is complete, including an intentionally
  empty list.
- `--change-manifest` is mutually exclusive with `--changed-path` and
  `--changes-complete`. It names a UTF-8 JSON document with schema
  `se-harness-change-set-v1`, Boolean `complete`, and an ordered `paths` array.
- A caller assertion is retained as evidence but is not proof that an
  undeclared path was not changed. Without a complete assertion, path-scope
  predicates report `not_assessable`.
- `transition` and provenance-preparation commands invoke the same checkpoint
  engine internally before their existing mutation planner applies a write.
- `check` always emits the schema-2 semantic result. Existing `focus`,
  `transition`, and preparation commands gain `--result-schema 1|2` during the
  compatibility window; schema 1 cannot express the new `not_done`,
  `blocked_by`, gate, or procedure fields. *Amended 2026-08-28 under
  `WO-ECP-005` (`REQ-ECP-010`): the window has closed; every one of those
  commands emits schema 2 only and `--result-schema` is an argument error.*

### Machine-readable policy

- `WORKFLOW.json` schema `se-harness-workflow-v2` owns transitions, ordered
  rules, procedure bindings, effects, non-effects, and restitution selection.
- `QUALITY_GATES.json` schema `se-harness-quality-gates-v1` owns executable gate
  and predicate IDs, evaluation triggers, evidence requirements, and evaluator
  keys. `QUALITY_GATES.md` owns explanatory policy and is the bound human
  rendering of those executable fields; it must not redefine them.
- The installed JSON files must be byte-identical to the packaged contracts
  loaded by `harnessctl`.
- `WORKFLOW.md` binds each workflow row to one `PROC-*` ID and renders its
  ordered steps. It must not substitute an unbound natural-language directive.

The workflow procedure registry uses this shape; kind-specific fields not shown
for a step are forbidden:

```json
{
  "procedures": [{
    "id": "PROC-WO-START",
    "parameters": [{"name": "artifact_id", "type": "artifact_id", "cardinality": "one", "source": "selection.primary"}],
    "steps": [
      {"id": "STEP-FOCUS", "kind": "command", "argv": ["harnessctl", "focus", ".", "--artifact", "{artifact_id}"], "gate_ids": [], "effects": [], "non_effects": []},
      {"id": "STEP-DECIDE", "kind": "decision", "decision_right": "DR-WO-START", "role": "engineering-owner", "artifact": "{artifact_id}", "outcomes": ["start", "stop"], "response": "Start {artifact_id} implementation.", "effects": [], "non_effects": []}
    ]
  }]
}
```

Scalar and repeated parameter cardinalities are `one`, `zero_or_one`, and
`one_or_more`; types are closed contract enums. A `reference` step contains
exactly one `procedure_id`; a step declaring `action_id` is rejected as a
withdrawn form. The quality-gate registry contains
`gates[]`, each with unique `id`, `checkpoints`, and `predicates[]`; each
predicate has unique `id`, one closed `evaluator` key, and non-empty
`required_evidence` descriptors.

### Repository-wide inspection

Invoking `harnessctl inspect` is an explicit repository-wide maintenance
operation. Its human and JSON outputs identify `mode = repository_wide`, contain
no selected artifact, and cannot serve as selected-iteration restitution.
Selected procedures must use `focus` or `check`; they must not invoke `inspect`.

## Outputs

Schema 2 extends the operation, selection, scope, state, findings, and mutation
data from `SPEC-WEX-001` and adds compliance, procedure, and restitution:

```json
{
  "schema": "se-harness-workflow-result-v2",
  "operation": {"kind": "check", "outcome": "completed|blocked"},
  "selection": {"primary": "WO-...", "artifacts": ["WO-..."]},
  "scope": {
    "mode": "selected",
    "governing": [],
    "dependencies": [],
    "declared_paths": [],
    "changed_paths": [],
    "change_set_complete": true
  },
  "compliance": {
    "checkpoint": "handoff",
    "workflow_rule_id": "WFL-...",
    "procedure_id": "PROC-...",
    "status": "pass|fail|not_assessable",
    "gates": [{
      "id": "QG-...",
      "status": "pass|fail|not_assessable",
      "predicates": [{
        "id": "QGP-...",
        "status": "pass|fail|not_assessable",
        "evidence": [{"kind": "artifact|command|path|result", "reference": "..."}],
        "message": "exact predicate result"
      }]
    }]
  },
  "procedure": {
    "id": "PROC-...",
    "current_step": "STEP-...",
    "steps": []
  },
  "restitution": {
    "outcome": "completed|blocked",
    "done": [],
    "not_done": [],
    "blocked_by": [],
    "current_lifecycle_state": [],
    "decision_required": null,
    "next": {"procedure_id": "PROC-...", "step_id": "STEP-...", "action": "..."},
    "command_or_response": {"kind": "command|response", "argv": [], "value": ""},
    "alternatives": []
  }
}
```

`decision_required` is either `null` or an object containing `decision_right`,
`role`, `artifact`, `decision`, and permitted outcomes. Command results use
canonical argument arrays as the machine authority. The human renderer applies
documented platform quoting without changing argument values.

The human restitution contains only these headings in this order: `Outcome`,
`Done`, `Not done`, conditional `Blocked by`, `Current lifecycle state`,
`Decision required`, `Next`, `Command or response`, and conditional
`Alternatives`. It contains no introduction, conclusion, repository-health
summary, or provider-authored next action.

## State model

| Checkpoint | Trigger | Required evaluation | Permitted result |
|---|---|---|---|
| `start` | Before implementation begins | selected scope, active workflow rule, `QG-G3-WORK-AUTHORIZATION`, start procedure | begin only on `pass`; otherwise stop |
| `pre-action` | Before the next command, decision, preparation, or external action | selected procedure step and every gate bound to it | expose or perform only the bound step on `pass` |
| `transition` | During transition planning and again immediately before apply | transition rule, selected IDs, required gates, decision input, proposed graph | plan/apply only on `pass` |
| `handoff` | Before the actor yields after completion or failure | final scope, declared change set, applicable completion gates, procedure position, restitution | always emit restitution; success requires `pass` |

Predicate status is `pass`, `fail`, or `not_assessable`. A gate is `fail` when
any predicate fails; otherwise it is `not_assessable` when any predicate is not
assessable; otherwise it is `pass`. Checkpoint status uses the same precedence.
No numeric or aggregate health score participates in lifecycle eligibility.

## Behavioral rules

### Scope confinement

1. Derive artifact scope using `SPEC-WEX-001`; do not use arbitrary graph
   reachability.
2. Classify findings as selected, repository-integrity, or unrelated using the
   fixed classifier. Only integrity failures that prevent reliable selected
   evaluation are repository blockers.
3. Compare every supplied changed path with `execution_scope.paths` after safe
   normalization. Every path must match one exact entry or admitted prefix.
4. Reject the entire governed mutation when one planned artifact or path is out
   of scope. Never expand scope automatically.
5. Exclude unrelated finding details, IDs, decisions, and actions from selected
   results. When present, background is one count and never a blocker or next
   step.
6. A repository-wide inspection remains separately labeled and is never merged
   into a selected result.
7. Repository-integrity blockers are limited to damaged managed policy or lock
   integrity, unreadable required repository context, duplicate formal IDs,
   invalid machine-policy contracts, parser failure that prevents construction
   of the complete formal graph, or an unsafe path escape. Every other formal
   finding is scoped by its affected artifact/path or classified as unrelated.
8. The evaluator may read managed policy and graph metadata outside the selected
   set only to establish integrity and typed relations. It must not return
   unrelated artifact bodies or use those reads to enlarge selected work.

### Compliance

9. Resolve the first matching workflow rule before selecting its gates or
   procedure. A caller cannot override rule ordering with `--procedure`.
10. Resolve every gate ID through `QUALITY_GATES.json` and every predicate's
   closed evaluator-key registry. Unknown or duplicate IDs invalidate the
   contract.
11. Evaluate all required predicates and retain exact evidence references and
   messages. Do not stop after the first failure in a read-only check when later
   predicates can be evaluated safely.
12. Treat absent, unreadable, stale, incomplete, or external required evidence
    as `not_assessable`.
13. Evidence is fresh only when it identifies the selected artifact and
    checkpoint and is bound to the current formal-snapshot digest. Command
    evidence also identifies canonical argv, exit status, and the digest
    manifest for its declared inputs. Elapsed time alone neither proves nor
    invalidates freshness.
14. Prevent a governed action or success claim unless the applicable checkpoint
    is `pass`. A failed handoff check still emits a blocked restitution.
15. A passing gate provides evidence only. It does not authenticate an actor,
    exercise a decision right, or authorize the next step.

### Procedures

16. Each workflow rule contains one `procedure_id`. A legal alternative names a
    different complete procedure, not an untyped prose branch.
17. Each procedure contains a stable ordered list of uniquely identified steps
    of kind `command`, `decision`, or `reference`.
18. A command step stores canonical `argv`, declared scalar or repeated
    parameters, parameter sources, effects, non-effects, and gates. It contains
    no shell expression or executable repository text.
19. A decision step stores the decision-right ID, accountable role, selected
    artifact expression, permitted outcomes, response template, effects, and
    non-effects. Procedure execution stops until that exact decision is
    supplied.
20. A reference step contains exactly one other procedure ID. A step declaring
    an `action_id` is rejected at contract validation as a withdrawn form,
    before resolution. Repository-specific operations are owner prose, not
    resolvable steps. References cannot escape the repository, form a cycle, or
    resolve ambiguously.
21. Resolve placeholders only from declared typed parameters. Missing required
    values block the step; unknown placeholders invalidate the contract.
22. A procedure contains at most 64 steps. Procedure-to-procedure references
    have maximum resolved depth 8; every direct or indirect cycle is invalid.
23. The standard `PROC-WO-START` procedure contains, in order: selected `focus`,
    start preflight, `DR-WO-START` decision, transition preview, transition
    apply, and final `focus`. Apply cannot be reached before the decision.
24. `WORKFLOW.md` rows identify the exact procedure ID. Phrases such as "run
    preflight", "inspect", "select", "resolve", or "use exact inputs" are
    nonconforming when used as actionable instructions without a command or
    fixed reference.

### Restitution

25. `done` contains only effects observed in this iteration. Equal effect types
    are grouped with stable ID/path ordering; command logs and narrative are
    excluded.
26. `not_done` contains only an authorized or expected effect in the selected
    procedure that remains incomplete. It is empty otherwise and renders as
    `None.`
27. `blocked_by` is present only for a blocked outcome and contains exact failed
    or non-assessable predicate IDs and messages.
28. `current_lifecycle_state` reports actual selected IDs and final states. It
    does not project related state as if transitioned.
29. `decision_required` is null or names one exact decision-right, role,
    artifact, decision, and permitted outcomes.
30. `next` names exactly one legal current procedure step. Alternatives appear
    only when the selected rule declares complete legal alternative procedures.
31. `command_or_response` is derived from the current typed step. It cannot be
    authored independently by a renderer or adapter.
32. Each human entry states one fact or action in one direct sentence. No fixed
    word limit may hide required effects, blockers, IDs, or decisions.
33. A conforming agent adapter returns the canonical human block verbatim when
    yielding a lifecycle result. It may transport the JSON separately but must
    not add findings, decisions, recommendations, or surrounding prose.

## Error and recovery behavior

| Code | Condition | Required result |
|---|---|---|
| `WEX200` | missing, invalid, or ambiguous execution scope | `not_assessable`; no governed mutation |
| `WEX201` | declared changed artifact or path is outside scope | `fail`; identify exact item; no governed mutation |
| `WEX202` | repository-wide output is used as selected restitution | `fail`; require selected `focus` or `check` |
| `WEX210` | workflow rule, gate, predicate, or evaluator cannot resolve | `fail`; contract invalid |
| `WEX211` | required predicate fails | `fail`; report predicate and evidence reference |
| `WEX212` | required evidence is unavailable or incomplete | `not_assessable`; report missing evidence |
| `WEX220` | procedure or step binding is missing, cyclic, or ambiguous | `fail`; contract invalid |
| `WEX221` | required procedure parameter cannot resolve | `not_assessable`; identify parameter |
| `WEX230` | restitution violates schema, ordering, or single-next rule | `fail`; do not present it as canonical |

Checkpoint failure writes nothing. A transition or preparation failure retains
the no-partial-write guarantees from `SPEC-WEX-001`. A failed handoff check
reports completed effects honestly, marks incomplete expected effects under
`Not done`, and recommends one retry or accountable escalation.

## Data and interface contracts

- `execution_scope.paths` uses the exact/prefix grammar defined above.
- `se-harness-change-set-v1` contains only `schema`, `complete`, and `paths`;
  unknown keys are rejected.
- `se-harness-workflow-v2`, `se-harness-quality-gates-v1`, and
  `se-harness-workflow-result-v2` reject unknown required enums, duplicate IDs,
  unresolved references, and unknown placeholders.
- A procedure has at most 64 steps and a procedure reference chain has at most 8
  resolved levels.
- Predicate IDs use `QGP-*`; procedure IDs use `PROC-*`; step IDs are unique
  within one procedure and use `STEP-*`. The `CTX-ACT-*` action-ID grammar is
  withdrawn and is not reused for another purpose.
- Procedure command templates store argument arrays, never shell command
  strings. Human display is derived from the array.
- Evidence entries are references and digests where applicable, not arbitrary
  evidence bodies.
- Machine arrays retain declared procedure order or stable artifact/path/rule
  order as applicable.

## Security and privacy properties

- Treat change manifests, path entries, procedure parameters, evidence
  references, and policy JSON as untrusted. No procedure step resolves content
  from a file the harness does not govern.
- Normalize and constrain all paths before matching or reading; reject path
  traversal, absolute paths, alternate separators, case ambiguity, links that
  escape the repository, and device or URI syntax.
- Never evaluate a procedure command through a shell. Machine consumers receive
  argument arrays; display quoting is not execution.
- Never interpolate repository text into a command, decision right, procedure
  ID, evaluator key, or suggested response.
- Normal selected output does not reveal unrelated artifact text, evidence
  bodies, environment values, credentials, or private URLs.
- The tool retains actor assertions as data and states that it cannot prove
  authority.

## Performance and capacity

- Index formal artifacts and machine contracts once per checkpoint.
- One checkpoint performs no more than one full formal validation plus indexed
  selected-scope, gate, and procedure traversal.
- At 1,000 formal artifacts and 10,000 declared changed paths, runtime and memory
  must remain bounded by the formal index, policy registries, evidence
  references, and path list; no network or non-standard runtime dependency is
  introduced.

## Observability

- Every result identifies selected versus repository-wide mode, primary ID,
  workflow rule, procedure, current step, checkpoint, gates, predicates,
  evidence references, scope classification, change-set completeness, outcome,
  decision boundary, and next step.
- Human and JSON output derive from one semantic result and use stable ordering.
- Contract validation reports the exact policy file, ID, and reference for
  conformance errors.
- Retained work-order evidence records candidate and released-evaluator
  identities separately, exact commands, result-schema version, and exit status.

## Compatibility and migration

- Existing schema-1 focus, transition, and preparation behavior remains governed
  by `SPEC-WEX-001`. Those commands support explicit schema 2 during one
  published compatibility window, and schema 2 becomes their default only in
  the release that advertises that interface change. The new `check` command has
  no schema-1 form. *Retirement amendment of 2026-08-28 under `WO-ECP-005`
  (`REQ-ECP-010`, `SPEC-ECP-005` `ECP-KRN-001` to `-003`): the compatibility
  window is closed without a no-op flag; schema 1, its builder, its
  projection and the `handoff` blocks of `WORKFLOW.json` are removed, and each
  rule carries only the `done` and `current_lifecycle_state` restitution
  prose. The sentences above are retained as history.*
- Schema 1 is rendered from the same internal result but omits new fields; it
  cannot be used as proof of REQ-WEX-007 through REQ-WEX-010 compliance.
- `inspect` remains repository-wide and read-only. It gains an explicit mode
  label but no selected-scope semantics.
- Existing completed work orders are not retroactively rejected for lacking
  `[execution_scope]`. A new or resumed implementation without that declaration
  reports `not_assessable` until an accountable scope revision supplies it.
- Existing free-form workflow commands remain readable only during the same
  compatibility window. New or changed rules must have typed procedures; after
  the window, any unbound actionable directive invalidates the contract.
- Managed templates, packaged policy, documentation, help, and conformance tests
  advance together through the standard released-evaluator boundary.
- Python 3.11+, standard-library runtime, no network dependency, and one standard
  installation remain mandatory.

## Examples and counterexamples

- **Conforming selected handoff:** `check --artifact WO-ABC-001 --checkpoint
  handoff --change-manifest target/WO-ABC-001-changes.json`
  accepts only paths declared by that WO, suppresses unrelated findings, reports
  each required predicate, and returns one canonical next procedure step.
- **Conforming start directive:** the `WFL-WO-START` row references
  `PROC-WO-START`; its current command step renders `harnessctl preflight .
  --work-order WO-ABC-001 --phase start` exactly.
- **Conforming decision stop:** after start preflight passes, the procedure emits
  a `DR-WO-START` response request and cannot expose transition apply as the
  current step until the engineering-owner decision is supplied.
- **Nonconforming:** selected restitution copies findings from `harnessctl
  inspect` concerning unrelated work orders.
- **Nonconforming:** a complete change-set assertion contains one path outside
  `execution_scope`, but the final handoff still reports success.
- **Nonconforming:** `WORKFLOW.md` says only "Run capture-verification with exact
  inputs" and no exact command or procedure ID owns those inputs.
- **Nonconforming:** a passing gate is described as approval, or a missing test
  result is treated as pass.
- **Nonconforming:** an adapter adds its own analysis or second recommended next
  action after the canonical restitution.

## Explicitly unspecified decisions

- Internal Python module, class, and function names.
- In-memory index, cache, and immutable result-object implementation.
- Exact test fixture layout and golden-file storage.
- Terminal color and wrapping that do not alter headings or semantic values.
- Whether human documentation is generated or conformance-compared, provided
  byte-stable policy ownership and every binding rule above hold.

The public checkpoint command, scope grammar, policy schemas, gate aggregation,
procedure step kinds, schema-2 restitution fields and order, compatibility
boundary, and failure codes are not delegated implementation choices.
