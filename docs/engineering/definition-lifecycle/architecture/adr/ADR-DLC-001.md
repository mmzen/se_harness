+++
id = "ADR-DLC-001"
type = "adr"
title = "Replace lifecycle-status inference with explicit declaration in three ordered increments"
status = "draft"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
decides = ["ARCH-DLC-001"]
+++

# ADR: Replace lifecycle-status inference with explicit declaration in three ordered increments

## Status

Proposed.

## Context

A definition's lifecycle status currently answers three questions at once:

- **Authority.** Does this artifact govern? `ACTIVE_COVERAGE_STATUSES` reads the
  status for this, correctly.
- **Generation.** Is this artifact from before `decision_assessment` existed?
  `LEGACY_ARCHITECTURE_STATUSES = {"implemented", "verified", "released"}` reads
  the status as a proxy. Measured against the graph, the proxy is right for 14
  of the 28 `implemented` architectures and wrong for the other 14, which are
  modern-shaped and already carry an assessment. It is a 50%-accurate era test.
- **Realization.** Has this been built? 165 definitions carry `implemented`, of
  which 104 are requirements. 49 of those 104 are named by more than one work
  order, and `REQ-DST-006` is named by 16.

Three findings make the `approved -> implemented` edge a defect rather than an
unused convenience:

1. `DR-DEFINITION-DECIDE` grants "Approve or reject" — two outcomes — while
   `PROC-DEFINITION-COMPLETE` offers `outcomes = ["implemented", "reject",
   "stop"]`. The contract admits an outcome no decision right authorizes.
2. The eleven numbered steps of the managed procedure in `WORKFLOW.md` never mark
   a definition `implemented`.
3. Planning `REQ-TCM-001=implemented` against the released `0.6.0` evaluator
   returns `PLANNED`, reports "implemented and terminal", and recommends exactly
   what the `approved` route already recommends. Both states carry
   `grants_authority: true`, so the edge grants nothing and, being terminal,
   forecloses everything.

The edge has been taken zero times across 630 definitions. The only recorded
definition edges are 181 `draft -> approved` and 6 `approved -> rejected`.

Behind all of this sits one permission: `validate_lifecycle_events` begins
`events = artifact.metadata.get("lifecycle_events"); if events is None:
continue`. 449 of 630 definitions — 71% — carry a status with no recorded
decision. That permission is why 165 definitions were authored straight into a
terminal state no decision right grants and nothing objected.

`HRN-005`, `WFL-004`, and `HRN-006` all say state changes only by explicit
decision and applied transition, and never by inference. The repository does not
currently hold itself to that.

There is an established precedent for the fix. `SPEC-LRE-001` and
`se_harness/legacy_release_evidence.py` replaced exactly this kind of inference
for release evidence: a frozen, closed, named self-hosting compatibility set of
six identifiers, plus a bounded declaration inside an approved work order,
fail-closed, with both implementations agreeing on a shared committed fixture.

## Decision drivers

- `HRN-001`: artifacts are authority and code is evidence. A validator branch
  keyed on a status is code deciding what an artifact means.
- `HRN-005`, `WFL-004`, `HRN-006`: no state by inference, and no state
  synchronized by implication.
- A fact that a later work order can falsify must not be stored in a terminal
  field, because a terminal field can never be corrected.
- 890 artifacts validate at 0 errors today. No increment may put that at risk,
  and no increment may quietly reduce a warning count either.
- No artifact byte may change. The 165 and the 449 are historical records, and 6
  of the 449 are already `rejected` — writing a decision for them would rewrite
  history.
- Consumer repositories pin the managed contract and the managed validator. A
  repository that would break must block with a named remedy, not be partly
  migrated.
- Every increment must be independently reviewable and independently reversible
  before the next one starts.
- The precedent already exists and is approved, implemented, and verified.
  Inventing a second mechanism for the same problem would be worse than reusing
  the first.

## Considered options

### Option A: three ordered increments, declaration over inference, no migration

Increment 1 replaces the generation proxy with a frozen 14-identifier set plus a
consumer declaration. Increment 2 terminates the definition lifecycle at
`approved`, keeps `implemented` as unreachable compatibility vocabulary, and adds
a derived realization report. Increment 3 makes `lifecycle_events` mandatory past
`draft` with a frozen 449-identifier pre-contract declaration.

Each increment is one work order with an independently measurable outcome. No
artifact is edited. Every grandfathered population stays visible as a permanent
maintenance diagnostic.

This is the most work of any option and adds two frozen sets and two declaration
surfaces the project must maintain forever.

### Option B: migrate the data

Edit the 165 `implemented` definitions back to `approved` and author
`lifecycle_events` chains for the 449.

This would leave a uniform graph with no grandfathering machinery at all. It is
rejected on three independent grounds. It would fabricate decisions that were
never taken — the worst possible outcome for a governance graph whose entire
claim is that state changes only by recorded decision. It would rewrite the 6
`rejected` and 3 `superseded` records. And editing an `implemented` architecture
to `approved` converts its `W014` into `E014`, so the migration cannot even be
performed until increment 1 has already landed.

### Option C: fix only the generation proxy and stop

Increment 1 alone. Cheap, safe, and it removes the one measurably wrong
inference.

It is rejected as insufficient rather than wrong. It leaves the edge that no
decision right authorizes, leaves the terminal claim that cannot stay true, and
leaves the permission that let all of this accumulate invisibly. The order it
establishes is right, so this option is really a partial adoption of Option A.

### Option D: keep the status proxy and document it

Add a note explaining that `implemented` means "pre-assessment generation" for
architectures.

Rejected. Documentation cannot make a 50%-accurate proxy accurate, and it
directly contradicts `HRN-001` by leaving a code branch as the authority on what
a status means.

### Option E: retire `implemented` and store realization in a new field

Terminate the lifecycle, then add a `realized` boolean or a `realized_at` field
to definitions.

Rejected. It reproduces the defect it is meant to fix. A stored flag set when the
first work order completes is falsified by the second, and the graph already
holds the true answer — `WO implemented -> VREC verified at a commit -> RLS
released` — which a derivation can read and which additionally names the commit
where coverage holds. A field never can.

### Option F: a cutover date instead of enumerated sets

Grandfather by comparing `created` against a frozen date rather than enumerating
identifiers.

Not rejected here. It is a live alternative for the grandfathering mechanism
specifically, and `ADR-DLC-002` decides it.

## Decision

Select Option A.

Replace status inference with explicit declaration for all three questions, in
three ordered increments, with no data migration of any kind.

Assign one mechanism per question. Authority stays with the lifecycle status,
which is what it is for. Generation moves to a frozen closed self-hosting set
plus a bounded declaration in an approved work order, on the `SPEC-LRE-001`
model, and `LEGACY_ARCHITECTURE_STATUSES` is removed from both validator copies.
Realization moves to a read-only derivation over work orders and the verification
records bound to them, which names the exact commit of each covering record and
stores nothing.

Terminate the reachable definition lifecycle at `approved` with `rejected` as its
only outgoing edge. Keep the `implemented` row in both contract copies with
`grants_authority: true`, `must_remain_visible: true`, and `transitionable:
false`, exactly as `ready`, `in_progress`, `verified`, `released`, and
`superseded` are already kept in that family. Keep `implemented` in
`ALLOWED_STATUSES`. Retire `PROC-DEFINITION-COMPLETE` and
`STEP-DEFINITION-COMPLETE`, the only carriers of the unauthorized outcome. Keep
`WFL-DEFINITION-WORK` matching `implemented` so the 165 existing records keep a
resolvable recommendation, and keep the `WFL-DEFINITION-COMPLETE` identifier
while re-pointing it at work selection. Leave `DR-DEFINITION-DECIDE` untouched;
it already describes the decision that survives.

Make `lifecycle_events` mandatory for every definition whose status is not
`draft`, with a frozen closed declaration covering exactly the 449 pre-contract
definitions and a bounded declaration for consumers.

Fix the order: generation, then lifecycle termination, then the recorded-decision
obligation. Generation must be first because it is the only increment that is
strictly a correction and because the other two both touch the `implemented`
population it protects. The obligation must be last because its frozen set cannot
be measured until the population it covers has stopped moving.

Report every grandfathered artifact, on every run, forever. No flag, field, or
configuration suppresses `W014` or `W025`. An exemption suppresses the error and
never the diagnostic.

## Consequences

### Positive

- Each of the three questions has exactly one mechanism, and none is answered by
  inference from another.
- The reachable lifecycle finally agrees with `DECISION_RIGHTS.md` and with the
  eleven-step procedure in `WORKFLOW.md`, both of which already describe it
  correctly.
- Realization becomes more informative than the state it replaces: it names the
  commit at which coverage holds, and it reopens automatically when a
  seventeenth work order arrives.
- The permission that hid this divergence for 449 artifacts is closed, so the
  next such divergence is visible on the first validation run.
- Grandfathered debt is enumerated, named, bounded, and permanently visible
  rather than implicit in a status value.
- One mechanism, already approved and verified, is reused three times instead of
  three new mechanisms being invented.

### Negative

- The project maintains two frozen sets — 14 identifiers and 449 — forever, plus
  two declaration surfaces.
- Warning volume rises substantially: 50 today, 499 after increment 3. The
  increase is entirely `W025` and is the point, not a side effect, but reviewers
  must be told that a large warning count here means recorded honesty rather than
  new breakage.
- `WFL-DEFINITION-COMPLETE` keeps a name that no longer matches its behavior,
  because consumers pin the identifier. The residue is accepted and disclosed.
- Three work orders, three verification records, and three coordinated changes to
  two byte-identical contract copies is materially more delivery work than any
  alternative.
- Anyone who has learned to read `implemented` on a requirement as "built" must
  learn to read the coverage report instead, and the 165 existing records will
  keep suggesting the old reading indefinitely.

### Operational and security

- Every mechanism is a pure function of governed artifact content. No lock, no
  installed evaluator identity, no environment value, no command-line flag, no
  network, no subprocess, no filesystem write, no Git mutation.
- Declaration arrays, declared identifiers, and work-order text are untrusted
  parser input, bounded at 512 entries per declaration, duplicate-key rejecting,
  and fail-closed.
- A declaration resolves only after its work order records a `draft -> approved`
  event, so approval authority stays with the engineering owner.
- The derivation is guarded by an independent write sentinel asserting
  byte-identical files after every run.
- No verified verification record and no released release record is read,
  rewritten, re-pointed, or superseded.

### Migration

- No artifact byte changes in any increment. No status is migrated, normalized,
  superseded, or re-decided.
- This repository's outcome is preserved exactly through increments 1 and 2: 890
  artifacts, 0 errors, 50 warnings, with identical `W013`, `W014`, and `W015`
  identifier sets. Increment 3 adds exactly 449 `W025` and moves no existing
  count.
- A consumer repository holding pre-assessment architectures or hand-authored
  statuses must add a declaration under an approved work order before upgrading,
  or those artifacts become `E014` or `E022`. Each increment ships a
  governance-migration scenario for its version pair.
- A predecessor evaluator that still admits the retired edge is handled by the
  migration contract's adapter path. The edge is never re-admitted.
- Increment 2 is a within-`se-harness-workflow-v3` retirement, decided 2026-08-26
  by the repository owner: the contract's shape does not change, so no generation
  bump is taken and the boundary is carried by the release version, the migration
  scenario, and the `implemented` row's `predecessor_adapter`. The accepted risk
  is that a consumer pinning `v3` sees reachable behaviour narrow without a
  generation signal. The two delivery copies stay byte-identical.

## Validation

- Assert `LEGACY_ARCHITECTURE_STATUSES` is absent from both validator copies and
  that no code path reads an architecture status in the assessment.
- Fixture-remove each of the 14 frozen identifiers and assert each becomes
  `E014`, proving the declaration and not the status suppresses the error.
- Assert exact identifier-set equality, not cardinality, for `W013`, `W014`, and
  `W015` between the merge base and each candidate, measured on Windows and
  Linux separately and labelled per platform.
- Plan `approved -> implemented` on one artifact of each of the nine definition
  families and assert every plan is refused; plan `approved -> rejected` and
  assert each succeeds.
- Enumerate all nine families against every status in `ALLOWED_STATUSES` and
  assert no pair occurring in the graph reaches the workflow resolver's
  `RuntimeError`.
- Assert the reachable transition graph matches the `WORKFLOW.md` state table and
  that the two contract copies are byte-identical.
- Validate and focus each of the 165 existing `implemented` definitions: zero
  errors, a resolvable recommendation, unchanged bytes.
- Exercise the derivation over covered, partially covered, uncovered, reopened,
  rejected-record, and superseded-record graphs, with an independent write
  sentinel asserting byte-identical files after every run.
- Author a fixture definition with a non-`draft` status and no chain, in no
  declaration, and assert `E022`; add a recorded event and assert it validates.
- Exercise every declaration failure mode for both resolvers and assert both
  implementations agree on the shared committed vector fixtures.
- Assert the exact changed-path inventory of each increment contains no artifact
  path outside this domain and that increment's own evidence directory.
