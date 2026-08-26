+++
id = "RLS-SEH-013"
type = "release_record"
title = "Release candidate 0.7.0"
status = "ready"
owners = ["release-owner"]
created = "2026-08-26"
updated = "2026-08-26"
version = "0.7.0"
commit = "e98b7885b016529aa2c262ad577acdc270bc9376"
git_object_format = "sha1"
prepared_at = "2026-08-26T16:42:15Z"
prepared_by = "release-owner"
evaluator_evidence_path = "docs/engineering/release-0-7-0/evidence/RLS-SEH-013-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"
tag = "v0.7.0"

[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1787732223
wheel = "se_harness-0.7.0-py3-none-any.whl"
wheel_sha256 = "aa52125ddcc573a3ed143ad9cba59eb8b76d47c665dad982e74dc34f4ca34069"
sdist = "se_harness-0.7.0.tar.gz"
sdist_sha256 = "848da4689dbd6261afe0748089e5c34d44ad050f84152c4e83b254a72aacc54a"
checksums = "SHA256SUMS"
checksums_sha256 = "665834e57e9fcb13e0bf3e52ad0e3e54355c50688ecb6de5dc3a1c33d42117e7"
source_manifest_sha256 = "62caeee9bd9b9fe44fd3ae3336a44b0b8a7763637051017228ca9fba87d0005d"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-016"]
includes_verification = ["VREC-SEH-013"]
releases_work = ["WO-ADS-001", "WO-ADS-002", "WO-AEX-001", "WO-AEX-002", "WO-AEX-003", "WO-AEX-004", "WO-AEX-005", "WO-HBI-001", "WO-HBI-002", "WO-HBI-003", "WO-HBI-004", "WO-HUP-004", "WO-IPK-001", "WO-LRE-001", "WO-REB-008", "WO-REB-009", "WO-REB-010", "WO-REB-011", "WO-REB-012", "WO-REB-013", "WO-REB-014", "WO-REB-015", "WO-REB-016", "WO-REB-017", "WO-REB-018", "WO-REB-019", "WO-REB-020", "WO-REB-021", "WO-REB-022", "WO-REB-023", "WO-RLO-004", "WO-RLO-005", "WO-RLO-006", "WO-RLS-011", "WO-TCM-001", "WO-TCM-002", "WO-VSP-007", "WO-WEX-003"]
+++

# Release Record Candidate

This ready record proposes release `0.7.0` for `WO-ADS-001`, `WO-ADS-002`, `WO-AEX-001`, `WO-AEX-002`, `WO-AEX-003`, `WO-AEX-004`, `WO-AEX-005`, `WO-HBI-001`, `WO-HBI-002`, `WO-HBI-003`, `WO-HBI-004`, `WO-HUP-004`, `WO-IPK-001`, `WO-LRE-001`, `WO-REB-008`, `WO-REB-009`, `WO-REB-010`, `WO-REB-011`, `WO-REB-012`, `WO-REB-013`, `WO-REB-014`, `WO-REB-015`, `WO-REB-016`, `WO-REB-017`, `WO-REB-018`, `WO-REB-019`, `WO-REB-020`, `WO-REB-021`, `WO-REB-022`, `WO-REB-023`, `WO-RLO-004`, `WO-RLO-005`, `WO-RLO-006`, `WO-RLS-011`, `WO-TCM-001`, `WO-TCM-002`, `WO-VSP-007`, `WO-WEX-003` from candidate commit `e98b7885b016529aa2c262ad577acdc270bc9376`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.


## What this record is, and what it is not

This is a `ready` release record. It fixes, in one place, the exact release unit,
the exact candidate identity and the exact distribution digests the release owner
would be authorizing, so that the release decision is a decision about named bytes
rather than about an intention. It authorizes nothing on its own. Preparing it
created no tag, published nothing, deployed nothing, used no credential, and left
the maintenance line untouched.

Two things a reader should know before the figures. First, the release decision is
the last point at which any figure in this record can be corrected, exactly as
verification was for `VREC-SEH-013`; a released record is not amended afterwards.
Second, the recipe-bound replay that the repository's own release sequence requires
**before** the release decision has not been dispatched yet. That dispatch is a
separate decision, and this record does not stand in for it.

## Exact release unit

| Reading | Value |
| --- | --- |
| Release contract | `REL-SEH-016`, `approved` |
| Verification record | `VREC-SEH-013`, `verified` at `2026-08-26T15:50:09Z` |
| Work orders released | 38, each `implemented` |
| Verification contracts | 21, through `VREC-SEH-013`'s `conforms_to` |
| Keyed evidence paths | 41, all tracked at the candidate |
| Version | `0.7.0` |
| Tag named | `v0.7.0` -- named as a field, created nowhere |

The 38 identifiers in `releases_work` are `REL-SEH-016`'s `gates` array, re-derived
from the contract immediately before preparation rather than transcribed. They are
the same 38 `VREC-SEH-013` verifies, so released coverage and verified coverage are
the same set by construction, not by comparison. `WO-AEX-006` stays excluded and
unmerged on pull request #155, and pull request #156 stays excluded, exactly as the
contract's approval records.

`prepare-release` enforced that equality rather than trusting it. A first invocation
was refused with `WEX401`, `released work does not match verification coverage:
verified but not released WO-RLS-011`, because the shell dropped the last
identifier from the argument list. Nothing was written by the refused run. The
guard is the reason the omission could not become a release record covering 37 of
38 work orders.

## Candidate identity, and how it was fixed

| Reading | Value |
| --- | --- |
| Candidate commit | `e98b7885b016529aa2c262ad577acdc270bc9376` |
| Object format | `sha1` |
| Committer epoch | 1787732223 |
| Published as | `candidate/0.7.0`, and `main`'s own tip |

This record did not choose its candidate. `se_harness/provenance.py` requires the
included verification records to identify exactly one candidate commit and object
format, and then takes the release record's commit from that single identity. The
commit above is therefore `VREC-SEH-013`'s commit, and it cannot diverge from it
while the record includes that VREC.

## The bound distribution

| Field | Value |
| --- | --- |
| `schema` | 2, recipe-bearing |
| `kind` | `python-wheel-sdist` |
| `source_date_epoch` | 1787732223 |
| `wheel` | `se_harness-0.7.0-py3-none-any.whl`, 431141 bytes |
| `wheel_sha256` | `aa52125ddcc573a3ed143ad9cba59eb8b76d47c665dad982e74dc34f4ca34069` |
| `sdist` | `se_harness-0.7.0.tar.gz`, 621507 bytes |
| `sdist_sha256` | `848da4689dbd6261afe0748089e5c34d44ad050f84152c4e83b254a72aacc54a` |
| `checksums` | `SHA256SUMS`, 190 bytes |
| `checksums_sha256` | `665834e57e9fcb13e0bf3e52ad0e3e54355c50688ecb6de5dc3a1c33d42117e7` |
| `source_manifest_sha256` | `62caeee9bd9b9fe44fd3ae3336a44b0b8a7763637051017228ca9fba87d0005d` |
| `build_recipe` | `release/build-recipe.json`, tracked at the candidate |
| `build_recipe_sha256` | `0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc` |

The binder refuses more than it accepts, and each refusal it did not have to make
is a fact about this pairing. It required a `ready` release record; it required
schema 2, since a new ready record may not use schema 1; it required the manifest's
version, commit and Git object format to equal this record's; it required the
manifest's `source_date_epoch` to equal the candidate commit's own committer epoch,
read from `git show -s --format=%ct`; and it required
`source_manifest_sha256(repository, commit)`, recomputed over the candidate tree at
binding time, to equal the manifest's. All five held on the first attempt. The
binder writes atomically and touches only the repository-owned `[distribution]`
table.

That last equality is the one that settles which commit this release is of.
`e98b788` reproduces `62caeee9...87d0005d` and epoch 1787732223; the governance
commit `339a10e` on this branch reproduces neither, and `WO-RLS-011`'s evidence
records both measurements. A release bound to the governance commit was not merely
undesirable, it was mechanically impossible.

## Where the distribution bytes are, and why not here

On the release owner's decision of 2026-08-26 the wheel, sdist, `SHA256SUMS`, the
replay result and the bundle manifest all stay **outside** this repository. This
record carries the distribution as digests, which is what the schema is for: a
schema-2 block names `build_recipe` as a path in the candidate tree, that path is
already tracked there, and the bundle manifest is read once at binding time and not
referenced afterwards. Binding therefore added no keyed evidence path, and
`VREC-SEH-013`'s 41 paths are still the 41 the contract names.

That follows the established practice rather than departing from it. No bundle
manifest has ever been tracked in this repository on any ref, including for
`RLS-SEH-012` at 0.6.0, whose record likewise carries only digests. The binder does
require the manifest to resolve inside the repository, so the 1086-byte manifest
was copied in as an untracked transient, verified byte-identical to the build's own
copy, read, and removed in the same step. Nothing was committed and no build byte
entered the repository.

## Measured over this record's own state

Taken with the exact released public 0.6.0 evaluator, run from outside the checkout
in isolated mode, with this record and its evaluator evidence present:

| Reading | Value |
| --- | --- |
| `validate` | PASS, 894 artifacts, 0 errors, 52 warnings |
| Planes | structure E0/W0, governance E0/W0, policy E0/W0, maintenance E0/W52 |
| `doctor` | 87 PASS, 0 FAIL, exit 0 |
| Release-distribution validation | PASS, 2 distribution-bearing records |
| `inspect` | 894 artifacts, 173 findings, 1 decision required, 0 assurance pending |
| `check` pre-action, `PROC-RLS-DECIDE` | Completed; names `DR-RLS-DECIDE` |

The warning count moved from 51 to 52 and the findings count from 171 to 173. The
new warning is one `W013` on this record, `artifact 'RLS-SEH-013' is valid outside
its canonical location`. It is the same maintenance class every release record in
this repository carries, including `RLS-SEH-012`; there are now 23 such
observations, and every prior release record is in that list. It is a consequence
of the per-release domain layout, not of anything in this record.

The one decision required is this record's own: `inspect` reports
`decision_required -> review-release-decision (release-owner)` for `RLS-SEH-013`,
and `check` at `pre-action` under `PROC-RLS-DECIDE` reports Completed and names
`release-owner must decide whether the exact candidate is authorized for release
under DR-RLS-DECIDE`, with permitted outcomes `released` and `reject`.

`RLS-SEH-013-evaluator.json` is 873 bytes with no carriage returns, and hashes to
the `fcfc1447...4171962` this record's front matter binds. It is byte-identical to
`VREC-SEH-013-evaluator.json`, which is expected: the same evaluator venv produces
the same evidence, and the candidate binding lives in the `commit` field, not in
the evaluator evidence.

## Qualification the release owner is being asked to rely on

The candidate commit's own four hosted lanes are green through `main`'s push event:
Engineering Harness 32946962510, Candidate Evidence 32946962546, Governor
Transition Assessment 32946962515, Publication Rehearsal 32946962531.

The governance branch carrying this record is green as well, at commit `f8afa4d`:
all seven runs across the four lanes completed success, including the integration
package build, both platform verifications and retention, which execute only on the
`pull_request` event. That reading is worth stating precisely because it did not
hold for most of 2026-08-26: hosted Actions was degraded for roughly twenty
minutes, runs died without a runner, and `VREC-SEH-013` was verified while that was
true. The verified record discloses that as a condition of the assurance owner's
decision and is not corrected by the later green.

## What has not happened, and what this record does not authorize

The repository's release sequence requires that
`.github/workflows/release-candidate-replay.yml` be dispatched on the review ref
with only `release_record=RLS-SEH-013` **before** the release decision. It rebuilds
twice from the already-bound recipe, hashes with read-only repository permission,
and retains technical evidence. It has not been dispatched. It cannot be dispatched
until this record is committed and pushed, because the workflow reads the record
from the ref. Until it runs, the byte-identity claim for this release rests on the
two agreeing local producer instances recorded in `WO-RLS-011`'s evidence and not
on a hosted, read-only reproduction.

`VREC-SEH-013`'s seven disclosures carry into this release unchanged and were
accepted by the assurance owner as disclosed limits rather than as satisfied
requirements. In particular, `VER-TCM-001`'s two independent reviewer judgments do
not exist; `VER-ADS-001` Scenario 8 needs the same kind of human classification;
`WO-AEX-005` names four residual limits it cannot close and its new runtime modules
are unreachable from `cli.py` and inert in 0.7.0, so release notes must not
describe delegated execution as available.

Preparation and binding authorize none of the following, each of which remains a
separate decision by an accountable owner: the release decision on this record;
the replay dispatch; creating or moving the `v0.7.0` tag, which does not exist on
any ref; GitHub or PyPI publication; Pages deployment; establishing or mutating the
`release/0.7` maintenance line, which does not exist -- `release/0.6` is the newest
that does; merging pull request #169, #155 or #156; credential use; external policy
change; and root-evaluator upgrade.
