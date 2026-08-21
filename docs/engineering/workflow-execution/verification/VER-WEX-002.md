+++
id = "VER-WEX-002"
type = "verification"
title = "Verify scoped compliance and executable restitution"
status = "approved"
owners = ["quality-owner", "assurance-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
verifies = ["REQ-WEX-007", "REQ-WEX-008", "REQ-WEX-009", "REQ-WEX-010"]
+++

# Verification Contract: Verify scoped compliance and executable restitution

## Independence

Primary acceptance invokes only installed public CLI entry points in disposable
repositories. Verifier-owned fixtures declare expected scope paths, findings,
workflow-rule selection, gate predicates, evidence status, procedure steps, and
schema-2 restitution. Tests must not import the candidate's scope matcher, gate
evaluators, procedure resolver, receipt builder, renderer, or adapter as their
oracle.

Verifier-owned parsers compare JSON with the schemas in `SPEC-WEX-002` and
compare human output with its required headings and semantic values. Candidate
unit tests, implementation snapshots, and self-reported agent summaries are
supplementary evidence only. The released evaluator remains installed outside
the checkout and is identified separately from candidate-source and
candidate-package evidence.

Verification cannot prove that a caller declared every changed path, that an
actor truly holds a role, or that a nonconforming host will return the canonical
block. It verifies honest treatment of completeness assertions, supported
adapter conformance, and failure when required evidence is absent.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-WEX-007` scope confinement | black-box checkpoint fixtures and exact path-set comparisons | exact files, directory prefixes, empty complete set, outside path, malformed path, unrelated findings, separately labeled inspection | only admitted paths and artifacts pass; out-of-scope governed mutation fails without writes; unrelated details never enter selected restitution |
| `REQ-WEX-008` executable compliance | verifier-owned gate matrix through every checkpoint | all-pass, one-fail, one-not-assessable, missing registry entry, stale evidence, transition recheck | every predicate and evidence reference is reported; aggregation follows fail/NA/pass precedence; governed action and success claim require pass |
| `REQ-WEX-009` canonical restitution | schema validation, golden human output, semantic comparison, adapter corpus | success, partial work, blocked gate, missing decision, alternatives, empty values, many effects | exact field order and meaning; honest done/not-done; exact blocker and decision; one primary next step; no unrelated or provider-added prose |
| `REQ-WEX-010` procedure binding | contract mutation corpus and resolved-procedure golden data | command, repeated parameter, decision stop, reference, unknown ID, cycle, missing parameter, vague directive | every action resolves to one typed step; commands are exact argument arrays; decisions stop; invalid or unbound directives fail conformance |

## Acceptance scenarios

1. A work order declaring one exact file and one directory prefix accepts those
   paths and descendants but rejects siblings, prefix lookalikes, alternate
   separators, absolute paths, traversal, wildcard entries, and case ambiguity.
2. An empty changed-path list with an explicit completeness assertion passes the
   path predicate when no implementation change was expected.
3. The same empty list without a completeness assertion reports
   `not_assessable` and cannot produce successful handoff compliance.
4. A valid `se-harness-change-set-v1` manifest and equivalent repeated
   `--changed-path` arguments produce the same normalized path set and result.
5. A manifest with unknown keys, duplicate paths, invalid encoding, invalid
   `complete`, or an escaping path fails without reading outside the repository.
6. One out-of-scope declared path makes the governed operation fail and leaves
   every pre-operation digest unchanged.
7. A formal lifecycle write listed as an allowed implementation path still
   fails when its transition contract does not authorize that mutation.
8. Selected `focus` and `check` results classify unrelated findings only as a
   count; no unrelated ID, message, decision, or action appears in restitution.
9. `harnessctl inspect` labels itself repository-wide, has no primary selection,
   and is rejected if supplied as selected restitution evidence.
10. Only managed/lock damage, unreadable required repository context, duplicate
    identity, invalid machine policy, graph-blocking parse failure, and unsafe
    path escape enter the repository-integrity blocker class; other findings are
    selected or unrelated by affected artifact/path.
11. Every recognized selected state resolves the first matching workflow rule,
    its exact gate IDs, and one procedure ID in stable order.
12. A caller-supplied alternative or later rule cannot override the first
    matching rule.
13. Every gate with all passing predicates reports `pass`; one
    `not_assessable` and no failure reports `not_assessable`; any failure reports
    `fail` even when another predicate is not assessable.
14. Missing, unreadable, stale, malformed, or external required evidence reports
    `not_assessable`, never pass.
15. Evidence bound to another artifact, checkpoint, formal-snapshot digest,
    command argv, exit status, or declared-input digest manifest is stale;
    timestamps alone do not change freshness.
16. Read-only checks evaluate every safely assessable predicate after an earlier
    failure and report each exact result.
17. Start, pre-action, transition, and handoff checkpoints use the same gate
    registry and aggregation rules.
18. Transition plan and apply re-evaluate required predicates; a changed input
    between them blocks apply and leaves no partial write.
19. A passing compliance result does not add lifecycle decision metadata,
    authenticate an actor, or execute its recommended action.
20. `PROC-WO-START` resolves exact `focus`, start-preflight, decision, transition
    preview, transition apply, and final-focus steps in that order.
21. The start procedure stops at `DR-WO-START` until an engineering-owner
    decision naming the artifact and target meaning is provided.
22. Scalar and repeated command parameters expand into canonical argument arrays
    without shell evaluation or order instability.
23. Missing parameters, unknown placeholders, unknown procedure IDs, duplicate
    step IDs, type mismatches, ambiguous references, and direct or indirect
    cycles invalidate the policy.
24. A 64-step procedure and an eight-level acyclic reference chain validate;
    the next step or level fails. Every cycle fails regardless of depth.
25. A `CTX-ACT-*` repository-context reference resolves exactly one matched
    begin/end marker pair; missing, duplicate, nested, mismatched, or malformed
    action blocks fail.
26. Every actionable row in `WORKFLOW.md` names its `PROC-*` binding and matches
    the ordered machine procedure. No unbound "run", "inspect", "select",
    "resolve", or "use exact inputs" instruction remains.
27. Completed restitution contains only observed effects; expected incomplete
    effects appear only under `Not done`.
28. Blocked restitution includes the exact predicate under `Blocked by`, actual
    unchanged or final state, and one safe retry or accountable escalation.
29. `Decision required` is either `None` or one exact decision right, role,
    artifact, decision, and permitted outcome set.
30. Every result has exactly one `Next`; alternatives exist only when the
    selected workflow rule names complete alternative procedures.
31. Empty `not_done` renders as `None.` and successful output omits `Blocked by`;
    blocked output includes it in the specified position.
32. Human and JSON outputs contain the same done, not-done, blockers, state,
    decision, next step, command/response, and alternatives.
33. ChatGPT-, Claude-, and Codex-facing supported adapters given the same result
    return the canonical human block byte-for-byte, with no preface, conclusion,
    extra finding, open-ended question, or second next action.

## Property and invariant tests

- Path acceptance equals exact membership or component-boundary directory-prefix
  membership after normalization; string-prefix coincidence never admits a
  path.
- Permuting filesystem enumeration, JSON object insertion, evidence discovery,
  or caller path order does not change canonical scope, gate, procedure, or
  restitution ordering.
- Selected results contain no artifact ID outside governing, dependency,
  selected mutation, or exact repository-integrity blocker evidence sets.
- An unrelated finding can change only the background count; it cannot change
  outcome, compliance, decision, next, command, or alternatives.
- A complete declared change set passes if and only if every path is admitted
  and every governed formal mutation satisfies its independent mutation
  contract.
- Gate and checkpoint status follow `fail > not_assessable > pass`; no score,
  warning count, or dashboard state changes the result.
- Every gate and predicate ID resolves once; every evaluator key is in the
  verifier-owned expected registry; every workflow gate reference resolves.
- Every procedure graph is finite and acyclic, step IDs are unique, and every
  command, decision, and reference satisfies its kind-specific schema.
- Command parameter expansion preserves each value as one argument and never
  interprets shell metacharacters, quotes, substitutions, or redirections.
- A decision step has no executable command and no later step becomes current
  before the required decision is supplied.
- Restitution fields occur once in fixed order; `next` cardinality is exactly
  one; conditional fields obey their outcome and contract predicates.
- Grouping repeated effects does not omit any selected ID or path and does not
  introduce narrative or unrelated state.
- Parsing canonical human or JSON output yields the same semantic result for
  every verifier-owned case.

## Static and architecture checks

- Confirm `WORKFLOW.json`, `QUALITY_GATES.json`, their human documents, packaged
  copies, managed lock, and runtime-loaded copies are synchronized and have one
  normative owner each.
- Confirm `WORKFLOW.md` renders or conformance-tests every workflow rule,
  procedure ID, typed step, effect, non-effect, gate, and decision-right binding.
- Confirm no parser, renderer, Skill, adapter, dashboard, or repository note
  owns a duplicate rule, gate predicate, procedure, or next-action mapping.
- Confirm public help documents every `check` input, checkpoint, change-manifest
  rule, result schema, and exit behavior.
- Confirm `inspect` remains repository-wide, while selected procedures use only
  `focus`, `check`, transition, or preparation interfaces.
- Confirm schema-1 compatibility for existing commands is derived from the same
  internal result and cannot be reported as schema-2 compliance evidence;
  confirm `check` rejects schema-1 output selection.
- Confirm an architecture decision assessment addresses the public CLI, new
  machine contracts, path-scope schema, evaluator registry, procedure graph,
  canonical output, and supported-agent adapter boundary.
- Confirm one standard installation, Python 3.11+ standard-library runtime,
  managed/repository ownership boundaries, and released-evaluator separation
  remain intact.

## Security and privacy checks

- Exercise absolute, traversal, dot-component, alternate-separator, device,
  drive, URI, symlink/junction escape, reserved-name, case-collision, and control
  character paths in scopes, manifests, evidence, and references.
- Exercise invalid UTF-8, duplicate JSON keys, deep nesting, huge scalar values,
  unknown keys, unknown enums, and repeated IDs in every new machine contract.
- Exercise shell metacharacters, quotes, whitespace, newlines, substitutions,
  redirects, format placeholders, and JSON/TOML fragments in procedure values
  and actor text; confirm they remain inert data.
- Confirm selected output cannot reveal unrelated messages, artifact bodies,
  evidence contents, credentials, environment secrets, or private URLs.
- Confirm a repository-context reference is displayed or resolved as data and
  never imported, evaluated, or executed by contract validation.
- Confirm actor assertions and passing gates are never represented as proof of
  identity, authority, approval, verification, release, or risk acceptance.

## Performance and resilience checks

- Measure start and handoff checkpoints on deterministic repositories near 100,
  500, and 1,000 formal artifacts and change sets near 0, 100, 1,000, and 10,000
  paths.
- Confirm each checkpoint performs at most one full validation and one indexed
  traversal of scope, gates, procedures, and changed paths.
- Repeat on supported Python 3.11+ runtimes, Windows and POSIX path fixtures,
  randomized enumeration, read-only filesystem, interrupted read, concurrent
  change, and malformed policy inputs.
- Confirm every failed read-only checkpoint changes no file, Git index, branch,
  commit, tag, remote, environment configuration, or external system.
- Inject failure at transition/preparation recheck and every existing atomic
  write boundary; verify the pre-operation digest set is retained.
- Run the full repository suite plus fresh-install, upgrade, managed-integrity,
  preflight, candidate-acceptance, package-data, and distribution-parity checks
  selected by the eventual work order.

## Manual assessments

- Requirements and product owners confirm selected background suppression does
  not hide a repository-integrity failure that makes safe evaluation impossible.
- Technical owners confirm exact/prefix path grammar and caller-declared
  completeness are honest without claiming trusted-base enforcement.
- Quality and assurance owners confirm every gate predicate has objective
  evidence, exact pass conditions, and correct `not_assessable` behavior.
- Decision-right owners review each procedure's decision stops, effects, and
  non-effects and confirm automation cannot cross them.
- Repository owners review schema-2 and `execution_scope` compatibility impacts
  and approve the published migration window before implementation approval.
- Supported-agent reviewers compare representative ChatGPT, Claude, and Codex
  outputs and confirm the canonical block makes done, not done, decision, and
  next action immediately visible without added prose.

## Evidence retention

Retain under the eventual WEX work-order evidence path:

- released-evaluator, candidate-source, and candidate-package identities as
  separately labeled records;
- exact commands, runtimes, test counts, duration, exit status, and environment
  boundary;
- verifier-owned scope, path, gate, procedure, and restitution fixture manifests
  with expected-result digests;
- human/JSON semantic comparisons and canonical adapter output digests;
- pre/post/failed-operation repository digest manifests;
- workflow/gate/documentation conformance and procedure-graph coverage reports;
- security, hostile-input, concurrency, interruption, and atomic-failure results;
- performance measurements at declared artifact and path scales;
- fresh-install, upgrade, managed-lock, package-data, distribution, preflight,
  candidate-acceptance, and full-suite outputs;
- manual assessments, deviations, unresolved risks, and exact changed paths.

## Residual uncertainty

Caller-declared change completeness cannot prove that an agent omitted no path;
that requires a trusted observation boundary intentionally excluded from this
packet. A repository cannot force an unsupported host to return a canonical
block, authenticate human roles, or determine whether a human judgment is
substantively correct. Black-box tests also cannot cover every shell display
quoting convention or exotic filesystem.

These limits must remain visible as evidence assertions and supported-platform
or supported-adapter boundaries. They do not permit out-of-scope governed
mutations, implicit gate passes, untyped procedures, provider-authored next
actions, or claims that this packet implements rejected `REQ-WEX-006`.
