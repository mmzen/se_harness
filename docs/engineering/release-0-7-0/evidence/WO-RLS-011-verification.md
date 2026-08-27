# WO-RLS-011 qualification evidence

artifact: WO-RLS-011
checkpoint: handoff
formal_snapshot_sha256: cffd7b4fa038f03a01a6e31bde09a347dc1bd6db5f36ed1406923802ed7c411a

Retained by the implementation actor on 2026-08-25. This file is evidence. It records
observations and refusals; it does not complete, verify, release, publish, deploy, tag,
or adopt anything, and no figure in it carries formal authority.

## Evidence status and authority boundary

This file records **two stages of `WO-RLS-011`, in that order, and nothing else.**

**Stage 1 is the preliminary working-tree stage**: every section from *Baseline and current
identity* down to *Planned aggregate VREC inputs*. Every reading there was taken against
the operational working tree on branch `chore/wo-rls-011-0-7-0-qualification`, whose
committed parent is `826c72cfdaa3401cccf06c67943c5315221c3f72` and which carried eight
uncommitted in-scope modifications. **No candidate commit existed when those readings were
taken.** The binding block at the top of this file is stage 1's binding: it names the
`handoff` gate reading and the artifact snapshot that reading cleared against, both of which
are historical facts and neither of which is re-pointed by stage 2.

**Stage 2 is the exact-candidate stage**: every section from *Exact-candidate stage:
identity and binding* onward, measured after the candidate commit existed.

**This file is committed as part of the candidate it describes, so it structurally cannot
name the candidate's own commit hash.** That is why the split exists rather than being a
convenience: the exact-candidate figures are measured after the commit and retained in the
later governance commit that carries them, which is also what keeps this work order's
constraint against mutating the candidate after exact-commit replay satisfiable.

**Stage 2 extends this file rather than opening a second one, and that is a contract
constraint, not a stylistic choice.** `REL-SEH-015` clause 10 fixes the aggregate at
thirty-seven work-order-keyed evidence paths, "the thirty-six existing paths measured at the
drafting commit plus the one `WO-RLS-011` retains", singular. A second keyed file under this
work order would make thirty-eight and falsify an approved contract that can no longer be
widened in place.

**Stage 1 is not corrected in place, and stage 2 supersedes it wherever the two speak to the
same quantity.** Read every stage 1 figure as the preliminary one: where stage 2 measures
the same thing, stage 2's figure stands; where stage 2 is silent, stage 1 stands
unqualified. *Exact-candidate stage: deferred work discharged* states row by row which
entries of *Deferred to the exact candidate* stage 2 closed and which remain open, with the
reason each remaining one is still open.

Nothing in either stage was authorized beyond the declared execution-scope paths, six as
approved and seven as amended on 2026-08-25, plus exactly three later acts the accountable
engineering owner decided explicitly on 2026-08-25 with the exact-candidate readings in
front of them: the candidate commit, this work order's `in_progress` to `implemented`
transition, and the push of the working branch. No promotable distribution was built, no tag
was created or moved, no GitHub or PyPI publication or Pages deployment was attempted, no
maintenance line was touched, and the root evaluator and root lock were not changed.
`REL-SEH-015` was not touched. `VREC-SEH-013` and `RLS-SEH-013` were neither prepared nor
transitioned. *Unperformed transitions and external actions* is stage 1's list and remains
accurate for stage 1; *Exact-candidate stage: unperformed transitions and external actions*
is the corresponding list for stage 2 and is the one that describes the state this file is
committed in.

## Baseline and current identity

| Item | Identity |
| --- | --- |
| `v0.6.0` annotated tag object | `03cae3d30ea1e3933a92c9e87683b0144f8ccc77` |
| Branch point and `origin/main` at every reading | `826c72cfdaa3401cccf06c67943c5315221c3f72` |
| Branch point tree | `d673d376ff843a701952e3cee1669af5e6642261` |
| Branch point provenance | true merge of pull request #154, the governance packet |
| Working branch | `chore/wo-rls-011-0-7-0-qualification` |
| Candidate commit | **does not exist; separately authorized** |
| Formal artifact snapshot before the scope amendment | `a8b39a43d4e56a1072b0c4f37910d47004da11a1e0cdc9a1b4aeeaa2307f9a07` |
| Formal artifact snapshot at handoff, after the amendment | `cffd7b4fa038f03a01a6e31bde09a347dc1bd6db5f36ed1406923802ed7c411a` |

The handoff gate cleared once against the first snapshot, before the amendment. Amending
`WO-RLS-011`'s `[execution_scope]` changed the artifact graph and therefore moved the
snapshot, which invalidated that binding and re-blocked the gate on `QGP-G4I-EVIDENCE`. The
binding block at the top of this file was re-pointed at the second snapshot and the gate was
re-run. **This is worth recording as a sequencing rule: a scope amendment during
implementation invalidates every previously retained evidence binding, so the evidence must
be re-bound after the amendment, never before.**

`origin/main` was re-fetched at the end of this stage and still reads
`826c72cfdaa3401cccf06c67943c5315221c3f72`, with zero commits ahead of the branch point.
**No work order reached `implemented` on `main` during this execution**, so the stop
condition on an approved contract whose `gates` no longer describes the unit has not
fired. See *Stop-condition watch* for two open pull requests that could still fire it.

## Aggregate scope, re-derived from the contract at this tree

`REL-SEH-015` is `approved`, so its `gates` array is fixed authority. Every figure below
was derived from that array in the contract file itself, never carried forward from prose,
and never inferred from commits or dates.

| Derived aggregate | Whole-`gates` basis | Historical-only basis |
| --- | --- | --- |
| Work orders named in `gates` | **36** entries, 36 unique, 0 duplicates | 35 |
| Members absent from the artifact graph | **0** | 0 |
| Members not at the expected status | **0** | 0 |
| Historical members without verified coverage | **0** | 0 |
| Verification contracts (union of `relations.verification`) | **21** | 20 |
| Requirement union (union of `relations.implements`) | **48** | 47 |
| Work-order-keyed evidence paths that exist now | **36** | 36 |
| Keyed evidence paths after this file | **37** | 36 |

The 21 verification contracts on the whole-`gates` basis are `VER-ADS-001`, `VER-ADS-002`,
`VER-AEX-001`, `VER-AEX-002`, `VER-AEX-003`, `VER-AEX-004`, `VER-DST-001`, `VER-HBI-001`,
`VER-HUP-004`, `VER-IPK-001`, `VER-LRE-001`, `VER-REB-006`, `VER-REB-007`, `VER-REB-008`,
`VER-REB-009`, `VER-REB-010`, `VER-RLO-004`, `VER-RLO-005`, `VER-TCM-001`, `VER-VSP-002`,
and `VER-WEX-003`.

`REL-SEH-015` states the whole-`gates` basis explicitly, so **`VREC-SEH-013` must be
captured on the whole-`gates` basis: 36 work orders, 21 verification contracts, 37 keyed
evidence paths.** The single gate with no keyed evidence before this file is `WO-RLS-011`
itself; this file is its keyed evidence and the thirty-seventh path.

`WO-TCM-001`, `WO-AEX-005`, `WO-ADS-001`, and `WO-ADS-002` were each re-read in this tree
and all four are `implemented`. `VREC-TCM-002` was re-read and is `verified`, so
`WO-TCM-001`'s assurance route is confirmed as route two — verify with the missing
manual-assessment judgments disclosed as accepted residual risk — and it is unchanged from
the reading carried in the work order.

### No ungated packaged bytes

Three work orders outside `gates` had their artifact change after `v0.6.0`. None places
ungated bytes in the packaged surface:

- `WO-HUP-002` is excluded by name in the contract, and its declared execution scope
  contains no `se_harness/` or `templates/` path.
- `WO-REB-006` and `WO-REB-007` are both named in `REL-SEH-011`'s `gates`, the already
  released 0.6.0 unit. Their post-`v0.6.0` artifact edits are succession bookkeeping, not
  new packaged bytes.

Of the 67 packaged-surface paths that changed in `v0.6.0..826c72c`, 65 fall inside a gated
work order's declared `execution_scope`. The two residual paths,
`se_harness/governance_migration_contract.py` and
`templates/repository/standard/gitattributes.fragment`, were both changed by the single
commit `ca275ac` from pull request #120 and belong to `WO-REB-021`, which is gated.

**Stated limitation of that containment check:** eleven gated work orders,
`WO-REB-008` through `WO-REB-018`, declare no `[execution_scope]` at all, so no changed
path can be attributed to them by containment. The check therefore proves that no changed
packaged path lies outside the gated set; it does not partition the set. Trailer-based
attribution was tried first and rejected as non-decisive: 16 of the 24 packaged-surface
commits in the range carry no `Harness-Work-Order` trailer, because they predate the
convention or carry it only in the pull-request body.

## Version inventory

| Surface | Reading | Expected |
| --- | --- | --- |
| `pyproject.toml` `version` | `0.7.0` | candidate |
| `se_harness/__init__.py` `__version__` | `0.7.0` | candidate |
| `README.md` current public install example (line 45) | `se-harness==0.7.0` | candidate |
| `python -m se_harness --version` in the checkout | `0.7.0` | candidate |
| `.engineering-harness.toml` `tool_version` | `0.6.0` | **unchanged** |
| Released evaluator `--version`, isolated, outside the checkout | `0.6.0` | **unchanged** |
| `AGENTS.md` pinned evaluator instruction | one `se-harness==0.6.0` occurrence | **unchanged** |
| `docs/notes/developing-se-harness.md` | states both `0.7.0` candidate and `0.6.0` `tool_version` | both required |

Historical version references in the developer note are preserved and were not rewritten:
`0.5.0a1` on one line, `0.5.0` on five, `0.6.0` on nine. `tests/test_public_onboarding`
and `tests/test_progressive_documentation` both pass against these edits (33 tests, OK),
which is the documentation contract's own proof that the simultaneous candidate-and-root
statements are intact.

## Owner decisions taken during this work, 2026-08-25

Four decisions were put to the owner together, each with its measurement already taken, and
all four were answered. None was inferred from another.

1. **Blocker A is remedied by a bounded scope amendment.** `tests/test_release_qualification.py`
   is added to `WO-RLS-011`'s `[execution_scope]` as the seventh declared path, for the
   version values in one fixture method only. Recorded in the work order's
   *Scope amendment, 2026-08-25* section. Applied below.
2. **Blocker B is routed to its own work order**, to be fixed before 0.7.0 ships.
   `.github/` remains outside this work order's scope and the defect is reported here, not
   repaired here. `WO-RLO-006` was drafted and then **approved by the engineering owner on
   2026-08-25 at 17:55:39Z**, on a separate branch; start preflight PASS, implementation not
   started.
3. **All three open pull requests are held and merge after 0.7.0 is done.** Taken as one
   decision covering the pull requests carrying `WO-AEX-006`, `WO-RSK-001`, and `WO-AEX-007`.
   `REL-SEH-015` is not reopened and no fourth contract succession is issued.
4. **The candidate commit and the branch push remain unauthorized.** The owner chose to
   receive the re-measured green reading first and take that decision separately. Both acts
   are therefore still unperformed.

## Declared change set

Eight paths, all inside the seven declared execution-scope paths as amended, and the set is
complete:

| Path | Change |
| --- | --- |
| `pyproject.toml` | `version` 0.6.0 to 0.7.0 |
| `se_harness/__init__.py` | `__version__` 0.6.0 to 0.7.0 |
| `README.md` | current public install example 0.6.0 to 0.7.0 |
| `docs/notes/developing-se-harness.md` | current-candidate-version statements |
| `docs/engineering/README.md` | one domain-list addition |
| `docs/engineering/release-0-7-0/work-orders/WO-RLS-011.md` | start transition |
| `docs/engineering/release-0-7-0/evidence/WO-RLS-011-verification.md` | this file |
| `tests/test_release_qualification.py` | fixture retargeted, under the scope amendment |

All seven pre-existing files preserve CRLF in the worktree; the CR count equals the line
count for each, so the checkout's `core.autocrlf=true` conversion was not disturbed.

### The amended fixture

`ReleaseQualificationTests.test_public_install_binds_released_record_wheel_and_payload` had
five version values pinned to `0.6.0`: the wheel filename, the released record's `version`,
the distribution metadata tuple, the installed distribution's `version`, and the mocked
`--version` subprocess output. All five are now derived from `se_harness.__version__`, which
required adding one import to the module. No other test method, no fixture file, and no
production module was touched, and the seven other `0.6.0` literals in the module were left
alone because the tests holding them do not compare against `__version__`.

Deriving rather than re-pinning was chosen deliberately. `release_qualification.py:771`
requires `wheel_version == version == installed.version == __version__`, so the fixture's
job is to express that equality, not to freeze one side of it. A literal `0.7.0` would red
again at the next bump for exactly the same reason, which is the trap this red revealed.

### The engineering domain index

One line was added after the `release-0.4.1/` entry:
`` - `release-0-7-0/`: aggregate qualification, provenance, and release records for version 0.7.0. ``
and nothing else in that repository-owned index was changed.

**Recorded decision on the standing `release-0-6-0/` absence: it was left to its own
decision and deliberately not corrected here.** The work order's expected change surface
binds this file to one domain-list addition and no other change, so correcting a second,
pre-existing omission in the same edit would exceed it. The absence is a real index defect
and needs its own owner decision and its own work order.

## Evaluator, source, and package origins

The governing evaluator is the exact public 0.6.0 wheel installed in
`C:\Users\mathi\se_harness_eval_060`, outside the checkout, and every governing command
below ran it in isolated mode. Its `qualify released-root` identity block reports
`evaluator_payload_manifest: se-harness-installed-payload-v1` and
`evaluator_payload_sha256: df1673f613b91d8edd3d7ac4b178e88e58d6df71d97db7b93379fcf6807b00cf`.

A second external environment, `C:\Users\mathi\se_harness_pred_050`, holds the exact
public 0.5.0 predecessor wheel for the migration rehearsal. That wheel was downloaded and
hashed independently: `se_harness-0.5.0-py3-none-any.whl`, 180369 bytes, SHA-256
`974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`, which equals both the
PyPI-published digest and the digest the rehearsal scenario pins.

No candidate package origin is recorded. No candidate wheel was built in this stage.

## Governing readings

All from the released 0.6.0 evaluator, isolated, outside the checkout, after the working
tree reached its final state for this stage.

| Command | Result |
| --- | --- |
| `validate .` | **PASS** — 887 artifacts, 0 errors, 50 warnings |
| `validate .` planes | structure E0/W0, governance E0/W0, policy E0/W0, maintenance E0/W50 |
| `doctor .` | **PASS** — 87 PASS, 0 FAIL |
| `inspect .` | Formal validation PASS — 887 artifacts, 3235 relations, 167 findings |
| `inspect .` severity | error 0, warning 64, info 103 |
| `inspect .` queues | decisions required 0, definitions pending 0, assurance pending 0, active work 4 |
| `upgrade .` (plan, no `--apply`) | 36 files, **36 unchanged** |
| `preflight . --work-order WO-RLS-011 --phase start` | PASS (recorded in the start transition) |
| `preflight . --work-order WO-RLS-011 --phase review` | PASS |
| `focus . --artifact WO-RLS-011 --result-schema 2` | Completed; `WO-RLS-011` is `in_progress` |
| `python scripts/validate_release_distributions.py --root .` | **PASS** (1 distribution-bearing record) |
| `python scripts/check_portable_release_surface.py --repository .` | **PASS** |

`upgrade`'s "36 files, 36 unchanged" is the managed-root integrity proof: the root is
byte-exactly the released 0.6.0 installation and the candidate bump did not leak into it.

### Warning disposition

The 50 validator warnings and the 64 the Explorer and `inspect` report are the same
population seen from two sides, and every one is a maintenance-plane or derived
observation. Composition:

| Code | Count | Disposition |
| --- | --- | --- |
| `W013` canonical-location | 21 | Pre-existing historical layout; each artifact is valid where it is. Out of scope. |
| `W014` legacy architecture without `decision_assessment` | 14 | Compatibility-window migration; separate governed work. |
| `W015` deprecated `constrains` relation | 15 | Compatibility-window migration; separate governed work. |
| **validator subtotal** | **50** | matches `validate`'s maintenance plane exactly |
| `W-HEX-002` inactive governing reference | 4 | Derived; owner-review queue, not a release blocker. |
| `W-HEX-003` older source against newer dependency | 9 | Derived; artifact-owner reassessment queue. |
| `W-REV-003` declared candidate commit unavailable in this clone | 1 | `VREC-IPK-001`; an artefact of clone depth, not a record defect. |
| **derived subtotal** | **14** | |
| **total reported by `inspect` and the Explorer** | **64** | |

No warning is unexplained and none is an error.

## Runtime suites

Every figure here is Windows. The hosted Linux lane is expected to run the same suite with
no skips and has not been read in this stage.

| Runtime | Tree | Result |
| --- | --- | --- |
| CPython 3.14.6 | control worktree at `826c72c` | 1002 tests, **OK**, 23 skips |
| CPython 3.14.6 | this working tree, bumped | 1002 tests, **1 failure**, 23 skips |
| CPython 3.11.9 | control worktree at `826c72c` | 1002 tests, **1 failure + 1 error**, 23 skips |
| CPython 3.11.9 | this working tree, bumped | 1002 tests, **2 failures + 1 error**, 23 skips |
| CPython 3.14.6 | this tree, **after the amendment** | 1002 tests, **OK**, 23 skips |
| CPython 3.11.9 | this tree, **after the amendment** | 1002 tests, **1 failure + 1 error**, 23 skips |

The control worktree was checked out at the branch point specifically so each red could be
attributed. The two pre-amendment matrices differ by exactly one test, which isolates the
bump's effect from the pre-existing Windows-plus-3.11 reds.

**After the amendment the bump contributes no red on either runtime.** The 3.14 reading is
identical to the 3.14 control, and the 3.11 reading is identical to the 3.11 control: same
count, same two named tests, same skip count. The residue is exactly blocker B, which
pre-dates this work order.

Targeted re-reading of the amended module on 3.11: `tests.test_release_qualification`,
11 tests, OK.

Targeted module readings taken against this tree:

| Module | Result |
| --- | --- |
| `tests.test_hash_bound_integrity` | 102 tests, OK, 1 skip |
| `tests.test_workflow_documentation_contract` | 7 tests, OK |
| `tests.test_context_routing_retirement` | 11 tests, OK |
| `tests.test_instruction_architecture` | 30 tests, OK |
| `tests.test_public_onboarding` + `tests.test_progressive_documentation` | 33 tests, OK |
| `tests.test_release_qualification` | 11 tests, **1 failure** |

`tests.test_hash_bound_integrity` carries `ByteExactSurfaceTests`, which is the byte-rule
inventory guard, and it passes. The 23 Windows skips are platform guards.

## Byte-rule inventory

The declared byte-exact surface is the `text eol=lf` set in `.gitattributes`: the managed
`docs/engineering/**/evidence/*.json` rule, the repository-owned migration-protocol rules,
`se_harness/agent_contract.json`, `se_harness/hash_bound_classes.json`,
`release/build-recipe.json`, `release/build-toolchain.lock`, and the by-tree rule
`templates/repository/standard/.agents/skills/**`.

**57 tracked paths match those patterns and every one carries zero CR bytes in the
worktree.** No conversion leaked in, and the owner-region byte rules from `WO-HBI-003` and
`WO-HBI-004` were not touched.

**Stated limitation:** the guard's inventory is the set of declared patterns. A byte-exact
assertion added on an undeclared extension by concurrent work would not be seen by it. The
by-tree rule from `WO-HBI-004` narrows but does not close that gap.

## Package data and template parity

Nineteen root managed paths were compared with their candidate template under
`templates/repository/standard/`, on LF-normalized SHA-256:

- **10 identical**, including `DECISION_RIGHTS.md`, `QUALITY_GATES.md`,
  `QUALITY_GATES.json`, `TRACEABILITY.md`, and six of the eight managed scripts.
- **4 differ**: `docs/engineering/WORKFLOW.md`, `docs/engineering/WORKFLOW.json`,
  `scripts/validate_engineering_artifacts.py`, and
  `scripts/select_harness_work_order.py`. Candidate development leads released 0.6.0 on
  each. This is the documented candidate-versus-released boundary, not skew to repair.
- **2 exist only in the candidate template**: `docs/engineering/OPERATING_CARD.md` and
  `docs/engineering/TECHNICAL_COMMUNICATION.md`. The released 0.6.0 root does not install
  them. These are the managed policy documents `WO-ADS-001` and `WO-ADS-002` added.
- **3 root paths have no same-named template** because the template tree names them
  differently: `.engineering-harness.toml.tpl`, `ENGINEERING_HARNESS.md.tpl`, and the
  managed workflow seed.

Managed-surface size, measured rather than assumed: a fresh candidate `init` into an empty
external directory writes **60 managed files**; the released 0.6.0 root manages **36**. The
24-file delta is the subject of the later, separately approved post-publication upgrade
packet, and adopting it is explicitly out of scope here.

## CLI surface: candidate versus released

The candidate command list contains two commands the released 0.6.0 evaluator does not
have: `qualify` and `rehearse-migration`. This is why the contract's own candidate-evidence
lane invokes `qualify` with candidate source rather than with the governing evaluator, and
why `qualify released-root` cannot be exercised by the 0.6.0 root at all.

## `qualify` operation boundaries

The five `qualify` operations were exercised from the checkout. Three refuse for reasons
that are structural rather than defects, and each refusal is recorded rather than worked
around.

| Operation | Reading |
| --- | --- |
| `released-root .` | **`passed: false`.** `RR001` runtime does not match the target root lock; `RR002`/`RR003` not run after evaluator identity failure; `RR004` target state unchanged, PASS. Evaluator diagnostics `RID002` resolved 0.7.0 expected 0.6.0, `RID003`, `RID006`, `RID007`. |
| `complete-candidate . --candidate-commit 826c72c…` | **`passed: false`** on runtime identity only: `RID009` user site-packages enabled, `RID015` full lowercase candidate commit required, `RID018` distribution metadata resolves outside the checkout. |
| `predecessor-view` | Not exercised directly; the publication rehearsal excludes the equivalent mechanic with a recorded reason (below). |
| `candidate-package` | Not exercised: requires an exact candidate wheel. |
| `public-install` | Not exercised: requires a published public wheel. |

`released-root` is refused **by construction**, and this is the correct result. The
operation asks whether the running runtime is the evaluator that owns the target's root
lock; the checkout's runtime is candidate 0.7.0 and the lock names 0.6.0, so the answer
must be no. The managed lane that runs this operation,
`.github/workflows/predecessor-evaluator-assessment.yml`, invokes it only when
`transition_required` is true, using the target evaluator. `.engineering-harness.toml` is
not in this change set, so no governor transition is required and that step will be
skipped. **This is the governor-succession finding: the released 0.6.0 evaluator governs
the 0.7.0 candidate root with no version-specific exception, because the root lock is not
being moved by this candidate at all.**

`scripts/validate_governor_transition.py plan` refuses with
`error: repository worktree must be clean` and `passed: false`, so the formal
governor-succession assessment is deferred to the exact candidate.

`complete-candidate`'s three diagnostics are all environment facts, not candidate defects.
`RID015` cannot be satisfied until the separately authorized candidate commit exists, and
`RID009`/`RID018` require an isolated environment. **The credential-free publication
rehearsal proves the operation passes once that environment is right**: inside the
rehearsal root its `complete-candidate-qualification` mechanic executed successfully,
qualifying the complete candidate graph at `826c72cfdaa3`.

## Other CLI boundaries

| Command | Reading |
| --- | --- |
| `init .` | Refused: init requires an empty or absent directory; use adopt. |
| `adopt .` | **Not a refusal — it mutated the checkout.** See *Deviations*. |
| `renumber-artifacts . --map WO-RLS-011=WO-RLS-099` | `mode: blocked` — renumbering requires a clean Git worktree. |
| `transition . --set WO-RLS-011=implemented` (preview) | Blocked: `WEX201` no retained work-order-keyed evidence. This file removes that blocker. |
| `capture-verification . --id VREC-SEH-013 …` | Refused: work order `WO-RLS-011` must be implemented. |
| `prepare-release . --id RLS-SEH-013 …` | Refused: `WEX210` unknown governed artifact `VREC-SEH-013`. |
| `check . --artifact WO-RLS-011 --checkpoint handoff` | Blocked before this file existed, on `QGP-G4I-COMPLETE`, `QGP-G4I-PATHS`, and `QGP-G4I-EVIDENCE`. |

The `capture-verification` and `prepare-release` refusals are the correct ordering
boundaries: aggregate capture needs an implemented work order, and release preparation
needs a governed verification record. Neither was worked around.

## Recovery rehearsal

`rehearse-recovery --repository . --candidate-commit 0000…0000 --target-version 0.7.0`
into an external empty directory: **PASS**, report written to
`rehearsal-report.json`. The synthetic all-zero commit is the command's own
version-neutral fixture form and is not represented as a candidate identity.

## Governance migration rehearsal

`rehearse-migration` was exercised on the `historical-0.5.0-to-0.6.0` scenario with the
exact public 0.5.0 predecessor and the exact public 0.6.0 successor, both external and
isolated. Predecessor interpreter 3.11.9, successor interpreter 3.14.6, host Windows.

**`overall_result: pass`.** All nine stages — prepare, validate-complete, reject, replace,
assess, release-plan, publish-plan, render, adopt — returned `pass`, with observed
mutations equal to permitted mutations at every stage and `first_failed_stage: null`. The
classification outcome is `migration-required` with six missing predecessor capabilities,
which is the historically correct answer for that pair.

| Identity | Value |
| --- | --- |
| Result `semantic_sha256` | `0b95598cb3af2e05561faed87bec7a3905293345632bc2c40268a50a682c6583` |
| Scenario `sha256` | `393f639eb06fdec17a31386c5fc94f526cceba2e0efc95cbde6e1077f99b8324` |
| Scenario `fixture_sha256` | `daf7ca33b6fe75246d9a14c5e1193f916c4da8ba4a0a100eae2f23a351c2517c` |
| Contract `sha256` | `61f2b658dd6fcf47846a57004425a94c86396e232fac57a52475d0a432c32087` |
| Contract `implementation_sha256` | `e8cdadd36e74494d793e98c9c70a718a87fd062a4929d51096da23238279fddc` |
| Predecessor archive | `se_harness-0.5.0-py3-none-any.whl` / `974ba2de5f43bb…dd812f` |
| Successor archive | `se_harness-0.6.0-py3-none-any.whl` / `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7` |

`operational_state.unchanged: true` — the operational repository's HEAD, refs digest, and
source digest are identical before and after. Every entry in `external_actions` is
`false`: no credential use, deployment, external policy change, lifecycle transition,
maintenance mutation, network, publication, release, tag, or root-evaluator upgrade.

Two boundary refusals were recorded on the way:

- `MIG211: predecessor version differs from the scenario`, when the 0.6.0 evaluator was
  offered as the predecessor.
- `MIG229: predecessor installed archive differs from the scenario`, when the predecessor
  came from an index install. The rehearsal reads the installed archive identity from
  `direct_url.json`, which a plain index install does not write. Installing the verified
  wheel file directly supplies it. **This is a usability sharp edge worth recording**: the
  refusal names an archive mismatch when the real condition is a missing archive record,
  and the wheel was in fact byte-identical to the pinned digest.

## Deterministic Explorer generation and resource budgets

Generated twice with the released 0.6.0 evaluator into two separate external directories.
**Byte-identical and deterministic:** both runs produced manifest
`54f241fa06babf8d5f0a8df41f9a104f9351a81f6d03db25863bc13e261c6974`, 1036 files, and
8564336 bytes.

| Measure | Reading | Declared budget | Headroom |
| --- | --- | --- | --- |
| `content_projected_bytes` | 5483103 | 16777216 total | 32.7% used |
| Largest projected document | within limit | 262144 per document | no document exceeded it |
| Largest resource, the topology bundle | 886069 | 2097152 acceptance | `topology_target_exceeded: false` |
| `content_document_count` | 1030 | — | — |
| `content_omitted_count` | 1 | — | — |
| `resource_count` | 1033 | — | — |
| `resource_bytes` | 8074279 | — | — |
| `dashboard_bytes` | 154409, SHA-256 `8323eeaf57c820a2fd75fa255bd62ba335b8f262644988989107839dec36cd78` | — | — |
| `elapsed_ms` | 1256 | — | — |
| `outcome` | `generated-valid`, 0 validator errors, 64 warnings | — | — |

The one omitted document is
`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-002-evaluator-upgrade.json`,
omitted with reason `unsupported_evidence_format` because it is JSON rather than Markdown.
It is referenced by three artifacts — `WO-HUP-002`, `VREC-HUP-003`, and `VREC-HUP-005` —
which is why three omission projections resolve to one distinct omitted document. It is
designed behaviour, it is not a budget omission, and the artifact it belongs to is
excluded from this release unit by name.

## Credential-free publication rehearsal

Run on Windows, in candidate mode, against an external rehearsal root, with
`PYPI_API_TOKEN`, `TWINE_PASSWORD`, `GITHUB_TOKEN`, and `GH_TOKEN` all unset. Twenty-three
mechanics, `unreported_mechanics: []`, `state: rehearsed`, candidate
`826c72cfdaa3401cccf06c67943c5315221c3f72`, `source_date_epoch 1787664248`.

**Windows, CPython 3.14.6: every applicable mechanic executed.** Two mechanics were
excluded with recorded reasons, and one platform-and-runtime combination failed:

| Runtime | Result |
| --- | --- |
| CPython 3.14.6 | 21 executed, 2 excluded, 0 failed. Teardown removed 6723 derived paths without following a link. |
| CPython 3.11.9 | 20 executed, 2 excluded, **1 failed**: `candidate-unit-suite`. Teardown removed 7548 derived paths without following a link. |

CI pins `python-version: "3.11"` on every lane, so **the 3.11 reading is the one that
describes the hosted Windows lane**, and it is red. See *Blockers*, item B.

Both runtimes agree on the substantive build mechanics:

- `deterministic-build`: two independent builds, then `build-determinism-comparison`
  reports both distribution sets **byte-identical**.
- `sdist-normalization`: both sdists normalized at epoch `1787664248`.
- `bundle-assembly`, `bundle-manifest-creation`, `build-manifest-verification`, and
  `bundle-verification` all executed; the second set's manifest verified against the first
  set's plan, and the assembled bundle verified against the plan.
- `complete-candidate-qualification` executed and qualified the complete candidate graph.
- `evaluator-acquisition-and-hash-proof` and `evaluator-identity-proof` executed: the
  released 0.6.0 evaluator was proved and installed through the `Scripts` layout and its
  identity proved with the `harnessctl.exe` entry point.

**The distributions built here are `se_harness-0.6.0-py3-none-any.whl` and
`se_harness-0.6.0.tar.gz`, not 0.7.0.** `candidate-export` exports from the repository
archive at the committed candidate, so it cannot see the seven uncommitted modifications.
These are ephemeral, explicitly non-promotable artifacts built outside the checkout, and
they were torn down. This is direct evidence that the reading belongs to the preliminary
stage: only an authorized candidate commit will produce 0.7.0-versioned distributions.
`preconditions` records the state honestly: `clean_worktree: false`,
`uncommitted_entries: 6`, `line_ending_conversion: "true"`.

Two mechanics excluded, with the rehearsal's own reasons:

- `predecessor-view-qualification`: no committed record binds the resolved evaluator as its
  predecessor. The resolved evaluator 0.6.0 is not the predecessor evaluator 0.5.0 that
  `RLS-SEH-012` binds. Only release-record mode against a record under preparation
  exercises it.
- `recipe-bound-build-replay`: no committed release record is a released
  distribution-schema-2 subject with a bound build recipe. The one committed
  distribution-bearing record declares schema 1, so the mechanic has no subject.
  **`RLS-SEH-013` binding schema-2 distributions is what will first give this mechanic a
  subject**, which is why the two recipe-bound replays cannot precede it.

`check-divergence` against `.github/workflows/publish-pypi.yml`: **EXACT — no uncovered or
stale mechanic.** Rehearsed jobs `qualify` and `resolve` on Linux and Windows. Five
orchestrator jobs are excluded and each exclusion is justified by a credential, a
protected environment, a write permission, or an external-state action: `github_release`,
`observe`, `pages_build`, `pages_deploy`, and `pypi`.

## Deviations

**One unintended mutation of the checkout, fully reverted.** `adopt .` was run against the
already-installed root expecting a refusal symmetric to `init`'s. It is not a refusal: it
re-ran installation, reported `37 files, 36 unchanged` and
`installed se-harness 0.6.0`, created the untracked file
`docs/engineering/ADOPTION_REPORT.md`, and rewrote `.engineering-harness.lock`.

Reverted immediately with `git checkout -- .engineering-harness.lock` and
`rm -f docs/engineering/ADOPTION_REPORT.md`. The lock's blob was in fact unchanged — Git
reported it modified only because `adopt` rewrote it with LF against a CRLF worktree — so
no managed content was altered. After the revert, `git status --porcelain=v1
--untracked-files=all` shows exactly the declared in-scope modifications, and `doctor`,
`validate`, and `validate_release_distributions.py` were all re-run and returned the same
readings recorded above. **`adopt` is idempotent re-installation, not a boundary refusal,
and it writes to the target. It must not be run against an operational root as a probe.**

## Blockers

Both fixes fell outside `WO-RLS-011`'s six originally declared execution-scope paths, so
neither could be applied under the work order as approved. Both were reported with their
measurements and put to the owner. **A is now remedied under a bounded scope amendment;
B is routed to its own work order and remains open.**

### A. The version bump breaks a version-coupled test fixture — REMEDIED

`tests/test_release_qualification.py::ReleaseQualificationTests::test_public_install_binds_released_record_wheel_and_payload`
fails. `se_harness/release_qualification.py:771` requires
`wheel_version == version == installed.version == __version__`, so
`qualify public_install` demands that the released record's version equal the candidate's
`__version__`. The test's mocked fixture hard-codes `0.6.0` throughout — wheel name,
release version, metadata, installed version, and subprocess stdout — then asserts
`result.passed`. With `__version__` at 0.7.0 the equality chain cannot hold.

Confirmed bump-caused, not pre-existing: the same single test passes in a control worktree
at `826c72c`.

**Remedy applied:** the owner amended `[execution_scope]` to add
`tests/test_release_qualification.py` for the version values in that one method, and the
fixture now derives all five from `se_harness.__version__`. Both runtimes re-read green on
this test afterwards, and neither matrix gained any other change.

### B. Windows plus Python 3.11 defeats the rehearsal's own link guard — OPEN

`tests/test_publication_rehearsal.py::TeardownTests::test_a_link_out_of_the_root_is_unlinked_and_its_target_survives`
errors and `test_a_linked_root_is_refused_rather_than_followed` fails, both at `826c72c`
too, so **neither is caused by the bump**.

Mechanism: `.github/scripts/rehearse_publication.py` detects junctions with
`os.path.isjunction` and `os.DirEntry.is_junction`, both Python 3.12 additions. On 3.11
each predicate silently returns `False`, so `walk()` recurses through a junction and
`remove_tree_without_following_links` either fails its own guard or follows a junctioned
root. That defeats `SPEC-RLO-005` rule 19, which requires deleting trees by unlinking
links rather than recursing through their targets, and rule 21, which forbids deleting a
path the rehearsal did not create. A junctioned rehearsal root would have its target's
contents deleted.

The test reaches a junction because directory-symlink creation is privileged on Windows
and the helper falls back to `cmd /c mklink /J`, which is the link shape a virtual
environment or build tool actually leaves behind there.

**Consequence measured, not assumed:** under 3.11 the credential-free publication
rehearsal's `candidate-unit-suite` mechanic **fails on Windows** naming exactly these two
tests, while under 3.14 the same mechanic passes with 1002 tests. Since CI pins 3.11
everywhere, the required verification "credential-free publication rehearsal on both
runner platforms" is not satisfiable on Windows at the pinned runtime with the code as it
stands.

**Uncertainty stated rather than resolved:** the hosted Windows runner may create real
symlinks, in which case the helper never falls back to a junction, `entry.is_symlink()`
catches the link, and both tests pass there — which would explain why the lane has been
green. Linux has no junctions, so the Linux lane is unaffected. That makes the hosted
Windows-plus-3.11 reading the one fact needed to settle whether this is a red lane or a
latent correctness defect, and it has not been taken. Either way the underlying defect is
real: on Windows plus 3.11, a junction present anywhere under a rehearsal root is followed.

The fix is in `.github/scripts/`, which this work order does not authorize.

**Routing decided, work not yet drafted as an artifact.** The owner decided this becomes its
own work order and is fixed before 0.7.0 ships. The governing chain is already in place from
`WO-RLO-005`, which built the rehearsal: requirements `REQ-RLO-015` and `REQ-RLO-016`,
specification `SPEC-RLO-005`, architecture `ARCH-RLO-005` and `ADR-RLO-005`, verification
`VER-RLO-005`. Every `WO-RLO-*` identifier on every local and remote ref was enumerated and
the next free number is **`WO-RLO-006`**; the three open pull requests were checked and none
claims it.

That work order's artifact is deliberately **not** created in this working tree. Doing so
would put `docs/engineering/release-orchestration/` into this work order's change set, and
that path is outside its scope even as amended, which would make the completeness assertion
on the handoff gate untrue.

**`WO-RLO-006` was drafted on 2026-08-25 on the owner's instruction, in a separate worktree
on branch `fix/wo-rlo-006-reparse-point-teardown` off `826c72cfdaa3401cccf06c67943c5315221c3f72`.**
It is `status = "draft"` and authorizes nothing. Because it lives outside this checkout, this
work order's change set and its formal snapshot are untouched by it: the artifact count here
remains 887 and the handoff binding holds. Validated with the released 0.6.0 evaluator in that
worktree: PASS, 888 artifacts, 0 errors, 50 warnings, and `inspect` reports 167 findings with
0 errors and 64 warnings, unchanged in composition. It relates to `REQ-RLO-015`,
`REQ-RLO-016`, `SPEC-RLO-005`, `ARCH-RLO-005`, `ADR-RLO-005`, and `VER-RLO-005`, amends none
of them, and declares no path under `se_harness/` or `templates/`.

**Sequencing consequence, measured rather than assumed.** If `WO-RLO-006` reaches
`implemented` before the candidate commit, the candidate will carry an ungated work order's
changes. That is the same shape as the stop condition, so the distributed surface was
measured: `pyproject.toml` distributes the `se_harness*` packages, six named JSON files as
package data, and an enumerated list of `templates/repository/standard/**` data files, and
`MANIFEST.in` adds only `scripts/normalize_sdist.py`, `se_harness/*.json`, and the skills
trees. **`.github/` appears in neither, so `WO-RLO-006` would place zero bytes in the wheel
or the sdist.** The stop condition guards packaged bytes, and it therefore does not fire.
What would remain true is narrower and must be disclosed rather than waved past: the
publication-rehearsal evidence for 0.7.0 would be produced by code from a work order the
approved `gates` does not name.

## Stop-condition watch: three open pull requests

`origin/main` did not move during this execution, but three open pull requests bear on the
frozen `gates`. All three were re-enumerated after the amendment; the third was discovered
then and is not covered by any decision.

**Pull request #155, `WO-AEX-006`, held by owner decision.** The owner decided to hold it
open until v0.7.0 is tagged, so `WO-AEX-006`'s exclusion is a branch-point boundary. Read
at the branch point: `WO-AEX-006` is `approved`, not `implemented`, and is not in `gates`.
The exclusion holds trivially, and it holds only as long as the hold does.

**Pull request #156, `WO-RSK-001`, is a live threat to the approved contract and is not
covered by any decision.** It is open, `MERGEABLE` against `main`, carries the trailer
`Harness-Work-Order: WO-RSK-001`, changes 47 files of which **19 are in the packaged
surface** — including `se_harness/cli.py`, `se_harness/workflow.py`,
`se_harness/workflow_contract.py`, `se_harness/quality_gates_contract.json`, and eleven
managed template paths. `WO-RSK-001` does not exist on `main` and is **not** in
`REL-SEH-015`'s `gates`.

If #156 merges before the candidate commit, `REL-SEH-015`'s approved `gates` immediately
stops describing the release. That is the stop condition this work order must report
rather than edit, and the only remedy is rejecting `REL-SEH-015` and issuing
`REL-SEH-016` — the fourth contract succession the owner explicitly decided to avoid.

**Decided: the owner held #156 until 0.7.0 is tagged**, on the same reasoning as the #155
hold. `REL-SEH-015` is not reopened.

**Pull request #157, `WO-AEX-007`, is a third instance of the same threat and has no
decision.** Discovered while enumerating identifiers for the `WO-RLO-006` routing, after the
first three decisions were taken. Open, **MERGEABLE** against `main`, trailer
`Harness-Work-Order: WO-AEX-007`, 21 files of which **9 are in the packaged surface**:
`se_harness/cli.py`, `se_harness/delegated_workflow.py`, `se_harness/mutation_guard.py`,
`se_harness/workflow_contract.py`, `se_harness/workflow_contract.json`, and four
`templates/repository/standard/**` paths including two managed policy documents.
`WO-AEX-007` is `approved`, not `implemented`, and is **not** in `gates`.

The consequence is identical to #156's and so is the only remedy.

**Decided on 2026-08-25: all three open pull requests are held and will be merged after the
0.7.0 release is done.** The owner took this as one decision covering the whole set, which
supersedes the earlier per-pull-request framing and extends the standing #155 and #156 holds
to #157. `REL-SEH-015`'s `gates` therefore stays frozen at 36 and no fourth contract
succession is issued.

Two obligations follow from that decision and belong to this work order rather than to the
holds:

1. The exclusions must be **re-confirmed at the candidate**, not assumed from this reading.
   `WO-AEX-006`, `WO-AEX-007`, and `WO-RSK-001` must each still be absent from `gates` and
   absent-or-unimplemented in the graph at the exact candidate commit, and the census must be
   re-derived there.
2. The hold is a decision about merge order, not about content. If any of the three lands
   before the candidate commit despite it, the stop condition fires exactly as described
   above and must be reported rather than absorbed.

## Residual risks carried forward without softening

These are disclosed limitations of coverage the release unit already holds. None is
re-litigated here, and every one must reach `VREC-SEH-013` unsoftened.

1. **`VER-TCM-001`'s two independent reviewer judgments do not exist.** `WO-TCM-001` holds
   verified coverage through `VREC-TCM-002` because the assurance owner verified with that
   gap as accepted residual risk. `WO-TCM-001` cannot cleanly conform to its verification
   contract until those judgments are recorded, which is later governed work.
2. **`VER-ADS-001`'s Scenario 8 independent-reviewer classification was never run.**
   `VREC-ADS-001` and `VREC-ADS-002` both disclose it, and this stage resolves nothing
   about it.
3. **`VREC-ADS-001` and `VREC-ADS-002` were verified with the Linux figure pending the
   pull-request lane.** This stage took no hosted reading, so that remains pending.
4. **`WO-AEX-005` contributed four new runtime modules that are unreachable from
   `se_harness/cli.py` and therefore inert in 0.7.0.** They ship; they cannot be invoked.
5. **Eleven gated work orders declare no `[execution_scope]`**, limiting the containment
   check as described above.
6. **The byte-rule guard is blind to an assertion on an undeclared extension.**

## Deferred to the exact candidate

Each of these is unmeasurable now for a stated structural reason, not skipped.

| Deferred work | Why it cannot be measured yet |
| --- | --- |
| `qualify complete-candidate` PASS | `RID015` needs the full candidate commit; `RID009`/`RID018` need an isolated environment. |
| Candidate-source identity with metadata resolving inside the checkout | Same three diagnostics. |
| Formal governor-succession assessment | `validate_governor_transition.py plan` requires a clean worktree. |
| `renumber-artifacts` plan beyond `blocked` | Requires a clean worktree. |
| Two recipe-bound replays and byte-identity proof | Needs explicit build authority, and needs a schema-2 distribution subject that only `RLS-SEH-013` will create. |
| Release bundle manifest bound to `release/build-recipe.json` | Same build authority. |
| Candidate-package identity and verifier-owned black-box acceptance | Needs an exact candidate wheel from an authorized build. |
| `qualify candidate-package` and `qualify public-install` | Need a candidate wheel and a published wheel respectively. |
| Hosted lane results, run, job, and artifact identities | Needs the authorized branch push. |
| Linux suite figures with zero skips | Needs the hosted lane. |
| Hosted Windows publication-rehearsal reading at 3.11 | Needs the hosted lane; it is the fact that settles blocker B. |
| Changed-path ledger, protected-control diff, secret scan, `git diff --check` | Bind an exact commit. |

**One environmental constraint, surfaced early rather than at the build:** Docker is not
installed on this host, so the digest-pinned Linux/amd64 recipe replay cannot run here at
all. The two recipe-bound replays will need a Linux/amd64 Docker host or a hosted lane.

## Unperformed transitions and external actions

None of the following was performed, and none is authorized by this stage: candidate
commit; branch push; `WO-RLS-011` transition to `implemented`; `VREC-SEH-013` capture,
preparation, or transition; `RLS-SEH-013` preparation, distribution binding, or
transition; any change to `REL-SEH-015`; promotable build; tag creation or movement;
GitHub Release; PyPI publication; Pages deployment; `release/0.7` maintenance-line
creation or mutation; credential use; external policy change; root evaluator, root lock,
or managed-root upgrade; merge of any pull request; force push; and history rewrite.

## Planned aggregate VREC inputs

For `VREC-SEH-013`, on the whole-`gates` basis `REL-SEH-015` states:

- **36** work orders, exactly the `gates` array.
- **21** verification contracts, derived from those members.
- **37** work-order-keyed evidence paths, being the 36 that exist plus this file.
- One clean candidate commit, one artifact snapshot, and matching evaluator evidence.
- The combined-evidence file
  `technical-communication/evidence/WO-TCM-001/WO-TCM-002-verification.md` is keyed by the
  directory-position rule to both `WO-TCM-001` and `WO-TCM-002` and counted once.

Every one of those three counts must be re-measured against the candidate at capture. No
figure in this file may be carried forward as scope.

## Exact-candidate stage: identity and binding

Everything from here to the end of this file is stage 2. It was measured after the candidate
commit existed, and it supersedes any stage 1 figure that speaks to the same quantity.

| Item | Identity |
| --- | --- |
| Candidate commit | `f76da5727e86fc53375bfa5cafcfcbf168c7456e` |
| Candidate tree | `52fdae8c6e090f62341df8b87c52fc308d5132f7` |
| Candidate parent | `826c72cfdaa3401cccf06c67943c5315221c3f72`, the true merge of pull request #154 |
| Candidate branch | `chore/wo-rls-011-0-7-0-qualification` |
| Candidate product version | `0.7.0` in `pyproject.toml`, `se_harness/__init__.py`, and the current `README.md` install example |
| Governing evaluator, unchanged | exact public `se-harness` 0.6.0, as `.engineering-harness.toml` records |
| Artifact snapshot at the candidate commit, CRLF checkout | `cffd7b4fa038f03a01a6e31bde09a347dc1bd6db5f36ed1406923802ed7c411a` |
| Artifact snapshot after the `implemented` transition, CRLF checkout | `0a507c964fbf3fd0df72b8864967a96c0d00515408f432c4bfb6f6e0e4c2467e` |
| Artifact snapshot in the governance commit, CRLF checkout | `ee4e1c7e02be4b48403d6c4552ad6887ed7ab168ed18584b34adec1f529cbe6b` |

The candidate is exactly its parent plus **eight changed files**, `835` insertions and `11`
deletions: `README.md`, `docs/engineering/README.md`, this evidence file,
`docs/engineering/release-0-7-0/work-orders/WO-RLS-011.md`,
`docs/notes/developing-se-harness.md`, `pyproject.toml`, `se_harness/__init__.py`, and
`tests/test_release_qualification.py`. All eight fall inside the seven declared
execution-scope paths; `docs/engineering/release-0-7-0/` is a directory and covers two of
them. **No held bytes leaked in**: the diff contains nothing from any work order the
approved `gates` does not name.

**The binding block at the top of this file is not re-pointed, and that is deliberate.** It
names the `handoff` gate reading that authorized the `implemented` transition, together with
the snapshot that reading cleared against. Re-pointing it would destroy the record of what
the owner actually decided on. The three snapshots above are stated as measurements instead,
and the second and third are explained below.

## Exact-candidate stage: the artifact snapshot is a per-checkout figure, not a per-commit one

`formal_snapshot_digest` hashes each artifact's bytes **as they sit in the working tree**,
via `read_bytes()`, in relative-posix order with each path and content length framed. This
checkout has `core.autocrlf=true`, so every artifact is CRLF on disk while the committed blob
is LF. Measured, not inferred, by checking the same commit out twice into throwaway worktrees:

| Checkout of `f76da5727e86fc53375bfa5cafcfcbf168c7456e` | Snapshot digest |
| --- | --- |
| `core.autocrlf=true`, CRLF on disk | `cffd7b4fa038f03a01a6e31bde09a347dc1bd6db5f36ed1406923802ed7c411a` |
| `core.autocrlf=false`, `core.eol=lf`, LF on disk | `16e1ef528a74ad3131aa7162686a63cd09644021e0b5514296223e76b6798a9b` |

**Consequence for `VREC-SEH-013`, stated now rather than discovered at capture: a
`formal_snapshot_sha256` is a statement about one checkout of one commit on one platform, not
about the commit.** The hosted `ubuntu-latest` lane checking out this same candidate will
compute `16e1ef52…`, not `cffd7b4f…`, and neither figure is wrong. Any record that binds a
snapshot digest must therefore say which checkout produced it, and a reviewer comparing a
Windows figure against a Linux figure is comparing two different measurements. Both worktrees
used to take this reading were removed afterwards.

The two later snapshots move for reasons that are fully accounted for:

- `0a507c96…` differs from `cffd7b4f…` by exactly the `[[lifecycle_events]]` entry the
  `implemented` transition appended to `WO-RLS-011.md`. Nothing else in the artifact set
  changed.
- `ee4e1c7e…` differs from `0a507c96…` by exactly the `## Lifecycle` prose correction the
  governance commit makes to the same file.
- **This file is not an artifact** — it carries no `+++` front matter and the released
  evaluator's loader does not enumerate it, confirmed by measurement — so extending it moves
  no snapshot. That is what makes stating `ee4e1c7e…` inside the file it describes
  non-circular.

Re-measured after the governance commit's edits and before it was written: `validate` still
reads **887 artifacts, 0 errors, 50 warnings**.

## Exact-candidate stage: governing readings from the released 0.6.0 evaluator

Every reading in this section was taken with the exact independently installed public
`se-harness` 0.6.0 evaluator, from outside the checkout, in isolated mode, against the clean
candidate commit. The in-tree CLI is refused for root operations by mutation guard `MG005` on
runtime identity, which is the boundary working as designed and not a defect.

| Reading | Result |
| --- | --- |
| `validate` | **PASS** — 887 artifacts, 0 errors, 50 warnings, every plane at `E0` |
| `inspect` | 887 artifacts, 3235 relations, **167 findings: 0 error, 64 warning, 103 info** |
| `doctor` | **87 PASS, 0 FAIL** |
| `preflight --phase review` | **PASS** |
| Managed-root `upgrade` plan | **36 files, 36 unchanged** |
| `validate_release_distributions.py` | **PASS**, one distribution-bearing record |
| `check_portable_release_surface.py --wheel … --repository .` | **PASS** |
| `validate_governor_transition.py plan` | **PASS**, `transition_required: false` |
| `rehearse-recovery` | **PASS** — synthetic 0.7.0, 7 stages, 3 negative cases, every restoration invariant true, no external action |
| `check --checkpoint handoff` | **Completed**, naming `DR-WO-COMPLETE` |

The 64 `inspect` warnings decompose as 50 validator warnings — 21 `W013`, 14 `W014`, 15
`W015` — plus 14 derived warnings: 4 `W-HEX-002`, 9 `W-HEX-003`, 1 `W-REV-003`. All 50 are
the pre-existing maintenance population stage 1 dispositioned; none is new at the candidate.

The governor-succession plan is the reading that matters most for the release boundary, so its
identities are recorded in full. Base and target both resolve to the same governor: lock
schema 3, lock digest
`abcb1fe70b0eab96b106378bc1549b11e65cf5fe23d9c4cafccfdd28a3bf3f79`, evaluator
`se_harness-0.6.0-py3-none-any.whl` at archive digest
`2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7` with payload manifest
`se-harness-installed-payload-v1` at
`c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42`. The plan's
`lock_materialization_sha256` block records the LF and Git materializations as equal at
`abcb1fe7…` and the CRLF materialization as
`978cebb7824b7928d95ed43897b0f848441cc4ab7403a0cdd08a55a77df2b79e`, which is the same
line-ending sensitivity the snapshot section documents, handled explicitly by the lock format.
`transition_required` is `false` with an empty `diagnostics` array and `applied: false`:
**the released 0.6.0 evaluator governs the 0.7.0 candidate root with no version-specific
exception and no succession.** `base_source` is `event`.

## Exact-candidate stage: candidate-controlled readings

These were taken from the candidate checkout itself and are candidate-controlled, therefore
non-authoritative by construction. They are recorded because the work order requires the
candidate's own `qualify` boundary behaviour, not because they carry authority.

`qualify complete-candidate` — **passed**, `completion: completed`, schema
`se-harness-release-qualification-v1`, `independence: candidate-controlled`, authority
recorded in the payload as "evidence-only; no lifecycle or external action authorized":

| Check | Subject | Result |
| --- | --- | --- |
| `CC001` | `candidate-runtime` | pass — candidate runtime is bound to the checkout |
| `CC002` | `candidate-commit` | pass — HEAD and tracked tree match the candidate |
| `CC003` | `engineering-graph` | pass — `artifacts=887; errors=0; warnings=56` |
| `CC004` | `repository-state` | pass — target state is unchanged |

Its evaluator block is the candidate-source identity reading that stage 1 deferred: role
`candidate-source`, version `0.7.0`, distribution `se-harness`, identity digest
`14f9dfe17e3ae551ce6be2ae652b24698540fc956db04209f78ac7a6d986e224`, `candidate_commit`
`f76da5727e86fc53375bfa5cafcfcbf168c7456e`, empty `diagnostics`, `isolated_python: false`,
`pythonpath_present: false`, `user_site_enabled: false`. Distribution metadata resolves
inside the checkout, which is what the candidate-source role requires and what makes
`RID018` absent. The target block records `kind: complete-candidate` with identity digest
`423c5c5e2691006734db4a30c52dbc72d4e4cdfd39c5aba8cf7a9696ad036856`.

**`CC003` reads 56 warnings where the governing evaluator reads 50.** That is the candidate
validator carrying six additional derived warnings the released one does not emit, and it is
expected candidate-versus-released skew rather than graph damage: the governing figure is 50
and it is the one that counts. Recording both is the point.

Two further candidate-controlled readings: `renumber-artifacts` refuses with **`REN043`**, a
stated boundary refusal rather than the `blocked` outcome stage 1 could only observe from a
dirty tree; and the byte-rule inventory covers **57 declared paths at zero carriage
returns**, matching `.gitattributes`' nine declared patterns.

## Exact-candidate stage: verifier-owned black-box package acceptance

Ten of ten scenarios **passed**. This was run by the verifier against an ephemeral,
explicitly non-promotable 0.7.0 wheel built outside the checkout, which the approved work
order permits for package acceptance and which authorizes no promotable build.

- Verifier: `se-harness` **0.6.0**, wheel digest
  `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`, contract digest
  `a443e93d6da7d0538bdf790a16f4dea49ac7a6ede384c65e40362627d7a84b75`. The wheel was
  independently re-downloaded from PyPI for this reading and its digest equals the one
  `RLS-SEH-012` binds, so the verifier is provably the released artifact and not a local
  rebuild.
- Candidate under test: commit `f76da5727e86fc53375bfa5cafcfcbf168c7456e`, version `0.7.0`,
  wheel digest `b2f115ea5bc061638bb7cbe03fab3093af396eb5d707b8fc44f816d0439bcdfe`.
- Runtime: CPython **3.14.6**. Schema `se-harness-functional-acceptance-v1`.

| Scenario | Outcome | Output digest |
| --- | --- | --- |
| `installed-identity` | passed | `23ed00195b101e2671e4737d571216254ba298654f1250b08b267d97e1d14a4e` |
| `init` | passed | `99602ff1a4b39e95975b69aad9fa97d1f5100a7b01b32ae181f007352473c481` |
| `adopt` | passed | `8b8bed020673d8ed4c0eb8b20873d39956b1145071e914952677989d01e787cb` |
| `doctor` | passed | `b11dfbc1284a1ccf92c692370c7e9dd845ce1afc9189e9a0e6e71a65f49814d4` |
| `validate` | passed | `8316ba2d7f4f97caeb4b0f7845e1a6e5681cba228ba9d56d8cefc58b8cb6cb8a` |
| `dashboard` | passed | `69184a108b4f8014b68e8b2f3ff4d735ddbd8d3ddadbefb308b17e5a6f185c09` |
| `safe-upgrade` | passed | `bbf7ab50b76f38bbcb0e3f8b5d258b0d0a6abbd35674ef027dd8cf77d2132bb2` |
| `customized-content-refusal` | passed | `f7d505e8d22a49b00b4942dad35c9ed161eed2a8b9a3fd888aca1598c31e758d` |
| `corrupted-integrity-refusal` | passed | `35ca80881f23cc14bd0a43d48400d1a33a527143901376bcf0289891fcddb3bd` |
| `authority-denial` | passed | `f5c5912d2db40d37d2b92afdf207126058d8cde8111d9c0cf4da518750e72baf` |

**One reading of the acceptance interface was corrected during this stage and is recorded so
nobody repeats the mistake.** `--verifier-wheel-sha256` was initially read as the digest of a
second, independent build of the candidate. It is not: the source passes it as
`evaluator_wheel_sha256` with `role="released-evaluator"`,
`expected_version=__version__` and `require_isolated_python=True`, so it is the **verifier's
own evaluator wheel digest**. Reading it the other way would have produced a claim of
cross-build byte identity that this stage never measured.

The checkout was byte-for-byte unchanged by the acceptance run.

## Exact-candidate stage: credential-free publication rehearsal

Run on Windows at the exact candidate, in `candidate` mode, on both locally available
runtimes. Twenty-three mechanics, no credential present, no external write attempted.

| Runtime | Verdict | Unit suite | Teardown |
| --- | --- | --- | --- |
| CPython **3.14.6** | **REHEARSED** | passed, **1002 tests** | 6727 derived paths removed without following a link |
| CPython **3.11.9** | **FAILED** | exited 1 with **2 failing tests** | 7552 derived paths removed without following a link |

The 3.11.9 failure is exactly and only
`test_a_link_out_of_the_root_is_unlinked_and_its_target_survives` and
`test_a_linked_root_is_refused_rather_than_followed`. **This is blocker B, it is pre-existing
at the candidate's parent, and the candidate does not cause it.** The defect is in
`.github/scripts/rehearse_publication.py`, where `_path_is_junction` resolves
`os.path.isjunction` and `_is_link` resolves `DirEntry.is_junction` through `getattr(...,
None)` and returns `False` when the attribute is absent; both are 3.12-only, so on 3.11 the
junction predicate silently degrades. `.github/` is outside this work order's execution
scope, so it is **not repaired here**: the owner routed it to `WO-RLO-006`, which is
separately approved and separately started.

Everything else in both runs executed identically and is what the release path depends on:
temporary-path identity confined to the rehearsal root; release-record format validation
accepting `RLS-SEH-012` and refusing 6 non-canonical forms; evaluator resolution, acquisition
with hash proof, and identity proof through the `harnessctl.exe` entry point; distribution
policy validation; canonical plan resolution; a bounded refusal document written and re-read
canonically; the candidate exported twice from the repository archive; pinned build tools
installed into a rehearsal-root environment; complete-candidate qualification at
`f76da5727e86`; the CLI smoke check; **two independent builds each producing
`se_harness-0.7.0-py3-none-any.whl`**; both sdists normalized at epoch **1787681167**; the
two distribution sets compared **byte-identical**; bundle assembly from the second set;
manifest creation for the first set and the assembled bundle; the second set's manifest
verified against the first set's plan; and the assembled bundle verified against the plan.

Both runs report the inherited checkout's `core.autocrlf=true` as a stated condition. Neither
reports an unclean inherited checkout, unlike the earlier reading taken at the parent commit.

`check-divergence` reads **`verdict: exact`** against orchestrator
`.github/workflows/publish-pypi.yml` and rehearsal lane
`.github/workflows/publication-rehearsal.yml`, over platforms Linux and Windows with
`permissions_read_only: true`. Of 23 mechanics, **22 are covered and 1 is rehearsal-only**.
Five orchestrator jobs are excluded with their reasons recorded: `github_release` and
`observe` for `contents: write` and four `GH_TOKEN`-naming steps; `pages_build` and
`pages_deploy` for `pages: write`, `id-token: write`, a protected environment and the
external-state Pages actions; and `pypi` for `id-token: write`, a protected environment, a
`GH_TOKEN`-naming asset-verification step and `pypa/gh-action-pypi-publish`. **That is the
credential seam holding exactly where it should.**

**`recipe-bound-build-replay` excluded itself on both runtimes, and the reason is structural
rather than environmental.** Its own words: "no committed release record is a released
distribution-schema-2 subject with a bound build recipe; the 1 committed records declare
distribution schema 1, so this mechanic has no subject to replay". `RLS-SEH-012` is the one
distribution-bearing record and it is schema 1. **The mechanic is therefore unavailable, not
untested, and the dependency runs record → replay.** Granting build authority now would not
make it run; only a schema-2 `RLS-SEH-013` under preparation creates a subject. This is why
build authority should be sequenced *with* `RLS-SEH-013` preparation and not ahead of it. It
is a different constraint from the separate local one that no Docker host is installed here,
which independently blocks the digest-pinned Linux/amd64 replay recipe on this workstation.

## Exact-candidate stage: determinism, changed-path ledger, and protected controls

Explorer generation ran twice at the candidate into two external output directories and was
**deterministic**: 1037 files each time, with only `elapsed_ms` and `generated_at` differing.
Both runs report `PASS | Artifacts: 887 | Relations: 3235 | Errors: 0 | Warnings: 64` and the
**same manifest digest**
`db9069cab01c0f931d09b762a8b7c0a862107af4934b0e043e4f401c3ac2e563`; the dashboard digest is
`bfc5d0bcfd84ba8801406290793734b4aef9655d8f05fe81064934941d009ee9`.

| Reading | Result |
| --- | --- |
| Changed-path ledger, `v0.6.0` to the candidate | **536 paths** |
| Candidate against its parent | **8 files**, 835 insertions, 11 deletions |
| Protected-control diff, parent to candidate | **empty** — no managed, hash-locked, or fragment-mode path moved |
| `git diff --check`, parent to candidate | **clean** |
| Secret and private-path scan over the candidate's added lines | **no credential material of any form** |

The scan's only hits are two occurrences of an operator-home absolute path naming the
external evaluator environments, in this file. They are disclosed rather than removed: the
same path form already appears in **34 other tracked files** at the candidate's parent, so
this is an established retained-evidence convention in this repository and not a new
disclosure class introduced by the candidate. It is recorded here so a later decision to
scrub the convention can be taken deliberately, across all of it, under its own work order.

## Exact-candidate stage: aggregate census re-derived at the candidate

Re-derived at the candidate from `REL-SEH-015`'s `gates` array in the contract file itself,
never carried forward from prose and never inferred from commits or dates. `REL-SEH-015` is
`approved`, so that array is fixed authority.

| Figure, whole-`gates` basis | At the candidate | At approval | Moved? |
| --- | --- | --- | --- |
| `gates` entries, unique | 36 / 36 | 36 / 36 | no |
| Duplicate entries | 0 | 0 | no |
| Members absent from the graph | 0 | 0 | no |
| Members not at the expected status | 0 | 0 | no |
| Historical members with no verified coverage | **0** | 0 | no |
| Verification contracts | **21** | 21 | no |
| Requirement union | **48** | 48 | no |
| Members with keyed evidence | 36 of 36 | 36 of 36 | no |
| Distinct keyed evidence paths that exist | **37** | 37 | no |

The 21 contracts, enumerated so `VREC-SEH-013` can be checked against a list rather than a
count: `VER-ADS-001`, `VER-ADS-002`, `VER-AEX-001`, `VER-AEX-002`, `VER-AEX-003`,
`VER-AEX-004`, `VER-DST-001`, `VER-HBI-001`, `VER-HUP-004`, `VER-IPK-001`, `VER-LRE-001`,
`VER-REB-006`, `VER-REB-007`, `VER-REB-008`, `VER-REB-009`, `VER-REB-010`, `VER-RLO-004`,
`VER-RLO-005`, `VER-TCM-001`, `VER-VSP-002`, `VER-WEX-003`. On the historical-only basis,
excluding `WO-RLS-011` itself, the figures are 20 contracts and a 47-requirement union.

**The census is unchanged from approval, and that is the measurement the work order exists to
make, not an assumption it was allowed to carry.** Zero uncovered members means every
historical member reads `implemented` with verified coverage at the candidate.

Two containment checks were run against the `gates` array rather than trusted:

- **Every one of the 36 gated work orders has a file touched since `v0.6.0`.** Of the 44
  work-order files touched in that range, 8 are not in `gates`: `WO-AEX-006`, `WO-AEX-007`,
  `WO-AEX-008`, `WO-HUP-002`, `WO-REB-006`, `WO-REB-007`, `WO-RLS-009`, `WO-RLS-010`.
  `WO-RLS-009` and `WO-RLS-010` are the rejected predecessors of this work order and carry no
  bytes. The other six are dispositioned below.
- **102 work orders sit outside `gates` at `implemented` or `in_progress`.** That is the
  expected shape: `gates` is a per-release allow-list, not a repository census, and the great
  majority of those predate `v0.6.0` and are already covered by earlier release records.

## Exact-candidate stage: the census gap, disclosed and not corrected

**Thirty-seven work orders reached `implemented` after the `v0.6.0` tag. Three of them are
absent from the approved `gates` array.** This is disclosed to the release owner as a
measured fact about an approved contract, and it is deliberately **not** corrected: an
approved contract is never widened in place, and the correct remedy — if the owner wants one
— is rejection and re-issue, which is the owner's decision and not this work order's.

| Absent member | Implemented at | Declared scope paths | Of which distributed | Verified coverage |
| --- | --- | --- | --- | --- |
| `WO-HUP-002` | 2026-08-23T19:14:40Z | 43 | **0** | `VREC-HUP-005` verified (`VREC-HUP-003` rejected) |
| `WO-REB-006` | 2026-08-22T16:29:22Z | 0 | 0 | `VREC-SEH-012` verified |
| `WO-REB-007` | 2026-08-22T16:24:55Z | 0 | 0 | `VREC-SEH-012` verified |

**None of the three contributes a single byte to the packaged surface**, tested against the
distributed surface as `pyproject.toml` and `MANIFEST.in` actually declare it: the
`se_harness/` and `templates/repository/standard/` prefixes plus `pyproject.toml`,
`MANIFEST.in` and `scripts/normalize_sdist.py`. `WO-REB-006` and `WO-REB-007` declare no
`[execution_scope]` at all and were verified as part of the 0.6.0 aggregate. `WO-HUP-002`
declares 43 paths and not one of them is distributed; the approved work order also names it
explicitly as governance bookkeeping rather than release-bearing product work. **So the
release unit still describes the release, and the stop condition on "a work order whose bytes
are in the packaged surface and which the contract does not name" did not fire.** The gap is
a completeness question about the contract's narrative, not a correctness question about the
0.7.0 payload.

`RLS-SEH-012`, the 0.6.0 record, carries an **empty** `gates` array, so no comparison against
a predecessor allow-list is available and none was invented.

## Exact-candidate stage: the held pull requests, re-confirmed rather than assumed

The owner's standing decision is that the open pull requests merge after 0.7.0 is tagged.
That hold was re-confirmed against the candidate rather than carried forward as an
assumption, and the three work orders it covers are `approved` only — never `implemented` —
so none is admissible to the unit regardless.

| Held work order | Declared paths | Paths already changed since `v0.6.0` | Of which distributed |
| --- | --- | --- | --- |
| `WO-AEX-006` | 20 | 11 | 6 |
| `WO-AEX-007` | 33 | 21 | 12 |
| `WO-AEX-008` | 25 | 31 | 18 |

**Those distributed overlaps are not leaks, and the distinction matters.** Every distributed
path in the three lists — `pyproject.toml`, `MANIFEST.in`, `se_harness/agent_contract.py`
and its JSON, `se_harness/mutation_guard.py`, `se_harness/runtime_state.py`,
`se_harness/cli.py`, `se_harness/provenance.py`, `se_harness/workflow.py`,
`se_harness/workflow_contract.py` and its JSON, `se_harness/skill_contract.py`, the
`WORKFLOW.json` and `WORKFLOW.md` templates, and the twelve `.agents/skills` plus three
`.claude/skills` template files — is **independently declared by a work order the approved
`gates` does name**, and the bytes at the candidate are that gated work order's bytes. The
proof is direct rather than inferential: the candidate is its parent plus eight files, none
of which is in `se_harness/` other than `__init__.py`'s version line.

**A fourth open pull request was found during this stage and is reported rather than
absorbed.** It carries `WO-RSK-002`, is stacked on the pull request carrying `WO-RSK-001`,
declares 12 distributed paths, and drafts a governor-upgrade work order whose own
precondition needs a released record covering `WO-ADS-001`, `WO-ADS-002` and `WO-RSK-001` —
which is to say it depends on 0.7.0 existing. It is treated as covered by the standing
"merge after 0.7.0" hold on the same reasoning as the other three, and the owner is invited
to correct that reading if the hold was meant to enumerate only the three then known.

## Exact-candidate stage: no digest measured here is bindable

**Stated plainly because it constrains the next stage: not one distribution digest measured
on this workstation may be bound into `RLS-SEH-013`.**

The normalized 0.7.0 wheel digest differs by interpreter. Measured:
`2a739ea0e1c819ddee1ecf6a6b5d7711872699842d37fe39a5c50d965cf8dba1` from CPython 3.11 and
`a0e405c3e075f6e2fb4440f5722ad7015cb3592245837b5e7fda7110f33fd5cd` from CPython 3.14. Two
raw, unnormalized `python -m build` runs outside the release path produced a third result
again — identical wheel size with a different digest, and sdists of 622640 and 622661 bytes —
which is expected of unnormalized builds and is precisely why the release path uses
`SOURCE_DATE_EPOCH` together with `scripts/normalize_sdist.py`.

**Reproducibility therefore holds *given* the interpreter, and only given it.** Both
rehearsal runtimes built 0.7.0 twice byte-identically within themselves, which is the property
the release actually needs; what does not hold is byte identity *across* interpreters. The
binding digest must come from the authorized build on the platform and runtime the release
record names, and the figures above are recorded as boundary evidence rather than as
candidates for binding.

## Exact-candidate stage: deferred work discharged

Row by row against stage 1's *Deferred to the exact candidate* table.

| Deferred work | Disposition at the candidate |
| --- | --- |
| `qualify complete-candidate` PASS | **Closed** — passed on `CC001`–`CC004`. |
| Candidate-source identity with metadata resolving inside the checkout | **Closed** — role `candidate-source`, identity `14f9dfe1…`, empty diagnostics. |
| Formal governor-succession assessment | **Closed** — PASS, `transition_required: false`. |
| `renumber-artifacts` plan beyond `blocked` | **Closed** — refuses with `REN043`, a stated boundary refusal. |
| Changed-path ledger, protected-control diff, secret scan, `git diff --check` | **Closed** — 536 paths, empty protected diff, no credential material, clean. |
| Candidate-package identity and verifier-owned black-box acceptance | **Closed** — 10 of 10 against an ephemeral non-promotable wheel. |
| Two recipe-bound replays and byte-identity proof | **Open** — needs build authority *and* a schema-2 subject that only `RLS-SEH-013` creates. No Docker host here either. |
| Release bundle manifest bound to the candidate's own `release/build-recipe.json` | **Open** — same build authority. The rehearsal's own bundle manifests were built inside a disposable rehearsal root and are not the release manifest. |
| `qualify candidate-package` and `qualify public-install` from the candidate | **Open** — `public-install` needs a *published* 0.7.0 wheel, which does not exist. The verifier-side acceptance above covers the package role; the candidate-side operations are not claimed. |
| Hosted lane results, run, job, and artifact identities | **Open** — the authorized branch push follows this commit; the readings are a later, separate act. |
| Linux suite figures with zero skips | **Open** — needs the hosted lane. |
| Hosted Windows publication-rehearsal reading at 3.11 | **Open** — needs the hosted lane. The local 3.11.9 reading identifies the defect precisely; the hosted reading is what formally settles blocker B, and `WO-RLO-006` is where it is fixed. |

The stage 1 note that no Docker host is installed on this workstation stands unchanged.

## Exact-candidate stage: residual risks, carried forward unsoftened

Stage 1's six residual risks are all unchanged at the candidate and every one must reach
`VREC-SEH-013` unsoftened. Nothing in stage 2 resolves any of them: `VER-TCM-001`'s two
independent reviewer judgments still do not exist; `VER-ADS-001`'s Scenario 8
independent-reviewer classification was still never run; `VREC-ADS-001` and `VREC-ADS-002`
were verified with the Linux figure pending the pull-request lane and this stage took no
hosted reading; `WO-AEX-005`'s four new runtime modules are unreachable from
`se_harness/cli.py` and therefore ship inert in 0.7.0; eleven gated work orders declare no
`[execution_scope]`, which bounds the containment check above to the members that do; and the
byte-rule guard's inventory is the set of declared patterns, so a concurrent change adding a
byte-exact assertion on an undeclared extension would reopen the Windows qualification
failure without the guard seeing it.

To those, stage 2 adds three:

7. **A `formal_snapshot_sha256` is a per-checkout figure.** Any record binding one must name
   the checkout that produced it, and Windows and Linux readings of the same commit are not
   comparable.
8. **Three work orders implemented after `v0.6.0` are absent from the approved `gates`.**
   None contributes packaged bytes; the contract's narrative is nonetheless incomplete, and
   only the release owner can decide whether that warrants rejection and re-issue.
9. **`recipe-bound-build-replay` has no subject until a schema-2 release record exists.** The
   mechanic is unavailable rather than passing, and no reading in this file should be taken as
   evidence that it works.

## Exact-candidate stage: the `implemented` transition

Applied with the governing released 0.6.0 evaluator from outside the checkout, in isolated
mode, on the accountable engineering owner's explicit `DR-WO-COMPLETE` decision, recorded at
**2026-08-25T18:43:37Z** as `in_progress` → `implemented` with `decided_by =
"engineering-owner"`. The command reported `Workflow transition: COMPLETED` and named the
next step as verification-record preparation via `capture-verification`, which is **not**
performed here and is not authorized by that transition.

Two facts about it are recorded rather than smoothed over:

1. **One noun in the recorded reason is wrong and is corrected in the work order's prose
   rather than rewritten in the event.** The reason says the change set was asserted complete
   over "the eight declared paths of the amended execution scope"; the amended scope declares
   **seven** paths and the candidate changes **eight files**. The set of bytes is exactly the
   intended one. A recorded lifecycle reason is immutable decision history, so the event is
   left untouched.
2. **The reason was rejected twice for length before it was accepted.** `--reason` is capped
   at 2000 characters and `WEX201` fires in argument validation, so the two `FAILED` verdicts
   at 2230 and 2076 characters said nothing whatever about the transition's legality. The
   accepted reason is 1844 characters. This is recorded because a `FAILED` transition verdict
   that originates in argument validation is easy to misread as a governance refusal.

After the transition the applicable gate changes: `check --checkpoint handoff` now returns
**`WEX210: gate QG-G4-CANDIDATE-READY does not apply at checkpoint handoff`**, because at
`implemented` the applicable gate is `QG-G4-CANDIDATE-READY`, evaluated when VREC preparation
is requested. `start` returns the same and `pre-action` returns `WEX220`, requiring
`--procedure`. **That is the lifecycle advancing, not a regression**, and it is recorded so a
later reader does not mistake the refusal for damage.

## Exact-candidate stage: unperformed transitions and external actions

This is the list that describes the state this file is committed in. It supersedes stage 1's
*Unperformed transitions and external actions*, which remains accurate as a statement about
stage 1.

**Performed, each on its own explicit owner decision of 2026-08-25:** the candidate commit;
this work order's `in_progress` → `implemented` transition; and the governance commit that
carries this stage. **Authorized and following immediately after this commit:** the push of
`chore/wo-rls-011-0-7-0-qualification` to `origin`, so the hosted `windows-2022` and
`ubuntu-latest` lanes can read the candidate. That push is a Git operation only — it merges
nothing, builds nothing, and creates or moves no tag. **Separately authorized:**
`WO-RLO-006`'s start, which is governed by its own work order.

**Not performed and not authorized by anything in this file:** a pull request; any merge;
`VREC-SEH-013` capture, preparation, or transition; `RLS-SEH-013` preparation, distribution
binding, or transition; any change to `REL-SEH-015`; any promotable build; the release bundle
manifest; either recipe-bound replay; tag creation or movement; a GitHub Release; PyPI
publication; Pages deployment; `release/0.7` maintenance-line creation or mutation; any
change to the root evaluator, the root lock, or the managed root; the pinned
`se-harness==0.6.0` evaluator instruction in the owner region of `AGENTS.md`; force push; and
history rewrite.

## Exact-candidate stage: planned aggregate VREC inputs, as measured

`VREC-SEH-013` must match, on the whole-`gates` basis, the figures **measured at the
candidate** and not the stage 1 figures:

- **36** work orders, exactly `REL-SEH-015`'s `gates` array, all `implemented` with verified
  coverage and zero uncovered.
- **21** verification contracts, enumerated above.
- **48** requirements in the union.
- **37** work-order-keyed evidence paths, being the 36 that exist plus this file — and
  exactly this file, because `REL-SEH-015` clause 10 says "the one `WO-RLS-011` retains",
  singular.
- One clean candidate commit, `f76da5727e86fc53375bfa5cafcfcbf168c7456e` at tree
  `52fdae8c6e090f62341df8b87c52fc308d5132f7`.
- One artifact snapshot, **named together with the checkout that produced it**.
- Matching evaluator evidence for the exact public 0.6.0 evaluator.
- `technical-communication/evidence/WO-TCM-001/WO-TCM-002-verification.md` keyed by the
  directory-position rule to both `WO-TCM-001` and `WO-TCM-002` and counted once;
  `WO-HBI-004` and `WO-RLO-005` each retaining two keyed files.

**Every one of those figures must still be re-measured at capture, against the commit
`VREC-SEH-013` actually binds.** The candidate is immutable from here, so they are expected
to hold — but "expected to hold" is not a measurement, and this file confers no authority to
skip taking one.
