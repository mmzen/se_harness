+++
id = "VER-AEX-002"
type = "verification"
title = "Independent single-agent skills MVP conformance"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
verifies = ["REQ-AEX-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T13:50:24Z"
decided_by = "assurance-owner"
+++

# Verification Contract: Independent single-agent skills MVP conformance

## Independence

Primary evidence comes from verifier-owned disposable repositories, hostile
input corpora, canonical expected results, and black-box installed package
interfaces. Expected outcomes are derived from approved formal contracts and
the target's exact released evaluator, not from implementer constants, skill
prose, candidate snapshots, or successful model execution.

For each representative scenario, the verifier executes the documented
command path and skill path against equivalent starting repositories and
compares governed effects, lifecycle state, gates, stops, evidence, and next
action. Candidate unit tests and implementer evidence are supplementary.

Applicable `VER-AEX-001` methods remain required for `REQ-AEX-005` and the
authority, decision-packet, receipt, portability, released-evaluator, and
single-agent invariants reused by the MVP. This contract verifies only the new
`REQ-AEX-008` obligation and does not amend `VER-AEX-001` retroactively.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-AEX-008` single-agent outcome workflow | black-box command/skill equivalence, installed-skill inventory, explicit-activation tests, lifecycle-state matrix, helper effect-sentinel tests, before/after repository and Git manifests, retained-evidence audit, and human/JSON comparison | draft creation and revision, approved versus in-progress work, successful and failed implementation, unexpected path, clean and dirty candidate, missing actor, ready VREC preparation, failed gates, stale state, absent subagents, provider-name scan, Git/external-action traps | all four skills are portable and unique; writing occurs only after explicit activation and current applicable authority; controlled effects remain inside the declared boundary; command and skill paths have equivalent governed effects and stops; receipts and evidence are complete; no skill approves, completes, verifies, delivers, releases, mutates Git, uses credentials, or performs an external action |

## Acceptance scenarios

1. `harness-draft-change` creates only the declared complete draft artifacts and
   optional declared planning note, validates the graph, and adds no lifecycle
   event.
2. Draft change rejects a used ID, a destination collision, an unselected
   existing draft, and every selected non-draft artifact before its controlled
   effect callback.
3. A natural-language match without explicit writing-skill selection changes
   no repository or Git byte.
4. `harness-execute-work-order` against an `approved` work order stops with the
   current work-start decision and invokes no implementation effect.
5. The same skill against an `in_progress` work order executes only admitted
   paths, records every command and result, retains required evidence, and
   stops before work completion.
6. Absolute, traversal, alternate-separator, case-colliding, wildcarded,
   symlink-escaping, and out-of-scope planned paths invoke zero effect callbacks.
7. A failed test or unexpected actual changed path prevents successful handoff
   and remains visible in evidence.
8. `harness-prepare-assurance` rejects a dirty or stale candidate, incomplete
   work or verification coverage, missing evidence, failed preparation gate,
   reused VREC ID, and missing preparation actor before record creation.
9. Valid assurance preparation creates exactly one `ready` VREC bound to the
   exact candidate and stops with the assurance decision packet.
10. No successful path applies an approval, work-completion, verification,
    delivery, release, Git, credential, network, or external effect.
11. The complete scenarios run without subagents and contain no provider-native
    skill, model, tool, permission, or hook dependency.
12. Fresh installation and approved upgrade place exactly one managed copy of
    all four canonical skill cores and preserve customized targets by failing
    without partial writes.

## Property and invariant tests

- Changing implicit activation from false to true on a writing skill makes its
  contract invalid.
- A missing, unknown, duplicate, malformed, or non-canonical v2 field fails
  closed; v1 orientation vectors remain byte-identical.
- Every helper-controlled effect callback count is zero unless exact evaluator
  identity, current state, selected scope, required checkpoint, and target path
  all pass immediately before invocation.
- The planned and actual changed-path sets are subsets of the selected path
  source for every completed result.
- Repository state drift between plan and pre-effect recheck always prevents
  the stale controlled effect.
- Permuting JSON keys, filesystem enumeration, and command completion order
  does not change canonical semantic output.
- Command and skill executions from identical fixtures have equal formal-state
  deltas and stop at the same managed next decision.
- Receipt completeness covers every requested operation, including failed,
  stopped, cancelled, timed-out, or missing output.
- Provider, model, sandbox, connector, and subagent availability cannot change
  authority, permitted paths, lifecycle effects, or required evidence.

## Static and architecture checks

- Confirm the three new `SKILL.md` files query harness-owned structured state
  and do not restate lifecycle legality, gate predicates, or accountable role
  mappings.
- Confirm `harness-orient` source, v1 contract, helper, digest vectors, and
  public results remain unchanged.
- Confirm v2 has a strict closed parser and v1 readers reject it rather than
  guessing compatibility.
- Confirm canonical skill sources exist only under the standard repository
  template and installed copies are managed.
- Confirm no `se_harness/skills/` duplicate, provider overlay, workflow-policy
  edit, new lifecycle command, autonomy-envelope effect API, subagent, or
  runtime adapter is introduced.
- Confirm every changed implementation, test, documentation, distribution, and
  evidence path is admitted by `WO-AEX-003`.

## Security and privacy checks

- Exercise hostile paths, artifact IDs, actor strings, commands, JSON, Git
  output, evidence paths, skill content, and repository instructions.
- Confirm structured evaluator launchers preserve arguments as data and reject
  shell strings, redirects, substitutions, option injection, and control
  characters.
- Confirm logs, receipts, packets, and retained evidence exclude credentials,
  environment dumps, hidden reasoning, unnecessary host paths, and private
  evidence bodies.
- Confirm candidate source, an in-tree executable, runtime permission, skill
  digest, receipt, or successful test cannot substitute for exact released-
  evaluator authority.
- Inject failure before, during, and after each controlled effect. Existing
  released-evaluator transactions remain atomic, and implementation failures
  never produce a false successful handoff.

## Performance and resilience checks

- Run drafting, execution planning, changed-path comparison, and assurance
  preparation against deterministic repositories near 100, 500, and 1,000
  formal artifacts.
- Bound artifact-plan, path, command, output, evidence, and diagnostic sizes.
- Repeat on supported Python 3.11+ runtimes and Windows/POSIX path fixtures.
- Exercise read-only filesystem, interrupted process, concurrent state drift,
  locked files, malformed evaluator output, and receipt-generation failure.
- Prove no retry widens path, operation, lifecycle, candidate, evidence, or
  external-action scope.

## Manual assessments

- Product and requirements owners confirm that the representative workflow
  removes procedural interactions while retaining all accountable decisions.
- Technical and repository owners confirm the v2 boundary, canonical source,
  public evaluator dependency, and Phase 4 separation.
- Engineering and quality owners confirm the work-order scope is implementable
  without informal expansion and that unexpected changes fail handoff.
- Assurance owner confirms a prepared VREC remains a proposal and receives
  enough exact evidence for an independent decision.
- Representative operators complete one full bounded path and confirm each
  human interruption is an accountable decision or separately authorized Git
  or external action, not a routine command-selection prompt.

## Evidence retention

Retain exact source, installed evaluator, candidate package, and candidate
commit identities; all four skill manifests and digests; v1 regression and v2
canonical vectors; command/skill equivalence matrices; explicit-activation and
state-transition matrices; effect-sentinel counts; before/after repository and
Git manifests; path-scope results; command results; retained evidence digests;
ready-VREC fixtures; install, upgrade, source, wheel, and fresh-install
inventories; performance results; manual assessments; deviations; and residual
uncertainty at
`docs/engineering/agentic-execution/evidence/WO-AEX-003-verification.md`.

## Residual uncertainty

This verification can establish portable procedure conformance and the
behavior of released-evaluator and helper-controlled boundaries. It cannot
prove that a hostile runtime followed `SKILL.md`, authenticate a real-world
actor, judge the substantive correctness of implementation, or authorize a
later lifecycle or external action.

Those limitations do not permit an inferred decision, hidden write, incomplete
receipt, candidate-as-governor substitution, or success claim after an
unexpected path or failed gate. Stronger evaluator-derived delegation and
runtime enforcement remain separately governed Phase 4 work.
