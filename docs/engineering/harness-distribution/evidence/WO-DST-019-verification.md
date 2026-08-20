# WO-DST-019 Implementation and Verification Evidence

Date: 2026-08-20

## Authority and lifecycle

- The repository owner approved `REQ-DST-061`, `SPEC-DST-019`, `ARCH-DST-012`, `ADR-DST-012`, `VER-DST-019`, and `WO-DST-019` with `I approve the issue-80 renumbering packet for implementation`.
- Exact released evaluator: `se-harness 0.5.0a1`, isolated at `work/released-evaluator-0.5.0a1` outside the checkout.
- Start preflight: PASS for `WO-DST-019`; the 15-file reading manifest was read before implementation.
- The implementation approval authorized implementation and retained evidence only; no commit or external authority action was performed under that approval.
- After review preflight, inspection, retained evidence, and this completed verification report, the repository owner explicitly instructed `OK: commit the reviewed candidate under WO-DST-019` on 2026-08-20. This authorizes one local candidate commit containing the bounded reviewed change set; it does not authorize push, pull-request mutation, VREC preparation or transition, release, tag, publication, deployment, or external action.

## Implemented behavior

- Added `harnessctl renumber-artifacts TARGET --map OLD=NEW [--map ...] [--json] [--apply]`.
- Plan mode is read-only. Apply mode re-attests the same deterministic plan and changes only selected `id` fields, parsed typed-relation values, and exact mapped tracked paths.
- Human and JSON output separate `manual_references`, `preserved_evidence_references`, and `unsupported_references`; output sets `manual_action_required` and refuses to claim complete repository repair while semantic work remains.
- Free-form artifact bodies, documentation, source, tests, and captured evidence are not rewritten automatically. Evidence bytes and hashes remain unchanged across path moves.
- Explicit one-to-one type-compatible mappings, clean Git state, full `HEAD`, eligible lifecycle, destination safety, managed ownership, link/hard-link safety, case folding, ignored paths, and VREC/RLS provenance are checked before mutation.
- Apply uses private same-filesystem recovery state, exclusive destination creation, deterministic changes, formal graph and Git-status postconditions, and verified rollback. A later invocation reports unfinished recovery state rather than starting another plan.
- The implementation runs Git without a shell, removes inherited `GIT_*` routing, disables optional index locks and filesystem-monitor integration, and escapes repository-controlled values in human output.

## Changed implementation and documentation

- `se_harness/renumber.py`
- `se_harness/cli.py`
- `tests/test_artifact_renumbering.py`
- `docs/notes/harnessctl-reference.md`
- `docs/engineering/harness-distribution/README.md`
- Governing artifacts `REQ-DST-061`, `SPEC-DST-019`, `ARCH-DST-012`, `ADR-DST-012`, `VER-DST-019`, and `WO-DST-019`
- This evidence file

## Focused verification

| Check | Result |
| --- | --- |
| Windows Python 3.12 focused renumbering suite | PASS: 12 tests in 27.198 seconds |
| Windows Python 3.14 focused and environment-reconciliation set | PASS: 14 tests in 27.910 seconds |
| WSL/POSIX Python 3.12 focused renumbering suite | PASS: 12 tests in 12.949 seconds |
| Multi-map order independence and cross-relation repair | PASS |
| Plan byte/path/index/ref/status preservation | PASS |
| Manual UTF-8/BOM/LF/CRLF/CR reference locations and no free-form edits | PASS |
| Structured UTF-8 BOM and CRLF byte preservation | PASS |
| Evidence and binary/non-UTF-8 classification with unchanged bytes | PASS |
| VREC/RLS reference refusal | PASS |
| Dirty state, lifecycle, type, duplicate, chain, cycle, nested-token, destination, ignore, and hard-link blockers | PASS |
| Injected postcondition failure and exact rollback | PASS |
| Interrupted recovery-state reporting | PASS |
| Capacity: 250 evidence files and 500 mapped occurrences | PASS |

The Windows and POSIX focused suites use disposable initialized Git repositories and compare exact paths and bytes before and after plan, apply, and rollback. Four full-suite tests are skipped on this Windows host because unprivileged symlink creation is unavailable; WSL provides the independent POSIX transaction run.

## Complete regression verification

- Windows bundled Python 3.12.13: PASS, 275 tests in 105.542 seconds, 4 platform skips.
- An initial full run from the released-evaluator Python 3.14 environment exposed two test-environment boundaries rather than candidate defects: Git safe-directory refusal for the externally cloned checkout and released distribution metadata correctly resolving outside candidate source. Both affected checks passed under scoped safe-directory configuration and candidate-source isolation; the complete renumbering suite plus those two checks then passed under Python 3.14.6.
- Existing CLI, authoring, progressive documentation, provenance, integrity, preflight, workflow, package, and release-orchestration regression tests remained green in the final full Python 3.12 run.

## Final repository gates

| Gate | Result |
| --- | --- |
| Exact released 0.5.0a1 formal validation | PASS: 518 artifacts, 0 errors, 44 unchanged maintenance warnings |
| Exact released 0.5.0a1 managed-integrity doctor | PASS; only the 15 existing canonical-placement advisories were reported |
| Release-distribution validation | PASS: 0 distribution-bearing records |
| Candidate-source `renumber-artifacts --help` | PASS; public parser matches `SPEC-DST-019` |
| Review preflight for `WO-DST-019` | PASS with `status = implemented` and no diagnostics |
| Harness inspection | PASS: 518 artifacts, 1 expected assurance-pending item for `WO-DST-019`, 44 existing maintenance findings |
| Harness Explorer generation | PASS: 518 artifacts, 1,894 relations, manifest `0397098d046940b0f2499dff1404fbab9e9779bd0b5c7434082a1c109d9db979` |

Inspection's sole new attention item is the expected non-authoritative prompt to prepare commit-bound verification after the separately authorized clean candidate commit. No ready VREC was prepared because VREC preparation remains a separate authority action.

## Runtime and residual uncertainty

- Exercised runtimes: Windows Python 3.12.13, Windows Python 3.14.6, and WSL Python 3.12.3; Git 2.45.1.windows.1.
- Python 3.11 was not installed in Windows or WSL, so the exact minimum-version run was not locally performable. The implementation uses Python 3.11-compatible standard-library APIs and requires commit-bound verification; the configured candidate CI remains the appropriate independent Python 3.11 execution point after separate commit authority.
- No fresh candidate wheel or release distribution was built because `WO-DST-019` expressly excludes distribution builds.
- A process interruption can leave a private recovery directory. The next invocation fails closed and reports its exact location for inspection; it does not guess that recovery is complete.
- Replacement identifiers can still collide with identifiers selected in unseen refs or clones because allocation, ref scanning, reservation, and remote coordination are deliberately out of scope.
- Human reviewers remain responsible for changing or explicitly documenting each reported current hard reference and for preserving historical narrative intentionally left unchanged.
