+++
id = "VER-TCM-003"
type = "verification"
title = "Independent evidence for reader-first requirements and the repository-owned glossary"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-09-04"
updated = "2026-09-04"

[relations]
verifies = ["REQ-TCM-006", "REQ-TCM-007", "REQ-TCM-008"]
+++

# Verification Contract: Independent evidence for reader-first requirements and the repository-owned glossary

## Independence

Expected values derive from `REQ-TCM-006`, `REQ-TCM-007`, `REQ-TCM-008`
and the `TCM-RFR-` rules of `SPEC-TCM-003`. Fixture requirements are
written for the tests, never taken from the corpus; the budgets are the
numbers in the rules, not the numbers the implementation reports.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-TCM-006` template | test | the candidate `REQUIREMENT.template.md` and every other definition template | the four reader-first sections are present in the requirement template and no retired section heading remains in any definition template |
| `REQ-TCM-006` advisories | test | one draft fixture per budget, one within every budget, one approved fixture over every budget | each over-budget draft raises exactly its advisory naming file, budget and measured value; the within-budget draft raises none; the approved fixture raises none; `validate` reports PASS throughout |
| `REQ-TCM-006` actor | test | statements opening `THE VALIDATOR SHALL` and `WHEN x, THE INSTALLER SHALL` | no `W-AUT-001` |
| `REQ-TCM-006` Explorer | test | a bundle generated from a fixture with and without `In plain words` | `plain_words` present and equal to the section text, absent otherwise; the built template renders it beneath the statement |
| `REQ-TCM-008` gate | test | a definition without the section and no blocking decision; the same with an open decision naming it in `blocks`; a legacy definition with prose in the section | `QGP-G1-AUTHORING` passes without the section; the decision predicate fails only in the second case and names the decision; `E-DCM-004` in the third |
| `REQ-TCM-008` amendment | inspection | `SPEC-DCM-001` | one amendment record dated and naming `WO-TCM-005`, rule 11 read as legacy |
| `REQ-TCM-007` seed | test | `init` and `adopt` into a fresh directory; a second `init`-like run over an existing glossary; `upgrade` | the glossary exists with no term after the first run; an edited glossary is byte-identical after the second and after `upgrade`; the lock does not list it |
| `REQ-TCM-007` report | test | a fixture corpus with one project term above threshold, one below, one harness term above threshold, and a glossary with one stale entry | the section names the frequent project term and the stale entry, and neither the low-frequency term nor the harness term; two runs give identical output |
| `REQ-TCM-007` boundary | test | the templates directory | no glossary term in any template file; the seed's `Terms` section is empty; this repository's frequent-term list is absent from the templates |
| all | existing suite | the full suite on Windows and the Linux lane | no failure beyond the recorded Windows baseline; skip counts labelled per platform |

## Acceptance scenarios

- Write a requirement in the reader-first shape within every budget; the
  validator is silent about it and the Explorer shows its plain-words line
  under the statement.
- Write a draft with a 40-word statement and a 300-word body; the
  validator names both budgets and still passes.
- Approve a requirement without an `Open decisions` section while a
  decision blocks it; the decision predicate refuses and names `decide`.
- Initialise a repository, edit its glossary, upgrade the harness; the
  glossary is untouched and the lock never lists it.
- Run `inspect` on a repository whose artifacts repeat a word eighty times;
  the vocabulary section names that word and no harness term.
- Grep the templates for the entries of this repository's glossary; find
  none.

## Evidence retention

`docs/engineering/technical-communication/evidence/WO-TCM-005/` and
`docs/engineering/technical-communication/evidence/WO-TCM-006/`: the
handoff packet with the suite figures per platform, the released-evaluator
readings, and the row-by-row mapping of this matrix to test names.

## Pass criteria

Every row of the matrix passes; the two work orders' handoff checks
complete over their Git-derived change sets; the hash-locked root copies
are unchanged; the diagnostic-code index equals its regeneration.

## Residual uncertainty

The reading-grade estimate is not mechanized, so grade 10 for `In plain
words` is a reviewer's judgement, not a test. The English stoplist is a
list; a project term that happens to be a common English word is not
reported. Whether the advisories should become blocking is decided after a
release of use, not by this evidence.
