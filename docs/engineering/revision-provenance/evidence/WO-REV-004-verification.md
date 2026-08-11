# Verification Evidence for WO-REV-004

Date: 2026-08-11

## Accountable decision

The repository owner reviewed the retained aggregate verification evidence and explicitly instructed `i validate, then transition and governance commit`. This instruction is the human assurance decision and authorizes the bounded governance commit; automation only records it.

## Reviewed lineage

- Aggregate implementation work order: `WO-AGR-001`.
- Portable-integrity implementation work order: `WO-PMI-001`.
- Governing verification contracts: `VER-AGR-001` and `VER-PMI-001`.
- Retained evidence: `docs/engineering/aggregate-release/evidence/WO-AGR-001-verification.md` and `docs/engineering/portable-managed-integrity/evidence/WO-PMI-001-verification.md`.
- Candidate commit: `505e889777c3c50f544b7e6d6fe58e2f765c1fea`.
- Ready-record governance commit: `0f7ee89d3a2078ebcf2f34120e209f81b4024d73`.
- Verification record: `VREC-PMI-001`, with unchanged candidate commit, clean captured worktree state, SHA-1 object format, both retained evidence paths, and artifact snapshot SHA-256.

The candidate commit is available locally and is an ancestor of the current governance checkout. The later ready-record and verification-governance commits do not replace the candidate named by the record.

## Commands and results

### Formal artifact graph

```powershell
.\.venv\Scripts\python.exe scripts/validate_engineering_artifacts.py --root .
```

Result: PASS. 86 artifacts, 0 errors, 0 warnings after the status transition and governance work order were present.

### Automated verification

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

Result: PASS. 45 tests run, with 2 conditional skips because this Windows host cannot create symbolic links.

### CLI and installation diagnostics

```powershell
.\.venv\Scripts\python.exe -m se_harness --help
.\.venv\Scripts\python.exe -m se_harness doctor .
```

Result: PASS. The CLI surface loaded and all 28 tracked installed-harness integrity checks passed.

### Candidate availability and ancestry

```powershell
git cat-file -e "505e889777c3c50f544b7e6d6fe58e2f765c1fea^{commit}"
git merge-base --is-ancestor 505e889777c3c50f544b7e6d6fe58e2f765c1fea HEAD
```

Result: PASS. The declared candidate is a locally available commit and remains in the governance checkout's ancestry.

## Transition

`VREC-PMI-001` changed only from `ready` to `verified`, with a human-decision note referencing `WO-REV-004`. Its candidate commit, object format, captured worktree state, timestamp, artifact snapshot, evidence paths, and typed relations were not changed.

## Deviations and residual risks

- The two conditional symlink tests remain not assessable on this host due to Windows privilege limitations; no symlink behavior changed in the verified work.
- Pull request #5 is not required to be merged for the assurance decision: the immutable candidate and later ready record are available on the current branch. If the pull request is rebased or squashed, the recorded candidate commit must remain reachable for provenance to remain useful.
- The current checkout is later than the verified candidate because it retains governance records. This expected checkout drift does not alter the candidate binding.

## Authority boundary

This decision verifies `VREC-PMI-001` only and authorizes its separate governance commit. It does not authorize a release record, tag, push, pull request update, merge, package publication, deployment, or release transition.
