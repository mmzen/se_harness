+++
id = "VER-TCM-006"
type = "verification"
title = "Independent evidence for reader-first specifications, coverage and the deviation anchor"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-09-06"
updated = "2026-09-06"

[relations]
verifies = ["REQ-TCM-014", "REQ-TCM-015", "REQ-TCM-016"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-06T10:57:11Z"
decided_by = "assurance-owner"
reason = "Approved by the accountable repository owner on 2026-09-06 with the instruction 'approve as recommended' on PR #358 (REQ-TCM-014, REQ-TCM-015, REQ-TCM-016, SPEC-TCM-006, VER-TCM-006, WO-TCM-009), after the product owner disposed DEC-TCM-001 to DEC-TCM-004 with the options the assessment recommends: identifiers, eight-sections, mechanical-table, advisory-then-blocking."
+++

# Verification Contract: Independent evidence for reader-first specifications, coverage and the deviation anchor

## Independence

Expected values derive from `REQ-TCM-014`, `REQ-TCM-015`, `REQ-TCM-016`
and the `TCM-RFS-` rules of `SPEC-TCM-006`. Fixture specifications are
written for the tests, never taken from the corpus, except where a rule
names a corpus file as its example; the budgets are the numbers in the
rules, not the numbers the implementation reports; a fixture's coverage
rows and rule identifiers are written by the test and compared with what
the validator and the generator read back.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-TCM-014` template | test | the candidate `SPECIFICATION.template.md` | `contract` in the front matter; the eight sections of TCM-RFS-001 present in order; none of the nine sections of TCM-RFS-002 present |
| `REQ-TCM-014` field | test | a specification with a valid `contract`; one without; one with an empty `contract` | the first two validate without error; the third is `E-AUT-002` (TCM-RFS-004, TCM-RFS-005) |
| `REQ-TCM-014` identity and shape | test | one draft per case: a paragraph without an identifier, a duplicate identifier, a 40-word rule, a two-sentence rule, a rule without a keyword, and one draft within every rule | `W-AUT-020` and `W-AUT-021` fire exactly for their cases and once each; the clean draft draws nothing (TCM-RFS-006, TCM-RFS-008, TCM-RFS-009) |
| `REQ-TCM-014` contract advisory | test | drafts with a missing, 40-word, two-sentence and code-span contract | `W-AUT-019` once per draft (TCM-RFS-007) |
| `REQ-TCM-014` legacy and budgets | test | a draft copy of `SPEC-PYP-001`; a draft with 400 words of prose outside the rules; a draft with a 30-word sentence in `Scope`; a draft without `In plain words`; a draft with 40 code identifiers | `W-AUT-023` once; `W-AUT-005` with the specification constant; `W-AUT-007`; `W-AUT-009`; no `W-AUT-008` (TCM-RFS-011 to TCM-RFS-013) |
| `REQ-TCM-014` silence | test | the 135 specifications of this repository at the candidate commit, plus one approved fixture over every budget, plus an intent and a requirement draft over the specification constants but within their own | zero specification advisories from the corpus except `SPEC-TCM-006` while it is a draft; the approved fixture draws nothing; the intent and requirement constants unchanged (TCM-RFS-014) |
| `REQ-TCM-014` checklist | inspection | the specification section of `ARTIFACT_AUTHORING.md` | every checklist line matches a rule, mechanical lines name their code, "Number rules" is absent, the nine optional sections each carry one sentence (TCM-RFS-003) |
| `REQ-TCM-015` coverage advisory | test | a draft whose table omits one specified requirement; one naming an undefined rule; one with no table; one complete | `W-AUT-022` once, once, once; nothing (TCM-RFS-010, TCM-RFS-015) |
| `REQ-TCM-015` projection | test | a bundle generated from a specification with three rules and two coverage rows, and from the requirements it specifies | `rules`, `coverage` and each requirement's `covered_by` equal the fixture's rows; a requirement covered by no rule projects an empty list (TCM-RFS-016, TCM-RFS-017) |
| `REQ-TCM-015` rendering | test | the built Explorer template | a specification record places the contract before the plain words, the rules list with identifier anchors before the coverage table, all before the lifecycle events; a requirement record places `covered_by` links beneath the plain words (TCM-RFS-018, TCM-RFS-019) |
| `REQ-TCM-016` error | test | a deviation against an existing rule identifier; one against `rule-7`; one against an identifier of another specification | the first validates; the second and third are `E-DCM-005` naming the specification and the fragment (TCM-RFS-020) |
| `REQ-TCM-016` amendment and link | inspection, test | `SPEC-DCM-001` rule 3 and its amendment record; the built Explorer template | the example is a rule identifier and the text names TCM-RFS-020; the deviation reference renders as a link to the rule anchor (TCM-RFS-021, TCM-RFS-022) |
| all | test | the two contract copies, the diagnostic-code index | byte-identical; the index equals its regeneration and lists `W-AUT-019` to `W-AUT-023` and `E-DCM-005` |
| all | existing suite | the full suite on Windows and the Linux lane | no failure beyond the recorded Windows baseline; skip counts labelled per platform |

## Acceptance scenarios

- Validate this repository with the candidate: the only specification
  advisories name `SPEC-TCM-006` while it is a draft, and none after its
  approval.
- Copy `SPEC-PYP-001` to a draft; twelve `W-AUT-020`, one `W-AUT-023` and
  one `W-AUT-022`; validation passes.
- Generate the Explorer for this repository; open `SPEC-TCM-006` and see
  the contract, the plain words, 23 anchored rules and the coverage table;
  open `REQ-TCM-015` and see the five rules that cover it.
- Raise a deviation against `SPEC-TCM-006#TCM-RFS-009` in a throwaway copy;
  it validates and its reference links to the rule. Change the fragment to
  `rule-9`; `E-DCM-005`.
- Run the full suite and the released-evaluator validation on this
  repository.

## Evidence retention

`docs/engineering/technical-communication/evidence/WO-TCM-009/`: the
handoff packet with the suite figures per platform, the released-evaluator
readings, and the row-by-row mapping of this matrix to test names.

## Pass criteria

Every row of the matrix passes; the work order's handoff check completes
over its Git-derived change set; the hash-locked root copies are unchanged;
the diagnostic-code index equals its regeneration; the requirement, intent
and capability constants of the type table are unchanged.

## Residual uncertainty

The reading grade of `In plain words` is not mechanized. A normative
keyword is checked as a word, so a rule that reads "the validator reports"
passes review only if the reviewer asks whether it is an obligation. The
one-sentence rule is measured by a sentence splitter that treats a period
inside a code span as text. Whether the advisories become blocking is
decided by `DEC-TCM-004` and executed later, not by this evidence.
