+++
id = "REL-SEH-028"
type = "release_contract"
title = "Release se-harness 0.17.0: the code-health programme, the risk artifact, the honest configuration and the hardened managed workflow"
status = "draft"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-09-09"
updated = "2026-09-09"
previous_release_tag = "v0.16.0"

[relations]
gates = [
  "WO-AUT-005",
  "WO-CIP-007",
  "WO-DST-025",
  "WO-DST-026",
  "WO-ECP-027",
  "WO-ECP-028",
  "WO-ECP-029",
  "WO-ECP-030",
  "WO-ECP-031",
  "WO-ECP-032",
  "WO-ECP-033",
  "WO-ECP-034",
  "WO-ECP-035",
  "WO-ECP-036",
  "WO-HUP-017",
  "WO-RSK-010",
  "WO-TST-004",
  "WO-RLS-023",
]

[release_unit]
untraced_exemptions = [
  "008c7b9819df62d1b0bb50f3ac6858a78ca7d1f3",
  "13a70218c95593bba6d349af65f048dd7ed48ce8",
  "2b1ffd2486ff464b701741f745bc597265b66140",
  "46eff4668adc6c1d37637862202ed43d51544a6e",
  "3a311d49f8052bfa0d09ec92ede460ed73397caa",
  "517dc5f6a72f80264b59d59d96de0c6e59cd379e",
]
+++

# Release contract: se-harness 0.17.0

## Lifecycle and authority

This contract is a definition. Its approval by the release owner authorizes
`WO-RLS-023` to be approved and started as separate acts; it authorizes no
candidate, build, verification record, release record, tag, publication or
deployment by itself. Every later step is the decision of the role that owns
it, recorded on the artifact it changes. The aggregate verification record
is `VREC-SEH-026`; the release record is `RLS-SEH-026`.

This contract was drafted on 2026-09-09 on the repository owner's
instruction "prepare release 0.17.0", with `main` at `4ea947be` and no work
order in progress. Every member whose assurance is `required` holds a
verified record. A member that reaches `implemented` after approval is a
stop condition, never a widening in place.

## Release unit

One `se-harness` 0.17.0 release derived from one clean candidate commit cut
from `main`: a recipe-bound reproducible wheel, a normalized source
distribution, a checksum manifest, a schema-2 bound distribution table, an
immutable `v0.17.0` tag, GitHub Release assets, publication of the same
qualified files to PyPI, the canonical `release/0.17` maintenance line
established at the released candidate, a release-bound static Explorer
demonstration, and the `last` alias tag and GitHub "latest" marker moved
to it.

The release-bearing work added after the immutable `v0.16.0` baseline is
seventeen work orders. They were measured on `main` at `4ea947be` as
active, `implemented`, holding work-order-keyed evidence, absent from the
`v0.16.0` tree, and unnamed by any released release record. Every one has
assurance `required` and holds verified coverage of its own.

| Work order | Outcome | Coverage at drafting |
| --- | --- | --- |
| `WO-HUP-017` | Adopt exact public 0.16.0 as the standard root, the simple way; the eight retired `scripts/` copies leave through the leaving-set rule; the candidate moved to 0.17.0 | `VREC-HUP-016` verified |
| `WO-DST-025` | The installed configuration holds five keys, each read by a named part of the harness; `schema_version` and the inert `[revision_provenance]` keys are gone (`DEC-DST-001`) | `VREC-DST-022` verified |
| `WO-ECP-027` | Wave 0 correctness: uniform exit codes, one code per refusal line, the mutation guard a `HarnessError`, bounded engine launches, no reachable traceback | `VREC-ECP-031` verified |
| `WO-ECP-028` | Wave 1, group A: dead code, orphan fixtures, dead configuration and unconsumed workflow outputs deleted | `VREC-ECP-034` verified |
| `WO-ECP-029` | Wave 1, group B: the `adopt` alias removed after its one release; `init` is the one installation command | `VREC-ECP-032` verified |
| `WO-ECP-030` | Wave 1, group C: `renumber-artifacts`, `rehearse-recovery` and the unwired journalled apply retired; the two unreachable contract entries removed from the candidate templates | `VREC-ECP-033` verified |
| `WO-RSK-010` | The risk artifact: `raise-risk`, the five-by-five score, the paired decision that blocks the threatened artifacts, `decide` disposing the risks it concerns, `risks` listing the threats; the managed `RISK.template.md` | `VREC-RSK-010` verified |
| `WO-ECP-031` | Wave 2, group A: one process launcher (`_process`) and one front-matter parser (`front_matter`) | `VREC-ECP-035` verified |
| `WO-ECP-032` | Wave 2, group B: the integrity primitives, the closed sets and the two grammars defined once | `VREC-ECP-036` verified |
| `WO-ECP-033` | Wave 2, group C: the diagnostic-code registry (`codes.py`, `CodedError`) and the four contract tables read at run time | `VREC-ECP-037` verified |
| `WO-TST-004` | Wave 4: every test discovered once, five shared support modules, one retired-surface table | `VREC-TST-004` verified |
| `WO-ECP-034` | Wave 3, group A: `se_harness/engine/` an import surface, its five twins folded into the package, the 73 engine codes in the registry | `VREC-ECP-038` verified |
| `WO-ECP-035` | Wave 3, group B: one validation per governance command; the report travels; preflight reports skew apart | `VREC-ECP-039` verified |
| `WO-ECP-036` | Wave 3, group C: the validator, the generator and the compliance module split along their seams; no private cross-module import; no function above complexity 60 | `VREC-ECP-040` verified |
| `WO-AUT-005` | Wave 5, corpus: fifteen architectures on typed relations with decision assessments, 271 requirements on the closed verification-method vocabulary, the one-shot script retired | `VREC-AUT-005` verified |
| `WO-CIP-007` | Wave 5, CI: one qualification per pull request, every action pinned by commit, one toolchain block, the lanes renamed after what they do | `VREC-CIP-007` verified |
| `WO-DST-026` | Wave 5, templates: the managed workflow surfaces the evaluator's refusal, names its steps and pins its actions; the `.gitignore` block takes hash markers | `VREC-DST-023` verified |

`WO-RLS-023` is the eighteenth member: it qualifies the candidate, takes the
build of record from the hosted pinned producer, and retains the evidence;
the candidate version already reads 0.17.0 (moved by `WO-HUP-017`). It
receives its verified coverage from `VREC-SEH-026`.

### What this release is for

0.17.0 is the release of the code-health programme (issues #375 to #381,
waves 0 to 5) and of the risk artifact. Since `v0.16.0` the packaged surface
changed in 64 paths as Git reads them with rename detection: the package
gains `_process.py`, `front_matter.py`, `codes.py`, `risks.py`,
`repository_graph.py`, `workflow_edges.py` and the three compliance seams,
the engine gains its nine validator seams and its two generator seams and
loses `artifact_layout_registry.py`; `renumber.py`, `recovery_rehearsal.py`
and `journaled_apply.py` are deleted; the CLI loses `adopt`,
`renumber-artifacts` and `rehearse-recovery` and gains `raise-risk` and
`risks`; every refusal follows the exit-code reference; the standard
template's `.engineering-harness.toml.tpl` holds five keys, its
`engineering-harness.yml` captures the evaluator's refusal and pins its
actions, its `QUALITY_GATES` and `WORKFLOW` tables lose two unreachable
entries, and `RISK.template.md` is new; `pyproject.toml` reads 0.17.0 and
drops the dead `[tool.unittest]` table. Every recorded engine output is
byte-identical across the three groups of wave 3 by the method their records
retain.

For this repository the release is the precondition of the adoption that
moves the root to 0.17.0, after which the in-tree `doctor` and the managed
workflow read the hardened template and the five-key configuration, and of
the delegated start of `WO-TCM-011`, whose own constraint was met when
`WO-HUP-017` adopted 0.16.0 and which the owner may start at any time after
this release is bound.

### Commit census

`harnessctl release-unit . --from v0.16.0 --to 4ea947be` reads 35
first-parent commits, all merge commits GitHub wrote for pull requests.
Seventeen work orders are traced through their branch commits'
`Harness-Work-Order` trailers. Six commits carry no trailer: the pull
requests #391 (the risk-management packet defining `WO-RSK-010`), #401 (the
test-suite packet defining `WO-TST-004`), #409, #410 and #411 (the wave 5
packets defining `WO-CIP-007`, `WO-DST-026` and `WO-AUT-005`), each touching
its domain's definitions only, and #402, the execution of `WO-TST-004`, whose
governance commits carry no trailer although its work order is implemented
and verified. The five packet merges are exempted above by the release
owner's decision, with the reason that a definition packet is traced by the
execution merge of the work order it defines; #402 is exempted with the
reason that its work order enters this unit as a member by name, and
`WO-RLS-023` repairs its trace on the release branch with one empty commit
carrying `Harness-Work-Order: WO-TST-004`, so that the derivation at the
candidate reads `WO-TST-004` through the first-parent path. With those six
exemptions the census yields seventeen traced work orders, of which sixteen
are members; with the trace repair it yields eighteen, of which seventeen
are members.

| Traced work order | Pull request(s) | Disposition |
| --- | --- | --- |
| `WO-RLS-022` | #369 | the 0.16.0 release branch; released by `RLS-SEH-025`, therefore outside `gates` by construction |
| `WO-HUP-017` | #370, #371 | member |
| `WO-DST-025` | #373 | member |
| `WO-ECP-027` | #382, #383 | member |
| `WO-ECP-028` | #386, #393 | member |
| `WO-ECP-029` | #387, #390 | member |
| `WO-ECP-030` | #388, #392 | member |
| `WO-RSK-010` | #394 | member (its packet #391 exempted) |
| `WO-ECP-031` | #395, #398, #403 | member |
| `WO-ECP-032` | #396, #399 | member |
| `WO-ECP-033` | #397, #400 | member |
| `WO-TST-004` | #402 (untraced, exempted; traced by the repair commit) | member |
| `WO-ECP-034` | #404, #407 | member |
| `WO-ECP-035` | #405, #412 | member |
| `WO-ECP-036` | #406, #414 | member |
| `WO-AUT-005` | #413 | member (its packet #411 exempted) |
| `WO-CIP-007` | #419 | member (its packet #409 exempted) |
| `WO-DST-026` | #420 | member (its packet #410 exempted) |

`WO-TCM-011` is `approved` and unstarted; its packet #366 merged before
`v0.16.0`, so no commit of this range traces it and the derivation does not
read it. Its own constraint, execution after `RLS-SEH-025` is released and
adopted as this repository's root, was met by `WO-HUP-017`. It is outside
this unit because it has no commit in the range; `WO-TCM-011` reaching
`in_progress` or `implemented` before the candidate is bound is a stop
condition for this contract, exactly as `REL-SEH-027` stated for the
previous release.

`harnessctl release-unit . --from v0.16.0 --to 4ea947be --contract
REL-SEH-028`, with each of the six exempted commits also passed as
`--exempt` (the command reads exemptions from its flags; the array above is
what the approval gate reads), derives untraced 0, exempted 6, and reports
the `E-CIP-001` findings this contract predicts by construction: the `gates`
difference, the released `WO-RLS-022` present in the derivation,
`WO-TST-004` absent from it until the trace repair, and `WO-RLS-023` not yet
derivable because its commits do not exist, as `REL-SEH-027` reported
`WO-RLS-022`; and, until the candidate exists, the absence of
`candidate_commit`. No other trace repair is needed.

This contract names no `candidate_commit`: the candidate is created by
`WO-RLS-023` after this approval. `QGP-G5P-RELEASE-UNIT` therefore passes
unmeasured at approval; the census above is the reported evidence, and
`WO-RLS-023` re-runs the derivation at the candidate and records it.

## Required evidence

### Entry criteria

- Every existing member is active, `implemented`, retains work-order-keyed
  evidence, and every member whose assurance is `required` holds verified
  coverage. Measured at `4ea947be`: seventeen of seventeen required
  members.
- No existing member is named by a released release record.
- No stale `ready` verification or release record exists in the graph
  beyond the canonical templates.
- No work order is `in_progress` on `main`; `WO-TCM-011` is `approved` and
  unstarted.
- `WO-RLS-023` is separately reviewed and approved before start preflight
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

Measured over `main` at `4ea947be` plus this packet, with the exact public
0.16.0 evaluator outside the checkout in isolated mode, installed from the
wheel whose SHA-256 `a969d6ab…` equals the distribution table of
`RLS-SEH-025`.

- `validate --advisories`: 1,433 artifacts, 0 errors, 44 pre-existing
  maintenance warnings, 0 advisories.
- `doctor`: 97 `PASS`, 0 `FAIL`, 44 `W013` location warnings on
  historical records.
- Hosted lanes at `4ea947be` on `main`: Engineering Harness, SE Harness
  Candidate Evidence, Publication Rehearsal and Predecessor Evaluator
  Assessment, all `success`.

### Exact aggregate verification

**Every figure here is measured over the whole `gates` array, all eighteen
entries.** `VREC-SEH-026` must bind one clean 0.17.0 candidate commit to
exactly the eighteen work orders named in `gates`, to twelve verification
contracts (`VER-AUT-003`, `VER-CIP-003`, `VER-DST-001`, `VER-DST-026`,
`VER-DST-027`, `VER-ECP-023`, `VER-ECP-024`, `VER-ECP-025`, `VER-ECP-026`,
`VER-HUP-017`, `VER-RSK-010`, `VER-TST-002`; the three groups of each of
waves 1, 2 and 3 share theirs), and to eighteen work-order-keyed evidence
paths: each member's handoff packet in its domain plus `WO-RLS-023`'s packet
under `docs/engineering/release-0-17-0/evidence/`. The requirement union of
the seventeen content members is twenty; with `REQ-DST-006` from
`WO-RLS-023` it is twenty-one.

### Candidate qualification

At the exact candidate commit, all with the governing 0.16.0 evaluator
outside the checkout unless stated: `validate` 0 errors; `doctor` 0 `FAIL`;
review preflight `PASS`; the handoff check over the Git-derived change set;
`scripts/validate_release_distributions.py` and
`scripts/check_portable_release_surface.py` `PASS` in `--repository`,
`--wheel` and `--harnessctl` modes; the candidate's own `qualify
complete-candidate` (read from the hosted Linux lane for the `RID018`
boundary reason); the full suite on Linux (hosted) and on Windows (this
workstation, `PYTHONUTF8=1`); the real upgrade rehearsal 0.16.0 to 0.17.0
`pass` on both hosted platforms with agreeing `semantic_sha256`; all
pull-request lanes `success` at the candidate head. Since `WO-CIP-007` the
SE Harness Candidate Evidence lane is the one lane that qualifies the
complete candidate graph and runs the suite for the commit under review, and
its `upgrade-rehearsal` job is the migration reading.

### Build of record

The recipe-bound replay run by the hosted Publication Rehearsal in
`candidate` mode, dispatched on `release/0.17.0` at the candidate head
(the pull-request event builds the merge commit, not the head):
`release-qualification.yml` executes `python -m repository_tools.release_build replay`
on the pinned linux/amd64 producer image through Docker on the GitHub
runner, two byte-identical producer runs, and retains
`release-build-replay.json` whose `manifest` is the schema-2 bundle
manifest. That manifest is downloaded from the run at the bound candidate,
its `candidate.commit` checked equal, retained as
`docs/engineering/release-0-17-0/evidence/RLS-SEH-026-bundle.json`, and
bound into `RLS-SEH-026`; the hosted `release-candidate-replay.yml`
dispatch on the review ref must then reproduce the same digests from the
bound record, as `WO-RLS-022` did for 0.16.0.

## Compatibility and migration

0.17.0 changes the command surface, the exit codes and three managed
template families. `upgrade` from 0.16.0 rewrites the managed
`engineering-harness.yml` (the refusal-surfacing steps, the named header,
the pinned actions), `QUALITY_GATES.json`, `QUALITY_GATES.md`,
`WORKFLOW.json`, `WORKFLOW.md`, `TRACEABILITY.md` and the templates
`README.md`, adds `RISK.template.md`, and rewrites the `.gitignore` block
between hash markers through the existing fragment rule; the installed
`.engineering-harness.toml` keeps the five keys the tool reads and the
installer carries the two values it preserves across an upgrade. Owner
content is untouched; a customized managed file blocks the upgrade as always.
A script that says `harnessctl adopt`, `renumber-artifacts` or
`rehearse-recovery` is refused by the parser as an unknown command, exit 2;
`init` is the installation command. A caller that read exit codes must
expect the reference's two rules: a guard refusal exits 2 on `transition` as
on its siblings, and a syntax error in `--set`, `--decision` or `--reason` is
a usage refusal. `validate`, `dashboard` and `inspect` produce the same
verdicts and the same files, byte for byte, as the wave 3 records retain;
the engine's modules stay runnable with `python -m se_harness.engine.<name>`.
No existing artifact needs to change: the risk type is additive, the
compatibility windows for the retired `constrains` relation and the string
`verification_method` stand as `SPEC-AUT-001` records them, and a 0.16.0 root
reads a 0.17.0-written lock without change.

## Security and provenance

The build of record is recipe-bound and digest-pinned
(`release/build-recipe.json` `0c3f368c…`, `release/build-toolchain.lock`
`826d70d4…`, both unchanged since `v0.12.0`); the release record binds the
wheel and sdist digests through a schema-2 distribution table; the
publication workflow moves only verified inert bytes into privileged jobs
and the `pypi` environment remains a separate human decision. Identity by
version, installed-payload digest and archive pair is unchanged. Every
public action in the repository's workflows is pinned to a commit with its
tag (`WO-CIP-007`); the portable release surface check covers
`pyproject.toml`, which drops one dead table and moves nothing.

## Promotion policy

- `VREC-SEH-026` verified by the assurance owner on the exact candidate.
- `RLS-SEH-026` prepared by generic `prepare-release` from a wheel-file
  installed 0.16.0 evaluator, then bound by
  `scripts/bind_release_distribution.py` to the build of record; the hosted
  replay dispatched on the review ref before the release decision.
- The `released` transition rides the release pull request to `main` and is
  the release owner's act.
- After the record is `released` on `main`: `publish-pypi.yml` dispatched
  from `main` with only `release_record=RLS-SEH-026`; tag `v0.17.0`, GitHub
  Release, `release/0.17` established, PyPI publication, the Pages
  deployment; then `gh release edit v0.17.0 --latest` and the `last` alias
  tag moved to `v0.17.0` after the observation passes.

## Human approval triggers

- Approval of this contract (release owner) and of `WO-RLS-023`
  (engineering owner), as two distinct decisions, after the census has been
  re-measured.
- Start of `WO-RLS-023`, its completion, the verification of
  `VREC-SEH-026`, the preparation and release of `RLS-SEH-026`, the
  publication dispatch and the `pypi` environment: each a separate decision
  by its accountable owner.
- Any work order reaching `implemented` with packaged-surface bytes after
  this contract's approval, and `WO-TCM-011` leaving `approved` before the
  candidate is bound, are stop conditions; the remedy is rejection and a
  successor contract, never widening in place.

## Rollback criteria and procedure

A defect found after publication is repaired forward by a successor
release; a published 0.17.0 is never withdrawn from PyPI. A consumer stays
on 0.16.0 by not upgrading; its managed workflow and templates simply stay
in place.

Stop condition: the candidate commit is not an ancestor of the ref being
released, or `harnessctl release-unit --contract REL-SEH-028` reports an
`E-CIP-001` finding beyond the `gates` difference and the incompleteness
predicted by construction above. The remedy is a new contract naming a new
candidate, never an in-place edit of `gates`.

## Post-release observation window

Within one week of publication: a fresh repository initialised from the
published 0.17.0 wheel holds a five-key `.engineering-harness.toml`, a
managed workflow whose check steps surface the evaluator's refusal, a
`RISK.template.md`, and a `.gitignore` block between hash markers;
`harnessctl raise-risk --with-decision` writes a raised risk and its open
decision and `harnessctl check` names the decision, never the risk; `adopt`
is refused as an unknown command; the public demonstration still renders.
This repository's adoption of 0.17.0 as its own root is an ordinary later
work order.

## Known open questions that do not block this release

- The suite runs hosted on Linux only; Windows readings remain workstation
  readings until a Windows test lane exists. On this workstation one test
  errors deterministically on a read-only temporary Git object during
  teardown (`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`),
  the baseline every work order of this cycle recorded; the complexity test
  of `tests/test_module_seams.py` skips where radon is absent.
- Five definition packets and one execution branch merged without the
  `Harness-Work-Order` trailer on their commits. The contract exempts them
  by name and repairs the one execution trace; whether the pull-request
  lanes should refuse a trailer-less governed commit is a process question
  for the owner, not a condition of this release.
- `WO-TCM-011` may start now that its constraint is met; whether it starts
  before or after this release is the owner's sequencing call, and starting
  it before the candidate is bound is a stop condition here.
- `DEC-ECP-002`'s revisit trigger fired with the wave 3 merge; the note on
  the decision and on `SPEC-ECP-023` belongs to the next work order in that
  domain.
- The `release_build.canonical_json_bytes` alias for
  `scripts/replay_release_build.py` is a wave 2 follow-up still open.
