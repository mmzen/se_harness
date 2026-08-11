# Verification Evidence for WO-REV-006

Date: 2026-08-11

## Accountable decision

The repository owner reviewed the retained aggregate 0.2.0 candidate evidence and explicitly instructed `i validate, then transition and governance commit`. This instruction is the human assurance decision and authorizes the bounded governance commit; automation only records it.

## Reviewed lineage

- Aggregate candidate: `VREC-SEH-001`, originally `ready`.
- Candidate commit: `1329c7a4472f323c4b21d869545cad3c647fe568`.
- Ready-record governance commit: `656f94276b7d6100c6c344c0b4db8cf1c1db261c`.
- Captured artifact snapshot SHA-256: `df8d285cf7aed30ef3f64eac6abfc5f2ca674724af42fac3afe07b707bc11374`.
- Work orders: `WO-AGR-001`, `WO-DOC-001`, `WO-DOC-002`, `WO-DST-001`, `WO-DST-002`, `WO-DST-003`, `WO-PMI-001`, `WO-REV-001`, `WO-RLS-001`, and `WO-VSP-001`.
- Verification contracts: `VER-AGR-001`, `VER-DST-001`, `VER-DST-002`, `VER-PMI-001`, `VER-REV-001`, and `VER-VSP-001`.
- Ready-record SHA-256 before transition: `119d662741b184833334bd1fc0f488fa113d4dc118b8bc881867c05e8114cab2`.

The candidate commit is available locally and is an ancestor of the current governance checkout. The ready-record governance commit retains the record after the candidate and does not replace the candidate identity it names.

## Retained evidence hashes

| Work order | Evidence SHA-256 |
|---|---|
| `WO-AGR-001` | `46152a7ed36e7e61e02c2099c8ccdd42a75a6894c1a49db2c9f26e5ef862888e` |
| `WO-DOC-001` | `2d1c2fc243a5c6d72233461e99b5326bc6d3a757a965d6bc85fcc84a5b74ef4e` |
| `WO-DOC-002` | `d8c9e59c535a8e56c3b2e74afb603664af0e1031e9749c9d3c3e93d46a99b04a` |
| `WO-DST-001` | `03df533a36faa1f57e3c8b3f9dc6364465410f3c7c5a014b8b32719462551ac5` |
| `WO-DST-002` | `d93e24bdcab6e91e44aae3053b0a7c6d7af33740bcc7cb22f2ce02c980ffe602` |
| `WO-DST-003` | `6b245ac8beb7d013c3f1b814e43a5520fcb0a94dccd23d321ce57f9cc93cd44e` |
| `WO-PMI-001` | `606acef1dab666bc24ed8d659b6ad8c552c927eee1c3a02a7459c2ee3e7b8972` |
| `WO-REV-001` | `dcbea1039bad5dd7db7cc1eb4c9171eaee885a3dd9bf3c03b11225dd824ea5ad` |
| `WO-RLS-001` | `08fcc8cfe8415d34be0c2938d3852b5491e3b346edc798737d8f43d14db4aec3` |
| `WO-VSP-001` | `9461428b2d57086238cc1b5d01c8de18dc42b86e66b1741fb68c4222e5f3f5c2` |

## Commands and results

### Formal artifact graph

```powershell
.\.venv\Scripts\python.exe scripts\validate_engineering_artifacts.py --root .
```

Result: PASS. `107` artifacts, `0` errors, and `0` warnings after the transition and governance decision work order were present.

### Automated verification

```powershell
py -3.11 -m unittest discover -s tests -p "test_*.py"
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
```

Result: PASS on Python `3.11.9` and Python `3.14.6`. Each runtime executed `54` tests with `2` conditional skips because this Windows host cannot create symbolic links.

### CLI and installation diagnostics

```powershell
py -3.11 -m se_harness --help
.\.venv\Scripts\python.exe -m se_harness doctor .
```

Result: PASS. The CLI surface loaded on the minimum supported runtime, and every required, cross-agent, seed, and managed-file integrity check passed on the source repository.

### Candidate availability and ancestry

```powershell
git cat-file -e "1329c7a4472f323c4b21d869545cad3c647fe568^{commit}"
git merge-base --is-ancestor 1329c7a4472f323c4b21d869545cad3c647fe568 HEAD
git log -1 --format="%H" -- docs/engineering/release-0.2.0/verification-records/VREC-SEH-001.md
```

Result: PASS. The candidate is a locally available ancestor, and the ready record was retained by governance commit `656f94276b7d6100c6c344c0b4db8cf1c1db261c`.

### Dashboard and diff review

```powershell
.\.venv\Scripts\python.exe -m se_harness dashboard .
git diff --check
git status --short
```

Result: PASS. Dashboard generation reported `107` artifacts, `383` relations, `0` errors, and `6` derived review warnings. The final snapshot SHA-256 is `00abd18f508983bd5e9334f91727d7d1a5f8edbf2773f64dad4f8c04f51b90aa`. The verified aggregate resolved the prior release-bearing coverage warnings; the remaining warnings concern governance-only verified work orders and the known stale-ready history. Diff hygiene passed, and only `WO-REV-006`, its evidence, and the bounded `VREC-SEH-001` transition were present.

## Transition

`VREC-SEH-001` changed only from `ready` to `verified`, with a human-decision note referencing `WO-REV-006`. Its candidate commit, Git object format, captured worktree state, timestamp, artifact snapshot, ten evidence paths, ten work-order relations, and six verification-contract relations were not changed.

## Deviations and residual risks

- Two conditional symlink tests remain not assessable on this host due to Windows privilege limitations; no symlink behavior changed in this governance decision.
- The current checkout is later than the verified candidate because it retains ready-record and verification-decision governance. This expected checkout drift does not alter the candidate binding.
- The dashboard will continue to show review warnings for governance-only verified work orders without separate commit-bound VRECs and for stale-ready history; these warnings neither invalidate this exact candidate nor grant supersession authority.
- Pull request #10 currently contains the candidate and ready record. This transition commit remains local until separately authorized push or PR update.

## Authority boundary

This decision verifies `VREC-SEH-001` only and authorizes its separate governance commit. It does not authorize release-record preparation or transition, an immutable tag, a push or pull-request update, GitHub release creation, PyPI publication, deployment, or any other release action.
