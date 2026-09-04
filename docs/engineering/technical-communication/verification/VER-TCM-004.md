+++
id = "VER-TCM-004"
type = "verification"
title = "Independent evidence for reader-first intents and the Explorer's outcome line"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-09-04"
updated = "2026-09-04"

[relations]
verifies = ["REQ-TCM-009", "REQ-TCM-010", "REQ-TCM-011"]
+++

# Verification Contract: Independent evidence for reader-first intents and the Explorer's outcome line

## Independence

Expected values derive from `REQ-TCM-009`, `REQ-TCM-010`, `REQ-TCM-011`
and the `TCM-RFI-` rules of `SPEC-TCM-004`. Fixture intents are written
for the tests, never taken from the corpus; the budgets and the acceptance
vocabulary are the values in the rules, not the values the implementation
reports. The 33 approved intents are a negative control: none may raise an
advisory.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-TCM-009` template | test | the candidate `INTENT.template.md` | the four reader-first sections are present in order, `outcome` is in the front matter, and none of the five retired headings remains |
| `REQ-TCM-009` field | test | an intent with a valid `outcome`; one without; one with an empty `outcome` | the first two validate without error; the third is `E-AUT-002` |
| `REQ-TCM-009` advisories | test | one draft fixture per budget of TCM-RFI-003, one within every budget, one approved fixture over every budget, one requirement draft over the intent constants but within the requirement ones | each over-budget intent draft raises exactly its advisory naming file, budget and measured value; the within-budget draft raises none; the approved fixture raises none; the requirement draft raises none of the intent advisories; `validate` reports PASS throughout |
| `REQ-TCM-009` corpus | test | the 33 intents of this repository | zero `W-AUT` advisories |
| `REQ-TCM-009` checklist | inspection | the intent section of `ARTIFACT_AUTHORING.md` | every checklist line matches a rule or a section of TCM-RFI-001, mechanical lines name their code, and the two sentences of TCM-RFI-005 are present |
| `REQ-TCM-010` acceptance | test | a draft with one operational row, one row naming each word of the acceptance vocabulary, one `Today` of `not measured`, one target of `0` | `W-AUT-013` once per acceptance row naming its measure; nothing on the operational row, the honest baseline or the zero target |
| `REQ-TCM-010` empty | test | a draft with the section and no data row; a draft with a malformed table | `W-AUT-014` once in each case and nothing else |
| `REQ-TCM-011` projection | test | a bundle generated from fixtures with and without `outcome` and `In plain words` | `outcome` and `plain_words` present and equal to the source text, absent otherwise; requirement records unchanged |
| `REQ-TCM-011` rendering | test | the built Explorer template | the record panel places the outcome before the plain words and both before the lifecycle events; the lineage first stage carries the outcome under the title |
| `REQ-TCM-011` condition | test | a work order reaching an intent with `outcome` and one measure row; one reaching an intent with `outcome` and no row; one reaching a legacy intent | `intent_quality` reads `satisfied`, `not_assessable`, `not_assessable`; the G0 gate's `intent_chain` condition is unchanged in all three |
| all | existing suite | the full suite on Windows and the Linux lane | no failure beyond the recorded Windows baseline; skip counts labelled per platform |

## Acceptance scenarios

- Write an intent in the reader-first shape within every budget, with three
  operational measures; the validator is silent about it and the Explorer
  shows its outcome and plain words under the title.
- Write a draft with no `outcome`, a 473-word Problem, sixteen line-range
  citations and a row observed "every CI run"; the validator names the
  outcome, the Problem budget, the citations and the acceptance row, and
  still passes.
- Approve that draft unchanged; every advisory falls silent.
- Generate the bundle for this repository; every intent renders as before
  and every G0 `intent_quality` condition reads `not_assessable`.
- Run the corpus check; the 33 approved intents raise nothing.

## Evidence retention

`docs/engineering/technical-communication/evidence/WO-TCM-007/`: the
handoff packet with the suite figures per platform, the released-evaluator
readings, and the row-by-row mapping of this matrix to test names.

## Pass criteria

Every row of the matrix passes; the work order's handoff check completes
over its Git-derived change set; the hash-locked root copies are
unchanged; the diagnostic-code index equals its regeneration.

## Residual uncertainty

The reading-grade estimate is not mechanized, so grade 10 for `In plain
words` is a reviewer's judgement, not a test. The acceptance vocabulary is
a closed list; a row observed by a check named in other words is not
reported. Whether the advisories should become blocking is decided after a
release of use, not by this evidence.
