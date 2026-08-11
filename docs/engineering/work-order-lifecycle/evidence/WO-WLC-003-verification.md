# Verification Evidence for WO-WLC-003

Date: 2026-08-11

## Accountable decision

The repository owner confirmed pull request #15 was merged, reviewed the retained lifecycle-consistency evidence, and explicitly instructed `i merged, then transition and governance commit + PR`. This instruction is the human assurance decision and authorizes the bounded status transition, governance commit, normal branch push, and pull request; automation only records it.

## Reviewed lineage

- Merged base: `main` at pull request #15 merge commit `0236f771d16a3cb4cdd28a95f92d264db002c81f`.
- Implementation work order: `WO-WLC-001`.
- Governing verification contract: `VER-WLC-001`.
- Candidate commit: `b907860afdb3e4eb387c00588f74e8d29c4ec136`.
- Ready-record governance commit: `2db0a1e26c7b92eb34fdc3ea23874da4f3d3a92f`.
- Retained evidence: `docs/engineering/work-order-lifecycle/evidence/WO-WLC-001-verification.md`, SHA-256 `a307a35f89541f54f87a68c328780c427aa18018138d7c90baeb9d12bfa6f5ce`.
- Ready-record SHA-256 before transition: `ffa00b369d417dd39a984dbaacac55bb8b722b5f9ef80e39b26f4d5f8e361d32`.
- Captured artifact snapshot SHA-256: `ad9dd5d800f44b1fd71ca2bd81295477999f771920368f54a446ee4c03d6ae21`.

The candidate and ready-record commits are available locally and are ancestors of the governance checkout. The later ready record, merge, and assurance-decision governance do not replace the candidate named by the VREC.

## Transition

`VREC-WLC-001` changed only from `ready` to `verified`, with a human-decision note referencing `WO-WLC-003`. Its candidate commit, Git object format, captured worktree state, capture timestamp, artifact snapshot, evidence path, work-order relation, and verification-contract relation were not changed.

## Commands and results

### Formal artifact graph

```powershell
python scripts\validate_engineering_artifacts.py --root .
```

Result: PASS with `143` formal artifacts, `0` errors, and `0` warnings.

### Automated verification

```powershell
python -m unittest discover -s tests -p "test_*.py"
C:\Users\mathi\Documents\Codex\2026-08-10\st\v0.2.0-final-smoke-311\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
```

Result: PASS on Python `3.14.6` and Python `3.11.9`. Each runtime executed `62` tests with `2` conditional skips because this Windows host cannot create symbolic links.

### CLI, installation, Explorer, lineage, and diff

Result: PASS. CLI help loaded, source doctor passed every required, cross-agent, seed, and managed-file integrity check, and Harness Explorer generated `143` artifacts and `501` relations with `0` errors and `1` derived warning. Its snapshot SHA-256 is `2a99e39b26617efcbd20f6cf67d6cf71e9f48f81d1e2ca31da36650277da36a8`. The sole warning remains the unrelated non-authoritative stale-ready review for `VREC-AGR-001`.

Candidate and ready-record commit availability and ancestry passed. Captured-field comparison confirmed every VREC front-matter field except `status` is unchanged. `git diff --check` passed, and the final change surface contains exactly the VREC transition, `WO-WLC-003`, and this evidence.

## Deviations and residual risks

- Two conditional symlink tests remain not assessable on this Windows host; no symlink behavior changed in this assurance decision.
- GitHub remains an external dependency; the PR is not merged by this work order.
- The governance checkout is later than the verified candidate by design and does not alter the captured candidate binding.

## Authority boundary

This decision verifies `VREC-WLC-001` and authorizes its bounded governance commit, normal push, and pull request only. It does not authorize another lifecycle transition, a release, tag, GitHub release change, merge, PyPI workflow action, package upload, publication, deployment, force push, or history rewriting.
