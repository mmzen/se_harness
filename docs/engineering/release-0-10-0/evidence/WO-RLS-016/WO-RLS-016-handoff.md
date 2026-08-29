```toml
artifact = "WO-RLS-016"
checkpoint = "handoff"
formal_snapshot_sha256 = "30f6ff8ce7a3efbf5bcdbd1ced708f895694d80c9a45c2c8fa7a72e0ee20d7c0"
rebound_at = "2026-08-29T09:46:32Z"
```

# WO-RLS-016 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## 1. What the candidate is

The candidate is the commit that adds this file's sections 1 and 2. No
version move is needed: `pyproject.toml`, `se_harness/__init__.py` and the
README install line read 0.10.0 since `WO-HUP-009`. The packaged bytes are
those of `main` at `3139f24`, the merge of #259; nothing under
`se_harness/`, no template and no workflow changes on this branch. The
governing evaluator for every reading below is exact public 0.9.0,
installed outside the checkout from the wheel file whose digest
`RLS-SEH-018` binds, invoked with `-I`; where the 0.9.0 root cannot run a
command on this Windows checkout (issues #254 and #256, repaired in this
candidate), the same wheel runs from an isolated Linux environment (WSL
Ubuntu 24.04, CPython 3.12.3) over an LF clone, and the evidence says so.

This file is the keyed handoff packet that the 0.9.0 root's `harnessctl
evidence` writes (`ECP-EVD-001`); it stands where `REL-SEH-021` and
`WO-RLS-016` name `WO-RLS-016-verification.md`, because the packet path is
decided by the evaluator, not the author, as `WO-ECP-012`'s packet recorded.

## 2. Qualification readings

| Check | Actor | Reading |
| --- | --- | --- |
| `validate` | released 0.9.0, outside the checkout, `-I` | 1,115 artifacts, 0 errors, 475 pre-existing maintenance warnings |
| `doctor` | released 0.9.0 | 0 FAIL |
| `preflight --work-order WO-RLS-016 --phase review` | released 0.9.0 | PASS, no diagnostic |
| `release-unit --from v0.9.0 --to <candidate> --contract REL-SEH-021` | released 0.9.0 | section 3 (re-run at the candidate) |
| `qualify complete-candidate --candidate-commit <candidate>` | candidate, `python -s`, no user site | section 3 |
| `scripts/validate_release_distributions.py --root .` | candidate | PASS (6 distribution-bearing records) |
| `scripts/check_portable_release_surface.py --repository .` / `--wheel` / `--harnessctl` | candidate | PASS / PASS / PASS, the latter two on an explicitly non-promotable ephemeral wheel built outside the checkout from a clean `git archive` export of the packet head (`se_harness-0.10.0-py3-none-any.whl`, `8e4bab8f7abb6b6fe940980f68d307462324d41bbad31fb3944281bb4d17df08`, discarded) |
| `repository_tools.upgrade_rehearsal`, twice | released 0.9.0 as predecessor, the ephemeral wheel installed outside the checkout as successor | `overall_result` pass both runs (0.9.0 -> 0.10.0, lock schema 3, successor payload `723c98ec…`); `semantic_sha256` `daae780d3696e9fa6d764aa9c0d2038e63d8a64e85c3eea62837b00eaecbb4ce` both runs |
| `python scripts/run_tests.py --scale full` | candidate, Linux (WSL Ubuntu 24.04, CPython 3.12.3), LF clone at `0579672` | OK, 4 skipped |
| `python scripts/run_tests.py --scale full` | candidate, Windows 11 (CPython 3.12), CRLF checkout at `0579672` | 1,117 tests, 2 failing names, both present on `main` and outside this work order: `test_artifact_authoring…test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`, `test_instruction_architecture…test_owner_region_stays_within_the_size_bound` (the CRLF-only owner-region reading) |
| `harnessctl check --checkpoint handoff --from-git` | released 0.9.0, LF clone | section 6 |
