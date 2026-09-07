+++
id = "REL-SEH-027"
type = "release_contract"
title = "Release se-harness 0.16.0: the evaluator scripts leave the governed repository, one installation command, the reader-first specification shape"
status = "approved"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-09-07"
updated = "2026-09-07"
previous_release_tag = "v0.15.0"

[relations]
gates = [
  "WO-DST-024",
  "WO-ECP-026",
  "WO-HUP-016",
  "WO-TCM-009",
  "WO-TCM-010",
  "WO-RLS-022",
]

[release_unit]
untraced_exemptions = [
  "e4192edd84a75972d91566050c78c6ccbd4b16be",
  "8f54c527fc66c2b56fdfd3f7db9c38808461e8a9",
  "079d6053dd5a1f075c060838e68db617475063e8",
  "2ef70ca6ec7838a33c957775e0e6257cd40c636a",
]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T07:26:08Z"
decided_by = "release-owner"
reason = "Approved by the accountable release owner on 2026-09-07 by selecting the presented option 'Approve both (Recommended)', as a decision distinct from the work order's approval, after the census was measured on main at 9069ff5d with every required member holding a verified record (VREC-HUP-015, VREC-TCM-009, VREC-ECP-030, VREC-DST-021), the released WO-RLS-021 and the approved, waiting WO-TCM-011 excluded by construction, the four notes-class merges #348, #351, #357 and #363 exempted by name, and every hosted lane except the pre-approval review preflight green at 4deaf4f2. The allow-list is exact at approval: six gates."
+++

# Release contract: se-harness 0.16.0

## Lifecycle and authority

This contract is a definition. Its approval by the release owner authorizes
`WO-RLS-022` to be approved and started as separate acts; it authorizes no
candidate, build, verification record, release record, tag, publication or
deployment by itself. Every later step is the decision of the role that owns
it, recorded on the artifact it changes. The aggregate verification record
is `VREC-SEH-025`; the release record is `RLS-SEH-025`.

This contract was drafted on 2026-09-07 on the repository owner's
instruction "release 0.16.0", with `main` at `9069ff5d` and no work order
in progress. Every member whose assurance is `required` holds a verified
record. A member that reaches `implemented` after approval is a stop
condition, never a widening in place.

## Release unit

One `se-harness` 0.16.0 release derived from one clean candidate commit cut
from `main`: a recipe-bound reproducible wheel, a normalized source
distribution, a checksum manifest, a schema-2 bound distribution table, an
immutable `v0.16.0` tag, GitHub Release assets, publication of the same
qualified files to PyPI, the canonical `release/0.16` maintenance line
established at the released candidate, a release-bound static Explorer
demonstration, and the `last` alias tag and GitHub "latest" marker moved
to it.

The release-bearing work added after the immutable `v0.15.0` baseline is
five work orders. They were measured on `main` at `9069ff5d` as active,
`implemented`, holding work-order-keyed evidence, absent from the `v0.15.0`
tree, and unnamed by any released release record. Four hold verified
coverage; `WO-TCM-010` (assurance `not_required`) is covered by the
aggregate record alone.

| Work order | Outcome | Coverage at drafting |
| --- | --- | --- |
| `WO-HUP-016` | Adopt exact public 0.15.0 as the standard root, the simple way; candidate moved to 0.16.0 | `VREC-HUP-015` verified |
| `WO-TCM-009` | The reader-first specification shape: the `contract` field, one identifier per rule, the `Coverage` table read by the validator and shown by the Explorer, `W-AUT-019` to `W-AUT-023` on specification drafts, `E-DCM-005` for a deviation that names no rule | `VREC-TCM-009` verified |
| `WO-TCM-010` | Correct the first example of `SPEC-TCM-006` by amendment record | assurance `not_required`; covered by `VREC-SEH-025` |
| `WO-ECP-026` | `init` is the one installation command, keyed by the target's content; `adopt` stays a plain alias for the 0.16.0 release only; `--dry-run` documented; seven definitions closed by amendment record | `VREC-ECP-030` verified |
| `WO-DST-024` | The evaluator's scripts live in `se_harness/engine/` inside the wheel and run as subprocesses by path; the installer writes none of them into a repository; the eight retired `scripts/` paths leave every installation at its next `upgrade --apply` through the leaving-set rule | `VREC-DST-021` verified |

`WO-RLS-022` is the sixth member: it qualifies the candidate, takes the
build of record from the hosted pinned producer, and retains the evidence;
the candidate version already reads 0.16.0 (moved by `WO-HUP-016`). It
receives its verified coverage from `VREC-SEH-025`.

### What this release is for

0.16.0 is a distribution release. Since `v0.15.0` the packaged surface
changed in 23 paths as Git reads them with rename detection: the four
evaluator scripts and the Explorer template moved from
`templates/repository/standard/scripts/` to `se_harness/engine/`, the
directory that no longer exists in the standard template, and the installer,
the CLI, preflight, provenance, renumbering, release qualification and
candidate acceptance now locate them there; the validator gains the
`Coverage` reading, `E-DCM-005` and the five specification advisories; the
Explorer gains the specification `plain_words` projection; the managed
`SPECIFICATION.template.md` takes the reader-first shape with the `contract`
field, `ARTIFACT_AUTHORING.md` and `DECISION.template.md` follow; `adopt` is
an alias of `init` with one help sentence; `pyproject.toml` ships the engine
files as package data and lists no `scripts/` data files; the version reads
0.16.0.

For this repository the release is the precondition of two things: the
adoption that removes the eight hash-locked 0.15.0 script copies from the
root `scripts/` directory, after which the in-tree `doctor` stops reporting
them as `lock-extra`; and the delegated start of `WO-TCM-011`, which by its
own constraint waits for `RLS-SEH-025` to be released and adopted.

### Commit census

`harnessctl release-unit . --from v0.15.0 --to 9069ff5d` reads 14
first-parent commits, all merge commits GitHub wrote for pull requests. Ten
are traced through their branch commits' `Harness-Work-Order` trailers. Four
carry no trailer: the pull requests #348 and #351 (the root-cause analysis of
issue #347, under `docs/notes/` then moved to `docs/rca/`), #357 (the
specification-readability assessment under `docs/notes/`) and #363 (the
specification terms of the repository-owned `GLOSSARY.md`, the file the
harness seeds once and never rewrites). Each touched only paths the owner
merges without a work order, and each is therefore exempted above by the
release owner's decision, with the reason that a notes-class pull request
needs a reviewer and not a work order. With those four exemptions the
census yields seven traced work orders, of which five are members.

| Traced work order | Pull request(s) | Disposition |
| --- | --- | --- |
| `WO-RLS-021` | #350 | the 0.15.0 release branch; released by `RLS-SEH-024`, therefore outside `gates` by construction |
| `WO-HUP-016` | #352, #353 | member |
| `WO-ECP-026` | #359, #361 | member |
| `WO-TCM-009` | #358, #362 | member |
| `WO-TCM-010` | #364 | member |
| `WO-TCM-011` | #366 | approved, not started; outside `gates` by construction, see below |
| `WO-DST-024` | #365 | member |

`WO-TCM-011` is traced through the merge of its definition packet #366,
whose two trailered commits touch `docs/engineering/technical-communication/`
only. It carries no implementation commit and no packaged byte; the
derivation reads it as `packaged` from its execution scope, not from the
path. Its own constraint states that execution starts only after
`RLS-SEH-025` is released and adopted as this repository's root, so that the
specification family has had its one release of advisories (`DEC-TCM-004`).
It is therefore excluded from this unit by construction, exactly as the
released `WO-RLS-021` is, and the derivation's blocker "`WO-TCM-011` is
approved, not implemented" is the reading this contract predicts at every
stage until the adoption that follows this release. `WO-TCM-011` reaching
`in_progress` or `implemented` before the candidate is bound is a stop
condition for this contract.

`harnessctl release-unit . --from v0.15.0 --to 9069ff5d --contract
REL-SEH-027`, with each of the four exempted commits also passed as
`--exempt` (the 0.15.0 command reads exemptions from its flags; the array
above is what the approval gate reads), derives untraced 0, exempted 4, and
reports the `E-CIP-001` findings this contract predicts by construction: the
`gates` difference, the released `WO-RLS-021` and the approved `WO-TCM-011`
present in the derivation and `WO-RLS-022` not yet derivable because its
commits do not exist, as `REL-SEH-026` reported `WO-RLS-020` and
`WO-RLS-021`; the incompleteness carried by `WO-TCM-011`; and, until the
candidate exists, the absence of `candidate_commit`. No trace repair is
needed.

This contract names no `candidate_commit`: the candidate is created by
`WO-RLS-022` after this approval. `QGP-G5P-RELEASE-UNIT` therefore passes
unmeasured at approval; the census above is the reported evidence, and
`WO-RLS-022` re-runs the derivation at the candidate and records it.

## Required evidence

### Entry criteria

- Every existing member is active, `implemented`, retains work-order-keyed
  evidence, and every member whose assurance is `required` holds verified
  coverage. Measured at `9069ff5d`: four of four required members.
- No existing member is named by a released release record.
- No stale `ready` verification or release record exists in the graph
  beyond the canonical templates.
- No work order is `in_progress` on `main`; `WO-TCM-011` is `approved` and
  waits by its own constraint.
- `WO-RLS-022` is separately reviewed and approved before start preflight
  or any edit.
- This contract is approved by the release owner before the candidate
  commit and the promotable build. Immediately before that approval the
  allow-list is re-measured and every work order that reached `implemented`
  since this file was written is reported and either added to `gates` or
  excluded by name; every new untraced first-parent commit is exempted by
  name with its reason or the derivation fails.
- Formal validation, released-evaluator `doctor`, managed-root integrity
  and start preflight pass without structure, governance or policy errors.

### Measured readiness at drafting

Measured over `main` at `9069ff5d` plus this packet, with the exact public
0.15.0 evaluator outside the checkout in isolated mode, installed from the
wheel whose SHA-256 `eb09343f…` equals the distribution table of
`RLS-SEH-024`.

- `validate --advisories`: 1,342 artifacts, 0 errors, 71 pre-existing
  maintenance warnings, 0 advisories.
- `doctor`: 116 `PASS`, 0 `FAIL`, 42 `W013` location warnings on
  historical records.
- Hosted lanes at `9069ff5d` on `main`: Engineering Harness `validate`,
  SE Harness Candidate Evidence, Governor Transition Assessment and
  Publication Rehearsal, all `success`.

### Exact aggregate verification

**Every figure here is measured over the whole `gates` array, all six
entries.** `VREC-SEH-025` must bind one clean 0.16.0 candidate commit to
exactly the six work orders named in `gates`, to five verification
contracts (`VER-DST-001`, `VER-DST-025`, `VER-ECP-022`, `VER-HUP-016`,
`VER-TCM-006`; `WO-TCM-009` and `WO-TCM-010` share the last), and to six
work-order-keyed evidence paths: each member's handoff packet in its domain
plus `WO-RLS-022`'s packet under `docs/engineering/release-0-16-0/evidence/`.
The requirement union of the five content members is seven; with
`REQ-DST-006` from `WO-RLS-022` it is eight.

### Candidate qualification

At the exact candidate commit, all with the governing 0.15.0 evaluator
outside the checkout unless stated: `validate` 0 errors; `doctor` 0 `FAIL`;
review preflight `PASS`; the handoff check over the Git-derived change set;
`scripts/validate_release_distributions.py` and
`scripts/check_portable_release_surface.py` `PASS` in `--repository`,
`--wheel` and `--harnessctl` modes; the candidate's own `qualify
complete-candidate` (read from the hosted Linux lane for the `RID018`
boundary reason); the full suite on Linux (hosted) and on Windows (this
workstation, `PYTHONUTF8=1`); the real upgrade rehearsal 0.15.0 to 0.16.0
`pass` on both hosted platforms with agreeing `semantic_sha256`; all
pull-request lanes `success` at the candidate head.

### Build of record

The recipe-bound replay run by the hosted Publication Rehearsal in
`candidate` mode, dispatched on `release/0.16.0` at the candidate head
(the pull-request event builds the merge commit, not the head):
`release-qualification.yml` executes `python -m repository_tools.release_build replay`
on the pinned linux/amd64 producer image through Docker on the GitHub
runner, two byte-identical producer runs, and retains
`release-build-replay.json` whose `manifest` is the schema-2 bundle
manifest. That manifest is downloaded from the run at the bound candidate,
its `candidate.commit` checked equal, retained as
`docs/engineering/release-0-16-0/evidence/RLS-SEH-025-bundle.json`, and
bound into `RLS-SEH-025`; the hosted `release-candidate-replay.yml`
dispatch on the review ref must then reproduce the same digests from the
bound record, as `WO-RLS-021` did for 0.15.0.

## Compatibility and migration

0.16.0 changes what the installer writes and one managed template family.
`upgrade` from 0.15.0 removes the eight managed `scripts/` paths
(`validate_engineering_artifacts.py`, `generate_harness_dashboard.py`,
`inspect_engineering_artifacts.py`, `select_harness_work_order.py`,
`artifact_layout_registry.py`, `check_engineering_harness.sh`,
`check_engineering_harness.ps1`, `harness_explorer/index.template.html`)
from every existing installation through the leaving-set rule and drops
their lock entries; the evaluator runs the same programs from inside the
installed package, so `validate`, `dashboard`, `inspect` and the managed
workflow produce the same verdicts. It rewrites the managed copies of
`SPECIFICATION.template.md`, `DECISION.template.md` and
`ARTIFACT_AUTHORING.md`. Owner content is untouched; a customized managed
file blocks the upgrade as always. No existing artifact needs to change: the
`contract` field and the `Coverage` table are additive, the five new
advisories fire on specification drafts only, and an approved specification
in the earlier shape is read as before. A repository that installs with
`harnessctl adopt` keeps working for this one release; the alias is removed
by a later work order under `REQ-ECP-030`, so scripts should say `init`. A
0.15.0 root reads a 0.16.0-written lock without change.

## Security and provenance

The build of record is recipe-bound and digest-pinned
(`release/build-recipe.json` `0c3f368c…`, `release/build-toolchain.lock`,
both unchanged since `v0.12.0`); the release record binds the wheel and
sdist digests through a schema-2 distribution table; the publication
workflow moves only verified inert bytes into privileged jobs and the
`pypi` environment remains a separate human decision. Identity by version,
installed-payload digest and archive pair is unchanged. `pyproject.toml`
moves the engine files into package data and removes the `scripts/`
data-files table (`WO-DST-024`); the portable release surface check covers
it.

## Promotion policy

- `VREC-SEH-025` verified by the assurance owner on the exact candidate.
- `RLS-SEH-025` prepared by generic `prepare-release` from a wheel-file
  installed 0.15.0 evaluator, then bound by
  `scripts/bind_release_distribution.py` to the build of record; the hosted
  replay dispatched on the review ref before the release decision.
- The `released` transition rides the release pull request to `main` and is
  the release owner's act.
- After the record is `released` on `main`: `publish-pypi.yml` dispatched
  from `main` with only `release_record=RLS-SEH-025`; tag `v0.16.0`, GitHub
  Release, `release/0.16` established, PyPI publication, the Pages
  deployment; then `gh release edit v0.16.0 --latest` and the `last` alias
  tag moved to `v0.16.0` after the observation passes.

## Human approval triggers

- Approval of this contract (release owner) and of `WO-RLS-022`
  (engineering owner), as two distinct decisions, after the census has been
  re-measured.
- Start of `WO-RLS-022`, its completion, the verification of
  `VREC-SEH-025`, the preparation and release of `RLS-SEH-025`, the
  publication dispatch and the `pypi` environment: each a separate decision
  by its accountable owner.
- Any work order reaching `implemented` with packaged-surface bytes after
  this contract's approval, and `WO-TCM-011` leaving `approved` before the
  candidate is bound, are stop conditions; the remedy is rejection and a
  successor contract, never widening in place.

## Rollback criteria and procedure

A defect found after publication is repaired forward by a successor
release; a published 0.16.0 is never withdrawn from PyPI. A consumer stays
on 0.15.0 by not upgrading; its `scripts/` copies and the earlier
specification template simply stay in place.

Stop condition: the candidate commit is not an ancestor of the ref being
released, or `harnessctl release-unit --contract REL-SEH-027` reports an
`E-CIP-001` finding beyond the `gates` difference and the incompleteness
predicted by construction above. The remedy is a new contract naming a new
candidate, never an in-place edit of `gates`.

## Post-release observation window

Within one week of publication: a fresh repository initialised from the
published 0.16.0 wheel holds no `scripts/` directory of the harness's making
and its lock names no `scripts/` path, `harnessctl validate` and
`harnessctl dashboard` run against it from the installed package, its
`SPECIFICATION.template.md` opens with the `contract` field, and `harnessctl
adopt` still answers as `init`; the public demonstration at
`mmzen.github.io/se_harness` still renders. This repository's adoption of
0.16.0 as its own root is an ordinary later work order and is where the
eight root `scripts/` copies leave and `WO-TCM-011` may start.

## Known open questions that do not block this release

- The suite runs hosted on Linux only; Windows readings remain workstation
  readings until a Windows test lane exists. On this workstation one test
  errors deterministically on a read-only temporary Git object during
  teardown (`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`),
  the baseline `WO-RLS-021` also recorded.
- Issue #269: the Linux fixture-teardown flake; a re-run is not a defect of
  the candidate.
- `docs/notes/getting-started.md` still pins `se-harness==0.14.0` in its
  install line; the note is ungoverned and is corrected by a notes pull
  request, not by this release.
- Pull request #363 changed `GLOSSARY.md` at the repository root without a
  work order. The glossary is repository-owned content the harness never
  rewrites, and the owner merged it as a notes-class change; the ungoverned
  path list in `AGENTS.md` does not name it. Whether to add it there is the
  owner's call and not a condition of this release.
- The `adopt` alias is a one-release window; its removal is a later work
  order under `REQ-ECP-030`.
