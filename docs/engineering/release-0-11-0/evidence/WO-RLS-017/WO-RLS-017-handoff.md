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

Written at the candidate, after this commit exists; see the next section
of this file in the commit that follows.
