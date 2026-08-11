# Verification Evidence for WO-PYP-003

Date: 2026-08-11

## Accountable decision

The repository owner confirmed pull request #13 was merged, reviewed the retained PyPI publication evidence, and explicitly instructed `i merged, then transition and governance commit + PR`. This instruction is the human assurance decision and authorizes the bounded transition, governance commit, normal branch push, and pull request; automation only records it.

## Reviewed lineage

- Merged base: `main` at pull request #13 merge commit `7884db868d74b4c72786c227d5ba070d90557ca9`.
- Implementation work order: `WO-PYP-001`.
- Governing verification contract: `VER-PYP-001`.
- Retained evidence: `docs/engineering/pypi-publication/evidence/WO-PYP-001-verification.md`, SHA-256 `53eab3e9d14d0d84963998933d291fc55f76417479e10624b818227d631bb822`.
- Candidate commit: `01fc231dc1fc4501fd1f74aee9eecfea9c1d9db9`.
- Ready-record governance commit: `8c81c8ae8091d52b62e0998044cacdd888d2989e`.
- Ready-record SHA-256 before transition: `827abd8d6ca6a68f3e5aa7c8a9ca1bd1c10a5ac11d3b6f7aedb8ecf225e74a73`.
- Captured artifact snapshot SHA-256: `3fde3c1a883eb58590bbb969aee57181dde102f94d375a8bb14cac419e3decc2`.

The candidate and ready-record governance commits are available locally and are ancestors of the governance checkout. The later merge and verification-decision governance do not replace the candidate identity named by the record.

## Commands and results

### Formal artifact graph

```powershell
python scripts\validate_engineering_artifacts.py --root .
```

Result: PASS. The expanded graph contains `125` formal artifacts with `0` errors and `0` warnings.

### Automated verification

```powershell
python -m unittest discover -s tests -p "test_*.py"
C:\Users\mathi\Documents\Codex\2026-08-10\st\v0.2.0-final-smoke-311\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
```

Result: PASS on Python `3.14.6` and Python `3.11.9`. Each runtime executed `60` tests with `2` conditional skips because this Windows host cannot create symbolic links. The six focused PyPI workflow-invariant tests also passed.

### CLI, installation, and workflow diagnostics

```powershell
python -m se_harness --help
python -m se_harness doctor .
python -m se_harness dashboard .
```

Result: PASS. CLI help loaded, source doctor passed every required, cross-agent, seed, and managed-file integrity check, and Harness Explorer generated `125` artifacts and `441` relations with `0` errors and `7` derived review warnings. Its snapshot SHA-256 is `b8a6e3e66b20357dd04cd7eb43b499a19aac67f394a0474ccd96dd2bfd43ea04`. PyYAML `BaseLoader` parsed the workflow, and its extracted Bash preflight passed `C:\Program Files\Git\bin\bash.exe -n` syntax validation.

The seven dashboard warnings are non-blocking derived findings: `WO-PYP-003` and the five existing revision-decision work orders have no separate commit-bound verification records, and historical `VREC-AGR-001` remains a possible supersession review item. The formal validator reported no diagnostics.

### Candidate availability and ancestry

```powershell
git cat-file -e "01fc231dc1fc4501fd1f74aee9eecfea9c1d9db9^{commit}"
git merge-base --is-ancestor 01fc231dc1fc4501fd1f74aee9eecfea9c1d9db9 HEAD
git cat-file -e "8c81c8ae8091d52b62e0998044cacdd888d2989e^{commit}"
git merge-base --is-ancestor 8c81c8ae8091d52b62e0998044cacdd888d2989e HEAD
```

Result: PASS. Both immutable lineage commits are locally available ancestors of the governance checkout.

## Transition

`VREC-PYP-001` changed only from `ready` to `verified`, with a human-decision note referencing `WO-PYP-003`. Its candidate commit, Git object format, captured worktree state, capture timestamp, artifact snapshot, evidence path, work-order relation, and verification-contract relation were not changed.

## Deviations and residual risks

- Two conditional symlink tests remain not assessable on this host due to Windows privilege limitations; no symlink behavior changed in this governance decision.
- GitHub and PyPI remain external dependencies. GitHub administrators retain the documented ability to bypass the environment protection rule.
- The governance checkout is later than the verified candidate because it retains the ready record, merge, and verification decision. This expected drift does not alter the candidate binding.
- The seven Harness Explorer warnings require governance review but do not invalidate this candidate or grant supersession, release, or publication authority.

## Authority boundary

This decision verifies `VREC-PYP-001` and authorizes its governance commit, normal branch push, and pull request only. It does not authorize a release record or transition, tag creation or movement, GitHub release mutation, PyPI workflow dispatch or approval, package upload, deployment, pull-request merge, force push, or history rewriting.
