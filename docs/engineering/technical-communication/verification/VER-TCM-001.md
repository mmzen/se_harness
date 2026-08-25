+++
id = "VER-TCM-001"
type = "verification"
title = "Independent evidence for managed technical communication"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
verifies = ["REQ-TCM-001", "REQ-TCM-002", "REQ-TCM-003", "REQ-TCM-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T07:53:59Z"
decided_by = "assurance-owner"
+++

# Verification Contract: Independent evidence for managed technical communication

## Independence

Verification derives expected behavior from the four requirements,
`SPEC-TCM-001`, `ARCH-TCM-001`, the accepted outcome of `ADR-TCM-001`, and the
existing released managed contracts. It does not accept implementation wording,
helper output, readability scores, or model confidence as proof.

Deterministic tests independently compare source and output bytes, contract
fields, installation plans, locks, manifests, paths, package payloads, process
effects, and existing skill baselines. Assurance reviewers assess meaning and
operator comprehension using a versioned corpus that is not generated from the
candidate output.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-TCM-001` managed policy | package, installer, upgrade, router, lock, doctor, preflight, and static claim tests | clean install, offline install, safe upgrade, missing file, customized collision, package wheel/sdist inspection, no-download scan | one canonical and installed managed policy exists; it is routed, lock-bound, policy-listed, packaged, offline, and contains no prohibited claim or standard payload |
| `REQ-TCM-002` protection | independent byte/digest corpus, helper unit tests, canonical-result regression, semantic review | commands, code, IDs, hashes, versions, paths, JSON/TOML/YAML, logs, evidence, quotations, operator text, normative obligations, thresholds, formulas, unknown terms, malformed spans | every exact span is byte-identical; no critical semantic meaning changes; ambiguity fails closed |
| `REQ-TCM-003` profiles | profile-selection tests and blinded technical review | operator explanation, requirement, specification, architecture, work order, verification, evidence, non-English, exact-output, approved artifact migration | correct profile is declared; only eligible prose changes; no mass rewrite; material deviations are complete; readers identify intended action and role |
| `REQ-TCM-004` operator skill | strict-contract tests, trigger corpus, effect sentinel, installed skill identity, result and receipt validation | explicit and implicit activation, overlap with four current skills, malformed source, missing current state, integrity failure, protected mismatch, repository write callback, network and credential sentinel | only explicit valid invocation completes; result and receipt validate; existing skills remain unchanged; changed paths and external effects are empty |

## Acceptance scenarios

### Scenario 1: install one managed policy and skill offline

Install the standard template in an isolated target with network access blocked.
Assert that the policy and three-file skill core appear once, use managed mode,
match their canonical sources, have schema-3 lock entries, and pass doctor.

### Scenario 2: route without duplication

Inspect the rendered managed router, `AGENTS.md` managed fragment, installed
skills, notes, and templates. The router contains one concise direct policy
route. No consumer contains the policy's complete normative rule set.

### Scenario 3: refuse missing or customized policy

Remove the installed policy and run doctor and start/review preflight. Restore it,
then customize it without changing the prior lock and plan an upgrade. The
missing case identifies the exact path. The customized case blocks before any
partial managed replacement.

### Scenario 4: preserve a canonical lifecycle block

Pass a complete canonical restitution block as exact protected content. The
operator result returns it byte for byte with no preface, conclusion, or second
next step. The receipt reports zero changed paths.

### Scenario 5: preserve mixed technical content

Use narrative prose containing inline code, a fenced command, JSON, an artifact
ID, a SHA-256, a path, a version, and a quotation. The brief may render eligible
narrative text. Every protected byte and its order remains identical.

### Scenario 6: stop on malformed protected spans

Exercise negative offset, out-of-range end, duplicate ID, overlap, unsorted
spans, wrong digest, invalid UTF-8, duplicate JSON key, excessive span count, and
oversized source. Each case returns one stable bounded diagnostic and no completed
brief or mutation.

### Scenario 7: protect normative meaning

Give independent reviewers original and rendered examples containing `MUST`,
`SHALL`, `SHOULD`, conditions, exceptions, thresholds, decision roles, and
safety qualifications. No rendered example can weaken force, broaden or narrow
scope, drop a qualification, change an actor, or alter a threshold.

### Scenario 8: select the artifact profile

Draft new narrative portions of one requirement, specification, architecture,
work order, and verification contract. Confirm direct language and consistent
terms in eligible prose while front matter, relations, normative statements,
semantic tables, code, and expected results remain protected.

### Scenario 9: reject a style-only catalog rewrite

Request profile consistency across approved historical artifacts without a
substantive governed revision. The result identifies the boundary and changes no
artifact.

### Scenario 10: explicit skill activation only

Run a trigger corpus containing explicit brief requests, ordinary explanations,
repository orientation, draft creation, implementation, assurance preparation,
transition decisions, Git operations, release, and external actions. Only the
exact explicit brief cases select `harness-operator-brief`.

### Scenario 11: current state requires a current result

Request a brief about current artifact state without supplying a current
structured evaluator result. The skill stops and routes to `harness-orient`.
It does not infer state from source prose or invoke a writing effect.

### Scenario 12: no standard retrieval or compliance claim

Run static and effect-sentinel checks over policy, skill, helper, package,
documentation, and tests. No runtime code opens a network path or retrieves the
standard. No public or installed text claims ASD approval, endorsement,
certification, or strict compliance.

## Property and invariant tests

- Source digest is lowercase SHA-256 over exact UTF-8 bytes.
- Protected spans are ordered, non-overlapping, within source bounds, unique by
  ID, and individually digest-bound.
- For every generated valid span partition, protected output bytes equal source
  bytes exactly.
- Inserting, deleting, reordering, normalizing, or changing one protected byte
  makes preservation fail.
- Invalid or unknown input fields fail closed and never reach the render callback.
- A render callback that reports or performs a repository write is rejected by
  an independent filesystem and Git-state sentinel.
- Result and receipt contain the expected skill identity, profile, source digest,
  evaluator identity, zero changed paths, and no hidden or sensitive metadata.
- Repeated structural validation of identical inputs is deterministic.
- Existing `harness-orient`, `harness-draft-change`,
  `harness-execute-work-order`, and `harness-prepare-assurance` contract bytes,
  manifests, parser results, activation behavior, and installation modes match
  the pre-change baseline.
- The formal graph remains valid with zero structure, governance, or configured
  policy warnings or errors introduced by this work.

## Static and architecture checks

- Canonical and installed policy paths match `SPEC-TCM-001` and use managed mode.
- The managed router directly routes the policy and remains within its existing
  thin-router responsibility.
- Detailed communication rules occur only in the policy; formal artifacts may
  specify them but runtime consumers do not restate them.
- Dependency direction remains machine/formal authority to managed communication
  policy to skill/runtime rendering to evidence to human decision.
- The new contract is one closed v2 instance, not an open arbitrary policy or
  skill registry.
- Skill core contains only `SKILL.md`, `skill-contract.json`, and
  `scripts/check_brief.py` and has one canonical source.
- Standard package metadata includes the policy and complete skill core in wheel
  and sdist payloads.
- Required and policy path manifests include the installed policy in stable order.
- Candidate work does not edit root managed copies or `.engineering-harness.lock`.

## Security and privacy checks

- Run with network APIs disabled and sentinel callbacks for network, credentials,
  subprocess mutation, repository writes, Git writes, lifecycle mutation, and
  external action.
- Exercise hostile source text, terminal controls, path text, environment-like
  values, secrets, very long terms, malformed JSON, symlinks, and Unicode edge
  cases.
- Confirm diagnostics and receipts do not reproduce unbounded source, secrets,
  host paths, environment dumps, credentials, or hidden reasoning.
- Confirm runtime write permissions and injected callback capability cannot
  change the read-only admitted effect.
- Confirm no source text is sent to an external service or retained in the target.

## Performance and resilience checks

- Measure validation at empty, typical, and maximum source and span bounds.
- Confirm work is linear in source bytes plus span count and does not use network,
  subagents, retries to external services, or unbounded recursion.
- Interrupt structural validation and confirm no target byte or external state is
  changed.
- Repeat installation and upgrade planning to confirm deterministic actions and
  no partial write on a customized-policy conflict.

## Manual assessments

Use a versioned review corpus with at least:

- four operator explanations at an assumed technical expertise level of 5/10;
- one current-decision, one blocked, one exact-output, and one no-current-state
  case;
- one requirement, specification, architecture, work order, and verification
  excerpt;
- one assurance-sensitive and one safety-qualified example; and
- one project-terminology ambiguity.

Two reviewers independently record the intended fact, actor, action, condition,
qualification, normative force, and result before seeing candidate output. Pass
requires agreement that candidate prose preserves all recorded meaning. Every
operator case must let the reviewer identify the intended outcome and one next
decision or action without consulting implementation code. Disagreement is an
unresolved finding, not an averaged readability score.

Review the complete policy for technical accuracy, permitted claim, concise
loading cost, clear precedence, actionable examples, and absence of copied
standard content. Reviewers do not certify ASD-STE100 compliance.

## Evidence retention

Retain under `docs/engineering/technical-communication/evidence/`:

- exact commands, evaluator identity, formal snapshot, and results;
- policy and skill canonical/installed manifest comparisons;
- pre-change and candidate skill contract and digest baselines;
- package payload inventories and offline install/upgrade observations;
- protected-content corpus manifest, source/output digests, and failure cases;
- effect-sentinel results;
- manual review form, independent judgments, dispositions, and residual findings;
- changed-path review and proof that root managed copies were not edited; and
- review preflight plus the final work-order completion report.

Do not retain hidden reasoning, credentials, unbounded source bodies, copyrighted
standard content, or an external standard download.

## Residual uncertainty

A deterministic helper can prove declared byte preservation but cannot prove
that all semantically sensitive content was classified or that prose is clear to
every reader. Model and runtime behavior can also vary. The representative
corpus, explicit-only pilot, managed policy precedence, fail-closed ambiguity,
and human semantic review reduce but do not eliminate this uncertainty.

The verification record must report corpus limits, reviewer disagreement,
unsupported languages, untested runtimes, and any material deviation. Passing
this contract supports the bounded feature; it does not establish ASD-STE100
compliance, ASD endorsement, universal readability, or substantive artifact
correctness.
