+++
id = "REL-SEH-021"
type = "release_contract"
title = "Release se-harness 0.10.0: the 0.9.0 root adopted, and the three defects it exposed repaired"
status = "approved"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
gates = ["WO-ECP-012", "WO-ECP-013", "WO-ECP-014", "WO-HUP-009", "WO-RLS-016"]

[release_unit]
previous_release_tag = "v0.9.0"
untraced_exemptions = ["aa997739a35bf44fa9af63aade591bf84b6310dc", "1d19d17c0d98458dffd480536071d27bddd9f976", "741a7743c35e68469a1e20835b20dcfd01e3b471", "3139f245fecb247ffadf944a9a3fc5f7270e6ce6"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T09:38:46Z"
decided_by = "release-owner"
reason = "Approved by the accountable release owner on 2026-08-29, 'Approve REL-SEH-021 and WO-RLS-016, start', as a decision distinct from the work order's approval. The allow-list was re-measured immediately before this transition over main 3139f24 plus this packet: the four existing members WO-HUP-009, WO-ECP-012, WO-ECP-013 and WO-ECP-014 are implemented and verified, no other work order reached implemented since the contract was drafted, and none is named by a released record. Readings under the governing exact public 0.9.0 root: validate PASS at 0 errors, doctor 0 FAIL, every push-event workflow green at 3139f24. The commit census reports four untraced merges, exempted by name, and the traced 0.9.0 record merge that names the released WO-RLS-015 by construction. This approval authorizes WO-RLS-016 to be approved and started as separate acts and nothing else."
+++

# Release contract: se-harness 0.10.0

## Lifecycle and authority

This contract is a definition. Its approval by the release owner authorizes
`WO-RLS-016` to be approved and started as separate acts; it authorizes no
candidate, build, verification record, release record, tag, publication or
deployment by itself. Every later step is the decision of the role that owns
it, recorded on the artifact it changes. The aggregate verification record
is `VREC-SEH-019`; the release record is `RLS-SEH-019`.

## Release unit

One `se-harness` 0.10.0 release derived from one clean candidate commit cut
from `main`: a recipe-bound reproducible wheel, a normalized source
distribution, a checksum manifest, a schema-2 bound distribution table, an
immutable `v0.10.0` tag, GitHub Release assets, publication of the same
qualified files to PyPI, the canonical `release/0.10` maintenance line
established at the released candidate, and a release-bound static Explorer
demonstration.

The release-bearing work added after the immutable `v0.9.0` baseline is
exactly these four work orders. Every row was measured on `main` at
`3139f24` as active, `implemented`, holding work-order-keyed evidence,
verified, absent from the `v0.9.0` tree, and unnamed by any released release
record.

| Work order | Outcome | Coverage at drafting |
| --- | --- | --- |
| `WO-HUP-009` | Adopt exact public 0.9.0 as the standard root, the simple way; candidate moved to 0.10.0 | `VREC-HUP-008` verified |
| `WO-ECP-012` | Resolve the evaluator's own artifact path on every host (issue #254); the `harnessctl check` reference | `VREC-ECP-015` verified |
| `WO-ECP-013` | The `scope` checkpoint, so the managed pull-request gate is green in every lifecycle state (issue #255) | `VREC-ECP-016` verified |
| `WO-ECP-014` | The line-ending-canonical formal snapshot (issue #256) | `VREC-ECP-017` verified |

`WO-RLS-016` is the fifth member: it qualifies and builds the candidate and
retains the evidence; the candidate version already reads 0.10.0 (moved by
`WO-HUP-009`). It receives its verified coverage from `VREC-SEH-019`.

Packaged-surface bytes in the unit come from `WO-HUP-009` (version
identity), `WO-ECP-012` (`artifact_layout.py`, `workflow_compliance.py`),
`WO-ECP-013` (`workflow_contract.py`, `workflow_compliance.py`,
`workflow_procedures.py`, `cli.py`, `quality_gates_contract.json` and the
template `QUALITY_GATES.json`/`.md`, `WORKFLOW.md`, the managed workflow, the
pull-request seed) and `WO-ECP-014` (`workflow_compliance.py`).

### Commit census

`harnessctl release-unit . --from v0.9.0 --to 3139f24` reads five
first-parent commits, all merge commits GitHub wrote for pull requests. One,
`7291602` (#252), carries a parseable `Harness-Work-Order: WO-RLS-015`
trailer and traces the 0.9.0 release work order, which `RLS-SEH-018`
released and which is therefore not a member; the other four carry no
trailer, while the branch commits behind each carry it in one final
paragraph, which the first-parent walk does not visit. The four are
exempted in `[release_unit].untraced_exemptions` for the reasons below; the
traced `7291602` cannot be exempted (an exemption covers only a commit
without a trailer) and stays in the derivation, so the contract comparison
reports `WO-RLS-015` as missing from `gates` by construction. It is
excluded from the unit because `RLS-SEH-018` released it, and that finding
is recorded evidence, not a defect, at approval and at the candidate. The
membership above is established by the allow-list and by each member's own
lifecycle state and evidence, as the 0.9.0 contract did for its merges.

| Commit | Pull request | Reason |
| --- | --- | --- |
| `7291602` | #252 | merge of the 0.9.0 release record; traced to `WO-RLS-015`, released by `RLS-SEH-018`, not a member, not exemptable |
| `aa99773` | #253 | merge of `WO-HUP-009`'s branch; GitHub merge commit, no trailer |
| `1d19d17` | #257 | merge of `WO-ECP-012`'s branch; same |
| `741a774` | #258 | merge of `WO-ECP-013`'s branch; same |
| `3139f24` | #259 | merge of `WO-ECP-014`'s branch; same |

This contract names no `candidate_commit`: the candidate is created by
`WO-RLS-016` after this approval. `QGP-G5P-RELEASE-UNIT` therefore passes
unmeasured at approval, as for `REL-SEH-020`; the census above is the
reported evidence, and `WO-RLS-016` re-runs the derivation at the candidate
and records it, expecting the same four exemptions, `WO-RLS-015` traced and
excluded, and `WO-RLS-016` traced.

## Required evidence

### Entry criteria

- The four existing members are active, `implemented`, retain
  work-order-keyed evidence, and hold verified assurance coverage. Measured
  at `3139f24`: four of four.
- No existing member is named by a released release record.
- No stale `ready` verification or release record exists in the graph beyond
  the two canonical templates. Measured at `3139f24`: none.
- `WO-RLS-016` is separately reviewed and approved before start preflight or
  any edit.
- This contract is approved by the release owner before the candidate commit
  and the promotable build. Immediately before that approval the allow-list is
  re-measured and every work order that reached `implemented` since this file
  was written is reported and either added to `gates` or excluded by name.
- Formal validation, released-evaluator `doctor`, managed-root integrity and
  start preflight pass without structure, governance or policy errors.

### Measured readiness at drafting

Measured over `main` at `3139f24` plus this packet, with the exact public
0.9.0 evaluator outside the checkout in isolated mode.

- `validate`: 0 errors, 475 pre-existing maintenance warnings.
- `doctor`: 0 `FAIL`.
- Hosted lanes at `3139f24` on `main`: every push-event workflow `success`.

### Exact aggregate verification

**Every figure here is measured over the whole `gates` array, all five
entries.** `VREC-SEH-019` must bind one clean 0.10.0 candidate commit to
exactly the five work orders named in `gates`, to five verification
contracts (`VER-DST-001`, `VER-ECP-008`, `VER-ECP-009`, `VER-ECP-010`,
`VER-HUP-009`), and to five work-order-keyed evidence paths: the four
members' handoff packets listed in the domain index plus
`docs/engineering/release-0-10-0/evidence/WO-RLS-016-verification.md`. The
requirement union is six: `REQ-DST-006`, `REQ-ECP-019`, `REQ-ECP-020`,
`REQ-ECP-021`, `REQ-HUP-018`, `REQ-HUP-019`.

### Candidate qualification

At the exact candidate commit, all with the governing 0.9.0 evaluator outside
the checkout unless stated: `validate` 0 errors; `doctor` 0 `FAIL`; review
preflight `PASS`; `scripts/validate_release_distributions.py` and
`scripts/check_portable_release_surface.py` `PASS` in `--repository`,
`--wheel` and `--harnessctl` modes; the candidate's own `qualify
complete-candidate`; the full suite on Linux and on Windows; the real upgrade
rehearsal 0.9.0 to 0.10.0 `pass` on both platforms with agreeing
`semantic_sha256`; all pull-request lanes `success` at the candidate head,
the managed lane's red after the completion transition excepted as issue
#255 on the 0.9.0 root.

### Build of record

The recipe-bound replay (`python -m repository_tools.release_build replay`)
run on a host with the pinned linux/amd64 producer image, two byte-identical
producer runs, the bundle manifest from
`scripts/create_release_bundle_manifest.py`, and the hosted
`release-candidate-replay.yml` dispatch on the review ref reproducing the same
digests.

## Compatibility and migration

0.10.0 changes the evaluator, the packaged quality-gates contract, one
managed workflow, one managed policy document and one seed; installed copies
regenerate on `upgrade`:

- **Windows.** `harnessctl evidence` and every `harnessctl check` that
  builds a checkpoint context work on Windows again (`WO-ECP-012`, issue
  #254); a `str` path containing a backslash is still refused as untrusted
  text.
- **The `scope` checkpoint.** `harnessctl check --checkpoint scope`
  evaluates only `QGP-G4I-SCOPE`, `QGP-G4I-COMPLETE` and `QGP-G4I-PATHS` of
  `QG-G4-IMPLEMENTATION-EVIDENCE` for a work order in any lifecycle state;
  the gate and its predicates declare the checkpoint in `QUALITY_GATES.json`
  and no identifier or evaluator moves. The managed workflow runs the scope
  check on every pull request and the handoff check with the
  `Harness-Restitution` comparison only while the work order is
  `in_progress`; after completion a declared digest is reported as bound at
  handoff and not recomputed. A consumer's pull request that carries its own
  completion and verification is green when its diff is inside scope, and a
  packet-only pull request is scope-checked for the first time (`WO-ECP-013`,
  issue #255). `harnessctl evidence` keeps four checkpoints.
- **The formal snapshot** is computed over line-ending-canonical
  (`utf8-text-lf-v1`) artifact bytes; on an LF tree every digest is
  unchanged, so no packet header or verification record moves; a packet
  bound on a CRLF checkout now matches the runner (`WO-ECP-014`, issue
  #256).
- **Documentation.** `docs/notes/harnessctl-check.md` is the reference for
  `check` (repository content, not a managed file).

A 0.9.0 root reads a 0.10.0-written lock without change (schema 3, five
evaluator fields). The canonical block and `result_sha256` preimage are
unchanged. Ready records prepared under 0.9.0 report `E012` after a root
advances to 0.10.0 until re-prepared; the upgrade rehearsal tolerates that
by design.

## Security and provenance

The build of record is recipe-bound and digest-pinned
(`release/build-recipe.json`, `release/build-toolchain.lock`); the release
record binds the wheel and sdist digests through a schema-2 distribution
table; the publication workflow moves only verified inert bytes into
privileged jobs and the `pypi` environment remains a separate human decision.
Identity by version, installed-payload digest and archive pair is unchanged.
The scope checkpoint writes nothing; the canonical snapshot changes no
stored digest on an LF tree.

## Promotion policy

- `VREC-SEH-019` verified by the assurance owner on the exact candidate.
- `RLS-SEH-019` prepared by generic `prepare-release` from a wheel-file
  installed 0.9.0 evaluator (the lock carries the archive pair since
  `WO-HUP-009`), then bound by `scripts/bind_release_distribution.py` to the
  build of record; the hosted replay dispatched on the review ref before the
  release decision.
- The `released` transition rides its own pull request to `main` and is the
  release owner's act.
- After the record is `released` on `main`: `publish-pypi.yml` dispatched from
  `main` with only `release_record=RLS-SEH-019`; tag `v0.10.0`, GitHub
  Release, `release/0.10` established, PyPI publication, Pages deployment,
  and the alias tag `last` moved to `v0.10.0` after the observation passes.

## Human approval triggers

- Approval of this contract (release owner) and of `WO-RLS-016` (engineering
  owner), as two distinct decisions.
- Start of `WO-RLS-016`, its completion, the verification of `VREC-SEH-019`,
  the preparation and release of `RLS-SEH-019`, the publication dispatch and
  the `pypi` environment: each a separate decision by its accountable owner.
- Any work order reaching `implemented` with packaged-surface bytes after this
  contract's approval is a stop condition; the remedy is rejection and a
  successor contract, never widening in place.

## Rollback

A defect found after publication is repaired forward by a successor release;
a published 0.10.0 is never withdrawn from PyPI. A consumer stays on 0.9.0
by not upgrading; this repository's root stays on 0.9.0 until a later
adoption work order.

## Observation window

The acceptance in the wild is this repository's adoption of 0.10.0 as its
standard root by an ordinary upgrade work order (`WO-HUP-010`), after which
its own pull requests run the state-independent gate, its Windows checkout
binds evidence packets directly, and the WSL clone route retires. That
adoption and the first pull request governed by the new lane are
`VER-ECP-009` scenario 6.

## Known open questions that do not block this release

- `harnessctl release-unit` walks the first-parent path and reads trailers
  only, so GitHub merge commits are untraced by construction and are
  exempted by name on every release; a later ordinary work order may let the
  derivation follow a merge to its second parent's trailers.
- The suite runs hosted on Linux only; Windows readings remain workstation
  readings until a Windows test lane exists.
