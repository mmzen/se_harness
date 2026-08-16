# WO-IAR-010 implementation and verification evidence

## Authority and scope

The repository owner authorized the bounded `IAR-010` implementation on 2026-08-16. This evidence records implementation checks against `VER-IAR-010`. It does not independently verify the candidate, authorize a commit, prepare or approve a VREC, push, open a pull request, release, publish, or deploy.

## Implemented behavior

- Replaced blanket relation-date comparison with an explicit fail-closed source-type/relation predicate in the shared Harness Explorer finding producer.
- Limited work-order comparison to `draft`, `approved`, and `in_progress`; completed and inactive work remains historical.
- Excluded VREC, RLS, derived, supersession, unknown, and inactive-definition edges from generic temporal reassessment.
- Preserved `W-HEX-003`, derived warning authority, and the existing non-automatic inspection suggestion while adding relation-specific message and evidence.
- Advanced the deterministic finding contract to `harness-findings-v7`.
- Updated the canonical distribution first, then used `harnessctl upgrade . --apply` to synchronize the root managed copy and schema-2 lock while preserving both self-hosting controls.
- Added concise operator documentation and the `IAR-010` domain index.

## Controlled predicate evidence

The focused tests independently cover every relation listed by `SPEC-IAR-010`, all three eligible work-order states, completed and inactive work orders, VREC and RLS states, rejected and superseded definitions, derived and unknown relations, missing/non-strict date boundaries, exact message/evidence fields, and the v7 version marker.

Before implementation, the focused suite failed on the v6 marker, the old generic message, and seventeen historical or unsupported cases. After the managed update:

- Python 3.11 affected suite: 73 tests passed, 1 expected skip.
- Python 3.14 affected suite: 73 tests passed, 1 expected skip.
- Python 3.11 full suite: 188 tests passed, 3 expected skips.
- Python 3.14 full suite: 188 tests passed, 3 expected skips.

Runtimes were Python 3.11.9 and Python 3.14.6.

## Current-repository before and after

The reviewed pre-change breakdown contained nineteen `W-HEX-003` observations: three living architecture dependencies, thirteen completed work-order dependencies, and three VREC dependencies.

The implemented inspection contains exactly three `W-HEX-003` observations and three corresponding non-automatic suggestions:

| Source | Declared relation | Newer target |
| --- | --- | --- |
| `ARCH-DST-007` | `addresses` | `REQ-DST-025` |
| `ARCH-DST-007` | `conforms_to` | `SPEC-DST-007` |
| `ARCH-DST-008` | `conforms_to` | `SPEC-DST-008` |

The full local inspection at this uncommitted implementation state reported 340 artifacts, 1,204 relations, and 75 findings: 0 errors, 30 informational observations, and 45 warnings. Forty warnings are the pre-existing formal maintenance backlog; the remaining non-IAR-010 observations are retained for separate maintenance work.

## Determinism and managed distribution

- Repeated JSON inspection output for the final implemented state had identical SHA-256 `72f2d59846bf942c03142f23100d98ab0350b8fd8e642f14de1246ae4a8b39e5`.
- Two independent Explorer outputs for the final implemented state each reported snapshot SHA-256 `ad29aac0e5f6ff6508992764f06d7ebffb798a69e63cee4647f06b2c1e8e76d6`.
- The root generator and canonical template are text-equivalent after platform newline normalization.
- The schema-2 lock records managed generator digest `d6fe46e4cafcd0524bdee8afdd65cea34d41effdac2fc3b12c4e3500ec02716d`.
- A second `harnessctl upgrade .` plan reported 32 unchanged files and only the two expected protected self-hosting controls; it proposed no managed update.

## Required gates

- `harnessctl validate .` and direct validator execution pass with no errors; the known maintenance warnings remain non-blocking.
- `harnessctl doctor .` passes all required and managed-integrity checks and reports only the known location-maintenance warnings.
- Start and review preflight for `WO-IAR-010` pass and identify the complete governed chain.
- `python -m se_harness --help` exposes the expected command surface.
- `git diff --check` passes; Git reports only expected Windows line-ending notices.
- Generated outputs stay under ignored `target/`; inspection itself remains read-only.

## Changed source and documentation surface

- Root and canonical `scripts/generate_harness_dashboard.py`.
- `tests/test_dashboard_webui.py`.
- `.engineering-harness.lock`.
- `docs/notes/harnessctl-reference.md`.
- `IAR-010` requirement, specification, architecture, ADR, verification contract, work order, evidence, and domain index.

No validator behavior, inspection JSON schema, suggestion catalog, dashboard UI, governor control, package version, release record, or historical maintenance artifact changed.

## Deviations and residual risk

No implementation deviation from `SPEC-IAR-010` was required. Timestamps remain a heuristic attention signal and cannot prove semantic impact. The three remaining architecture findings require accountable maintenance review. Generic temporal reassessment intentionally does not diagnose commit-bound provenance; a future dedicated rule would require separate governance.
