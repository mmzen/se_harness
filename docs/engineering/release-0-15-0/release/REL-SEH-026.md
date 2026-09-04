+++
id = "REL-SEH-026"
type = "release_contract"
title = "Release se-harness 0.15.0: the decision artifact, the reader-first definitions and the repository-owned glossary"
status = "draft"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-09-04"
updated = "2026-09-04"
previous_release_tag = "v0.14.0"

[relations]
gates = [
  "WO-CIP-006",
  "WO-DCM-001",
  "WO-DOC-014",
  "WO-DOC-015",
  "WO-DPG-002",
  "WO-ECP-025",
  "WO-HUP-015",
  "WO-TCM-004",
  "WO-TCM-005",
  "WO-TCM-006",
  "WO-TCM-007",
  "WO-TCM-008",
  "WO-RLS-021",
]

[release_unit]
untraced_exemptions = [
  "3078575cc306e9b472028c70856c7effccc733d3",
  "2e215823c66b614cd3183267a8caf16dad6c71db",
  "7863cc6c8c53aa598e52914d4786f2b4857f1cf0",
  "387caa471432be99b343f970488bfc784b941676",
  "0db0686fb3d63ad20dd3bd77c220efa9b19895ed",
  "f790e6b466d346ba92676d327b48906cb9e79c62",
  "e5aafca23a176281c0df5708fb3df00a190a6dac",
  "8c4008041de1cdfb890b090997e14f3fbadbae9f",
  "6dca7773d15dcb36ed923e5e4de1859bbb33cd2b",
  "11babc9c3a51f989c852b9ffda5a56457db830c2",
  "2fb39a3572227b3eba30291a6bb1d63ba87f521a",
]
+++

# Release contract: se-harness 0.15.0

## Lifecycle and authority

This contract is a definition. Its approval by the release owner authorizes
`WO-RLS-021` to be approved and started as separate acts; it authorizes no
candidate, build, verification record, release record, tag, publication or
deployment by itself. Every later step is the decision of the role that owns
it, recorded on the artifact it changes. The aggregate verification record
is `VREC-SEH-024`; the release record is `RLS-SEH-024`.

This contract was drafted while work was still in progress on `main`,
re-measured on 2026-09-04 after that work landed as `WO-DOC-014` and
`WO-DOC-015`, and re-measured again after `WO-DOC-014`'s verification record
was prepared and verified as a post-merge repair (issue #347). Every member
whose assurance is `required` now holds a verified record. A member that
reaches `implemented` after approval is a stop condition, never a widening
in place.

## Release unit

One `se-harness` 0.15.0 release derived from one clean candidate commit cut
from `main`: a recipe-bound reproducible wheel, a normalized source
distribution, a checksum manifest, a schema-2 bound distribution table, an
immutable `v0.15.0` tag, GitHub Release assets, publication of the same
qualified files to PyPI, the canonical `release/0.15` maintenance line
established at the released candidate, a release-bound static Explorer
demonstration, and the `last` alias tag and GitHub "latest" marker moved
to it.

The release-bearing work added after the immutable `v0.14.0` baseline is
twelve work orders. They were measured on `main` at `2e90dc6` as active,
`implemented`, holding work-order-keyed evidence, absent from the `v0.14.0`
tree, and unnamed by any released release record. Eleven hold verified
coverage; `WO-DOC-015` (assurance `not_required`) is covered by the
aggregate record alone.

| Work order | Outcome | Coverage at drafting |
| --- | --- | --- |
| `WO-HUP-015` | Adopt exact public 0.14.0 as the standard root, the simple way; candidate moved to 0.15.0 | `VREC-HUP-014` verified |
| `WO-DPG-002` | Let the Pages packager find its notice boundary in the designed Explorer | `VREC-DPG-002` verified |
| `WO-ECP-025` | Delete the four CLI tombstone guards, by the delegated route | `VREC-ECP-029` verified |
| `WO-CIP-006` | Let the pull-request rehearsal select a record the base already holds | `VREC-CIP-006` verified |
| `WO-DCM-001` | The decision artifact (`DEC-`), its gate predicates, `harnessctl decide`, standing deviations | `VREC-DCM-001` verified |
| `WO-TCM-004` | Register the `E-DCM` and `W-DCM` families in the diagnostic-code index | `VREC-TCM-004` verified |
| `WO-TCM-005` | The reader-first requirement shape, `W-AUT-003` at 30 words, `W-AUT-005` to `W-AUT-010`, the `Open decisions` section retired | `VREC-TCM-005` verified |
| `WO-TCM-006` | The repository-owned glossary seed `GLOSSARY.md`, the `inspect` vocabulary report | `VREC-TCM-006` verified |
| `WO-TCM-007` | The reader-first intent shape, the `outcome` field, `W-AUT-011` to `W-AUT-015`, the Explorer's outcome line | `VREC-TCM-007` verified |
| `WO-TCM-008` | The reader-first capability shape, the `ability` field, `W-AUT-016` to `W-AUT-018`, derivation read from the graph | `VREC-TCM-008` verified |
| `WO-DOC-014` | Publish the owner-reviewed Verity Plane README | `VREC-DOC-007` verified, prepared after the #344 merge as the repair issue #347 records |
| `WO-DOC-015` | Add the supplied Verity Plane logo to the published README | assurance `not_required`; covered by `VREC-SEH-024` |

`WO-RLS-021` is the thirteenth member: it qualifies the candidate, takes the
build of record from the hosted pinned producer, and retains the evidence;
the candidate version already reads 0.15.0 (moved by `WO-HUP-015`). It
receives its verified coverage from `VREC-SEH-024`.

### What this release is for

0.15.0 is a content release. Since `v0.14.0` the packaged surface changed
in 30 files, the 29 below and the README the source distribution carries as
its long description: the evaluator gains the `decision` lifecycle family, the
`decision_gate_clear` evaluator behind one `QGP-*-DECISION` predicate per
gate, `harnessctl decide`, and the standing-deviation projection; the
managed templates gain `DECISION.template.md` and the reader-first
`REQUIREMENT`, `INTENT` and `CAPABILITY` templates with the `statement`,
`outcome` and `ability` lines the Explorer lifts out; the authoring guide,
`QUALITY_GATES`, `WORKFLOW`, `TRACEABILITY` and `DECISION_RIGHTS` follow;
the validator gains `E-DCM-001` to `E-DCM-004`, `W-DCM-001`, `W-DCM-002`
and the draft-time advisories `W-AUT-005` to `W-AUT-018`; the inspection
script gains the vocabulary report; the Explorer shows decisions, the
plain-words lines, the outcome, the ability and what derives from a
capability; every repository that installs or upgrades receives an
empty `GLOSSARY.md` seed of its own, once; and the published README is the
owner-reviewed Verity Plane text with its logo (`WO-DOC-014`, `WO-DOC-015`).

For this repository the release is the precondition of using any of it:
the root is governed by 0.14.0, so a `DEC-` file fails the managed check
today and new drafts still end with `Open decisions` reading `None`. The
adoption work order that follows this release is where that changes.

### Commit census

`harnessctl release-unit . --from v0.14.0 --to 2e90dc6` reads 32
first-parent commits, all merge commits GitHub wrote for pull requests.
Twenty-one are traced through their branch commits' `Harness-Work-Order`
trailers. Eleven carry no trailer: the notes-only pull requests #318, #323,
#324, #325, #326, #327, #328, #333, #334, #338 and #339, each of which
touched only `docs/notes/`, the ungoverned path `AGENTS.md` names, and is
therefore exempted above by the release owner's decision, with the reason
that a notes-only pull request needs a reviewer and not a work order. With
those eleven exemptions the census is `complete: true` with thirteen work
orders.

| Traced work order | Pull request(s) | Disposition |
| --- | --- | --- |
| `WO-RLS-020` | #315 | the 0.14.0 release branch; released by `RLS-SEH-023`, therefore outside `gates` by construction |
| `WO-DPG-002` | #316 | member |
| `WO-HUP-015` | #317 | member |
| `WO-ECP-025` | #319, #320 | member |
| `WO-CIP-006` | #321, #322 | member |
| `WO-DCM-001` | #329, #330 | member |
| `WO-TCM-004` | #331, #332 | member |
| `WO-TCM-005` | #335, #336 | member (the packet #335 also carries `WO-TCM-006`'s draft) |
| `WO-TCM-006` | #337 | member |
| `WO-TCM-007` | #340, #341 | member |
| `WO-TCM-008` | #342, #343 | member |
| `WO-DOC-014` | #344, #349 | member; #349 is the governance commit carrying `VREC-DOC-007` |
| `WO-DOC-015` | #346 | member |

`harnessctl release-unit . --from v0.14.0 --to 2e90dc6 --contract
REL-SEH-026`, with each of the eleven exempted commits also passed as
`--exempt` (the 0.14.0 command reads exemptions from its flags; the array
above is what the approval gate reads), derives `complete: true` and
reports two `E-CIP-001` findings, both by construction: the `gates`
difference, the released `WO-RLS-020` present in the derivation and
`WO-RLS-021` not yet derivable because its commits do not exist, as
`REL-SEH-025` reported `WO-RLS-019`; and, until the candidate exists, the
absence of `candidate_commit`. No trace repair is needed.

This contract names no `candidate_commit`: the candidate is created by
`WO-RLS-021` after this approval. `QGP-G5P-RELEASE-UNIT` therefore passes
unmeasured at approval; the census above is the reported evidence, and
`WO-RLS-021` re-runs the derivation at the candidate and records it.

## Required evidence

### Entry criteria

- Every existing member is active, `implemented`, retains work-order-keyed
  evidence, and every member whose assurance is `required` holds verified
  coverage. Measured at `2e90dc6`: eleven of eleven required members.
- No existing member is named by a released release record.
- No stale `ready` verification or release record exists in the graph
  beyond the canonical templates.
- The work that was in progress at drafting landed as `WO-DOC-014` and
  `WO-DOC-015` and the census was re-measured with it on 2026-09-04.
- `WO-RLS-021` is separately reviewed and approved before start preflight
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

Measured over `main` at `2e90dc6` plus this packet, with the exact public
0.14.0 evaluator outside the checkout in isolated mode, installed from the
wheel whose SHA-256 `70d438b5…` equals the distribution table of
`RLS-SEH-023`.

- `validate`: 1,308 artifacts, 0 errors, 69 pre-existing maintenance
  warnings, 0 advisories.
- `doctor`: 0 `FAIL`.
- Hosted lanes at `2e90dc6` on `main`: Engineering Harness `validate`,
  Candidate source evidence, Candidate package evidence, Governance
  migration on Linux and Windows, Governor transition assessment, both
  Publication Rehearsal legs, and the integration-package build, verify and
  retain jobs, all `success`.

### Exact aggregate verification

**Every figure here is measured over the whole `gates` array, all thirteen
entries.** `VREC-SEH-024` must bind one clean 0.15.0 candidate commit to
exactly the thirteen work orders named in `gates`, to eleven verification
contracts (`VER-CIP-002`, `VER-DCM-001`, `VER-DPG-001`, `VER-DST-001`,
`VER-DST-024`, `VER-ECP-021`, `VER-HUP-015`, `VER-TCM-002`, `VER-TCM-003`,
`VER-TCM-004`, `VER-TCM-005`), and to thirteen work-order-keyed evidence
paths: each member's handoff packet in its domain plus `WO-RLS-021`'s
packet under `docs/engineering/release-0-15-0/evidence/`. The requirement
union of the twelve content members is eighteen; with `REQ-DST-006` from
`WO-RLS-021` it is nineteen.

### Candidate qualification

At the exact candidate commit, all with the governing 0.14.0 evaluator
outside the checkout unless stated: `validate` 0 errors; `doctor` 0 `FAIL`;
review preflight `PASS`; the handoff check over the Git-derived change set;
`scripts/validate_release_distributions.py` and
`scripts/check_portable_release_surface.py` `PASS` in `--repository`,
`--wheel` and `--harnessctl` modes; the candidate's own `qualify
complete-candidate` (read from the hosted Linux lane for the `RID018`
boundary reason); the full suite on Linux (hosted) and on Windows (this
workstation, `PYTHONUTF8=1`); the real upgrade rehearsal 0.14.0 to 0.15.0
`pass` on both hosted platforms with agreeing `semantic_sha256`; all
pull-request lanes `success` at the candidate head.

### Build of record

The recipe-bound replay run by the hosted Publication Rehearsal in
`candidate` mode, dispatched on `release/0.15.0` at the candidate head
(the pull-request event builds the merge commit, not the head):
`release-qualification.yml` executes `python -m repository_tools.release_build replay`
on the pinned linux/amd64 producer image through Docker on the GitHub
runner, two byte-identical producer runs, and retains
`release-build-replay.json` whose `manifest` is the schema-2 bundle
manifest. That manifest is downloaded from the run at the bound candidate,
its `candidate.commit` checked equal, retained as
`docs/engineering/release-0-15-0/evidence/RLS-SEH-024-bundle.json`, and
bound into `RLS-SEH-024`; the hosted `release-candidate-replay.yml`
dispatch on the review ref must then reproduce the same digests from the
bound record, as `WO-RLS-020` did for 0.14.0.

## Compatibility and migration

0.15.0 changes managed templates and evaluator behaviour. `upgrade` from
0.14.0 rewrites the managed copies of the four definition templates that
changed, adds `DECISION.template.md`, rewrites `ARTIFACT_AUTHORING.md`,
`QUALITY_GATES.json` and `.md`, `WORKFLOW.json` and `.md`,
`TRACEABILITY.md`, `DECISION_RIGHTS.md` and the templates index, rewrites
the four managed scripts and the Explorer template, and installs
`GLOSSARY.md` once as a seed when absent. Owner content is untouched; a
customized managed file blocks the upgrade as always. No existing artifact
needs to change: the new front-matter fields are additive, the new
advisories fire on drafts only, and a legacy `Open decisions` section is
read as before. A 0.14.0 root reads a 0.15.0-written lock without change.
A repository on 0.15.0 can raise `DEC-` artifacts; one on 0.14.0 cannot.

## Security and provenance

The build of record is recipe-bound and digest-pinned
(`release/build-recipe.json`, `release/build-toolchain.lock`, both
unchanged since `v0.12.0`); the release record binds the wheel and sdist
digests through a schema-2 distribution table; the publication workflow
moves only verified inert bytes into privileged jobs and the `pypi`
environment remains a separate human decision. Identity by version,
installed-payload digest and archive pair is unchanged. `pyproject.toml`
gains one data-files line for the glossary seed (`WO-TCM-006`); the
portable release surface check covers it.

## Promotion policy

- `VREC-SEH-024` verified by the assurance owner on the exact candidate.
- `RLS-SEH-024` prepared by generic `prepare-release` from a wheel-file
  installed 0.14.0 evaluator, then bound by
  `scripts/bind_release_distribution.py` to the build of record; the hosted
  replay dispatched on the review ref before the release decision.
- The `released` transition rides the release pull request to `main` and is
  the release owner's act.
- After the record is `released` on `main`: `publish-pypi.yml` dispatched
  from `main` with only `release_record=RLS-SEH-024`; tag `v0.15.0`, GitHub
  Release, `release/0.15` established, PyPI publication, the Pages
  deployment; then `gh release edit v0.15.0 --latest` and the `last` alias
  tag moved to `v0.15.0` after the observation passes.

## Human approval triggers

- Approval of this contract (release owner) and of `WO-RLS-021`
  (engineering owner), as two distinct decisions, after the in-progress
  work has landed and the census has been re-measured.
- Start of `WO-RLS-021`, its completion, the verification of
  `VREC-SEH-024`, the preparation and release of `RLS-SEH-024`, the
  publication dispatch and the `pypi` environment: each a separate decision
  by its accountable owner.
- Any work order reaching `implemented` with packaged-surface bytes after
  this contract's approval is a stop condition; the remedy is rejection and
  a successor contract, never widening in place.

## Rollback criteria and procedure

A defect found after publication is repaired forward by a successor
release; a published 0.15.0 is never withdrawn from PyPI. A consumer stays
on 0.14.0 by not upgrading; the decision artifact and the new templates
simply stay unavailable to it.

Stop condition: the candidate commit is not an ancestor of the ref being
released, or `harnessctl release-unit --contract REL-SEH-026` reports an
`E-CIP-001` finding beyond the `gates` difference predicted by construction
above. The
remedy is a new contract naming a new candidate, never an in-place edit of
`gates`.

## Post-release observation window

Within one week of publication: a fresh repository initialised from the
published 0.15.0 wheel carries `GLOSSARY.md` with no term, its
`REQUIREMENT.template.md` opens with `In plain words`, and `harnessctl
inspect` prints a vocabulary section; the public demonstration at
`mmzen.github.io/se_harness` still renders. This repository's adoption of
0.15.0 as its own root is an ordinary later work order and is where
`DEC-` artifacts become usable here.

## Known open questions that do not block this release

- The suite runs hosted on Linux only; Windows readings remain workstation
  readings until a Windows test lane exists.
- Issue #269: the Linux fixture-teardown flake; a re-run is not a defect of
  the candidate.
- Issue #347: `WO-DOC-014` was merged without its assurance decision; the
  record was repaired as `VREC-DOC-007` before this contract's approval,
  and the deterministic merge-boundary control the issue asks for is a
  later packet, not a condition of this release.
- The three per-type advisory functions in the validator could be one
  table-driven helper; it is a behavior-neutral refactor for a maintenance
  work order, disclosed by `VREC-TCM-008`.
- `REQ-TCM-007`'s Behavior row still names `docs/notes/glossary.md`; the
  path moved to the repository root by amendment record on `SPEC-TCM-003`,
  and the approved requirement was not rewritten.
