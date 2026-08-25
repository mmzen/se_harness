+++
id = "VER-HUP-005"
type = "verification"
title = "Verify standard-root adoption of the released successor of 0.6.0"
status = "draft"
owners = ["assurance-owner", "quality-owner", "security-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
verifies = ["REQ-HUP-010", "REQ-HUP-011"]
+++

# Verification Contract: Verify standard-root adoption of the released successor of 0.6.0

## Requirement-to-evidence matrix

| Rule | Method | Evidence | Pass condition |
|---|---|---|---|
| `HUP5-PRE-001` | record inspection | the released RLS and the work order's table | digests equal; work order approved after the table is complete |
| `HUP5-PRV-001` | isolated identity capture | evaluator evidence JSON | released-evaluator origin; version, wheel, payload equal the record |
| `HUP5-TRX-001/002` | plan review and apply transcript; lock diff | retained plan, before/after lock digests | only the expected managed set changed; fragments byte-exact; owner content untouched |
| `HUP5-PST-001` | successor `doctor`, `validate`, `preflight`, `check`; router text | command transcripts | 0 FAIL, 0 errors, closed manifest, corrective form rendered, scope section present |
| `HUP5-PST-002` | scratch `raise-risk` | transcript | raised risk accepted by the root validator; handoff blocked |
| `HUP5-PST-003` | full suite on both platforms | figures | pass with the exceptions retired |
| `HUP5-PST-004` | notes diff | text | version and date stated |

## Pass criteria

All of the above on Windows and Linux; the successor's `validate` reports 0
errors on the complete graph; the work order's handoff check completes under
the successor, which is now the governor.
