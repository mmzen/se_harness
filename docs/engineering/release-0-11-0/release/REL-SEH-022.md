+++
id = "REL-SEH-022"
type = "release_contract"
title = "Release se-harness 0.11.0: the 0.10.0 root adopted, one projection command, records admitted by construction, and Phase 4 reduced to its guarantee"
status = "approved"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
gates = ["WO-ECP-006", "WO-ECP-015", "WO-ECP-016", "WO-ECP-017", "WO-HUP-010", "WO-RLS-017"]

[release_unit]
previous_release_tag = "v0.10.0"
untraced_exemptions = ["47f67de2d4c41b5da0cd8df1b3a5be459de74061"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T14:25:20Z"
decided_by = "release-owner"
reason = "Approved by the accountable release owner on 2026-08-29, 'Approve REL-SEH-022 and WO-RLS-017, start', as a decision distinct from the work order's approval. The allow-list was re-measured immediately before this approval over main at 8db0b96: the five implemented, verified, unreleased work orders are exactly WO-HUP-010, WO-ECP-015, WO-ECP-016, WO-ECP-017 and WO-ECP-006, and no work order reached implemented since the packet was drafted. This approval authorizes WO-RLS-017 to be approved and started as separate acts; it authorizes no candidate, build, record, tag, publication or deployment."
+++

# Release contract: se-harness 0.11.0

## Lifecycle and authority

This contract is a definition. Its approval by the release owner authorizes
`WO-RLS-017` to be approved and started as separate acts; it authorizes no
candidate, build, verification record, release record, tag, publication or
deployment by itself. Every later step is the decision of the role that owns
it, recorded on the artifact it changes. The aggregate verification record
is `VREC-SEH-020`; the release record is `RLS-SEH-020`.

## Release unit

One `se-harness` 0.11.0 release derived from one clean candidate commit cut
from `main`: a recipe-bound reproducible wheel, a normalized source
distribution, a checksum manifest, a schema-2 bound distribution table, an
immutable `v0.11.0` tag, GitHub Release assets, publication of the same
qualified files to PyPI, the canonical `release/0.11` maintenance line
established at the released candidate, a release-bound static Explorer
demonstration, and the `last` alias tag and GitHub "latest" marker moved
to it.

The release-bearing work added after the immutable `v0.10.0` baseline is
exactly these five work orders. Every row was measured on `main` at
`8db0b96` as active, `implemented`, holding work-order-keyed evidence,
verified, absent from the `v0.10.0` tree, and unnamed by any released
release record.

| Work order | Outcome | Coverage at drafting |
| --- | --- | --- |
| `WO-HUP-010` | Adopt exact public 0.10.0 as the standard root, the simple way; candidate moved to 0.11.0 | `VREC-HUP-009` verified |
| `WO-ECP-015` | Fold `focus` into `check`: the checkpoint-less projection, one name in every contract | `VREC-ECP-018` verified |
| `WO-ECP-016` | Admit the selected work order's own verification and release records to the change set (issue #264) | `VREC-ECP-019` verified |
| `WO-ECP-017` | Remove the `focus` alias and move `harness-orient` to `check` | `VREC-ECP-020` verified |
| `WO-ECP-006` | Remove the Phase 4 envelope, bundle and broker; keep the journaled apply; retire the stubbed skills | `VREC-ECP-021` verified |

`WO-RLS-017` is the sixth member: it qualifies and builds the candidate and
retains the evidence; the candidate version already reads 0.11.0 (moved by
`WO-HUP-010`). It receives its verified coverage from `VREC-SEH-020`.

Packaged-surface bytes in the unit come from `WO-HUP-010` (version
identity), `WO-ECP-015` (`workflow.py`, `cli.py`, `workflow_contract.json`
and the template `WORKFLOW.json`/`.md`, the `harness-orient` skill notes),
`WO-ECP-016` (`workflow_compliance.py`), `WO-ECP-017` (`cli.py`,
`workflow.py`, `workflow_compliance.py`, the template `harness-orient`
core, the template README seed) and `WO-ECP-006` (nine modules and two
catalogs removed, `journaled_apply.py` added, `cli.py`, `mutation_guard.py`,
`pyproject.toml`, the template validator and work-order template, three
skills and their adapters removed).

### Commit census

`harnessctl release-unit . --from v0.10.0 --to 8db0b96` reads eight
first-parent commits, all merge commits GitHub wrote for pull requests.
Since `RLS-SEH-019` the derivation follows a merge to its second-parent
range, so seven of the eight trace through the branch commits they merged:
`103127c` (#260) traces `WO-RLS-016`, which `RLS-SEH-019` released and
which is therefore not a member; `5e5e9d6` (#262) `WO-HUP-010`; `5bde10a`
(#263) `WO-ECP-015`; `01f648f` (#265) `WO-ECP-016`; `78306e0` (#266)
`WO-ECP-017`; `bc8d242` (#267) and `8db0b96` (#268) `WO-ECP-006`. One,
`47f67de` (#261), merged a documentation-only pull request that carries no
work order by this repository's rule for `docs/notes/`, and is exempted in
`[release_unit].untraced_exemptions`. The traced, released `WO-RLS-016`
cannot be exempted (an exemption covers only a commit without a trailer)
and stays in the derivation, so the contract comparison reports it as
missing from `gates` by construction; that finding is recorded evidence, not
a defect, at approval and at the candidate.

| Commit | Pull request | Traces | Disposition |
| --- | --- | --- | --- |
| `103127c` | #260 | `WO-RLS-016` | released by `RLS-SEH-019`, not a member, not exemptable |
| `47f67de` | #261 | nothing | documentation pull request, exempted |
| `5e5e9d6` | #262 | `WO-HUP-010` | member |
| `5bde10a` | #263 | `WO-ECP-015` | member |
| `01f648f` | #265 | `WO-ECP-016` | member |
| `78306e0` | #266 | `WO-ECP-017` | member |
| `bc8d242` | #267 | `WO-ECP-006` | member |
| `8db0b96` | #268 | `WO-ECP-006` | member (post-merge verification commit) |

This contract names no `candidate_commit`: the candidate is created by
`WO-RLS-017` after this approval. `QGP-G5P-RELEASE-UNIT` therefore passes
unmeasured at approval, as for `REL-SEH-021`; the census above is the
reported evidence, and `WO-RLS-017` re-runs the derivation at the candidate
and records it, expecting the one exemption, `WO-RLS-016` traced and
excluded, and `WO-RLS-017` traced.

## Required evidence

### Entry criteria

- The five existing members are active, `implemented`, retain
  work-order-keyed evidence, and hold verified assurance coverage. Measured
  at `8db0b96`: five of five.
- No existing member is named by a released release record.
- No stale `ready` verification or release record exists in the graph beyond
  the two canonical templates. Measured at `8db0b96`: none.
- `WO-RLS-017` is separately reviewed and approved before start preflight or
  any edit.
- This contract is approved by the release owner before the candidate commit
  and the promotable build. Immediately before that approval the allow-list is
  re-measured and every work order that reached `implemented` since this file
  was written is reported and either added to `gates` or excluded by name.
- Formal validation, released-evaluator `doctor`, managed-root integrity and
  start preflight pass without structure, governance or policy errors.

### Measured readiness at drafting

Measured over `main` at `8db0b96` plus this packet, with the exact public
0.10.0 evaluator outside the checkout in isolated mode.

- `validate`: 0 errors, 479 pre-existing maintenance warnings.
- `doctor`: 0 `FAIL`.
- Hosted lanes at `8db0b96` on `main`: the managed lane and the governor
  assessment `success`; the publication rehearsal and candidate evidence
  read at the candidate.

### Exact aggregate verification

**Every figure here is measured over the whole `gates` array, all six
entries.** `VREC-SEH-020` must bind one clean 0.11.0 candidate commit to
exactly the six work orders named in `gates`, to seven verification
contracts (`VER-DST-001`, `VER-ECP-007`, `VER-ECP-011`, `VER-ECP-012`,
`VER-ECP-013`, `VER-ECP-014`, `VER-HUP-010`), and to six work-order-keyed
evidence paths: the five members' handoff packets listed in the domain
index plus `WO-RLS-017`'s packet under
`docs/engineering/release-0-11-0/evidence/`. The requirement union is
eight: `REQ-DST-006`, `REQ-ECP-014`, `REQ-ECP-018`, `REQ-ECP-022`,
`REQ-ECP-023`, `REQ-ECP-024`, `REQ-HUP-020`, `REQ-HUP-021`.

### Candidate qualification

At the exact candidate commit, all with the governing 0.10.0 evaluator
outside the checkout unless stated: `validate` 0 errors; `doctor` 0 `FAIL`;
review preflight `PASS`; `scripts/validate_release_distributions.py` and
`scripts/check_portable_release_surface.py` `PASS` in `--repository`,
`--wheel` and `--harnessctl` modes; the candidate's own `qualify
complete-candidate`; the full suite on Linux and on Windows; the real
upgrade rehearsal 0.10.0 to 0.11.0 `pass` on both platforms with agreeing
`semantic_sha256`; all pull-request lanes `success` at the candidate head.

### Build of record

The recipe-bound replay (`python -m repository_tools.release_build replay`)
run on a host with the pinned linux/amd64 producer image, two byte-identical
producer runs, the bundle manifest from
`scripts/create_release_bundle_manifest.py`, and the hosted
`release-candidate-replay.yml` dispatch on the review ref reproducing the same
digests.

## Compatibility and migration

0.11.0 changes the evaluator, the packaged workflow contract, the template
validator, the template work-order template, one managed policy document,
one seed and the shipped skills; installed copies regenerate on `upgrade`:

- **One projection command.** `harnessctl check --artifact ID` without a
  checkpoint is the projection `focus` returned; `focus` was an alias
  through 0.10.0 and is removed: a script still calling it exits 2 with
  `harnessctl check --artifact ID` named on standard error. The five
  procedure steps and `WFL-003` name `check`; `harness-orient` invokes
  `check` and probes for the optional `--checkpoint` first, so the shipped
  0.11.0 core degrades (not blocks) against an older evaluator
  (`WO-ECP-015`, `WO-ECP-017`).
- **Records admitted by construction.** The `scope` and `handoff`
  checkpoints admit the selected work order's own verification and release
  records and their evaluator evidence, so a pull request carrying its own
  records is green without listing a records directory (`WO-ECP-016`,
  issue #264). Packets written for 0.10.0 that listed
  `verification-records/` keep working.
- **Phase 4 reduced to its guarantee.** `harnessctl delegated-workflow`,
  the `[agentic_delegation]` work-order table and its validator (`E021`),
  the autonomy envelope, change bundles, receipts and the effect broker are
  gone; a work order carrying `[agentic_delegation]` is no longer validated
  against a removed schema and the table should be deleted. The three
  writing skills (`harness-draft-change`, `harness-execute-work-order`,
  `harness-prepare-assurance`) and their `.claude` adapters are removed on
  `upgrade` (`doctor` reports `remove`, not drift); `harness-orient` and
  `harness-operator-brief` remain. The journaled apply survives as
  `se_harness.journaled_apply`, not yet the write path of any command
  (`WO-ECP-006`; `REQ-ECP-017` and `REQ-ECP-011` follow later).
- **Root identity.** This repository's own root moved to 0.10.0
  (`WO-HUP-010`); consumers are unaffected.

A 0.10.0 root reads a 0.11.0-written lock without change (schema 3, five
evaluator fields). The canonical block and `result_sha256` preimage are
unchanged. Ready records prepared under 0.10.0 report `E012` after a root
advances to 0.11.0 until re-prepared; the upgrade rehearsal tolerates that
by design.

## Security and provenance

The build of record is recipe-bound and digest-pinned
(`release/build-recipe.json`, `release/build-toolchain.lock`); the release
record binds the wheel and sdist digests through a schema-2 distribution
table; the publication workflow moves only verified inert bytes into
privileged jobs and the `pypi` environment remains a separate human decision.
Identity by version, installed-payload digest and archive pair is unchanged.
The removal of Phase 4 removes 8,876 lines reachable from the CLI and every
consumer's installed skills; the wheel is walked at the candidate to show
none of the removed names ships.

## Promotion policy

- `VREC-SEH-020` verified by the assurance owner on the exact candidate.
- `RLS-SEH-020` prepared by generic `prepare-release` from a wheel-file
  installed 0.10.0 evaluator, then bound by
  `scripts/bind_release_distribution.py` to the build of record; the hosted
  replay dispatched on the review ref before the release decision.
- The `released` transition rides its own pull request to `main` and is the
  release owner's act.
- After the record is `released` on `main`: `publish-pypi.yml` dispatched from
  `main` with only `release_record=RLS-SEH-020`; tag `v0.11.0`, GitHub
  Release, `release/0.11` established, PyPI publication, Pages deployment;
  then, as the release note records since #261, `gh release edit v0.11.0
  --latest` and the `last` alias tag moved to `v0.11.0` after the
  observation passes.

## Human approval triggers

- Approval of this contract (release owner) and of `WO-RLS-017` (engineering
  owner), as two distinct decisions.
- Start of `WO-RLS-017`, its completion, the verification of `VREC-SEH-020`,
  the preparation and release of `RLS-SEH-020`, the publication dispatch and
  the `pypi` environment: each a separate decision by its accountable owner.
- Any work order reaching `implemented` with packaged-surface bytes after this
  contract's approval is a stop condition; the remedy is rejection and a
  successor contract, never widening in place.

## Rollback

A defect found after publication is repaired forward by a successor release;
a published 0.11.0 is never withdrawn from PyPI. A consumer stays on 0.10.0
by not upgrading; this repository's root stays on 0.10.0 until a later
adoption work order.

## Observation window

The acceptance in the wild is this repository's adoption of 0.11.0 as its
standard root by an ordinary upgrade work order, after which its own pull
requests carry their records without scoping a records directory
(`VER-ECP-012`'s hosted demonstration), its shipped `harness-orient`
invokes `check`, and its root validator no longer carries the
`[agentic_delegation]` rule.

## Known open questions that do not block this release

- The suite runs hosted on Linux only; Windows readings remain workstation
  readings until a Windows test lane exists.
- Issue #269: a Linux fixture-teardown race (`Directory not empty: '.git'`)
  made three lanes red on 2026-08-29, each green on re-run; a re-run is not a
  defect of the candidate.
