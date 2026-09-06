+++
id = "VER-TCM-007"
type = "verification"
title = "Independent evidence that authoring advisories refuse approval"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-09-06"
updated = "2026-09-06"

[relations]
verifies = ["REQ-TCM-017"]
+++

# Verification Contract: Independent evidence that authoring advisories refuse approval

## Independence

Expected values derive from `REQ-TCM-017` and the `TCM-RFB-` rules of
`SPEC-TCM-007`. Fixture drafts are written for the tests with a known
number of advisories; the gate's message is compared with the validator's
own diagnostics for the same fixture, not the other way round; the budgets
are the constants of `SPEC-TCM-003` to `SPEC-TCM-006` and the tests assert
they are unchanged.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-TCM-017` function | test | `authoring_advisories` on a clean draft, an over-budget draft, an approved artifact with the same body, and one of each other type | the clean draft returns none; the over-budget draft returns exactly the validator's diagnostics; the approved body returns the same as the draft (TCM-RFB-002); other types return none (TCM-RFB-001, TCM-RFB-006) |
| `REQ-TCM-017` refusal | test | an unapplied and an applied `transition` to approved on a requirement draft with a 31-word statement, an intent draft with a 40-word outcome, a capability draft without `under`, a specification draft with two long rules | each is refused; the predicate is `QGP-G1-AUTHORING` or `QGP-G2-AUTHORING`; the message lists each code and message in the validator's order and ends with the corrective sentence; no file is written (TCM-RFB-004, TCM-RFB-005, TCM-RFB-010) |
| `REQ-TCM-017` order | test | a draft with a surviving placeholder and an advisory | the placeholder failure is reported first (TCM-RFB-003) |
| `REQ-TCM-017` other types and targets | test | a verification, an architecture and an ADR draft approved; an approved requirement moved to implemented | approvals pass on the placeholder check alone; the implementation transition reads no advisory (TCM-RFB-006, TCM-RFB-012) |
| `REQ-TCM-017` validation unchanged | test | `validate --advisories` on a repository with drafts drawing twelve advisories | PASS, advisories counted apart, errors and warnings unchanged (TCM-RFB-009) |
| `REQ-TCM-017` budgets unchanged | test | the constants and codes of the four families | byte-equal to the values before this work order (TCM-RFB-008) |
| `REQ-TCM-017` one module | inspection | `authoring_ready`'s source | reads through the validator module the preflight loads; no budget constant in `se_harness/` (TCM-RFB-007) |
| `REQ-TCM-017` checklist | inspection | the four definition sections of `ARTIFACT_AUTHORING.md` | each states that a draft drawing an advisory is not approved until fixed (TCM-RFB-011) |
| `REQ-TCM-017` corpus | test | this repository at the candidate commit | every approved definition transitions in a throwaway copy without reading advisories; the drafts of the packet itself are approved only when clean |
| all | existing suite | the full suite on Windows and the Linux lane | no failure beyond the recorded Windows baseline; skip counts labelled per platform |

## Acceptance scenarios

- Copy `REQ-HUP-031` to a draft in a throwaway repository and approve it:
  refused with five advisories named. Trim it within budget and approve
  again: accepted.
- Approve `SPEC-TCM-007` itself in this repository at the end of the
  packet: accepted, because it is written within its own budgets.
- Approve a verification contract draft with a placeholder left in it:
  refused for the placeholder, with no advisory read.
- Run the full suite and the released-evaluator validation.

## Evidence retention

`docs/engineering/technical-communication/evidence/WO-TCM-011/`: the
handoff packet with the suite figures per platform, the released-evaluator
readings, and the row-by-row mapping of this matrix to test names.

## Pass criteria

Every row of the matrix passes; the work order's handoff check completes
over its Git-derived change set; the hash-locked root copies are unchanged;
the two contract copies stay byte-identical; no budget constant moved.

## Residual uncertainty

The gate reads the validator that ships with the same release, so a
repository whose root lags the candidate is refused by the root's budgets,
not the candidate's; that is the intended reading. Whether owners will
want a per-draft waiver is learned after one release of refusals, not by
this evidence.
