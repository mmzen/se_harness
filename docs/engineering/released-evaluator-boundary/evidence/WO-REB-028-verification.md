# WO-REB-028 Predecessor-Bootstrap Retirement Evidence

Date: 2026-08-27

Authority: non-authoritative retained implementation evidence. This file does not approve, verify, release, publish, tag, or deploy anything. It records what was measured on one platform at one commit. `WO-REB-028` carries `commit_bound_verification = "required"`, so commit-bound assurance is a separate `VREC` decision by an accountable verifier and this file is not that decision. The work order was `in_progress` throughout every measurement below; the completion transition the repository owner directed afterwards is recorded in the work order's own lifecycle events, in a later commit on this branch. Section 12 lists seven coverage gaps and disclosures that are explicit inputs to that review, including two the work order's own text does not anticipate.

artifact: WO-REB-028
checkpoint: handoff
formal_snapshot_sha256: 7f36d03248d40fc5a525c77e71f53853256527d1099ac1ae37881cf32a16aa2f

## 1. Governing packet and preflight

`WO-REB-028` implements `REQ-REB-029` under `SPEC-REB-013`, `ARCH-REB-012`, `ADR-REB-012` and `VER-REB-012`. The five packet artifacts and the work order were transitioned `draft` to `approved` at `2026-08-27T16:43:16Z` on the accountable owner's single act, "I approve the artifacts". The work order moved `approved` to `in_progress` at `2026-08-27T16:56:39Z` on the owner's later decision, "you can start". The owner holds the requirements-steward, technical-owner, quality-owner, security-owner, release-owner, repository-owner and engineering-owner roles in this repository.

Every lifecycle act and every governor reading below used the exact public 0.6.0 evaluator installed in a virtual environment outside this checkout and run with `-I`:

```text
../se-harness-eval/Scripts/python -I -m se_harness --version
0.6.0

../se-harness-eval/Scripts/python -I -m se_harness preflight . --work-order WO-REB-028 --phase review
Harness preflight: PASS
Phase: review
Work order: WO-REB-028 (in_progress)
Assurance classification: commit-bound verification required, decided by repository-owner
exit code 0
```

## 2. Base commit and commits under this work order

Base: `f605e58`, `main` at "Merge pull request #197 from mmzen/governance/hup-006-rejection", `2026-08-27T17:57:04+02:00`.

Branch: `governance/reb-028-retire-predecessor-bootstrap`.

| Commit | Time | Subject |
| --- | --- | --- |
| `62f13c2` | `2026-08-27T18:57:08+02:00` | `governance(reb): approve and start WO-REB-028 to retire the predecessor-bootstrap path` |
| `b848b7a` | `2026-08-27T19:52:28+02:00` | `refactor(reb): retire the predecessor-bootstrap release path` |

`origin/main` advanced to `f0ecd9b` while this work order was in progress, and that commit was merged into the branch as `cb56673`. Section 14 re-derives every figure the merge moved and records the resolution. A later commit on the same branch carries this evidence document and the packet index correction of section 11. It cannot record its own hash, so it is named here rather than listed above; it changes no code, no workflow and no governed artifact, and section 13 shows the handoff result is identical before and after it.

`git merge-base --is-ancestor f605e58 HEAD` holds. Nothing was pushed: the branch exists only in this checkout. All measurements below were taken at `b848b7a` unless stated otherwise.

## 3. The twelve deleted paths and their pre-deletion identity

Every path is absent from the worktree at `b848b7a`. Blob identity, line count and byte count are read from `f605e58`, so each row is recoverable from history by `git show f605e58:<path>`.

| Path | Pre-deletion blob | Lines | Bytes |
| --- | --- | --- | --- |
| `repository_tools/release_bootstrap.py` | `5d165ab36eecdf283431107982b007026d841532` | 979 | 42,435 |
| `repository_tools/predecessor_preparation.py` | `3adc494488fba57cd55337d81ff6106ceab2199c` | 1,167 | 51,675 |
| `repository_tools/predecessor_publication.py` | `d7ef8e08b7c45fa11fb325e5874ded7c2ce9be74` | 959 | 41,112 |
| `repository_tools/predecessor_assessment.py` | `4f0e3ff3329b7461206492ef5ee631a425f14a6a` | 746 | 30,529 |
| `scripts/bind_release_bootstrap.py` | `47267d7824748155cc98bbff3da666d997a842da` | 65 | 2,404 |
| `scripts/prepare_predecessor_release.py` | `6ea1670f4cb13421f9cce00b6dcb97024b4b2c95` | 76 | 2,936 |
| `scripts/validate_predecessor_publication_view.py` | `53423083d59266150fcd5665c31452dee24e92eb` | 76 | 2,706 |
| `scripts/assess_predecessor_evaluator.py` | `842a7a5d1b4e8b841302c3a8bbe42b7858d1dce3` | 69 | 2,561 |
| `tests/test_release_bootstrap.py` | `be7a3ba557383c6d980b014fa069a607ec648c5d` | 951 | 40,418 |
| `tests/test_predecessor_preparation.py` | `9506ee74b0372d6f971812434846af0eae4fcbeb` | 887 | 35,239 |
| `tests/test_predecessor_publication.py` | `f086614c6851a5bba14372b8ec6c9ed80ca42906` | 323 | 15,980 |
| `tests/test_predecessor_assessment_contract.py` | `f46296c6193bb5a4124ba19bf14ae80f6952cb5a` | 95 | 4,001 |

Total: 6,393 lines, 271,996 bytes, matching the figure the work order states.

Stale bytecode for the four deleted product modules and the four deleted test modules was removed from the untracked `__pycache__` directories, so no import can resolve through it:

```text
python -c "import repository_tools.release_bootstrap"
ModuleNotFoundError: No module named 'repository_tools.release_bootstrap'
```

The same result holds for `predecessor_preparation`, `predecessor_publication` and `predecessor_assessment`.

## 4. Released-governor readings before and after

Both readings are from the same exact public 0.6.0 evaluator outside the checkout. The base reading was taken in a throwaway detached worktree at `f605e58`, which was removed afterwards.

| Reading | Artifacts | Errors | Warnings |
| --- | --- | --- | --- |
| `validate` at `f605e58` | 976 | 0 | 53 |
| `validate` at `b848b7a` | 982 | 0 | 53 |

The difference is exactly six artifacts: `REQ-REB-029`, `SPEC-REB-013`, `ARCH-REB-012`, `ADR-REB-012`, `VER-REB-012` and `WO-REB-028`, this packet's own additions. Errors and warnings did not move, which is `VER-REB-012`'s second matrix row. All 53 warnings are maintenance-plane `W013`, `W014` and `W015` notices on retained legacy artifacts, unchanged from the base.

```text
../se-harness-eval/Scripts/python -I -m se_harness validate .
Artifacts: 982 | Errors: 0 | Warnings: 53

../se-harness-eval/Scripts/python -I -m se_harness doctor .
111 checks: 87 PASS, 24 WARN, 0 FAIL
exit code 0
```

## 5. Retained history: the six closed 0.6.0 artifacts

`git diff --name-only f605e58 HEAD` lists none of the six, so all six are byte-identical to their parent-commit content, `[bootstrap]` tables and `preparation_schema` markers included.

| Artifact | Blob at `b848b7a` | Retained marker |
| --- | --- | --- |
| `docs/engineering/release-0-6-0/release/REL-SEH-008.md` | `d14090b88ff6d1c032333d7a2454ca9a571854e5` | `[bootstrap]` |
| `docs/engineering/release-0-6-0/release/REL-SEH-009.md` | `9dda66cc2ac1020863f3a1d6199b55bbe72f9f95` | `[bootstrap]` |
| `docs/engineering/release-0-6-0/release/REL-SEH-010.md` | `61d3f8b0eca7c7a145805a359a08dc9e0e542f3c` | `[bootstrap]` |
| `docs/engineering/release-0-6-0/release/REL-SEH-011.md` | `849ca9f7e337591db3ae95ddaf0fae2f3f692e53` | `[bootstrap]` |
| `docs/engineering/release-0-6-0/releases/RLS-SEH-009.md` | `0b9661f570e8a85afa4acb4dd995eda57bfc7f67` | `preparation_schema = "se-harness-predecessor-bootstrap-v1"` |
| `docs/engineering/release-0-6-0/releases/RLS-SEH-012.md` | `090ad5f5b7779748b7a866df913d72aaf9f1372b` | `preparation_schema = "se-harness-predecessor-bootstrap-v1"` |

The three bound evidence digests were recomputed from the bound files in this worktree and every one still verifies:

| Record | Field | Bound file | Digest | Verifies |
| --- | --- | --- | --- | --- |
| `RLS-SEH-012` | `preparation_view_evidence_sha256` | `docs/engineering/release-0-6-0/evidence/RLS-SEH-012-preparation-view.json` | `77474d1e22422371d48f3d1a281810a6c7f9bf55982a17e565f602978bbab4d7` | yes |
| `RLS-SEH-012` | `evaluator_evidence_sha256` | `docs/engineering/release-0-6-0/evidence/RLS-SEH-012-evaluator.json` | `11a4aec338f1da102a112faca6589d18541e115e139e695e8d66e4d509125404` | yes |
| `RLS-SEH-009` | `evaluator_evidence_sha256` | `docs/engineering/release-0-6-0/evidence/RLS-SEH-009-evaluator.json` | `11a4aec338f1da102a112faca6589d18541e115e139e695e8d66e4d509125404` | yes |

`RLS-SEH-009` and `RLS-SEH-012` sharing one evaluator-evidence digest is expected and not a defect: the same evaluator environment yields the same evidence bytes, and the candidate binding lives in the record's commit and its dashboard snapshot rather than in the sidecar.

`REL-SEH-011` keeps `from_lock_sha256 = "08441ec0b4825db4c017ce4169f23092162995ff06476004d267f0671c7443b3"` with `from_lock_tool_version = "0.5.0"`. That digest binds the historical 0.5.0 lock, not this checkout's current `.engineering-harness.lock`, and `se_harness/hash_bound_classes.json` still declares the field under the `standard-lock` class in `utf8-text-lf-v1` mode. The three hash-bound checks pass from the candidate interpreter:

```text
hash-bound-class-declared: PASS - 3 classes cover 62 tracked paths; 9 digest fields declared out of scope
hash-bound-attribute-effective: PASS - 2 raw classes effective for 61 tracked paths
hash-bound-mode-consistent: PASS - one mode per class: evaluator-evidence=raw, governance-migration-protocol=raw, standard-lock=utf8-text-lf-v1
```

No evidence sidecar under `docs/engineering/**/evidence/` appears in the changed-path set, so all of them are byte-unchanged by a second route.

## 6. Installed-surface check against an ephemeral candidate wheel

`VER-REB-012` requires the installed-surface case to run against a built candidate wheel installed outside the checkout, never against candidate source. `AGENTS.md` permits an approved candidate-evidence work order to build explicitly non-promotable ephemeral wheels outside the checkout for package acceptance. One such wheel was built by reproducing the `candidate-source` recipe of `.github/workflows/candidate-evidence.yml` in a directory outside this repository:

```text
git archive b848b7a | tar -x -C C:\Users\mathi\reb028-pkg\candidate-export
python -m pip wheel --disable-pip-version-check --no-deps \
  --wheel-dir C:\Users\mathi\reb028-pkg\candidate-dist C:\Users\mathi\reb028-pkg\candidate-export

se_harness-0.7.0-py3-none-any.whl
sha256 f44ca11e59ce10f26ada73cb29e4193db58a5a79092b93b1c8c597671a6aa64a
482,740 bytes, 110 members
```

That wheel is candidate evidence, not a distribution. It was built on Windows, which cannot produce a build of record, it is bound by no release record and no manifest, its filename collides with the already-published 0.7.0, and it was deleted after the readings below. It must not be promoted.

The wheel was installed into a second virtual environment outside the checkout and the repository-owned surface checker was run against both the archive and the installed console script:

```text
python scripts/check_portable_release_surface.py --wheel <candidate wheel>
portable release surface: PASS
exit code 0

python scripts/check_portable_release_surface.py --harnessctl C:\Users\mathi\reb028-pkg\installed\Scripts\harnessctl.exe
portable release surface: PASS
exit code 0
```

The installed CLI publishes exactly four qualification operations and no fifth:

```text
C:\Users\mathi\reb028-pkg\installed\Scripts\harnessctl.exe qualify --help
usage: harnessctl qualify [-h]
                          {released-root,complete-candidate,candidate-package,public-install} ...
```

`predecessor-view` occurs zero times in that help output, `rehearse-migration` is present in `harnessctl --help`, and `PV001` and `PV002` occur in the installed package only as the reserved tuple in `se_harness/release_qualification.py`. The wheel's member list contains no `predecessor`, no `bootstrap` and no `repository_tools` member, and none of the four forbidden self-hosting members `candidate-evidence.yml` checks for.

`scripts/check_portable_release_surface.py --repository .` also passes at `b848b7a`. Its `FORBIDDEN_CLI` tuple now includes `predecessor-view`, so a reintroduction of the operation fails the check rather than shipping.

## 7. Workflow static review

| File | Change | Effect |
| --- | --- | --- |
| `.github/workflows/publish-pypi.yml` | 0 added, 47 removed | The `--release-record` argument is gone from the evaluator step, and the inline contract reader, the `qualify predecessor-view` branch and the exclusion-observation writer are deleted. |
| `.github/workflows/pages-publication.yml` | 11 added, 55 removed | The conditional "Validate with the released evaluator" step is replaced by an unconditional "Materialize the complete governance snapshot for generation" step. |
| `.github/scripts/publish_dashboard.py` | 3 added, 479 removed | `read_evaluator` loses its `release_record` parameter and now requires a schema-3 evaluator lock; `_validated_bootstrap_contract`, `_without_preparation_bindings`, `_validated_preparation_view`, `_bytes_at` and `_canonical_utf8_text_lf` are deleted. |

No remaining step references a deleted path, selects a record for a view, or branches on a contract-declared `[bootstrap]` tuple, and no step writes an exclusion observation. `candidate-evidence.yml` still resolves `repository_tools.predecessor_facts`, which is retained and untouched.

The `$RUNNER_TEMP/predecessor-view` temporary directory name is deliberately retained in `pages-publication.yml`. `SPEC-REB-013` rule 5 requires the generator invocation to stay byte-identical, and the generator reads its root from that path. The directory now always holds the complete governance snapshot at the governance commit, with nothing omitted for any record; the name is a path, not a behaviour.

## 8. Interpreter-safety declaration

`se_harness/interpreter_safety.json` declared eight boundaries at `f605e58` and declares two at `b848b7a`. Both remaining modules exist:

| Boundary | Kind | Module |
| --- | --- | --- |
| `se_harness.governance_migration.runtime_probe` | rule | `se_harness/governance_migration.py` |
| `se_harness.runtime_identity.installed_interpreter` | rule | `se_harness/runtime_identity.py` |

Six were removed, not the two the work order's bullet and `SPEC-REB-013` rule 7 name. Section 12 discloses this.

## 9. Repository gates at `b848b7a`

| Gate | Result |
| --- | --- |
| `python scripts/run_tests.py` | 943 tests, OK, skipped=22 |
| `python scripts/validate_engineering_artifacts.py --root .` | PASS, 982 artifacts, 0 errors, 53 warnings |
| `python scripts/validate_release_distributions.py --root .` | PASS, 3 distribution-bearing records |
| `python -m se_harness --help` | exit code 0 |
| `python scripts/check_portable_release_surface.py --repository .` | PASS |
| `../se-harness-eval/Scripts/python -I -m se_harness validate .` | 982 / 0 / 53 |
| `../se-harness-eval/Scripts/python -I -m se_harness doctor .` | 111 checks, 0 FAIL, exit code 0 |
| `../se-harness-eval/Scripts/python -I -m se_harness preflight . --work-order WO-REB-028 --phase review` | PASS |
| `python -m unittest tests.test_predecessor_bootstrap_retirement` | 15 tests, OK |

The suite count moved from 983 to 943 and the skip count from 24 to 22. A control run of the whole suite at `f605e58` in a throwaway worktree, on this same host, produced `983 tests, OK, skipped=24`, and both deltas reconcile exactly per module:

| Module | Base tests | Candidate tests | Delta |
| --- | --- | --- | --- |
| `tests/test_release_bootstrap.py` | 25 | absent | -25 |
| `tests/test_predecessor_preparation.py` | 14 (2 skipped) | absent | -14 |
| `tests/test_predecessor_publication.py` | 6 | absent | -6 |
| `tests/test_predecessor_assessment_contract.py` | 3 | absent | -3 |
| `tests/test_hash_bound_integrity.py` | 97 | 93 | -4 |
| `tests/test_interpreter_safety.py` | 89 | 87 | -2 |
| `tests/test_release_qualification.py` | 11 | 10 | -1 |
| `tests/test_release_orchestration.py` | 23 | 23 | 0 |
| `tests/test_dashboard_publication.py` | 23 | 23 | 0 |
| `tests/test_predecessor_bootstrap_retirement.py` | absent | 15 | +15 |

983 - 48 - 7 + 15 = 943, and the only two skips lost were the two Windows-only guards inside the deleted `tests/test_predecessor_preparation.py`. No test that passed at the base fails at the candidate.

`tests/test_predecessor_bootstrap_retirement.py` is the new absence-and-reservation module: 315 lines, 15 tests, four classes. Its import scan reads 6 trees and asserts it visited more than 100 files, so it cannot pass vacuously. `VER-REB-012`'s "every hash-bound field resolves for every artifact that carries it" property was not duplicated: `tests/test_hash_bound_integrity.py::test_this_repository_passes_every_check` already holds it.

## 10. Non-change proofs

`git diff --name-only f605e58 HEAD` lists 40 paths. None of the following appears in it, so each is byte-unchanged:

| Path | Blob at `b848b7a` |
| --- | --- |
| `scripts/validate_engineering_artifacts.py` | `5c3637b58636de0c224c0885e4ee99f6149e54bb` |
| `templates/repository/standard/scripts/validate_engineering_artifacts.py` | `a978702e09f38d544f6777d624b7c10150959145` |
| `se_harness/hash_bound_classes.json` | `68234638b0905a56b4ee140c82410b91866e537d` |
| `.engineering-harness.lock` | `d282bde74a7728a7ac4b4a957ea9212cc80f68c0` |
| `.engineering-harness.toml` | `fdeff45accb4fea446eab5f34c8b04785772c95a` |
| `.gitattributes` | `bb9a3d8d4de3015ebc3019ced8ab22a23e4fa495` |
| `AGENTS.md` | `97d59377483308ced278c08c225386e1be6a34d0` |
| `CLAUDE.md` | `af7294e0be990d06385b530d8912b7f77e0133cc` |
| `.gitignore` | `857a7dd42dd11c305d200f9d3570dc2882110d66` |
| `ENGINEERING_HARNESS.md` | `61c0b3cdddd856c339da9b5877162253a29999d4` |
| `docs/engineering/WORKFLOW.json` | `e17addd0acf47299a4b5ebce45079b0e61693a11` |
| `docs/engineering/QUALITY_GATES.json` | `a57c6070d2668b7647ed0ab9d81406a445200e20` |

`VER-REB-012`'s last required case states that leaving both `validate_engineering_artifacts.py` copies byte-identical is a pass condition, not an omission. The two copies are not byte-identical to each other, and were not made so: the root copy is released 0.6.0 and the template copy is candidate source for a later release. Their two conditional bootstrap rules are inert for any artifact without a `[bootstrap]` table or a `preparation_schema` marker, so leaving them changes no verdict.

No managed hash-locked path was touched: the three root managed files, the seven managed documents under `docs/engineering/`, all of `docs/engineering/templates/`, and the eight managed scripts are all absent from the changed-path set. No fragment digest moved. No refs or tags were created, moved or deleted: 79 refs and the ten tags `last`, `v0.2.0`, `v0.2.1`, `v0.2.2`, `v0.3.0`, `v0.4.0`, `v0.4.1`, `v0.5.0`, `v0.5.0a1`, `v0.6.0`, `v0.7.0` are unchanged. No credential was used, no network write was made, and no root change of this repository was performed. No promotable distribution was built; section 6's wheel is ephemeral candidate evidence and was deleted. No `VREC` or `RLS` artifact was created, transitioned or edited.

## 11. Retirement recorded by amendment, not by status

The work order's approval declares the supersession of `REQ-REB-012`, `REQ-REB-015` and `SPEC-REB-007`. Measurement showed the declared `superseded` status is not representable for these three artifacts, and the retirement was recorded by dated amendment instead.

Setting `status = "superseded"` produced six errors from the released governor:

```text
[E014] REQ-REB-012.md: last lifecycle event target 'approved' must equal artifact status 'superseded'
[E014] REQ-REB-015.md: last lifecycle event target 'approved' must equal artifact status 'superseded'
[E014] SPEC-REB-007.md: last lifecycle event target 'approved' must equal artifact status 'superseded'
[E016] ARCH-REB-004.md: active architecture addresses inactive requirement 'REQ-REB-012'
[E016] ARCH-REB-006.md: active architecture addresses inactive requirement 'REQ-REB-015'
[E016] ARCH-REB-006.md: active architecture conforms to inactive specification 'SPEC-REB-007'
```

Appending an `approved` to `superseded` lifecycle event to satisfy `E014` is refused in turn:

```text
[E014] REQ-REB-012.md: lifecycle event 2 contains unsupported transition approved -> superseded
```

`docs/engineering/WORKFLOW.json` gives the definition families only `draft -> approved, rejected` and `approved -> implemented, rejected`. `WORKFLOW.md` `WFL-005` states that `superseded` is terminal, applies only to a ready verification record with one eligible successor, and that historical lifecycle events must remain append-only. So the only two ways to set the status are to contradict the existing `draft -> approved` event or to delete it, and both are refused. `REQ-REB-005`, the one requirement in this repository that carries `status = "superseded"`, never carried lifecycle events at all, which is why it validates.

Each of the three artifacts therefore keeps `status = "approved"`, carries `updated = "2026-08-27"`, and gains a `## Retirement amendment of 2026-08-27` section as its first section. Each section states who retired the artifact, on what date, under which work order and successor, what is withdrawn, what survives as fact, and discloses the mechanical reason the status was not set. That is the same instrument the work order already authorizes for `SPEC-REB-003` and `SPEC-REB-005`, which gain an appended section of the same name.

This disposition also removed the `E016` cascade at its source. Applying the status would have forced edits to `ARCH-REB-004`, `ARCH-REB-006` and `ADR-REB-006` and, through their coverage, to about thirteen completed work orders, none of which is inside this work order's execution scope.

The validator reads 0 errors with the amendments in place. Whether the status is later applied through a new transition, or the definition family gains one, is a separate owner decision; the retirement itself does not depend on it.

## 12. Coverage gaps and disclosures

1. **The `superseded` status was not applied.** Section 11 records the measurement, the reason and the alternative used. The three artifacts read `approved` with a dated retirement amendment. This is a deviation from the approval's own wording and is an owner decision to confirm.
2. **Six interpreter-safety boundaries were removed, not two.** The work order's bullet and `SPEC-REB-013` rule 7 name two. Six sites named a deleted module or the deleted `release_qualification` external-evaluator path, and the rule's invariant — every declared site resolves to a present file — requires all six to go. Section 8 lists what remains.
3. **`repository_tools/interpreter_safety.py` now has no production caller.** It is retained deliberately and out of scope: it is the second independent loader that the conformance tests hold in agreement with the packaged one. Removing it would remove that agreement check.
4. **The `predecessor-view` temporary path name is retained** in `pages-publication.yml`, deliberately, so the generator invocation stays byte-identical. Section 7 explains it.
5. **Three out-of-scope notes still carry stale references** to the retired path: `docs/notes/evaluator-migration-rehearsal.md:67`, `docs/notes/harness-dashboard-publication.md:35` and `:88`, and `docs/notes/release-qualification-roles.md:25` and `:40`. They are ungoverned documentation outside this work order's execution scope and belong to a separate pull request that carries no work-order trailer.
6. **The packet README still labels `WO-REB-024`, `WO-REB-025` and `WO-REB-026` "(draft)"** although all three are `implemented`. Correcting those three lines is outside the declared index task, which is this packet's own entry, so they were left as they are.
7. **No hosted evidence exists.** `VER-REB-012` requires the pull request's own lanes, `publication-rehearsal` and `release-qualification` in both modes, and a dispatch-mode rehearsal of `publish-pypi.yml` and `pages-publication.yml` on the candidate branch, stating explicitly that static review of those two files is not sufficient on its own. That rehearsal needs a push and a hosted dispatch, and neither is authorized. Section 7 is static review only, and the requirement remains open. Nothing in this file substitutes for it.

## 13. Handoff checkpoint result

The complete changed-path set is the 40 paths of `git diff --name-only origin/main HEAD` at `cb56673`, passed as 40 repeated `--changed-path` arguments with `--changes-complete`. `QG-G4-IMPLEMENTATION-EVIDENCE` reads `pass`, with no scoped and no repository blocker; the 55 unrelated findings are the same maintenance-plane warnings sections 4 and 14 record. The exact public 0.6.0 evaluator outside the checkout returns:

```text
Outcome
Completed.

Done
- Evaluated handoff compliance for WO-REB-028.

Not done
None.

Current lifecycle state
- WO-REB-028 is in_progress.

Decision required
engineering-owner must decide whether the authorized implementation and evidence are complete for WO-REB-028 under DR-WO-COMPLETE; permitted outcomes: implemented, continue, reject.

Next
whether the authorized implementation and evidence are complete (PROC-WO-IMPLEMENT/STEP-WO-IMPLEMENT-DECIDE).

Command or response
Mark WO-REB-028 implemented.
```

`result_sha256` is `b18c0b374de2d942d928349519c68f5c6660442fd5464f895d4c4ba416fb7676`. Released 0.6.0 does not emit that field, so it was taken from the candidate CLI's own schema-2 result and checked back against the released block: the canonical digest of the released governor's result object equals it exactly, and both report the same `formal_snapshot_sha256`. The digest covers the `ADS-DIG-001` canonical bytes of the rendered restitution block alone — outcome, done, not done, lifecycle state, decision required, next step and command — and nothing else in the result object. This file's own bytes therefore do not enter it, so recording it here does not move it, and it is also unchanged across the merge that section 14 records: that merge moved the formal snapshot and the change set, both of which the block does not render, and not one rendered line. The reading above was taken again at `cb56673` after the merge and is byte-identical.

The decision this result asks for is the engineering owner's under `DR-WO-COMPLETE`. The repository owner took it on 2026-08-27 and directed the completion transition, the verification record and the pull request. This file is not that decision and is not the commit-bound assurance either: `VREC-REB-025` under `VER-REB-012` is, and section 12's seven gaps and disclosures, together with the merge disclosure of section 14, are explicit inputs to it.

## 14. Re-derivation after merging `origin/main`

`origin/main` advanced from `f605e58` to `f0ecd9b` (pull request #202, "fix/rlo-017-host-independent-candidate-export") while this work order was in progress. That commit was merged into the branch, never rebased onto it, as `cb56673`. Sections 3 to 13 above were measured at `b848b7a`, before the merge. Every figure the merge moved is re-derived here at `cb56673`, against the new base `f0ecd9b`.

The merge produced no conflict. Exactly one path is in both change sets, `docs/notes/developing-se-harness.md`, and Git merged it without a conflict hunk: `origin/main` rewrote the release-sequence section for the 0.7.1 release, and this work order removed the retired-path sentences elsewhere in the file. Both changes are present in the result, the file is 180 lines with CRLF throughout, and it contains no occurrence of the bare retired operator term the portable-surface checker forbids. No other resolution was needed, so no conflict resolution is uncovered code.

`origin/main` also raised the version from `0.7.0` to `0.7.1` in `pyproject.toml` and `se_harness/__init__.py`, added the `release-0-7-1` packet with `RLS-SEH-016`, added `REQ-RLO-017` with `WO-RLO-008` and `VREC-RLO-008`, and changed `repository_tools/predecessor_facts.py` and `repository_tools/release_build.py`. `predecessor_facts.py` is the retained module this work order must not disturb; it is untouched by this branch, and `tests/test_predecessor_bootstrap_retirement.py::test_the_live_predecessor_facts_and_transition_tools_are_untouched` still passes against `origin/main`'s newer version of it.

| Reading | at `f0ecd9b` (new base) | at `cb56673` (candidate) |
| --- | --- | --- |
| Released 0.6.0 `validate`: artifacts / errors / warnings | 983 / 0 / 55 | 989 / 0 / 55 |
| `python scripts/run_tests.py` | 989 tests, OK, skipped=26 | 949 tests, OK, skipped=24 |

The artifact difference is again exactly six, this packet's own additions, with errors and warnings unmoved. The suite difference is again exactly -40 tests and -2 skips, reconciling per module the same way section 9 records: 989 - 48 - 7 + 15 = 949, and the two lost skips are the two Windows-only guards in the deleted `tests/test_predecessor_preparation.py`. Both control runs were taken on this same host in a throwaway detached worktree at `f0ecd9b`, which was removed afterwards.

| Gate at `cb56673` | Result |
| --- | --- |
| `python scripts/validate_engineering_artifacts.py --root .` | PASS, 989 artifacts, 0 errors, 55 warnings |
| `../se-harness-eval/Scripts/python -I -m se_harness doctor .` | 113 checks, 87 PASS, 26 WARN, 0 FAIL, exit code 0 |
| `python scripts/validate_release_distributions.py --root .` | PASS, 4 distribution-bearing records |
| `python scripts/check_portable_release_surface.py --repository .` | PASS |
| `python -m se_harness --help` | exit code 0 |
| `../se-harness-eval/Scripts/python -I -m se_harness preflight . --work-order WO-REB-028 --phase review` | PASS |

The four distribution-bearing records were three before the merge; `RLS-SEH-016` is the fourth and belongs to `origin/main`, not to this work order.

The three retained hash-bound digests were recomputed at `cb56673` and all three still verify, unchanged from section 5. `REL-SEH-011` still declares `from_lock_sha256 = "08441ec0…"` with `from_lock_tool_version = "0.5.0"`. The three hash-bound checks still pass; the declaration now covers 66 tracked paths rather than 62, because `origin/main` added four evidence sidecars of its own. `git diff --name-only origin/main HEAD -- docs/engineering/release-0-6-0/` is empty, so the six closed 0.6.0 artifacts remain byte-identical to the new base, and the same command over the managed hash-locked paths and `se_harness/hash_bound_classes.json` is also empty.

The ephemeral non-promotable candidate wheel of section 6 was rebuilt at `cb56673` by the same recipe, because the merge changed packaged bytes:

```text
se_harness-0.7.1-py3-none-any.whl
sha256 53223241cdb8f984bffa05396173027d6ad5cd575e6ef0ed8ee7720260de9a33
482,740 bytes, 110 members
```

Both surface readings pass against it, `qualify --help` from the installed console script offers the same four operations with zero occurrences of `predecessor-view`, `rehearse-migration` is present, and the member list contains no `predecessor`, `bootstrap` or `repository_tools` member. That wheel and its virtual environment were deleted after the readings, as the 0.7.0 one was. Neither is promotable, and 0.7.1 is already published from a build of record that this host cannot produce.

The formal snapshot moved with the merge, from `77b5543356ee540325a9de44a35e3d4ebd9b35140e32c4ffca120475faaeeb35` at `b848b7a` to `299a568e8f98a62225842a5eff8c1ffcb70f6d4533cd2d541c89e5ee3b3f3d75` at `cb56673`. The binding block at the top of this file declares the second value, which is the one the handoff gate reads. Re-running the handoff check before this section was written returned `QGP-G4I-EVIDENCE: No readable evidence for WO-REB-028, checkpoint handoff, and formal snapshot 299a568e… is available` — the gate passing once does not mean it still passes, and re-binding the evidence is what makes it pass again. Section 13 records the re-derived result.

## 15. Governor upgrade to 0.7.1, and the retraction of VREC-REB-025

`origin/main` advanced again, from `f0ecd9b` to `fda0fa1`, while this work order was being closed. Those nine commits adopt the exact public **0.7.1** evaluator as the standard root (pull request #203, `WO-HUP-007`), so the governing evaluator of this repository is no longer the 0.6.0 one every reading in sections 1 to 14 used. `fda0fa1` was merged into the branch, never rebased onto it, as `f089e83`, with no conflict. `AGENTS.md` and `CLAUDE.md` at the merge are byte-identical to `origin/main`; this branch changes neither.

`.engineering-harness.toml` now pins `tool_version = "0.7.1"` and the lock records the 0.7.1 evaluator payload `995ee973b2959af3bcbf7f7cc4388f079ad033e7c68509e71feb142b0691451f` with a null archive pair. Every reading in this section was taken with the exact public 0.7.1 evaluator installed in `../se-harness-eval-071` outside the checkout and run with `-I`, which reports `se_harness.__version__ == "0.7.1"`. The candidate version in the checkout moved from `0.7.1` to `0.8.0` with the same merge.

### 15.1 Why VREC-REB-025 was retracted rather than rejected or repaired

`VREC-REB-025` was prepared with the then-governing 0.6.0 evaluator, so its evaluator evidence names that evaluator. Under 0.7.1 the record earns:

```text
- [E012] [governance] docs/engineering/released-evaluator-boundary/verification-records/VREC-REB-025.md: evaluator evidence differs from the standard lock
```

This is by design: `_validate_evaluator_evidence_binding` is called with `match_current_lock=artifact.status == "ready"`, so a **ready** record must bind the evaluator identity of the current standard lock, while an already `verified` record keeps the identity it was verified under. That is why the nine earlier `VREC-REB-*` records, which carry the same 0.6.0 evaluator sidecar bytes, stay valid and only this one does not.

Three routes were considered and two are closed:

| Route | Outcome |
| --- | --- |
| Verify it | Not available here. Verification is the accountable decision of `VER-REB-012`'s owners, and the record is invalid under the current governor. |
| Reject it | Mechanically refused. `transition --set VREC-REB-025=rejected` returns `[WEX201] current artifact graph is invalid [E012]: evaluator evidence differs from the standard lock`. The only artifact making the graph invalid is the record being rejected, so the transition can never run. |
| Repair it in place | Refused as a matter of instruction. Editing a prepared record's evaluator binding, candidate commit or artifact snapshot by hand would rewrite record facts. |

The record is therefore **retracted**: `VREC-REB-025.md` and `VREC-REB-025-evaluator.json` are deleted from the tree in the same commit as this section. Nothing is rewritten. The record was never verified, never merged to `main`, and its full text stays in this branch's history at commit `e6231d5`, together with the commit message that prepared it. Its successor, `VREC-REB-026`, is captured with the 0.7.1 evaluator, binds a post-merge candidate commit, and names the same work order, the same contract and the same retained evidence.

Retraction leaves the graph valid and the review checkpoint passing, which the deletion is required for:

```text
Harness preflight: PASS
Phase: review
Work order: WO-REB-028 (implemented)
```

Before the deletion was staged the same command returned `FAIL` with `[A-E012]` on the record. Staging matters: with the files removed from the worktree but the deletion unstaged, preflight instead reports `[I001] hash-bound-class-declared: cannot read ...VREC-REB-025.md`, which is a reading artefact of the index, not a governor finding.

### 15.2 Every figure re-derived under the 0.7.1 governor

The control is a throwaway detached worktree at `origin/main` `fda0fa1`, measured on this same host and removed afterwards.

| Reading | at `fda0fa1` (new base) | at the candidate |
| --- | --- | --- |
| 0.7.1 `validate`: artifacts / errors / warnings | 990 / 0 / 469 | 996 / 0 / 471 |
| `python scripts/run_tests.py` | 993 tests, 1 failure, skipped=26 | 953 tests, 1 failure, skipped=24 |

The artifact difference is again exactly six, this packet's own additions. The suite difference is again exactly -40 tests and -2 skips, and reconciles the same way: 993 - 48 deleted - 7 removed cases + 15 new = 953.

Two things in that table are not this work order's:

- **The two extra warnings** are both new 0.7.1 authoring advisories against `REQ-REB-029`: `[W-AUT-003] statement is 322 characters; the review threshold is 300` and `[W-AUT-004] verification_method is a free-text string; the closed vocabulary is an array of test, analysis, inspection, demonstration`. The requirement was authored and approved under 0.6.0, which has no such check. Clearing them means amending an approved requirement's statement and metadata, which is a separate decision, so they are disclosed and left. The remaining 469 are the base's own advisories, unmoved.
- **The one failure is pre-existing on `main`**: `tests.test_instruction_architecture.OwnerInstructionRegionTests.test_owner_region_stays_within_the_size_bound`, `AssertionError: 6036 not less than 6000 : owner region is 6036 bytes`. The control at `fda0fa1` fails identically, `AGENTS.md` at the candidate is byte-identical to `origin/main`, and the file is not in this work order's execution scope. It is `main`'s to fix, not this branch's, and this branch neither causes nor hides it.

| Gate at the candidate | Result |
| --- | --- |
| `harnessctl validate .` (0.7.1, outside the checkout) | PASS, 996 artifacts, 0 errors, 471 warnings |
| `harnessctl doctor .` | 169 checks, 143 PASS, 26 WARN, 0 FAIL |
| `harnessctl preflight . --work-order WO-REB-028 --phase review` | PASS |
| `python scripts/validate_engineering_artifacts.py --root .` | PASS, 996 / 0 / 471 |
| `python scripts/validate_release_distributions.py --root .` | PASS, 4 distribution-bearing records |
| `python scripts/check_portable_release_surface.py --repository .` | PASS |
| `python -m se_harness --help` | exit code 0 |
| `hash_bound.assess` | 3 PASS: 3 classes cover 69 tracked paths with 9 digest fields out of scope; 2 raw classes effective for 68 |
| `tests/test_predecessor_bootstrap_retirement.py` | 15 tests, OK |

The retirement module passing is what re-verifies the retained history: its `RETAINED_EVIDENCE_BINDINGS` cases recompute `RLS-SEH-012`'s two digests and `REL-SEH-011`'s `from_lock_sha256` from the files themselves, so section 5's three digests still verify under the new base. `git diff --name-only origin/main HEAD -- docs/engineering/release-0-6-0/` is empty, and so is the same command over every managed hash-locked path, now including `docs/engineering/ARTIFACT_AUTHORING.md`, `OPERATING_CARD.md`, `TECHNICAL_COMMUNICATION.md`, `.agents/skills/` and `.claude/skills/`, which the 0.7.1 adoption added to the managed set.

The ephemeral non-promotable candidate wheel was rebuilt once more, because the merge changed packaged bytes again:

```text
se_harness-0.8.0-py3-none-any.whl
sha256 d3e6f3409c0bd1d200db58ea23b3b65563aab6a80c1b2a4465e1b6e3f20f909f
482,742 bytes, 110 members
```

It was built from the merge commit `f089e83` by the same `git archive` and `pip wheel` recipe, installed into a throwaway virtual environment outside the checkout, and both surface readings pass against it: `--wheel` PASS, `--harnessctl` PASS, `qualify --help` offers exactly the four operations with zero occurrences of `predecessor-view`, `rehearse-migration` is present, and no member matches `predecessor`, `bootstrap` or `repository_tools`. The wheel and its environment were deleted after the readings. The candidate commit differs from `f089e83` only under `docs/engineering`, which the wheel does not package. Neither this wheel nor the 0.7.1 and 0.7.0 ones before it is promotable, and 0.7.1 is already published from a build of record this host cannot produce.

The formal snapshot moved again, to `7f36d03248d40fc5a525c77e71f53853256527d1099ac1ae37881cf32a16aa2f`, and the binding block at the top of this file now declares that value. The block always names the current snapshot, because that is what `QGP-G4I-EVIDENCE` matches against; sections 13 and 14 name the snapshot each of their readings was taken at. The changed-path set against `fda0fa1` is 41 paths.

### 15.3 The handoff checkpoint no longer applies

Section 13's reading was the last one taken at the handoff checkpoint, with the then-governing 0.6.0 evaluator, while the work order was still `in_progress`. Re-running it now is refused, correctly:

```text
Blocked by
- WEX210: WEX210: gate QG-G4-CANDIDATE-READY does not apply at checkpoint handoff
```

The governing reading for the current state is the projection of the work order's own scope, which the 0.7.1 evaluator returns as:

```text
Outcome
Completed.

Done
- WO-REB-028 is implemented; no assurance decision was inferred.

Not done
None.

Current lifecycle state
- WO-REB-028 is implemented.

Decision required
engineering-owner must decide whether to prepare one ready verification record with exact approved inputs for WO-REB-028 under DR-VREC-PREPARE; permitted outcomes: prepare, stop.

Next
whether to prepare one ready verification record with exact approved inputs (PROC-WO-PREPARE-VREC/STEP-WO-PREPARE-VREC-DECIDE).

Command or response
Prepare one ready VREC for WO-REB-028 with the exact approved verification contract and retained evidence.
```

That is the act `VREC-REB-026` performs, in the commit after this one. The assurance decision under `VER-REB-012` remains outstanding, and section 12's seven gaps, section 14's merge, and this section's three disclosures - the retraction, the two new authoring advisories, and `main`'s own pre-existing suite failure - are all inputs to it.

## 16. Hosted lanes, and what the one local failure actually is

This section is appended after the commit `VREC-REB-026` binds, `67a52b9`, because hosted readings cannot exist until the commit carrying the record is pushed, and a record cannot bind evidence describing the runs its own push triggers. The append changes no artifact, so it moves neither the formal snapshot nor the record's `artifact_snapshot_sha256`, and the bound evidence path is unchanged. Everything below was read from GitHub Actions at head `c20b673`, the commit that carries `VREC-REB-026`.

### 16.1 The four hosted lanes are green

| Lane, `pull_request` event at `c20b673` | Run | Result |
| --- | --- | --- |
| Engineering Harness (`validate`) | 33106416126 | success |
| Governor Transition Assessment | 33106416125 | success |
| SE Harness Candidate Evidence | 33106416177 | success |
| Publication Rehearsal | 33106417138 | success |

Thirteen required checks pass, including candidate-source evidence, candidate-package evidence, governance migration on Linux and Windows, integration-package verification on Linux and Windows, and both qualification replays of the Publication Rehearsal lane. The pull request reads `MERGEABLE`.

The first push of this branch, at head `e6231d5`, was **red in three of those four lanes**, and every one of the three failed for the same single reason: `[E012]` on the then-present `VREC-REB-025`. The candidate-evidence lane failed check `CC003` with `artifacts=997; errors=1; warnings=471`, the publication rehearsal failed both replays on the same count, and the Engineering Harness lane failed its review preflight with `[A-E012]`. Section 15.1 records why the record was retracted rather than rejected. Nothing else was wrong, and nothing else changed between the two pushes except the retraction and the successor record.

### 16.2 The owner-region failure is a Windows checkout artifact, not a defect

Section 15.2 reports one local suite failure, `test_owner_region_stays_within_the_size_bound`, and states it is pre-existing on `main`. The hosted lanes settle what it is:

```text
Candidate source evidence / Run complete candidate-source regression
Ran 953 tests in 28.219s (115 classes, 4 workers)
OK (skipped=4)
```

The same 953 tests pass on the Linux runner with no failure. The test measures `AGENTS.md` minus its managed block **as checked out**:

| Owner region of `AGENTS.md` | Bytes | Against the 6,000-byte bound |
| --- | --- | --- |
| as checked out on this Windows host, CRLF | 6,036 | fails |
| with LF, which is the tracked blob and the runner's checkout | 5,969 | passes |

So the bound is not exceeded by the tracked content; it is exceeded by the 80 carriage returns a Windows checkout adds, 67 of which fall inside the owner region. `SPEC-IAR-012` rule 12 is satisfied for the repository's own bytes. The correct reading of section 15.2 is therefore narrower than it states: this is a **Windows-only local reading**, it reproduces identically in a control worktree at `origin/main` `fda0fa1`, `AGENTS.md` here is byte-identical to `origin/main`, and there is nothing for this branch or for `main` to fix in the file. It is noted rather than fixed, and it is the only difference between the local Windows suite verdict and the hosted Linux one, along with 20 Windows-only skips: 24 skips locally against 4 on the runner.

### 16.3 The rehearsal gap VER-REB-012 names is still open

The Publication Rehearsal lane that passed above is `.github/workflows/release-qualification.yml` on the `pull_request` event. It is **not** the evidence `VER-REB-012` asks for. That contract requires a `workflow_dispatch` rehearsal of the two workflows this work order edits, `.github/workflows/publish-pypi.yml` and `.github/workflows/pages-publication.yml`, and says in terms that static review of those two files is not sufficient evidence on its own. No dispatch run of either exists. Both files are exercised only by the static review of section 7 and by the ordinary lanes above, which never invoke them. This remains the largest single gap in front of the assurance decision, and only an owner with dispatch rights can close it.

### 16.4 The formal snapshot sequence, and one correction to section 15

Preparing `VREC-REB-026` added an artifact, so it moved the formal snapshot once more. The complete sequence is:

| Formal snapshot | Commit | State |
| --- | --- | --- |
| `77b5543356ee540325a9de44a35e3d4ebd9b35140e32c4ffca120475faaeeb35` | `b848b7a` | first measurement, 0.6.0 governor, sections 3 to 13 |
| `299a568e8f98a62225842a5eff8c1ffcb70f6d4533cd2d541c89e5ee3b3f3d75` | `cb56673` | after merging `f0ecd9b`, section 14 |
| `7f36d03248d40fc5a525c77e71f53853256527d1099ac1ae37881cf32a16aa2f` | `67a52b9` | after merging `fda0fa1` and retracting `VREC-REB-025`, section 15 |
| `5ab8585bae55cf112ef8eb91026987b7e7951dec1ee6614e372a4c03e50368b2` | `c20b673` | after preparing `VREC-REB-026`, which is itself an artifact |

Section 15.2 says the binding block at the top of this file "always names the current snapshot". That is one commit too loose, and the accurate statement is this: the block names `7f36d032`, the snapshot at `67a52b9`, which is exactly the candidate commit `VREC-REB-026` binds. A verification record's own preparation necessarily moves the snapshot after the commit it binds, so a bound reading can never name the snapshot of the commit that carries the record. No gate reads the block in the current state in any case, because the handoff checkpoint no longer applies, as section 15.3 records; the review preflight the hosted lane runs passes at every commit since the retraction.

## 17. The owner review of 2026-08-27 on pull request #206

The repository owner reviewed this change at `2026-08-27T19:04:30Z` against issue #208, which is P0-2 of the 2026-08 complexity audit and the finding this work order answers. The review states its readings were reproduced independently rather than taken from the pull-request body, approves the content, and raises four gaps. This section is appended for the same reason section 16 was: the review does not exist until the branch is pushed, and a verification record cannot bind evidence describing events its own push causes. The append changes no artifact, so the formal snapshot and `VREC-REB-026`'s `artifact_snapshot_sha256` do not move.

One reading in the review cross-checks this document arithmetically. The review reports the pinned 0.6.0 validator at `e6231d5` as 990 artifacts, 0 errors, 55 warnings. Section 14 reports 989 / 0 / 55 at `01084d8` with the same validator, and `e6231d5` is exactly the commit that added `VREC-REB-025`, one artifact. The two independent readings agree.

### 17.1 The four gaps, measured again here

Each gap was re-measured at `03e4f0d` rather than accepted from the review text.

| # | The review's gap | Measured here | True? |
| --- | --- | --- | --- |
| 1 | The consumer-installed validator still ships the predecessor rules | `_validate_predecessor_view_evidence` at lines 1135 to 1457, 323 lines; `_bootstrap_for_release_record` at 854 to 921, 68 lines; `_validated_release_bootstrap` at 791 to 844, 54 lines; the three retired schema constants at 58 to 60; call sites at 1940 to 1954, 1991 to 1992 and 2115 to 2126 | yes |
| 2 | `repository_tools/interpreter_safety.py` is dead code | the only importer left in the repository is `tests/test_interpreter_safety.py`, which pins it byte-equal to `se_harness/interpreter_safety.py`; no product module, script or workflow imports it | yes |
| 3 | `ADR-REB-009` still decides five operations | line 69 names `predecessor-view` among "exactly five typed subcommands"; `ADR-REB-012` does not mention `ADR-REB-009` at any point, and `ADR-REB-009` carries no amendment | yes |
| 4 | The `$RUNNER_TEMP/predecessor-view` directory name is kept | six lines in `.github/workflows/pages-publication.yml`, 174 to 187 | yes |

Issue #208's four acceptance criteria read as follows at `03e4f0d`, using the issue's own commands:

| Criterion | Reading |
| --- | --- |
| No `predecessor_view` or `predecessor-view` outside `docs/engineering/` | not met: nine occurrences remain, six of them the temp-directory name of gap 4, two the validator constants of gap 1 in each of the two copies, and one the `FORBIDDEN_ACTIVE_CONTENT` entry in `check_portable_release_surface.py` that exists in order to forbid the string |
| `se_harness/` contains no import of `repository_tools` | met; the two textual matches in `se_harness/interpreter_safety.py` are a docstring and the `RUNTIMES` name tuple, not imports |
| `validate_engineering_artifacts.py --root .` reports 0 errors | met, and it is the same figure from both the in-tree copy of the released validator and the evaluator installed outside the checkout: 997 artifacts, 0 errors, 471 warnings. Section 15.2 reads 996 at `67a52b9`; the extra artifact is `VREC-REB-026` itself |
| No bootstrap-tuple branch in the release-qualification and publish-pypi workflows | met: zero occurrences of `bootstrap` in `publish-pypi.yml`, `release-qualification.yml` and `pages-publication.yml` |

### 17.2 Gap 1 is forbidden by this work order's own approval, and is a release-time change

Two facts decide it. First, the approval that authorized this work says, verbatim, "No byte of scripts/validate_engineering_artifacts.py, its templates copy, or se_harness/hash_bound_classes.json", and `templates/` is absent from `[execution_scope] paths`, so `QGP-G4I-PATHS` would refuse the changed path with `WEX201`.

Second, the change would not alter how this repository is judged. The two copies are byte-identical:

| Copy | Bytes | Lines | sha256 |
| --- | --- | --- | --- |
| `scripts/validate_engineering_artifacts.py` | 159,767 | 3,679 | `312375bc455cfbf716300e235c976c8bfe9ac90bb5d74748bef31836a944d724` |
| `templates/repository/standard/scripts/validate_engineering_artifacts.py` | 159,767 | 3,679 | `312375bc455cfbf716300e235c976c8bfe9ac90bb5d74748bef31836a944d724` |

The template copy is therefore not lagging candidate source here; it is the exact released 0.7.1 file. The governing evaluator that validates this repository is installed outside the checkout and would keep enforcing those rules whatever the template says, so deleting them changes only what a future release ships to consumers, and it takes effect at that release. Several tests also pin the template byte-equal to the root copy, so the edit needs a declared candidate exception in each of them. That is a self-contained piece of work with its own release consequence and its own verification, not a late addition to this one.

### 17.3 No further work can be done under WO-REB-028

`docs/engineering/WORKFLOW.json` gives the work-order lifecycle as `implemented -> ["verified", "released"]`. There is no edge back to `in_progress`, and none from `implemented` to itself. `WO-REB-028` is `implemented`, so it can take no further implementation work, and widening its execution scope would not change that. The completion decision already recorded on it enumerates exactly what was done and cannot be corrected.

`VREC-REB-026` compounds it: the record is `ready` and binds candidate `67a52b9` with `artifact_snapshot_sha256 = f1bdbf96...`. Any artifact change now moves the formal snapshot and the artifact snapshot, which would force the record to be retracted and prepared a third time, as section 15.1 describes for the first one.

So gaps 1, 3 and 4 are all deferred, not by preference but because the only route to them is a new work order:

| Gap | Where it goes |
| --- | --- |
| 1, the consumer-installed validator | step 4 of issue #208, in a new work order; #208 stays open for it |
| 2, `repository_tools/interpreter_safety.py` | issue #220, P1-8, which is open and proposes deleting the copy. Disclosure 3 of the completion decision argues the opposite case, that the copy earns its place as the second independent loader the cross-runtime conformance test holds in agreement with the packaged one. #220 is where that is settled; this work order reports only the measured fact that the module has no production caller left |
| 3, `ADR-REB-009` | step 6 of issue #208, in the same new work order; the route is a dated amendment on `ADR-REB-009`, because the definition lifecycle admits no `superseded` transition, which is the same finding as the first disclosure of the completion decision |
| 4, the temp-directory name | the same new work order, or left; it is a directory name inside one job, it is deliberate, and the comment at lines 166 to 168 of `pages-publication.yml` records that the path is retained so the generator invocation below it is unchanged |

Gap 3 is a real inconsistency and is stated as one: after this change `harnessctl qualify` offers four operations while an approved architecture decision says five. Nothing mechanical detects it, `validate` reports 0 errors, and no gate refuses it. It is a governance defect of record until the amendment lands.

### 17.4 One step of the route the review proposes is closed

The review's remedy for the red lanes is: merge `origin/main` in, never rebase, keep `bc872f4` reachable, reject `VREC-REB-025`, capture a fresh record under the 0.7.1 evaluator, re-derive the readings and expect the W-AUT advisories. Every step of that was followed except one, and the exception is mechanical:

```text
$ harnessctl transition . --set VREC-REB-025=rejected --apply
[WEX201] current artifact graph is invalid [E012]: evaluator evidence differs from the standard lock
```

`transition` refuses to run while the artifact graph is invalid, and the only artifact making the graph invalid is the record being rejected. Rejection is unreachable for a `ready` record that a governor upgrade has invalidated. Section 15.1 records the retraction taken instead, which deletes the record and its sidecar in an append-only commit and leaves the full text at `e6231d5`.

The rest of the route holds as stated: `fda0fa1` was merged, never rebased, `bc872f4` is reachable from `HEAD`, `VREC-REB-026` was captured with the exact public 0.7.1 evaluator outside the checkout, every figure was re-derived in section 15.2, and the W-AUT advisories appeared exactly as predicted, two of them, both on `REQ-REB-029`, and both warnings rather than errors. The four lanes are green at `c20b673` in section 16.1 and at `03e4f0d`.
