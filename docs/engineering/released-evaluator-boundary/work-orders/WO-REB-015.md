+++
id = "WO-REB-015"
type = "work_order"
title = "Use one long Windows candidate-test temp path"
status = "in_progress"
owners = ["engineering-owner", "quality-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[assurance]
commit_bound_verification = "required"
rationale = "Exact candidate tests on the retained Windows runner must observe one lexical temporary-root identity rather than conflicting 8.3 and long aliases."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-REB-015"]
specifications = ["SPEC-REB-007"]
architecture = ["ARCH-REB-006", "ADR-REB-006"]
verification = ["VER-REB-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T21:13:25Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-22T21:13:26Z"
decided_by = "engineering-owner"
+++

# Work Order: Use one long Windows candidate-test temp path

## Lifecycle

This bounded corrective work is in progress under the repository owner's explicit authority to finalize release 0.6.0. Commit-bound assurance remains required before another publication retry.

## Objective

Run exact C6 tests with `TEMP` and `TMP` bound to one dedicated non-8.3 path under the already normalized Windows runner temporary root.

## In scope

- Retain run `32598732033`, job `97093696145`, its 645/0 candidate validation, and the seven path-alias test errors/failures.
- Create one dedicated candidate test temporary directory under `temp_root`.
- Export native long-path `TEMP` and identical `TMP` before installing build tools and running candidate tests.
- Assert the exact bounded environment setup remains present.

## Out of scope

- Skipping, filtering, or changing C6 tests; changing product code; changing runner/runtime/toolchain/build inputs; or changing any release, distribution, privilege, credential, or external-policy state.

## Required verification

- Run focused workflow policy, complete release-orchestration, complete isolated suite, current/predecessor graph, distribution, portable-surface, whitespace, and clean-checkout checks.
- Prove the test command remains the complete C6 suite and no result is waived.
- Prepare and verify a later commit-bound VREC before retry.

## Evidence

Retain results in `../evidence/WO-REB-015-windows-test-temp.md`.
