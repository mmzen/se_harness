# Approval requested: finish adoption with valid human release identities

The repository now selects evaluator **0.22.0**, CI selects 0.22.0, and
development source is **0.22.1**. Its 12-file change exactly matches the
reviewed adoption diff. The full suite passes: **1,259 tests, 22 skips**.

## Blocker

The predecessor CI checker rejects RLS-SEH-032 because it requires the literal
label `release-owner`. The released record correctly names `mmzen` as both
the authorizer and the maker of its ready-to-released decision. The actual
error is `trusted base must contain exactly one released distribution for the target version`.

## Proposed correction

Change only these two implementation/test files:

- `scripts/validate_governor_transition.py`: match the release event to its
  non-empty recorded authorizer, preserving legacy role-label records.
- `tests/test_governor_transition.py`: cover named humans, legacy labels,
  missing or malformed authorizers, and mismatched decisions.

[Exact proposed diff](proposed-correction.patch). No release record or archived
evidence changes. Trusted-base, released-state, unique-record, version, tag,
wheel digest and transaction checks remain in effect.

## Evidence

The temporary proposal reproduces the named-human failure against the original
checker. The correction passes **35 tests, 2 platform skips**, and its planning
check selects RLS-SEH-032 for the real adoption. See [results](prototype-results.json)
and the [original failure](original-assessment.json). The corrected implementation
has not been applied to the repository. Its exact committed assessment, full
combined checks and hosted CI will follow approval.

## Decision

Approve [WO-HUP-029](../../work-orders/WO-HUP-029.md) and
[VER-HUP-024](../../verification/VER-HUP-024.md), with required commit-bound
verification in the planned VREC-HUP-027. Include this bounded correction in
the existing review branch/PR grant. Human verification acceptance and merge
remain separate. Claude and Codex desktop remain untested by this work.

This approval is needed because the checker and test file are outside
[WO-HUP-028](../../work-orders/WO-HUP-028.md)'s approved path scope.
