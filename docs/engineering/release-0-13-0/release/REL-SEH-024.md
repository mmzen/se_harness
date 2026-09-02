+++
id = "REL-SEH-024"
type = "release_contract"
title = "Release se-harness 0.13.0: the designed self-contained Explorer, the delegated route travelled, and the 0.12.0 root"
status = "approved"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-09-02"
updated = "2026-09-02"
previous_release_tag = "v0.12.0"

[relations]
gates = ["WO-DST-023", "WO-ECP-024", "WO-HUP-013", "WO-RLS-019"]

[release_unit]
untraced_exemptions = []

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-02T06:40:19Z"
decided_by = "release-owner"
reason = "Approved by the accountable release owner on 2026-09-02 by selecting the presented option 'Approve REL-SEH-024 and WO-RLS-019, start', as a decision distinct from the work order's approval. The allow-list was re-measured immediately before this approval over main at 75d1902 with the exact public 0.12.0 evaluator outside the checkout: the three implemented, verified, unreleased work orders are exactly the three members named in gates, and no work order reached implemented since the packet was drafted; the census from v0.12.0 reads zero untraced commits and needs no exemption. This approval authorizes WO-RLS-019 to be approved and started as separate acts; it authorizes no candidate, build, record, tag, publication or deployment."
+++

# Release contract: se-harness 0.13.0

## Lifecycle and authority

This contract is a definition. Its approval by the release owner authorizes
`WO-RLS-019` to be approved and started as separate acts; it authorizes no
candidate, build, verification record, release record, tag, publication or
deployment by itself. Every later step is the decision of the role that owns
it, recorded on the artifact it changes. The aggregate verification record
is `VREC-SEH-022`; the release record is `RLS-SEH-022`.

## Release unit

One `se-harness` 0.13.0 release derived from one clean candidate commit cut
from `main`: a recipe-bound reproducible wheel, a normalized source
distribution, a checksum manifest, a schema-2 bound distribution table, an
immutable `v0.13.0` tag, GitHub Release assets, publication of the same
qualified files to PyPI, the canonical `release/0.13` maintenance line
established at the released candidate, a release-bound static Explorer
demonstration, and the `last` alias tag and GitHub "latest" marker moved
to it.

The release-bearing work added after the immutable `v0.12.0` baseline is
exactly these three work orders. Every row was measured on `main` at
`75d1902` as active, `implemented`, holding work-order-keyed evidence,
verified, absent from the `v0.12.0` tree, and unnamed by any released
release record.

| Work order | Outcome | Coverage at drafting |
| --- | --- | --- |
| `WO-HUP-013` | Adopt exact public 0.12.0 as the standard root, the simple way; candidate moved to 0.13.0 | `VREC-HUP-012` verified |
| `WO-ECP-024` | Remove the dead `.gitattributes` tail, by the delegated route: the first work order started, completed and record-prepared by the `delegated-executor` under the green gate | `VREC-ECP-028` verified |
| `WO-DST-023` | Integrate the designed self-contained Explorer as the canonical template: no runtime CDN, the computed indicators and record proof fields, the generator extended | `VREC-DST-020` verified |

`WO-RLS-019` is the fourth member: it qualifies the candidate, takes the
build of record from the hosted pinned producer, and retains the evidence;
the candidate version already reads 0.13.0 (moved by `WO-HUP-013`). It
receives its verified coverage from `VREC-SEH-022`.

The packaged surface changes by exactly two managed template files since
`v0.12.0`, both from `WO-DST-023`:
`templates/repository/standard/scripts/harness_explorer/index.template.html`
and `templates/repository/standard/scripts/generate_harness_dashboard.py`,
plus the version markers in `pyproject.toml`, `se_harness/__init__.py` and
the README install line from `WO-HUP-013`. No evaluator module, contract
JSON, hash-bound class, lock schema, workflow template or skill changes.

### Commit census

`harnessctl release-unit . --from v0.12.0 --to 75d1902` reads seven
first-parent commits, all merge commits GitHub wrote for pull requests,
every one traced through its branch commits' `Harness-Work-Order`
trailers: zero untraced, zero exemptions, `complete: true`.

| Commit | Pull request | Traces | Disposition |
| --- | --- | --- | --- |
| `63889f7` | #304 | `WO-RLS-018`, `WO-ECP-023`, `WO-HUP-012`, `WO-LRE-002`, `WO-REB-031`, `WO-TCM-003` | the 0.12.0 release branch and its five trace commits; all six released by `RLS-SEH-021`, therefore outside `gates` by construction |
| `c8206cb` | #306 | `WO-HUP-013` | member |
| `3f6b553` | #307 | `WO-HUP-013` | `VREC-HUP-012` governance; records of a member |
| `a9180e1` | #308 | `WO-ECP-024` | member's definition packet and delegation |
| `c065e3d` | #309 | `WO-ECP-024` | member's delegated execution and `VREC-ECP-028` |
| `5a93794` | #311 | `WO-DST-023` | member |
| `75d1902` | #312 | `WO-DST-023` | `VREC-DST-020` governance; records of a member |

The derivation reads nine work orders: the three members plus the six
`RLS-SEH-021` released through the #304 merge, which release did not move
out of `implemented` (`WFL-002`). `--contract REL-SEH-024` therefore
reports one `E-CIP-001` finding on `gates` at every stage by construction,
the six released members, as `REL-SEH-023` reported `WO-RLS-017` and
`REL-SEH-022` reported `WO-RLS-016`; and, until the candidate exists, the
absence of `candidate_commit`. No trace repair is needed for this unit.

This contract names no `candidate_commit`: the candidate is created by
`WO-RLS-019` after this approval. `QGP-G5P-RELEASE-UNIT` therefore passes
unmeasured at approval; the census above is the reported evidence, and
`WO-RLS-019` re-runs the derivation at the candidate and records it.

## Required evidence

### Entry criteria

- The three existing members are active, `implemented`, retain
  work-order-keyed evidence, and hold verified assurance coverage. Measured
  at `75d1902`: three of three.
- No existing member is named by a released release record.
- No stale `ready` verification or release record exists in the graph
  beyond the canonical templates.
- `WO-RLS-019` is separately reviewed and approved before start preflight
  or any edit.
- This contract is approved by the release owner before the candidate
  commit and the promotable build. Immediately before that approval the
  allow-list is re-measured and every work order that reached `implemented`
  since this file was written is reported and either added to `gates` or
  excluded by name.
- Formal validation, released-evaluator `doctor`, managed-root integrity
  and start preflight pass without structure, governance or policy errors.

### Measured readiness at drafting

Measured over `main` at `75d1902` plus this packet, with the exact public
0.12.0 evaluator outside the checkout in isolated mode, installed from the
wheel whose SHA-256 `639edbee…` equals the distribution table of
`RLS-SEH-021`.

- `validate`: 1,231 artifacts, 0 errors, 65 pre-existing maintenance
  warnings, 0 advisories.
- `doctor`: 113 `PASS`, 0 `FAIL`.
- Hosted lanes at `75d1902` on `main`: Engineering Harness, SE Harness
  Candidate Evidence, Publication Rehearsal and Governor Transition
  Assessment, all `success`.

### Exact aggregate verification

**Every figure here is measured over the whole `gates` array, all four
entries.** `VREC-SEH-022` must bind one clean 0.13.0 candidate commit to
exactly the four work orders named in `gates`, to six verification
contracts (`VER-DST-001`, `VER-DST-013`, `VER-DST-014`, `VER-DST-023`,
`VER-ECP-020`, `VER-HUP-013`), and to four work-order-keyed evidence
paths: the three members' handoff packets in their domains plus
`WO-RLS-019`'s packet under `docs/engineering/release-0-13-0/evidence/`.
The requirement union is seven: `REQ-DST-006`, `REQ-DST-055`,
`REQ-DST-067`, `REQ-DST-068`, `REQ-ECP-029`, `REQ-HUP-025`, `REQ-HUP-026`.

### Candidate qualification

At the exact candidate commit, all with the governing 0.12.0 evaluator
outside the checkout unless stated: `validate` 0 errors; `doctor` 0 `FAIL`;
review preflight `PASS`; the handoff check over the Git-derived change set;
`scripts/validate_release_distributions.py` and
`scripts/check_portable_release_surface.py` `PASS` in `--repository`,
`--wheel` and `--harnessctl` modes; the candidate's own `qualify
complete-candidate` (read from the hosted Linux lane for the `RID018`
boundary reason, as for `REL-SEH-023`); the full suite on Linux (hosted)
and on Windows (this workstation); the real upgrade rehearsal 0.12.0 to
0.13.0 `pass` on both hosted platforms with agreeing `semantic_sha256`; all
pull-request lanes `success` at the candidate head.

### Build of record

The recipe-bound replay run by the hosted Publication Rehearsal in
`candidate` mode at the candidate head: `.github/workflows/release-qualification.yml`
executes `python -m repository_tools.release_build replay` on the pinned
linux/amd64 producer image through Docker on the GitHub runner, two
byte-identical producer runs, and retains `release-build-replay.json`
whose `manifest` is the schema-2 bundle manifest. That manifest is
downloaded from the run at the candidate head, verified against the
candidate commit, retained as
`docs/engineering/release-0-13-0/evidence/RLS-SEH-022-bundle.json`, and
bound into `RLS-SEH-022`; the hosted `release-candidate-replay.yml`
dispatch on the review ref must then reproduce the same digests from the
bound record. The build is a function of the candidate and the recipe alone
(`REQ-RLO-017`, `WO-RLO-008`); this workstation has no Docker engine, so
the hosted runner is the build host for this unit.

## Compatibility and migration

0.13.0 changes two managed template files and nothing else in the
evaluator; installed copies regenerate on `upgrade`:

- **The designed self-contained Explorer (`WO-DST-023`).** The canonical
  `harness_explorer/index.template.html` is the designed page built from
  retained sources: one bootstrap marker, three script elements, a Content
  Security Policy without any remote origin, the four designed views, the
  shell, and the Readiness view carried forward. No runtime CDN is fetched.
  `generate_harness_dashboard.py` raises `MAX_INDEX_BYTES` to 524,288,
  projects `evaluator_evidence_path`, `evaluator_evidence_sha256` and the
  scalar `[distribution]` table onto record details, carries `path` and
  release `version`, `released_at` and `distribution` on compact topology
  rows, adds the `metrics` object to the summary and a normalized GitHub
  `source_url` to the repository descriptor. The bundle-v2 manifest
  contract, resource prefixes, bundle verifier, Pages workflow and
  `harness-dashboard-snapshot-v1` are unchanged. `REQ-DST-032` and
  `REQ-DST-036` are superseded by `REQ-DST-067`; `SPEC-DST-008`,
  `SPEC-DST-010`, `SPEC-DST-011`, `SPEC-DST-012`, `SPEC-DST-016` and
  `SPEC-DST-017` by `SPEC-DST-023`; their verification contracts stay
  active because verified records bind them.
- **The delegated route travelled (`WO-ECP-024`).** The `.gitattributes`
  change is owner content of this repository; consumers are unaffected.
  The work order is the first to have its start, completion and record
  preparation applied by the `delegated-executor` under the enforced green
  gate, the 0.12.0 delegation class doing the work it was built for.
- **Root identity (`WO-HUP-013`).** This repository's own root moved to
  0.12.0 and the candidate to 0.13.0; consumers are unaffected.

A 0.12.0 root reads a 0.13.0-written lock without change: lock schema 3,
five evaluator fields, the same hash-bound classes. `validate`, `doctor`,
`check`, `transition`, the record commands and the managed lane template
are byte-identical to 0.12.0 in behaviour; the diagnostic-code index is
unchanged.

## Security and provenance

The build of record is recipe-bound and digest-pinned
(`release/build-recipe.json`, `release/build-toolchain.lock`, both
unchanged since `v0.12.0`); the release record binds the wheel and sdist
digests through a schema-2 distribution table; the publication workflow
moves only verified inert bytes into privileged jobs and the `pypi`
environment remains a separate human decision. Identity by version,
installed-payload digest and archive pair is unchanged. The Explorer
page's Content Security Policy names no remote origin, so a generated
dashboard loads nothing from outside its own bundle.

## Promotion policy

- `VREC-SEH-022` verified by the assurance owner on the exact candidate.
- `RLS-SEH-022` prepared by generic `prepare-release` from a wheel-file
  installed 0.12.0 evaluator, then bound by
  `scripts/bind_release_distribution.py` to the build of record; the hosted
  replay dispatched on the review ref before the release decision.
- The `released` transition rides the release pull request to `main` and is
  the release owner's act.
- After the record is `released` on `main`: `publish-pypi.yml` dispatched
  from `main` with only `release_record=RLS-SEH-022`; tag `v0.13.0`, GitHub
  Release, `release/0.13` established, PyPI publication, Pages deployment;
  then `gh release edit v0.13.0 --latest` and the `last` alias tag moved to
  `v0.13.0` after the observation passes.

## Human approval triggers

- Approval of this contract (release owner) and of `WO-RLS-019`
  (engineering owner), as two distinct decisions.
- Start of `WO-RLS-019`, its completion, the verification of
  `VREC-SEH-022`, the preparation and release of `RLS-SEH-022`, the
  publication dispatch and the `pypi` environment: each a separate decision
  by its accountable owner.
- Any work order reaching `implemented` with packaged-surface bytes after
  this contract's approval is a stop condition; the remedy is rejection and
  a successor contract, never widening in place.

## Rollback criteria and procedure

A defect found after publication is repaired forward by a successor
release; a published 0.13.0 is never withdrawn from PyPI. A consumer stays
on 0.12.0 by not upgrading; this repository's root stays on 0.12.0 until a
later adoption work order.

Stop condition: the candidate commit is not an ancestor of the ref being
released, or `harnessctl release-unit --contract REL-SEH-024` reports an
`E-CIP-001` finding beyond the two predicted by construction above. The
remedy is a new contract naming a new candidate, never an in-place edit of
`gates`.

## Post-release observation window

The acceptance in the wild is this repository's adoption of 0.13.0 as its
standard root by an ordinary upgrade work order, after which its own
generated Explorer is the designed self-contained page and the public
demonstration at `mmzen.github.io/se_harness` is regenerated from it.

## Known open questions that do not block this release

- The suite runs hosted on Linux only; Windows readings remain workstation
  readings until a Windows test lane exists.
- Issue #269: the Linux fixture-teardown flake; a re-run is not a defect of
  the candidate.
- The build of record is taken from the hosted candidate-mode replay rather
  than a workstation Docker run; both execute the same interpreter on the
  same pinned image, and the bound-record replay re-proves the digests
  before the release decision.
