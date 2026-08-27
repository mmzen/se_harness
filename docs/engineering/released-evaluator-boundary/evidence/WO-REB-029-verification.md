# WO-REB-029 Consumer-Installed Validator Retirement Evidence

Date: 2026-08-27

Authority: non-authoritative retained implementation evidence. This file does not approve, verify, release, publish, tag, or deploy anything. It records what was measured on one platform at one commit. `WO-REB-029` carries `commit_bound_verification = "required"`, so commit-bound assurance is a separate `VREC` decision by an accountable verifier and this file is not that decision. The work order was `in_progress` throughout every measurement below. Section 17 lists every disclosure and gap in one numbered set, including the several the work order's own text does not anticipate.

artifact: WO-REB-029
checkpoint: handoff
formal_snapshot_sha256: 8c1e2d2a26b5a565bd4ff8e019e90c7b7eab7d0bad62c2519716729ee9bd2b16

## 1. Governing packet and preflight

`WO-REB-029` implements `REQ-REB-029` under `SPEC-REB-013` and `SPEC-REB-014`, with `ARCH-REB-012`, `ADR-REB-012` and `VER-REB-013`. Both specifications are selected because both specify `REQ-REB-029`: `SPEC-REB-013` keeps its force and is not amended, reopened or re-scoped, and `SPEC-REB-014` authorizes the managed-validator edit that `SPEC-REB-013` excludes in terms.

`SPEC-REB-014`, `VER-REB-013` and `WO-REB-029` were transitioned `draft` to `approved` at `2026-08-27T20:11:19Z` on the accountable owner's single act, "i approve the 3 draft artifacts", taken on the owner review of pull request #206. The work order moved `approved` to `in_progress` at `2026-08-27T20:16:24Z` on the owner's later decision, "after approval is made, you can start the work". The owner holds the requirements-steward, technical-owner, quality-owner, security-owner, release-owner, repository-owner and engineering-owner roles in this repository, so neither act is implied by the other.

Every lifecycle act and every authoritative reading below used the exact public 0.7.1 evaluator installed in a virtual environment outside this checkout and run with `-I`:

```text
C:\Users\mathi\se-harness-eval-071\Scripts\python -I -m se_harness --version
0.7.1

C:\Users\mathi\se-harness-eval-071\Scripts\python -I -m se_harness preflight . --work-order WO-REB-029 --phase review
Harness preflight: PASS
Phase: review
Work order: WO-REB-029 (in_progress)
Assurance classification: commit-bound verification required, decided by repository-owner
exit code 0
```

`preflight` accepts `--phase start` and `--phase review` only; there is no implementation phase, so the review phase is the reading taken during implementation.

## 2. Base commit and commits under this work order

Chain base: `fda0fa1`, `main` at the 0.7.1 release state that governs this checkout.

Branch base: `29a05c3`, the tip of `governance/reb-028-retire-predecessor-bootstrap`, `2026-08-27T21:26:06+02:00`, "docs(reb): dispose of the owner review of pull request #206". That branch is pull request #206, which is not merged; this work order's branch is stacked on it as pull request #230.

Branch: `governance/reb-029-retire-managed-validator-bootstrap-rules`.

| Commit | Time | Subject |
| --- | --- | --- |
| `200f270` | `2026-08-27T21:39:49+02:00` | `governance(reb): draft WO-REB-029 to retire the managed validator's bootstrap rules` |
| `70c3e16` | `2026-08-27T21:51:15+02:00` | `governance(reb): co-select SPEC-REB-013 so WO-REB-029 passes review preflight` |
| `b5f0542` | `2026-08-27T22:11:53+02:00` | `governance(reb): approve WO-REB-029, SPEC-REB-014 and VER-REB-013` |

The implementation commit carries every change measured in this document, including this document. It cannot record its own hash, so it is named here rather than listed above. Section 16 records the handoff checkpoint result read from the working tree that commit captures.

## 3. The measured deletion

One file changed: `templates/repository/standard/scripts/validate_engineering_artifacts.py`, the copy of the managed validator that consumer repositories install.

| Reading | Before | After |
| --- | --- | --- |
| Lines | 3679 | 3094 |
| Bytes, CRLF worktree | 159767 | 132053 |
| sha256, CRLF worktree | `312375bc455cfbf716300e235c976c8bfe9ac90bb5d74748bef31836a944d724` | `f3e29ea609fd0142cbb62130706b95cc0fc49a997fa7413e8d061248fd8f4676` |

585 lines were deleted. Nothing was added and nothing was rewritten, which section 11 states as an executable declaration rather than as a claim.

The ten deleted blocks, by first line in the root copy, span in lines, and first line of the block:

| Root line | Lines | First line |
| --- | --- | --- |
| 58 | 15 | `RELEASE_BOOTSTRAP_SCHEMA = "se-harness-release-bootstrap-v1"` |
| 791 | 133 | `def _validated_release_bootstrap(` |
| 932 | 1 | `    bootstrap_contract: dict[str, Any] | None = None,` |
| 1062 | 39 | `    if bootstrap_contract is not None:` |
| 1133 | 325 | `def _validate_predecessor_view_evidence(` |
| 1940 | 18 | `    approved_bootstrap_contracts = [` |
| 1990 | 3 | `            _validated_release_bootstrap(artifact, errors, report_root)` |
| 2115 | 23 | `            bootstrap_contract = _bootstrap_for_release_record(` |
| 2180 | 27 | `            if artifact.status == "ready" and bootstrap_contract is not None:` |
| 2237 | 1 | `                bootstrap_contract=bootstrap_contract,` |

The sixteen deleted names, counted in each copy. Each is named individually, as `VER-REB-013` case 1 requires: one regular expression over the file would also pass while a renamed survivor stayed behind. Presence in the root copy is asserted as well, so a name that was never there cannot make the absence case pass for nothing.

| Name | Root copy | Candidate copy |
| --- | --- | --- |
| `RELEASE_BOOTSTRAP_SCHEMA` | 2 | 0 |
| `PREDECESSOR_PREPARATION_SCHEMA` | 4 | 0 |
| `PREDECESSOR_VIEW_EVIDENCE_SCHEMA` | 2 | 0 |
| `PREDECESSOR_VIEW_EVIDENCE_MAX_BYTES` | 2 | 0 |
| `RELEASE_BOOTSTRAP_KEYS` | 2 | 0 |
| `_validated_release_bootstrap` | 3 | 0 |
| `_bootstrap_for_release_record` | 2 | 0 |
| `_validate_predecessor_view_evidence` | 2 | 0 |
| `_canonical_utf8_text_lf` | 3 | 0 |
| `bootstrap_contract` | 24 | 0 |
| `approved_bootstrap_contracts` | 3 | 0 |
| `rejected_predecessor_history` | 2 | 0 |
| `preparation_schema` | 8 | 0 |
| `preparation_view_evidence` | 6 | 0 |
| `se-harness-release-bootstrap-v1` | 1 | 0 |
| `se-harness-predecessor-bootstrap-v1` | 1 | 0 |

`REQ-REB-029`'s measure, "zero code paths that read a contract `[bootstrap]` tuple or construct a predecessor view", now reads zero for this copy. The root copy is out of scope and is unchanged; section 14 measures that.

## 4. Case 2: zero errors under the candidate validator

The full artifact graph, read by the edited file. This is a candidate reading, labelled as such, and it is not the governing verdict.

```text
python templates/repository/standard/scripts/validate_engineering_artifacts.py --root .
Engineering artifact validation: PASS
Artifacts: 1000 | Errors: 0 | Warnings: 471
Planes: structure E0/W0 | governance E0/W0 | policy E0/W0 | maintenance E0/W471
exit code 0
```

## 5. Case 3: zero errors under the evaluator outside the checkout, against a control

```text
C:\Users\mathi\se-harness-eval-071\Scripts\python -I -m se_harness validate .
Engineering artifact validation: PASS
Artifacts: 1000 | Errors: 0 | Warnings: 471
Planes: structure E0/W0 | governance E0/W0 | policy E0/W0 | maintenance E0/W471
exit code 0

C:\Users\mathi\se-harness-eval-071\Scripts\python -I -m se_harness doctor .
143 PASS | 26 WARN | 0 FAIL
exit code 0
```

The 471 warnings are all in the maintenance plane and all authoring advisories: `W-AUT-001`, `W-AUT-002`, `W-AUT-003`, `W-AUT-004`, `W013`, `W014`, `W015`, `W024`. None is an error and none is new.

`VER-REB-013`'s security check requires the before and after readings to be compared artifact for artifact, not by total, because a deletion that removed checks could hide a newly accepted artifact behind an unchanged count. Three readings were taken and their diagnostic sets compared element by element as sorted `(code, path, message)` triples:

| Reading | Artifacts | Errors | Warnings | sha256 of the sorted diagnostic triples |
| --- | --- | --- | --- | --- |
| Candidate copy, this tree | 1000 | 0 | 471 | `369c1cc41a8615a143a8651403d4e3077541ca9add3b5cbac7f4efc42bb56450` |
| Root copy, this tree | 1000 | 0 | 471 | `369c1cc41a8615a143a8651403d4e3077541ca9add3b5cbac7f4efc42bb56450` |
| Root copy, control worktree at `b5f0542` | 1000 | 0 | 471 | `369c1cc41a8615a143a8651403d4e3077541ca9add3b5cbac7f4efc42bb56450` |

The three sets are identical: same paths, same codes, same messages, in the same number. The control worktree is a separate checkout of `b5f0542`, the branch state before the deletion, so the middle and last rows are the before reading and the first row is the after reading. No artifact changed verdict, no diagnostic disappeared, and no artifact became acceptable. The plane counts and the whole error taxonomy are identical between the two validator copies.

## 6. Acceptance scenarios: a consumer-shaped repository with no bootstrap marker

`VER-REB-013`'s acceptance scenarios also require a repository that carries no retained `[bootstrap]` table to validate clean and unchanged. This repository is not that case, so a throwaway consumer repository was created outside the checkout with the 0.7.1 evaluator, and both validator copies were run against it.

```text
C:\Users\mathi\se-harness-eval-071\Scripts\python -I -m se_harness init C:\Users\mathi\reb029-consumer --project-name reb029-consumer
summary: 61 files, 0 unchanged
installed se-harness 0.7.1 in C:\Users\mathi\reb029-consumer
```

The tree contains no `[bootstrap]` table and no `preparation_schema` marker, counted at zero across every Markdown file. Both copies read it identically:

| Tree state | Root copy | Candidate copy |
| --- | --- | --- |
| Bare install, 0 artifacts | PASS, 0 errors, 0 warnings | PASS, 0 errors, 0 warnings |
| One scaffolded domain and two drafts, 2 artifacts | FAIL, 1 error, `E006` on `REQ-SMP-001` | FAIL, 1 error, `E006` on `REQ-SMP-001` |

The standard output of the two runs is byte-identical in both states, including the failing case, so the deletion neither narrows nor widens what a consumer repository is told. The throwaway tree was deleted after the reading.

The installed 0.7.1 validator is byte-identical to this repository's root copy once line endings are canonicalized: LF-normalized sha256 `cf9bf4827f2b07827b056181b3235b9e4a2dce161959849a5970412323777a2a` for both. The root copy in this worktree is therefore the released 0.7.1 file, CRLF as `core.autocrlf` wrote it, which is what makes the root reading in section 5 the released behaviour.

## 7. Case 4: the six closed artifacts are inert data

| Artifact | Path | Blob at `HEAD` | Retained marker |
| --- | --- | --- | --- |
| `REL-SEH-008` | `docs/engineering/release-0-6-0/release/REL-SEH-008.md` | `d14090b88ff6d1c032333d7a2454ca9a571854e5` | `[bootstrap]` |
| `REL-SEH-009` | `docs/engineering/release-0-6-0/release/REL-SEH-009.md` | `9dda66cc2ac1020863f3a1d6199b55bbe72f9f95` | `[bootstrap]` |
| `REL-SEH-010` | `docs/engineering/release-0-6-0/release/REL-SEH-010.md` | `61d3f8b0eca7c7a145805a359a08dc9e0e542f3c` | `[bootstrap]` |
| `REL-SEH-011` | `docs/engineering/release-0-6-0/release/REL-SEH-011.md` | `849ca9f7e337591db3ae95ddaf0fae2f3f692e53` | `[bootstrap]` |
| `RLS-SEH-009` | `docs/engineering/release-0-6-0/releases/RLS-SEH-009.md` | `0b9661f570e8a85afa4acb4dd995eda57bfc7f67` | `preparation_schema = "se-harness-predecessor-bootstrap-v1"` |
| `RLS-SEH-012` | `docs/engineering/release-0-6-0/releases/RLS-SEH-012.md` | `090ad5f5b7779748b7a866df913d72aaf9f1372b` | `preparation_schema = "se-harness-predecessor-bootstrap-v1"` |

Each blob is the same object at `fda0fa1`, at `b5f0542` and in the working tree: byte-identical to its state before the change, and unchanged by `WO-REB-028` as well. `git diff` reports no change anywhere under `docs/engineering/release-0-6-0/`.

The marker counts under that domain are pinned, not merely observed: `[bootstrap]` occurs 4 times and `preparation_schema` occurs 2 times, and `tests/test_predecessor_bootstrap_retirement.py` fails if either number moves. The same test asserts that neither marker appears in the candidate validator, which is what makes the data inert: the bytes stay and every reader of them is gone. All six artifacts are inside the 1000 that validate with zero errors in sections 4 and 5.

## 8. Case 5: the three retained digests still verify

Recomputed from the files they bind, under the unit suite, not under a validator rule. The rule that re-derived one of them is what this work order deleted, so the suite is now the only mechanical check that they hold.

| Record | Field | Digest | Bound file |
| --- | --- | --- | --- |
| `RLS-SEH-012` | `preparation_view_evidence_sha256` | `77474d1e22422371d48f3d1a281810a6c7f9bf55982a17e565f602978bbab4d7` | `docs/engineering/release-0-6-0/evidence/RLS-SEH-012-preparation-view.json` |
| `RLS-SEH-012` | `evaluator_evidence_sha256` | `11a4aec338f1da102a112faca6589d18541e115e139e695e8d66e4d509125404` | `docs/engineering/release-0-6-0/evidence/RLS-SEH-012-evaluator.json` |
| `RLS-SEH-009` | `evaluator_evidence_sha256` | `11a4aec338f1da102a112faca6589d18541e115e139e695e8d66e4d509125404` | `docs/engineering/release-0-6-0/evidence/RLS-SEH-009-evaluator.json` |

All three recompute to the digest the record states. The two `evaluator_evidence_sha256` values are equal because the evaluator evidence is identical across those records, which is a property of the retained history and not of this change. `se_harness/hash_bound_classes.json` still declares `evaluator_evidence_sha256`, `preparation_view_evidence_sha256` and `from_lock_sha256`, and is not edited: retiring a producer must not retire a binding, or an unclaimed digest field would stop being checked at all.

## 9. Case 6: `REQ-REB-011` is preserved

`REQ-REB-011` is not retired and not narrowed. What the deletion removed is the condition that narrowed one of its checks to records marked `se-harness-predecessor-bootstrap-v1`. `VER-REB-013` therefore requires a negative case showing the general rule still holds, and `test_a_rejected_record_still_cannot_claim_a_version_against_a_successor` is that case. It is functional, not textual: it loads the edited file by path, builds synthetic release records, and calls `validate_revision_consistency`.

| Reading | Result |
| --- | --- |
| `rejected` reserves a version | False |
| `ready` reserves a version | True |
| `released` reserves a version | True |
| A rejected record and a ready successor on one version | no collision |
| A rejected record and a released successor on one version | no collision |
| A rejected record carrying `preparation_schema = "se-harness-predecessor-bootstrap-v1"` and a released successor | no collision, and no diagnostic mentioning bootstrap or predecessor |
| A ready and a released record on one version | 2 collisions, both naming `RLS-TST-103, RLS-TST-104` |

The rule now stands on the lifecycle matrix alone, which is stronger than the condition it replaces: a rejected record is inert whether or not it carries the retired marker, and two records that do reserve the version still collide. The removal narrowed nothing beyond the named rules.

## 10. Case 7: the packaged copy

The template was read as it ships, not as candidate source. The checkout was copied outside itself, an ephemeral wheel was built from the copy, and the wheel was installed with `--no-deps --no-index` into a temporary virtual environment outside the checkout.

| Reading | Value |
| --- | --- |
| Wheel | `se_harness-0.8.0-py3-none-any.whl` |
| Wheel bytes | 478672 |
| Wheel sha256 | `5a12377fb6f4d0dd0735076ad4ba0ec7e479136f55eef588410df10df7f1e348` |
| Packaged validator bytes | 132053 |
| Packaged validator sha256 | `f3e29ea609fd0142cbb62130706b95cc0fc49a997fa7413e8d061248fd8f4676` |
| Deleted names present in the packaged copy | 0 of 16 |

The packaged file is byte-identical to the candidate copy in section 3, so what a consumer installs is what was edited. The wheel is explicitly non-promotable: it was never bound to any release record, never published, never tagged, and it, its build tree and both virtual environments were deleted after the reading. `AGENTS.md` permits exactly this, "an approved candidate-evidence work order may build explicitly non-promotable ephemeral wheels outside the checkout for package acceptance", and `WO-REB-029` is not a release work order. The `0.8.0` version string comes from `pyproject.toml` and does not indicate a release.

## 11. Case 8: the divergence is declared

Before this change, no test pinned the two managed validator copies byte-equal, so case 8 had no existing test to amend. The declaration was written instead, as `test_the_candidate_copy_differs_from_the_root_copy_only_by_the_declared_deletions`. It runs `difflib.SequenceMatcher` over the two files line by line and asserts:

- every non-equal opcode is a `delete`, so nothing is inserted and nothing is replaced;
- there are exactly ten of them;
- each starts at the declared root line, spans the declared number of lines, and contains the declared first line;
- the ten spans sum to 585, which equals the measured difference in line count.

The ten declared blocks are the table in section 3, held as `CANDIDATE_VALIDATOR_DELETIONS` in `tests/test_predecessor_bootstrap_retirement.py`. A future edit to either copy that is not in that table fails the test with the offending root line named. No test is disabled, skipped or redirected away from the comparison; one existing test was widened, which section 17 discloses.

## 12. The four amendments

Each is an in-place dated section appended to the artifact, in the exact form `WO-REB-028` used for `REQ-REB-012`, `REQ-REB-015`, `SPEC-REB-003`, `SPEC-REB-005` and `SPEC-REB-007`. No lifecycle event is added, edited or removed, and no prose below the amendment is rewritten.

`REQ-REB-008`, `## Retirement amendment of 2026-08-27`:

> Retired on 2026-08-27 by `REQ-REB-029` under `WO-REB-029`, on the repository owner's direction, which decided this requirement is superseded. The contract-bound bootstrap release record is withdrawn. No release contract carries bootstrap authority, no release record resolves one, and the consumer-installed validator no longer reads a `[bootstrap]` tuple, resolves a bootstrap contract for a release record, or enforces at most one approved bootstrap contract in a repository.

Its second paragraph records that the declared `superseded` status is not applied, because `docs/engineering/WORKFLOW.json` admits no `approved` to `superseded` transition for a definition and `WFL-005` requires the artifact's own `draft` to `approved` event to stay append-only. Setting the status would either contradict that event, measured as `E014` on 2026-08-27, or delete it.

`REQ-REB-010`, `## Retirement amendment of 2026-08-27`:

> Retired on 2026-08-27 by `REQ-REB-029` under `WO-REB-029`, on the repository owner's direction, which decided this requirement is superseded. The rejected predecessor-bootstrap tuple is no longer validated. [...] What this requirement protected against is unaffected: no rejected contract can grant bootstrap authority, because no contract grants bootstrap authority at all, and nothing can reuse a tuple that no rule reads.

Its second paragraph is the one section 9 measures:

> `REQ-REB-011` is not retired and is not narrowed. Its rule stands in full: a rejected record remains valid but inert and does not claim a version against a second ready or released successor. Only the condition that narrowed one of its checks to records marked `se-harness-predecessor-bootstrap-v1` is removed, because that schema name no longer has a reader, and `VER-REB-013` requires a negative case proving the general rule still holds.

`ARCH-REB-009`, `## Amendment of 2026-08-27`:

> Amended on 2026-08-27 under `WO-REB-029`, on the repository owner's direction. The `harnessctl qualify` namespace has four typed operations, not five: `released-root`, `complete-candidate`, `candidate-package` and `public-install`. `WO-REB-028` withdrew `predecessor-view` together with the predecessor-compatible view it qualified, and `ADR-REB-009` carries the same amendment.

It also records the three parts of the architecture that lose their subject and are retained unchanged: the `Predecessor-view coordinator` component and its handler, the shared predecessor-view service in the dependency diagram and in `Dependency direction`, and the conformance check that enumerated options `for all five subcommands`, which reads four. `PV001` and `PV002` stay reserved by `SPEC-REB-013`.

`ADR-REB-009`, `## Amendment of 2026-08-27`:

> Amended on 2026-08-27 under `WO-REB-029`, on the repository owner's direction. The namespace this ADR created now has four typed subcommands: `released-root`, `complete-candidate`, `candidate-package` and `public-install`. [...] The decision recorded below is not rewritten and neither is the title. A decision record states what was decided on 2026-08-24 and why, including the options that were rejected; editing it would replace the record with its own consequence.

## 13. The Pages lane and the tests that pin it

`.github/workflows/pages-publication.yml`: the temporary directory `$RUNNER_TEMP/predecessor-view` is now `$RUNNER_TEMP/generation-snapshot`, at all six occurrences in lines 174 to 187. The comment at 166 to 168 kept a sentence that existed only to explain why the retired path was kept, "The path is retained so the generator invocation below is unchanged"; it now reads "Nothing is omitted from it for any release record, and the path is named for what it holds." The lane's behaviour is unchanged: it materializes the complete governance snapshot unconditionally for every release record, which is `SPEC-REB-013` rule 5.

The retired name occurs zero times in the workflow, zero times in `tests/test_dashboard_publication.py`, and zero times in `tests/test_release_orchestration.py` except where a lane's own retired job name is asserted absent.

| Module | Change |
| --- | --- |
| `tests/test_dashboard_publication.py` | the generator-invocation assertion and its negative pair follow the rename, and a new `assertNotIn("predecessor-view", self.workflow)` closes the whole lane against the name |
| `tests/test_release_orchestration.py` | both `mkdir` assertions and the generator-invocation assertion follow the rename, and `"predecessor-view"` joins the tuple of strings the lane must not contain |
| `tests/test_predecessor_bootstrap_retirement.py` | extended from 315 to 533 lines: the five cases of `ConsumerValidatorRetirementTests`, the loader for the candidate copy, the sixteen deleted names, the ten declared blocks, and the pinned marker counts |

`tests/test_predecessor_bootstrap_retirement.py` was extended rather than replaced by a new module, as the work order requires. It runs 20 tests, all passing.

## 14. Property, invariant, static and security readings

| Check | Reading |
| --- | --- |
| `[bootstrap]` occurrences under `docs/engineering/release-0-6-0/` | 4, unchanged, pinned by the suite |
| `preparation_schema` occurrences under the same domain | 2, unchanged, pinned by the suite |
| New error code in the taxonomy | none; the taxonomy is identical between the two validator copies |
| `PV001` and `PV002` | reserved as `RETIRED_CHECK_CODES` in `se_harness/release_qualification.py:55`, pinned by `tests/test_predecessor_bootstrap_retirement.py:255`, and emitted by no check: zero occurrences in either validator copy |
| `scripts/validate_engineering_artifacts.py`, the root copy | byte-identical to its state before the change; the same blob `a978702e09f38d544f6777d624b7c10150959145` at `fda0fa1`, at `b5f0542` and in the working tree |
| `se_harness/hash_bound_classes.json` | unchanged |
| The four amendments | present and dated 2026-08-27; section 17 discloses the one frontmatter field two of them move |
| The Pages lane | no occurrence of the retired name |
| Hash-bound digests changed | none |
| Credentials, network writes, root changes of this repository | none |

The security reading of the deletion is in section 5: removing checks cannot be shown safe by an unchanged total, so the diagnostic sets were compared element by element and are identical. Nothing previously rejected became accepted.

## 15. The unit suite against a control at the same base

Both runs used the in-tree interpreter on Windows with `python scripts/run_tests.py`, 8 workers. The control is a separate worktree at `b5f0542`, the branch state before the change.

| Tree | Tests | Classes | Failures | Skipped | Time |
| --- | --- | --- | --- | --- | --- |
| This working tree | 958 | 116 | 1 | 24 | 82.321s |
| Control at `b5f0542` | 953 | 115 | 1 | 24 | 97.210s |

The five extra tests and the extra class are `ConsumerValidatorRetirementTests`. The one failure is the same in both trees:

```text
FAIL: test_instruction_architecture.OwnerInstructionRegionTests.test_owner_region_stays_within_the_size_bound
AssertionError: 6036 not less than 6000 : owner region is 6036 bytes
```

It is a pre-existing Windows measurement, not a regression: the owner region carries 67 newlines, so it is 5969 bytes with LF and 6036 bytes with CRLF, and the assertion reads the worktree bytes. The hosted Linux lane reads 5969 and passes. The control at the same base fails identically, which is what makes this a baseline red rather than an effect of this work order. The 24 skips are the Windows-only platform guards.

## 16. The handoff checkpoint result

Read from the working tree the implementation commit captures, with every changed path declared and completeness asserted, using the evaluator outside the checkout. Thirteen changed paths were declared, one per flag, and this document is one of them.

```text
C:\Users\mathi\se-harness-eval-071\Scripts\python -I -m se_harness check . --artifact WO-REB-029 --checkpoint handoff \
  --changed-path '.github/workflows/pages-publication.yml' \
  --changed-path 'docs/engineering/released-evaluator-boundary/README.md' \
  --changed-path 'docs/engineering/released-evaluator-boundary/architecture/ARCH-REB-009.md' \
  --changed-path 'docs/engineering/released-evaluator-boundary/architecture/adr/ADR-REB-009.md' \
  --changed-path 'docs/engineering/released-evaluator-boundary/requirements/REQ-REB-008.md' \
  --changed-path 'docs/engineering/released-evaluator-boundary/requirements/REQ-REB-010.md' \
  --changed-path 'docs/engineering/released-evaluator-boundary/work-orders/WO-REB-029.md' \
  --changed-path 'docs/engineering/released-evaluator-boundary/evidence/WO-REB-029-verification.md' \
  --changed-path 'docs/notes/developing-se-harness.md' \
  --changed-path 'templates/repository/standard/scripts/validate_engineering_artifacts.py' \
  --changed-path 'tests/test_dashboard_publication.py' \
  --changed-path 'tests/test_predecessor_bootstrap_retirement.py' \
  --changed-path 'tests/test_release_orchestration.py' \
  --changes-complete

Outcome
Completed.

Done
- Evaluated handoff compliance for WO-REB-029.

Not done
None.

Current lifecycle state
- WO-REB-029 is in_progress.

Decision required
engineering-owner must decide whether the authorized implementation and evidence are complete for WO-REB-029 under DR-WO-COMPLETE; permitted outcomes: implemented, continue, reject.

Next
whether the authorized implementation and evidence are complete (PROC-WO-IMPLEMENT/STEP-WO-IMPLEMENT-DECIDE).

Command or response
Mark WO-REB-029 implemented.
```

The same run with `--json` emits the `se-harness-workflow-result-v2` result. `QG-G4-IMPLEMENTATION-EVIDENCE` passes on all eight predicates:

| Predicate | Status | Message |
| --- | --- | --- |
| `QGP-G4I-STATUS` | pass | `WO-REB-029 status is in_progress.` |
| `QGP-G4I-GRAPH` | pass | `The selected formal graph is valid.` |
| `QGP-G4I-INTEGRITY` | pass | `No repository-integrity blocker prevents selected evaluation.` |
| `QGP-G4I-SCOPE` | pass | `WO-REB-029 declares 5 normalized scope path(s).` |
| `QGP-G4I-COMPLETE` | pass | `The caller explicitly asserted that the declared change set is complete.` |
| `QGP-G4I-PATHS` | pass | `All 13 declared changed path(s) are within execution scope.` |
| `QGP-G4I-PREFLIGHT` | pass | `Released-installation review preflight inputs are ready.` |
| `QGP-G4I-EVIDENCE` | pass | `Fresh retained evidence is bound at docs/engineering/released-evaluator-boundary/evidence/WO-REB-029-verification.md.` |

The result reports `change_set_complete: true`, the same thirteen changed paths against the five declared scope paths, `writes: []`, no scoped blocker and no repository blocker, and `WO-REB-029` `in_progress` both before and after. The governing scope it resolves is `INT-REB-001`, `CAP-REB-001`, `REQ-REB-029`, `SPEC-REB-013`, `SPEC-REB-014`, `ARCH-REB-012`, `ADR-REB-012` and `VER-REB-013`.

`QGP-G4I-EVIDENCE` binds this document to the formal snapshot in its own header. That the predicate passes is also the measurement that adding this document did not move the snapshot digest: `8c1e2d2a26b5a565bd4ff8e019e90c7b7eab7d0bad62c2519716729ee9bd2b16` was read before the file existed and the same digest is bound after it does, because the formal snapshot covers formal artifacts and not retained evidence.

The decision this result requires is the owner's. A passing handoff checkpoint is not a completion, a verification or a release.

## 17. Disclosures and gaps

These are explicit inputs to the commit-bound verification decision, which this file does not make.

1. **The deletion is 585 lines in ten blocks; the work order says roughly 500 in eight ranges.** Three of the ten are not in its list: the `bootstrap_contract` parameter at root line 932, the `if artifact.status == "ready" and bootstrap_contract is not None:` block at 2180, and the keyword argument at 2237. Each is a signature or a call site of a deletion the work order names, which its own words cover, "and the call sites". No rule outside the named ones was removed, and no rule, condition or message was added.
2. **The work order's line ranges do not match the file exactly.** It names `_validate_predecessor_view_evidence` at 1135 to 1457 where the function starts at root line 1133 and spans 325 lines, and the at-most-one-contract rule at 1940 to 1954 where the block spans 18. The ranges were approximations taken while drafting. The measured blocks in section 3 are the authoritative record and are held as an executable constant, so the difference is visible rather than latent.
3. **`_canonical_utf8_text_lf` was deleted although the work order does not name it.** Its only callers were inside `_validate_predecessor_view_evidence`, so it became unreachable. It is a text helper, not a rule.
4. **`ADR-REB-009`'s title still reads "One qualification namespace with five typed operations".** The amendment states why: a decision record states what was decided and editing the title would replace the record with its own consequence. A reader who reads only the title reads five.
5. **`VER-REB-013`'s static check says the four amendments "change no frontmatter field", and two of them move one.** `REQ-REB-008` and `REQ-REB-010` move `updated` from `2026-08-21` to `2026-08-27`. This is the exact form `WO-REB-028` used, which moved `REQ-REB-012`'s `updated` from `2026-08-22` to `2026-08-27`. `ARCH-REB-009` and `ADR-REB-009` change nothing, as their own amendments state. The wording of the contract and the precedent disagree; the precedent was followed and the divergence is recorded here rather than resolved silently.
6. **`docs/notes/harnessctl-reference.md` is unchanged, and the work order's item 6 says "the two notes".** It is not in `execution_scope`, and its two statements about the retirement are still exactly true after this change: that `WO-REB-028` retired a fifth operation, `predecessor-view`, and that `harnessctl rehearse-migration` is the one mechanism for predecessor-to-successor assurance. It was read and deliberately left alone. Reconciling the work order's wording with its own scope is not something this evidence can do.
7. **One existing test was widened.** `test_nothing_reconstructs_a_predecessor_view` skipped both managed validator copies, because one of them still described a predecessor view. The candidate copy no longer does, so the exception was removed and the scan now covers every source in `se_harness`, `repository_tools`, `scripts` and `.github/scripts` with no exception. A separate test permits a retired schema name in the root copy alone, narrowed from both copies. Both changes tighten what is pinned.
8. **No test pinned the two validator copies byte-equal before this change.** `VER-REB-013` case 8 asks every such test to declare the exact expected difference; there was none to amend, so the declaration in section 11 was added. A reviewer should read it as the new pin, not as a relaxation of an old one.
9. **The root copy still carries both rules, so this repository's own verdicts are unchanged.** The retirement reaches consumer repositories at the next release and reaches this repository only when the root evaluator next advances. A repository that adopts the new copy cannot have the change withdrawn from it, which is the assurance rationale for requiring commit-bound verification.
10. **In-tree `se_harness` already runs the edited rules.** `se_harness/preflight.py:242-260` `_load_validator_module()` loads `template_root()/scripts/validate_engineering_artifacts.py`, the candidate copy. So an in-tree `preflight` or `check` reads the deletion, while the 0.7.1 evaluator outside the checkout does not. Every reading presented here as authoritative used the evaluator outside the checkout; the candidate reading in section 4 is labelled as candidate.
11. **The local suite is one failure red, and so is the control.** Section 15 measures it as the Windows CRLF owner-region bound, identical at the same base. The hosted Linux lane is the settling reading.
12. **The hosted lanes for the implementation commit are not in this commit and cannot be.** An evidence file cannot contain the hash of its own commit or the identifiers of runs triggered by it. They are recorded in a later commit on this branch, as `WO-REB-028` did, and `VER-REB-013` requires them enumerated by run identifier per head commit with `validate`, both governance-migration platforms and both integration package platforms named.
13. **`origin/main` advanced to `290f2fb` while this work order was in progress.** That advance is 54 files and 6,960 insertions: a new execution-control-plane definition packet and two notes. It touches no path in this work order's `execution_scope`. This branch is not merged with it, so every graph figure here is 1000 artifacts at this branch state. A later merge would raise the artifact count and move the formal snapshot, and every figure would have to be re-derived against the merged tree.
14. **`VER-REB-012`'s `workflow_dispatch` rehearsal is still open.** `VER-REB-013` requires none and accepts static review of the Pages lane rename as sufficient evidence for a temporary directory name. That acceptance is recorded in `VER-REB-013`'s own approval and does not discharge, re-scope or reopen `VER-REB-012`'s gap.
15. **Issue #220 is where `repository_tools/interpreter_safety.py` is settled.** `WO-REB-028` measured that the module has no production caller left and disclosed the argument both ways. Nothing here changes that module or that open decision.
16. **Two authoring advisories fall on `REQ-REB-029` itself**, `W-AUT-003` for a 322-character statement against a 300-character review threshold and `W-AUT-004` for a free-text `verification_method`. Both are among the 471 maintenance warnings, both pre-date this work order, and neither is an error. Nine more of the same two kinds fall on other requirements in this packet.
17. **The ephemeral wheel of section 10 was deleted.** It was built outside the checkout, never bound to a record, never published or tagged, and its build tree and both virtual environments were removed after the reading. Its `0.8.0` version string is the candidate version in `pyproject.toml`, not a release.
18. **Every figure in this document was measured on Windows 11 with Python 3.11.9 and a CRLF worktree**, under the public 0.7.1 evaluator at `C:\Users\mathi\se-harness-eval-071` for the authoritative readings. Byte counts, digests of worktree files and the owner-region reading of section 15 are platform-dependent by construction; blob identifiers, artifact counts, diagnostic sets and the deleted-line counts are not.
19. **The bound formal snapshot digest hashes worktree bytes, so it is a fixed point of this working tree and not of the committed content.** `formal_snapshot_digest` reads each of the 1000 artifacts with `read_bytes()`. In this worktree 990 artifacts are CRLF, as `core.autocrlf` wrote them on checkout, and 10 are LF, being artifacts authored here and not yet round-tripped through a checkout; three of those are this work order's own packet. The same 1000 artifacts hash to `8c1e2d2a26b5a565bd4ff8e019e90c7b7eab7d0bad62c2519716729ee9bd2b16` as the worktree stands, to `b598e46e159411431ecdf8770a79365e8e1e26949551133ee0024a6546bf5c2c` if every artifact is read as LF, which is how git stores them and how a Linux checkout reads them, and to `bcda3c551425ed4003cd81bef331744f579fdb95bed57cce5d9eb7cb4195e9fd` if every artifact is read as CRLF, which is what a fresh Windows checkout of this commit produces. All three were measured with the released 0.7.1 evaluator. Re-deriving the bound digest therefore requires reproducing these line endings, and no choice of line endings makes one digest reproducible on both platforms. `WO-REB-028`'s evidence binds its digest the same way. Anyone re-measuring should read section 16's `QGP-G4I-EVIDENCE` pass as the binding for this tree and re-derive the digest rather than compare it across platforms.
