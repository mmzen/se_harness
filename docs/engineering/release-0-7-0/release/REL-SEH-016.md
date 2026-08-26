+++
id = "REL-SEH-016"
type = "release_contract"
title = "Release se-harness 0.7.0 as the first ordinary schema-3 release"
status = "draft"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
gates = ["WO-REB-008", "WO-REB-009", "WO-REB-010", "WO-REB-011", "WO-REB-012", "WO-REB-013", "WO-REB-014", "WO-REB-015", "WO-REB-016", "WO-REB-017", "WO-REB-018", "WO-REB-019", "WO-REB-020", "WO-REB-021", "WO-REB-022", "WO-REB-023", "WO-HUP-004", "WO-HBI-001", "WO-HBI-002", "WO-HBI-003", "WO-HBI-004", "WO-AEX-001", "WO-AEX-002", "WO-AEX-003", "WO-AEX-004", "WO-AEX-005", "WO-VSP-007", "WO-LRE-001", "WO-IPK-001", "WO-RLO-004", "WO-RLO-005", "WO-RLO-006", "WO-WEX-003", "WO-TCM-001", "WO-TCM-002", "WO-ADS-001", "WO-ADS-002", "WO-RLS-011"]
+++

# Release Contract: Release se-harness 0.7.0 as the first ordinary schema-3 release

## Lifecycle and authority

This contract, once approved by the release owner, is what permits a promotable
build, the candidate commit, and release preparation. Its authoritative state,
and the timestamp and reason of every decision taken on it, are the front matter
and `[[lifecycle_events]]` above; read those rather than this prose. It is the
fifth contract issued for this release and the successor to `REL-SEH-015`.

**This contract is `draft`.** Nothing below is authority yet. It carries a
thirty-eight-work-order allow-list measured over `main` at
`e98b7885b016529aa2c262ad577acdc270bc9376`. On approval that list becomes the
exact 0.7.0 release unit and can no longer be widened, narrowed, or repaired in
place; a work order that reaches `implemented` with bytes in the packaged
surface after that timestamp would be a stop condition whose only remedy is
rejecting this contract and issuing `REL-SEH-017`.

## Why this contract supersedes `REL-SEH-015`

`REL-SEH-015` was approved at 2026-08-25T12:57:58Z on a thirty-six-work-order
allow-list. It defined its own stop condition in three places — under **Lifecycle
and authority**, under **Release unit**, and under **Rollback criteria and
procedure** — in the same words each time: a work order that reaches
`implemented` with bytes in the packaged surface after that timestamp is a stop
condition, "and the only remedy is rejecting this contract and issuing
`REL-SEH-016` with the re-measured unit. There is no in-place correction to
`gates`."

That condition occurred, twice, and neither instance is the one `REL-SEH-015`
anticipated. It named `WO-AEX-006` on open pull request #155 as the known live
instance. Pull request #155 is still open, at head `61c6880`, and its bytes are
still absent from `main`. What landed instead were two repairs to this release's
own qualification program:

- `WO-RLO-006`, "Tear down the reparse point without the 3.12 predicates",
  reached `implemented` at 2026-08-25T20:22:47Z — five hours and twenty-five
  minutes after the freeze.
- `WO-REB-023`, "Run the governance migration lane against a scenario whose
  successor is the candidate", reached `implemented` at 2026-08-26T06:47:01Z —
  the following morning.

Both are verified. `VREC-RLO-006` verified `WO-RLO-006` at 2026-08-26T08:06:11Z
against candidate commit `c8b3693f896822e029afcdf85c0c7cad25bf5282`, conforming
to `VER-RLO-005`. `VREC-REB-020` verified `WO-REB-023` at 2026-08-26T07:58:28Z
against candidate commit `0ea54d18ed9812cc25d8aca4482a70db90cad546`, conforming
to `VER-REB-007`. Both reached `main` through true merges, of pull requests #167
and #168, and both bound candidates remain ancestors of
`e98b7885b016529aa2c262ad577acdc270bc9376`.

The stop condition turns on whether their bytes are in the packaged surface, and
that was measured rather than argued. Between them the two work orders changed
six files outside `docs/`:

| File | Change | In the packaged surface |
| --- | --- | --- |
| `tests/test_publication_rehearsal.py` | +352 / -0 | **yes** — the sdist ships `tests/test*.py` |
| `tests/test_governance_migration.py` | +129 / -9 | **yes** |
| `tests/test_standard_repository_lifecycle.py` | +4 / -1 | **yes** |
| `.github/scripts/rehearse_publication.py` | +52 / -8 | no — this repository's own CI |
| `.github/workflows/candidate-evidence.yml` | +3 / -3 | no — this repository's own CI |
| `tests/fixtures/governance_migration/candidate-0.6.0-to-0.7.0.json` | +1 / -0 | no — `tests/fixtures/**` is not shipped |

Three files totalling **+485 / -10 distributed lines** therefore enter the
packaged surface with no gate in `REL-SEH-015` naming them. That membership was
confirmed by building an explicitly non-promotable ephemeral source
distribution from `git archive` of `main` outside the checkout and reading its
member list: all three test modules are present, `tests/fixtures/**` contributes
zero members, and the only `.github` members are the four distributed
*template* files under `templates/repository/standard/.github/`, not this
repository's own workflows. The same probe reproduced the 0.6.0 sdist digest
recorded in `RLS-SEH-012`, which is why the measurement is trusted to describe
the genuine released surface rather than an artefact of the local toolchain.

`REL-SEH-015` is therefore rejected and this contract re-issued, exactly as
`REL-SEH-015` prescribed for itself. No approved allow-list was widened,
narrowed, or repaired in place. `REL-SEH-015`'s own lifecycle events, including
the release owner's real approval at 2026-08-25T12:57:58Z, are preserved
unrewritten as immutable rejected history, and it joins `REL-SEH-012`,
`REL-SEH-013`, and `REL-SEH-014` in that history. No work was started under
`REL-SEH-015` beyond `WO-RLS-011`, whose own authority is separate and is
discussed below: no version identity was moved on any branch that reached
`main`, no promotable distribution was built, and no candidate commit exists.

`REL-SEH-015` named no release contract in `WO-RLS-011`'s relations and
`WO-RLS-011` names none in return, so rejecting `REL-SEH-015` orphans nothing in
the graph and no successor work order is required for the rejection itself. That
was measured, not assumed: `WO-RLS-011`'s `relations` table contains no
`release_contract` entry.

On 2026-08-26 the repository owner, shown this measured stop condition and its
cost, chose from measured options to reject `REL-SEH-015` and issue this
contract gating thirty-eight work orders, rather than ship from an earlier
candidate or amend an approved allow-list. Two alternatives were closed by
measurement before that choice was put:

- Shipping from a candidate that predates the two repairs is not available.
  At `6fdb23a0`, which carries the 0.7.0 version bump and `WO-RLS-011`'s
  qualification but neither fix, the hosted `SE Harness Candidate Evidence`
  lane is a **failure**: run 32886901131 shows `Governance migration` failing on
  both platforms with four dependent jobs skipped. That is the defect
  `WO-REB-023` repaired.
- Waiting is not available either, in the sense that there is nothing to wait
  for: at `e98b788` all four hosted lanes are green, all nine candidate-evidence
  jobs pass, and `Publication Rehearsal` passes on both runner platforms for the
  first time since `WO-RLO-006`'s repair.

On 2026-08-26 the owner separately decided that `WO-RLS-011`'s stale
exact-candidate qualification is to be re-measured inside `VREC-SEH-013` rather
than through a successor work order. That decision and its consequences are
recorded below under **`WO-RLS-011`: approved, with a superseded qualification
reading**.

Approval of this contract will authorize none of the following, each of which
remains a separate later decision: the promotable build, the candidate commit,
`VREC-SEH-013` or `RLS-SEH-013` preparation or transition, the governance commit
carrying this packet, branch push, credential use, tag creation, GitHub or PyPI
publication, Pages deployment, `release/0.7` maintenance-line mutation,
external policy change, or root-evaluator upgrade.

## Release unit

One incremental `se-harness` 0.7.0 release derived from one clean candidate
commit: a recipe-bound reproducible wheel, a normalized source distribution, a
checksum manifest, a schema-2 bound distribution table, an immutable `v0.7.0`
tag, GitHub Release assets, publication of the same qualified files to PyPI,
the canonical `release/0.7` maintenance line, and a release-bound static
Explorer demonstration.

The historical release-bearing work added after the immutable `v0.6.0` baseline
is exactly these thirty-seven work orders. Every row was measured as active,
`implemented`, holding work-order-keyed evidence, absent from the `v0.6.0` tree,
unnamed by any released release record, and holding verified assurance coverage.

| Work order | Outcome | Verified coverage |
| --- | --- | --- |
| `WO-REB-008` | Correct publication validation for rejected bootstrap history | `VREC-REB-004` |
| `WO-REB-009` | Use candidate semantics for immutable release-archive qualification | `VREC-REB-005` |
| `WO-REB-010` | Provide exact Git context to release-candidate tests | `VREC-REB-006` |
| `WO-REB-011` | Remove the inapplicable candidate-root doctor gate | `VREC-REB-007` |
| `WO-REB-012` | Pin the released distribution build backend | `VREC-REB-008` |
| `WO-REB-013` | Rebuild released bytes on their retained platform | `VREC-REB-009` |
| `WO-REB-014` | Normalize Windows Git-Bash release paths | `VREC-REB-010` |
| `WO-REB-015` | Use one long Windows candidate-test temp path | `VREC-REB-011` |
| `WO-REB-016` | Retain the proven predecessor view for Pages generation | `VREC-REB-012` |
| `WO-REB-017` | Separate Pages plan output consumption and view setup | `VREC-REB-013` |
| `WO-REB-018` | Implement the predecessor-to-successor governance migration rehearsal | `VREC-REB-014` |
| `WO-REB-019` | Centralize lifecycle semantics and rejected-history handling | `VREC-REB-015` |
| `WO-REB-020` | Implement role-specific release qualification commands | `VREC-REB-016` |
| `WO-REB-021` | Implement the declared environment entry-point safety rule | `VREC-REB-019` |
| `WO-REB-022` | Repair the junction-predicate capability rule on the pinned Python 3.11 lane | `VREC-REB-018` |
| `WO-REB-023` | Run the governance migration lane against a scenario whose successor is the candidate | `VREC-REB-020` |
| `WO-HUP-004` | Replace version-specific predecessor CI with portable governor succession | `VREC-HUP-004`, `VREC-HUP-005` |
| `WO-HBI-001` | Declare hash-bound text classes and assess their completeness in `doctor` | `VREC-HBI-001` |
| `WO-HBI-002` | Take every hash mode from the declared class and fix the lock's divergence | `VREC-HBI-002` |
| `WO-HBI-003` | Declare a byte rule for the byte-exact surfaces no recorded digest binds | `VREC-HBI-003` |
| `WO-HBI-004` | Declare byte-exact surfaces by tree and derive the guard's inventory from the tracked set | `VREC-HBI-004` |
| `WO-AEX-001` | Implement the read-only `harness-orient` pilot | `VREC-AEX-001` |
| `WO-AEX-002` | Implement runtime-neutral AEX core contract validation | `VREC-AEX-002` |
| `WO-AEX-003` | Implement the single-agent outcome skills MVP | `VREC-AEX-003` |
| `WO-AEX-004` | Install repository-scoped Codex and Claude skill surfaces | `VREC-AEX-004` |
| `WO-AEX-005` | Implement live observation and delegated authority derivation | `VREC-AEX-005` |
| `WO-VSP-007` | Align prepared VREC supersession with lifecycle validation | `VREC-VSP-002` |
| `WO-LRE-001` | Implement declared legacy release-evidence exemptions and the pre-apply upgrade refusal | `VREC-LRE-001` |
| `WO-IPK-001` | Implement the qualified integration-package lane | `VREC-IPK-001` |
| `WO-RLO-004` | Implement recipe-bound release build replay | `VREC-RLO-004` |
| `WO-RLO-005` | Rehearse the credential-free last mile on both runner platforms | `VREC-RLO-005` |
| `WO-RLO-006` | Tear down the reparse point without the 3.12 predicates | `VREC-RLO-006` |
| `WO-WEX-003` | Implement semantic-fidelity lifecycle handoffs | `VREC-WEX-006` |
| `WO-TCM-001` | Implement managed technical communication and the operator-brief skill | `VREC-TCM-002`, with a disclosed limitation stated below |
| `WO-TCM-002` | Align router contract tests with the managed technical-communication route | `VREC-TCM-001` |
| `WO-ADS-001` | Implement enforced failure rendering, shared next-step resolution, the operating card, trap diagnostics, the restitution digest, and router scope | `VREC-ADS-001`, with a disclosed limitation stated below |
| `WO-ADS-002` | Close the reading manifest, minimise the operating card, and retire the repository-context file | `VREC-ADS-002`, with a disclosed limitation stated below |

`WO-RLS-011` adds the 0.7.0 versioning, integrated qualification,
reproducibility, exact-candidate evidence, and aggregate-VREC preparation
needed to form the final thirty-eight-work-order release unit.

This contract is an explicit allow-list. It is not an inference from dates,
branches, merge order, lifecycle status, or every commit after the baseline. On
the release owner's approval it becomes fixed authority: the list is re-measured
against the graph immediately before that transition, and from then on it can
only be replaced, not corrected. `WO-RLS-011` is obliged to report any work order
that reaches `implemented` with bytes in the packaged surface after that
timestamp, as a stop condition rather than as an edit.

## `WO-RLO-006` and `WO-REB-023`: the two additions, and what they change

Both are admitted because their authorized bytes are in the 0.7.0 packaged
surface, measured as set out above. Neither is admitted on the strength of being
recent, merged, or related to the release.

`WO-RLO-006`, "Tear down the reparse point without the 3.12 predicates", is
`implemented` as of 2026-08-25T20:22:47Z and verified by `VREC-RLO-006` against
commit `c8b3693f896822e029afcdf85c0c7cad25bf5282` at 2026-08-26T08:06:11Z,
conforming to `VER-RLO-005`. It repaired the publication rehearsal's junction
teardown so that a directory reparse point is classified and removed without
relying on Python 3.12 path predicates that the pinned 3.11 lane does not have.
Its distributed change is the 352 added lines of
`tests/test_publication_rehearsal.py`; its change to
`.github/scripts/rehearse_publication.py` is this repository's own CI and is not
distributed.

`WO-REB-023`, "Run the governance migration lane against a scenario whose
successor is the candidate", is `implemented` as of 2026-08-26T06:47:01Z and
verified by `VREC-REB-020` against commit
`0ea54d18ed9812cc25d8aca4482a70db90cad546` at 2026-08-26T07:58:28Z, conforming
to `VER-REB-007`. It re-pointed the migration rehearsal at a scenario whose
declared successor is the candidate under test, and repaired a lane assertion
that the removal of the historical predecessor pair had broken. Its distributed
change is `tests/test_governance_migration.py` and
`tests/test_standard_repository_lifecycle.py`; the fixture it added and the
workflow it edited are not distributed.

Two facts about these additions are stated because they are the reason the
aggregate figures below moved less than the work-order count did, and because an
unexplained flat count invites the suspicion that it was inherited rather than
measured.

- Neither addition brings a new verification contract. `WO-RLO-006` conforms to
  `VER-RLO-005`, already in the union through `WO-RLO-005`; `WO-REB-023`
  conforms to `VER-REB-007`, already in the union through `WO-REB-018`. The
  verification-contract count is therefore twenty-one on the whole-`gates`
  basis, unchanged from `REL-SEH-015`, and this was measured over the graph, not
  carried forward.
- Neither addition brings a new requirement. `WO-RLO-006` implements
  `REQ-RLO-015` and `REQ-RLO-016`, both already in the union through
  `WO-RLO-005`; `WO-REB-023` implements `REQ-REB-016` and `REQ-REB-017`, both
  already in the union through `WO-REB-018`. The requirement union is therefore
  forty-eight, unchanged, on the same measured basis.

What did move is the keyed-evidence-path count, by four, because each addition
retains two work-order-keyed evidence files.

## A correction to how `REL-SEH-015` described the suite

`REL-SEH-015` justified including `WO-HBI-003` and `WO-HBI-004` while describing
their changes as touching "the suite's byte-exact guard, not a distributed
byte". That parenthetical is wrong on the measured packaged surface, and this
contract states so rather than repeat it.

The source distribution ships `tests/test*.py`. `WO-HBI-003` changed
`tests/test_hash_bound_integrity.py` by 70 added lines and `WO-HBI-004` changed
the same file by 82 added and 12 removed lines plus
`tests/test_agentic_execution.py` by 27 added and 1 removed. Those are
distributed bytes. Their `.gitattributes` changes are confined to the
owner-controlled region and are not distributed.

The conclusion is unaffected: both work orders were included and remain
included, and the classification call the release owner is asked to confirm
below is unchanged. What changes is the reasoning — they are included because
they change distributed bytes, which is the ordinary rule, and not only because
of the secondary argument about which bytes Windows qualification reads. Stating
this matters because it is the same rule that requires `WO-RLO-006` and
`WO-REB-023`, and a contract that applied one rule to the additions and a
different one to the incumbents would not be an allow-list.

## `WO-RLS-011`: approved, with a superseded qualification reading

`WO-RLS-011` is `implemented` as of 2026-08-25T18:43:37Z. It was approved at
2026-08-25T12:35:00Z, before `REL-SEH-015`, and its approval is not carried by
this contract and is not disturbed by `REL-SEH-015`'s rejection. It remains in
this unit.

Its retained exact-candidate evidence, however, no longer describes a commit in
the release's history. `WO-RLS-011`'s completion reason declares candidate
`f76da5727e86fc53375bfa5cafcfcbf168c7456e`, tree `52fdae8c`, at 887 artifacts,
with the census 36 / 21 / 48 / 37. That commit predates `WO-RLO-006` and
`WO-REB-023`, so it is superseded as a candidate: shipping from it would ship
the failing migration lane recorded above. The graph now reads 891 artifacts and
the census is 38 / 21 / 48 / 41.

On 2026-08-26 the repository owner decided, from measured options, that the
re-qualification is folded into `VREC-SEH-013` rather than issued as a successor
work order. `VREC-SEH-013` therefore carries three obligations that follow from
that decision:

- It re-measures every figure at the new candidate commit, and takes none from
  `WO-RLS-011`'s retained reading.
- It discloses, in its own prose, that `WO-RLS-011`'s retained exact-candidate
  reading describes superseded commit `f76da572` at 887 artifacts and the 36 /
  21 / 48 / 37 census, and that those figures are historical rather than wrong.
- It carries `WO-RLS-011`'s own disclosed limitations forward unsoftened. In
  particular `WO-RLS-011` disclosed that "No digest measured on this workstation
  is bindable: the normalized digest differs by interpreter." That limitation is
  not resolved by this contract and must not be restated as resolved.

`WO-RLS-011` is not re-issued and its prose is not amended. The harness has no
re-approval transition with which to amend an approved work order's narrative,
and rejecting an otherwise-correct work order over a stale measurement would
cost a succession for prose. This section is the disclosure. Read this
contract's `gates` and `VREC-SEH-013`'s measured figures for the release's real
census, never `WO-RLS-011`'s retained reading.

## `WO-TCM-001`: covered, with an accepted limitation the release must carry

`WO-TCM-001` holds verified assurance coverage through `VREC-TCM-002`, captured
against candidate commit `f7b69d0ad40321caa0520f9fed137be8e32bcf1f` and verified
at 2026-08-25T10:51:11Z.

The coverage is real but it is not a clean pass, and this contract states that
rather than let `gates` imply otherwise. `VER-TCM-001`'s **Manual assessments**
section requires two reviewers to independently record the intended fact, actor,
action, condition, qualification, normative force, and result before seeing
candidate output, and its **Evidence retention** list requires a retained manual
review form carrying those judgments and their dispositions. Those judgments do
not exist. The bound evidence says so itself: the eleven-case corpus is in place
and automated tests confirm its structure and exact token presence, but the
reviewer judgments are not yet recorded and must be completed before a record
can claim the semantic and operator-comprehension conditions passed.

The owner verified `VREC-TCM-002` with that gap disclosed rather than record the
reviews first or reject. The semantic and operator-comprehension conditions of
`VER-TCM-001` are therefore accepted residual risk on this release, not
satisfied conditions. A verified record cannot be corrected, so the disclosure
stands permanently in `VREC-TCM-002`'s prose and in its transition reason.
Closing the gap properly would require recording the two judgments, retaining
the review form, and binding it through a successor verification record; that is
later governed work and is not in this release unit.

`VREC-SEH-013` must name `WO-TCM-001` and must not restate its coverage as
unqualified. `VREC-SEH-013` is `WO-TCM-001`'s second verified coverage, not its
first.

## `WO-AEX-005`: admitted, and what it does and does not activate

`WO-AEX-005`, "Implement live observation and delegated authority derivation",
is admitted. It is `implemented` as of 2026-08-25T10:29:40Z and verified by
`VREC-AEX-005` against commit `5846dca8b2fe84d3c2c94c9fe3a5799532a76271` at
2026-08-25T10:39:01Z, conforming to `VER-AEX-001` and `VER-AEX-004`.

It must be in the unit because its authorized bytes are in the 0.7.0 packaged
surface. Two parts of that surface reach adopting repositories:

- `templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md`
  gains an optional `[agentic_delegation]` table and a guidance paragraph. This
  is a managed-surface change that adopting repositories receive on upgrade.
- `templates/repository/standard/scripts/validate_engineering_artifacts.py`
  gains 147 lines that validate that table. This is a distributed managed
  validator change.

Four new runtime modules also ship in the wheel: `se_harness/agent_contract.py`,
`se_harness/delegated_authority.py`, `se_harness/repository_state.py`, and
`se_harness/runtime_state.py`. They are reachable only from each other.
`se_harness/cli.py` references none of them, and no command path invokes
`delegated_authority`. They are therefore inert in 0.7.0 and activate only when
`WO-AEX-006` through `WO-AEX-008` land. Publishing 0.7.0 ships governed,
verified, tested, unreachable scaffolding, and the release notes must not
describe delegated execution as available.

Phase 4 is explicitly sequential and is excluded from this unit. `WO-AEX-007` and
`WO-AEX-008` are approved and not started. `WO-AEX-006` is no longer unstarted:
it reads `implemented` on open pull request #155, "implement transactional effect
broker", measured at that branch's head `61c6880`. It is excluded all the same,
by name, on the owner's 2026-08-25 decision to ship 0.7.0 without waiting for
Phase 4 — but the exclusion depends on the candidate's history, not on the work
order's lifecycle status, and the release notes must not describe delegated
execution as available on the strength of it. None of the three is blocked by
this release.

`WO-AEX-005` resolved a declared test-contract conflict rather than waiving it:
a legacy test had required the candidate and released work-order templates to be
byte-identical. The amended test now reconstructs the candidate template from
the unchanged released root template plus the exact declared delegation table
and guidance paragraph, and separately proves the released template carries no
delegation table. The released root copy was not edited, which the root managed
integrity rules require.

## `WO-ADS-001` and `WO-ADS-002`: admitted, with a disclosed manual gap

Both are admitted, and both must be in the unit because their authorized bytes
are in the 0.7.0 packaged surface and in the distributed managed templates that
adopting repositories receive on upgrade.

`WO-ADS-001`, "Implement enforced failure rendering, shared next-step resolution,
the operating card, trap diagnostics, the restitution digest, and router scope",
is `implemented` as of 2026-08-25T11:15:03Z and verified by `VREC-ADS-001`
against commit `eda9e6d516bf331fb048f945072471bcc85b3228` at
2026-08-25T11:19:37Z, conforming to `VER-ADS-001`. It changes the workflow
machine contract, result rendering, preflight manifests, diagnostics, the
installer, and the CLI, and it changes six distributed managed surfaces while
adding a seventh: the router template, `docs/engineering/WORKFLOW.json` and
`WORKFLOW.md`, the pull-request template seed, the managed CI workflow,
`scripts/select_harness_work_order.py`, and the new managed
`docs/engineering/OPERATING_CARD.md`.

`WO-ADS-002`, "Close the reading manifest, minimise the operating card, and
retire the repository-context file", is `implemented` as of 2026-08-25T11:54:14Z
and verified by `VREC-ADS-002` against commit
`459b04d3830804a29047be38e2572537befb8a1f` at 2026-08-25T11:56:41Z, conforming to
`VER-ADS-002`. It brings the operating card inside its 1024-byte bound, closes
the preflight reading manifest, retires this repository's owner-facing
repository-context document, and supersedes `REQ-IAR-020`. The release-build,
release-binding, and last-mile publication sequences that document carried now
live once, in `docs/notes/developing-se-harness.md#release-sequences`.

That retirement is enforced by an exact allow-list: `WO-ADS-002`'s suite asserts
which files may name the retired path, and no file in this release packet is on
it. This packet therefore describes the retirement in prose and never writes the
path. Repairing a mention would require editing `tests/`, which is outside
`WO-RLS-011`'s execution scope.

Two limitations are disclosed rather than implied clean by `gates`, and this
contract carries them:

- `VER-ADS-001`'s **Scenario 8** was not run. That scenario requires independent
  reviewers to read the rendered router scope paragraph and classify four cases —
  an unconstrained repository review, a transition inside an answer, a finding
  labelled as formal, and a question about a work order — and its pass criteria
  require zero misclassifications. Those reviewer classifications do not exist.
  The assurance owner verified `VREC-ADS-001` with that gap accepted, so the
  operator-comprehension condition of `VER-ADS-001` is accepted residual risk on
  this release, not a satisfied condition. This is the same class of gap as
  `VER-TCM-001`'s two missing reviewer judgments.
- Both records were verified with the hosted Linux figure pending the
  pull-request lane. The ADS pull-request lanes have since reported `success`,
  but at `aa042f05` and `d952cd3d`, which are descendants of the bound candidates
  `eda9e6d` and `459b04d` rather than those commits themselves. `VREC-SEH-013`
  must record which of these the candidate's own dual-platform run resolves and
  which remain residual risk.

`VREC-ADS-001` also records accepted deviations — a third corrective kind
`response`, the router scope section placed after the invariants without a second
`HRN-003` occurrence, the manifest prefix still listing routed policies, and
`W-ADS-001` and `W-ADS-002` reported as blockers rather than as a warning tier —
and `VREC-ADS-002` records four more, including the card header dropping one
sentence to fit the byte bound. Those are recorded decisions, not open items, and
they are named here so `VREC-SEH-013` does not restate this coverage as
unqualified.

## Two classification calls the release owner should confirm or revise

Both are carried unchanged from `REL-SEH-015` and are stated because measurement
does not settle them; classification is an accountable decision. The release
owner confirmed neither explicitly when approving `REL-SEH-015`, and they are
therefore re-put here rather than treated as settled by that approval.

- `WO-HUP-004` is **included**. It replaced version-specific predecessor CI
  with portable governor succession. It changed no distributed byte
  (`scripts/validate_governor_transition.py` and one workflow only), so it
  could be read as repository maintenance. It is included because the
  succession mechanism is the machinery that proves a released evaluator can
  govern its successor's root, and the 0.7.0 release decision relies on it.
- `WO-HBI-003` and `WO-HBI-004` are **included**, and on a corrected basis. They
  change distributed bytes — `tests/test_hash_bound_integrity.py` and
  `tests/test_agentic_execution.py`, both shipped in the source distribution — as
  set out above, so the ordinary rule includes them. The secondary argument
  `REL-SEH-015` gave, that the release orchestrator qualifies the candidate
  inside a `git worktree` that inherits their `.gitattributes` rules and so they
  determine which bytes Windows qualification reads, also holds and is retained.

## Baseline and exclusions

The previous public release baseline is immutable annotated tag `v0.6.0`, whose
tag object is `03cae3d30ea1e3933a92c9e87683b0144f8ccc77` and whose released
candidate commit is `3b339e9fc70cc634e6dc6bda07ea6a9b1a465798`, released by
`RLS-SEH-012` under `REL-SEH-011`. This contract was drafted over `main` commit
`e98b7885b016529aa2c262ad577acdc270bc9376`, tree
`fc190614ee06b7ceda0ac931d08af503d7dc5286`. The branch touches only
`docs/engineering/release-0-7-0/`, which is the same subtree `REL-SEH-015`
occupies.

None of the thirty-seven selected historical work orders exists in the `v0.6.0`
tree, and none is named by any released `RLS-SEH-*` record. Both figures were
re-measured for the two additions specifically: neither `WO-RLO-006` nor
`WO-REB-023` and none of their requirements, evidence, or verification records
appears anywhere in the `v0.6.0` tree, and neither appears in the
`releases_work` union of the released records.

The following are explicitly excluded from `releases_work`:

- `WO-HUP-002`, which adopted exact public 0.6.0 as this repository's standard
  root evaluator. It changed this repository's own root, not the distributed
  harness, and is the same class as `WO-HUP-001`, which `REL-SEH-007` excluded
  by name;
- `WO-AEX-006`, `WO-AEX-007`, and `WO-AEX-008`, which must proceed sequentially
  after `WO-AEX-005` and which the owner decided on 2026-08-25 to ship 0.7.0
  without. This exclusion is a **branch-point boundary**, not a claim that the
  work is unstarted: `WO-AEX-007` and `WO-AEX-008` are approved and not started,
  but `WO-AEX-006` already reads `implemented` on open pull request #155, which
  was re-confirmed open at head `61c6880` while this contract was drafted. The
  exclusion holds for as long as the candidate commit's history does not contain
  those bytes. If pull request #155 is merged and the candidate is taken from a
  state that includes it, the packaged surface would carry bytes no gate in this
  contract names, and the remedy is rejection and re-issue as `REL-SEH-017` — not
  a silent widening. The exposure is not only additive: measured on pull request
  #155, `WO-AEX-006` adds `se_harness/effect_broker.py`,
  `se_harness/change_bundle.py`, and `se_harness/effect_contract.json`, and it also
  **modifies** `se_harness/agent_contract.py`, `se_harness/mutation_guard.py`,
  `se_harness/runtime_state.py`, and `pyproject.toml`. Two of those modules are
  `WO-AEX-005` bytes already inside this unit's packaged surface, so merging #155
  into the candidate's history would change bytes this contract gates as well as
  adding bytes it does not. `VREC-SEH-013` must confirm at the candidate that the
  tree contains none of them;
- pull request #156, the governed `RISK` artifact proposal, re-confirmed open at
  head `598a50c` while this contract was drafted. It is excluded on the same
  branch-point terms and on the same condition: the exclusion holds only while
  the candidate's history excludes its bytes;
- `docs/notes/agentic-execution-plugin-distribution.md`, a non-authoritative
  exploration note the owner decided on 2026-08-25 needs no artifact or work
  order. It carries no work-order trailer, changes no managed file, formal
  artifact, or lifecycle state, and creates no release-bearing payload;
- the roadmap, which is outside every work order by standing repository rule and
  whose commits carry no work-order trailer;
- merge-only commits, VREC preparation and transition commits, supersession
  bookkeeping, contract rejection commits, and derived publication
  observations; and
- every other implemented work order not named in this contract.

Repository-governance, RCA, and note documents may remain in the source tree
and source distribution without converting their work orders into
release-bearing payload.

## Required evidence

### Entry criteria

- The selected historical work orders are active, `implemented`, retain
  work-order-keyed evidence, and hold verified assurance coverage. All
  thirty-seven named above are measured as satisfying this at the drafting
  commit, with zero uncovered members, and must be re-measured immediately
  before this contract's approval.
- `WO-RLO-006` is `implemented` and holds verified assurance coverage. Met by
  `VREC-RLO-006`, verified 2026-08-26T08:06:11Z.
- `WO-REB-023` is `implemented` and holds verified assurance coverage. Met by
  `VREC-REB-020`, verified 2026-08-26T07:58:28Z.
- `WO-TCM-001` holds verified assurance coverage. Met by `VREC-TCM-002`,
  verified 2026-08-25T10:51:11Z, subject to the accepted limitation stated
  above. The limitation is disclosed, not resolved.
- `WO-AEX-005` is `implemented` and holds verified assurance coverage. Met by
  `VREC-AEX-005`, verified 2026-08-25T10:39:01Z.
- `WO-ADS-001` and `WO-ADS-002` are `implemented` and hold verified assurance
  coverage. Met by `VREC-ADS-001`, verified 2026-08-25T11:19:37Z, and
  `VREC-ADS-002`, verified 2026-08-25T11:56:41Z, both subject to the disclosed
  limitations stated above. Those limitations are disclosed, not resolved.
- No selected historical work order is named by an existing released RLS.
- No stale `ready` verification or release record exists in the graph. Measured
  at the drafting commit: the only `ready` records are the two canonical
  templates, `VREC-000` and `RLS-000`.
- `REL-SEH-015` is rejected before this contract is approved, so the graph never
  holds two approved release contracts for one release.
- `WO-RLS-011`'s approval stands and its stale exact-candidate reading is
  disclosed above rather than corrected in place.
- This contract is reviewed and approved by the release owner before a promotable
  build, the candidate commit, and release preparation. **Not yet met.** The owner
  approved earlier units three times, as `REL-SEH-013` at 2026-08-25T11:38:12Z, as
  `REL-SEH-014` at 2026-08-25T11:53:28Z, and as `REL-SEH-015` at
  2026-08-25T12:57:58Z; all three contracts are rejected and none of those
  approvals is reused as authority here. This contract requires its own.
- The allow-list is re-measured against the graph immediately before this
  contract's approval, and every work order that reached `implemented` after this
  file was written is reported to the release owner and either added to `gates` or
  excluded by name.
- Formal validation, released-evaluator `doctor`, managed-root integrity, and
  start preflight pass without structure, governance, or policy errors.

### Measured readiness at drafting

Each figure below was measured over `main` at
`e98b7885b016529aa2c262ad577acdc270bc9376`, tree
`fc190614ee06b7ceda0ac931d08af503d7dc5286`, before this packet was committed.
None is a claim about a later candidate, and every figure must be re-measured
against the candidate itself and again immediately before this contract's
approval.

- Exact public 0.6.0 evaluator outside the checkout, in isolated mode: `doctor`
  87 `PASS`, 0 `FAIL`, exit 0; `validate` `PASS`, 891 artifacts, 0 errors, 50
  maintenance-plane warnings, and every plane at E0. Adding this contract takes
  the count to 892.
- `scripts/validate_release_distributions.py`: `PASS`, one distribution-bearing
  record.
- Local Windows suite: 1021 tests, `OK`, 23 platform-guard skips, exit 0. Run
  twice — once at `e98b788` before this packet existed and once over this
  packet's own state — with an identical verdict and identical counts both
  times, which is how this packet is known to break nothing. The count moved
  from the 1002 `REL-SEH-015` measured because `WO-RLO-006` and `WO-REB-023`
  added nineteen tests between them. This is a Windows figure; the hosted Linux
  lane runs the same suite without the platform-guard skips, so the skip count
  is not a coverage gap and must not be quoted as one.
- `WO-ADS-002`'s retired-path allow-list test, the hash-bound integrity tests,
  and the instruction-architecture tests were additionally run as a targeted
  group over this packet: 143 tests, `OK`, 1 skip.
- Review-phase preflight for `WO-RLS-011`: `PASS`. `check` at the `pre-action`
  checkpoint under `PROC-WO-PREPARE-VREC` reports `Completed` with both changed
  paths accepted, confirming they lie inside `WO-RLS-011`'s declared
  `docs/engineering/release-0-7-0/` execution scope.
- `inspect`: 891 artifacts, 3251 relations, formal validation `PASS`, 169
  findings at error 0 / warning 64 / info 105, 0 decisions required, 0
  definitions pending, and 1 assurance pending. The single assurance-pending
  item is `WO-RLS-011`, which is expected: it is the work order `VREC-SEH-013`
  will cover, and it resolves when that record is verified.
- Re-measured over this packet's own state, with `REL-SEH-015` rejected and this
  contract added: `validate` `PASS` at 892 artifacts, 0 errors, 50
  maintenance-plane warnings, every plane at E0; `doctor` 87 `PASS`, 0 `FAIL`;
  release-distribution validation `PASS`; `inspect` 892 artifacts, 3289
  relations, 0 decisions required, 1 assurance pending, and **1 definition
  pending**. That one pending definition is this contract while it is `draft`;
  it resolves to zero on approval, exactly as it did for `REL-SEH-015`. It is
  recorded so that a reader does not mistake it for an unrelated gap.
- Hosted lanes at `e98b788` on `main`: Engineering Harness (run 32946962510),
  SE Harness Candidate Evidence (32946962546), Governor Transition Assessment
  (32946962515), and Publication Rehearsal (32946962531) all `success`, all on
  the `push` event. All nine candidate-evidence jobs pass, including
  `Governance migration` on both Windows and Linux and the reconcile job that
  `WO-REB-023` repaired; `Publication Rehearsal` passes its Windows and Linux
  rehearsals and the divergence refusal, which is the first hosted green reading
  of `WO-RLO-006`'s repair. These are `push`-event readings; the `pull_request`
  lane is a separate observation and the candidate's own dual-platform run is
  where it is resolved.
- One trap this packet had to clear, recorded so it is not reintroduced:
  `WO-ADS-002`'s suite asserts an exact allow-list of files permitted to name the
  retired repository-context path, and no release-packet file is on it. This
  contract therefore names that path nowhere.

### Exact aggregate verification

**Every figure in this section is measured over the whole `gates` array, all
thirty-eight entries including `WO-RLS-011` itself.** That basis is stated
explicitly because a union taken over only the thirty-seven historical members is
a different number, and mixing the two bases is how an aggregate record comes to
disagree with its own contract. On the historical-only basis the same measurement
gives thirty-seven work orders, twenty verification contracts, forty-seven
requirements, and forty keyed evidence paths; those are not the figures
`VREC-SEH-013` must match.

`VREC-SEH-013` must bind one clean 0.7.0 candidate commit to exactly the
thirty-eight work orders named in `gates`, to twenty-one verification contracts
(`VER-ADS-001`, `VER-ADS-002`, `VER-AEX-001`, `VER-AEX-002`, `VER-AEX-003`,
`VER-AEX-004`, `VER-HBI-001`, `VER-HUP-004`, `VER-IPK-001`, `VER-LRE-001`,
`VER-REB-006`, `VER-REB-007`, `VER-REB-008`, `VER-REB-009`, `VER-REB-010`,
`VER-RLO-004`, `VER-RLO-005`, `VER-TCM-001`, `VER-VSP-002`, `VER-WEX-003`, and
`VER-DST-001`), and to forty-one work-order-keyed evidence paths.

The union of requirements those thirty-eight work orders implement is
forty-eight.

Against `REL-SEH-015`'s frozen figures, admitting `WO-RLO-006` and `WO-REB-023`
moved the work-order count from thirty-six to thirty-eight and the keyed
evidence paths from thirty-seven to forty-one, and moved neither the
verification-contract count nor the requirement union, for the measured reasons
given above. The four added paths are:

- `docs/engineering/release-orchestration/evidence/WO-RLO-006-implementation.md`
- `docs/engineering/release-orchestration/evidence/WO-RLO-006-verification.md`
- `docs/engineering/released-evaluator-boundary/evidence/WO-REB-023-migration-scenario-successor.md`
- `docs/engineering/released-evaluator-boundary/evidence/WO-REB-023-verification.md`

Three counting rules apply and were measured, not assumed. The combined evidence
file `technical-communication/evidence/WO-TCM-001/WO-TCM-002-verification.md` is
keyed by directory position to both `WO-TCM-001` and `WO-TCM-002` and is counted
once. `WO-HBI-004` and `WO-RLO-005` each retain two keyed evidence files, and so
do both additions, which is why thirty-seven historical members hold forty
existing paths. Paths are keyed either by an enclosing directory named for the
work order or by a file name beginning with the work-order identifier; both
forms occur in this unit and both were counted.

### Candidate and distribution evidence

- Exact candidate commit, tree, `SOURCE_DATE_EPOCH`, and clean-worktree proof.
- Recipe-bound reproducible build through
  `repository_tools.release_build replay` from the candidate's own
  `release/build-recipe.json` and `release/build-toolchain.lock`, with
  byte-for-byte equality across two fresh producer instances. The recipe names
  a `linux/amd64` producer image by digest, so this evidence can only be
  produced on a host with a working container runtime; `WO-RLS-011`'s disclosure
  that no workstation-measured digest is bindable stands until that build runs.
- Wheel, sdist, checksum, source-manifest, and bundle-manifest identities.
- Dual-runtime candidate package acceptance.
- Hosted run, job, and artifact identities for every required lane, on the
  candidate's own commit rather than on an ancestor or descendant.
- Read-only `release-candidate-replay` dispatch evidence for the bound ready
  record before the release decision.
- Proof that historical candidates, VRECs, RLS records, contracts, rejected
  history, evidence, root managed files, maintenance state, and external policy
  remain unchanged. `VREC-TCM-002` binds `f7b69d0`, `VREC-RLO-006` binds
  `c8b3693`, and `VREC-REB-020` binds `0ea54d1`; all three reached `main`
  through true merges and all three must remain reachable from the candidate.

## Compatibility and migration

- This is the first **ordinary** release of this repository: the root lock is
  schema 3 at exact public 0.6.0, and the released 0.6.0 evaluator validates
  the complete current graph without error. No predecessor-bootstrap contract,
  no derived compatibility view, and no expected-red managed lane apply. This
  contract therefore declares no `[bootstrap]` table, unlike `REL-SEH-011`.
- The ready record must use distribution schema 2. `RLS-SEH-012` bound schema
  1; a new ready record cannot, because
  `repository_tools/release_distribution.py` permits schema 1 only on records
  that are already `released`. That rule arrived with `WO-RLO-004`, which is
  itself in this release unit, so 0.7.0 is the first release obliged to satisfy
  a constraint it ships. `RLS-SEH-013` is therefore the first recipe-bound
  release record, and the strict recipe interpreter is used for both
  pre-release replay and publication.
- The published 0.7.0 is a minor version. It adds the `qualify` and `migrate`
  command namespaces, declared hash-bound text classes, declared interpreter
  and entry-point safety, legacy release-evidence exemptions, the agent and
  skill contracts, the managed technical-communication policy, and five
  repository-installed skills. Existing installed repositories are not changed
  by publication; they change only through a separately approved
  `harnessctl upgrade --apply`.
- The managed technical-communication policy is a new managed file that adopting
  repositories receive on upgrade, and the managed router template gains one
  routing row for it. Both are managed-surface additions that an upgrade plan
  must show before any apply.
- The managed work-order template gains an optional `[agentic_delegation]`
  table and its guidance paragraph, and the distributed managed validator gains
  the rules that check it. This is a third managed-surface addition an upgrade
  plan must show. The table is optional and declarative: it records a maximum
  delegation, starts no work, and grants no standing authority. Nothing in
  0.7.0 consumes it at runtime.
- `docs/engineering/OPERATING_CARD.md` is a fourth new managed file, added by
  `WO-ADS-001` and bounded to 1024 bytes by `WO-ADS-002`. Adopting repositories
  receive it on upgrade, and an upgrade plan must show it before any apply.
- `WO-ADS-001` and `WO-ADS-002` also change six distributed managed surfaces that
  already exist in adopting repositories: the router template, both workflow
  policy files, the pull-request template seed, the managed CI workflow, and the
  managed work-order selection script. An upgrade plan must show each of those
  changes, and an adopting repository that customized any of them will be blocked
  rather than partially written, as the managed upgrade rules require.
- `WO-RLO-006` and `WO-REB-023` change no distributed managed surface and no
  runtime module. Their distributed bytes are three test modules in the source
  distribution. Adopting repositories are unaffected by them on upgrade, and the
  release notes should not describe either as a user-facing change.
- The retirement of this repository's owner-facing repository-context document is
  a change to this repository's own instruction surface, not to a distributed
  managed file. Adopting repositories are unaffected by it.
- Exact public 0.6.0 predates the `qualify` namespace, so the independent
  package lane retains its documented `accept-candidate` bootstrap exception
  for this release. Removing that path after 0.7.0 is published is a later
  governed change and is out of scope here.
- The root remains schema 3 at 0.6.0 through preparation and publication.
  Adopting 0.7.0 as this repository's root evaluator requires independently
  published bytes and a separate approved upgrade work order.

## Security and provenance

- Treat Git state, paths, sparse state, workflow context, logs, artifacts,
  evaluator bytes, commands, JSON, hashes, locks, recipes, and environments as
  untrusted input.
- Require exact agreement among the candidate commit, the governance commit,
  the evaluator identity, the root lock, this contract, the work set,
  `VREC-SEH-013`, `RLS-SEH-013`, the bound recipe and distribution evidence,
  the two builds, and every hosted observation.
- The producer image is pinned by digest in `release/build-recipe.json` and the
  build toolchain is pinned by hash in `release/build-toolchain.lock`. Neither
  may be relaxed to make a build succeed on a host that cannot run the pinned
  producer; a host without a working container runtime is a reason to move the
  build, not to change the recipe.
- Only verified inert bytes may cross into credential-bearing jobs. The
  protected `pypi` environment remains a separate human decision.
- Stop before any write or credential use on ambiguity, contamination, drift,
  partial output, unsafe cleanup, or provenance disagreement.

## Promotion policy

1. Done on 2026-08-25: `REL-SEH-012`, `REL-SEH-013`, `REL-SEH-014`,
   `WO-RLS-009`, and `WO-RLS-010` were rejected across four successions as the
   unit changed, and `REL-SEH-015` was approved at 2026-08-25T12:57:58Z on the
   thirty-six-work-order unit. `WO-RLS-011` was approved at 2026-08-25T12:35:00Z
   and reached `implemented` at 2026-08-25T18:43:37Z.
2. Done on 2026-08-25 and 2026-08-26: `WO-RLO-006` and `WO-REB-023` repaired the
   publication rehearsal's junction teardown and the governance migration lane's
   successor mismatch, reached `implemented`, were verified by `VREC-RLO-006` and
   `VREC-REB-020`, and reached `main` through the true merges of pull requests
   #167 and #168. Their distributed bytes triggered `REL-SEH-015`'s declared stop
   condition.
3. Next: the release owner rejects `REL-SEH-015` and approves this contract on
   the re-measured thirty-eight-work-order unit. Neither act is taken by the
   other, and this contract's approval must be its own recorded decision.
4. Next: obtain a working container runtime for the pinned `linux/amd64`
   producer, then build the recipe-bound distributions outside the checkout
   under this contract's authority. `gates` is frozen from approval, so any work
   order that reaches `implemented` with bytes in the packaged surface during
   this step is a stop condition reported to the release owner, not an edit.
5. Separately authorize one clean candidate commit and a dedicated candidate
   branch push. Before that commit, confirm the tree carries no `WO-AEX-006`
   bytes and no pull request #156 bytes, since either may merge into `main` in
   the meantime.
6. Require green hosted Engineering Harness, Candidate Evidence, Governor
   Transition Assessment, and Publication Rehearsal lanes on the candidate's own
   commit. No expected-red lane is anticipated; any red is a stop condition, not
   an accepted boundary.
7. Separately prepare, review, and verify `VREC-SEH-013` with exactly the
   work-order set, keyed evidence paths, and verification contracts this
   contract names at its approval, measured on the whole-`gates` basis, and
   carrying the disclosures this contract requires, including `WO-RLS-011`'s
   superseded qualification reading.
8. Separately authorize `RLS-SEH-013` preparation and schema-2 distribution
   binding, dispatch the read-only recipe replay, and have the release owner
   release or reject it.
9. Separately authorize the tag, GitHub and PyPI publication, Pages
   deployment, `release/0.7` maintenance reconciliation, and any later root
   adoption.

Automation creates observations and proposals only. No expected or passing
result exercises accountable authority.

## Human approval triggers

Requirements, technical, security, assurance, engineering, and release owners
decide the artifacts they own. Taken so far and recorded in the affected
artifacts' own lifecycle events: `WO-TCM-001`'s admission and completion,
`VREC-TCM-002`'s verification, the rejections of `REL-SEH-012`, `REL-SEH-013`,
`REL-SEH-014`, `WO-RLS-009`, and `WO-RLS-010`, the succession and ship-now
decisions, the approvals of `REL-SEH-013`, `REL-SEH-014`, `WO-RLS-011`, and
`REL-SEH-015`, `WO-RLO-006`'s and `WO-REB-023`'s admission and completion, and
`VREC-RLO-006`'s and `VREC-REB-020`'s verification.

Taken on 2026-08-26 and recorded here because they shape this file rather than a
single artifact's lifecycle: the decision to reject `REL-SEH-015` and issue this
contract gating thirty-eight work orders rather than ship from an earlier
candidate; the decision to fold `WO-RLS-011`'s re-qualification into
`VREC-SEH-013` rather than issue a successor work order; and the decision to
obtain a container runtime for the pinned producer rather than relax the recipe,
release under schema 1, or add a hosted producer lane.

**This contract's approval has not been taken.** It requires the release owner's
own decision on this contract's own terms. `REL-SEH-015`'s rejection is a
separate decision and does not carry it, and none of the three earlier approvals
is reused as authority.

Outstanding beyond that: `REL-SEH-015`'s rejection, work start, the promotable
build, the candidate commit, branch and credential use, `VREC-SEH-013`
preparation and verification, `RLS-SEH-013` preparation and release, tag
creation, publication, deployment, maintenance-line mutation, external policy
change, and root adoption.

## Known open questions that do not block this release

- `VER-TCM-001`'s two independent reviewer judgments are owed and are accepted
  residual risk on this release, as stated above. Recording them is later
  governed work requiring a successor verification record.
- `VER-ADS-001`'s Scenario 8 reviewer classifications are owed on the same terms
  and are accepted residual risk, as stated above. Two of the three human
  assessment obligations in this release unit are therefore unmet and disclosed,
  and approving this contract accepts that disposition afresh rather than
  inheriting `REL-SEH-015`'s acceptance of it.
- Both ADS records were verified with the hosted Linux figure pending. The
  candidate's own dual-platform run is the place that resolves it, and
  `VREC-SEH-013` must record what it resolves and what remains.
- Eleven gated work orders, `WO-REB-008` through `WO-REB-018`, declare no
  `[execution_scope]` table. That predates the convention rather than violating
  it, and it was re-measured on the thirty-eight-entry basis rather than carried
  forward: the eleven are the same eleven, and neither addition is among them.
  It remains a data-quality observation for later governed correction.
- The byte-exact surface guard derives its inventory from the declared
  `.gitattributes` patterns, so a concurrently developed change that adds a
  byte-exact assertion on an undeclared extension would not be seen by it. This
  is a known blindness in the guard, not a defect in this unit, and it is stated
  so that a green guard reading is not over-read.
- The formal artifact snapshot digest is computed over the checkout's own
  artifact set and is sensitive to the checkout's directory basename, its clone
  depth, and `HEAD`. Snapshot digests recorded in different records are
  therefore not comparable across checkouts, and `VREC-SEH-013` must measure its
  own rather than compare to another record's.
- Issue #142 asks whether `build_recipe_sha256` should leave
  `unbound_digest_fields` and become a declared hash-bound class. It is open
  and deliberately unmeasured. The recipe's bytes are currently guarded by a
  versioned `.gitattributes` rule and `ByteExactSurfaceTests`, both of which
  this release carries. Answering the question is not in this release unit.
- The `RCA RC-060-*` issue series records 0.6.0 release-process learning.
  Those issues remain open and are not gated by this contract.
- Whether plugin distribution should replace the repository-installed skill
  surface is recorded as an exploration note only. Its own accepted decision
  defers plugin distribution until the repository-scoped path is proven, so it
  is outside this release unit.
- `WO-RLO-005` carries no `[[lifecycle_events]]` entries while reading
  `implemented`. It holds keyed evidence and verified coverage through
  `VREC-RLO-005`, so its membership is measured rather than inferred, but the
  missing history is a data-quality observation for later governed correction.

## Rollback criteria and procedure

Once this contract is `approved`, a newly implemented work order whose bytes are
in the packaged surface is a **stop condition**, and the only remedy is rejecting
this contract and issuing `REL-SEH-017` with the re-measured unit. There is no
in-place correction to `gates`. `REL-SEH-015` is the worked precedent: it froze
thirty-six gates, two work orders landed distributed test bytes within eighteen
hours, and it was rejected rather than widened. Two live instances are known —
`WO-AEX-006` on open pull request #155 and the `RISK` artifact proposal on open
pull request #156 — and the exclusions above hold only while the candidate's
history excludes their bytes.

Before publication, stop on incomplete authority, a work order whose bytes are in
the packaged surface and which is either unnamed by this contract or without
verified coverage, more than one active version claim, arbitrary or nonexact
omission, historical or root drift, evaluator mismatch, candidate contamination,
nondeterminism, hosted mismatch, unsafe cleanup or archive handling, evidence
disagreement, or any failed required gate. Remove only exact temporary and
uncommitted outputs after path and digest verification; never rewrite history.
Correct through another governed candidate if trusted candidate state changes.

After publication, never move `v0.7.0` and never replace immutable files.
Preserve the facts, block unsafe adoption, and prepare a separately governed
corrective release.

## Post-release observation window

After separately authorized publication, verify the immutable tag and assets,
PyPI hashes and attestations, a fresh Python 3.11 installation, Windows and LF
evidence stability, candidate identity, `init` and `adopt`, `doctor`,
`validate`, `inspect`, `dashboard`, the five installed skills, the managed
technical-communication policy and its router row, the optional work-order
delegation table and its validator rules, the new managed operating card and its
1024-byte bound, the enforced failure rendering and restitution digest, the
`qualify` and `migrate` namespaces, Pages provenance, the `release/0.7`
maintenance state, and later root-upgrade readiness.
