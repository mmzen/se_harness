# WO-OCA-002 implementation and verification evidence

## Authority and scope

The repository owner approved correction points 1 and 2, withheld the other proposed operating-model extensions, and instructed implementation of the explicit OPS migration on 2026-08-16. This evidence records completed work and derived checks against `VER-OCA-002`. It does not independently verify the candidate or authorize a commit, push, pull request, VREC transition, release, tag, publication, or deployment.

## Implemented controls

- `OPS.assures` is now typed as `operating_contract -> requirement`; a known wrong target type emits structure diagnostic `E011` for every OPS lifecycle state.
- Every active OPS must assure an active requirement with at least one work order in `implemented`, `verified`, or `released` that directly implements it. Missing readiness emits governance diagnostic `E017`.
- When `revision_provenance.required_for_verified_work` is true, at least one completed implementing work order must be covered by a `verified` or `released` VREC. Missing eligible coverage emits policy diagnostic `E018`.
- One eligible implementation path is sufficient. Unrelated incomplete work does not invalidate it, and automation does not approve or transition the OPS.

The canonical validator was changed first. `harnessctl upgrade . --apply` then synchronized the root validator and `TRACEABILITY.md` and refreshed `.engineering-harness.lock`. A final upgrade plan reports 32 unchanged managed files and only the two protected self-hosting controls.

## Explicit legacy migration

`OPS-DST-001.assures` changed from `REL-DST-001` to exactly `REQ-DST-001..006`. `OPS-REV-001.assures` changed from `REL-REV-001` to exactly `REQ-REV-001..008`. Both contracts remain `approved`; their owners and operating prose are unchanged. These sets match the original accepted packets and deliberately do not infer later domain requirements.

Together with the six contracts activated by `WO-OCA-001`, all eight approved OPS records now use requirement-only targets. Formal repository validation confirms that every assured requirement is active and has both completed implementing work and an eligible verified or released VREC path under the configured policy.

## Automated verification

- Focused operating-readiness tests pass for REQ, REL, SPEC, and unknown targets; inactive requirement states; absent, incomplete, and completed work states; policy on/off; every eligible and ineligible VREC state; multiple implementation paths; inactive OPS behavior; and exact diagnostic planes.
- The focused readiness, revision-provenance, and taxonomy suite passes: 42 tests with one expected skip.
- Python 3.11.9 full suite: 195 tests passed with 3 expected skips.
- Python 3.14.6 full suite: 195 tests passed with 3 expected skips.
- Fresh-install, upgrade, package-data, validator parity, provenance, dashboard, CLI, and managed-integrity coverage is included in the full suite.

## Repository gates

- `harnessctl validate .` passes with 354 artifacts, zero errors, and the same 40 pre-existing maintenance warnings: `structure E0/W0`, `governance E0/W0`, `policy E0/W0`, `maintenance E0/W40`.
- `harnessctl doctor .` passes required files, distribution parity, managed integrity, and the released self-hosting governor check; only the known historical-location advisories remain.
- Start preflight for `WO-OCA-002` passes and selects the complete authorized chain.
- Two consecutive final JSON inspections are byte-identical. The snapshot contains 354 artifacts, 1,289 relations, zero error findings, zero informational findings, and 43 warning findings; the captured UTF-8 output SHA-256 is `e632f99d28152ac2b272087ea69dbeea5619fe5efe95914bf6cb79800b95a35e`.
- `git diff --check` passes with only expected Windows line-ending notices.

## Residual boundary

This change proves graph reachability to one eligible implementation and commit-bound verification path. It does not prove continuing real-world conformance with an operating contract, require every later work order to be verified, attach OPS records to releases, or add recurring operational assessment. Those extensions were not approved. Long-term graph-schema compatibility is separately deferred to GitHub issue #52.
