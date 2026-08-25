+++
id = "WO-REB-023"
type = "work_order"
title = "Give the migration rehearsal a scenario whose successor is the current candidate"
status = "in_progress"
owners = ["engineering-owner", "release-owner", "quality-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[assurance]
commit_bound_verification = "required"
rationale = "This changes which scenario the candidate-evidence governance-migration gate runs and adds the canonical scenario bytes it runs against. That gate is the only proof that released evaluator N-1 governs the candidate N, and release approval reads it. A scenario that declared the wrong identities, or a workflow pointed at the wrong scenario, would turn a real refusal into a green gate, so assurance must bind the exact commit whose scenario and workflow produced the reading."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "tests/fixtures/governance_migration/",
  ".github/workflows/candidate-evidence.yml",
  "tests/test_governance_migration.py",
  "docs/engineering/released-evaluator-boundary/README.md",
  "docs/engineering/released-evaluator-boundary/work-orders/WO-REB-023.md",
  "docs/engineering/released-evaluator-boundary/evidence/",
]

[relations]
implements = ["REQ-REB-016", "REQ-REB-017"]
specifications = ["SPEC-REB-008"]
architecture = ["ARCH-REB-007", "ADR-REB-007"]
verification = ["VER-REB-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T20:48:00Z"
decided_by = "engineering-owner"
reason = "Approved by the engineering owner on 2026-08-25 with the boundary measurement in front of them, in one act carrying four decisions. (1) The work order is approved as drafted and its required commit-bound verification classification stands; a VREC is owed and is not authorized by this approval. (2) Route A is the scenario's route: a version-truthful candidate-0.6.0-to-0.7.0 scenario classifying compatible, because the pair has no boundary the current contract can express. classify_migration is a set difference over eight closed capability names that 0.6.0 already holds in full, and the boundary MIG404 demands of a historical- scenario is hard-coded to the schema-3 and evaluator-evidence rule 0.6.0 itself introduced. A real gap exists, since released 0.6.0 exposes no qualify, but the vocabulary cannot name it. Route B, a new contract version naming that capability, is rejected for this work order rather than judged wrong; it would amend SPEC-REB-008 and the contract days before the release and needs its own scope decision. The execution scope is unchanged because it was already drawn for route A. (3) Evidence retains under this work order's own key, as a routine reading of VER-REB-007, which named WO-REB-018 before this work order existed. VER-REB-007 is not amended. (4) The historical 0.5.0-to-0.6.0 pair is dropped from the CI lane and stays byte-identical and exercised by the unit suite. No second matrix dimension is added, because running it against the public 0.6.0 wheel would make CI assert a fact about a released package rather than about the candidate. Route A gives up the MIG404 guard and the forced predecessor archive pin, so the work order pins the predecessor by digest anyway and asserts the compatible outcome in a test. Approval authorizes no start, no governing amendment, and no release act."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-25T21:09:57Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit instruction of 2026-08-25, taken after the approval of the same day and as a separate accountable act. Start preflight reads PASS with the released 0.6.0 evaluator from outside the checkout, at d91ed5d, main's merge of PR #162, which is also the branch point of fix/wo-reb-023-candidate-scenario. Authorized work is route A only, inside the six declared execution-scope paths: a candidate-0.6.0-to-0.7.0 scenario fixture declaring compatible, the governance-migration job's scenario path and its two predecessor env values, removal of the historical pair from that lane, new tests including a successor-version divergence test and a compatible-classification test, the domain-index bullet, and retained evidence under this work order's own key. The historical scenario stays byte-identical and exercised by the unit suite. Not authorized by this start: any edit to the migration runner, the contract module or the contract JSON; any new contract version, which is route B and was rejected at approval; any amendment to REQ-REB-016, REQ-REB-017, SPEC-REB-008, ARCH-REB-007, ADR-REB-007 or VER-REB-007; any change to docs/notes/, which is an ungoverned path and a separate pull request; any change to pyproject.toml or the candidate version; and every release act, meaning candidate commit, promotable build, verification record, release record, tag, publication, deployment, maintenance-line mutation, credential use and root-evaluator change. If the lane can only be made green by relaxing an identity comparison or waiving a diagnostic, the work stops and the finding is escalated rather than the gate being made to pass."
+++

# Work Order: Give the migration rehearsal a scenario whose successor is the current candidate

## Lifecycle

This work order is `approved`. Its authoritative state, and the timestamp and
reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above; read those rather than this prose.

The owner routed this defect to its own work order, asked that it be fixed before
0.7.0 ships, and then approved this text on 2026-08-25 after the measurement in
*The pair has no expressible boundary* was put in front of them. Four decisions
were taken in that one act, and each is recorded where it changes the work:

- The `required` commit-bound verification classification and its rationale stand
  as proposed. A `VREC` is owed and is not authorized by this approval.
- **Route A** is the scenario's route: a version-truthful `compatible` scenario, no
  governing amendment, and the `[execution_scope]` above unchanged. Escalation
  question 2 is answered.
- Evidence retains under this work order's own key, as a routine reading of a
  verification contract written before this work order existed. `VER-REB-007` is
  not amended. Escalation question 1 is answered.
- The historical pair is dropped from the CI lane and stays byte-identical and
  exercised by the unit suite. Escalation question 3 is answered.

Approval, start, and completion remain three separate accountable acts. Approval
authorizes no start, no release act, and no governing amendment; the answers above
are decisions of record, not permission to exceed the scope they shape.

## Objective

Restore the candidate-evidence governance-migration gate on both platforms by
adding a canonical scenario whose declared successor version is the version the
candidate actually builds, and by pointing the workflow and its pinned predecessor
at that scenario. Do not edit the completed historical scenario.

## The defect

Measured, not inferred. `SE Harness Candidate Evidence` run `32886901131`, event
`push`, branch `chore/wo-rls-011-0-7-0-qualification`, head
`6fdb23a0911b0e9c0185d73ca55ea74b228398d7`, **failed**:

| Job | Id | Conclusion |
|---|---|---|
| Candidate source evidence | `97929364771` | success |
| Candidate package evidence | `97929972663` | success |
| Governance migration (Windows) | `97930154875` | **failure** |
| Governance migration (Linux) | `97930154913` | **failure** |
| Build deterministic integration package | `97930458774` | skipped |
| Reconcile governance migration platforms | `97930458842` | skipped |
| Verify integration package | `97930459343` | skipped |
| Retain verified integration package | `97930460668` | skipped |

Both migration jobs failed at the same step, *Rehearse the exact
predecessor-to-successor handover twice*, with the same diagnostic:

```
harnessctl: MIG211: successor version differs from the scenario
```

The failure is at the **first** of the two rehearsals, so the double-replay
`semantic_sha256` comparison never ran, and the four downstream jobs — including
the deterministic integration package and its verification — never started.

The cause is exact. `.github/workflows/candidate-evidence.yml` runs
`tests/fixtures/governance_migration/historical-0.5.0-to-0.6.0.json`, whose
`versions` object is `{"predecessor": "0.5.0", "successor": "0.6.0"}`, against a
successor built from the exact candidate commit. `pyproject.toml` on that branch
declares `version = "0.7.0"`, bumped by commit `f76da57` as part of the 0.7.0
candidate stage. `_verify_runtime_identity` compares the successor runtime's
reported `version` against the scenario's declared successor version and refuses
when they differ, which is `SPEC-REB-008` rule 4, *Exact identities*, working
exactly as specified. The refusal is correct; the configuration is what is wrong.

Every other branch is green on this lane because every other branch is still at
`0.6.0`.

**This is the first candidate version bump since the migration rehearsal landed**
(`ca275ac`, 2026-08-23, after 0.6.0 shipped). So the lane has never survived a
bump, there is no precedent commit to copy, and nothing in
`docs/notes/developing-se-harness.md#release-sequences` lists adding a scenario as
a release step. That omission is why the gap reached CI rather than being caught
during the bump.

## Why the obvious fix is forbidden

Editing `versions.successor` in the existing scenario is prohibited by the
governing artifacts and by the retained notes, in three places:

- `SPEC-REB-008`: "Future successors add scenario data or a new versioned contract
  when semantics change; they do not edit completed historical scenarios."
- `SPEC-REB-008`: "The first scenario preserves exact 0.5.0 and 0.6.0 historical
  facts."
- `docs/notes/evaluator-migration-rehearsal.md`: "The exact 0.5.0-to-0.6.0
  scenario is permanent regression history", and "Do not silently modify a
  completed historical scenario."

The scenario also binds its own bytes: it carries `fixture_sha256`, the workflow
and the unit suite read its `sha256`, and
`tests/test_hash_bound_integrity.py` covers
`tests/fixtures/governance_migration/*.json` under a hash-bound rule. An edit
would either fail those bindings or force them to be re-measured, which is the
mechanical expression of the same prohibition.

Two other shapes were considered and are rejected rather than left unstated:

- **Run the version-neutral `synthetic-n-minus-1-to-n.json` in the lane instead.**
  It cannot work. That scenario declares `41.2.0` to `42.0.0` and fabricates both
  runtimes; it never takes the real candidate as successor, so it proves nothing
  about the candidate and would replace a real gate with a self-test.
- **Keep the historical scenario in the lane but supply the public `0.6.0` wheel
  as the successor.** This passes — it is what `WO-RLS-011`'s local evidence
  measured — and it is the worst option, because it makes the gate assert a fact
  about a released package rather than about the candidate. The gate's entire
  purpose is proving that evaluator N-1 governs the candidate.

## The pair has no expressible boundary

Measured while this work order was `draft`, because the answer changes the work's
shape and therefore belongs in front of the owner at approval rather than in a
completion report. Three readings, each from a named line of the repository or a
named command:

1. **The classification is a set difference over a closed vocabulary.**
   `classify_migration` at `se_harness/governance_migration_contract.py:438` is
   `missing = successor_required - predecessor`, and the outcome is
   `migration-required` only when `missing` is non-empty. The contract's
   `capabilities` object declares exactly eight capability names and the scenario
   validator admits no others. The `historical-0.5.0-to-0.6.0` scenario declares
   `successor_required` as **all eight** of them, which is this repository's own
   recorded assertion that 0.6.0 holds all eight. A truthful predecessor set for a
   0.6.0-to-0.7.0 scenario is therefore all eight, `missing` is empty,
   `affected_operations` is empty, and the outcome is `compatible`. Declaring
   anything else would be a false capability claim about a released version.

2. **The boundary the rehearsal reproduces is hard-coded, and it is 0.6.0's.**
   `_proposal_validation` at `se_harness/governance_migration.py:373` calls a
   proposal valid only when `schema == 3` and `evaluator_evidence is True`; the
   scenario validator closes the proposal `schema` field to `{2, 3}` at
   `governance_migration_contract.py:245`. The historical scenario's initial
   proposal is `schema = 2, evaluator_evidence = false`, so both codes fire and the
   outcome is `migration-required` — which is exactly the 0.5.0-to-0.6.0 history.
   `_stage_validate_complete` refuses with `MIG404` when a scenario whose
   `scenario_id` starts with `historical-` does **not** reproduce that outcome. So a
   `historical-0.6.0-to-0.7.0` scenario must either trip `MIG404` or declare that
   0.7.0 introduces the schema-3 and evaluator-evidence boundary that 0.6.0 already
   introduced. The second is a false historical fact, which is the thing this whole
   packet exists to prevent.

3. **A real capability gap does exist, and it has no name in the vocabulary.**
   Measured from the two runtimes: released 0.6.0's command surface is `init,
   adopt, validate, inspect, dashboard, doctor, preflight, focus, check, transition,
   select-work-order, upgrade, rehearse-recovery, scaffold-domain, create-artifact,
   renumber-artifacts, identity, accept-candidate, capture-verification,
   prepare-release`. The candidate adds `rehearse-migration` and `qualify`, and
   re-labels `accept-candidate` as a compatibility alias for `qualify
   candidate-package`. Typed qualification is a successor behavior the predecessor
   cannot govern, so `SPEC-REB-008`'s framing is satisfied in behavior; it is the
   contract's eight-name vocabulary that cannot express it.

The consequence is that the fix is not simply "add a scenario". It is a choice
between a truthful `compatible` scenario that keeps the gate on the candidate while
asserting less than the historical one does, and a new contract version that names
the real 0.7.0 capability. **The owner chose the first at approval — route A.** The
second route would have added `se_harness/governance_migration_contract.json`,
`SPEC-REB-008`, and probably `REQ-REB-016` to the surface; it is not authorized
here, and the `[execution_scope]` above is unchanged because it was already drawn
for route A.

Route A asserts strictly less in one respect, and this work order compensates
rather than passing over it. Because the new `scenario_id` does not start with
`historical-`, `MIG404` no longer demands a reproduced boundary and
`governance_migration.py:345` no longer forces the predecessor to be a
digest-pinned archive. So the predecessor is pinned by digest anyway, as a
requirement of this work order rather than of the runner, and the `compatible`
outcome is asserted explicitly in a test — a future version that does introduce a
boundary must fail that assertion rather than pass quietly.

## In scope

1. Author `tests/fixtures/governance_migration/candidate-0.6.0-to-0.7.0.json` as a
   canonical `se-harness-governance-migration-v1` scenario: UTF-8 with LF, the
   closed nine-stage catalog in order (`prepare`, `validate-complete`, `reject`,
   `replace`, `assess`, `release-plan`, `publish-plan`, `render`, `adopt`), only
   capabilities, roles, views, adapters, decisions and stages the contract version
   already allows, and its fixture and decision bytes bound with SHA-256. The
   `candidate-` prefix is deliberate: it is not `historical-`, because the pair has
   no historical boundary to preserve, and it is not `synthetic-`, because both
   runtimes are real.
2. **Declare only what has been measured.** The classification the scenario
   declares is `compatible`, with the predecessor holding all eight capabilities
   and an empty missing-capability set, because that is what *The pair has no
   expressible boundary* measured. Assert that outcome in the scenario and in a
   test rather than leaving it implied, and do not fabricate a capability gap to
   make the shape look like the historical scenario's.
3. Point the lane at the new scenario in `.github/workflows/candidate-evidence.yml`
   and move its pinned predecessor to `0.6.0`, replacing both
   `PREDECESSOR_VERSION` and `PREDECESSOR_WHEEL_SHA256`. The new digest must be
   measured from the already-public wheel, not copied from anywhere. Keep the digest
   pin even though a non-`historical-` scenario no longer forces one.
4. Remove the historical pair from the lane, which is the owner's decision at
   approval. It is not deleted, not edited, and not un-exercised: it stays
   byte-identical and covered by the unit suite. No second matrix dimension is
   added, because running it against the public 0.6.0 wheel would make CI assert a
   fact about a released package rather than about the candidate.
5. Extend `tests/test_governance_migration.py` so the new scenario is covered by
   the same deterministic assertions as the existing pair, including at least one
   test that fails if a scenario's declared successor version and the version the
   candidate builds ever diverge again. That test is the point of this work order:
   the next bump must break a unit test on the author's workstation instead of a
   hosted gate. Add one more that fails if the pair's classification stops being
   `compatible`, which is route A's compensation for the `MIG404` guard the
   `candidate-` prefix gives up.
6. Keep `historical-0.5.0-to-0.6.0.json` byte-identical and still exercised by the
   unit suite, which is what makes it permanent regression history rather than
   dead weight. Evidence it by digest, before and after.
7. Record the measured before-and-after readings, and one bullet in
   `docs/engineering/released-evaluator-boundary/README.md`. Retain the evidence
   under this work order's own key, which is the owner's reading of `VER-REB-007`
   taken at approval; state that reading in the retained record so a reviewer sees
   it was a decision and not an oversight.

## Out of scope

- Any edit to `historical-0.5.0-to-0.6.0.json`, `synthetic-n-minus-1-to-n.json`,
  `se_harness/governance_migration.py`,
  `se_harness/governance_migration_contract.py`, or
  `se_harness/governance_migration_contract.json`. If the new scenario cannot be
  expressed without touching the contract or the runner, that is a stop
  condition, not a scope extension.
- Any new contract version. `SPEC-REB-008` reserves that for a migration with new
  semantic stages and requires accountable review.
- Any amendment to `REQ-REB-016`, `REQ-REB-017`, `SPEC-REB-008`, `ARCH-REB-007`,
  `ADR-REB-007` or `VER-REB-007`.
- `docs/notes/evaluator-migration-rehearsal.md` and
  `docs/notes/developing-se-harness.md`. Both are ungoverned paths under
  `AGENTS.md`: they change by pull request and reviewer, carry no
  `Harness-Work-Order` line, and the owner accepts the resulting red managed
  check. The release-sequence step this defect shows to be missing therefore
  belongs to a separate ungoverned pull request, and this work order must not
  smuggle it in.
- `pyproject.toml`, the candidate version, and anything under
  `docs/engineering/release-0-7-0/`. This work order repairs the gate; it does not
  touch the candidate it gates.
- Every release act: candidate commit, promotable build, verification record,
  release record, tag, publication, deployment, maintenance-line mutation,
  credential use, and root-evaluator change.

## Authorized decision envelope

The implementation agent may decide locally: the scenario's internal fixture
layout and adapter selection within what the contract already allows; the
identifiers and prose of the new tests; the wording of the domain-index bullet and
the retained evidence; and the order of the commits.

It may not decide: which of the two routes in question 2 below the scenario takes,
including anything that would make route B's surface necessary; whether to retire
the historical scenario from the lane, which is question 3 below; whether evidence
retains under a new key, which is question 1 below; or anything the *Out of scope*
list names.

## Constraints

- `SPEC-REB-008` rule 4 is the rule that fired. Satisfy it by declaring true
  identities, never by relaxing the comparison.
- `SPEC-REB-008` rule 15, *No diagnostic waiver*: no substring allowlist, no
  ignored exit code, no caller-supplied omission, and no `continue-on-error`
  conversion may be used to make this lane green. If the lane cannot pass with
  true identities, it must stay red and the finding must be escalated.
- The lane runs both platforms and reconciles their normalized results, so the new
  scenario must produce an identical `semantic_sha256` on Windows and Linux across
  two consecutive runs.
- The runner is read-only with respect to the operational root, has no network and
  no credential path, and must leave the checkout unchanged; the existing *Prove
  migration evidence made no checkout change* step must still pass.
- The predecessor must be an already-public, digest-pinned wheel installed from the
  wheel file, because the rehearsal reads installed archive identity from
  `direct_url.json`, which a plain index install does not write. `WO-RLS-011`
  recorded that sharp edge as `MIG229`; do not rediscover it.
- Docker is absent on the author's workstation and only Windows is available
  locally, so the Linux half of the platform reconciliation can only be read from
  a hosted run. Say which figures are local and which are hosted, and never merge
  them.

## Expected change surface

One new scenario fixture; in `.github/workflows/candidate-evidence.yml`, the
`governance-migration` job's scenario path, its two predecessor `env` values, and
the removal of the historical pair from the lane; new tests in
`tests/test_governance_migration.py`; one bullet in the domain index; one retained
evidence file. No change to the migration runner, the contract, the existing
scenarios, or any governing artifact.

`tests/test_hash_bound_integrity.py` is expected to need **no** edit, because its
rule already covers `tests/fixtures/governance_migration/*.json` by glob rather
than by enumeration. Confirm that by running it rather than by reading it; the
byte-rule guard's inventory is the declared patterns, so a new file that matches
an existing pattern is covered while a new pattern would not be.

## Required verification

- `harnessctl rehearse-migration` on the new scenario, run twice, with the
  predecessor and successor resolved outside the checkout and isolated from each
  other: `overall_result: pass`, all nine stages `pass`, `first_failed_stage:
  null`, observed mutations equal to permitted mutations at every stage,
  `operational_state.unchanged: true`, every `external_actions` entry `false`, and
  an identical `semantic_sha256` across the two runs.
- The same reading on the hosted lane on **both** `windows-latest` and
  `ubuntu-latest` at the pinned 3.11, with the reconcile job green. Read it from
  the runs API and quote the run and job identities; a green badge on a push-event
  run is not a reading of the `pull_request` lane.
- The full unit suite, before and after, on each interpreter it is run on, with
  the platform named. The new divergence test must fail against the current
  fixture-and-workflow pair; demonstrate that failure rather than asserting it.
- `harnessctl validate`, `doctor`, and review-phase `preflight` with the governing
  released evaluator from outside the checkout.

## Evidence to record

Retain `docs/engineering/released-evaluator-boundary/evidence/WO-REB-023-migration-scenario-successor.md`
with the artifact, checkpoint, and formal-snapshot binding block, and name the
checkout convention beside the snapshot digest, because that digest hashes
worktree bytes and is not a per-commit figure.

Record: the measured classification outcome and capability difference for the
0.6.0-to-0.7.0 pair, with how each was read; the new scenario's `sha256`,
`fixture_sha256`, and the contract `sha256` and `implementation_sha256` it ran
against; the public 0.6.0 predecessor wheel's name and digest and where the digest
was measured; both `semantic_sha256` values from the local double run and both
from each hosted platform; the before-and-after unit-suite figures labelled by
interpreter and platform; the failing reading of the new divergence test against
the unrepaired pair; the run and job identities of the hosted readings; the fact
that `historical-0.5.0-to-0.6.0.json` is byte-identical, evidenced by digest, and
still exercised by the unit suite after being removed from the lane; the four owner
decisions taken at approval and that they were taken with the boundary measurement
in front of them; the `VER-REB-007` retention reading and that it is a reading
rather than an amendment; and every out-of-scope action not performed.

## Stop and escalate conditions

**All three questions below were answered by the owner at approval on 2026-08-25**,
which is why they were raised while this text was `draft`; the answers are
summarized in *Lifecycle* and written into the scope they shape. They are kept here
with the reasoning that produced them, because a decision is only reviewable
alongside the alternatives it rejected. The recorded reason on the approval
`[[lifecycle_events]]` entry is the authority; this prose is a reading of it.

1. **`VER-REB-007` names `WO-REB-018` as the retention key** — "Retain under the
   `WO-REB-018` key". This work order would retain under its own key. Either that
   is a routine reading of a verification contract written before this work
   existed, or `VER-REB-007` needs an amendment. The owner decides which, and an
   amendment is outside this scope.

   **Answered: the routine reading.** Evidence retains under `WO-REB-023`, and
   `VER-REB-007` is not amended. Two alternatives were rejected: amending the
   verification artifact to name both keys, which is durable but a governing
   amendment outside this scope; and filing this repair's evidence under the
   `WO-REB-018` key literally, which would leave a retained record that does not
   identify the work order that produced it — a predicate `QG-G4` reads. The
   retained record must state this reading explicitly.
2. **Which of two routes the truthful scenario takes.** No longer a measurement —
   *The pair has no expressible boundary* above settles the facts, and they leave a
   decision the implementation agent must not take for itself.

   - **Route A, a version-truthful `compatible` scenario.** Add
     `candidate-0.6.0-to-0.7.0.json`, declaring the predecessor as holding all
     eight capabilities and therefore classifying `compatible`. The lane keeps
     running the real candidate as successor and keeps every other assertion it
     makes today: the nine stages in order, permitted-versus-observed mutations at
     each stage, the unchanged operational state, every external action false, the
     double-replay `semantic_sha256` determinism, and the two-platform
     reconciliation. It asserts strictly less in one respect — the `scenario_id`
     no longer starts with `historical-`, so `MIG404` no longer guards the boundary
     and `governance_migration.py:345` no longer forces the predecessor to be a
     digest-pinned archive. The work order compensates by pinning the predecessor
     wheel anyway and by asserting the `compatible` outcome explicitly in a test,
     so a future version that *does* introduce a boundary fails rather than passes
     quietly. No governing artifact is amended. This is the recommendation, and the
     `[execution_scope]` above is drawn for it.
   - **Route B, a new contract version naming the real capability.** Add a ninth
     capability for typed qualification to a `-v2` contract and model a genuine
     0.6.0-to-0.7.0 boundary, which reading 3 above shows exists in behavior. It is
     the higher-fidelity answer and the one that keeps `historical-` meaning what
     it says. It is also a governing-artifact amendment before 0.7.0 ships:
     `SPEC-REB-008` reserves a new contract version for a migration with new
     semantic stages and requires accountable review, and the scope grows to
     include the contract JSON, its loader, `SPEC-REB-008` and probably
     `REQ-REB-016`. It needs its own scope decision.

   Route B is the better artifact and the worse thing to start days before a
   release. Route A is honest about what it proves and can be read in full by one
   reviewer.

   **Answered: route A.** Route B is rejected for this work order, not judged wrong:
   reading 3 shows the capability it would name is real, so if a later accountable
   act wants the contract to express it, the finding above is the evidence and a
   separate work order is the vehicle. Nothing here authorizes it.
3. **Whether the lane should still run the historical pair as well.** It cannot be
   run against the candidate any more, so the choice is between dropping it from
   the lane while the unit suite keeps exercising it, and adding a second matrix
   dimension that runs it against the public 0.6.0 wheel. Under route A this
   question is nearly settled by the measurement — the historical pair's successor
   can only ever be 0.6.0 — but the second matrix dimension remains expressible, so
   it is a decision and not a deduction.

   **Answered: dropped from the lane, kept in the unit suite.** The second matrix
   dimension is rejected because it reintroduces exactly the released-package
   assertion rejected in *Why the obvious fix is forbidden*. The scenario file is
   not deleted and not edited, and scope item 6 requires its byte-identity to be
   evidenced by digest, so "dropped from the lane" must not become "quietly stopped
   being exercised".

Stop also if: the lane can only be made green by relaxing an identity comparison
or waiving a diagnostic; the new scenario cannot be expressed without editing the
contract or the runner; the two platforms cannot be made to agree; or any
governing artifact turns out to need amendment.

## Completion report format

State, in order: the commits; the scenario's identity digests; the measured
classification outcome for the pair and how it was read; the predecessor wheel
identity and where its digest was measured; the local double-run readings and both
hosted platform readings with run and job identities; the unit-suite figures
before and after, labelled by interpreter and platform, and the divergence test's
failure against the unrepaired pair; the governing `validate`, `doctor` and
`preflight` readings; the answers taken on the three questions above and who took
them; and every out-of-scope action not performed. Label every figure with its
platform and interpreter, and never merge a local figure with a hosted one.
