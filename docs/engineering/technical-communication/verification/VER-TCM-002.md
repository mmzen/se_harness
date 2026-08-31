+++
id = "VER-TCM-002"
type = "verification"
title = "Independent evidence for the diagnostic-code index"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-31"
updated = "2026-08-31"

[relations]
verifies = ["REQ-TCM-005"]
+++

# Verification Contract: Independent evidence for the diagnostic-code index

## Independence

Expected values derive from `REQ-TCM-005` and the `TCM-DCI-` rules of
`SPEC-TCM-002`; the known-code sample is taken from the source modules the
assessment named as undocumented (`MG`, `RID`, `EPS`, `PRE`), never from
the generator's own output.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-TCM-005` no drift | test | regenerate in memory, compare to the committed page | byte-equal after newline normalization; `--check` exits non-zero on an edited copy |
| `REQ-TCM-005` coverage | test | every registered prefix | at least one code per prefix; the known set (`A001`, `I001`, `E012`, `W013`, `W-AUT-002`, `WEX210`, `WEX-ECP-030`, `MG001`, `RID018`, `EPS001`, `JNL001`, `PRE001`, `REN010`, `RR001`, `PV001`) present |
| `REQ-TCM-005` exclusion | test | artifact and rule identifiers | `WO-ECP-010`, `SPEC-ECP-006`, `ECP-DLG-001`, `SHA256` absent from the code tables |
| `TCM-DCI-003` page shape | test | the committed page | generated marker, target-expertise comment, Summary section, prefix table, per-prefix tables |
| `TCM-DCI-006` links | existing + new test | notes index and check note | the index row resolves (the progressive-documentation link test covers the index); the check note names the page |
| `TCM-DCI-004` determinism | test | two regenerations | identical bytes |

## Acceptance scenarios

1. Run the suite: the pinning test passes on the committed page.
2. Append a fake diagnostic to a copy of the page: `--check` exits
   non-zero naming the drift.
3. Read the page: an operator finds `MG001` under the mutation-guard
   prefix with its message text, without opening the source.

## Evidence retention

Under `docs/engineering/technical-communication/evidence/WO-TCM-003/`.

## Pass criteria

Every deterministic test passes on the Linux lane; the Windows workstation
reading is at its baseline. Graph and integrity readings come from the
exact released evaluator, se-harness 0.11.0, installed outside the
checkout.

## Residual uncertainty

The registry is curated: a wholly new diagnostic prefix added without
registration would be invisible to the index until registered. The pinning
test cannot detect that case; review of changes that add a prefix remains
the control.
