+++
id = "REL-SEH-023"
type = "release_contract"
title = "Release se-harness 0.12.0: the assessment executed - ceremony cut, CLI normalized, advisories apart, the compatibility floor, the delegation class, and the missing pages"
status = "draft"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-31"
updated = "2026-08-31"

[relations]
gates = ["WO-AUT-004", "WO-DST-022", "WO-ECP-018", "WO-ECP-019", "WO-ECP-020", "WO-ECP-021", "WO-ECP-022", "WO-ECP-023", "WO-HUP-011", "WO-HUP-012", "WO-LRE-002", "WO-REB-031", "WO-RLS-018", "WO-TCM-003"]

[release_unit]
previous_release_tag = "v0.11.0"
untraced_exemptions = [
  "d42ab2fe017520d2f7b6e66b02e9174d7d0c1f7b",
  "73d13b878aa2516def3d13add9d4172f7875a638",
  "2f91797b7b16825b36b267104cc6c86059b32b9b",
  "11ab2f58e09ed751e9c752bab94bce51c9991b7c",
  "4b29d8a52709037dc43b27ac32624c638b288ea5",
  "8b389d58bdbbdadd39d7ca91d3c6c5a72d39497a",
  "39777aa8646cb442329e0565b7c24dcbe382bd6c",
  "609cb254c05a042fcb28ea6e11f15f08c9337021",
  "5b479f4b19cb63ebb49de7c5c3ae0a804c1bffd9",
  "24110ac614ad0e74482f0f3c4aabe3c6665c616f",
  "8f59e9c9a8d8640e1fe6f28ee4432783fb4942c5",
  "1ba300979ca0bc44c82b7f77c7fe50c3187168cb",
  "4028e727de0f8c308268296d7ba4c183b7eda64b",
  "2761f89058063ceb4d512702344601484c520b22",
]
+++

# Release contract: se-harness 0.12.0

## Lifecycle and authority

This contract is a definition. Its approval by the release owner authorizes
`WO-RLS-018` to be approved and started as separate acts; it authorizes no
candidate, build, verification record, release record, tag, publication or
deployment by itself. Every later step is the decision of the role that owns
it, recorded on the artifact it changes. The aggregate verification record
is `VREC-SEH-021`; the release record is `RLS-SEH-021`.

## Release unit

One `se-harness` 0.12.0 release derived from one clean candidate commit cut
from `main`: a recipe-bound reproducible wheel, a normalized source
distribution, a checksum manifest, a schema-2 bound distribution table, an
immutable `v0.12.0` tag, GitHub Release assets, publication of the same
qualified files to PyPI, the canonical `release/0.12` maintenance line
established at the released candidate, a release-bound static Explorer
demonstration, and the `last` alias tag and GitHub "latest" marker moved
to it.

The release-bearing work added after the immutable `v0.11.0` baseline is
exactly these thirteen work orders — the functional assessment of
2026-08-30 executed. Every row was measured on `main` at `2761f89` as
active, `implemented`, holding work-order-keyed evidence, verified, absent
from the `v0.11.0` tree, and unnamed by any released release record.

| Work order | Outcome | Coverage at drafting |
| --- | --- | --- |
| `WO-HUP-011` | Adopt exact public 0.11.0 as the standard root, the simple way; candidate moved to 0.12.0 | `VREC-HUP-010` verified |
| `WO-ECP-018` | The delegation class: three transitions unlocked by the green pull-request gate | `VREC-ECP-022` verified |
| `WO-DST-022` | Retire managed files that leave the managed set on upgrade (issue #271) | `VREC-DST-019` verified |
| `WO-ECP-019` | Fold `next` into the `check` projection and retire `accept-candidate` | `VREC-ECP-023` verified |
| `WO-ECP-020` | Remove the `next` alias | `VREC-ECP-024` verified |
| `WO-AUT-004` | Report authoring advisories apart from errors and warnings (issue #283) | `VREC-AUT-004` verified |
| `WO-ECP-021` | The managed lane reads the live pull-request body (issue #280) | `VREC-ECP-025` verified |
| `WO-ECP-022` | Normalise the `harnessctl` command shape (issue #282) | `VREC-ECP-026` verified |
| `WO-ECP-023` | The Git-derived handoff check self-binds in one run (issue #280) | `VREC-ECP-027` verified |
| `WO-REB-031` | Remove the expired 0.6.0 bootstrap acceptance path (issue #285a) | `VREC-REB-029` verified |
| `WO-HUP-012` | Enforce the lock-schema floor (issue #285a; closes #224) | `VREC-HUP-011` verified |
| `WO-LRE-002` | Enforce the evaluator-evidence floor (issue #285a; closes #214) | `VREC-LRE-002` verified |
| `WO-TCM-003` | Generate the diagnostic-code index (issue #281b) | `VREC-TCM-003` verified |

`WO-RLS-018` is the fourteenth member: it qualifies and builds the
candidate and retains the evidence; the candidate version already reads
0.12.0 (moved by `WO-HUP-011`). It receives its verified coverage from
`VREC-SEH-021`.

### Commit census

`harnessctl release-unit . --from v0.11.0 --to 2761f89` reads twenty-three
first-parent commits, all merge commits GitHub wrote for pull requests.
Nine trace through their branch commits: `896f8fa` (#270) traces
`WO-RLS-017`, which `RLS-SEH-020` released and which is therefore not a
member; `d3b5a3f` (#272) `WO-HUP-011`; `970a0ae` (#275) `WO-ECP-018`;
`edcef3e` (#276) and `27e40e5` (#278) `WO-DST-022`; `70508cd` (#277)
`WO-ECP-019`; `574e132` (#279) `WO-ECP-020`; `7cac025` (#289)
`WO-AUT-004`; `08193d9` (#292) `WO-ECP-022` and, through the base merges
its branch carried, `WO-ECP-021`.

Fourteen first-parent commits carry no trailer Git parses and are exempted
in `[release_unit].untraced_exemptions`:

| Commit | Pull request | Content | Disposition |
| --- | --- | --- | --- |
| `d42ab2f` | #288 | functional assessment note | documentation, exempted |
| `73d13b8` | #290 | getting started, glossary | documentation, exempted |
| `2f91797` | #291 | notes history move | documentation, exempted |
| `11ab2f5` | #293 | one-commit-record note | documentation, exempted |
| `4b29d8a` | #294 | `WO-ECP-021` chain | member traced through #292; exempted |
| `8b389d5` | #295 | `WO-REB-031` | member restored by trace commit; exempted |
| `39777aa` | #296 | `WO-HUP-012` | member restored by trace commit; exempted |
| `609cb25` | #297 | `VREC-REB-029` governance | records of a member; exempted |
| `5b479f4` | #299 | `WO-ECP-023` | member restored by trace commit; exempted |
| `24110ac` | #298 | `VREC-HUP-011` governance | records of a member; exempted |
| `8f59e9c` | #300 | `WO-LRE-002` | member restored by trace commit; exempted |
| `1ba3009` | #301 | `VREC-LRE-002` governance | records of a member; exempted |
| `4028e72` | #302 | `WO-TCM-003` | member restored by trace commit; exempted |
| `2761f89` | #303 | `VREC-TCM-003` governance | records of a member; exempted |

### Trace repair

The branch commits of #295, #296, #299, #300 and #302 carried their
`Harness-Work-Order` line in a middle paragraph of the commit message,
which Git does not parse as a trailer, so five implemented, verified
members are invisible to the derivation. `WO-RLS-018` records the trace on
its branch: one empty commit per member whose message body names the
delivering pull request and whose final trailer block carries the member's
`Harness-Work-Order` line. Each trace commit changes no file; the member's
packaged bytes entered `main` through the exempted merge it names, and the
member's own lifecycle, evidence and verified record are unchanged. The
derivation at the candidate therefore reads all thirteen members plus the
released `WO-RLS-017` (reported as outside `gates` by construction, as
`WO-RLS-016` was for `REL-SEH-022`) and `WO-RLS-018` itself.

This contract names no `candidate_commit`: the candidate is created by
`WO-RLS-018` after this approval. `QGP-G5P-RELEASE-UNIT` therefore passes
unmeasured at approval; the census above is the reported evidence, and
`WO-RLS-018` re-runs the derivation at the candidate and records it.

## Required evidence

### Entry criteria

- The thirteen existing members are active, `implemented`, retain
  work-order-keyed evidence, and hold verified assurance coverage. Measured
  at `2761f89`: thirteen of thirteen.
- No existing member is named by a released release record.
- No stale `ready` verification or release record exists in the graph
  beyond the canonical templates.
- `WO-RLS-018` is separately reviewed and approved before start preflight
  or any edit.
- This contract is approved by the release owner before the candidate
  commit and the promotable build. Immediately before that approval the
  allow-list is re-measured and every work order that reached `implemented`
  since this file was written is reported and either added to `gates` or
  excluded by name.
- Formal validation, released-evaluator `doctor`, managed-root integrity
  and start preflight pass without structure, governance or policy errors.

### Measured readiness at drafting

Measured over `main` at `2761f89` plus this packet, with the exact public
0.11.0 evaluator outside the checkout in isolated mode, installed from the
digest-verified wheel.

- `validate`: 0 errors, 486 pre-existing maintenance warnings (the root
  validator counts the advisory class as warnings until adoption).
- `doctor`: 0 `FAIL`.
- Hosted lanes at `2761f89` on `main`: all thirteen push-event runs
  `success`.

### Exact aggregate verification

**Every figure here is measured over the whole `gates` array, all fourteen
entries.** `VREC-SEH-021` must bind one clean 0.12.0 candidate commit to
exactly the fourteen work orders named in `gates`, to thirteen verification
contracts (`VER-AUT-002`, `VER-DST-001`, `VER-DST-022`, `VER-ECP-015`,
`VER-ECP-016`, `VER-ECP-017`, `VER-ECP-018`, `VER-ECP-019`, `VER-HUP-011`,
`VER-HUP-012`, `VER-LRE-002`, `VER-REB-015`, `VER-TCM-002`), and to
fourteen work-order-keyed evidence paths: the thirteen members' handoff
packets in their domains plus `WO-RLS-018`'s packet under
`docs/engineering/release-0-12-0/evidence/`. The requirement union is
fourteen: `REQ-AUT-007`, `REQ-DST-006`, `REQ-DST-066`, `REQ-ECP-011`,
`REQ-ECP-025`, `REQ-ECP-026`, `REQ-ECP-027`, `REQ-ECP-028`, `REQ-HUP-022`,
`REQ-HUP-023`, `REQ-HUP-024`, `REQ-LRE-003`, `REQ-REB-031`, `REQ-TCM-005`.

### Candidate qualification

At the exact candidate commit, all with the governing 0.11.0 evaluator
outside the checkout unless stated: `validate` 0 errors; `doctor` 0 `FAIL`;
review preflight `PASS`; `scripts/validate_release_distributions.py` and
`scripts/check_portable_release_surface.py` `PASS` in `--repository`,
`--wheel` and `--harnessctl` modes; the candidate's own `qualify
complete-candidate` (read from the hosted Linux lane for the `RID018`
boundary reason, as for `REL-SEH-022`); the full suite on Linux and on
Windows; the real upgrade rehearsal 0.11.0 to 0.12.0 `pass` on both
platforms with agreeing `semantic_sha256`; all pull-request lanes `success`
at the candidate head.

### Build of record

The recipe-bound replay (`python -m repository_tools.release_build replay`)
run on a host with the pinned linux/amd64 producer image, two
byte-identical producer runs, the bundle manifest from
`scripts/create_release_bundle_manifest.py`, and the hosted
`release-candidate-replay.yml` dispatch on the review ref reproducing the
same digests.

## Compatibility and migration

0.12.0 changes the evaluator, the CLI shape, the installed validator, the
managed lane template and the candidate-evidence lane; installed copies
regenerate on `upgrade`:

- **The lock-schema floor (breaking).** A lock whose schema is 1 or 2 is no
  longer read by any operation, including `doctor` and `upgrade`; the one
  diagnostic names the route — remove the stale lock and re-adopt, protected
  by adopt's non-overwrite behavior. A 0.2.x–0.5.x root can no longer be
  upgraded in place (`WO-HUP-012`, the owner's floor decision of
  2026-08-30).
- **The evaluator-evidence floor.** A released release record carrying
  neither evidence field is not assessed: no error, no `W024`, no
  declaration, no upgrade refusal; `W024` is retired and reserved. A
  partially bound record stays an error. A work order carrying the old
  declaration key stays valid; the key is inert (`WO-LRE-002`).
- **One acceptance path.** The candidate-evidence lane runs the typed
  `qualify candidate-package` unconditionally; the 0.6.0 bootstrap fallback
  and its contract table are gone (`WO-REB-031`).
- **The CLI shape.** Command naming, `--json`, and the exit-code rule are
  normalized; `WEX210` no longer prints its code twice; record-preparation
  refusals carry cause-split codes (`WEX301`–`WEX304`, `WEX401`–`WEX404`);
  a mutation-guard refusal on a record command exits 2 (`WO-ECP-021`,
  `WO-ECP-022`).
- **`next` and `accept-candidate` removed.** Both exit 2 naming their
  replacement (`check`, `qualify candidate-package`); `focus` keeps its
  0.11.0 tombstone (`WO-ECP-019`, `WO-ECP-020`).
- **Advisories apart.** The `W-AUT-*` family is an advisory class, raised
  only on drafts, outside the warning count; the summary carries four
  numbers and `validate --advisories` lists them (`WO-AUT-004`).
- **Ceremony cut.** The Git-derived handoff check self-binds in one run,
  and the managed lane template reads the live pull-request body, so a body
  edit no longer needs a push (`WO-ECP-023`, `WO-ECP-021`).
- **The delegation class.** A work order carrying the `[delegation]` table
  lets a non-human actor start it, complete it and prepare its record while
  the required pull-request check is green; validated by the installed
  validator (`WO-ECP-018`).
- **Upgrades retire departed files.** A managed file the new template no
  longer names is removed by `upgrade` when its bytes match the locked
  digest (`WO-DST-022`).
- **The missing pages.** Getting started, the glossary and the generated
  diagnostic-code index ship in `docs/notes/`; the index is pinned by a
  test (`WO-TCM-003`).
- **Root identity.** This repository's own root moved to 0.11.0
  (`WO-HUP-011`); consumers are unaffected.

A 0.11.0 root reads a 0.12.0-written lock without change (schema 3, five
evaluator fields). Ready records prepared under 0.11.0 report `E012` after
a root advances to 0.12.0 until re-prepared; the upgrade rehearsal
tolerates that by design.

## Security and provenance

The build of record is recipe-bound and digest-pinned
(`release/build-recipe.json`, `release/build-toolchain.lock`); the release
record binds the wheel and sdist digests through a schema-2 distribution
table; the publication workflow moves only verified inert bytes into
privileged jobs and the `pypi` environment remains a separate human
decision. Identity by version, installed-payload digest and archive pair is
unchanged. The floor work removes roughly 1,200 lines of compatibility
machinery reachable from every consumer's installed validator and
evaluator.

## Promotion policy

- `VREC-SEH-021` verified by the assurance owner on the exact candidate.
- `RLS-SEH-021` prepared by generic `prepare-release` from a wheel-file
  installed 0.11.0 evaluator, then bound by
  `scripts/bind_release_distribution.py` to the build of record; the hosted
  replay dispatched on the review ref before the release decision.
- The `released` transition rides the release pull request to `main` and is
  the release owner's act.
- After the record is `released` on `main`: `publish-pypi.yml` dispatched
  from `main` with only `release_record=RLS-SEH-021`; tag `v0.12.0`, GitHub
  Release, `release/0.12` established, PyPI publication, Pages deployment;
  then `gh release edit v0.12.0 --latest` and the `last` alias tag moved to
  `v0.12.0` after the observation passes.

## Human approval triggers

- Approval of this contract (release owner) and of `WO-RLS-018`
  (engineering owner), as two distinct decisions.
- Start of `WO-RLS-018`, its completion, the verification of
  `VREC-SEH-021`, the preparation and release of `RLS-SEH-021`, the
  publication dispatch and the `pypi` environment: each a separate decision
  by its accountable owner.
- Any work order reaching `implemented` with packaged-surface bytes after
  this contract's approval is a stop condition; the remedy is rejection and
  a successor contract, never widening in place.

## Rollback

A defect found after publication is repaired forward by a successor
release; a published 0.12.0 is never withdrawn from PyPI. A consumer stays
on 0.11.0 by not upgrading; this repository's root stays on 0.11.0 until a
later adoption work order.

## Observation window

The acceptance in the wild is this repository's adoption of 0.12.0 as its
standard root by an ordinary upgrade work order (issue #284), after which
its own gate counts advisories apart, the managed lane reads the live
pull-request body, the handoff check self-binds, and — with branch
protection enabled — the delegation class does the work it was built for.

## Known open questions that do not block this release

- The suite runs hosted on Linux only; Windows readings remain workstation
  readings until a Windows test lane exists.
- Issue #269: the Linux fixture-teardown flake; a re-run is not a defect of
  the candidate.
- The commit-trailer form that made five merges untraced is a working
  convention, not a contract; the trace-repair pattern above is the
  recorded remedy for this unit.
