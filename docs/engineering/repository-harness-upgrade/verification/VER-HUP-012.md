+++
id = "VER-HUP-012"
type = "verification"
title = "Independent evidence for the lock-schema floor"
status = "approved"
owners = ["assurance-owner", "security-owner"]
created = "2026-08-30"
updated = "2026-08-30"

[relations]
verifies = ["REQ-HUP-024"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-30T19:20:01Z"
decided_by = "assurance-owner"
reason = "Approved by the accountable owner on 2026-08-30 by selecting the presented option 'Approve, start, complete on green' for WO-HUP-012: refusal, writer, deletion-sweep, guard, hash-bound, script and repository rows; readings from the exact released 0.11.0 evaluator outside the checkout."
+++

# Verification Contract: Independent evidence for the lock-schema floor

## Independence

Expected values derive from `REQ-HUP-024` and the `HUP-LSF-` rules of
`SPEC-HUP-012`, never from the changed modules. Fixture repositories are
built by the tests with hand-written schema-1 and schema-2 locks; the
repository-level readings use this repository's own schema-3 root and the
exact released evaluator.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-HUP-024` refusal | test | doctor and upgrade on a fixture with a `"schema": 1` lock and one with `"schema": 2` | each fails before any write with the one floor diagnostic naming schema 3 and re-adoption; the tree and lock bytes are unchanged |
| `REQ-HUP-024` writer | test | applied init, adopt, and a schema-3-to-schema-3 upgrade | every emitted lock declares `"schema": 3`; the schema-1 preservation branch is gone |
| `REQ-HUP-024` deletion | test + sweep | `se_harness/` and `scripts/` | no `LEGACY_CANONICAL_LOCK_SCHEMA`, `legacy_tracked_sha256`, `matches_legacy_newline_variant`, `legacy-canonical`, `legacy-newline-variant`, or `legacy exact` survives |
| `HUP-LSF-005` guard | test | ordinary mutation on a fixture with a pre-3 lock | fails at read with the floor diagnostic wrapped by the guard's existing read failure; `MG002` is emitted by no path and stays reserved |
| `HUP-LSF-006` hash-bound | test | a canonical-mode declared digest recorded over CRLF bytes | fails; only the canonical digest matches; raw mode unchanged |
| `HUP-LSF-007` script | test | the transition assessment on a schema-2 lock fixture | refused naming schema 3 |
| `SPEC-HUP-012` this repository | reading | the exact released 0.11.0 evaluator outside the checkout | `doctor` 0 FAIL, `validate` 0 errors, distributions PASS on the schema-3 root |

## Acceptance scenarios

1. Build a fixture with a schema-2 lock: `doctor` fails one check naming
   the floor; `upgrade --apply` refuses before writing; every file byte is
   unchanged afterward.
2. Delete the fixture's lock and run `adopt`: it proceeds under the
   existing non-overwrite behavior and writes a schema-3 lock.
3. Sweep the package and scripts for every deleted symbol and label: zero
   hits.

## Evidence retention

Under `docs/engineering/repository-harness-upgrade/evidence/WO-HUP-012/`.

## Pass criteria

Every deterministic test passes on the Linux lane; the Windows workstation
reading is at its baseline. Graph and integrity readings come from the
exact released evaluator, se-harness 0.11.0, installed outside the
checkout.

## Residual uncertainty

No live pre-3 consumer root is available to test against; the fixtures are
constructed from the schema definitions the retired code carried. The
released 0.11.0 root evaluator keeps its own read paths until the next
root adoption, so this repository's gate behavior is unchanged until then.
