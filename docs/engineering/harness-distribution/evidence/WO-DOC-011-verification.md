# WO-DOC-011 verification evidence

Date: 2026-08-13

## Scope and authority

This evidence covers the documentation-only implementation authorized by `WO-DOC-011`: three supplied Harness Explorer screenshots, their concise placement in the public README, and a focused regression assertion. It is retained implementation evidence, not an accountable verification decision, VREC, release decision, or publication record.

The work reuses the approved `REQ-DST-020` / `SPEC-DST-006` / `ARCH-DST-006` / `ADR-DST-006` / `VER-DST-006` chain. No runtime, managed template, package metadata, lifecycle rule, historical VREC/RLS fact, dashboard candidate, or release surface changed.

## Supplied assets and exact copies

| Supplied file | Repository file | Bytes | Dimensions | SHA-256 |
| --- | --- | ---: | ---: | --- |
| `screenshort_report_1.png` | `docs/images/harness-explorer-overview.png` | 678217 | 3073 x 1813 | `54a9cb0e0aca2172c0eab05d7af032094dfc09f6b883276fd1d3b3cc61f94e81` |
| `screenshort_report_2.png` | `docs/images/harness-explorer-lineage.png` | 191706 | 3012 x 1816 | `d88ecd0723af28c647169fa054cd610cd8e972068282b108d2eaf8709b772eb6` |
| `screenshort_report_3.png` | `docs/images/harness-explorer-readiness.png` | 206335 | 3069 x 1828 | `de661bf32879570ffaf63be3d694f49248f412a54d1c5fc497345f93e8e8c429` |

PowerShell `Get-FileHash -Algorithm SHA256` produced identical source and repository hashes for every pair. A standard-library PNG-header inspection confirmed the signatures and dimensions. No crop, annotation, recompression, or metadata edit was performed.

## README assessment

- The gallery is inside `What this looks like in practice`, after the existing workflow diagram and before `What you get`; no new top-level section was introduced.
- Display order is Overview, Lineage, Readiness.
- Each image has meaningful alternative text and a repository-relative `docs/images/...` link.
- Captions explain the reader question rather than duplicating dashboard documentation.
- The closing boundary says the views are derived and read-only and do not approve work, verify a commit, or authorize a release.
- The README remains below the enforced 200-line and nine-top-level-heading limits.

## Automated verification

| Check | Result |
| --- | --- |
| `python -B -m unittest tests.test_public_onboarding -v` | PASS: 14 tests |
| `python -B -m unittest discover -s tests -p "test_*.py"` | PASS: 148 tests, 3 expected skips |
| `python -B scripts/validate_engineering_artifacts.py --root .` | PASS: 281 artifacts, 0 errors, 38 pre-existing compatibility/location warnings |
| `python -B -m se_harness doctor .` | PASS: required and managed files intact; existing location advisories reported |
| `python -B -m se_harness --help` | PASS |
| start `preflight` for `WO-DOC-011` | PASS while status was `approved`; complete governing manifest inspected |
| `git diff --check` | PASS |

The focused onboarding test asserts the exact three-image sequence, relative paths, repository containment, file existence, PNG signature, and the derived-authority wording. Its existing Markdown traversal also confirms all ordinary local README links resolve.

## Deterministic Explorer check

Two real-repository generations used separate explicit external output directories. Both reported 281 artifacts, 986 relations, 0 errors, 39 derived warnings, and snapshot SHA-256:

`1e558043ff6c5e910d052ca4c97fc2aa043620e8d507bcb7222f0ab946d690ea`

The two `dashboard-data.json` hashes were identical. The generated output remained external and is not formal authority or part of this change.

## Changed and protected paths

Expected paths are `README.md`, the three PNG files under `docs/images/`, `tests/test_public_onboarding.py`, `WO-DOC-011.md`, and this evidence file. Managed policy, managed templates, CLI/runtime source, package metadata, version files, historical verification/release records, `VREC-DST-007`, and candidate commit `52e713a9b041a0c8355f2ad8ad8f71c7dd65d1f2` are unchanged.

## Manual review and residual limits

Source review confirms that a 6/10 reader can connect each screenshot to a practical question without treating the dashboard as a decision-maker. The detailed screenshots are intentionally full-size rather than cropped; renderer scaling determines their displayed size. Local checks verify portable relative paths and files, but a future PyPI publication preview remains necessary because external Markdown renderers can handle repository-relative image URLs differently.

No accountable verification, commit, push, pull request, merge, release, package publication, or deployment is claimed by this evidence.
