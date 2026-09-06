# Assessment of specification readability, 2026-09-06

<!-- Target expertise: 4/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> Point-in-time. Measured on `main` at `aad82a9`, the first commit governed
> by the 0.15.0 root. This note is an operator analysis. It has no
> authority. The managed contract, the formal artifacts and the accountable
> decisions stay authoritative. This note changes no rule. It proposes. It
> is the fourth pass after the
> [requirement](assessment-requirement-readability-2026-09-04.md),
> [intent](assessment-intent-readability-2026-09-04.md) and
> [capability](assessment-capability-readability-2026-09-04.md)
> assessments, and it uses their method and their vocabulary.

## Summary

A specification is where the detail lives. A requirement says what must be
true; the specification says exactly how, in rules that a test can cite, a
work order can execute and a deviation can name. It is the artifact the
implementer reads most and the verifier reads first. Today the reader finds
a median body of 760 words at a reading grade above college, arranged in
one of 79 heading shapes, with rules that are identified two different ways
because the template and the checklist disagree: the template says "number
rules", the checklist says give each a stable identifier. Seventy-one
files number, forty-one use identifiers, twenty have no rules section at
all. Half of the 1,431 rules carry no word that makes them a rule.

The result in two sentences. The specification layer holds the most
valuable content in the graph and cites it worst: a rule is addressed as
"rule 3" in 29 work orders and 33 evidence packets, an address that moves
the day a rule is inserted, and 54 of 132 verification contracts never
name a specification at all. The fourteen-section template asks for
sections that fewer than half the authors have anything to say in, so the
authors write the sections anyway, and the reader wades through them to
reach the rules.

This note measures the 135 specifications, names the causes, and proposes
one rule identity, a template of seven sections with the rest optional, a
`contract` field, draft-time advisories, a mechanical coverage table and a
forward-only migration. It ends with the four decisions that belong to the
owner.

## Terms

Terms used below, in plain words. The [glossary](../../GLOSSARY.md) has
the rest.

- **Rule.** One testable sentence in a specification that an implementation
  must satisfy. The unit a test, a work order and a deviation cite.
- **Rule identifier.** A stable name for one rule, `<PREFIX>-<AREA>-NNN`,
  that does not change when rules are added or removed around it.
- **Coverage.** The statement that every requirement a specification
  `specifies` is met by at least one of its rules.
- **Deviation.** A decision artifact of kind `deviation`, which names the
  one rule an implementation cannot meet as `SPEC-xxx#<rule>`.
- **Advisory.** A validator message that informs but does not fail
  validation. The `W-AUT` family fires only on drafts.
- **Reading grade.** The Flesch-Kincaid estimate of the school year a
  reader needs. Grade 8 to 10 is plain language for a technical audience;
  grade 14 is college level.

## Method

Every file under `docs/engineering/*/specifications/` was read by a
script. The body was measured for words, sentence length, passive-voice
markers, code identifiers in backticks and section headings, with code
spans, tables and headings removed from the prose measures. The rules
section was measured for its identification form, the number of rules,
their length and whether each carries a normative or refusal verb. Every
verification contract, work order and evidence packet was searched for the
way it cites a rule. The `specifies` relation was compared with the
requirements the body names. Three files were read in full: the shortest
(`SPEC-RCD-001`), the median (`SPEC-PYP-001`) and the longest
(`SPEC-AEX-003`), with `SPEC-TCM-005` as the identifier-led example. The
template, the checklist in `ARTIFACT_AUTHORING.md`, the decision
specification `SPEC-DCM-001` and the validator were read against the
corpus.

## What the corpus looks like

| Measure | Reading |
| --- | --- |
| Specifications | 135: 97 `approved`, 32 `implemented`, 6 `superseded` |
| Requirements per specification | median 2, up to 18 |
| Body length | median 760 words, from 124 to 4,493; 91 files carry more than 300 words outside their rules and examples |
| Reading grade | median 18.4, highest 34.8 |
| Sentence length | 134 files carry a sentence over 25 words; 129 carry one over 40 |
| Passive voice | 1,183 markers; 99 files with five or more |
| Code identifiers | median 42 per body; 118 files over 20 |
| Template shapes in use | 79 distinct heading sets; 48 files carry all 14 template sections |
| Sections present | `Scope` 115, `Compatibility and migration` 91, `Explicitly unspecified decisions` 90, `Behavioral rules` 95; the other eight between 52 and 67 |
| Sections the template does not have | `Failure behaviour` 32, `Terms` 27, `Coverage` 26, `Amendment record` 19, `Rules` 12, `Purpose` 10 |
| Rules section | present in 115 files under some name, absent in 20 |
| Rule identification | 71 files number their rules, 41 lead each rule with a stable identifier, 3 write prose; 490 distinct identifiers exist |
| Rules per file | median 11, up to 40 |
| Rule length | 1,431 rules; median 26 words, longest 243; 751 over 25 words, 127 over 50 |
| Rules with a normative or refusal verb | 737 of 1,431 |
| Coverage | 26 files carry a `Coverage` table, and all 26 list every specified requirement; 83 bodies never name a requirement they specify |
| How rules are cited | "rule N" in 29 work orders, 33 evidence packets, 5 verification contracts; an identifier in 23 verification contracts (88 identifiers); 54 of 132 verification contracts name no specification |
| Deviation reference | `against = "SPEC-xxx#<fragment>"`; the example is `#rule-7`; no specification renders such an anchor and nothing checks the fragment exists |
| Mechanical checks on the checklist's three lines | none; no `W-AUT` advisory fires on a specification |
| Trend | of the 11 specifications drafted in September, 10 lead with identifiers |

## Findings

### Two rule identities, and the managed documents disagree

The template says: "Number rules so tests and discussions can reference
them." The checklist says: "Every rule carries a stable identifier
(`<PREFIX>-<AREA>-NNN`) and one testable sentence." The corpus followed
both. Seventy-one files number, and the number is the address: `WO-HUP-016`
executes "rule 3", `VER-HUP-016` measures "rule 10", the evidence packet
reports "rules 8, 9 and 10". Forty-one files lead each rule with an
identifier, `TCM-RFC-003`, `ECP-ADM-001`, `WEX-ECP-002`, and their
verification contracts cite the identifier.

A number is an address that moves. The 19 amendment records in the corpus
show how a specification changes after approval: rules are added at the
end, because inserting one would renumber the citations in every work
order and packet. So the rules of an amended specification are in the
order they were written, not the order a reader needs. An identifier costs
one token per rule and never moves. The September drafts already chose
it, 10 of 11.

### The deviation mechanism has no anchor to point at

Since the 0.15.0 root, a deviation names the rule it departs from as
`against = "SPEC-xxx#<fragment>"`. The validator accepts any fragment. No
specification renders a heading or anchor for `rule-7`, so the link in the
Explorer resolves to nothing, and a typo in the fragment is not caught.
With identifiers as rule names, the fragment is the identifier, the
Explorer can anchor it, and the validator can refuse a fragment that names
no rule of that specification.

### Half the rules are not written as rules

A rule is a sentence someone can fail. Of 1,431 rules, 737 carry a word
that says so: shall, must, only, never, refuses, rejects, fails. The other
694 are descriptions in the indicative: "The lock records the archive
pair." A reader cannot tell a description of the current code from an
obligation the code must keep. The requirement layer solved this with the
`WHEN ... THE SYSTEM SHALL` form and an advisory that reads it; the
specification layer has no form and no advisory.

Rule length has the same shape as everywhere else in the corpus: median
26 words, and 127 rules over 50. `SPEC-PYP-001` rule 9 names the
publisher, its pinned commit, the version tag and three conditions in one
sentence. It is correct. It is not one testable sentence.

### The template asks fourteen questions and most have no answer

The template has fourteen sections. Four of them are present in more than
two thirds of the files: `Scope`, the rules, `Compatibility and migration`
and `Explicitly unspecified decisions`. The other ten are present in
between 38 and 50 percent, and when they are present they are often one
sentence saying the section does not apply. Authors have answered this
themselves: 27 files add a `Terms` section, 32 a `Failure behaviour`
section, 26 a `Coverage` table, none of which the template has. The
sections authors add are the ones readers use; the sections the template
has are the ones authors skip.

The cost is length. Ninety-one files carry more than 300 words outside
their rules and examples, and the median body is 760 words at grade 18.
`SPEC-AEX-003` carries a 3,509-word "Normative contract catalog" that is
the real specification, after 984 words of the template's sections.
`SPEC-RCD-001` ignores the template, writes an `Exact scope` table, six
`Transition rules` and an `Exclusions` paragraph in 124 words, and is the
most readable file in the corpus.

### Coverage is asserted by hand or not at all

The checklist's second line, every specified requirement covered by at
least one rule, is the promise a specification makes to its requirements.
Twenty-six files keep it visibly, in a `Coverage` table mapping each
requirement to the rules that meet it, and all 26 tables are complete.
Eighty-three files never name a requirement they specify anywhere in the
body. The validator checks that each active requirement has some active
specification; it does not check that any rule of that specification
covers it. The requirement is therefore covered by a relation, not by a
rule, and the reader who wants to know which rule answers `REQ-HUP-032`
reads the whole file.

### Verification does not read the specification

The verification contract is the specification's first reader, and 54 of
132 contracts do not name one. The matrix maps requirements to methods
and pass conditions; the rules that make the pass condition precise are
in another file the matrix does not cite. Where identifiers exist, the
contracts use them: 23 contracts cite 88 identifiers. Where numbers exist,
five contracts cite "rule N" and the rest describe the rule again in their
own words, which is the duplication the requirement and capability passes
found at every other boundary.

### Inconsistency is a cost of its own

Seventy-nine shapes across 135 files. The same content is called
`Behavioral rules` in 95 files and `Rules` in 12; `Error and recovery
behavior` in 67, `Failure behaviour` in 32, `Error and recovery` in 11.
Two files carry `Open decisions` sections that the requirement pass
retired; three carry an `Approval` section that records in prose what the
lifecycle events record authoritatively.

## Standards worth leaning on

- **ISO/IEC/IEEE 29148:2018** gives the characteristics of a well-formed
  requirement that apply to a rule unchanged: necessary, unambiguous,
  singular, verifiable, traceable. "Singular" fails at 243 words;
  "traceable" fails when the address is a number.
- **RFC 2119 and RFC 8174** define the keywords MUST, MUST NOT, SHOULD, MAY
  and how to read them. Every IETF specification opens by citing them and
  then uses them; that is why an RFC rule can be recognised as a rule from
  across the room.
- **INCOSE Guide to Writing Requirements** supplies the sentence rules
  already adopted for requirements: active voice, one thought per
  sentence, name the actor, one term for one concept, no escape clauses.
- **ASD-STE100** sets the sentence budget at 25 words for descriptive text
  and one topic per paragraph; `TECHNICAL_COMMUNICATION.md` already cites
  it.
- **Gherkin** (Given, When, Then) is the everyday form of an example and a
  counterexample, and the form the requirement template adopted for its
  `Examples` section.
- **ISO 24495-1:2023 (plain language)** supplies the test: the intended
  reader can find what they need, understand it, and use it, on first
  reading.

## Proposal

### 1. One rule identity

Every rule leads with a stable identifier, `<PREFIX>-<AREA>-NNN`, in bold,
followed by one sentence. The identifier is the rule's name in the
verification matrix, the work order's scope, the evidence packet and the
deviation's `against` fragment: `SPEC-TCM-005#TCM-RFC-003`. The template's
"Number rules" line is replaced by the checklist's line, so the two managed
documents say one thing. Numbers stay valid in approved files; a rule
cited by number is never renumbered.

### 2. A reader-first template of seven sections

```markdown
+++
id = "SPEC-xxx"
type = "specification"
title = "<What this specification binds, as a noun phrase>"
status = "draft"
owners = ["<technical/domain owner>"]
created = "YYYY-MM-DD"
updated = "YYYY-MM-DD"
contract = "<One sentence: what an implementation must do to conform.>"

[relations]
specifies = ["REQ-xxx"]
+++

# Specification: <title>

## In plain words

<One or two sentences a newcomer understands. Grade 10 or below.>

## Scope

<At most three sentences: what this specification governs and what it
leaves to another. Name the neighbours by id.>

## Terms

- **<term>.** <one sentence; only terms this specification introduces>

## Rules

**<PREFIX>-<AREA>-001.** <One testable sentence of at most 30 words with
one MUST, MUST NOT, SHALL, MAY or refuses.>

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| <the condition> | <what the implementation does, in one sentence> | `<code>` |

## Examples

**Given** <state>, **when** <event>, **then** <the rule that holds, by id>.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-xxx` | `<PREFIX>-<AREA>-001`, `<PREFIX>-<AREA>-004` |

## Not decided here

- <a choice this specification leaves to the implementation, at most five>
```

`contract` is to a specification what `statement` is to a requirement,
`outcome` to an intent and `ability` to a capability: the one line the
Explorer lifts out and the validator can measure. `Behavioral rules`
becomes `Rules`; `Error and recovery behavior` becomes the `Failure
behaviour` table 32 authors already write; `Explicitly unspecified
decisions` becomes `Not decided here`, the name the capability template
uses. `Terms` and `Coverage` are promoted from author practice into the
template. The eight sections present in fewer than half the files,
`Actors and external systems`, `Inputs`, `Outputs`, `State model`, `Data
and interface contracts`, `Security and privacy properties`, `Performance
and capacity`, `Observability`, leave the template and move to the
guidance as optional sections, each with one sentence on when it earns its
place. `Compatibility and migration` stays optional too: 91 files have it
because most specifications here change a managed root, which is this
repository's situation and not every repository's.

### 3. Make the rule shape mechanical, on drafts

New `W-AUT` advisories on specification drafts only, in the same family
and on the same maintenance plane as the requirement, intent and
capability ones:

| Advisory | Fires when |
| --- | --- |
| contract | `contract` is missing, exceeds 30 words, or contains a code span |
| rule identity | a rule in `Rules` does not lead with `<PREFIX>-<AREA>-NNN`, or two rules share an identifier |
| rule shape | a rule exceeds 30 words, spans more than one sentence, or carries no MUST, MUST NOT, SHALL, MAY or refuses |
| coverage | a requirement in `specifies` does not appear in the `Coverage` table, or a `Coverage` row names a rule that does not exist |
| body length | the body outside `Rules`, `Failure behaviour`, `Examples` and `Coverage` exceeds 300 words |
| sentence length | any body sentence outside `Rules` exceeds 25 words |
| legacy shape | a `Behavioral rules`, `Open decisions` or `Approval` heading is present |
| plain words | `In plain words` is missing or exceeds two sentences |

Advisory for one release, then blocking at approval through the existing
`QGP-G1-AUTHORING` predicate, if the owner so decides, in step with the
three earlier decisions. The per-type constants and functions that
`WO-TCM-007` and `WO-TCM-008` introduced take a fourth type; the code
change is one more table row and one more function, not a new mechanism.

### 4. Make coverage mechanical

The `Coverage` table becomes the authoritative statement of which rule
meets which requirement. The validator reads it: every `specifies` target
appears in it, every rule it names exists in `Rules`. The Explorer's record
panel shows the table on the specification and, on each requirement, the
rules that cover it, read from the same table. The relation `specifies`
stays; the table makes it precise.

### 5. Give the deviation its anchor

The `against` fragment must be a rule identifier present in the named
specification's `Rules` section, checked by a new `E-DCM` error on
deviations, and the Explorer renders each rule with an anchor of that
identifier so the link resolves. `SPEC-DCM-001` rule 3's example changes
from `SPEC-DST-014#rule-7` to an identifier.

### 6. Give the Explorer the one line and the rules

The dashboard generator projects `contract` and `plain_words` on
specifications as it does `statement` on requirements and `ability` on
capabilities. The record panel renders the contract first, the plain words
beneath it, then the rules as a list by identifier with anchors, then the
coverage table, before the rest of the body.

### 7. Forward-only migration

`TECHNICAL_COMMUNICATION.md` forbids a style-only rewrite of approved
artifacts, and 129 of 135 specifications are approved or implemented. New
specifications use the new shape. An approved specification adopts it only
when amended for another reason, and then adopts identifiers for its rules
while keeping the numbers in a `formerly rule N` note, so the 29 work
orders and 33 packets that cite numbers stay true. The Explorer renders the
contract where present and the title where not.

## What this changes, and where

The template, the authoring guide, the validator advisories and the
deviation error, the dashboard generator and the Explorer template are
managed files. The change lands in the candidate templates under a work
order in the technical-communication domain, ships with the next release
and reaches this repository at its next root adoption, like `WO-TCM-005`
and `WO-TCM-008`. The `contract` field is additive front matter; no
existing specification needs to change. The deviation anchor touches
`SPEC-DCM-001` and its validator rules, which are a decision-management
work order's to amend. Since the 0.15.0 root, the owner's four decisions
below can be raised as one `DEC-` artifact concerning this note's
requirement, and this is the first pass where that is possible; the
recommendation is to do so, so that the disposition lives in the graph and
not in a note. This note needs no work order.

## Decisions that belong to the owner

1. **Rule identity.** A stable identifier on every rule, mandatory on new
   drafts and the only form the deviation anchor accepts, as proposed; or
   numbers kept as an accepted form with the advisory silent on them.
2. **The template.** Seven sections with the eight rarely-used ones
   optional in the guidance, plus the `contract` field, as proposed; or the
   fourteen sections kept with the identifier and coverage changes only.
3. **Coverage.** The `Coverage` table mechanical, checked by the validator
   and rendered on both sides by the Explorer, as proposed; or coverage
   left to the `specifies` relation alone.
4. **Budgets.** Advisory only; or advisory for one release and then
   blocking at approval, in step with the requirement, intent and
   capability decisions.

The recommendation is identifiers, seven sections with the field, a
mechanical table, and advisory then blocking.

## What this note does not do

It does not change a template, a rule, a specification or a gate. It does
not measure architectures, verification contracts or work orders, which
are the next passes. It does not claim that shorter is always better:
`SPEC-AEX-003`'s 3,509-word catalog is the contract for the whole agentic
execution domain, and the proposal moves it under `Rules` with identifiers
rather than asking it to be shorter. It does not rewrite any of the 71
numbered specifications; the numbers stay valid where they are cited.
