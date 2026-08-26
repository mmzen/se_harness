+++
id = "VER-DLC-001"
type = "verification"
title = "Independent evidence for definition lifecycle disentanglement"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
verifies = ["REQ-DLC-001", "REQ-DLC-002", "REQ-DLC-003", "REQ-DLC-004", "REQ-DLC-005"]
+++

# Verification Contract: Independent evidence for definition lifecycle disentanglement

## Independence

Verification derives expected behavior from the five requirements, the three
specifications, `ARCH-DLC-001`, and the accepted outcomes of `ADR-DLC-001` and
`ADR-DLC-002`. It does not accept implementation wording, a passing test name, a
green CI badge, or a summary count as proof.

The central independence requirement is a control measurement. Every outcome
claim is a comparison between two runs of the released-lineage evaluator: one at
the increment's merge base and one at its candidate, taken the same way, on the
same platform, and recorded in full. A single-sided reading is not evidence.

Diagnostic identifier sets are compared for exact set equality, never for
cardinality. A count that matches while membership differs must fail, and a
reduced warning count must fail rather than pass as an improvement.

Each increment is verified separately against its own merge base. A combined
reading across two increments is not accepted, because it cannot attribute a
moved outcome to the change that moved it.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-DLC-001` declared generation | static absence scan, fixture ablation, dual-implementation vector fixture, merge-base comparison | `LEGACY_ARCHITECTURE_STATUSES` absent from both validator copies; each of the 14 frozen identifiers removed in turn; every declaration failure mode; `W014` set at base and candidate | no code path reads an architecture status in the assessment; each ablated identifier becomes `E014`; the `W014` identifier set is identical at base and candidate; both implementations agree on every stable reason |
| `REQ-DLC-002` terminal approval | transition-plan enumeration over nine families, contract conformance, recommendation exhaustiveness, existing-record regression | `approved -> implemented` and `approved -> rejected` planned per family; reachable graph versus `WORKFLOW.md` table; all nine families against every status in `ALLOWED_STATUSES`; all 165 existing implemented definitions validated, focused, and displayed | every `implemented` plan is refused through the ordinary legality path and every `rejected` plan succeeds; the reachable graph matches the state table; no pair occurring in the graph reaches the resolver's `RuntimeError`; the 165 report zero errors, resolve a recommendation, and are byte-unchanged |
| `REQ-DLC-003` derived realization | classification corpus, write sentinel, determinism repetition, commit-citation check | covered, partially covered, uncovered, reopened, rejected-record, superseded-record, and no-work-order graphs; `REQ-DST-006` with its 16 naming work orders; repeated runs | classification is correct in every case; `covered` names each record and its exact bound commit; every run leaves all files byte-identical; repeated runs produce identical findings in identical order; no artifact field is written and no transition proposed |
| `REQ-DLC-004` recorded decision | obligation fixture, chain-shape regression, declaration failure corpus, dual-implementation vector fixture | non-`draft` status with no chain and no declaration; the same with a recorded event; malformed chains; declaration in a draft work order; 513-entry declaration; stale declaration | `E022` for the undeclared case and clean for the recorded one; malformed chains keep their existing diagnostics and never consult the resolver; every failure mode resolves nothing with its named reason; `W025` for exactly the declared population, every run |
| `REQ-DLC-005` outcome preservation | paired released-lineage measurement, exact set equality, changed-path inventory, governance-migration scenario | base and candidate runs per increment, per platform; full diagnostic identifier sets; complete changed-path list; consumer upgrade across the version boundary | zero errors at both ends of every pair; `W013`, `W014`, and `W015` identifier sets exactly equal through increments 1 and 2; increment 3 adds exactly the declared `W025` set and moves no other; no artifact path outside this domain and the increment's own evidence directory; a migration scenario exists for each version pair |

## Acceptance scenarios

### Scenario 1: the status is no longer an input

Search both validator copies for `LEGACY_ARCHITECTURE_STATUSES` and for any read
of an architecture's `status` within the decision-assessment path. Both are
absent. The scan covers the package module, the self-contained script, and the
canonical template copy of the script.

### Scenario 2: ablate the frozen set, one identifier at a time

For each of the 14 frozen architecture identifiers, run validation on a fixture
graph with that identifier removed from the frozen set and nothing else changed.
Each run reports `E014` for exactly that architecture. This proves the
declaration, and not the lifecycle status, suppresses the error in the real run.

### Scenario 3: the exempt population does not move

Run the released-lineage evaluator at increment 1's merge base and at its
candidate. Both report zero errors. The `W013`, `W014`, and `W015` identifier
sets are identical, member for member. `W015` still includes `ARCH-IAR-004`. An
equal count with unequal membership fails.

### Scenario 4: an empty frozen set must fail loudly

Run increment 1's candidate with the frozen set emptied. Exactly 14 governance
errors appear and the run is not green. This confirms the acceptance criteria
cannot be satisfied by a change that merely suppresses the check.

### Scenario 5: exemption never suppresses the diagnostic

Search the implementation and configuration surfaces for any flag, field,
environment value, or declaration key that suppresses `W014` or `W025`. None
exists. Run every exempt case twice and confirm the diagnostic appears on both
runs.

### Scenario 6: the retired edge is refused for every family

For one artifact of each of the nine definition families, plan `approved ->
implemented`. Every plan is refused with the ordinary illegal-transition
diagnostic and no special-case message. Plan `approved -> rejected` for each and
confirm every plan succeeds. Include a plan of `REQ-TCM-001=implemented`, which
returns `PLANNED` at the merge base and must be refused at the candidate.

### Scenario 7: no status loses its recommendation

Enumerate all nine definition families against every status in
`ALLOWED_STATUSES`. For every pair that occurs anywhere in the repository, a
recommendation rule resolves. No such pair reaches the workflow resolver's
`RuntimeError`. The 165 existing implemented definitions resolve through
`WFL-DEFINITION-WORK`.

### Scenario 8: existing records keep authority and bytes

Validate, focus, report, and display each of the 165 definitions carrying
`implemented`. The verdict is zero errors, each is treated as governing authority
for coverage, and each file is byte-identical to the merge base. The same is
asserted for the 3 `superseded` and 7 `rejected` chainless definitions.

### Scenario 9: the two contract copies stay identical

Compare `se_harness/workflow_contract.json` and the standard template's
`docs/engineering/WORKFLOW.json` byte for byte. Confirm the reachable transition
graph derived from the contract matches the `WORKFLOW.md` state table exactly,
including the changed definition row.

### Scenario 10: retired procedure and re-pointed recommendation

Confirm `PROC-DEFINITION-COMPLETE` and `STEP-DEFINITION-COMPLETE` are absent, no
remaining outcome named `implemented` exists for a definition anywhere in the
contract, `WFL-DEFINITION-COMPLETE` retains its identifier and its `approved`
match while naming the work-selection procedure with `DR-WO-SELECT` and
`QG-G3-WORK-AUTHORIZATION`, and `DR-DEFINITION-DECIDE` is unchanged.

### Scenario 11: coverage reopens

Take a requirement whose naming work orders are all `verified`. Confirm it is
reported `covered` with each record and its exact bound commit named. Add a new
approved work order naming it. Confirm the next run reports `partially_covered`,
names the new work order as outstanding, emits no diagnostic about the earlier
classification, and changes no artifact. Repeat the check against `REQ-DST-006`
and its 16 naming work orders.

### Scenario 12: coverage is not verification and is not stored

Confirm the derived output cites verification records rather than restating their
verdicts, never describes a definition as implemented, and states that the result
grants no authority. Run the derivation under an independent filesystem and
Git-state sentinel and confirm zero writes. Confirm no artifact field, no lock,
and no cache holds a coverage value.

### Scenario 13: uncovered is not a defect

Confirm every intent, capability, and verification contract is classified
`uncovered` without an error or warning, and that a definition named only by
rejected or superseded work orders is `uncovered` while a definition whose only
verification record is `rejected` is `partially_covered` with no commit claimed.

### Scenario 14: the permission is closed

Author a fixture requirement with `status = "approved"` and no
`lifecycle_events`, named in no declaration. Validation reports `E022`. Add a
recorded `draft -> approved` event and confirm it validates cleanly. Repeat for
each of the nine definition families and confirm work orders, verification
records, and release records are unaffected.

### Scenario 15: no chain is ever fabricated

Search the implementation for any code path that writes, defaults, infers, or
backfills a `lifecycle_events` entry. None exists. Confirm the increment's
changed-path inventory contains no existing artifact file, and that the 6
`rejected` and 3 `superseded` chainless definitions are untouched.

### Scenario 16: declaration failure corpus

For both resolvers, exercise: malformed declaration, non-array value, duplicate
object keys, 513 entries, declaration in a `draft` work order, invalid
identifier, unknown target, ambiguous target, wrong target type, `draft` target,
and a target that already satisfies the obligation. Each resolves nothing, names
its stable reason, reports the affected artifacts as errors, and does not abort
validation of unrelated artifacts. Confirm two approved 512-entry declarations
resolve together.

### Scenario 17: the frozen sets are measured, not asserted

Re-run the committed generating measurement for each frozen set inside the test
suite and compare its output against the committed constant. The 14-identifier
set equals the `W014` identifier set at increment 1's merge base. The
449-identifier set equals the definitions carrying a non-`draft` status with no
chain at increment 3's candidate.

### Scenario 18: no forgeable exemption input

Confirm no exemption resolution reads a date, `created`, a Git reference, a
commit, an environment value, a command-line flag, a lock, an installed evaluator
identity, or any artifact-supplied field on the exempted artifact itself.

### Scenario 19: consumer upgrade across the boundary

Upgrade an isolated target repository holding pre-assessment architectures and
hand-authored statuses. Without a declaration, the affected artifacts become
`E014` or `E022` and the upgrade path names the remedy. With an approved
declaration, they become `W014` or `W025` and the verdict is zero errors. A
customized managed file blocks before any partial replacement.

### Scenario 20: increment ordering is enforced by evidence

Confirm increment 3's frozen set was measured at a commit at or after increments
1 and 2 landed, and record the measurement commit. A set measured earlier is a
finding, not a rounding difference.

## Property and invariant tests

- Both frozen sets are immutable frozen collections in both implementations and
  agree between the two copies.
- Resolution is a pure function of governed artifact content: identical content
  yields identical resolutions under a changed working directory, a changed
  directory basename, a depth-1 checkout, and a full clone.
- Resolution is order-independent and idempotent; two runs produce identical
  diagnostics in identical order.
- A declaration array is bounded, duplicate-key rejecting, and case-sensitive.
- Every declaration defect is fail-closed: it resolves nothing and never grants
  an exemption by accident.
- Every stale declaration is reported and resolves nothing.
- Exemption suppresses only the error; the maintenance diagnostic is emitted on
  every run.
- `E015` behavior is unchanged: an exempt architecture with no deciding ADR still
  reports it, and `W015` remains status-independent.
- `implemented` remains in `ALLOWED_STATUSES`, and the `implemented` contract row
  retains `grants_authority`, `must_remain_visible`, and `transitionable: false`.
- The derivation writes nothing, proposes no transition, and never reads a
  definition's own status.
- `HRN-006` holds: no work-order transition moves a definition and no derived
  result is written into an artifact.
- The full existing test suite matches its baseline, with local skips understood
  as Windows-only guards rather than coverage gaps.
- The formal graph introduces no structure, governance, or configured-policy error
  and no unaccounted warning.

## Static and architecture checks

- Each mechanism lives in its own module and answers only its own question.
- No mechanism reads another mechanism's output.
- Dependency direction remains governed artifact content to resolver to
  diagnostic, and work orders and records to derivation to report, with no arrow
  from a report back into an artifact field.
- The declaration surface matches `SPEC-LRE-001`'s shape, bound, and approval
  precondition rather than introducing a second mechanism.
- No new artifact field, relation type, artifact type, role, decision right, or
  quality gate appears in any increment.
- Candidate work edits no root managed copy and not `.engineering-harness.lock`;
  managed changes are made in `templates/repository/standard/`.
- The `WFL-DEFINITION-COMPLETE` name-versus-behavior residue is disclosed in the
  implementation notes.

## Security and privacy checks

- Run with network APIs disabled and sentinel callbacks for network, credentials,
  subprocess mutation, repository writes, Git writes, and lifecycle mutation.
- Treat artifact metadata, work-order text, declaration arrays, and declared
  identifiers as hostile input: oversized arrays, deep nesting, terminal
  controls, path-like and environment-like values, invalid UTF-8, duplicate keys,
  and Unicode edge cases.
- Confirm diagnostics reproduce no file body, host path, environment dump, or
  credential, and contain identifiers, statuses, and stable reasons only.
- Confirm runtime write permission does not change the read-only admitted effect
  of the derivation.

## Performance and resilience checks

- Measure validation over the full graph at the merge base and the candidate and
  confirm no material regression.
- Confirm resolution is linear in artifacts plus declared entries, with no
  unbounded recursion, no network, and no subprocess.
- Interrupt a validation run and confirm no repository byte changed.
- Repeat the paired measurement to confirm the reported figures are stable, and
  label every figure by platform. A green Windows reading is not evidence about
  Linux and the reverse.

## Manual assessments

Assurance reviewers independently confirm, without reading the implementation:

- that `DR-DEFINITION-DECIDE` grants no outcome the revised contract omits, and
  that the revised contract admits no outcome the decision right does not grant;
- that the revised `WORKFLOW.md` state table and the reachable graph say the same
  thing, and that the text states `implemented` remains accepted, visible, and
  authority-granting;
- that the `W014` and `W025` diagnostic texts assert only that a fact is
  declared, and never that a decision was taken, by whom, or when;
- that the derived coverage output cannot be read as an approval, a transition, or
  a verification verdict;
- that the increment-3 diff's 449-entry constant is trusted through its
  generating measurement and comparison test rather than by manual transcription,
  and that the reviewer has confirmed the measurement's commit; and
- that the residual reading risk of 165 records still carrying `implemented` is
  disclosed rather than described as resolved.

Reviewer disagreement is an unresolved finding, not an averaged judgment.

## Evidence retention

Retain under `docs/engineering/definition-lifecycle/evidence/`:

- exact commands, evaluator identity and version, and full output for the merge
  base and candidate runs of each increment, labelled by platform;
- complete diagnostic identifier sets, not counts, for both ends of every pair;
- the ablation matrix for the 14 frozen identifiers;
- the generating measurement output for each frozen set and its commit;
- the transition-plan enumeration over the nine families and both directions;
- the recommendation-exhaustiveness enumeration;
- the byte comparison of the two contract copies and the derived reachable graph;
- the coverage classification corpus and write-sentinel results;
- the declaration failure corpus with each stable reason;
- the consumer upgrade observations and the governance-migration scenario;
- the complete changed-path inventory per increment;
- the full test-suite report with skips named and attributed; and
- review preflight plus the work-order completion report.

Do not retain hidden reasoning, credentials, unbounded file bodies, or host
environment dumps.

## Residual uncertainty

Four limits are known and must be reported rather than resolved.

The coverage findings render in `inspect` and not in the dashboard, by an owner
decision of 2026-08-26 that defers the dashboard surface to separately approved
work. Until that work lands, `I-DLC-001` and `W-DLC-001` behave unlike every other
member of the family they join, and an operator reading the dashboard sees no
coverage signal at all. Verification confirms the derivation is
surface-independent; it cannot confirm that the deferred work will be scoped.

The frozen sets are correct as of the commit at which they are measured. Nothing
in the mechanism prevents them from having been measured at the wrong commit;
only the recorded measurement commit and its comparison test stand behind them.

The 165 records carrying `implemented` remain in the graph indefinitely. Every
mechanism treats them correctly, but a human reader encountering one will still
read it as "built". No test can close that gap, and the domain deliberately
declines to close it by editing them.

Passing this contract establishes that the three mechanisms behave as specified
and that no existing outcome moved. It does not establish that the exempt
populations are complete, that a declared exemption reflects a decision that was
actually taken, or that the derived coverage report is a substitute for reading
the verification records it cites.
