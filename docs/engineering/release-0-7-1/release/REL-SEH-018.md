+++
id = "REL-SEH-018"
type = "release_contract"
title = "Release se-harness 0.7.1: the simple released-evaluator upgrade"
status = "draft"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
gates = ["WO-REB-024", "WO-REB-025", "WO-REB-026", "WO-REB-027", "WO-RLS-013"]

[release_unit]
previous_release_tag = "v0.7.0"
untraced_exemptions = ["20fa9f0b77241c0158020fe94ddd5d2f29afb061", "76100cf75c4349fefe310c25e379a59f17e9cffe", "088b08befbce5874289fd5877510000048f24226", "28487f0112b2f67c5f5471f1028840ec30cca6e5", "7284743d167ee33ccd8236f7c96409c32e1d2faa", "f605e580e6366a739dc020559cac35a89e1ffc39"]
+++

# Release Contract: Release se-harness 0.7.1: the simple released-evaluator upgrade

## Lifecycle and authority

This contract's approval by the release owner is what permits a promotable build,
the candidate commit, and release preparation. Its authoritative state, and the
timestamp and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. It succeeds `REL-SEH-017`, the released 0.7.0
contract, and rejects nothing.

On 2026-08-27 the repository owner gave standing direction: *the verification of
the newly installed wheel: sha256 signature, and an existing work order is way
too restrictive. This check (leading to error MG004) must be removed as well as
MG007 (that require to bind to a work order). The install process must be simple
and straight forward.* `WO-REB-027` implemented that on `main` and holds verified
coverage (`VREC-REB-024`). It cannot govern this repository until it is released,
because only a released evaluator installed outside the checkout governs
(`REQ-REB-001`). This contract releases it as 0.7.1.

Approval authorizes nothing on its own. It is the precondition for
`WO-RLS-013`'s candidate commit and promotable build, `VREC-SEH-015`, and
`RLS-SEH-016` preparation; each remains a separate later decision.

## Release unit

One incremental `se-harness` 0.7.1 release derived from one clean candidate
commit cut from `main`: a recipe-bound reproducible wheel, a normalized source
distribution, a checksum manifest, a schema-2 bound distribution table, an
immutable `v0.7.1` tag, GitHub Release assets, publication of the same qualified
files to PyPI, the canonical `release/0.7` maintenance line advanced to the
released candidate, and a release-bound static Explorer demonstration.

The release-bearing work added after the immutable `v0.7.0` baseline is exactly
these four work orders. Every row was measured on `main` at `f605e58` as
active, `implemented`, holding work-order-keyed evidence, absent from the
`v0.7.0` tree, unnamed by any released release record, and holding verified
assurance coverage.

| Work order | Outcome | Verified coverage |
| --- | --- | --- |
| `WO-REB-024` | Select the closed predecessor history from bootstrap records only | `VREC-REB-021` |
| `WO-REB-025` | Exercise the publication predecessor view only when its condition holds | `VREC-REB-022` |
| `WO-REB-026` | Materialize the complete governance snapshot as the Pages view when no predecessor view applies | `VREC-REB-023` |
| `WO-REB-027` | Make the evaluator upgrade simple: payload identity, no packet, index installs | `VREC-REB-024` |

`WO-RLS-013` is the fifth member: it moves the candidate identity to 0.7.1,
qualifies and builds the candidate, and retains the evidence. It receives its
verified coverage from the aggregate record `VREC-SEH-015`.

Packaged-surface bytes in the unit come from `WO-REB-027` (`se_harness/`) and
from `WO-RLS-013` (the version identity). `WO-REB-024` through `WO-REB-026`
changed repository tooling and workflows only; they are members because their
commits are on the release path and they are the repairs that let an ordinary
record publish.

### Commit census

`harnessctl release-unit . --from v0.7.0 --to f605e58` traces `WO-REB-027`
from the merge commit of pull request #198 and reports six first-parent commits
without a standalone `Harness-Work-Order` trailer. Each is exempted in
`[release_unit].untraced_exemptions` for the reason given here; with these
exemptions the derivation is complete.

| Commit | Pull request | Reason |
| --- | --- | --- |
| `20fa9f0` | #184 | merge of `WO-REB-024`'s branch; the trailer is on the branch commits and in the pull-request body, not on the merge commit |
| `76100cf` | #183 | merge of the `REL-SEH-017` contract and `WO-RLS-012` governance for 0.7.0, released as `RLS-SEH-015` |
| `088b08b` | #185 | merge of the `RLS-SEH-015` released transition, a release-record act with no work order |
| `28487f0` | #186 | merge of `WO-REB-025`'s branch; trailer on the branch commits and in the body |
| `7284743` | #188 | merge of `WO-REB-026`'s branch; trailer on the branch commits and in the body |
| `f605e58` | #197 | merge of the `WO-HUP-006` rejection, a lifecycle decision with no eligible carrier; the owner accepted the red managed check |

This contract names no `candidate_commit`: the candidate is created by
`WO-RLS-013` after this approval. `QGP-G5P-RELEASE-UNIT` therefore passes
unmeasured at approval, exactly as for `REL-SEH-017`; the census above is the
reported evidence, and `WO-RLS-013` re-runs the derivation at the candidate and
records it.

## Required evidence

### Entry criteria

- The four existing members are active, `implemented`, retain work-order-keyed
  evidence, and hold verified assurance coverage. Measured at `f605e58`: four
  of four.
- No existing member is named by a released release record.
- No stale `ready` verification or release record exists in the graph beyond the
  two canonical templates.
- `WO-RLS-013` is separately reviewed and approved before start preflight or any
  edit.
- This contract is approved by the release owner before the candidate commit and
  the promotable build. Immediately before that approval the allow-list is
  re-measured and every work order that reached `implemented` since this file
  was written is reported and either added to `gates` or excluded by name.
- Formal validation, released-evaluator `doctor`, managed-root integrity and
  start preflight pass without structure, governance or policy errors.

### Measured readiness at drafting

Measured over `main` at `f605e58` plus this packet, with the exact public 0.6.0
evaluator outside the checkout in isolated mode.

- `validate`: `PASS`, 976 artifacts, 0 errors, 53 pre-existing maintenance
  warnings.
- `doctor`: 0 `FAIL`.
- Hosted lanes at `f605e58` on `main`: `success` on the `push` event for the
  Engineering Harness, Publication Rehearsal and Governor Transition Assessment
  workflows; the Candidate Evidence run is recorded in `WO-RLS-013`'s evidence.

### Exact aggregate verification

**Every figure here is measured over the whole `gates` array, all five
entries.** `VREC-SEH-015` must bind one clean 0.7.1 candidate commit to exactly
the five work orders named in `gates`, to four verification contracts
(`VER-DST-001`, `VER-REB-004`, `VER-REB-006`, `VER-REB-011`), and to five
work-order-keyed evidence paths: the four existing under
`docs/engineering/released-evaluator-boundary/evidence/` plus
`docs/engineering/release-0-7-1/evidence/WO-RLS-013-verification.md`. The
requirement union is six: `REQ-DST-006`, `REQ-REB-011`, `REQ-REB-012`,
`REQ-REB-015`, `REQ-REB-027`, `REQ-REB-028`.

### Candidate qualification

At the exact candidate commit, all with the governing 0.6.0 evaluator outside
the checkout unless stated: `validate` 0 errors; `doctor` 0 `FAIL`; review
preflight `PASS`; `scripts/validate_release_distributions.py` and
`scripts/check_portable_release_surface.py` `PASS`; the candidate's own
`qualify complete-candidate`; the full suites on the workstation on CPython 3.14
and 3.11 and on the hosted Linux lane; the governance migration rehearsal
0.6.0 to 0.7.1 `pass` and compatible; all pull-request lanes `success` at the
candidate head.

### Build of record

The recipe-bound replay (`python -m repository_tools.release_build replay`)
run on a Linux host, two byte-identical producer runs, the bundle manifest
from `scripts/create_release_bundle_manifest.py`, and the hosted
`release-candidate-replay.yml` dispatch on the review ref reproducing the same
digests. A Windows host cannot produce the build of record; the workstation
build runs from WSL Ubuntu.

## Compatibility and migration

0.7.1 changes no artifact schema, no managed policy document and no template.
The standard lock's evaluator table keeps its five fields; the archive pair may
be `null` when the installation recorded none (`REQ-REB-028`). A 0.7.0 or
0.6.0 root reads a 0.7.1-written lock without change. The upgrade packet, the
`--work-order` option of `upgrade`, `MG007` and `se_harness.upgrade_authorization`
are removed (`REQ-REB-027`, `SPEC-REB-012`); any consumer automation that
passed `--work-order` must drop it. The governance-migration rehearsal 0.6.0 to
0.7.1 must read `pass` and compatible at the candidate.

## Security and provenance

The build of record is recipe-bound and digest-pinned (`release/build-recipe.json`,
`release/build-toolchain.lock`); the release record binds the wheel and sdist
digests through a schema-2 distribution table; the publication workflow moves
only verified inert bytes into privileged jobs and the `pypi` environment
remains a separate human decision. `RID022` now fires only on a recorded,
differing archive digest; identity by version and installed-payload digest is
unchanged and remains what every mutation guard proves.

## Promotion policy

- `VREC-SEH-015` verified by the assurance owner on the exact candidate.
- `RLS-SEH-016` prepared by generic `prepare-release`, then bound by
  `scripts/bind_release_distribution.py` to the Linux build of record; the hosted
  replay dispatched on the review ref before the release decision.
- The `released` transition rides its own pull request to `main` and is the
  release owner's act.
- After the record is `released` on `main`: `publish-pypi.yml` dispatched from
  `main` with only `release_record=RLS-SEH-016`; tag `v0.7.1`, GitHub Release,
  `release/0.7` advanced, PyPI publication, Pages deployment, and the alias tag
  `last` moved to `v0.7.1` as for 0.7.0.

## Human approval triggers

- Approval of this contract (release owner) and of `WO-RLS-013` (engineering
  owner), as two distinct decisions.
- Start of `WO-RLS-013`, its completion, the verification of `VREC-SEH-015`,
  the preparation and release of `RLS-SEH-016`, the publication dispatch and the
  `pypi` environment: each a separate decision by its accountable owner.
- Any work order reaching `implemented` with packaged-surface bytes after this
  contract's approval is a stop condition; the remedy is rejection and a
  successor contract, never widening in place.

## Known open questions that do not block this release

- `MG004` still guards release-record preparation (`require_archive`), accepted
  as deviation 1 of `WO-REB-027`; preparing a release from an index-installed
  root needs a wheel-file install.
- `SPEC-RLO-005` rule 37's release-record clause still reads as bootstrap-only;
  amendment owed.
- The candidate-package lane's typed branch (`qualify candidate-package`) runs
  only once a verifier carrying `qualify` is the root; under 0.6.0 the legacy
  bootstrap runs, by rule.

## Rollback criteria and procedure

A published 0.7.1 that fails its post-release observation is not withdrawn from
PyPI; a successor release supersedes it. Before publication, any failed gate
stops the sequence at the record: `RLS-SEH-016` is rejected with the reason and
a successor record is prepared from a fresh candidate. The `last` alias tag is
moved only after the public observation passes.

## Post-release observation window

Within one day of publication: `pip install "se-harness==0.7.1"` into a fresh
venv from the index, `harnessctl identity` and `qualify released-root` on a root
initialized by it, and the adoption of 0.7.1 as this repository's governor by
`harnessctl upgrade . --apply` under an ordinary work order. The adoption is the
release's acceptance test and is recorded in that work order's evidence.
