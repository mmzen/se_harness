# WO-RLS-012 qualification evidence

artifact: WO-RLS-012
checkpoint: handoff
formal_snapshot_sha256: 685a2400d0e04bdc4f6dbf6ce2d2c677352691e48b570bbda565f673f8d8b08b

Retained by the implementation actor on 2026-08-26. This file is evidence. It
records observations and refusals; it does not complete, verify, release,
publish, deploy, tag, or adopt anything, and no figure in it carries formal
authority.

## Evidence status and authority boundary

This file records two stages of `WO-RLS-012`, in that order, and nothing else,
for the reason `WO-RLS-011`'s evidence gives: the file is committed inside the
candidate it describes, so the exact-candidate figures can only be measured
after the commit exists and are retained in the later governance commit that
carries them.

**Stage 1 is the working-tree stage**: every section down to *Deferred to the
exact candidate*. Every reading was taken on branch
`governance/release-0-7-0-contract-017`, whose committed tip was
`503d15c135cae86e538d4ebdbc184f52b5e9314a` (the start transition of this work
order) carrying `main` unmoved at `be2f0cfec18b86d273400466cdf1c8c691d92f75`,
with this file as the only uncommitted change. No candidate commit existed when
the readings were taken.

**Stage 2 is the exact-candidate stage**, appended after the candidate commit
exists. Where the two speak to the same quantity, stage 2 stands.

## Baseline and current identity

| Identity | Value |
| --- | --- |
| `v0.6.0` annotated tag object | `03cae3d30ea1e3933a92c9e87683b0144f8ccc77` |
| `v0.6.0` released candidate commit | `3b339e9fc70cc634e6dc6bda07ea6a9b1a465798` |
| `main` at drafting and at every reading | `be2f0cfec18b86d273400466cdf1c8c691d92f75`, tree `fd9bccb5631bef0279ae92c40353b818016cd277` |
| Branch tip at the readings | `503d15c135cae86e538d4ebdbc184f52b5e9314a` |
| Root evaluator | exact public `0.6.0`, lock schema 3, `tool_version = "0.6.0"` |

The branch is `main` plus three governance commits touching only
`docs/engineering/release-0-7-0/`: the packet (`f310024`), the two approvals
(`6d5aeab`), and the start (`503d15c`).

## Aggregate scope, re-derived from the contract at this tree

`REL-SEH-017` is `approved` (2026-08-26T20:59:11Z) and names fifty-three gates.
Re-derived from that array at `503d15c`:

| Figure | Reading |
| --- | --- |
| Members | 53: 52 read `implemented`, `WO-RLS-012` reads `in_progress` |
| Verified coverage | 51 of the 52 implemented members hold a verified record; `WO-RLS-011` is covered by the planned aggregate record, as the contract states |
| Verification contracts, whole-`gates` basis | **24** |
| Requirement union, whole-`gates` basis | **65** |
| Keyed evidence paths | **57 existing** plus this file = **58** |
| Members in the `v0.6.0` tree | 0 |
| Members named by a released record | 0 |
| Implemented, unreleased work orders outside `gates` | 45, none declaring a path under `se_harness/`, `templates/`, `repository_tools/`, `release/`, or `pyproject.toml` |
| `ready` records | only the two canonical templates |

### Bound verification commits

Fifty-two verified records cover members. Fifty-one bind a commit that is an
ancestor of `503d15c`. **One does not: `VREC-IPK-001` binds
`6d4a727789668395365d885be0c2e829f1aaba2c`**, which GitHub resolves as a
pull-request merge-preview commit ("Merge cb5cfe0 into a57e73e") that exists on
no branch and is absent from a full (non-shallow) clone. This is the standing
`W-REV-003` observation `WO-RLS-011`'s evidence dispositioned as a clone-depth
artefact; measured here on a full clone, it is not clone depth — the bound
commit is a `refs/pull/*/merge` object. The record is verified and cannot be
corrected; the bytes it verified reached `main` through the true merge of that
pull request. Carried as a residual risk, not softened.

### The reported commit census

`harnessctl release-unit . --from v0.6.0 --to be2f0cf --json`: nine work
orders traced from trailers, ninety-three untraced first-parent commits,
`complete: false`. Reported, not enforced, on the owner's 2026-08-26 decision.

### Packaged surface versus the excluded work orders

An explicitly non-promotable ephemeral bundle was built outside the checkout
from `503d15c` (see *Recipe-bound replay rehearsal*). Its sdist holds 176
files: `se_harness/` 44, `templates/` 61, `tests/` 59, `scripts/` 1, plus
`LICENSE`, `MANIFEST.in`, `PKG-INFO`, `README.md`, `pyproject.toml`,
`setup.cfg`, and the egg-info. It contains no `docs/` tree, so none of the
forty-five excluded work orders' declared scopes — all under `docs/` or
`.github/` — has bytes in it.

## Version inventory

| Surface | Reading | Status |
| --- | --- | --- |
| `pyproject.toml` `version` | `0.7.0` | candidate, unchanged by this work order |
| `se_harness/__init__.py` `__version__` | `0.7.0` | candidate, unchanged |
| `README.md` current public install example (line 45) | `se-harness==0.7.0` | candidate, unchanged |
| `tests/fixtures/governance_migration/candidate-0.6.0-to-0.7.0.json` | declares successor `0.7.0`; `predecessor_facts derive` resolves it, `scenario_sha256 0b21462c…` | in place (`WO-REB-023`) |
| `.engineering-harness.toml` `tool_version` | `0.6.0` | **unchanged** |
| `AGENTS.md` pinned evaluator instruction | one `se-harness==0.6.0` occurrence | **unchanged** |
| `docs/notes/developing-se-harness.md` | names candidate 0.7.0 and root 0.6.0 | both required; unchanged |

Nothing moved: every candidate-bearing surface already read 0.7.0 on `main`.

## Evaluator, source, and package origins

- Governing evaluator: `C:\Users\mathi\se-harness-eval`, `se-harness 0.6.0`
  installed from the wheel file whose digest
  `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7` equals the
  one `RLS-SEH-012` binds (`direct_url.json` records it); CPython 3.14.6;
  every command below run with `-I`.
- Candidate source: this checkout at `503d15c`.
- Candidate package: the ephemeral bundle below, non-promotable by
  construction (built from a governance commit that is not the candidate).

## Governing readings, released 0.6.0 evaluator

| Command | Reading |
| --- | --- |
| `validate .` | **PASS** — 952 artifacts, 0 errors, 50 warnings; planes structure E0/W0, governance E0/W0, policy E0/W0, maintenance E0/W50 |
| `doctor .` | **87 PASS, 0 FAIL** |
| `inspect .` | 952 artifacts, 3494 relations, 183 findings: error 0, warning 64, info 119; decisions required 0, definitions pending 0, assurance pending 1 (`WO-RLS-011`, covered by the planned aggregate record) |
| `upgrade .` (plan) | 36 files, **36 unchanged** |
| `preflight --phase start` | **PASS** (recorded in the start transition) |
| `preflight --phase review` | **PASS** |
| `python scripts/validate_release_distributions.py --root .` | **PASS**, one distribution-bearing record |
| `python scripts/check_portable_release_surface.py --repository .` | **PASS** |
| `git diff --check` | clean |

### Warning disposition

| Code | Count | Disposition |
| --- | --- | --- |
| `W013` canonical location | 21 | Pre-existing historical layout; out of scope |
| `W014` legacy architecture without `decision_assessment` | 14 | Compatibility-window migration; separate governed work |
| `W015` deprecated `constrains` relation | 15 | Same |
| `W-HEX-002` / `W-HEX-003` (derived, `inspect`) | 4 / 9 | Owner-review queues, not release blockers |
| `W-REV-003` declared candidate commit unavailable | 1 | `VREC-IPK-001`; see *Bound verification commits* |

Unchanged from `WO-RLS-011`'s readings in kind and count for the validator
warnings.

## Runtime suites

| Runtime | Command | Reading |
| --- | --- | --- |
| Windows 11, CPython 3.14.6 | `python scripts/run_tests.py --workers 8 --scale full` | **`Ran 995 tests in 84.853s (117 classes, 8 workers)` — `OK (skipped=24)`**; the 1,000-artifact scale size ran |
| Windows 11, CPython 3.11.9 | `py -3.11 scripts/run_tests.py --workers 8 --scale full` | **`Ran 995 tests in 83.900s (117 classes, 8 workers)` — `OK (skipped=24)`**; same counts and verdict as 3.14 |

The 24 skips are the Windows platform guards; the hosted Linux lane runs the
same suite without them (`WO-TST-003` sets the full scale there).

## Byte-rule inventory

74 tracked paths match the `text eol=lf` rules in `.gitattributes`; every one
carries zero CR bytes in the worktree. The owner-region rules from `WO-HBI-003`
and `WO-HBI-004` were not touched. (57 at `WO-RLS-011`'s reading; the growth is
the evidence JSON and skill files the sixteen later members added.)

## Governor succession, recovery, migration, Explorer

| Reading | Result |
| --- | --- |
| `scripts/validate_governor_transition.py plan --repository .` | **`passed: true`, `transition_required: false`** — base `be2f0cf` and target `503d15c` both at evaluator 0.6.0, lock `abcb1fe7…`, schema 3; the released 0.6.0 evaluator governs the 0.7.0 candidate root without succession |
| `rehearse-recovery --candidate-commit 0000…0000 --target-version 0.7.0` into an external empty directory | **PASS** — immutable-selection, isolated-local-build, simulated-publication, external-install-proof, interrupted-root-transaction (rolled back) and the remaining stages all `pass` |
| `rehearse-migration` on `candidate-0.6.0-to-0.7.0.json`, predecessor = the external 0.6.0 evaluator (3.14.6), successor = a fresh venv holding the ephemeral 0.7.0 wheel (3.14.6) | **`overall_result: pass`**, all nine stages pass, classification `compatible` with no missing capability, `operational_state.unchanged: true`, `semantic_sha256 6322ce453ba76c8b399c358ffde74bbdc32b0a5844e3941b621c8c12cd148904` |
| `dashboard . --output <external>` twice, released evaluator | **deterministic**: both runs `PASS`, 952 artifacts, 3494 relations, 0 errors, 64 warnings, manifest `858213af53a8964cf32cc4cd2dd65ba5c8aebc2a430ff89a6ddcec136b8c5db5`; 1121 files, 9,377,033 bytes; the only differing file is `generation-summary.json` (`elapsed_ms`, `generated_at`) |

## `qualify` operation boundaries

| Operation | Reading |
| --- | --- |
| `released-root .` | `passed: false` on `RR001` runtime does not match the target root lock (the checkout is candidate 0.7.0, the root is 0.6.0); `RR002`/`RR003` not run; `RR004` unchanged. Structural refusal, as at `WO-RLS-011` |
| `complete-candidate . --candidate-commit 503d15c…` | `CC001` candidate runtime identity failed (this shell's interpreter is not isolated); `CC002` HEAD and tracked tree match; `CC003` not run; `CC004` unchanged. Same reading class as `WO-RLS-011`; the hosted `candidate`-mode rehearsal is the reading of record |
| `predecessor-view` | not applicable to an ordinary release |
| `candidate-package`, `public-install` | require the exact candidate wheel and a published wheel; stage 2 and the post-release window |

## Recipe-bound replay rehearsal on this workstation

The declared build path was exercised end to end from Windows 11 through Docker
Desktop (daemon 29.7.2, `linux/amd64`), against `503d15c` — a governance commit,
so the output is **explicitly non-promotable** and exists only to prove the
path and to supply the acceptance and migration inputs above. The exact
candidate build is stage 2.

`python -m repository_tools.release_build replay --repository . --commit
503d15c… --version 0.7.0 --output-directory <external> --result <replay.json>`:
exit 0, `state: exact`.

| Identity | Value |
| --- | --- |
| Producer | `python@sha256:2856e6af199e8128161abd320575eb9b341f3b76f017b5d0c9cd364f60d8a050`, linux/amd64 |
| Recipe | `release/build-recipe.json`, `se-harness-release-build-recipe/v1`, sha256 `0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc` |
| `SOURCE_DATE_EPOCH` | 1787777982 (the commit's own timestamp) |
| Source manifest | `a4ce8244865a44d4ebb893763afd462529c3e6cda8d2c88477e1e02364b6af08` |
| Build a and build b | wheel `dc7f69ed955c53465019dc4a1fde606e9e109d8f8b56713a27d9ba225c228d1e`, sdist `1421cb1a8bfc7fd2e4bf85426f62aec40a94a246fc701729f7da3b24f88c10c8` — **byte-identical** |
| Checksums file | `9c46d04fc53121d0d7b6a0a2f2d9a9b261da421ccd0f81f4daa2f00e38f21853` |

The `WO-RLO-007` hand-back (`chown` through the pinned image) is POSIX-only
and did not run here; teardown on this workstation succeeded without it. That
is a platform fact recorded, not a change to the interpreter.

## Verifier-owned black-box package acceptance

Run by the released 0.6.0 evaluator (`accept-candidate`) against the ephemeral
0.7.0 wheel above, with `--checkout-root` set to this checkout. **Ten of ten
scenarios passed**; schema `se-harness-functional-acceptance-v1`; verifier
wheel `2a952eb6…`, contract `a443e93d6da7d0538bdf790a16f4dea49ac7a6ede384c65e40362627d7a84b75`;
candidate wheel `dc7f69ed…`, commit `503d15c…`; CPython 3.14.6. A first run
without `--checkout-root` was refused at `installed-identity` with `RID005`
checkout boundary is required; the flag is the documented form and the refusal
is recorded, not worked around.

## Declared change set

| Path | Change |
| --- | --- |
| `docs/engineering/release-0-7-0/evidence/WO-RLS-012-verification.md` | this file |

Every other in-scope change is in the three committed governance commits.
`docs/engineering/README.md` and `docs/notes/developing-se-harness.md` were
measured and needed no edit: the index already names `release-0-7-0/`, and the
note already states both identities and the current release sequences.

## Determinism, changed-path ledger, and protected controls

| Reading | Result |
| --- | --- |
| Changed-path ledger, `v0.6.0` to `503d15c` | 684 paths |
| Branch against `main` | 4 files, 787 insertions, 55 deletions, all under `docs/engineering/release-0-7-0/` |
| Protected-control diff, `main` to `503d15c` | **empty** — no managed, hash-locked, or fragment-mode path moved |
| Secret and private-path scan over the branch's added lines | no credential material; zero operator-home paths outside this file |

## Deviations from the work order, recorded for the completion decision

1. **The replay was rehearsed on a governance commit before the candidate
   exists.** The work order authorizes the recipe-bound build "from the exact
   candidate"; the build at `503d15c` is a rehearsal whose output is
   non-promotable and is used only as the acceptance and migration input. The
   exact-candidate build is stage 2. Chosen within the decision envelope
   (build host and deterministic temporary directories).
2. **`VREC-IPK-001`'s bound commit is a pull-request merge-preview object, not
   a clone-depth artefact.** Measured on a full clone; the earlier disposition
   is corrected here. The record cannot be corrected; the risk is carried.
3. **The acceptance needed `--checkout-root`.** The first run was refused at
   `RID005`; the second, with the checkout boundary declared, passed ten of
   ten. Recorded because the refusal is a usability edge worth knowing.

## Deviation acceptances

Recorded on 2026-08-26 from the owner's interactive answers, before the
completion decision. These are the owner's statements; the assurance decision
on `VREC-SEH-014` remains separate.

| Deviation | Owner answer |
| --- | --- |
| 1 - replay rehearsed on the governance commit before the candidate | Accept: within the envelope; the build of record is stage 2. |
| 2 - `VREC-IPK-001` binds a merge-preview object | Carry as residual risk; restate in `VREC-SEH-014`. |
| 3 - acceptance needed `--checkout-root` | Accept: recorded as a usability edge. |

The owner also authorized, in the same exchange, the candidate commit on this
branch, its push, and a pull request against `main`.

## Residual risks carried forward without softening

- `VER-TCM-001`'s two reviewer judgments and `VER-ADS-001`'s Scenario 8
  classifications do not exist (`REL-SEH-017`).
- `VREC-IPK-001` binds an unbranched merge-preview commit.
- The hosted dual-platform readings for the candidate itself are stage 2.

## Deferred to the exact candidate

| Item | Why |
| --- | --- |
| Exact candidate commit, tree, epoch, clean-worktree proof | needs the commit |
| Recipe-bound build of record and bundle manifest | needs the commit |
| Hosted `candidate`-mode rehearsal on both platforms | needs the push and pull request |
| `qualify candidate-package` on the exact wheel | needs the build of record |
| Re-derived census at the candidate | re-measured, not carried |
| Handoff check binding | the snapshot above |

## Unperformed transitions and external actions

No candidate commit, push, pull request, `implemented` transition,
`VREC-SEH-014` or `RLS-SEH-014` preparation or transition, tag, GitHub or PyPI
publication, Pages deployment, `release/0.7` mutation, credential use, or
root-evaluator change was performed.

## Exact-candidate stage: identity and binding

| Identity | Value |
| --- | --- |
| Candidate commit | `24cf7c767583e83b9056d03d7dd5de6622fef91c` |
| Candidate tree | `05b0e6dd2b39da89180e4712a5a2fdc6d2f861f4` |
| Parent | `503d15c135cae86e538d4ebdbc184f52b5e9314a` (first-parent path to `main` at `be2f0cf`) |
| `SOURCE_DATE_EPOCH` | 1787778641 (the commit's own timestamp) |
| Candidate against its parent | 1 file, 287 insertions: this file's stage 1 |
| Worktree at every stage-2 reading | clean, 0 dirty paths |
| Pull request | #183, body carries `Harness-Work-Order: WO-RLS-012` with zero CR bytes |

The candidate is `main` plus four commits confined to
`docs/engineering/release-0-7-0/`; no product byte differs from `main`.

## Exact-candidate stage: governing readings, released 0.6.0 evaluator

| Command | Reading |
| --- | --- |
| `validate .` | **PASS** — 952 artifacts, 0 errors, 50 warnings, every plane at E0 |
| `doctor .` | **87 PASS, 0 FAIL** |
| `preflight --phase review` | **PASS** |
| `validate_release_distributions.py` | **PASS**, one distribution-bearing record |
| `check --checkpoint handoff` | **Completed** on both evaluators at formal snapshot `685a2400d0e04bdc4f6dbf6ce2d2c677352691e48b570bbda565f673f8d8b08b` (the snapshot excludes retained evidence, so it is unchanged by this file's stages) |
| `dashboard` twice | deterministic, manifest `6621d36da93079318887723d1708be3f081ce46f8f28524b63591f9eb21c4059`, 1122 files, 9,394,471 bytes |
| `release-unit . --from v0.6.0 --to 24cf7c7` | 9 work orders traced, 97 untraced first-parent commits, `complete: false` — reported, not enforced |

## Exact-candidate stage: the build of record

`python -m repository_tools.release_build replay --repository . --commit
24cf7c767583e83b9056d03d7dd5de6622fef91c --version 0.7.0 --output-directory
<external> --result <replay.json>` on this workstation through Docker Desktop
(daemon 29.7.2, `linux/amd64`): exit 0, **`state: exact`**, two fresh producer
instances **byte-identical**.

| Identity | Value |
| --- | --- |
| Producer | `python@sha256:2856e6af199e8128161abd320575eb9b341f3b76f017b5d0c9cd364f60d8a050`, linux/amd64 |
| Recipe | `release/build-recipe.json`, sha256 `0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc` |
| Source manifest | `21f6955719e91b0bd589516cd9f45b9f869fc4108585a2f0926cff3cc16cfcde` |
| Wheel `se_harness-0.7.0-py3-none-any.whl` | `4d0589fded5c3da4f247c3f54e4204334ad283ea6b90f6dcc67c559726f557ca` |
| Sdist `se_harness-0.7.0.tar.gz` | `d05541fd94a3d444da20bb539eb6ca211ae10e1ccb0ff04a0f1628ec7e111f6c` |
| `SHA256SUMS` | `a77c49c97bd1bea13bcf140fb952546e862105e2f3b1016de108678e29cb1b58` |
| Bundle manifest (`create_release_bundle_manifest.py`) | schema `se-harness-release-bundle/v2`, file sha256 `52b5848c9f5dc4b72d94d13b0bd2b0b3598cbc037fa77835552dc20b8ed89e46`, held outside the checkout for `RLS-SEH-014`'s binding |

Sdist: 176 files (`se_harness/` 44, `templates/` 61, `tests/` 59, `scripts/`
1, metadata), no `docs/` tree, no unsafe archive member. Wheel: 111 files.
The `WO-RLO-007` hand-back did not run (POSIX-only); teardown on Windows
succeeded without it.

## Exact-candidate stage: verifier-owned black-box package acceptance

Released 0.6.0 verifier (`accept-candidate`, `--checkout-root` this
checkout) against the exact wheel `4d0589fd…` at `24cf7c7…`: **ten of ten
scenarios passed**, CPython 3.14.6, schema
`se-harness-functional-acceptance-v1`, verifier wheel `2a952eb6…`, contract
`a443e93d…`. The checkout was unchanged by the run.

`qualify candidate-package` on the same inputs: the released 0.6.0 evaluator
predates the `qualify` namespace and refuses the command; run from the candidate
checkout it refuses at `CP001` released verifier identity failed, because the
verifier it requires is a released evaluator that carries `qualify`. This is the
documented `accept-candidate` bootstrap exception `REL-SEH-017` retains for this
release; `accept-candidate` above is the reading of record.

## Exact-candidate stage: hosted lanes on pull request #183

All four lanes ran on the `pull_request` event for head `24cf7c7` and
concluded **success**: Engineering Harness (also `success` on the `push`
event), Governor Transition Assessment, SE Harness Candidate Evidence (candidate
source, candidate package, governance migration on Linux and Windows,
deterministic integration package built, verified on both platforms and
retained), and Publication Rehearsal run `33014118865` (`Qualify and replay
(candidate)` success; the release-record job skipped, no schema-2 record
existing yet).

The hosted rehearsal's suite step on Linux: **`Ran 995 tests in 49.017s` —
`OK (skipped=4)`** at full scale, the same 995 as both Windows runtimes with the
platform guards not skipping. Its artifact
`qualification-candidate-82d4f24b…` holds `complete-candidate-qualification.json`
(`passed: true`, `completion: completed`) and `release-build-replay.json`
(`state: exact`, two identical builds). **Its digests differ from the build of
record and must not be quoted for it**: the `pull_request` event checks out the
merge-preview commit `82d4f24bde4ded86beab0088aa153d0ba0dbb2c9` (parents
`be2f0cf` and `24cf7c7`), whose tree is the candidate's tree
`05b0e6dd…` exactly but whose epoch is 1787778646, so its wheel reads
`88cd5154…`. The hosted replay therefore proves the recipe path and the tree,
and the read-only `release-candidate-replay` dispatch on the bound record is
the hosted reading of the candidate's own hashes.

## Exact-candidate stage: disclosed limitations, dispositioned

- `VER-ADS-001`/`VER-ADS-002` pull-request-lane gap: the candidate's own
  `pull_request` runs on both platforms are green at head `24cf7c7`, which
  contains both bound ADS candidates; the missing reviewer classifications
  remain owed.
- `VER-TCM-001` reviewer judgments: unchanged, owed.
- `VREC-IPK-001` merge-preview commit: unchanged, carried.

## Exact-candidate stage: aggregate census re-derived at the candidate

Unchanged from stage 1 and re-measured, not carried: 53 members, 52
`implemented` and this work order `in_progress`; 51 verified records plus
`WO-RLS-011` covered by the planned aggregate record; **24** verification
contracts; **65** requirements; **58** keyed evidence paths (57 plus this file,
now existing). No work order reached `implemented` during execution; `main`
is unmoved at `be2f0cf`.

## Exact-candidate stage: planned aggregate VREC inputs, as measured

`VREC-SEH-014` binds candidate `24cf7c767583e83b9056d03d7dd5de6622fef91c` to
the 53 work orders `REL-SEH-017` names, the 24 verification contracts and the
58 keyed evidence paths above, with the released 0.6.0 evaluator's identity
evidence and the distribution identities of the build of record. Neither the
record nor `RLS-SEH-014` is prepared by this stage.

## Exact-candidate stage: unperformed transitions and external actions

No `implemented` transition, no `VREC-SEH-014` or `RLS-SEH-014` preparation
or transition, no distribution binding, no tag, no GitHub or PyPI publication,
no Pages deployment, no `release/0.7` mutation, no credential use, no
root-evaluator change. The candidate was not mutated after the build of record.
