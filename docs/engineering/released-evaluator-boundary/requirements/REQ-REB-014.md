+++
id = "REQ-REB-014"
type = "requirement"
title = "Keep failure injection local to the exclusive-create boundary"
status = "approved"
owners = ["requirements-steward", "quality-owner", "security-owner"]
created = "2026-08-22"
updated = "2026-08-22"
statement = "WHEN assurance injects exclusive-create or between-write failures, THE SYSTEM SHALL intercept only the repository adapter boundary and SHALL remain compatible with supported platform cleanup implementations."
verification_method = "automated-python311-linux-windows-failure-injection-matrix"

[relations]
derives_from = ["CAP-REB-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T07:15:02Z"
decided_by = "requirements-steward"
+++

# Requirement: Keep failure injection local to the exclusive-create boundary

## Rationale

Hosted C4 run `32558379908` exposed two errors because tests patched the shared process-wide `os.open`. Linux Python 3.11 temporary-directory cleanup calls `os.open(..., dir_fd=...)`; the test side effects accepted only the adapter's three positional arguments. Windows qualification did not exercise that cleanup path.

The production rollback behavior was not the failing invariant, but a platform-sensitive mock invalidates the required assurance evidence. Failure injection must target an adapter-owned seam rather than a shared standard-library module object.

## Preconditions and trigger

- The adapter performs an exclusive create or a recheck between its two authorized writes.
- Assurance needs deterministic failure before, during, or after that boundary.
- Python 3.11 and the current supported runtime execute on Windows and Linux cleanup implementations.

## Required response

- Introduce or use one adapter-local exclusive-create seam with the same flags, mode, and fail-closed behavior as the existing operation.
- Patch only that seam in tests; do not replace process-global `os.open`.
- Preserve existing atomicity, rollback, idempotence, permission, and error-translation behavior.
- Run the focused failure matrix and complete suite on Python 3.11/Linux and the current qualification runtime.

## Failure and boundary behavior

Any injected failure that escapes the intended call, interferes with temporary cleanup, changes call ordering nondeterministically, leaves an output, or masks the original adapter error fails qualification.

## Constraints

- Do not weaken production `O_EXCL` behavior or replace it with pre-existence checks.
- Do not special-case operating systems in the product contract.
- Do not treat a test-only correction as evidence that the hosted predecessor-assessment gap is solved.

## Acceptance examples

### Example: normal behavior

**Given** Linux Python 3.11 and an injected second exclusive-create failure

**When** the adapter exits and its temporary directory is cleaned

**Then** the intended adapter error is observed, the new evidence is rolled back, and cleanup completes without mock interference.

### Example: failure behavior

**Given** a mock on the shared `os.open` module

**When** cleanup supplies `dir_fd`

**Then** assurance rejects the test design even if it happens to pass on Windows.

## Open decisions

Internal helper naming is delegated. Process-local interception, unchanged exclusive-create semantics, and cross-platform qualification are not.
