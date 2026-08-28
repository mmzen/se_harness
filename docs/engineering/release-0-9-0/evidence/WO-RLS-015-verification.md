# WO-RLS-015 implementation evidence

artifact: WO-RLS-015
checkpoint: handoff

Retained by the implementation actor on 2026-08-28. This file is evidence. It
does not complete, verify, or release the work order.

## 1. What the candidate is

The candidate is the commit that adds this file's sections 1 and 2 and the
index line. No version move is needed: `pyproject.toml`,
`se_harness/__init__.py` and the README install line read 0.9.0 since
`WO-HUP-008`. The packaged bytes are those of `main` at `effbcbc`, the
merge of #251; nothing under `se_harness/`, no template and no workflow
changes on this branch. The governing evaluator for every reading below is
exact public 0.8.0, installed outside the checkout from the wheel file whose
digest `RLS-SEH-017` binds, invoked with `-I`.

## 2. Qualification readings

| Check | Actor | Reading |
| --- | --- | --- |
| `validate` | released 0.8.0, outside the checkout, `-I` | 1,088 artifacts, 0 errors, 473 pre-existing maintenance warnings |
| `doctor` | released 0.8.0 | 0 FAIL |
| `preflight --work-order WO-RLS-015 --phase review` | released 0.8.0 | ready, no diagnostic |
| `release-unit --from v0.8.0 --to <candidate> --contract REL-SEH-020` | released 0.8.0 | section 3 (re-run at the candidate) |
| `qualify complete-candidate --candidate-commit <candidate>` | candidate, `python -s`, no user site | section 3 |
| `scripts/validate_release_distributions.py --root .` | candidate | PASS (5 distribution-bearing records) |
| `scripts/check_portable_release_surface.py --repository .` / `--wheel` / `--harnessctl` | candidate | PASS / PASS / PASS, the latter two on an explicitly non-promotable ephemeral wheel built outside the checkout from a clean tree (`se_harness-0.9.0-py3-none-any.whl`, `f3fa54573a1760e83c72e3d134d37d40f299bf8a16a32a2eaf8d00631341255a`) and its `harnessctl` entry point |
| `repository_tools.upgrade_rehearsal`, twice | released 0.8.0 as predecessor, the ephemeral wheel installed outside the checkout as successor | `overall_result` pass both runs (0.8.0 -> 0.9.0 | lock 3 0.9.0); `semantic_sha256` `74437a1ccea16fc4937d1224345949db481bbbf8236edd55fb40b5808f800ce0` in both, equal |
| `python scripts/run_tests.py --scale full` | candidate, Linux, CPython 3.12 | 1,117 tests, 1 failure, 4 skipped; the failure is `test_release_build…test_declared_mode_set_is_what_a_posix_export_already_carries`, the file-mode artefact of this checkout that passes on the hosted runner; the Windows figure is the hosted lane's |
| `harnessctl check --checkpoint handoff` | released 0.8.0 | section 5 |
