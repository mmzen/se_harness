+++
id = "VER-AUT-002"
type = "verification"
title = "Independent evidence for the advisory class"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-30"
updated = "2026-08-30"

[relations]
verifies = ["REQ-AUT-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-30T08:59:22Z"
decided_by = "assurance-owner"
reason = "Approved by the assurance owner on 2026-08-30 with the words 'Approve and start WO-AUT-004': classification, draft-only, rendering, JSON, CLI, consumer and repository-reading rows; the root validator stays the 0.11.0 copy until the next root adoption."
+++

# Verification Contract: Independent evidence for the advisory class

## Independence

Expected values derive from `REQ-AUT-007` and the `AUT-ADV-` rules of
`SPEC-AUT-002`. The validator tests build fixtures from the specification;
the CLI test drives `harnessctl validate` through `main()`; the
repository-level reading uses this repository's own tree.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-AUT-007` classification | validator tests | a draft requirement with an unknown opener, two `SHALL`s, 301 characters, a free-text `verification_method` | four entries in `advisories`, none in `warnings`; `warning_count` 0; `advisory_count` 4 |
| `REQ-AUT-007` draft only | validator tests | the same four faults on an `approved` requirement | `advisories` empty |
| `REQ-AUT-007` summary and listing | render tests | report with one advisory, with and without `--advisories` | summary shows `Advisories: 1`; the `Advisories:` section only with the flag; `Planes:` unchanged |
| `REQ-AUT-007` JSON | script test | `--json` | `advisories`, `advisory_count` present; `warning_count` and `plane_counts` exclude them |
| `REQ-AUT-007` CLI | `main(["validate", root, "--advisories"])` | fixture repository | the flag reaches the script; exit code unchanged |
| `REQ-AUT-007` consumers | existing `inspect`, `check`, `doctor` tests | unchanged | pass; `inspect`'s finding count excludes advisories |
| `SPEC-AUT-002` this repository | reading | `validate .` with the candidate template script | `Errors: 0`, warnings equal to the pre-change count minus the `W-AUT-*` count, `Advisories: 0` |

## Acceptance scenarios

1. Draft a requirement with two `SHALL`s; `validate --advisories` lists
   `W-AUT-002` under `Advisories:` and the warning count is unchanged.
2. Approve it; `validate --advisories` lists nothing.
3. Run the template validator over this repository; the summary reads
   `Errors: 0 | Warnings: 69 | Advisories: 0` (69 being the count of
   non-`W-AUT` warnings at the candidate commit; the packet states the
   measured figure).

## Evidence retention

Under `docs/engineering/artifact-authoring/evidence/WO-AUT-004/`.

## Pass criteria

Every deterministic test passes on the Linux lane; the Windows workstation
reading is at its baseline. Graph and integrity readings come from the
exact released evaluator, se-harness 0.11.0, installed outside the checkout.

## Residual uncertainty

The root validator copy is the released 0.11.0 one and reports the four
codes as warnings until the next root adoption; the released evaluator's
own `validate .` reading therefore stays at its pre-change count until then.
