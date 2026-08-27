+++
id = "REL-SEH-014"
type = "release_contract"
title = "Release se-harness 0.7.0 as the first ordinary schema-3 release"
status = "rejected"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-25"
updated = "2026-08-25"

rejected_at = "2026-08-25T12:34:51Z"
rejected_by = "release-owner"
rejection_reason = "Rejected by the accountable release owner on 2026-08-25, atomically with WO-RLS-010, and superseded by REL-SEH-015. This contract's approved allow-list stopped describing the release forty-six seconds after it was fixed: WO-ADS-002 reached implemented at 2026-08-25T11:54:14Z and, with WO-ADS-001 implemented at 11:15:03Z, both reached main through the true merges of pull requests #152 and #153 at 701e456. Both change se_harness runtime modules and distributed managed templates, so both belong in the 0.7.0 release unit, and an approved allow-list is never widened or repaired in place. This is the third staleness event in this release, after REL-SEH-012 and REL-SEH-013, and it was the fastest. Shown the measured cost of a fourth succession, the owner decided to break the cycle: REL-SEH-015 carries the measured thirty-six-gate unit and is deliberately held in draft until immediately before the candidate commit, so a further landing costs one in-place edit instead of another rejection pair. WO-RLS-011 replaces WO-RLS-010 with its aggregate census deferred to whatever REL-SEH-015 names at its approval, so its approved prose cannot go stale either. Measured immediately before this transition over merged branch state 5acccdebac50f1fe2bbeca9774c9ad110bac6c91 carrying main 701e456: thirty-five historical members all implemented with verified coverage and zero uncovered; twenty-one verification contracts, a forty-eight-requirement union and thirty-seven keyed evidence paths on the whole-gates basis; validate PASS at 887 artifacts with 0 errors and 50 maintenance warnings; doctor 87 PASS, 0 FAIL. This rejection is terminal and rewrites nothing: the approval recorded at 2026-08-25T11:53:28Z stands as history. No work was started under this contract: no start preflight, no version move, no build, no candidate commit, no tag, no publication."
[relations]
gates = ["WO-REB-008", "WO-REB-009", "WO-REB-010", "WO-REB-011", "WO-REB-012", "WO-REB-013", "WO-REB-014", "WO-REB-015", "WO-REB-016", "WO-REB-017", "WO-REB-018", "WO-REB-019", "WO-REB-020", "WO-REB-021", "WO-REB-022", "WO-HUP-004", "WO-HBI-001", "WO-HBI-002", "WO-HBI-003", "WO-HBI-004", "WO-AEX-001", "WO-AEX-002", "WO-AEX-003", "WO-AEX-004", "WO-AEX-005", "WO-VSP-007", "WO-LRE-001", "WO-IPK-001", "WO-RLO-004", "WO-RLO-005", "WO-WEX-003", "WO-TCM-001", "WO-TCM-002", "WO-RLS-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T11:53:28Z"
decided_by = "release-owner"
reason = "Approved by the accountable release owner on 2026-08-25, in the same decision that approved WO-RLS-010. This contract succeeds REL-SEH-013 and carries the identical release unit with WO-RLS-010 substituted for the rejected WO-RLS-009. The owner approved that unit once already, as REL-SEH-013 at 2026-08-25T11:38:12Z, but that contract is rejected and its approval is expressly not reused as authority here; the owner was asked again and approved this contract on its own terms. Approval fixes the release unit as an explicit allow-list of exactly 34 work orders: the 33 release-bearing work orders measured after the v0.6.0 baseline plus WO-RLS-010. It fixes 19 verification contracts, a 41-requirement union, and 35 keyed evidence paths, being the 34 existing paths measured now plus the one WO-RLS-010 will retain. Every figure was re-derived from the graph immediately before this transition rather than inherited: gates holds 34 unique entries ending in WO-RLS-010, all 33 historical members read implemented and hold verified VREC coverage with zero uncovered members, every table cell matched measured coverage, and the governing exact public 0.6.0 evaluator outside the checkout reports validate PASS at 866 artifacts, 0 errors, 50 pre-existing maintenance warnings, every plane at E0, with doctor 87 PASS, 0 FAIL, exit 0 at main commit 73b7b5437637bc2ac2d9af2c8c9295b4d4475d68. Two disclosures are accepted by this approval and stated in the contract rather than implied by gates. First, WO-TCM-001 holds verified coverage through VREC-TCM-002 that is not a claim of conformance to VER-TCM-001 manual-assessment conditions; the two reviewer judgments do not exist and are accepted residual risk. Second, WO-AEX-005 ships four runtime modules unreachable from cli.py and inert in 0.7.0, so release notes must not describe delegated execution as available. This approval authorizes no version bump, build, candidate commit, tag, publication, deployment, or credential use."

[[lifecycle_events]]
from = "approved"
to = "rejected"
decided_at = "2026-08-25T12:34:51Z"
decided_by = "release-owner"
reason = "Rejected by the accountable release owner on 2026-08-25, atomically with WO-RLS-010, and superseded by REL-SEH-015. This contract's approved allow-list stopped describing the release forty-six seconds after it was fixed: WO-ADS-002 reached implemented at 2026-08-25T11:54:14Z and, with WO-ADS-001 implemented at 11:15:03Z, both reached main through the true merges of pull requests #152 and #153 at 701e456. Both change se_harness runtime modules and distributed managed templates, so both belong in the 0.7.0 release unit, and an approved allow-list is never widened or repaired in place. This is the third staleness event in this release, after REL-SEH-012 and REL-SEH-013, and it was the fastest. Shown the measured cost of a fourth succession, the owner decided to break the cycle: REL-SEH-015 carries the measured thirty-six-gate unit and is deliberately held in draft until immediately before the candidate commit, so a further landing costs one in-place edit instead of another rejection pair. WO-RLS-011 replaces WO-RLS-010 with its aggregate census deferred to whatever REL-SEH-015 names at its approval, so its approved prose cannot go stale either. Measured immediately before this transition over merged branch state 5acccdebac50f1fe2bbeca9774c9ad110bac6c91 carrying main 701e456: thirty-five historical members all implemented with verified coverage and zero uncovered; twenty-one verification contracts, a forty-eight-requirement union and thirty-seven keyed evidence paths on the whole-gates basis; validate PASS at 887 artifacts with 0 errors and 50 maintenance warnings; doctor 87 PASS, 0 FAIL. This rejection is terminal and rewrites nothing: the approval recorded at 2026-08-25T11:53:28Z stands as history. No work was started under this contract: no start preflight, no version move, no build, no candidate commit, no tag, no publication."
+++

# Release Contract: Release se-harness 0.7.0 as the first ordinary schema-3 release

## Lifecycle and authority

This contract requires the release owner's approval before start preflight,
versioning, code or documentation edits, or a promotable build. Its authoritative
state, and the timestamp and reason of every decision taken on it, are the front
matter and `[[lifecycle_events]]` above; read those rather than this prose. It is
the third contract issued for this release and the successor to `REL-SEH-013`.

On 2026-08-25 the repository owner instructed `objective is to make the 0.7.0
release, you can start the release process`, then `additional content landed on
main, can you refresh, and integrate the newly implemented work orders`. Those
instructions authorize deriving the ledger against current `main` and drafting
this packet for accountable review. They authorize nothing else.

On 2026-08-25 the owner approved `REL-SEH-012` and `WO-RLS-009`, added
`docs/engineering/README.md` to the release work order's execution scope,
admitted `WO-TCM-001` to the release unit, and authorized its transition to
`implemented`, which the engineering owner applied at 2026-08-25T10:21:06Z.

On 2026-08-25 the owner then accepted `VREC-TCM-002` and authorized its
transition to `verified`, its governance commits, a branch push, and a pull
request. The assurance owner applied the verified transition at
2026-08-25T10:51:11Z, and the owner merged pull request #151 into `main` as a
true merge at `73b7b5437637bc2ac2d9af2c8c9295b4d4475d68`.

On 2026-08-25, resuming release work, the owner chose from measured options to
reject `REL-SEH-012` and issue a successor rather than amend an approved
allow-list in place, and to ship 0.7.0 now rather than wait for `WO-AEX-006`
through `WO-AEX-008`. The release owner rejected `REL-SEH-012`, `REL-SEH-013`
was drafted with the thirty-four-work-order unit, and the owner approved it at
2026-08-25T11:38:12Z with `I approve REL-SEH-013`.

That approval did not answer `WO-RLS-009`'s amended aggregate scope, which had
been put in the same decision. Asked how to re-approve it, and shown that the
governing exact public 0.6.0 evaluator refuses an `approved` to `approved`
transition (`WEX201`), the owner chose to reject `WO-RLS-009` and issue
`WO-RLS-010`. Because `REL-SEH-013` named `WO-RLS-009` in `gates`, that choice
left an approved allow-list naming a rejected member, and an approved contract is
not widened or repaired in place. The release owner therefore rejected
`WO-RLS-009` and `REL-SEH-013` in one atomic transaction at
2026-08-25T11:47:44Z, and this contract succeeds `REL-SEH-013` with `WO-RLS-010`
substituted for `WO-RLS-009` in `gates`.

`REL-SEH-012`, `REL-SEH-013`, and `WO-RLS-009` are all preserved as immutable
rejected history. None of their recorded lifecycle events was rewritten. No work
was started under any of them: no start preflight was run, no version identity
was moved, no distribution was built, and no candidate commit exists.

Approving this contract will not authorize the candidate commit, `VREC-SEH-013`
or `RLS-SEH-013` preparation or transition, the governance commit carrying this
packet, branch push, credential use, tag creation, GitHub or PyPI publication,
Pages deployment, maintenance-line mutation, external policy change, or
root-evaluator upgrade. `WO-RLS-010`'s approval is a separate decision and is
not carried by approving this contract.

## Why this contract supersedes `REL-SEH-013` and `REL-SEH-012`

`REL-SEH-012` was approved at 2026-08-25T10:28:10Z naming a thirty-three-gate
allow-list. `WO-AEX-005` reached `implemented` at 2026-08-25T10:29:40Z, ninety
seconds later, and `VREC-AEX-005` verified it at 2026-08-25T10:39:01Z. Its
authorized bytes are inside the 0.7.0 packaged surface, so that approved
allow-list stopped describing the release unit almost immediately after it was
fixed. `REL-SEH-013` carried the corrected thirty-four-gate unit and was
approved, then had to be retired in turn because its final member, `WO-RLS-009`,
was rejected so that its unapproved scope amendment could be re-issued cleanly
as `WO-RLS-010`.

An allow-list contract cannot be silently widened, nor repaired, after the
approval that fixed it. The 0.6.0 history is the governing precedent:
`REL-SEH-008`, `REL-SEH-009`, and `REL-SEH-010` were each rejected and re-issued
as that unit changed from nine to twelve to thirteen to fourteen gates under
`REL-SEH-011`, and no approved contract was ever amended in place.

This contract carries the same thirty-four-work-order unit as `REL-SEH-013`,
with `WO-RLS-010` in place of `WO-RLS-009`. The thirty-three historical members,
the nineteen verification contracts, the forty-one-requirement union, the
thirty-five keyed evidence paths, the baseline, the exclusions, the two
classification calls, and both disclosures are unchanged, and every figure was
re-measured against the graph rather than inherited.

## Release unit

One incremental `se-harness` 0.7.0 release derived from one clean candidate
commit: a recipe-bound reproducible wheel, a normalized source distribution, a
checksum manifest, a schema-2 bound distribution table, an immutable `v0.7.0`
tag, GitHub Release assets, publication of the same qualified files to PyPI,
the canonical `release/0.7` maintenance line, and a release-bound static
Explorer demonstration.

The historical release-bearing work added after the immutable `v0.6.0` baseline
is exactly these thirty-three work orders. Every row was measured as active,
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
| `WO-WEX-003` | Implement semantic-fidelity lifecycle handoffs | `VREC-WEX-006` |
| `WO-TCM-001` | Implement managed technical communication and the operator-brief skill | `VREC-TCM-002`, with a disclosed limitation stated below |
| `WO-TCM-002` | Align router contract tests with the managed technical-communication route | `VREC-TCM-001` |

`WO-RLS-010` adds the 0.7.0 versioning, integrated qualification,
reproducibility, exact-candidate evidence, and aggregate-VREC preparation
needed to form the final thirty-four-work-order release unit.

This contract is an explicit allow-list. It is not an inference from dates,
branches, merge order, lifecycle status, or every commit after the baseline.

## `WO-TCM-001`: covered, with an accepted limitation the release must carry

`REL-SEH-012` left one entry criterion open: `WO-TCM-001` held no verified
assurance coverage. That criterion is now met, by Route 1 of the two routes that
contract named. The assurance owner captured `VREC-TCM-002` against candidate
commit `f7b69d0ad40321caa0520f9fed137be8e32bcf1f`, where `WO-TCM-001` reads
`implemented`, and verified it at 2026-08-25T10:51:11Z.

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
unqualified.

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

Phase 4 is explicitly sequential. `WO-AEX-006`, `WO-AEX-007`, and `WO-AEX-008`
are approved and not started. They are excluded from this unit and are not
blocked by this release.

`WO-AEX-005` resolved a declared test-contract conflict rather than waiving it:
a legacy test had required the candidate and released work-order templates to be
byte-identical. The amended test now reconstructs the candidate template from
the unchanged released root template plus the exact declared delegation table
and guidance paragraph, and separately proves the released template carries no
delegation table. The released root copy was not edited, which the root managed
integrity rules require.

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
`RLS-SEH-012` under `REL-SEH-011`. This contract was drafted from clean `main`
commit `73b7b5437637bc2ac2d9af2c8c9295b4d4475d68`, tree
`4497eb9c94eef17ff8a214c46dafa8a8c4fdfbfc`.

None of the thirty-three selected work orders exists in the `v0.6.0` tree, and
none is named by any released `RLS-SEH-*` record. The union of work released by
the seven released records is sixty-one work orders and was measured as having
an empty intersection with this allow-list.

The following are explicitly excluded from `releases_work`:

- `WO-HUP-002`, which adopted exact public 0.6.0 as this repository's standard
  root evaluator. It changed this repository's own root, not the distributed
  harness, and is the same class as `WO-HUP-001`, which `REL-SEH-007` excluded
  by name;
- `WO-AEX-006`, `WO-AEX-007`, and `WO-AEX-008`, which are approved, not started,
  and must proceed sequentially after `WO-AEX-005`;
- `docs/notes/agentic-execution-plugin-distribution.md`, a non-authoritative
  exploration note the owner decided on 2026-08-25 needs no artifact or work
  order. It carries no work-order trailer, changes no managed file, formal
  artifact, or lifecycle state, and creates no release-bearing payload;
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
  thirty-three named above are measured as satisfying this at the drafting
  commit.
- `WO-TCM-001` holds verified assurance coverage. Met by `VREC-TCM-002`,
  verified 2026-08-25T10:51:11Z, subject to the accepted limitation stated
  above. The limitation is disclosed, not resolved.
- `WO-AEX-005` is `implemented` and holds verified assurance coverage. Met by
  `VREC-AEX-005`, verified 2026-08-25T10:39:01Z.
- No selected historical work order is named by an existing released RLS.
- No stale `ready` verification or release record exists in the graph. Measured
  at the drafting commit: the only `ready` records are the two canonical
  templates.
- This contract and `WO-RLS-010` are separately reviewed and approved before
  start preflight, versioning, code or documentation edits, or a promotable
  build. This criterion is satisfied only by the approval events recorded in
  this contract's and `WO-RLS-010`'s own front matter, which are authoritative
  over this paragraph. The owner approved the identical thirty-four-work-order
  unit as `REL-SEH-013` at 2026-08-25T11:38:12Z, but that contract is rejected
  and its approval is not reused as authority here; `WO-RLS-010`'s scope had
  never been approved in any form before this packet. Until both approval events
  exist, this is the one open entry criterion and it blocks start preflight.
- Formal validation, released-evaluator `doctor`, managed-root integrity, and
  start preflight pass without structure, governance, or policy errors.

### Measured readiness at the drafting commit

Each figure is a measurement of `73b7b5437637bc2ac2d9af2c8c9295b4d4475d68`, not
a claim about a later candidate. Every figure must be re-measured against the
candidate.

- Exact public 0.6.0 evaluator outside the checkout, in isolated mode: `doctor`
  87 `PASS`, 0 `FAIL`, exit 0; `validate` `PASS`, 0 errors, 50 maintenance-plane
  warnings, and every plane at E0. The artifact count is 861 for the committed
  tree alone, measured in a throwaway worktree at the same commit, and 864 with
  this draft packet present in the working tree: `REL-SEH-012`, `REL-SEH-014`,
  and `WO-RLS-010`.
- `scripts/validate_release_distributions.py`: `PASS`, one distribution-bearing
  record.
- Local Windows suite: 954 tests, `OK`, 22 platform-guard skips. The count moved
  from 943 at the predecessor contract's drafting commit because `WO-AEX-005`
  added eleven tests.
- Hosted lanes at `73b7b54` on `main`: Engineering Harness, SE Harness Candidate
  Evidence, Governor Transition Assessment, and Publication Rehearsal all
  `success`.
- No pending assurance item at that commit: `inspect` reports assurance pending
  as empty, and the only active work is `WO-RLS-010`.

### Exact aggregate verification

`VREC-SEH-013` must bind one clean 0.7.0 candidate commit to exactly the
thirty-four work orders named in `gates`, to nineteen verification contracts
(`VER-AEX-001`, `VER-AEX-002`, `VER-AEX-003`, `VER-AEX-004`, `VER-HBI-001`,
`VER-HUP-004`, `VER-IPK-001`, `VER-LRE-001`, `VER-REB-006`, `VER-REB-007`,
`VER-REB-008`, `VER-REB-009`, `VER-REB-010`, `VER-RLO-004`, `VER-RLO-005`,
`VER-TCM-001`, `VER-VSP-002`, `VER-WEX-003`, and `VER-DST-001`), and to
thirty-five work-order-keyed evidence paths: the thirty-four existing paths
measured at the drafting commit plus the one `WO-RLS-010` retains.

The union of requirements those work orders implement is forty-one. Admitting
`WO-AEX-005` raised the work-order count from thirty-three to thirty-four, the
requirement union from forty to forty-one by adding `REQ-AEX-010`, the
verification-contract count from eighteen to nineteen by adding `VER-AEX-004`,
and the existing keyed-evidence-path count from thirty-three to thirty-four by
adding
`docs/engineering/agentic-execution/evidence/WO-AEX-005-verification.md`.
`WO-AEX-005`'s other two declared requirements, `REQ-AEX-002` and `REQ-AEX-004`,
were already in the union through `WO-AEX-001` through `WO-AEX-004`, and
`VER-AEX-001` was already among the contracts.

`VREC-SEH-013` is `WO-TCM-001`'s second verified coverage, not its first.

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
  remain unchanged. `VREC-TCM-002` binds `f7b69d0`, which reached `main` through
  a true merge; that commit must remain reachable.

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
- The managed work-order template gains an optional `[agentic_delegation]`
  table and its guidance paragraph, and the distributed managed validator gains
  the rules that check it. This is a third managed-surface addition an upgrade
  plan must show. The table is optional and declarative: it records a maximum
  delegation, starts no work, and grants no standing authority. Nothing in
  0.7.0 consumes it at runtime.
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

1. Done on 2026-08-25: the owner admitted `WO-TCM-001`, the engineering owner
   transitioned it to `implemented`, the assurance owner verified
   `VREC-TCM-002` with its limitation disclosed, and the owner merged pull
   request #151 into `main` as a true merge.
2. Done on 2026-08-25: the release owner rejected `REL-SEH-012`, `REL-SEH-013`
   carried the thirty-four-gate unit and was approved and then rejected together
   with `WO-RLS-009`, and this contract and `WO-RLS-010` were issued as their
   successors.
3. Approve this contract and `WO-RLS-010` as separate accountable decisions,
   recorded in their own lifecycle events, then commit this packet under an
   authorized governance commit. The packet is uncommitted working-tree state
   until that commit is separately authorized.
4. Run start preflight, then implement only `WO-RLS-010`: move candidate
   version identity to 0.7.0, requalify locally, build the recipe-bound
   distributions outside the checkout, and retain complete evidence.
5. Separately authorize one clean candidate commit and a dedicated candidate
   branch push.
6. Require green hosted Engineering Harness, Candidate Evidence, Governor
   Transition Assessment, and Publication Rehearsal lanes. No expected-red lane
   is anticipated; any red is a stop condition, not an accepted boundary.
7. Separately transition `WO-RLS-010` to `implemented` in its own governance
   commit after complete local and hosted evidence.
8. Separately prepare, review, and verify `VREC-SEH-013` with exactly the
   thirty-four-work-order set, thirty-five keyed evidence paths, and nineteen
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
decide the artifacts they own. Taken so far: `WO-TCM-001`'s admission and
completion, `VREC-TCM-002`'s verification, `REL-SEH-012`'s rejection, and the
succession and ship-now decisions, `REL-SEH-013`'s approval, and the rejection
of `REL-SEH-013` and `WO-RLS-009`. This contract's approval and `WO-RLS-010`'s
approval are recorded in their own lifecycle events if taken. Outstanding beyond
those: the governance commit carrying this packet,
work start, the candidate commit, branch and credential use, work-order
completion, `VREC-SEH-013` preparation and verification, `RLS-SEH-013`
preparation and release, tag creation, publication, deployment,
maintenance-line mutation, external policy change, and root adoption.

## Known open questions that do not block this release

- `VER-TCM-001`'s two independent reviewer judgments are owed and are accepted
  residual risk on this release, as stated above. Recording them is later
  governed work requiring a successor verification record.
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
technical-communication policy and its router row, the optional work-order
delegation table and its validator rules, the `qualify` and `migrate`
namespaces, Pages provenance, the `release/0.7` maintenance state, and later
root-upgrade readiness.
