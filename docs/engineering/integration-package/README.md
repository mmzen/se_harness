# Integration Package

This domain governs installable, commit-addressed packages produced for testing
candidate SE Harness behavior without creating release authority.

## Formal chain

- Intent: `INT-IPK-001`
- Capability: `CAP-IPK-001`
- Requirements: `REQ-IPK-001`, `REQ-IPK-002`, `REQ-IPK-003`
- Specification: `SPEC-IPK-001`
- Architecture: `ARCH-IPK-001`
- Decision: `ADR-IPK-001`
- Verification: `VER-IPK-001`
- Work order: `WO-IPK-001`

Every artifact is initially `draft`. The packet authorizes nothing until the
accountable owners apply the managed lifecycle transitions and separately start
the work order.

## Boundary

An integration package is an expiring GitHub Actions artifact. It is installable
for testing, but it is never a PyPI publication, GitHub Release asset, release
record, governing evaluator, or promotable distribution.
