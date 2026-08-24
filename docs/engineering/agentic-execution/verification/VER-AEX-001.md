+++
id = "VER-AEX-001"
type = "verification"
title = "Independent agentic execution conformance contract"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
verifies = ["REQ-AEX-001", "REQ-AEX-002", "REQ-AEX-003", "REQ-AEX-004", "REQ-AEX-005", "REQ-AEX-006", "REQ-AEX-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T09:03:54Z"
decided_by = "assurance-owner"
+++

# Verification Contract: Independent agentic execution conformance contract

## Independence

Primary acceptance uses verifier-owned fixtures and installed public interfaces
in disposable repositories. The expected authority boundary, autonomy envelope,
decision packet, execution receipt, skill result, orchestration result, and
adapter plan come from the approved formal contracts and verifier-maintained
oracles. Tests must not import candidate authorization, scope, receipt,
orchestration, or adapter code as their source of expected results.

The same scenario corpus is exercised through command-driven execution and the
single-agent skill path. Optional multi-agent and runtime-adapter paths must
produce semantically equivalent governed results. Candidate unit tests,
implementer-authored snapshots, worker summaries, and successful runtime
execution are supplementary evidence only. The target repository's exact
released evaluator remains external to the checkout and is identified
separately from candidate source and candidate packages.

Verification can establish conformance of asserted roles, scopes, decisions,
effects, and evidence. It cannot prove a person's real-world identity, the
substantive quality of an accountable judgment, or enforcement by an
unsupported runtime.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-AEX-001` authority separation | black-box role/profile/permission matrix, complete decision-right catalog comparison, and static contract review | all 12 current managed decision rights, unknown future right, accountable roles, similarly named profiles, unrestricted runtime permissions, absent actor assertion, conflicting assertions | the catalog and classification are complete; unknown rights fail to `accountable-decision-required`; no execution profile, model capability, tool access, or runtime permission supplies an accountable decision fact |
| `REQ-AEX-002` bounded delegation | envelope parser, stale-state fixtures, scope and transaction fault injection | missing or stale work order, operation/path denial, parent-child narrowing, retry exhaustion, parallel-writer limit, interrupted write | invalid or expanded delegation fails before effects; every child is equal or narrower; failure leaves no unplanned partial mutation |
| `REQ-AEX-003` decision points | semantic human/JSON comparison and decision-class matrix | `routine-read-only`, `advance-delegation-required`, `accountable-decision-required`, `action-time-authorization-required`, failed gate, not-assessable gate, multiple apparent choices | accountable decisions and action-time-authorized actions stop before effects and emit exactly one complete primary decision with the required accountable role |
| `REQ-AEX-004` execution evidence | canonical JSON vectors, deterministic receipt corpus, retention-boundary checks, and failure injection | completion, degradation, stop, failure, timeout, cancellation, missing worker result, rollback failure, large output, secret-bearing input | canonical bytes and digest match independent vectors; every requested worker and governed effect is represented; read-only receipts are returned without target retention; identities remain distinct; secrets and hidden reasoning are absent |
| `REQ-AEX-005` portable skills | canonical-source and installed-package inspection, manifest vectors, and command/skill equivalence | explicit and implicit activation, non-match cases, missing or modified skill, LF variants, unsupported feature, duplicate package copy, single-agent fallback | `.agents/skills/harness-orient/` is installed once from the canonical template; contract and digest validate; skill procedure invokes harness-owned rules, grants no authority, and preserves the command-driven governed result |
| `REQ-AEX-006` read-only orientation | exact-evaluator 0.5.0 capability matrix, fresh-install, and hostile-repository black-box tests with pre/post digests | valid repository, invalid graph, missing or old evaluator, candidate/released skew, managed damage, unsupported focus, selected artifact, read-only filesystem | required operations block honestly, optional focus degrades only selected scope, output is decision-ready and correctly labeled, and repository, Git, lifecycle, environment, and external-state digests remain unchanged |
| `REQ-AEX-007` bounded orchestration and adapters | single/multi-agent equivalence, worker-failure corpus, deterministic adapter plans | read-only parallelism, overlapping writers, isolated disjoint writers, stale integration, conflict, disabled subagents, unsupported runtime | fallback remains correct; all workers are visible; writers are safely bounded; derived adapters cannot alter authority or owner content |

## Acceptance scenarios

1. A worker profile named `assurance-owner` runs tests but cannot create a
   verification decision or verification record.
2. Workspace-write or unrestricted tool permission does not authorize a
   governed mutation absent the selected work order and applicable envelope.
3. An envelope whose work-order digest, repository observation, evaluator
   digest, operation, path, or parent scope no longer matches fails before a
   write.
4. A child delegation that adds a path, operation, profile, retry, writer, or
   later stop boundary is rejected.
5. A `routine-read-only` operation can continue, while an architecture,
   assurance, release, risk, credential, publication, or other accountable
   decision or external action stops with one decision packet.
6. A failed or not-assessable required gate cannot be rendered as approval,
   successful completion, or an authorized next effect.
7. Human and JSON decision packets represent the same decision, facts,
   uncertainties, effects, non-effects, and suggested response.
8. A completed, stopped, failed, timed-out, cancelled, or output-missing worker
   appears in the aggregate receipt with its actual outcome.
9. `harness-orient` on a pristine installed repository reports exact released
   evaluator identity, formal state, blockers, and next decision without
   changing any byte or Git reference.
10. A missing exact evaluator produces an install or escalation instruction but
    does not install software, use candidate source as the governor, or change
    the target.
11. Modified skill instructions cannot make a prohibited lifecycle transition
    pass or change the accountable role required by managed policy.
12. Disabled subagents and unavailable runtime-specific features select the
    deterministic single-agent fallback and preserve the governed result.
13. Required writers with overlapping scope are rejected; later disjoint
    writers use isolated worktrees and one integration coordinator.
14. Adapter configuration is a deterministic derivation of approved portable
    contracts, preserves owner-controlled content, and reports unsupported
    features rather than silently weakening the contract.
15. The verifier compares every current managed decision-right ID with the
    `SPEC-AEX-001` table, rejects a missing or duplicate row, and classifies a
    synthetic future right as `accountable-decision-required`.
16. Skill manifest vectors prove stable path ordering, LF/CRLF/CR equivalence,
    changed-byte sensitivity, runtime-overlay exclusion, required-file coverage,
    and rejection of symlinks, case collisions, escapes, and invalid UTF-8.
17. Source distribution, non-promotable ephemeral wheel, and fresh standard
    installation contain one canonical `harness-orient` core and no
    `se_harness/skills/` duplicate.
18. Exact released evaluator 0.5.0 completes version, identity, doctor,
    validation JSON, and inspection JSON. A selected artifact reports
    `focus-json` as unavailable, sets selected scope to `not_assessable`, and
    returns `degraded` without invoking candidate source.
19. A missing required evaluator operation, identity mismatch, integrity
    failure, malformed required JSON, or evaluator older than 0.5.0 returns
    `blocked` or `failed` as specified and leaves every observed state digest
    unchanged.
20. Independently encoded decision packets and receipts match
    `se-harness-canonical-json-v1`; read-only orientation returns its receipt
    inline and creates no evidence file in the target.

## Property and invariant tests

- Accountable authority is a function of valid formal state, managed decision
  rights, and an explicit actor assertion; it is invariant under model, profile,
  sandbox, permission, tool, and worker-name changes.
- An autonomy envelope and every child envelope are monotonic restrictions of
  the approved work order; no normalization, default, retry, or fallback widens
  them.
- Every governed write is preceded by a successful identity and scope recheck;
  a failed recheck changes no governed byte.
- Permuting filesystem enumeration, worker completion order, JSON key insertion,
  locale, or runtime scheduling does not change canonical semantic output.
- Receipt coverage equals the requested worker set, including unsuccessful and
  absent outputs; summary filtering cannot create complete coverage.
- Human and machine renderings decode to the same selected scope, lifecycle
  state, blockers, decision, next step, effects, non-effects, and evidence.
- A skill, profile, adapter, receipt, or successful command cannot create a
  lifecycle event, accountable decision, or wider runtime permission.
- Command-driven and skill-driven execution produce equivalent governed state
  and decision boundaries for every common fixture.
- Read-only execution changes no repository file, Git state, environment
  configuration, credential store, network service, or external system.
- The managed decision-right set equals the classified set; an unclassified
  future ID is `accountable-decision-required` and can never become
  `advance-delegation-required` through a default.
- Portable skill digest equality is invariant under LF, CRLF, and CR line
  endings and enumeration order, but changes for any canonical content or path
  change.
- A missing optional evaluator operation can change only its declared output to
  `not_assessable` and the overall outcome to `degraded`; it cannot change
  authority, repository findings, or required-operation results.

## Static and architecture checks

- Confirm lifecycle rules, decision rights, gates, and mutation legality have
  one normative harness-owned source and are not duplicated in `SKILL.md`,
  profiles, adapters, prompts, or provider configuration.
- Confirm dependency direction remains authority contract to portable skill to
  execution profile to adapter, with evidence flowing back without authority.
- Confirm logical execution profiles do not use accountable role names as
  authority and runtime defaults are absent from the portable core contract.
- Confirm every mutable interface has strict schemas, stable diagnostics, safe
  paths, plan-before-apply behavior, rollback, and explicit effect/non-effect
  reporting.
- Confirm the standard repository template is the canonical managed source;
  root managed files are changed only by approved refresh or upgrade procedures.
- Confirm the only portable pilot source is
  `templates/repository/standard/.agents/skills/harness-orient/`, the installed
  target is `.agents/skills/harness-orient/`, `skill-contract.json` is retained,
  and no authoritative `se_harness/skills/` copy exists.
- Confirm package data, installer, managed lock, fresh installation, safe
  upgrade, and distribution parity include the approved skill inputs exactly.
- Confirm `WO-AEX-001` admits every changed installer, contract, package,
  documentation, test, and evidence path and admits no CLI, workflow-policy,
  adapter, subagent, or second-runtime implementation surface.
- Confirm `WO-AEX-001` selects only read-only `harness-orient`; autonomy-envelope
  mutation, additional skills, subagent orchestration, writer worktrees, and
  runtime adapter materialization require later work orders.
- Confirm candidate source, candidate packages, and the exact released evaluator
  are labeled and invoked as distinct identities.

## Security and privacy checks

- Exercise absolute, traversal, dot-component, alternate-separator, drive,
  device, URI, wildcard, symlink/junction escape, case-collision, reserved-name,
  control-character, and invalid-encoding paths.
- Exercise duplicate JSON keys, unknown fields, invalid enums, repeated IDs,
  excessive nesting, oversized values, malformed digests, and ambiguous scope
  prefixes in every proposed machine contract.
- Treat skill text, repository content, model output, profile metadata, adapter
  configuration, commands, evidence paths, and worker results as untrusted.
- Exercise quotes, whitespace, newlines, shell metacharacters, substitutions,
  redirects, option-like values, and structured fragments; confirm all remain
  inert arguments or data.
- Confirm no skill script, worker, receipt, packet, log, or adapter exposes
  credentials, tokens, environment dumps, hidden reasoning, private evidence
  bodies, or unrelated repository content.
- Confirm technical permission changes cannot bypass harness denial,
  accountable-decision-required stops, or action-time authorization.

## Performance and resilience checks

- Measure orientation, envelope validation, packet generation, and receipt
  generation on deterministic repositories near 100, 500, and 1,000 formal
  artifacts.
- Bound worker count, nesting, output size, retries, worktrees, and integration
  attempts; reject unbounded recursive delegation.
- Compare single-agent and optional multi-agent wall time, compute or token cost,
  coverage, conflicts, and retry rates before enabling parallel execution.
- Repeat on supported Python 3.11+ runtimes, Windows and POSIX path fixtures,
  randomized enumeration, read-only filesystems, concurrent changes, interrupted
  reads and writes, malformed runtime capabilities, and missing evaluator state.
- Inject failure at every plan, identity recheck, worker aggregation, adapter
  conflict, transactional write, rollback, receipt, and final-validation
  boundary; retain exact pre-operation state or report restoration failure.

## Manual assessments

- Product and requirements owners confirm the proposed decision classes retain
  the human judgments that determine intent and acceptance.
- Technical owners decide the architecture assessment, both proposed ADRs, the
  portable schemas and storage boundaries, and confirm the complete current
  decision classification: only WO start/completion and VREC/RLS preparation
  are `advance-delegation-required`, only related-record selection is
  `routine-read-only`, and all other current rights are
  `accountable-decision-required` or `action-time-authorization-required` as
  specified.
- Repository and engineering owners confirm each work order is narrow enough to
  implement without informal scope expansion.
- Quality and assurance owners confirm test independence, exact released-
  evaluator separation, negative cases, receipt completeness, and
  commit-bound evidence needs.
- Security, risk, service, and release owners review credential, external action,
  supply-chain, runtime-adapter, and release boundaries before those features
  enter an implementation work order.
- Representative operators confirm each decision packet is concise, presents
  one decision at the right point, and makes deferral consequences clear.

## Evidence retention

For the Phase 1 pilot, retain exact commands, runtimes, released and candidate
identities, test counts, fixture digests, pre/post read-only state manifests,
canonical packet, receipt, and skill-manifest vectors, the complete 0.5.0
capability matrix, human/JSON comparisons, hostile-input results, fresh-install
and upgrade results, non-promotable wheel inventory and hash, package and
managed-integrity parity, performance measurements, manual assessments,
deviations, and residual risks under
`docs/engineering/agentic-execution/evidence/WO-AEX-001-verification.md`.

Later work orders must name their own evidence paths and execute every applicable
row before autonomy-envelope mutation, multi-agent execution, or runtime
adapters are accepted. Implementer-generated output alone is never retained as
independent proof.

## Residual uncertainty

Repository-local contracts cannot authenticate real-world actors, guarantee
that every provider enforces requested sandbox settings, prove that a human
decision is substantively correct, or eliminate model nondeterminism. A receipt
can show declared and observed execution but cannot prove that undisclosed work
did not occur outside the trusted observation boundary.

These limitations must remain explicit in packets and retained evidence. They
do not permit inferred authority, silent feature degradation, incomplete worker
coverage, candidate-as-governor evaluation, or external action without exact
action-time authorization.
