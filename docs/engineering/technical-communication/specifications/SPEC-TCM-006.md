+++
id = "SPEC-TCM-006"
type = "specification"
title = "Reader-first specifications: one rule identity, the contract field and mechanical coverage"
status = "approved"
owners = ["technical-owner", "quality-owner"]
created = "2026-09-06"
updated = "2026-09-06"
contract = "A conforming specification names every rule once, states each rule as one testable sentence, and maps every specified requirement to the rules that meet it."

[relations]
specifies = ["REQ-TCM-014", "REQ-TCM-015", "REQ-TCM-016"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-06T10:57:11Z"
decided_by = "technical-owner"
reason = "Approved by the accountable repository owner on 2026-09-06 with the instruction 'approve as recommended' on PR #358 (REQ-TCM-014, REQ-TCM-015, REQ-TCM-016, SPEC-TCM-006, VER-TCM-006, WO-TCM-009), after the product owner disposed DEC-TCM-001 to DEC-TCM-004 with the options the assessment recommends: identifiers, eight-sections, mechanical-table, advisory-then-blocking."
+++

# Specification: Reader-first specifications: one rule identity, the contract field and mechanical coverage

## In plain words

This specification is written in the shape it prescribes. Each rule below
has a name that never moves and one sentence a test can fail, and the
coverage table at the end says which rules meet which requirement.

## Scope

The managed specification template and its authoring-guide section; a
specification row of the per-type advisory table of `SPEC-TCM-004`; an
additive `contract` field; the coverage table read by the validator and the
Explorer; the deviation reference of `SPEC-DCM-001` rule 3 and its
validator check. No approved artifact is rewritten. The proposal is
`docs/notes/assessment-specification-readability-2026-09-06.md`; the four
decisions it leaves to the owner are `DEC-TCM-001` to `DEC-TCM-004`.

## Terms

- **Rule identifier.** A token `<PREFIX>-<AREA>-NNN`: letters and digits,
  a hyphen, letters and digits, a hyphen, three digits; unique within the
  specification and never reused after removal.
- **Rule.** A paragraph of the `Rules` section that opens with a rule
  identifier in bold, followed by one sentence.
- **Normative keyword.** One of `MUST`, `MUST NOT`, `SHALL`, `SHALL NOT`,
  `MAY`, or the verb `refuses`.
- **Prose budget.** The words of the body outside the `Rules`, `Failure
  behaviour`, `Examples` and `Coverage` sections, with code spans removed.
- **Type table.** The per-artifact-type constants that `SPEC-TCM-004` rule
  `TCM-RFI-003` establishes so shared advisory codes fire with the
  constants of the type being validated.

## Rules

**TCM-RFS-001.** `SPECIFICATION.template.md` MUST carry the common front
matter, a `contract` placeholder with a comment stating its rule, and the
body sections `In plain words`, `Scope`, `Terms`, `Rules`, `Failure
behaviour`, `Examples`, `Coverage` and `Not decided here`, in that order.

**TCM-RFS-002.** The template MUST NOT carry the sections `Actors and
external systems`, `Inputs`, `Outputs`, `State model`, `Data and interface
contracts`, `Security and privacy properties`, `Performance and capacity`,
`Observability` or `Compatibility and migration`.

**TCM-RFS-003.** The specification section of `ARTIFACT_AUTHORING.md` MUST
list the nine sections of TCM-RFS-002 as optional, each with one sentence
stating when it earns its place, and MUST replace "Number rules" with the
rule-identifier line.

**TCM-RFS-004.** `contract` MUST be one sentence of at most 30 words
without a code span, and the validator MUST report `E-AUT-002` when the
field is present but empty or not a string.

**TCM-RFS-005.** A specification without `contract` MUST validate without
error, and no existing specification changes.

**TCM-RFS-006.** The validator MUST read rules from a `Rules` section or,
for legacy files, from a `Behavioral rules` section, as paragraphs opening
with a bold rule identifier.

**TCM-RFS-007.** On specification drafts only, the validator MUST raise
`W-AUT-019` when `contract` is missing, exceeds 30 words, spans more than
one sentence or contains a code span.

**TCM-RFS-008.** On specification drafts only, the validator MUST raise
`W-AUT-020` for each paragraph of the rules section that does not open with
a rule identifier, and for each identifier defined twice.

**TCM-RFS-009.** On specification drafts only, the validator MUST raise
`W-AUT-021` for each rule that exceeds 30 words, spans more than one
sentence, or carries no normative keyword.

**TCM-RFS-010.** On specification drafts only, the validator MUST raise
`W-AUT-022` when the `Coverage` table is absent, when a requirement in
`specifies` has no row, or when a row names a rule identifier the rules
section does not define.

**TCM-RFS-011.** On specification drafts only, the validator MUST raise
`W-AUT-023` when the body carries a `Behavioral rules`, `Open decisions` or
`Approval` heading.

**TCM-RFS-012.** On specification drafts only, the shared codes MUST fire
with specification constants: `W-AUT-005` when the prose budget exceeds
300 words, `W-AUT-007` when a sentence outside the rules exceeds 25 words,
and `W-AUT-009` when `In plain words` is missing or exceeds two sentences.

**TCM-RFS-013.** The validator MUST NOT raise `W-AUT-008` on a
specification, because code identifiers are the substance of a rule.

**TCM-RFS-014.** No advisory of TCM-RFS-007 to TCM-RFS-012 MAY fire on an
approved, implemented or superseded specification, or on any other
artifact type, and the requirement, intent and capability constants MUST
be unchanged.

**TCM-RFS-015.** The `Coverage` section MUST be a table whose first column
is a requirement id in a code span and whose second column lists rule
identifiers separated by commas.

**TCM-RFS-016.** The dashboard generator MUST project `contract`,
`plain_words`, `rules` (each rule's identifier and sentence, in order) and
`coverage` (each row's requirement and rule identifiers) on specification
artifacts where present.

**TCM-RFS-017.** The dashboard generator MUST project `covered_by` on each
requirement artifact: the sorted pairs of specification id and rule
identifier whose coverage rows name it.

**TCM-RFS-018.** The record panel MUST render a specification's contract
first, the plain words beneath it, then the rules as a list whose items
carry an anchor equal to the rule identifier, then the coverage table,
all before the lifecycle events.

**TCM-RFS-019.** The record panel MUST render a requirement's `covered_by`
list as links to the rule anchors, beneath the plain words and before the
lifecycle events.

**TCM-RFS-020.** The validator MUST report `E-DCM-005` when a deviation's
`against` fragment is not a rule identifier defined in the named
specification's rules section.

**TCM-RFS-021.** `SPEC-DCM-001` rule 3 MUST be amended by record so that
its example reads a rule identifier and its text names TCM-RFS-020 as the
check.

**TCM-RFS-022.** The record panel MUST render a deviation's `against`
reference as a link to the rule anchor of TCM-RFS-018.

**TCM-RFS-023.** No approved specification MAY be rewritten for shape; an
approved specification adopts identifiers only when amended for another
reason, keeping each former number in a note beside the identifier.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| A rule identifier appears twice in one specification | one advisory on a draft, silence on an approved file | `W-AUT-020` |
| A coverage row names a rule that does not exist | one advisory on a draft; the Explorer shows the row with no link | `W-AUT-022` |
| A deviation's fragment names no rule | validation fails; the deviation cannot be raised | `E-DCM-005` |
| `contract` is an empty string | validation fails | `E-AUT-002` |
| A specification has no `Rules` and no `Behavioral rules` section | the rules list is empty; coverage rows naming any rule draw `W-AUT-022` on a draft | `W-AUT-022` |
| A requirement is covered by no rule of any specification | `covered_by` is an empty list; no diagnostic, because the relation check of the existing validator already reports a requirement without a specification | none |

## Examples

**Given** a draft in the shape this specification prescribes, each rule one
sentence of at most 30 words with a normative keyword, every sentence
outside the rules under 25 words and every specified requirement in the
coverage table, **when** the validator runs, **then** no advisory of
TCM-RFS-007 to TCM-RFS-012 names it (amended under `WO-TCM-010`; see the
amendment record).

**Given** `SPEC-PYP-001`, approved, with twelve numbered rules under
`Behavioral rules`, **when** the validator runs, **then** it is silent about
the file (TCM-RFS-014) and the Explorer shows its title and body unchanged.

**Given** a draft copy of `SPEC-PYP-001`, **when** the validator runs,
**then** `W-AUT-020` fires twelve times, `W-AUT-023` once and `W-AUT-022`
once (TCM-RFS-008, TCM-RFS-010, TCM-RFS-011).

**Given** a deviation against `SPEC-TCM-006#TCM-RFS-009`, **when** the
validator runs, **then** it passes and the Explorer links the reference to
the rule (TCM-RFS-020, TCM-RFS-022).

**Given** a deviation against `SPEC-TCM-006#rule-9`, **when** the validator
runs, **then** `E-DCM-005` names the specification and the fragment
(TCM-RFS-020).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-TCM-014` | TCM-RFS-001, TCM-RFS-002, TCM-RFS-003, TCM-RFS-004, TCM-RFS-005, TCM-RFS-006, TCM-RFS-007, TCM-RFS-008, TCM-RFS-009, TCM-RFS-011, TCM-RFS-012, TCM-RFS-013, TCM-RFS-014, TCM-RFS-016, TCM-RFS-018, TCM-RFS-023 |
| `REQ-TCM-015` | TCM-RFS-010, TCM-RFS-015, TCM-RFS-016, TCM-RFS-017, TCM-RFS-019 |
| `REQ-TCM-016` | TCM-RFS-020, TCM-RFS-021, TCM-RFS-022 |

## Not decided here

- The exact wording of each advisory and of `E-DCM-005`.
- The tokenizer used for word and sentence counts, and whether a keyword
  inside a code span counts.
- Test names and fixture layout.
- Whether the advisories later become blocking at approval, which
  `DEC-TCM-004` decides as a regime and a later work order executes.
- Whether the state model and other behavioural diagrams join the
  template, which the owner set aside on 2026-09-06.

## Amendment record

- 2026-09-06, under `WO-TCM-010` (approved by the repository owner with "I
  approve WO-TCM-010", PR #364), by the engineering owner. `WO-TCM-009`'s
  evidence packet (disclosure 1) found the first example false as written:
  read as a draft by the candidate validator, this approved specification
  draws `W-AUT-021` on rules `TCM-RFS-003`, `TCM-RFS-010`, `TCM-RFS-012`,
  `TCM-RFS-014` and `TCM-RFS-018`, which run to 31 to 39 words, and
  `W-AUT-007` on a 40-word sentence in `Scope`. The example now describes a
  draft in the prescribed shape within every budget, which the tests of
  `VER-TCM-006` prove. The five rules and the `Scope` sentence stand as
  written: `TCM-RFS-023` forbids a shape rewrite of an approved
  specification, and the rules' identifiers, meaning and coverage are
  unchanged.
