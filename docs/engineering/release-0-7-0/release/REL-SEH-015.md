+++
id = "REL-SEH-015"
type = "release_contract"
title = "Release se-harness 0.7.0 as the first ordinary schema-3 release"
status = "approved"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
gates = ["WO-REB-008", "WO-REB-009", "WO-REB-010", "WO-REB-011", "WO-REB-012", "WO-REB-013", "WO-REB-014", "WO-REB-015", "WO-REB-016", "WO-REB-017", "WO-REB-018", "WO-REB-019", "WO-REB-020", "WO-REB-021", "WO-REB-022", "WO-HUP-004", "WO-HBI-001", "WO-HBI-002", "WO-HBI-003", "WO-HBI-004", "WO-AEX-001", "WO-AEX-002", "WO-AEX-003", "WO-AEX-004", "WO-AEX-005", "WO-VSP-007", "WO-LRE-001", "WO-IPK-001", "WO-RLO-004", "WO-RLO-005", "WO-WEX-003", "WO-TCM-001", "WO-TCM-002", "WO-ADS-001", "WO-ADS-002", "WO-RLS-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T12:57:58Z"
decided_by = "release-owner"
reason = "Approved by the accountable release owner on 2026-08-25, freezing the thirty-six-work-order allow-list in gates as the exact 0.7.0 release unit. This approval is taken earlier than the sequencing the owner chose earlier the same day, which was to hold this contract in draft until immediately before the candidate commit; the owner's acceptance supersedes that ordering, and the prose was finalised in the same commit, the last point at which an approved contract can be corrected. Re-measured immediately before this transition over committed branch state 8b4932f51a7be0b9d1d1d0478af46dd7755c59c4 carrying unmoved main 701e456: gates holds thirty-six unique entries, the thirty-five historical members all read implemented with verified coverage and zero uncovered, and on the whole-gates basis it aggregates twenty-one verification contracts, a forty-eight-requirement union and thirty-seven keyed evidence paths, thirty-six existing plus the one WO-RLS-011 retains; the historical-only basis gives twenty and forty-seven and is not the basis VREC-SEH-013 must match. Governing public 0.6.0 evaluator outside the checkout: validate PASS at 887 artifacts, 0 errors, 50 pre-existing maintenance warnings, every plane at E0; doctor 87 PASS, 0 FAIL; release-distribution validation PASS. One fact is disclosed here: WO-AEX-006 is excluded by name yet reads implemented on open pull request #155, so that exclusion is now a branch-point boundary rather than a statement that the work is unstarted, and taking its bytes into the candidate's history would put ungated bytes in the packaged surface and force rejection and re-issue. Three limitations are carried as accepted residual risk and must not be restated as clean: VER-TCM-001's two reviewer judgments, VER-ADS-001's Scenario 8 classifications, and WO-AEX-005's inert scaffolding. This approval gates the promotable build, the candidate commit and release preparation; it authorizes none of them, and nothing has been started under WO-RLS-011."
+++

# Release Contract: Release se-harness 0.7.0 as the first ordinary schema-3 release

## Lifecycle and authority

This contract's approval by the release owner is what permits a promotable build,
the candidate commit, and release preparation. Its authoritative state, and the
timestamp and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above; read those rather than this prose. It is the fourth
contract issued for this release and the successor to `REL-SEH-014`.

**This contract is `approved`, and its `gates` array is therefore fixed
authority.** The release owner approved it at 2026-08-25T12:57:58Z. From that
moment the thirty-six-work-order allow-list below is the exact 0.7.0 release
unit: it cannot be widened, narrowed, or repaired in place, and a work order that
reaches `implemented` with bytes in the packaged surface after that timestamp is a
stop condition whose only remedy is rejecting this contract and issuing
`REL-SEH-016`.

That is a different sequencing from the one the owner chose earlier the same day.
After three approved allow-lists went stale within minutes — `REL-SEH-012` after
ninety seconds, `REL-SEH-013` through its rejected member, `REL-SEH-014` after
forty-six seconds — the owner decided this successor would stay `draft` and be
corrected in place until immediately before the candidate commit, so a further
landing would cost one edit instead of a rejection pair. The owner then accepted
this contract, which supersedes that ordering. The deferral is recorded here
because it explains the shape of this file, not because it is still in force.

Two consequences of approving now, both accepted:

- Every figure below was re-measured immediately before the approving transition
  rather than carried forward from drafting, and `main` was confirmed unmoved at
  `701e456794636e83ff78eb9910df55dfc1eedd9c`. The entry criterion that required
  that re-measurement is met, not waived.
- The window between this approval and the candidate commit is now exposed to the
  same staleness that retired three predecessors. `WO-AEX-006` is the live
  instance: it is excluded from this unit by name and already reads `implemented`
  on open pull request #155. That exclusion is stated below as a branch-point
  boundary, so it survives the work being implemented — but taking those bytes
  into the candidate's history would put ungated bytes in the packaged surface
  and force rejection and re-issue.

Approval does not extend `WO-RLS-011`'s authorized scope. `WO-RLS-011`'s start was
never gated on an approved release contract in the first place: the governing exact
public 0.6.0 workflow contract names `release_contract` only in artifact-type
selectors, and `focus` on the release work order reports start preflight as the
next step with the engineering owner as the required actor. What this approval
gates is the promotable build, the candidate commit, aggregate verification, and
release preparation, and each of those remains a separate later decision that this
approval does not take.

Because this contract is no longer `draft`, keeping `gates` current in place is no
longer available to `WO-RLS-011` and is no longer part of its authorized work. Its
obligation is now to report any work order that reaches `implemented` with bytes in
the packaged surface, as a stop condition, to the release owner.

One consequence is recorded here rather than left implicit. `WO-RLS-011` was
approved at 2026-08-25T12:35:00Z, twenty-three minutes before this contract, and
its approved prose therefore describes this contract as held in `draft` until
immediately before the candidate commit and as edited in place as work lands. Those
sentences were true when that approval was taken and are now stale. They are
narrative about this contract's planned lifecycle, not `WO-RLS-011`'s scope: what
its approval binds is the six declared execution-scope paths and a **deferred**
census, and the deferral resolves to this contract's `gates` — which this approval
has now settled. `WO-RLS-011` is therefore not falsified by this approval and is
not re-issued; the harness has no re-approval transition with which to amend the
stale narrative, and rejecting an otherwise-correct work order over it would cost a
succession for prose. This paragraph is the disclosure. Read `gates` and this
contract's `[[lifecycle_events]]` for the contract's real state, never
`WO-RLS-011`'s prose.

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
2026-08-25T11:47:44Z. `REL-SEH-014` succeeded `REL-SEH-013` with `WO-RLS-010`
substituted for `WO-RLS-009` in `gates`, and the release owner and the
engineering owner approved both in one atomic transition at
2026-08-25T11:53:28Z.

Forty-six seconds after that approval, at 2026-08-25T11:54:14Z, `WO-ADS-002`
reached `implemented`. Together with `WO-ADS-001`, implemented at
2026-08-25T11:15:03Z, it reached `main` through the true merges of pull requests
#152 and #153 at `701e456794636e83ff78eb9910df55dfc1eedd9c`. Both change
`se_harness/` runtime modules and distributed managed templates, so both belong
in the release unit, and `REL-SEH-014`'s approved allow-list stopped describing
the release for the second time in two hours.

Shown that measured cost, the owner decided on 2026-08-25 to break the cycle
instead of paying it a third time: reject `REL-SEH-014` and `WO-RLS-010`, issue
this contract with the measured thirty-six-gate unit, hold it in `draft` until
immediately before the candidate commit, and issue `WO-RLS-011` with its
aggregate census deferred to whatever this contract names at its approval. The
release owner rejected `REL-SEH-014` and `WO-RLS-010` in one atomic transaction,
recorded in those artifacts' own lifecycle events, so the graph never held an
approved contract naming a rejected member. Later the same day the owner accepted
this contract, taking the approval that ordering had deferred; the deferral
therefore shaped this file without ever governing a candidate. `WO-RLS-011`'s
deferred census still holds, because it defers to what this contract names in
`gates` — which is now settled.

`REL-SEH-012`, `REL-SEH-013`, `REL-SEH-014`, `WO-RLS-009`, and `WO-RLS-010` are
all preserved as immutable rejected history. None of their recorded lifecycle
events was rewritten, and the owner's real approval of `REL-SEH-014` and
`WO-RLS-010` at 11:53:28Z stands in the record rather than being erased. No work
was started under any of them: no start preflight was run, no version identity
was moved, no distribution was built, and no candidate commit exists.

This contract's approval did not authorize the candidate commit, `VREC-SEH-013`
or `RLS-SEH-013` preparation or transition, the governance commit carrying this
packet, branch push, credential use, tag creation, GitHub or PyPI publication,
Pages deployment, maintenance-line mutation, external policy change, or
root-evaluator upgrade. `WO-RLS-011`'s approval is a separate decision and is
not carried by this one; it was taken separately, at 2026-08-25T12:35:00Z, and is
recorded in `WO-RLS-011`'s own lifecycle events.

## Why this contract supersedes `REL-SEH-014`, `REL-SEH-013`, and `REL-SEH-012`

Three approved allow-lists went stale, all for the same reason. The pattern is
why this one was drafted to be approved last, and it is the risk this contract
now carries again, deliberately, in the window before the candidate commit.

`REL-SEH-012` was approved at 2026-08-25T10:28:10Z naming a thirty-three-gate
allow-list. `WO-AEX-005` reached `implemented` ninety seconds later, at
2026-08-25T10:29:40Z, and `VREC-AEX-005` verified it at 2026-08-25T10:39:01Z. Its
authorized bytes are inside the 0.7.0 packaged surface, so that approved
allow-list stopped describing the release unit almost immediately after it was
fixed.

`REL-SEH-013` carried the corrected thirty-four-gate unit and was approved at
2026-08-25T11:38:12Z, then had to be retired in turn because its final member,
`WO-RLS-009`, was rejected so that its unapproved scope amendment could be
re-issued cleanly as `WO-RLS-010`.

`REL-SEH-014` carried the same thirty-four-gate unit with `WO-RLS-010`
substituted, and was approved at 2026-08-25T11:53:28Z. `WO-ADS-002` reached
`implemented` forty-six seconds later, at 2026-08-25T11:54:14Z, and with
`WO-ADS-001` it put two more work orders' bytes into the packaged surface. The
third staleness event was therefore faster than the second and the first.

An allow-list contract cannot be silently widened, nor repaired, after the
approval that fixed it. The 0.6.0 history is the governing precedent:
`REL-SEH-008`, `REL-SEH-009`, and `REL-SEH-010` were each rejected and re-issued
as that unit changed from nine to twelve to thirteen to fourteen gates under
`REL-SEH-011`, and no approved contract was ever amended in place.

What changed here is the sequencing, not the rule. This contract carries a
thirty-six-work-order unit: `REL-SEH-014`'s thirty-three historical members plus
`WO-ADS-001` and `WO-ADS-002`, with `WO-RLS-011` in place of `WO-RLS-010`. Every
derived figure was measured over that thirty-six-gate array against the merged
branch state rather than inherited: twenty-one verification contracts, a
forty-eight-requirement union, and thirty-seven keyed evidence paths. The
baseline and the two classification calls are unchanged, and the exclusions are
unchanged in substance with `WO-AEX-006`'s rationale restated as a branch-point
boundary. A third disclosure is added, for `WO-ADS-001` and `WO-ADS-002`.

The rule this contract restores is the strict one. While it was `draft`, a fourth
landing would have cost one in-place edit to this file. Now that it is `approved`,
a fourth landing costs a fifth contract, `REL-SEH-016`, with `WO-RLS-012` beside
it if the work order's approved prose is falsified too — which is precisely why
`WO-RLS-011` fixes no census and names no release contract.

## Release unit

One incremental `se-harness` 0.7.0 release derived from one clean candidate
commit: a recipe-bound reproducible wheel, a normalized source distribution, a
checksum manifest, a schema-2 bound distribution table, an immutable `v0.7.0`
tag, GitHub Release assets, publication of the same qualified files to PyPI,
the canonical `release/0.7` maintenance line, and a release-bound static
Explorer demonstration.

The historical release-bearing work added after the immutable `v0.6.0` baseline
is exactly these thirty-five work orders. Every row was measured as active,
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
| `WO-ADS-001` | Implement enforced failure rendering, shared next-step resolution, the operating card, trap diagnostics, the restitution digest, and router scope | `VREC-ADS-001`, with a disclosed limitation stated below |
| `WO-ADS-002` | Close the reading manifest, minimise the operating card, and retire the repository-context file | `VREC-ADS-002`, with a disclosed limitation stated below |

`WO-RLS-011` adds the 0.7.0 versioning, integrated qualification,
reproducibility, exact-candidate evidence, and aggregate-VREC preparation
needed to form the final thirty-six-work-order release unit.

This contract is an explicit allow-list. It is not an inference from dates,
branches, merge order, lifecycle status, or every commit after the baseline. The
release owner's approval at 2026-08-25T12:57:58Z turned it into fixed authority:
the list was re-measured against the graph immediately before that transition, and
from then on it can only be replaced, not corrected. `WO-RLS-011` is obliged to
report any work order that reaches `implemented` with bytes in the packaged
surface after that timestamp, as a stop condition rather than as an edit.

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

Phase 4 is explicitly sequential and is excluded from this unit. `WO-AEX-007` and
`WO-AEX-008` are approved and not started. `WO-AEX-006` is no longer unstarted:
it reads `implemented` on open pull request #155, "implement transactional effect
broker", measured at that branch's head `61c6880`. It is excluded all the same,
by name, on the owner's 2026-08-25 decision to ship 0.7.0 without waiting for
Phase 4 — but the exclusion now depends on the candidate's history, not on the
work order's lifecycle status, and the release notes must not describe delegated
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
path, and `WO-RLS-011` carries that as a constraint. Repairing a mention would
require editing `tests/`, which is outside `WO-RLS-011`'s execution scope.

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
  `eda9e6d` and `459b04d` rather than those commits themselves. `WO-RLS-011` must
  record which of these the candidate's own dual-platform run resolves and which
  remain residual risk.

`VREC-ADS-001` also records accepted deviations — a third corrective kind
`response`, the router scope section placed after the invariants without a second
`HRN-003` occurrence, the manifest prefix still listing routed policies, and
`W-ADS-001` and `W-ADS-002` reported as blockers rather than as a warning tier —
and `VREC-ADS-002` records four more, including the card header dropping one
sentence to fit the byte bound. Those are recorded decisions, not open items, and
they are named here so `VREC-SEH-013` does not restate this coverage as
unqualified.

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
`RLS-SEH-012` under `REL-SEH-011`. This contract was drafted over `main` commit
`701e456794636e83ff78eb9910df55dfc1eedd9c`, tree
`46d9bf7b5c46c84a732883890d8e5d708bacd2bf`, merged into this packet's governance
branch as `5acccdebac50f1fe2bbeca9774c9ad110bac6c91`, tree
`fc4038b805c5ddce91bec55ac4a47a82bdf0f364`. The merge was a true merge and was
clean: the branch touches only `docs/engineering/release-0-7-0/`, which `main`
does not contain.

None of the thirty-five selected work orders exists in the `v0.6.0` tree, and
none is named by any released `RLS-SEH-*` record. The union of work released by
the seven released records is sixty-one work orders and was measured as having
an empty intersection with this allow-list.

The following are explicitly excluded from `releases_work`:

- `WO-HUP-002`, which adopted exact public 0.6.0 as this repository's standard
  root evaluator. It changed this repository's own root, not the distributed
  harness, and is the same class as `WO-HUP-001`, which `REL-SEH-007` excluded
  by name;
- `WO-AEX-006`, `WO-AEX-007`, and `WO-AEX-008`, which must proceed sequentially
  after `WO-AEX-005` and which the owner decided on 2026-08-25 to ship 0.7.0
  without. This exclusion is a **branch-point boundary**, not a claim that the
  work is unstarted: `WO-AEX-007` and `WO-AEX-008` are approved and not started,
  but `WO-AEX-006` already reads `implemented` on open pull request #155. The
  exclusion holds for as long as the candidate commit's history does not contain
  those bytes. If pull request #155 is merged and the candidate is taken from a
  state that includes it, the packaged surface would carry bytes no gate in this
  contract names, and the remedy is rejection and re-issue as `REL-SEH-016` — not
  a silent widening. The exposure is not only additive: measured on pull request
  #155, `WO-AEX-006` adds `se_harness/effect_broker.py`,
  `se_harness/change_bundle.py`, and `se_harness/effect_contract.json`, and it also
  **modifies** `se_harness/agent_contract.py`, `se_harness/mutation_guard.py`,
  `se_harness/runtime_state.py`, and `pyproject.toml`. Two of those modules are
  `WO-AEX-005` bytes already inside this unit's packaged surface, so merging #155
  into the candidate's history would change bytes this contract gates as well as
  adding bytes it does not. `WO-RLS-011` must confirm at the candidate that the
  tree contains none of them;
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
  thirty-five named above are measured as satisfying this at the drafting commit
  and again immediately before this contract's approval, with zero uncovered
  members both times.
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
  templates.
- `WO-RLS-011` is separately reviewed and approved before start preflight,
  versioning, or code or documentation edits. That criterion is satisfied only by
  the approval event recorded in `WO-RLS-011`'s own front matter, which is
  authoritative over this paragraph.
- This contract is reviewed and approved by the release owner before a promotable
  build, the candidate commit, and release preparation. **Met**: approved at
  2026-08-25T12:57:58Z. The owner had approved an earlier unit twice, as
  `REL-SEH-013` at 2026-08-25T11:38:12Z and as `REL-SEH-014` at
  2026-08-25T11:53:28Z; both contracts are rejected and neither approval is reused
  as authority here. This one was taken on this contract's own terms.
- The allow-list is re-measured against the graph immediately before this
  contract's approval, and every work order that reached `implemented` after this
  file was written is reported to the release owner and either added to `gates` or
  excluded by name. **Met**: the thirty-six-entry array, the thirty-five
  historical members' status and coverage, and all three aggregate figures were
  re-measured immediately before the approving transition; `main` was confirmed
  unmoved at `701e456`. One work order reached `implemented` after this file was
  written — `WO-AEX-006`, on unmerged pull request #155 — and it is reported and
  excluded by name above rather than added.
- Formal validation, released-evaluator `doctor`, managed-root integrity, and
  start preflight pass without structure, governance, or policy errors.

### Measured readiness at approval

Each figure was measured over the governance branch state carrying `main` at
`701e456794636e83ff78eb9910df55dfc1eedd9c`: first at the drafting commit
`5acccdebac50f1fe2bbeca9774c9ad110bac6c91`, then re-measured over the committed
state `8b4932f51a7be0b9d1d1d0478af46dd7755c59c4` immediately before the approving
transition, where every figure was unchanged. None is a claim about a later
candidate, and every figure must be re-measured against the candidate itself.

- Exact public 0.6.0 evaluator outside the checkout, in isolated mode: `doctor`
  87 `PASS`, 0 `FAIL`, exit 0; `validate` `PASS`, 0 errors, 50 maintenance-plane
  warnings, and every plane at E0. The artifact count is 887, which is the 885
  committed before this packet plus the two artifacts it adds, `REL-SEH-015` and
  `WO-RLS-011`.
- `scripts/validate_release_distributions.py`: `PASS`, one distribution-bearing
  record.
- Local Windows suite: 1002 tests, `OK`, 23 platform-guard skips, exit 0, run
  against this packet's final state. The count moved from 954 at
  `REL-SEH-014`'s drafting commit because `WO-ADS-001` and `WO-ADS-002` added
  forty-eight tests and one platform-guarded case. This is a Windows figure; the
  hosted Linux lane runs the same suite without the platform-guard skips.
- One trap this packet had to clear, recorded so it is not reintroduced:
  `WO-ADS-002`'s suite asserts an exact allow-list of files permitted to name the
  retired repository-context path, and no release-packet file is on it. A draft of
  `WO-RLS-011` named the path and turned that test red; the prose was rewritten
  rather than editing `tests/`, which is outside the work order's execution scope.
- Hosted lanes at `701e456` on `main`: Engineering Harness, SE Harness Candidate
  Evidence, Governor Transition Assessment, and Publication Rehearsal all
  `success`, all on the `push` event.
- `inspect`: 887 artifacts, 3235 relations, formal validation `PASS`, 0 decisions
  required, 0 assurance pending, and 0 definitions pending. Definitions pending
  read exactly one while this contract was `draft` and went to zero on its
  approval. Active work is four items: `WO-RLS-011` and the three excluded Phase 4
  work orders `WO-AEX-006` through `WO-AEX-008`, all of which still read `approved`
  in this branch's graph because pull request #155 is unmerged.

### Exact aggregate verification

**Every figure in this section is measured over the whole `gates` array, all
thirty-six entries including `WO-RLS-011` itself.** That basis is stated
explicitly because a union taken over only the thirty-five historical members is
a different number, and mixing the two bases is how an aggregate record comes to
disagree with its own contract. On the historical-only basis the same measurement
gives twenty verification contracts and forty-seven requirements; those are not
the figures `VREC-SEH-013` must match.

`VREC-SEH-013` must bind one clean 0.7.0 candidate commit to exactly the
thirty-six work orders named in `gates`, to twenty-one verification contracts
(`VER-ADS-001`, `VER-ADS-002`, `VER-AEX-001`, `VER-AEX-002`, `VER-AEX-003`,
`VER-AEX-004`, `VER-HBI-001`, `VER-HUP-004`, `VER-IPK-001`, `VER-LRE-001`,
`VER-REB-006`, `VER-REB-007`, `VER-REB-008`, `VER-REB-009`, `VER-REB-010`,
`VER-RLO-004`, `VER-RLO-005`, `VER-TCM-001`, `VER-VSP-002`, `VER-WEX-003`, and
`VER-DST-001`), and to thirty-seven work-order-keyed evidence paths: the
thirty-six existing paths measured at the drafting commit plus the one
`WO-RLS-011` retains.

The union of requirements those thirty-six work orders implement is forty-eight.

Admitting `WO-ADS-001` and `WO-ADS-002` moved every aggregate from
`REL-SEH-014`'s figures: the work-order count from thirty-four to thirty-six, the
verification-contract count from nineteen to twenty-one by adding `VER-ADS-001`
and `VER-ADS-002`, the requirement union from forty-one to forty-eight by adding
`REQ-ADS-001` through `REQ-ADS-007`, and the existing keyed-evidence-path count
from thirty-four to thirty-six by adding
`docs/engineering/agent-directive-surface/evidence/WO-ADS-001/WO-ADS-001-verification.md`
and
`docs/engineering/agent-directive-surface/evidence/WO-ADS-002/WO-ADS-002-verification.md`.
No ADS requirement or verification contract was already in either union.

Two counting rules apply and were measured, not assumed. The combined evidence
file `technical-communication/evidence/WO-TCM-001/WO-TCM-002-verification.md` is
keyed by directory position to both `WO-TCM-001` and `WO-TCM-002` and is counted
once. `WO-HBI-004` and `WO-RLO-005` each retain two keyed evidence files, which
is why thirty-five historical members hold thirty-six existing paths.

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
- `docs/engineering/OPERATING_CARD.md` is a fourth new managed file, added by
  `WO-ADS-001` and bounded to 1024 bytes by `WO-ADS-002`. Adopting repositories
  receive it on upgrade, and an upgrade plan must show it before any apply.
- `WO-ADS-001` and `WO-ADS-002` also change six distributed managed surfaces that
  already exist in adopting repositories: the router template, both workflow
  policy files, the pull-request template seed, the managed CI workflow, and the
  managed work-order selection script. An upgrade plan must show each of those
  changes, and an adopting repository that customized any of them will be blocked
  rather than partially written, as the managed upgrade rules require.
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
- Only verified inert bytes may cross into credential-bearing jobs. The
  protected `pypi` environment remains a separate human decision.
- Stop before any write or credential use on ambiguity, contamination, drift,
  partial output, unsafe cleanup, or provenance disagreement.

## Promotion policy

1. Done on 2026-08-25: the owner admitted `WO-TCM-001`, the engineering owner
   transitioned it to `implemented`, the assurance owner verified
   `VREC-TCM-002` with its limitation disclosed, and the owner merged pull
   request #151 into `main` as a true merge.
2. Done on 2026-08-25: `REL-SEH-012` was rejected; `REL-SEH-013` carried the
   thirty-four-gate unit, was approved, and was rejected together with
   `WO-RLS-009`; `REL-SEH-014` and `WO-RLS-010` succeeded them and were approved
   at 11:53:28Z; `WO-ADS-002` reached `implemented` forty-six seconds later; and
   the release owner rejected `REL-SEH-014` and `WO-RLS-010` in one atomic
   transaction so this contract and `WO-RLS-011` could carry the thirty-six-gate
   unit.
3. Done on 2026-08-25T12:35:00Z: the engineering owner approved `WO-RLS-011`.
4. Done on 2026-08-25: the packet was committed under an authorized governance
   commit as `8b4932f51a7be0b9d1d1d0478af46dd7755c59c4` and pushed to pull request
   #154, with this contract still `draft` at that commit.
5. Done on 2026-08-25T12:57:58Z: the release owner approved this contract on the
   re-measured thirty-six-work-order unit. This step was planned for immediately
   before the candidate commit and was taken here instead, at the owner's
   decision. The allow-list is now fixed: it can no longer be corrected, only
   rejected and re-issued.
6. Run start preflight, then implement only `WO-RLS-011`: move candidate version
   identity to 0.7.0, requalify locally, build the recipe-bound distributions
   outside the checkout, and retain complete evidence. `gates` is frozen, so any
   work order that reaches `implemented` with bytes in the packaged surface during
   this step is a stop condition reported to the release owner, not an edit.
7. Separately authorize one clean candidate commit and a dedicated candidate
   branch push. Before that commit, confirm the tree carries no `WO-AEX-006`
   bytes, since pull request #155 may merge into `main` in the meantime.
8. Require green hosted Engineering Harness, Candidate Evidence, Governor
   Transition Assessment, and Publication Rehearsal lanes. No expected-red lane
   is anticipated; any red is a stop condition, not an accepted boundary.
9. Separately transition `WO-RLS-011` to `implemented` in its own governance
   commit after complete local and hosted evidence.
10. Separately prepare, review, and verify `VREC-SEH-013` with exactly the
    work-order set, keyed evidence paths, and verification contracts this
    contract names at its approval, measured on the whole-`gates` basis.
11. Separately authorize `RLS-SEH-013` preparation and schema-2 distribution
    binding, dispatch the read-only recipe replay, and have the release owner
    release or reject it.
12. Separately authorize the tag, GitHub and PyPI publication, Pages
    deployment, `release/0.7` maintenance reconciliation, and any later root
    adoption.

Automation creates observations and proposals only. No expected or passing
result exercises accountable authority.

## Human approval triggers

Requirements, technical, security, assurance, engineering, and release owners
decide the artifacts they own. Taken so far: `WO-TCM-001`'s admission and
completion, `VREC-TCM-002`'s verification, `REL-SEH-012`'s rejection, the
succession and ship-now decisions, `REL-SEH-013`'s approval, the rejection of
`REL-SEH-013` and `WO-RLS-009`, the approval of `REL-SEH-014` and `WO-RLS-010`,
the decision to hold this contract in `draft` until the candidate rather than
approve and re-issue it, the rejection of `REL-SEH-014` and `WO-RLS-010`,
`WO-RLS-011`'s approval, and this contract's approval. Each is recorded in the
affected artifact's own lifecycle events.

**This contract's approval has been taken.** The release owner approved it at
2026-08-25T12:57:58Z on a freshly re-measured allow-list, earlier than the
deferred-until-the-candidate ordering the owner had chosen the same day. In
approving it the owner also accepted the three disclosed limitations below and the
re-exposure of the window before the candidate commit to the staleness that
retired three predecessor contracts.

Outstanding beyond that: work start,
the candidate commit, branch and credential use, work-order completion,
`VREC-SEH-013` preparation and verification, `RLS-SEH-013` preparation and
release, tag creation, publication, deployment, maintenance-line mutation,
external policy change, and root adoption.

## Known open questions that do not block this release

- `VER-TCM-001`'s two independent reviewer judgments are owed and are accepted
  residual risk on this release, as stated above. Recording them is later
  governed work requiring a successor verification record.
- `VER-ADS-001`'s Scenario 8 reviewer classifications are owed on the same terms
  and are accepted residual risk, as stated above. Two of the three human
  assessment obligations in this release unit are therefore unmet and disclosed.
  The release owner accepted that disposition in approving this contract at
  2026-08-25T12:57:58Z; the obligations remain owed as later governed work.
- Both ADS records were verified with the hosted Linux figure pending. The
  candidate's own dual-platform run is the place that resolves it, and
  `WO-RLS-011` must record what it resolves and what remains.
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

This contract is `approved`, so a newly implemented work order whose bytes are in
the packaged surface is a **stop condition**, and the only remedy is rejecting this
contract and issuing `REL-SEH-016` with the re-measured unit. There is no in-place
correction to `gates`. That is the cost of approving before the candidate commit
rather than immediately before it, and the release owner accepted it. `WO-AEX-006`
on open pull request #155 is the known live instance; the exclusion above holds
only while the candidate's history excludes its bytes.

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
delegation table and its validator rules, the new managed operating card and its
1024-byte bound, the enforced failure rendering and restitution digest, the
`qualify` and `migrate` namespaces, Pages provenance, the `release/0.7`
maintenance state, and later root-upgrade readiness.
