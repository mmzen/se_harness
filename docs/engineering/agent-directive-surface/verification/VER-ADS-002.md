+++
id = "VER-ADS-002"
type = "verification"
title = "Independent evidence for a bounded reading surface without retired files"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
verifies = ["REQ-ADS-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T11:40:02Z"
decided_by = "assurance-owner"
+++

# Verification Contract: Independent evidence for a bounded reading surface without retired files

## Independence

Expected values derive from `REQ-ADS-007` and `SPEC-ADS-002`; fixtures are
written from the specification, not from candidate output.

## Requirement-to-evidence matrix

| Rule | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `ADS-RDS-001` manifest | preflight test, start and review | fresh install with one packet | manifest equals router, card, owner file, then the chain; no routed policy listed |
| `ADS-RDS-002` card | template byte test; mutation test | contract with one added stop condition | template equals rendering; size under 1,024; exactly `## Stop when` and `## Traps`; mutation fails conformance |
| `ADS-RDS-003` router | installed router text | rendered router | sentence present verbatim; no command name; each `HRN-` ID once |
| `ADS-RDS-004` owner region | substring and size tests | this repository's `AGENTS.md` | names the note anchor; does not name the retired path; under 6,000 bytes; every other `REQ-IAR-020` fact present |
| `ADS-RDS-005` note and removal | file and index tests | tree | note section present with the four paragraphs; retired file absent; index line absent |
| `ADS-RDS-006` supersession | graph validation | `REQ-IAR-020`, `REQ-ADS-007` | validator passes with `REQ-IAR-020` superseded and `REQ-ADS-007` implemented |
| `ADS-RDS-007` inventory | retirement tests | repository `*.md` scan | only historical records and the migration note name the path |

## Acceptance scenarios

1. Install, add a packet, run both preflight phases; assert the closed manifest.
2. Regenerate the card; assert bytes, size, and sections; mutate; assert failure.
3. Read this repository's owner region; assert the note anchor and the
   absence of the retired path; measure bytes.
4. Run the complete suite on Windows and Linux; label figures per platform.
5. Run released-evaluator identity, doctor, validate, review preflight, and
   the handoff check with the complete changed-path set.

## Pass criteria

All deterministic tests pass on both platforms; the released evaluator
reports 0 errors; the handoff check completes; no root managed file or lock
changes.
