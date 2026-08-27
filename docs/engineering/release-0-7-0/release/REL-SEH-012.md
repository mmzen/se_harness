+++
id = "REL-SEH-012"
type = "release_contract"
title = "Release se-harness 0.7.0 as the first ordinary schema-3 release"
status = "rejected"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-25"
updated = "2026-08-25"

rejected_at = "2026-08-25T11:18:09Z"
rejected_by = "release-owner"
rejection_reason = "The accountable repository owner resumed release work on 2026-08-25 after merging PR #151 and chose, from measured options, to reject this contract and issue successor REL-SEH-013 rather than amend this approved contract in place. WO-AEX-005 reached implemented at 2026-08-25T10:29:40Z and was verified by VREC-AEX-005 at 10:39:01Z, ninety seconds after this contract was approved at 10:28:10Z. Its authorized bytes are inside the 0.7.0 packaged surface: four se_harness runtime modules, the optional agentic_delegation table in the distributed managed work-order template, and 147 lines of distributed managed validator. This contract is an explicit allow-list of thirty-three gates, so it no longer describes the release unit, and an allow-list cannot be silently widened after the approval that fixed it. This follows the 0.6.0 precedent, where REL-SEH-008, REL-SEH-009 and REL-SEH-010 were each rejected and re-issued as the unit changed and no approved contract was ever amended in place. REL-SEH-013 preserves this contract as immutable history and carries the thirty-four-gate unit. The owner also decided to ship 0.7.0 now rather than wait for WO-AEX-006 through WO-AEX-008, accepting that WO-AEX-005 four Python modules are unreachable from cli.py and stay inert until those work orders land. Rejecting this contract exercises no release, build, tag, publication, or deployment authority, and REL-SEH-013 requires its own separate approval decision."
[relations]
gates = ["WO-REB-008", "WO-REB-009", "WO-REB-010", "WO-REB-011", "WO-REB-012", "WO-REB-013", "WO-REB-014", "WO-REB-015", "WO-REB-016", "WO-REB-017", "WO-REB-018", "WO-REB-019", "WO-REB-020", "WO-REB-021", "WO-REB-022", "WO-HUP-004", "WO-HBI-001", "WO-HBI-002", "WO-HBI-003", "WO-HBI-004", "WO-AEX-001", "WO-AEX-002", "WO-AEX-003", "WO-AEX-004", "WO-VSP-007", "WO-LRE-001", "WO-IPK-001", "WO-RLO-004", "WO-RLO-005", "WO-WEX-003", "WO-TCM-001", "WO-TCM-002", "WO-RLS-009"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T10:28:10Z"
decided_by = "release-owner"
reason = "On 2026-08-25 the accountable repository owner stated: I approve: REL-SEH-012 and WO-RLS-009, the docs/engineering/README.md should be added to the scope. For WO-TCM-001 i accept it, you can transition it to implemented. That decision approves this release contract, admits WO-TCM-001 to the thirty-three-work-order release unit, and authorizes WO-TCM-001's transition to implemented, which the engineering owner applied at 2026-08-25T10:21:06Z. One entry criterion remains open by design: no verification record covers WO-TCM-001, and the assurance owner must close that gap before VREC-SEH-013 is prepared. This approval grants no authority to commit, push, build, tag, publish, deploy, prepare or transition VREC-SEH-013 or RLS-SEH-013, mutate the maintenance line, use credentials, change external policy, or upgrade the root evaluator."

[[lifecycle_events]]
from = "approved"
to = "rejected"
decided_at = "2026-08-25T11:18:09Z"
decided_by = "release-owner"
reason = "The accountable repository owner resumed release work on 2026-08-25 after merging PR #151 and chose, from measured options, to reject this contract and issue successor REL-SEH-013 rather than amend this approved contract in place. WO-AEX-005 reached implemented at 2026-08-25T10:29:40Z and was verified by VREC-AEX-005 at 10:39:01Z, ninety seconds after this contract was approved at 10:28:10Z. Its authorized bytes are inside the 0.7.0 packaged surface: four se_harness runtime modules, the optional agentic_delegation table in the distributed managed work-order template, and 147 lines of distributed managed validator. This contract is an explicit allow-list of thirty-three gates, so it no longer describes the release unit, and an allow-list cannot be silently widened after the approval that fixed it. This follows the 0.6.0 precedent, where REL-SEH-008, REL-SEH-009 and REL-SEH-010 were each rejected and re-issued as the unit changed and no approved contract was ever amended in place. REL-SEH-013 preserves this contract as immutable history and carries the thirty-four-gate unit. The owner also decided to ship 0.7.0 now rather than wait for WO-AEX-006 through WO-AEX-008, accepting that WO-AEX-005 four Python modules are unreachable from cli.py and stay inert until those work orders land. Rejecting this contract exercises no release, build, tag, publication, or deployment authority, and REL-SEH-013 requires its own separate approval decision."
+++

# Release Contract: Release se-harness 0.7.0 as the first ordinary schema-3 release

## Lifecycle and authority

On 2026-08-25, after reviewing the `v0.6.0`-to-`main` ledger, the measured
release-bearing allow-list, the exclusions, and the readiness state, the
repository owner instructed `objective is to make the 0.7.0 release, you can
start the release process`. That instruction authorizes creation and completion
of this draft contract and draft `WO-RLS-009` for accountable review. It
authorizes nothing else.

Later on 2026-08-25 the owner instructed `additional content landed on main, can
you refresh, and integrate the newly implemented work orders`. That instruction
authorizes re-derivation of the ledger against the current `main` and revision of
these two drafts. It grants no further authority and takes no lifecycle
decision.

On 2026-08-25, after reviewing the completed packet, the accountable owner stated
`I approve: REL-SEH-012 and WO-RLS-009, the docs/engineering/README.md should be
added to the scope. For WO-TCM-001 i accept it, you can transition it to
implemented`. That decision approves this contract, adds
`docs/engineering/README.md` to `WO-RLS-009`'s execution scope, admits
`WO-TCM-001` to the release unit, and authorizes its `in_progress` to
`implemented` transition. `WO-TCM-001` was transitioned on
2026-08-25T10:21:06Z by the engineering owner. This contract moved `draft` to
`approved` at 2026-08-25T10:28:10Z under the release owner, and `WO-RLS-009` in
the same packet under the engineering owner.

The approval explicitly does not authorize the candidate commit, `VREC-SEH-013`
or `RLS-SEH-013` preparation or transition, a verification record for
`WO-TCM-001`, branch push, credential use, tag creation, GitHub or PyPI
publication, Pages deployment, maintenance-line mutation, external policy
change, or root-evaluator upgrade.

## Release unit

One incremental `se-harness` 0.7.0 release derived from one clean candidate
commit: a recipe-bound reproducible wheel, a normalized source distribution, a
checksum manifest, a schema-2 bound distribution table, an immutable `v0.7.0`
tag, GitHub Release assets, publication of the same qualified files to PyPI,
the canonical `release/0.7` maintenance line, and a release-bound static
Explorer demonstration.

The historical release-bearing work added after the immutable `v0.6.0` baseline
is exactly these thirty-two work orders. Every row was measured as active,
`implemented`, holding work-order-keyed evidence, absent from the `v0.6.0` tree,
and unnamed by any released release record. Thirty-one also hold verified
assurance coverage; `WO-TCM-001` does not yet, which the row below states and the
required-evidence section governs.

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
| `WO-HUP-004` | Replace version-specific predecessor CI with portable governor succession | `VREC-HUP-004`, `VREC-HUP-005` |
| `WO-HBI-001` | Declare hash-bound text classes and assess their completeness in `doctor` | `VREC-HBI-001` |
| `WO-HBI-002` | Take every hash mode from the declared class and fix the lock's divergence | `VREC-HBI-002` |
| `WO-HBI-003` | Declare a byte rule for the byte-exact surfaces no recorded digest binds | `VREC-HBI-003` |
| `WO-HBI-004` | Declare byte-exact surfaces by tree and derive the guard's inventory from the tracked set | `VREC-HBI-004` |
| `WO-AEX-001` | Implement the read-only `harness-orient` pilot | `VREC-AEX-001` |
| `WO-AEX-002` | Implement runtime-neutral AEX core contract validation | `VREC-AEX-002` |
| `WO-AEX-003` | Implement the single-agent outcome skills MVP | `VREC-AEX-003` |
| `WO-AEX-004` | Install repository-scoped Codex and Claude skill surfaces | `VREC-AEX-004` |
| `WO-VSP-007` | Align prepared VREC supersession with lifecycle validation | `VREC-VSP-002` |
| `WO-LRE-001` | Implement declared legacy release-evidence exemptions and the pre-apply upgrade refusal | `VREC-LRE-001` |
| `WO-IPK-001` | Implement the qualified integration-package lane | `VREC-IPK-001` |
| `WO-RLO-004` | Implement recipe-bound release build replay | `VREC-RLO-004` |
| `WO-RLO-005` | Rehearse the credential-free last mile on both runner platforms | `VREC-RLO-005` |
| `WO-WEX-003` | Implement semantic-fidelity lifecycle handoffs | `VREC-WEX-006` |
| `WO-TCM-001` | Implement managed technical communication and the operator-brief skill | **none yet** |
| `WO-TCM-002` | Align router contract tests with the managed technical-communication route | `VREC-TCM-001` |

`WO-RLS-009` adds the 0.7.0 versioning, integrated qualification,
reproducibility, exact-candidate evidence, and aggregate-VREC preparation
needed to form the final thirty-three-work-order release unit.

This contract is an explicit allow-list. It is not an inference from dates,
branches, merge order, lifecycle status, or every commit after the baseline.

## `WO-TCM-001`: admitted, and its outstanding assurance

`WO-TCM-001`, "Implement managed technical communication and the operator-brief
skill", was `in_progress` and uncovered when this contract was first drafted. The
owner has since accepted it into the release unit and authorized its transition to
`implemented`, which the engineering owner applied on 2026-08-25T10:21:06Z. It is
named in `gates` above.

It mattered, and still matters, because its authorized bytes are already on
`main` and inside the 0.7.0 packaged surface:
`se_harness/skill_contract.py`, `se_harness/preflight.py`, `pyproject.toml`, the
new managed policy document
`templates/repository/standard/docs/engineering/TECHNICAL_COMMUNICATION.md`, the
managed router template, and the whole
`templates/repository/standard/.agents/skills/harness-operator-brief/` skill.
Publishing 0.7.0 without `WO-TCM-001` in the unit would have shipped a
behavioral change that no release record attributes. Admitting it fixes that.

What admitting it does **not** fix is assurance. No verification record covers
`WO-TCM-001`. `VREC-TCM-001` names only `WO-TCM-002`. `WO-TCM-001` holds keyed
evidence at
`docs/engineering/technical-communication/evidence/WO-TCM-001/WO-TCM-002-verification.md`,
which the directory-position attribution rule keys to both TCM work orders, so no
new evidence file is required and the keyed-evidence-path count does not change.
Coverage, however, is still an open assurance-owner decision, and one of two
routes must be taken before the release decision:

- **Route 1, recommended.** The assurance owner captures and verifies a
  commit-bound record for `WO-TCM-001` before candidate qualification. This
  matches how every other member of the unit qualified and satisfies the entry
  criterion below verbatim. `capture-verification` requires the work order to be
  `implemented` at the bound commit, so the record must bind a commit at or after
  the transition, not the merged implementation commit `1b94c82`.
- **Route 2.** The aggregate `VREC-SEH-013` becomes `WO-TCM-001`'s first and only
  verified coverage. This satisfies `releases_work` mechanically, because the
  aggregate record would cover it, but it makes one release-preparation record
  the sole assurance for a packaged behavioral change affecting managed policy
  distribution, the managed router, preflight inputs, and the strict portable
  skill contract.

The route is not chosen by approving this contract, and `WO-RLS-009` stops if it
reaches candidate qualification with the question still open.

## Two classification calls the release owner should confirm or revise

Both are stated because measurement does not settle them; classification is an
accountable decision.

- `WO-HUP-004` is **included**. It replaced version-specific predecessor CI
  with portable governor succession. It changed no distributed byte
  (`scripts/validate_governor_transition.py` and one workflow only), so it
  could be read as repository maintenance. It is included because the
  succession mechanism is the machinery that proves a released evaluator can
  govern its successor's root, and the 0.7.0 release decision relies on it.
- `WO-HBI-003` and `WO-HBI-004` are **included**. Both changed only the
  owner-controlled region of `.gitattributes` and the suite's byte-exact guard,
  not a distributed byte. They are included because the release orchestrator
  qualifies the candidate inside a `git worktree` that inherits those rules, so
  they determine which bytes Windows qualification actually reads.

## Baseline and exclusions

The previous public release baseline is immutable annotated tag `v0.6.0`, whose
tag object is `03cae3d30ea1e3933a92c9e87683b0144f8ccc77` and whose released
candidate commit is `3b339e9fc70cc634e6dc6bda07ea6a9b1a465798`, released by
`RLS-SEH-012` under `REL-SEH-011`. This packet was drafted from clean `main`
commit `0276dd750393fa09d9d20dcd270492258982bd48`, tree
`a9160245fdf74e1cfa43c6e2330afc0eb24e3e44`.

None of the thirty-two selected work orders exists in the `v0.6.0` tree, and
none is named by any released `RLS-SEH-*` record. The union of work released by
the seven released records is sixty-one work orders and does not intersect this
allow-list.

The following are explicitly excluded from `releases_work`:

- `WO-HUP-002`, which adopted exact public 0.6.0 as this repository's standard
  root evaluator. It changed this repository's own root, not the distributed
  harness, and is the same class as `WO-HUP-001`, which `REL-SEH-007` excluded
  by name;
- `docs/notes/agentic-execution-plugin-distribution.md`, a non-authoritative
  exploration note the owner decided on 2026-08-25 needs no artifact or work
  order. It carries no work-order trailer, changes no managed file, formal
  artifact, or lifecycle state, and creates no release-bearing payload;
- merge-only commits, VREC preparation and transition commits, supersession
  bookkeeping, and derived publication observations; and
- every other implemented work order not named in this contract.

Repository-governance, RCA, and note documents may remain in the source tree
and source distribution without converting their work orders into
release-bearing payload.

## Required evidence

### Entry criteria

- The selected historical work orders are active, `implemented`, retain
  work-order-keyed evidence, and already hold verified assurance coverage.
  Thirty-one of the thirty-two named above are measured as satisfying this at the
  drafting commit.
- `WO-TCM-001` is `implemented` and named in this contract's allow-list. Met: the
  owner admitted it on 2026-08-25 and the engineering owner applied the
  transition at 2026-08-25T10:21:06Z.
- `WO-TCM-001` holds verified assurance coverage. This criterion is **not met**.
  It is the one open entry criterion, and the section above states the two routes
  that can close it. It must be closed before `VREC-SEH-013` is prepared, because
  the aggregate record's work set is fixed at that point.
- No selected historical work order is named by an existing released RLS.
- No stale `ready` verification or release record exists in the graph. Measured
  at the drafting commit: the only `ready` records are the two canonical
  templates.
- This contract and `WO-RLS-009` are separately reviewed and approved before
  start preflight, versioning, code or documentation edits, or a promotable
  build. Met: both were approved on 2026-08-25T10:28:10Z, this contract by the
  release owner and `WO-RLS-009` by the engineering owner.
- Formal validation, released-evaluator `doctor`, managed-root integrity, and
  start preflight pass without structure, governance, or policy errors.

### Measured readiness at the drafting commit

Each figure is a measurement of `0276dd750393fa09d9d20dcd270492258982bd48`, not
a claim about a later candidate. Every figure must be re-measured against the
candidate.

- Exact public 0.6.0 evaluator outside the checkout, in isolated mode: `doctor`
  87 `PASS`, 0 `FAIL`, exit 0; `validate` `PASS`, 0 errors, 50 maintenance-plane
  warnings, and every plane at E0. The artifact count is 845 for the committed
  tree alone, measured in a throwaway worktree at the same commit, and 847 with
  this draft packet present in the working tree. The candidate validator returns
  the same counts.
- `scripts/validate_release_distributions.py`: `PASS`, one distribution-bearing
  record.
- Local Windows suite: 943 tests, `OK`, 22 platform-guard skips. The count moved
  from 932 at the previous drafting commit because the technical-communication
  work added eleven tests.
- Hosted lanes at `0276dd7` on `main`: Engineering Harness, SE Harness Candidate
  Evidence, Governor Transition Assessment, and Publication Rehearsal all
  `success`.
- One pending lifecycle item at that commit: active work `WO-TCM-001`, then
  `in_progress`. Its authorized transition to `implemented` is a working-tree
  change at the time of writing and is not yet committed, so the committed tree at
  `0276dd7` still reads `in_progress`. Re-measure after the governance commit.

### Exact aggregate verification

`VREC-SEH-013` must bind one clean 0.7.0 candidate commit to exactly the
thirty-three work orders named in `gates`, to eighteen verification contracts
(`VER-AEX-001`, `VER-AEX-002`, `VER-AEX-003`, `VER-HBI-001`, `VER-HUP-004`,
`VER-IPK-001`, `VER-LRE-001`, `VER-REB-006`, `VER-REB-007`, `VER-REB-008`,
`VER-REB-009`, `VER-REB-010`, `VER-RLO-004`, `VER-RLO-005`, `VER-TCM-001`,
`VER-VSP-002`, `VER-WEX-003`, and `VER-DST-001`), and to thirty-four
work-order-keyed evidence paths: the thirty-three existing paths plus the one
`WO-RLS-009` retains.

The union of requirements those work orders implement is forty. Admitting
`WO-TCM-001` raised the work-order count from thirty-two to thirty-three and the
requirement union from thirty-seven to forty, by adding `REQ-TCM-002`,
`REQ-TCM-003`, and `REQ-TCM-004`. It moved neither the verification-contract count
nor the keyed-evidence-path count, because `VER-TCM-001` and the combined TCM
evidence file already serve both TCM work orders: the evidence path
`docs/engineering/technical-communication/evidence/WO-TCM-001/WO-TCM-002-verification.md`
keys to `WO-TCM-001` through its directory component and to `WO-TCM-002` through
its filename.

Whether `VREC-SEH-013` is `WO-TCM-001`'s only verified coverage or its second
depends on the route taken above. Either way `VREC-SEH-013` must name it.

### Candidate and distribution evidence

- Exact candidate commit, tree, `SOURCE_DATE_EPOCH`, and clean-worktree proof.
- Recipe-bound reproducible build through
  `repository_tools.release_build replay` from the candidate's own
  `release/build-recipe.json` and `release/build-toolchain.lock`, with
  byte-for-byte equality across two fresh producer instances.
- Wheel, sdist, checksum, source-manifest, and bundle-manifest identities.
- Dual-runtime candidate package acceptance.
- Hosted run, job, and artifact identities for every required lane.
- Read-only `release-candidate-replay` dispatch evidence for the bound ready
  record before the release decision.
- Proof that historical candidates, VRECs, RLS records, contracts, rejected
  history, evidence, root managed files, maintenance state, and external policy
  remain unchanged.

## Compatibility and migration

- This is the first **ordinary** release of this repository: the root lock is
  schema 3 at exact public 0.6.0, and the released 0.6.0 evaluator validates
  the complete current graph without error. No predecessor-bootstrap contract,
  no derived compatibility view, and no expected-red managed lane apply. This
  contract therefore declares no `[bootstrap]` table, unlike `REL-SEH-011`.
- The ready record must use distribution schema 2. `RLS-SEH-012` bound schema
  1; a new ready record cannot. `RLS-SEH-013` is therefore the first
  recipe-bound release record, and the strict recipe interpreter is used for
  both pre-release replay and publication.
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
- Only verified inert bytes may cross into credential-bearing jobs. The
  protected `pypi` environment remains a separate human decision.
- Stop before any write or credential use on ambiguity, contamination, drift,
  partial output, unsafe cleanup, or provenance disagreement.

## Promotion policy

1. Done on 2026-08-25: the owner approved this contract and `WO-RLS-009`, admitted
   `WO-TCM-001` to the allow-list, and the engineering owner transitioned it to
   `implemented`.
2. Commit `WO-TCM-001`'s lifecycle transition and this approved packet under
   separately authorized governance commits. The transition and the packet are
   working-tree changes until then.
3. Close `WO-TCM-001`'s open assurance criterion by taking Route 1 or Route 2
   above under assurance-owner authority. Route 1 must complete before
   `VREC-SEH-013` preparation; Route 2 is a decision to record, not an action.
4. Run start preflight, then implement only `WO-RLS-009`: move candidate
   version identity to 0.7.0, requalify locally, build the recipe-bound
   distributions outside the checkout, and retain complete evidence.
5. Separately authorize one clean candidate commit and a dedicated candidate
   branch push.
6. Require green hosted Engineering Harness, Candidate Evidence, Governor
   Transition Assessment, and Publication Rehearsal lanes. No expected-red lane
   is anticipated; any red is a stop condition, not an accepted boundary.
7. Separately transition `WO-RLS-009` to `implemented` in its own governance
   commit after complete local and hosted evidence.
8. Separately prepare, review, and verify `VREC-SEH-013` with exactly the
   thirty-three-work-order set, thirty-four keyed evidence paths, and eighteen
   verification contracts named above.
9. Separately authorize `RLS-SEH-013` preparation and schema-2 distribution
   binding, dispatch the read-only recipe replay, and have the release owner
   release or reject it.
10. Separately authorize the tag, GitHub and PyPI publication, Pages
    deployment, `release/0.7` maintenance reconciliation, and any later root
    adoption.

Automation creates observations and proposals only. No expected or passing
result exercises accountable authority.

## Human approval triggers

Requirements, technical, security, assurance, engineering, and release owners
decide the artifacts they own. Two of those decisions are taken: this contract's
and `WO-RLS-009`'s approval, and `WO-TCM-001`'s admission and completion. The
governance commits carrying them, `WO-TCM-001`'s verified coverage, work start,
the candidate commit, branch and credential use, work-order completion,
`VREC-SEH-013` preparation and verification, `RLS-SEH-013` preparation and
release, tag creation, publication, deployment, maintenance-line mutation,
external policy change, and root adoption each remain separate action-time
decisions.

## Known open questions that do not block this release

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

## Rollback criteria and procedure

Before publication, stop on incomplete authority, a work order whose bytes are in
the packaged surface and which is either unnamed by this contract or without
verified coverage, more than one active version claim,
arbitrary or nonexact omission, historical or root drift, evaluator mismatch,
candidate contamination, nondeterminism, hosted mismatch, unsafe cleanup or
archive handling, evidence disagreement, or any failed required gate. Remove
only exact temporary and uncommitted outputs after path and digest verification;
never rewrite history. Correct through another governed candidate if trusted
candidate state changes.

After publication, never move `v0.7.0` and never replace immutable files.
Preserve the facts, block unsafe adoption, and prepare a separately governed
corrective release.

## Post-release observation window

After separately authorized publication, verify the immutable tag and assets,
PyPI hashes and attestations, a fresh Python 3.11 installation, Windows and LF
evidence stability, candidate identity, `init` and `adopt`, `doctor`,
`validate`, `inspect`, `dashboard`, the five installed skills, the managed
technical-communication policy and its router row, the `qualify` and `migrate`
namespaces, Pages provenance, the `release/0.7` maintenance state, and later
root-upgrade readiness.
