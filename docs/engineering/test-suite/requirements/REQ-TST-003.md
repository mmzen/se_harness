+++
id = "REQ-TST-003"
type = "requirement"
title = "Take a standard repository from a per-session cache instead of running init in every fixture"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-26"
updated = "2026-08-26"
statement = "WHEN a test fixture needs a fresh standard repository, THE SYSTEM SHALL copy it from one repository initialised once per test session and SHALL yield bytes identical to a direct init."
verification_method = "automated-test-and-timed-comparison"
[relations]
derives_from = ["CAP-TST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T19:18:13Z"
decided_by = "requirements-steward"
+++

# Requirement: Take a standard repository from a per-session cache instead of running init in every fixture

## Rationale

`harnessctl init` writes 61 files with durable atomic writes and costs
about 0.57 seconds; about three hundred tests run it in `setUp`, close to
half the serial suite. A copied tree costs about 0.05 seconds and is
byte-identical.

## Preconditions and trigger

A fixture calls the shared helper for a fresh standard repository.

## Required response

- A helper in `tests/` initialises one standard repository into a
  session-scoped temporary directory on first use and returns
  `shutil.copytree` copies afterwards, each in the caller's own temporary
  directory.
- The copy is byte-identical to a direct `init` (asserted by a test that
  compares the two trees, including the lock).
- Tests that assert on `init`'s own behaviour (its output, its refusal
  paths) keep calling `init` directly.

## Failure and boundary behavior

If the cache directory has been removed, the helper re-initialises it.

## Constraints

Fixture helpers only; no change to the installer.

## Acceptance examples

**Given** the helper **When** called twice **Then** `init` ran once and both
trees equal a direct `init`'s bytes.

## Open decisions

None.
