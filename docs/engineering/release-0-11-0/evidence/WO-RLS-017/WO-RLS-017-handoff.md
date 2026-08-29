```toml
artifact = "WO-RLS-017"
checkpoint = "handoff"
formal_snapshot_sha256 = "2de795df2e57ce5284647f771a6826224f4509db2847e32a2a6fd34b17744cbd"
rebound_at = "2026-08-29T14:29:07Z"
```

# WO-RLS-017 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## 1. What the candidate is

The candidate is the commit that adds this file's sections 1 to 3. No
version move is needed: `pyproject.toml`, `se_harness/__init__.py` and the
README install line read 0.11.0 since `WO-HUP-010`. The packaged bytes are
those of `main` at `8db0b96`, the merge of #268; nothing under
`se_harness/`, no template and no workflow changes on this branch. The
governing evaluator for every reading below is exact public 0.10.0,
installed outside the checkout from the wheel file whose digest
`RLS-SEH-019` binds, invoked with `-I`, on this Windows checkout; since the
0.10.0 root every reading runs natively here (issues #254 and #256 are
repaired in that root).

## 2. Qualification readings

| Check | Actor | Reading |
| --- | --- | --- |
| `validate` | released 0.10.0, outside the checkout, `-I` | 1,144 artifacts, 0 errors, 479 pre-existing maintenance warnings |
| `doctor` | released 0.10.0 | 0 FAIL |
| `preflight --work-order WO-RLS-017 --phase review` | released 0.10.0 | PASS, no diagnostic |
| `release-unit --from v0.10.0 --to <candidate> --exempt 47f67de --contract REL-SEH-022` | released 0.10.0 | section 3 (re-run at the candidate) |
| `qualify complete-candidate --candidate-commit <candidate>` | candidate, `python3 -s`, Linux | section 3 |
| `scripts/validate_release_distributions.py --root .` | candidate | PASS (7 distribution-bearing records) |
| `scripts/check_portable_release_surface.py --repository .` / `--wheel` / `--harnessctl` | candidate | PASS / PASS / PASS, the latter two on an explicitly non-promotable ephemeral wheel built outside the checkout and installed into a disposable environment |
| `repository_tools.upgrade_rehearsal`, twice | released 0.10.0 as predecessor, the ephemeral wheel installed outside the checkout as successor | `overall_result` pass both runs (0.10.0 -> 0.11.0); `semantic_sha256` `7af8e380f002da6cd22fce5a9607bee736e96a0826a61957e3d39c71a35f1fc5` both runs |
| `python scripts/run_tests.py --scale full` | candidate, Windows 11 (CPython 3.14), CRLF checkout at `cf771ad` | 1,128 tests, 26 skipped, 2 failing names, both present on `main` and outside this work order (`test_artifact_authoring...test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`, `test_instruction_architecture...test_owner_region_stays_within_the_size_bound`) |
| `python scripts/run_tests.py` | candidate, Linux | the pull request's suite lane, section 7 |
| `harnessctl check --checkpoint handoff --from-git` | released 0.10.0 | section 6 |

## 3. Census re-run at the candidate

`harnessctl release-unit . --from v0.10.0 --to c016fbb --exempt 47f67de2d4c41b5da0cd8df1b3a5be459de74061 --contract REL-SEH-022`,
released 0.10.0: untraced 0, exempted 1; seven work orders traced, six of
them through the second-parent trailers of the merges GitHub wrote:
`WO-HUP-010`, `WO-ECP-015`, `WO-ECP-016`, `WO-ECP-017`, `WO-ECP-006`
(two merges), `WO-RLS-016` through `103127c` (the merge of the 0.10.0
release record, released by `RLS-SEH-019` and excluded, as the contract
states by construction), and `WO-RLS-017` through its four branch commits.
The comparison reports the four `E-CIP-001` findings the contract predicts
at this stage: no `candidate_commit` and no top-level
`previous_release_tag` are declared (the contract carries the tag in
`[release_unit]`, as `REL-SEH-021` did), the gates differ by exactly
`WO-RLS-016` (traced, released, excluded), and `WO-RLS-017` is
`in_progress`, the state this reading is taken in.

`qualify complete-candidate . --candidate-commit c016fbb` with candidate
source, `python3 -s`, on the Linux environment (WSL Ubuntu 24.04, LF clone
at the candidate, clean): PASS - CC001 candidate runtime bound to the
checkout, CC002 HEAD and tracked tree match the candidate, CC003
artifacts=1144 errors=0 warnings=479, CC004 target state unchanged. On this
Windows interpreter the same command reads CC001 FAIL with `RID018`: a
machine-wide `se-harness 0.8.0` distribution sits on its system
site-packages, the candidate-source runtime boundary `AGENTS.md` documents
and not a property of the candidate; recorded as deviation 1.

## 4. Build of record

Run on 2026-08-29 on this Windows workstation through Docker Desktop
(daemon 29.7.2, linux/amd64) and the pinned producer image, at the exact
candidate `c016fbb`:

| Reading | Value |
| --- | --- |
| command | `python -m repository_tools.release_build replay --repository . --commit c016fbb39e30c0de02604a7242a231151a5df633 --version 0.11.0` |
| state | `exact`; two producer runs `a` and `b` byte-identical |
| producer | `python@sha256:2856e6af199e8128161abd320575eb9b341f3b76f017b5d0c9cd364f60d8a050`, linux/amd64, digest-pinned by `release/build-toolchain.lock` |
| recipe | `release/build-recipe.json`, `0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc` |
| wheel | `se_harness-0.11.0-py3-none-any.whl`, `fef2459585670c81414360d24b5d34c37c8429b5ad723df33dba73530db6c24f` |
| sdist | `se_harness-0.11.0.tar.gz`, `2b6b4307416cca10f234816889c1de16d01a4d51398141c75dd3974eb5cd5c17` |
| checksums | `SHA256SUMS`, `b37d081fc4582c0506e425ea4b8dc0b136d846eec9c0f7134bf666aeea9ffffc` |
| source manifest | `ca051ce45c3abc18bea08a1a98ffd71d65fcc4985dd5a4257fccfa1ab3bec92c`, `source_date_epoch` 1788013748 |
| bundle manifest | `scripts/create_release_bundle_manifest.py` (schema `se-harness-release-bundle/v2`); to be retained as `docs/engineering/release-0-11-0/evidence/RLS-SEH-020-bundle.json` when the record is prepared |
| wheel walk (`VER-ECP-014` scenario 1, repeated on the build of record) | `RECORD` carries none of the ten Phase 4 names and carries `journaled_apply.py`; shipped skills `harness-operator-brief`, `harness-orient`, adapter `harness-orient`; from a disposable `-I` install 25 public submodules import, 29 help pages name no removed concept, `delegated-workflow` is an argument error |

These are local replay readings. The hosted `release-candidate-replay.yml`
dispatch on the review ref, before the release decision, must reproduce the
wheel and sdist digests of the commit the record binds; until it does they
are not quoted in any record.

## 5. Deviations, recorded for the completion decision

1. `qualify complete-candidate` is read from the Linux environment, not
   this Windows interpreter, for the `RID018` boundary reason in section 3;
   the reading is the candidate's own code over the same commit and tree.
