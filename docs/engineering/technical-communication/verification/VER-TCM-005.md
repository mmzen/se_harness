+++
id = "VER-TCM-005"
type = "verification"
title = "Independent evidence for reader-first capabilities and the graph-read derivation"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-09-04"
updated = "2026-09-04"

[relations]
verifies = ["REQ-TCM-012", "REQ-TCM-013"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-04T19:45:21Z"
decided_by = "assurance-owner"
reason = "Approved by the accountable repository owner on 2026-09-04 with the instruction 'i apprive' (approve), after reviewing PR #342 (REQ-TCM-012, REQ-TCM-013, SPEC-TCM-005, VER-TCM-005, WO-TCM-008), carrying the owner's four decisions on the capability assessment of the same day."
+++

# Verification Contract: Independent evidence for reader-first capabilities and the graph-read derivation

## Independence

Expected values derive from `REQ-TCM-012`, `REQ-TCM-013` and the
`TCM-RFC-` rules of `SPEC-TCM-005`. Fixture capabilities are written for
the tests, never taken from the corpus; the budgets are the numbers in the
rules, not the numbers the implementation reports; the deriving
requirements of a fixture are written into the fixture's requirements, not
read back from the generator.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-TCM-012` template | test | the candidate `CAPABILITY.template.md` | the three reader-first sections are present in order, `ability` is in the front matter, and none of the four retired headings remains |
| `REQ-TCM-012` field | test | a capability with a valid `ability`; one without; one with an empty `ability` | the first two validate without error; the third is `E-AUT-002` |
| `REQ-TCM-012` advisories | test | one draft fixture per budget of TCM-RFC-003, one within every budget, one approved fixture over every budget, one intent draft and one requirement draft over the capability constants but within their own | each over-budget capability draft raises exactly its advisory naming file, budget and measured value; the within-budget draft, the approved fixture, the intent and the requirement raise none of the capability advisories |
| `REQ-TCM-012` corpus | test | the 36 capabilities of this repository | zero `W-AUT` advisories, because every one is approved |
| `REQ-TCM-012` checklist | inspection | the capability section of `ARTIFACT_AUTHORING.md` | every checklist line matches a rule or a section of TCM-RFC-001, mechanical lines name their code, the line "lists its derived requirements" is absent, the two guidance sentences are present |
| `REQ-TCM-013` template | test | the candidate `CAPABILITY.template.md` and the checklist | no `Candidate requirements` or `Derived requirements` heading or line |
| `REQ-TCM-013` projection | test | a bundle generated from a capability with three deriving requirements, one with none, one with a legacy list naming two of five | `derived_requirements` equals the sorted ids from `derives_from` in every case, and never the legacy list |
| `REQ-TCM-013` rendering | test | the built Explorer template | the record panel places the ability before the plain words, both before the `Derives` list, and all before the lifecycle events; the lineage second stage carries the ability |
| `REQ-TCM-013` legacy | test | a draft with a `Candidate requirements` heading | `W-AUT-018` once and nothing else from the capability family |
| all | existing suite | the full suite on Windows and the Linux lane | no failure beyond the recorded Windows baseline; skip counts labelled per platform |

## Acceptance scenarios

- Write a capability in the reader-first shape within every budget with a
  22-word ability; the validator is silent about it and the Explorer shows
  the ability, the plain words and the deriving requirements.
- Write a draft with a 60-word ability lacking `under` and a body ending in
  a `Candidate requirements` list; the validator names `W-AUT-016` and
  `W-AUT-018` and still passes.
- Open `CAP-HUP-003` in an Explorer bundle of this repository; its two
  deriving requirements appear under the title from the graph, and its
  approved body is unchanged.
- Run the full suite and the released-evaluator validation on this
  repository.

## Evidence retention

`docs/engineering/technical-communication/evidence/WO-TCM-008/`: the
handoff packet with the suite figures per platform, the released-evaluator
readings, and the row-by-row mapping of this matrix to test names.

## Pass criteria

Every row of the matrix passes; the work order's handoff check completes
over its Git-derived change set; the hash-locked root copies are unchanged;
the diagnostic-code index equals its regeneration; the intent and
requirement constants of the type table are unchanged.

## Residual uncertainty

The reading grade of `In plain words` is not mechanized. The words `can`
and `under` are checked as words, so an ability written around them
("is able to", "when") passes the mechanical check and fails only review.
Whether the capability layer should stay mandatory is decided after one
release of use, not by this evidence.
