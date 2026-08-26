+++
id = "REL-SEH-017"
type = "release_contract"
title = "Release se-harness 0.7.0 from everything on main as the first ordinary schema-3 release"
status = "draft"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
gates = ["WO-REB-008", "WO-REB-009", "WO-REB-010", "WO-REB-011", "WO-REB-012", "WO-REB-013", "WO-REB-014", "WO-REB-015", "WO-REB-016", "WO-REB-017", "WO-REB-018", "WO-REB-019", "WO-REB-020", "WO-REB-021", "WO-REB-022", "WO-REB-023", "WO-HUP-004", "WO-HBI-001", "WO-HBI-002", "WO-HBI-003", "WO-HBI-004", "WO-AEX-001", "WO-AEX-002", "WO-AEX-003", "WO-AEX-004", "WO-AEX-005", "WO-AEX-006", "WO-AEX-007", "WO-AEX-008", "WO-VSP-007", "WO-LRE-001", "WO-IPK-001", "WO-RLO-004", "WO-RLO-005", "WO-RLO-006", "WO-RLO-007", "WO-WEX-003", "WO-TCM-001", "WO-TCM-002", "WO-ADS-001", "WO-ADS-002", "WO-AUT-001", "WO-AUT-002", "WO-CIP-001", "WO-CIP-002", "WO-CIP-003", "WO-CIP-004", "WO-CIP-005", "WO-TST-001", "WO-TST-002", "WO-TST-003", "WO-RLS-011", "WO-RLS-012"]
+++

# Release Contract: Release se-harness 0.7.0 from everything on main as the first ordinary schema-3 release

## Lifecycle and authority

This contract's approval by the release owner is what permits a promotable build,
the candidate commit, and release preparation. Its authoritative state, and the
timestamp and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above; read those rather than this prose. It is the sixth
contract issued for this release and the successor to `REL-SEH-015`, which the
release owner rejected at 2026-08-26T20:48:50Z under that contract's own stop
condition.

On 2026-08-26 the repository owner instructed: *make the 0.7.0 release. The
previous attempt (materialized by PR #169, that will be closed without being
merged) was a failure. 0.7.0 must contain everything that is currently in main,
and follow the complete release process.* Put three measured options, the owner
decided the same day:

- the release unit is the payload-bearing verified work on `main` — the
  thirty-five historical members `REL-SEH-015` named, the sixteen work orders
  that reached `implemented` with verified coverage since, `WO-RLS-011`, and the
  new release work order `WO-RLS-012` — with governance-only work excluded by
  name-class as every previous contract did;
- the contract keeps the explicit allow-list form, and the commit census from
  `v0.6.0` to `main` is reported as evidence rather than enforced, because the
  history between the two predates the `Harness-Work-Order` trailer that the
  derivation reads (`WO-CIP-004`, deviation 2 accepted);
- `WO-RLS-011` is succeeded by `WO-RLS-012` for the remaining release work.

One part of that third decision could not be applied as put. The owner chose to
reject `WO-RLS-011`, but the governing workflow contract admits only `verified`
or `released` from `implemented` (`WEX201` on the planned transition), and the
work order's candidate `f76da5727e86fc53375bfa5cafcfcbf168c7456e` — the 0.7.0
version bump and its qualification evidence — is on `main` and inside the
packaged surface. `WO-RLS-011` therefore stays `implemented`, is a member of this
unit, and receives its verified coverage from the aggregate record, exactly as
`REL-SEH-015` intended for it. `WO-RLS-012` carries what remains. That is stated
here as a deviation from the owner's decision, not silently absorbed.

Approval of this contract authorizes nothing on its own. It is the precondition
for `WO-RLS-012`'s promotable build, the candidate commit, `VREC-SEH-014`, and
`RLS-SEH-014` preparation; each of those remains a separate later decision.

## Why this contract supersedes `REL-SEH-015` and why `REL-SEH-016` is not reused

`REL-SEH-015` was approved at 2026-08-25T12:57:58Z on a thirty-six-work-order
allow-list and stated that a work order reaching `implemented` with bytes in the
packaged surface after that timestamp is a stop condition whose only remedy is
rejection and re-issue. Sixteen did, all with verified coverage and all on
`main`: `WO-RLO-006`, `WO-REB-023`, the three Phase 4 work orders `WO-AEX-006`
through `WO-AEX-008` that the contract had excluded as a branch-point boundary,
`WO-AUT-001`, `WO-AUT-002`, `WO-CIP-001` through `WO-CIP-005`, `WO-RLO-007`, and
`WO-TST-001` through `WO-TST-003`.

A first successor, `REL-SEH-016`, was issued and approved on the thirty-eight-gate
unit on the branch of pull request #169, where `VREC-SEH-013` was verified and
`RLS-SEH-013` was prepared against a candidate `e98b788`. The owner decided on
2026-08-26 that the attempt had failed and that #169 is closed unmerged. Nothing
from that branch reaches `main`; the identifiers `REL-SEH-016`, `VREC-SEH-013`,
and `RLS-SEH-013` are treated as spent because the identifier space is shared
across branches, and this packet uses `REL-SEH-017`, `VREC-SEH-014`, and
`RLS-SEH-014`. No fact from that branch is carried forward: every figure below
was measured on `main` at `be2f0cfec18b86d273400466cdf1c8c691d92f75`, tree
`fd9bccb5631bef0279ae92c40353b818016cd277`.

`REL-SEH-012` through `REL-SEH-015`, `WO-RLS-009`, and `WO-RLS-010` are preserved
as immutable rejected history; no recorded lifecycle event was rewritten.

## Release unit

One incremental `se-harness` 0.7.0 release derived from one clean candidate
commit cut from `main`: a recipe-bound reproducible wheel, a normalized source
distribution, a checksum manifest, a schema-2 bound distribution table, an
immutable `v0.7.0` tag, GitHub Release assets, publication of the same qualified
files to PyPI, the canonical `release/0.7` maintenance line, and a release-bound
static Explorer demonstration.

The release-bearing work added after the immutable `v0.6.0` baseline is exactly
these fifty-one historical work orders. Every row was measured on `main` at
`be2f0cf` as active, `implemented`, holding work-order-keyed evidence, absent
from the `v0.6.0` tree, unnamed by any released release record, and holding
verified assurance coverage.

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
| `WO-REB-023` | Give the migration rehearsal a scenario whose successor is the current candidate | `VREC-REB-020` |
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
| `WO-AEX-006` | Implement the transactional change-bundle effect broker | `VREC-AEX-006` |
| `WO-AEX-007` | Integrate delegated workflow advancement and assurance preparation | `VREC-AEX-007` |
| `WO-AEX-008` | Integrate Phase 4 execution skills and package qualification | `VREC-AEX-008` |
| `WO-VSP-007` | Align prepared VREC supersession with lifecycle validation | `VREC-VSP-002` |
| `WO-LRE-001` | Implement declared legacy release-evidence exemptions and the pre-apply upgrade refusal | `VREC-LRE-001` |
| `WO-IPK-001` | Implement the qualified integration-package lane | `VREC-IPK-001` |
| `WO-RLO-004` | Implement recipe-bound release build replay | `VREC-RLO-004` |
| `WO-RLO-005` | Rehearse the credential-free last mile on both runner platforms | `VREC-RLO-005` |
| `WO-RLO-006` | Detect junctions without the 3.12 predicates so teardown never follows a link | `VREC-RLO-006` |
| `WO-RLO-007` | Tear down the producer workspace on a hosted runner after a recipe replay | `VREC-RLO-007` |
| `WO-WEX-003` | Implement semantic-fidelity lifecycle handoffs | `VREC-WEX-006` |
| `WO-TCM-001` | Implement managed technical communication and the operator-brief skill | `VREC-TCM-002`, with a disclosed limitation stated below |
| `WO-TCM-002` | Align router contract tests with the managed technical-communication route | `VREC-TCM-001` |
| `WO-ADS-001` | Implement enforced failure rendering, shared next-step resolution, the operating card, trap diagnostics, the restitution digest, and router scope | `VREC-ADS-001`, with a disclosed limitation stated below |
| `WO-ADS-002` | Close the reading manifest, minimise the operating card, and retire the repository-context file | `VREC-ADS-002`, with a disclosed limitation stated below |
| `WO-AUT-001` | Implement the authoring policy, requirement template, statement signals, attributes, and checklist | `VREC-AUT-001` |
| `WO-AUT-002` | Migrate the verification-method vocabulary and add the approval predicates | `VREC-AUT-002` |
| `WO-CIP-001` | Run once per commit and build once per workflow | `VREC-CIP-001` |
| `WO-CIP-002` | One qualification definition for the rehearsal and the release; one Pages job; one schema leg | `VREC-CIP-002` |
| `WO-CIP-003` | Derive the predecessor evaluator facts from the declared governor | `VREC-CIP-003` |
| `WO-CIP-004` | Freeze the release unit by candidate commit and derive its census | `VREC-CIP-004` |
| `WO-CIP-005` | Refuse the approval of a release contract whose census differs from the derivation | `VREC-CIP-005` |
| `WO-TST-001` | The parallel runner and the scale marker | `VREC-TST-001` |
| `WO-TST-002` | The cached fixture install | `VREC-TST-002` |
| `WO-TST-003` | Run the scale tests at full size in the release qualification | `VREC-TST-003` |

`WO-RLS-011` is the fifty-second member. It moved the candidate identity to
0.7.0, retargeted one version-coupled fixture, and retained the first
qualification evidence; its candidate `f76da57` is on `main`. It holds no
individual verified record and is covered by `VREC-SEH-014`, which must name it.

`WO-RLS-012` is the fifty-third member: the remaining qualification of the final
candidate, the recipe-bound build, the bundle manifest, and the evidence the
aggregate record and the release record consume.

This contract is an explicit allow-list. It is not an inference from dates,
branches, merge order, lifecycle status, or every commit after the baseline.
Once approved it can only be replaced, not corrected: a work order that reaches
`implemented` with bytes in the packaged surface after the approval is a stop
condition whose only remedy is rejection and re-issue as `REL-SEH-018`.

### The commit census, reported and not enforced

`harnessctl release-unit . --from v0.6.0 --to be2f0cf` traces nine work orders
from `Harness-Work-Order` trailers on the first-parent path and reports
ninety-three untraced commits, because the trailer convention post-dates most of
the history between the two points. The owner accepted that limitation when
`WO-CIP-004` was completed (deviation 2) and chose the allow-list form for this
contract on 2026-08-26. The contract therefore names no `candidate_commit`, the
`QGP-G5P-RELEASE-UNIT` predicate passes unmeasured at its approval, and
`WO-RLS-012` must retain the derivation's output at the candidate as evidence,
stating which members it traces and which it cannot.

## Disclosed limitations carried from `REL-SEH-015`

These are recorded decisions carried unchanged, not open items, and
`VREC-SEH-014` must not restate any of this coverage as unqualified.

- `WO-TCM-001`: `VREC-TCM-002`, verified 2026-08-25T10:51:11Z against
  `f7b69d0`, discloses that `VER-TCM-001`'s two independent reviewer judgments
  do not exist. The semantic and operator-comprehension conditions are accepted
  residual risk on this release. `VREC-SEH-014` is that work order's second
  verified coverage, not its first.
- `WO-ADS-001` and `WO-ADS-002`: `VER-ADS-001`'s Scenario 8 reviewer
  classifications were not run; both records were verified with the hosted Linux
  figure pending and the lanes went green at descendants of the bound candidates.
  `WO-RLS-012` must record what the final candidate's own dual-platform run
  resolves and what remains.
- `WO-AEX-005`'s runtime scaffolding is no longer inert: `WO-AEX-006` through
  `WO-AEX-008` are in this unit, so the release notes may describe delegated
  execution only as those three work orders' verification records describe it,
  and nothing beyond.
- The two classification calls `REL-SEH-015` put to the release owner —
  `WO-HUP-004` included for the succession machinery the release decision relies
  on, `WO-HBI-003` and `WO-HBI-004` included for the byte rules the qualification
  worktree inherits — are carried unchanged. Approving this contract confirms
  them.

## Baseline and exclusions

The previous public release baseline is immutable annotated tag `v0.6.0`, tag
object `03cae3d30ea1e3933a92c9e87683b0144f8ccc77`, released candidate commit
`3b339e9fc70cc634e6dc6bda07ea6a9b1a465798`, released by `RLS-SEH-012` under
`REL-SEH-011`. This contract was drafted over `main` at
`be2f0cfec18b86d273400466cdf1c8c691d92f75`, the merge of pull request #182, on a
governance branch that touches only `docs/engineering/release-0-7-0/`.

None of the fifty-two existing members exists in the `v0.6.0` tree, and none is
named by any released `RLS-SEH-*` record.

Ninety-seven work orders on `main` read `implemented` and are unreleased. The
fifty-two existing members are above. The forty-five others are excluded by
name-class, as every previous contract of this repository excluded them: they
are documentation, revision-provenance, publication-history, verification-
supersession, work-order-lifecycle, root-evaluator adoption, RCA, and
historical release-disposition work whose declared execution scope names no
packaged-surface path. Measured at `be2f0cf`: not one of the forty-five declares
a path under `se_harness/`, `templates/`, `repository_tools/`, `release/`, or
`pyproject.toml`. Eighteen of them hold verified coverage (`WO-DOC-003`,
`WO-DOC-005`, `WO-DOC-013`, `WO-DST-004`, `WO-DST-010`, `WO-DST-017`,
`WO-DST-018`, `WO-EVK-001`, `WO-HUP-001`, `WO-HUP-002`, `WO-IAR-011`,
`WO-PYP-004`, `WO-RCA-001`, `WO-RCD-001`, `WO-RLO-001`, `WO-RLO-002`,
`WO-RLO-003`, `WO-SHB-004`) and twenty-seven do not (`WO-DOC-004`, `WO-DOC-006`,
`WO-DST-005`, `WO-DST-006`, `WO-DST-008`, `WO-PUB-001` through `WO-PUB-005`,
`WO-PYP-002`, `WO-PYP-003`, `WO-REV-002` through `WO-REV-006`, `WO-RLS-003`,
`WO-SHB-003`, `WO-SHB-005`, `WO-VSP-002` through `WO-VSP-006`, `WO-WLC-002`,
`WO-WLC-003`). `WO-HUP-001` and `WO-HUP-002` adopted a released evaluator as this
repository's own root and are excluded on the same ground as `REL-SEH-007` and
`REL-SEH-015` excluded them. `WO-RLS-011`'s rejected predecessors `WO-RLS-009`
and `WO-RLS-010` are terminal and not members.

Also excluded: merge-only commits, VREC preparation and transition commits,
supersession bookkeeping, contract rejection commits, derived publication
observations, and the exploration note on plugin distribution. Repository-
governance, RCA, and note documents may remain in the source tree and source
distribution without converting their work orders into release-bearing payload.
`WO-RLS-012` must confirm at the candidate that the packaged surface carries no
bytes authorized by an excluded work order.

## Required evidence

### Entry criteria

- The fifty-two existing members are active, `implemented`, retain
  work-order-keyed evidence, and — all but `WO-RLS-011` — hold verified
  assurance coverage. Measured at `be2f0cf`: fifty-one verified, one
  (`WO-RLS-011`) covered only by the planned aggregate record, zero other gaps.
- No existing member is named by a released release record.
- No stale `ready` verification or release record exists in the graph. Measured
  at `be2f0cf`: the only `ready` records are the two canonical templates.
- `WO-RLS-012` is separately reviewed and approved before start preflight or any
  edit. Its approval event, in its own front matter, is authoritative.
- This contract is approved by the release owner before a promotable build, the
  candidate commit, and release preparation. Immediately before that approval
  the allow-list is re-measured against the graph and every work order that
  reached `implemented` since this file was written is reported and either added
  to `gates` or excluded by name.
- Formal validation, released-evaluator `doctor`, managed-root integrity, and
  start preflight pass without structure, governance, or policy errors.

### Measured readiness at drafting

Measured over `main` at `be2f0cf` plus this packet, with the exact public 0.6.0
evaluator outside the checkout in isolated mode; the figures are recorded in
`WO-RLS-012`'s evidence when re-measured and none is a claim about the candidate.

- `validate`: `PASS`, 0 errors, every plane at E0, with the maintenance-plane
  warnings that predate this packet.
- `doctor`: 0 `FAIL`.
- `scripts/validate_release_distributions.py`: `PASS`.
- Hosted lanes at `be2f0cf` on `main`: `success` on the `push` event.

### Exact aggregate verification

**Every figure here is measured over the whole `gates` array, all fifty-three
entries including `WO-RLS-011` and `WO-RLS-012`.** On the fifty-one-member
historical basis the verification-contract union is twenty-three and the
requirement union sixty-four; those are not the figures `VREC-SEH-014` must
match.

`VREC-SEH-014` must bind one clean 0.7.0 candidate commit to exactly the
fifty-three work orders named in `gates`, to twenty-four verification contracts
(`VER-ADS-001`, `VER-ADS-002`, `VER-AEX-001`, `VER-AEX-002`, `VER-AEX-003`,
`VER-AEX-004`, `VER-AUT-001`, `VER-CIP-001`, `VER-DST-001`, `VER-HBI-001`,
`VER-HUP-004`, `VER-IPK-001`, `VER-LRE-001`, `VER-REB-006`, `VER-REB-007`,
`VER-REB-008`, `VER-REB-009`, `VER-REB-010`, `VER-RLO-004`, `VER-RLO-005`,
`VER-TCM-001`, `VER-TST-001`, `VER-VSP-002`, `VER-WEX-003`), and to fifty-eight
work-order-keyed evidence paths: the fifty-seven existing paths measured at
`be2f0cf` plus the one `WO-RLS-012` retains.

The union of requirements the fifty-three work orders implement is sixty-five.

Three counting rules apply and were measured, not assumed. The combined evidence
file `technical-communication/evidence/WO-TCM-001/WO-TCM-002-verification.md`
is keyed by directory position to both TCM work orders and is counted once.
`WO-HBI-004`, `WO-RLO-005`, `WO-REB-023`, `WO-RLO-006`, `WO-AUT-002`, and
`WO-CIP-004` each retain two keyed evidence files. `WO-RLS-011`'s single
evidence file carries both of its stages and is one path.

### Candidate and distribution evidence

- Exact candidate commit, tree, `SOURCE_DATE_EPOCH`, and clean-worktree proof.
- Recipe-bound reproducible build through `repository_tools.release_build
  replay` from the candidate's own `release/build-recipe.json` and
  `release/build-toolchain.lock`, byte-for-byte equal across two fresh producer
  instances, with the `WO-RLO-007` hand-back.
- Wheel, sdist, checksum, source-manifest, and bundle-manifest identities.
- Dual-runtime candidate package acceptance.
- Hosted run, job, and artifact identities for every required lane, on the
  events `WO-CIP-001` fixed: the publication rehearsal in `candidate` mode on
  the pull request, and the release qualification in `release-record` mode.
- Read-only `release-candidate-replay` dispatch evidence for `RLS-SEH-014` in
  `ready` before the release decision.
- Proof that historical candidates, VRECs, RLS records, contracts, rejected
  history, evidence, root managed files, maintenance state, and external policy
  remain unchanged, and that every commit a member's verified record binds is
  reachable from the candidate.

## Compatibility and migration

- First **ordinary** release: the root lock is schema 3 at exact public 0.6.0
  and that evaluator validates the complete graph without error. No
  `[bootstrap]` table, no predecessor view, no expected-red lane.
- `RLS-SEH-014` must use distribution schema 2 and is the first recipe-bound
  release record; the strict recipe interpreter is used for pre-release replay
  and for publication through the single qualification definition
  (`WO-CIP-002`).
- The candidate version and the governance-migration scenario are one fact
  recorded twice (`WO-REB-023`); `main` already carries 0.7.0 in
  `pyproject.toml` and `se_harness/__init__.py` and the matching scenario, so
  `WO-RLS-012` moves no version.
- 0.7.0 is a minor version. Beyond what `REL-SEH-015` listed — the `qualify`
  and `migrate` namespaces, declared hash-bound text classes, interpreter and
  entry-point safety, legacy release-evidence exemptions, the agent and skill
  contracts, the managed technical-communication policy, the managed operating
  card, five repository-installed skills — it adds the Phase 4 effect broker and
  delegated execution (`WO-AEX-006` through `WO-AEX-008`), the authoring policy,
  requirement template and approval predicates (`WO-AUT-001`, `WO-AUT-002`), the
  release-unit derivation, the `release-unit` command and the
  `QGP-G5P-RELEASE-UNIT` predicate (`WO-CIP-004`, `WO-CIP-005`), the
  predecessor-facts derivation (`WO-CIP-003`), and the fixture cache and parallel
  runner in the distributed test surface (`WO-TST-001`, `WO-TST-002`). Every
  managed-surface addition or change must appear in an upgrade plan before any
  apply; an adopting repository that customized a changed managed file is
  blocked rather than partially written.
- Exact public 0.6.0 predates the `qualify` namespace, so the independent
  package lane retains its documented `accept-candidate` bootstrap exception.
- The root remains schema 3 at 0.6.0 through preparation and publication.
  Adopting 0.7.0 as this repository's root evaluator needs published bytes and
  a separate approved upgrade work order.

## Security and provenance

- Treat Git state, paths, sparse state, workflow context, logs, artifacts,
  evaluator bytes, commands, JSON, hashes, locks, recipes, and environments as
  untrusted input.
- Require exact agreement among the candidate commit, the governance commit,
  the evaluator identity, the root lock, this contract, the work set,
  `VREC-SEH-014`, `RLS-SEH-014`, the bound recipe and distribution evidence,
  the two builds, and every hosted observation.
- Only verified inert bytes may cross into credential-bearing jobs. The
  protected `pypi` environment remains a separate human decision.
- Stop before any write or credential use on ambiguity, contamination, drift,
  partial output, unsafe cleanup, or provenance disagreement.

## Promotion policy

1. Done on 2026-08-26T20:48:50Z: the release owner rejected `REL-SEH-015`.
2. Approve `WO-RLS-012` (engineering owner) and this contract (release owner),
   each in its own recorded decision, on a re-measured allow-list.
3. Run start preflight, then implement only `WO-RLS-012`: requalify the
   candidate locally and on both hosted platforms, replay the recipe-bound
   build twice, produce the bundle manifest, retain complete evidence. Any work
   order reaching `implemented` with packaged-surface bytes during this step is
   a stop condition reported to the release owner.
4. Separately authorize one clean candidate commit on a dedicated branch and its
   push.
5. Require green hosted lanes on the candidate's pull request. Any red is a
   stop condition.
6. Separately transition `WO-RLS-012` to `implemented` in its own governance
   commit after complete evidence.
7. Separately prepare, review, and verify `VREC-SEH-014` with exactly the
   work-order set, keyed evidence paths, and verification contracts this
   contract names, measured on the whole-`gates` basis.
8. Separately authorize `RLS-SEH-014` preparation and schema-2 distribution
   binding, dispatch the read-only recipe replay on the review ref, and have the
   release owner release or reject it on `main`.
9. Separately authorize `publish-pypi.yml` from `main` with only the record
   identifier: tag, GitHub Release, PyPI, Pages, `release/0.7`.
10. Any later root adoption is a separate upgrade work order.

Automation creates observations and proposals only. No expected or passing
result exercises accountable authority.

## Human approval triggers

Requirements, technical, security, assurance, engineering, and release owners
decide the artifacts they own. Taken so far on this contract's lineage:
`REL-SEH-015`'s rejection and the three 2026-08-26 decisions recorded above.
Outstanding: `WO-RLS-012`'s approval, this contract's approval, work start, the
candidate commit and its push, work-order completion, `VREC-SEH-014`
preparation and verification, `RLS-SEH-014` preparation and release, tag
creation, publication, deployment, maintenance-line mutation, external policy
change, and root adoption.

## Known open questions that do not block this release

- `VER-TCM-001`'s two reviewer judgments and `VER-ADS-001`'s Scenario 8
  classifications remain owed as later governed work.
- Issue #142 (`build_recipe_sha256` as a declared hash-bound class) is open and
  deliberately unmeasured; the recipe's bytes are guarded by the versioned
  `.gitattributes` rule and `ByteExactSurfaceTests`.
- The `RCA RC-060-*` issue series stays open and ungated.
- `WO-RLO-005` carries no `[[lifecycle_events]]` entries while reading
  `implemented`; membership is measured through its evidence and `VREC-RLO-005`.
- The recipe replay's hand-back is POSIX-only (`WO-RLO-007`). Running the
  replay from a Windows workstation through Docker Desktop is inside
  `WO-RLS-012`'s decision envelope; if the workstation cannot complete it, the
  hosted `candidate`-mode rehearsal on the candidate's pull request is the
  build of record.

## Rollback criteria and procedure

Before publication, stop on incomplete authority, a work order whose bytes are
in the packaged surface and which is either unnamed by this contract or without
verified coverage, more than one active version claim, arbitrary or nonexact
omission, historical or root drift, evaluator mismatch, candidate
contamination, nondeterminism, hosted mismatch, unsafe cleanup or archive
handling, evidence disagreement, or any failed required gate. An approved
allow-list is never widened in place; the remedy is `REL-SEH-018`. Remove only
exact temporary and uncommitted outputs after path and digest verification;
never rewrite history. Correct through another governed candidate if trusted
candidate state changes.

After publication, never move `v0.7.0` and never replace immutable files.
Preserve the facts, block unsafe adoption, and prepare a separately governed
corrective release.

## Post-release observation window

After separately authorized publication, verify the immutable tag and assets,
PyPI hashes and attestations, a fresh Python 3.11 installation, Windows and LF
evidence stability, candidate identity, `init` and `adopt`, `doctor`,
`validate`, `inspect`, `dashboard`, `release-unit`, the installed skills, the
managed technical-communication policy and its router row, the work-order
delegation table and its validator rules, the effect broker's refusal
boundaries, the managed operating card and its 1024-byte bound, the enforced
failure rendering and restitution digest, the `qualify` and `migrate`
namespaces, Pages provenance, the `release/0.7` maintenance state, and later
root-upgrade readiness.
