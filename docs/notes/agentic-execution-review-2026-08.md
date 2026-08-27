# Agentic execution review: evolution, current state, and trajectory

<!-- Target expertise: 7/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

Repository-owned note. It records a read-only review of the tree at
`992fd73` (2026-08-27; 782 commits; v0.2.0 to v0.7.1 in sixteen days) of how
the agentic execution model has evolved, how it works today, and where it is
heading. It grants no approval, verification, or release authority, changes no
lifecycle state, and proposes no work order by itself. Every recommendation
that touches an approved artifact is an amendment under this repository's own
rules.

Method: five independent read-only passes (Git history across every tag; the
command-driven workflow kernel; Phase 4 delegated execution; the agent-facing
surface, with read-only `harnessctl` runs; artifacts, evidence, and decision
rights). Each load-bearing claim was re-verified by grep or execution. The
[complexity audit](complexity-audit-2026-08.md) was used as a lead, not as
evidence; where checked it held, except that its "REL-SEH-015 calls Phase 4
inert" line comes from rejected REL records, while the shipped `REL-SEH-017`
says the opposite. Nothing in the repository was modified.

## 1. Executive assessment

SE Harness has converged, at the interface, on a sound execution kernel: one
selected artifact, a machine-computed next step (`focus`, `check`), explicit
human transitions (`transition --apply`), and commit-bound records with hashed
evidence. The invariants `HRN-001` to `HRN-008` have been stable since v0.6.0
and the mandatory agent reading set shrank to three files plus the selected
chain (about 12k tokens). That core is durable.

Underneath, three strata accumulated in sixteen days and were never retired:
the 0.6.0 self-hosting bootstrap bridge (about 6,000 lines, still shipped,
breaks consumer `doctor`), Phase 4 delegated execution (8,766 lines, 39% of
the package, reachable from the CLI but never exercised on any real work
order), and duplicated engines (two result schemas, two next-step selectors,
three precondition implementations) that let `check` and `transition`
disagree on the same state.

The most consequential finding is the gap between declared and enforced
authority. Human decisions are free-text role strings
(`--decision WO=assurance-owner`) with no identity check anywhere
(`se_harness/workflow.py:606`); execution scope is enforced only in `check`,
from a path list the agent types by hand, and in CI only when the agent
volunteers a trailer. Governance is honour-based for the agent it is designed
to bound, while the machinery that is enforced (evaluator identity,
hash-bound bytes, nonce'd envelopes) defends against threats agents do not
pose.

The right direction is a thin control plane that owns state, scope,
identifiers, and evidence binding, and pushes enforcement to the one boundary
an agent cannot bypass: the commit and pull request. Phase 4's
proposed-workspace broker duplicates Git as a write boundary and should be cut
to its crash-safe apply and scope narrowing. Five changes (a `next` command,
Git-derived change sets, harness-authored evidence and identifiers,
authenticated decisions, deletion of the bootstrap bridge) would remove most
agent friction without weakening a single guarantee.

## 2. Evolution timeline

| Date | Stage | Execution model | Trigger | Evidence |
| --- | --- | --- | --- | --- |
| 08-11 | Prose contract and validator | A 37-line, all-managed `AGENTS.md`; "pick one approved work order"; five CLI commands | Founding thesis: "Code is not the source of product intent." | `4af1241`; `v0.2.0:AGENTS.md` |
| 08-11/12 | Instruction architecture | Managed block shrinks to a three-line gate; `ENGINEERING_HARNESS.md` becomes the single router; `preflight` emits a reading manifest; `Harness-Work-Order:` trailer | "an enforcement boundary that depends too heavily on agents following prose" | `9b42d3b`; `INT-IAR-001`; `ADR-IAR-001` |
| 08-15/16 | Self-hosting evaluator (v0.3, v0.4) | Hash-pinned in-tree evaluator, `accept-candidate`, assurance classification on work orders | Candidate code was validating itself | `addcf26`; `134b745`; `INT-OCA-001` |
| 08-19 | Prose lifecycle handoffs | Named handoff fields and a state-to-next-step table, still computed by the agent | Agents ended turns with "What would you like me to do next?" | `e347e5e` |
| 08-20 | Deadlock, then the released-evaluator boundary | In-tree evaluator removed; an index-installed released wheel outside the checkout evaluates; `mutation_guard` | Changing the evaluator required authorization from the evaluator being replaced (RCA 0.5.0) | `docs/rca/2026-08-20-0.5.0-release-governance-deadlock.md`; `3685a94` |
| 08-20/21 | Deterministic kernel (v0.6.0) | `focus`, `transition`, `check`; `WORKFLOW.json` procedures; `QUALITY_GATES.json` predicates; result schema 2; `[execution_scope]`; `HRN-004` | "different agents can choose different working scopes, mutate related records differently, report unrelated findings" (`INT-WEX-001`) | `5f220a6`; `f97bbb6`; `ADR-WEX-001`, `ADR-WEX-002` |
| 08-21 to 23 | 0.6.0 bootstrap bridge | Predecessor view, migration rehearsal, lock schema 3, role-specific `qualify` | Evaluator 0.5 could not parse the records 0.6 needed (RCA 0.6.0) | `ca275ac`; `7365150` |
| 08-24 | Agentic-execution domain, Phases 1 to 3 | Read-only `harness-orient`; agent and skill contracts; explicit-only writing skills as `harnessctl` clients; `.claude/skills` adapters | "A human may therefore be asked to confirm routine procedural steps" (`INT-AEX-001`) | `6268821`; `65244b1`; `9a740be`; `284b842` |
| 08-24 | Verbatim restitution becomes semantic handoff | Router stops demanding byte-exact output; direct renderer for exact consumers | "Repository instructions can request a format; they cannot prove or enforce exact final bytes." (`ADR-WEX-003`) | `caeebb0` |
| 08-25 | Phase 4 delegated execution | Closed four-operation catalog, five-minute nonce'd envelopes, content-addressed bundles, journaled effect broker, receipts; built in about 72 hours | "validation can detect but not prevent an out-of-scope or stale effect" (`ADR-AEX-007`) | `c7b6c41` to `0bcbea1`; PRs #155, #157, #159 |
| 08-25 | Agent-directive surface | Manifest closed to three files plus the chain; 1 KB `OPERATING_CARD.md`; per-predicate corrective forms; `result_sha256` verified in CI | "about 65 KB of policy prose and 41 KB of machine contracts"; "a blocked handoff checkpoint named its own command as the retry" (`INT-ADS-001`) | `24fcf15`; `543fb85` |
| 08-26/27 | 0.7.x ships; simplification turn | `MG004` and `MG007` retired (-818 lines); root adopts 0.7.1; complexity audit filed | | `8dcd561`; `9ef784d`; `31a963a` |

**Replaced or abandoned:** the all-managed `AGENTS.md`;
the repository-context scaffold (three commits over fourteen days to leave:
`fef8f29`, `01d5351`, `543fb85`); the self-hosting evaluator; prose handoff
tables; verbatim restitution; result schema 1 (still the default on
`transition`, `capture-verification`, and `prepare-release`); workflow
contract v1 to v4 in five days; skill contract v1 to v3 in two days, all three
frozen in `skill_contract.py`; the Phase 2 envelope v1 constructors (about 700
lines, zero product callers).

**Architectural, surviving every rewrite:** the formal graph as sole
authority (`HRN-001`); one bounded work order per iteration (`HRN-003`); "a
record cannot contain the hash of its own commit"; automation prepares `ready`
and never decides (`HRN-005`); thin gate plus one router; released evaluator
outside the checkout; `focus`, `check`, `transition`.

**Coherence verdict.** The contract an agent must honour is smaller and
single-sourced than at any earlier tag. The implementation beneath it is at
its largest (2,727 lines at v0.2.2, 22,571 at v0.7.1) and carries three
unretired strata. Coherence was bought by displacing prose into machine
contracts, not by deletion. Agent-facing shipped policy grew from about 107
lines (v0.2.0) to about 1,800 lines plus 2,500 skill lines (v0.7.0); the
mandatory read set for one work order is now bounded and machine-emitted.

## 3. Current architecture

- **Receiving work.** No selection algorithm exists. The agent picks a work
  order; `focus` projects its governing chain and declared scope; `preflight
  --phase start` admits `approved` or `in_progress` and emits a twelve-file
  reading manifest. `select-work-order` only parses a pull-request body
  (`se_harness/workflow.py:402-468`; `se_harness/preflight.py:34-63`).
- **Bounding.** `[execution_scope].paths` in work-order front matter, enforced
  only by `check --changed-path ... --changes-complete` (`QGP-G4I-PATHS`).
  Paths are agent-typed and never compared to `git diff`
  (`se_harness/workflow_compliance.py:156-165`, `:316-322`). `transition`
  never checks scope; the template CI checks it only when a
  `Harness-Restitution:` trailer is present
  (`templates/repository/standard/.github/workflows/engineering-harness.yml:56-89`).
- **Procedures and checkpoints.** Eighteen `PROC-*`, twenty-four steps, three
  public checkpoints. First match over fifteen `WFL-*` rules; only four steps
  carry gates and correctives (`docs/engineering/WORKFLOW.json:492-624`). The
  gate contract's `transition` checkpoint is unreachable: `_gate_results` has
  one caller, `check_workflow`, which refuses `transition`
  (`se_harness/workflow_compliance.py:395`, `:460`).
- **`harnessctl`.** Computes legality and the next step (`HRN-004`); the sole
  state mutator through atomic staged writes with stale-input checks
  (`se_harness/workflow.py:753-938`). Read-only commands run in-tree;
  mutations require the released evaluator (`MG005`).
- **Artifacts.** 1,045 TOML-front-matter Markdown files. Work orders move
  `draft`, `approved`, `in_progress`, `implemented`, `verified`, `released`; a
  verification record binds `commit`, `evidence_paths`, the dashboard-manifest
  digest, and the evaluator sidecar; a release record binds the tag,
  distribution hashes, and the release unit
  (`docs/engineering/release-0-7-0/verification-records/VREC-SEH-014.md:1-30`).
- **Evidence.** Agent-authored Markdown under `<domain>/evidence/` containing
  three literal lines (`artifact:`, `checkpoint:`, `formal_snapshot_sha256:`)
  matched by substring (`se_harness/workflow_compliance.py:266-291`);
  `capture-verification` writes the record and sidecar in a later commit
  (`se_harness/provenance.py:330-442`).
- **State and progress.** Only front-matter `status` plus append-only
  `[[lifecycle_events]]`. No session, no persisted change set, no partial
  progress. Every command recomputes from disk.
- **Human control.** Declared: seven roles and twelve decision rights; every
  transition needs `--decision ID=ACTOR`. Enforced: the actor is a string of
  at most 128 characters; no Git-author, `GITHUB_ACTOR`, `CODEOWNERS`, or
  signature check exists anywhere in `se_harness/` or `scripts/`.
- **Failure and retry.** A corrective form per failing predicate, with the
  self-loop forbidden at load time; the compatibility path still emits "rerun
  the same command" (reproduced live: `check --checkpoint start` on an
  implemented work order returns `WEX210: WEX210: ...` with that corrective;
  the correct call, `pre-action --procedure PROC-DELIVERY-SELECT`, is nowhere
  suggested). Verified records are terminal; supersession is the only repair.
- **Multiple agents.** Command path: no locks, optimistic byte comparison on
  apply, hand-typed identifiers checked only in the current tree. Phase 4: one
  OS-locked session per repository and `max_parallel_writers` fixed at 1
  (`se_harness/runtime_state.py:150-188`; `se_harness/agent_contract.py:886-887`).
  Orchestration exists only in the roadmap.

**Implemented versus intended.**

- Phase 4 is reachable through `harnessctl delegated-workflow`, but no formal
  work order carries `[agentic_delegation]`, so `resolve_delegation` raises
  `AEXAUTH003` on every real one. It has never run outside tests.
- The three writing skills inject a stub client and print
  `"evaluator_invoked": false` while their `SKILL.md` says they invoke the
  evaluator (`.agents/skills/harness-execute-work-order/scripts/check_scope.py:190-199`;
  `check_prepare.py:174-180`; `guard.py:177-185`).
- `QUALITY_GATES.md` `QG-010` promises that transitions recheck contract
  predicates; `plan_transition` never loads the gate table
  (`se_harness/workflow.py:685-750`).
- `WORKFLOW.md:277` says the evaluated command is never the retry;
  `WORKFLOW.json:83` says "rerun the same command".
- `MG007` is referenced in documents and absent from code.

## 4. Strengths, prioritised

1. **Deterministic next step.** The same repository state yields the same
   restitution across hosts. This is what makes the agent replaceable:
   `ADR-WEX-001`'s observed divergence across ChatGPT, Claude, and Codex is
   closed by construction rather than by prompting.
2. **Commit-bound, terminal records.** 116 of 117 verified records bind a
   commit reachable from `HEAD`; the `RLS-SEH-015` chain walks release record,
   contract, verification record, work order, requirement, specification,
   decision, intent, and root-cause analysis entirely inside the tree.
3. **The released-evaluator boundary.** The only place governance is enforced
   against the code rather than the agent; it is why the bad 0.6.0 release
   was caught (`se_harness/mutation_guard.py:119-196`).
4. **Scope as data.** An out-of-scope write is a coded predicate (`WEX201`),
   not an opinion.
5. **Fail-closed exact predicates.** `pass`, `fail`, or `not_assessable`;
   `not_assessable` honestly names what the harness cannot see.
6. **Repository-native and provider-independent.** Standard library only;
   provider names appear in code only as reject lists
   (`se_harness/agent_contract.py:105-113`).
7. **Candour about enforcement limits.** `ADR-WEX-003` withdrew verbatim
   output enforcement because the repository cannot provide it; `ADR-AEX-004`
   "does not claim hard enforcement against an agent runtime that ignores a
   skill". That candour is what makes the remaining claims trustworthy.
8. **Crash-safe multi-file writes.** `TransitionPlan`'s staged apply, and the
   Phase 4 broker's journal with `human-recovery-stop` and its eleven-stage
   fault matrix (`tests/test_effect_broker.py:308-344`).
9. **Resumability by recomputation.** Any session resumes from the working
   tree alone.

## 5. Weaknesses, by severity

Severe:

1. *Architectural.* **Authority is declared, not enforced.** Any agent can
   pass `--decision VREC-X=assurance-owner`; the value is validated for length
   and control characters only. The mutation guard proves which evaluator
   wrote, never who decided.
2. *Architectural.* **Scope rests on self-declaration.** Twenty-two hand-typed
   paths for `WO-REB-027`; `transition` to `implemented` skips scope; CI checks
   scope only with a volunteered trailer; the `result_sha256` preimage renders
   restitution fields only, so identical digests cover different change sets
   (`se_harness/workflow_result.py:174-207`).
3. *Architectural.* **Phase 4 defends the wrong boundary.** The envelope's
   nonce, five-minute lifetime, revocation store, retry ordinal, and
   two-capture stability guard a token that never leaves the process that
   minted it (`se_harness/cli.py:1259-1304` accepts no envelope input;
   `revoked=` has zero callers; `retry_ordinal` is always 0). Gates reaching
   the broker are caller-asserted JSON (`gates_passed=True` at
   `se_harness/delegated_workflow.py:399`). At least six full-tree digests per
   bundle. It re-implements a version-control write boundary, then still stops
   before Git.
4. *Implementation.* **Duplicate engines that disagree.** `check` accepts a
   work order that `transition` blocks on `I001 lock-entry:*`; `check` demands
   content-bound evidence while `transition` to `implemented` needs only a
   keyed file; the CLI labels every transition failure `WEX201`
   (`se_harness/cli.py:521`).
5. *Implementation.* **Self-hosting residue ships to consumers.** `init`, a
   commit, then `doctor` exits 1 in every fresh repository; `qualify
   predecessor-view` in the wheel imports the unpackaged `repository_tools`;
   six `RLS-SEH-*` identifiers are hard-coded in generic code.

Significant:

6. *Architectural.* The agent is the state machine's memory: no session; the
   formal snapshot digest moves on any artifact edit (`WO-HUP-007` re-bound its
   evidence twice).
7. *Architectural.* Evidence is prose matched by substring; the harness
   neither writes nor rebinds it.
8. *Implementation.* Correctives can still self-loop through the
   compatibility path.
9. *Architectural.* Governance and execution are coupled through front-matter
   shape at thirteen points (`transition` reads `[revision_provenance]`,
   requires `[assurance]`, appends events by name; `capture-verification`
   requires `conforms_to` to equal the union of work-order verification; the
   dashboard generator's manifest is a verification-record field).
10. *Maturity.* Skills are inert for a normal work order: writing skills are
    `disable-model-invocation: true`, require a delegation table no work order
    has, and stub the evaluator. A frontier agent reading `HRN-004` goes
    straight to `harnessctl`, which is correct, so 28 KB of hash-locked skill
    scripts are dead weight.
11. *Maturity.* 467 diagnostic codes across 36 prefixes; `W013` means two
    things; failures are classified by message substring.
12. *Implementation.* JSON mirrors of Python constants read by no consumer.

Moderate:

13. *Architectural.* Human-workflow assumptions: pull-request bodies as
    transport; decision steps typed as English `response` strings;
    `TECHNICAL_COMMUNICATION.md` governing the agent's prose; commit
    choreography as the state machine.
14. *Maturity.* Traceability stops at roles; `VREC-IPK-001` binds a GitHub
    merge-preview commit absent from the clone.
15. *Maturity.* `ADR-AEX-004` to `ADR-AEX-007` are `approved` in front matter
    and "Status: Proposed" in the body.
16. *Implementation.* Every command runs the 3,679-line validator over all
    1,045 artifacts (twice for `focus_schema2`); any merge to `main`
    invalidates every branch's handoff evidence; thirteen CI jobs per pull
    request.

## 6. Agent cognitive-load analysis

Traced on `WO-REB-027`, a normal product-code work order (eight commits,
PR #198).

| Dimension | Measured |
| --- | --- |
| Auto-loaded by Claude Code | `CLAUDE.md` importing `AGENTS.md`: 7.6 KB, about 1.9k tokens, 79% owner narrative |
| Mandatory reading | Twelve-file manifest, 49.5 KB, about 12.4k tokens; 30% repository-generic |
| Realistic reading when anything fails | Plus 115 KB of routed policy, about 41k tokens; worst case with notes and skills about 100k |
| Concepts | Eleven artifact types; nine transitions plus legacy vocabulary; fifteen rules, eighteen procedures, twenty-four steps, three checkpoints; eleven gates and 36 predicates; twelve decision rights and seven roles; evaluator versus candidate; three file-ownership classes; hash-bound classes; corrective forms; commit ordering; a second execution model to recognise and ignore |
| Decisions the agent makes alone | Which work order; which checkpoint and procedure; which evaluator binary; new identifiers across every ref; the complete changed-path set; evidence file name, directory, and body; commit partitioning; whether a deviation is acceptable; when to stop; whether a `doctor` failure is skew or damage |
| Commands on the happy path | Seventeen steps from `doctor` to the third human decision |
| State carried in context | Launcher path; work-order id and thirteen-entry scope; twenty-two changed paths; current snapshot digest; commit roles; verbally obtained decisions re-typed as `--reason`; `result_sha256`; the reserved record id |
| Provided automatically | Rule, procedure, step; governing chain; declared scope; manifest; corrective with the snapshot substituted; renderer and digest; trailer parse with CR offset; record digests |
| Left to inference | Which `check` invocation fits the state; the change set; the evidence body; evaluator selection; commit and trailer discipline; identifier allocation; skew versus drift versus damage; the handoff's seven MUSTs |

Every failure mode has precedent in the repository: running the in-tree CLI as
the evaluator (RCA 0.5.0, `RC-060-09`); the wrong checkpoint (reproduced); a
CRLF trailer (`REQ-ADS-004` exists because it recurred); editing hash-locked
files (`RC-060-02`); stale evidence binding (`WO-HUP-007`, twice); an
incomplete change set (unobservable by design); rebase orphaning a ready record
(PR #176); a dirty worktree at capture (`PV001`).

Load can be cut with most leverage by: one `next` call returning manifest,
scope, and the exact next command; change sets derived from Git;
harness-authored and harness-rebound evidence; evaluator auto-resolution from
the lock; identifier allocation across refs; trailer and pull-request-body
generation; structured decision records; and dropping the `AGENTS.md` owner
region from the manifest.

## 7. Gaps between the implementation and an execution control plane

| Control-plane property | Today | Gap |
| --- | --- | --- |
| Agent requests the next authorized action | The next step is emitted only after an operation (`restitution.next`); `focus` gives the decision step, not the `check` command | No `next` or session command |
| Harness determines the allowed context | Manifest and declared scope are machine-emitted | Close; scope is checked against agent-typed paths |
| Harness returns canonical state | Schema 2 is canonical and digested | Schema 1 still default on three mutators; the digest excludes the change set |
| Agent performs the work | Freely, in the working tree | Right as it is |
| Harness validates outcomes | `check` at handoff; CI recomputes only with a trailer; Phase 4 accepts asserted gates | Enforcement is opt-in at the only unavoidable boundary |
| Harness determines the next transition | `transition` validates edge legality atomically | Its own precondition engine, not the gate contract |
| Humans retain authority | Role string on every transition | Unauthenticated |
| Multiple agents | None in the command path; forbidden in Phase 4 | Git branches already isolate; nothing uses them as the model |

**Challenge to the model.** "The harness returns canonical instructions" is
the weakest leg. Capable agents do not need instructions; they need an
unambiguous state (what is selected, allowed, and missing) and a boundary they
cannot argue with. Prose instructions are exactly what `ADR-IAR-001` and
`ADR-WEX-003` already found unenforceable. The stronger form is state plus
boundary: the harness owns state, scope, identifiers, and evidence binding;
enforcement lives at commit and pull-request time against Git facts (diff,
author, signature), not at a proposed-workspace broker that re-implements a
version-control system. Phase 4 chose the broker because "validation can
detect but not prevent"; a required, non-optional CI gate on the pull request
is prevention for anything that reaches `main`, and it is the boundary that
survives an agent ignoring every skill.

## 8. What should be preserved

- The formal artifact graph and validator; Markdown with TOML front matter as
  the store.
- `HRN-001` to `HRN-008`, the stop-condition list, and the gate, router, and
  card structure.
- `focus`, `check`, `transition` as the kernel; schema 2 and `result_sha256`;
  corrective forms and the rule that the evaluated command is never the retry.
- Commit-bound, terminal verification and release records; supersession and
  amendment records; "a record cannot contain the hash of its own commit".
- The released-evaluator boundary; `MG001` to `MG006`; the runtime and
  evaluator identity layers; hash-bound classes with the no-default-mode rule.
- Explicit `not_assessable`; fail-closed gates.
- `TransitionPlan`'s staged atomic apply; the broker's journaled apply,
  rollback, and `human-recovery-stop` with its fault tests;
  `resolve_delegation` scope narrowing; the intent of `_DEFAULT_DENIED`.
- Provider neutrality: canonical skills under `.agents/`, reject lists for
  provider markers, no runtime authority.

## 9. What should be simplified, redesigned, or removed

| Action | Target | Why |
| --- | --- | --- |
| Remove | Predecessor-view adapters, the migration stage machine, the recovery rehearsal, `validate_governor_transition.py`, lock schema 1, `accept-candidate`, the `governance-migration-protocol` hash-bound class | Bootstrap-era bridge; breaks consumer `doctor`; cannot pass the upgrade the owner wants |
| Remove | Envelope nonce, lifetime, revocation, retry, and stability; v1 envelope constructors; `skill_contract.py`; `agent_contract.json`, `effect_contract.json`, and the other JSON mirrors; `refuse_prohibited_action`; dry-run receipts; stub skill clients | Zero product callers, or defending a trust boundary that does not exist |
| Redesign | The Phase 4 write boundary | Agent works on a branch; the harness derives the change set from Git; the pull-request gate is mandatory. Keep journaled apply only for the harness's own multi-file artifact writes |
| Redesign | The decision channel | Structured decision records (role, artifact, outcome, reason, signer) validated against an identity source and consumed by `transition` |
| Consolidate | Schema 2 only; `_recommend` delegates to `select_rule`; `plan_transition` evaluates the contract's `transition` gates; one repository snapshot loader; one validator invoker | Removes every `check` and `transition` disagreement |
| Simplify | Evidence: a harness-authored packet with a machine header, automatic rebind, identifier allocation across refs, trailer generation | Turns the top agent failure modes from "remember" into "cannot get wrong" |
| Simplify | Skills: keep `harness-orient` as a real wrapper; retire the three stubbed writing skills until they call the evaluator; fold the operator brief into the communication policy | Inert today; 28 KB of hash-locked reading |
| Simplify | Reading manifest: drop the `AGENTS.md` owner region; keep commands and managed-path lists as a generated block | 30% of the mandatory set is repository-generic |

## 10. Recommended target architecture

```text
Human approves the work order (scope, assurance class, delegation class)
        |
Agent:  harnessctl next . [--artifact WO]        one call; no prior reading
        |   returns: selected artifact and state, governing chain, declared
        |            scope, reading set, exact next command, decision required
        v
Agent works on a branch (any host, any tools)
        |
Agent:  harnessctl check . --artifact WO --checkpoint handoff --from-git <base>
        |   change set derived from Git; evidence packet written or rebound
        |   by the harness
        v
Commit and pull request (trailer and restitution line from `harnessctl pr-body`)
        |
CI gate, mandatory: recompute the check at the head; scope, digest, evaluator
        |
Human:  signed decision record -> harnessctl transition --decision-record ...
        |   identity verified; role checked against DECISION_RIGHTS
        v
capture-verification and prepare-release, unchanged, bound to a
merge-reachable commit
```

Principles:

1. State lives in the harness, not the agent: selection, scope, identifiers,
   evidence binding, the next command.
2. Enforcement lives at Git boundaries: the diff for scope, the pull-request
   gate for gates, signature or actor for authority.
3. Instructions shrink to the router and the card; everything else is returned
   by `next` on demand.
4. Concurrency is branches: two agents on two work orders are two branches;
   the formal snapshot should be scoped to the governing chain so a merge
   elsewhere does not invalidate handoff evidence.
5. Delegation is a work-order attribute that unlocks `transition` for start,
   completion, and record preparation when the gate is green; no envelope, no
   broker.
6. Phase 5 orchestration is not harness machinery: a host's subagents are
   execution detail, and the combined branch is what the gate validates.

## 11. Top five next changes, by leverage

1. **Ship `harnessctl next` and derive change sets from Git.** Collapses
   `focus`, `preflight`, and "which check" into one call and removes the
   largest agent-carried state. Fixes the live `WEX210` self-loop. It composes
   existing functions: `focus_schema2`, `run_preflight`,
   `select_current_step`, `git diff --name-only`.
2. **Make the pull-request gate mandatory and scope-aware without a
   trailer.** CI already recomputes the handoff check; run it unconditionally
   on the diff and fail on `WEX201`. This is the only change that turns scope
   from honour-based into enforced for any agent.
3. **Authenticate decisions.** Bind `--decision` to an identity source (commit
   signature, or `GITHUB_ACTOR` in CI) and check the role against
   `DECISION_RIGHTS.md`. Until this exists, "accountable humans retain
   authority" is a documentation claim.
4. **Delete the bootstrap bridge and Phase 4's dead weight** (audit P0-1 to
   P0-4, P1-3, P1-5 to P1-7): about 10,000 lines; fixes consumer `doctor`;
   removes the second execution model agents must recognise and ignore. Decide
   Phase 4 first (audit P0-5); the recommendation here is to keep journaled
   apply and narrowing and drop the broker and envelope.
5. **One result schema, one selector, one precondition engine,
   harness-authored evidence.** Ends every `check` and `transition`
   disagreement and the substring-matched evidence contract, and makes
   `result_sha256` cover the change set so the restitution line proves what
   was declared.

## 12. Long-term trajectory

As agents become more capable, the durable pieces are the ones that bind facts
an agent cannot argue with: the artifact graph, commit-bound terminal records,
the released-evaluator boundary, deterministic next-step computation, and the
pull-request gate. The pieces likely to disappear are those that exist to
steer agent behaviour through prose or ritual: the communication policy as an
agent obligation, the prose handoff MUSTs, skill scripts that wrap commands
the agent can call directly, and Phase 4's envelope apparatus. The harness
becomes more valuable if it becomes the accountable memory and boundary for
autonomous work, and a bottleneck if it keeps asking the agent to carry its
state and to be trusted at exactly the points where it claims not to trust it.

## Know what is authoritative

This note observes and recommends. Formal artifacts under `docs/engineering/`
and the accountable owners named in `DECISION_RIGHTS.md` decide. If this note
and an approved artifact disagree, the artifact governs and the note is the
thing to correct.
