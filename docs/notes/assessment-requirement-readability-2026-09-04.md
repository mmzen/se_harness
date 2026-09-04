# Assessment of requirement readability, 2026-09-04

<!-- Target expertise: 4/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> Point-in-time. Measured on `main` at `bceb7b5`. This note is an operator
> analysis. It has no authority. The managed contract, the formal artifacts
> and the accountable decisions stay authoritative. This note changes no
> rule. It proposes.

## Summary

A requirement in this repository is one obligation the harness must meet.
The reader should find that obligation, understand it, and know how to check
it, on first reading. Today the reader has to find it inside a document of
four hundred words written at college level, in a vocabulary the glossary
does not cover, in one of two template shapes that coexist. The obligation
itself, the `statement` field, is the only part of the artifact that the
Explorer shows, and one statement in four is longer than the authoring rule
allows.

The result in two sentences. The statements follow a sound grammar (EARS) and
the checklist around them is right. The prose around the statements is too
long, too dense and too varied for the reader it exists for, and nothing
mechanical pushes back.

This note measures the 328 requirements, names the causes, and proposes a
shorter template, a plain-language summary line, a named actor, draft-time
advisories for length, a repository-owned glossary, and a forward-only
migration. It ends with the three decisions that belong to the owner.

## Terms

Terms used below, in plain words. The [glossary](glossary.md) has the rest.

- **Statement.** The `statement` field in a requirement's front matter: the
  one sentence that says what the harness shall do.
- **EARS.** Easy Approach to Requirements Syntax. Five sentence shapes for a
  requirement, each opening with a keyword: `THE SYSTEM SHALL`, `WHEN`,
  `WHILE`, `IF … THEN`, `WHERE`. The template already uses it.
- **Body.** Everything below the front matter: rationale, behavior, examples.
- **Advisory.** A validator message that informs but does not fail
  validation. The authoring advisories are the `W-AUT` family and they fire
  only on drafts.
- **Reading grade.** The Flesch-Kincaid estimate of the school year a reader
  needs. Grade 8 to 10 is plain language for a technical audience; grade 14
  is college level.

## Method

Every file under `docs/engineering/*/requirements/` was read by a script.
Front matter was measured for the statement; the body was measured for
sentence length, passive voice markers, long words, section headings and
project vocabulary. The reading grade is an estimate over the body prose
with code spans removed. Three files were read in full: the shortest
(`REQ-REV-002`), a median one (`REQ-ADS-004`) and the longest
(`REQ-DST-065`). The template, the authoring guide (`ARTIFACT_AUTHORING.md`),
the communication policy (`TECHNICAL_COMMUNICATION.md`) and the glossary
were read against the corpus.

## What the corpus looks like

| Measure | Value |
| --- | --- |
| Requirements | 328; 321 approved or later |
| Body length | median 409 words; longest 1,588 words (`REQ-DST-065`); shortest 16 words (`REQ-REV-002`) |
| Statement length | median 37 words; 81 exceed the 300-character rule; 67 carry more than one `SHALL` |
| Statement shape | 312 open with `WHEN`; 8 with `THE SYSTEM SHALL`; 3 `IF`; 2 `WHILE`; 1 `WHERE`; 2 none |
| Sentences | mean 18.9 words; 20 percent over 25 words; 18 percent with a passive marker |
| Long words | 17 percent of words have nine letters or more |
| Reading grade | about 14 |
| Template shapes in use | 224 with the older seven sections; 42 with the current `Behavior` shape; 44 with no acceptance section; a tail of ad hoc headings |
| Vocabulary | `candidate` 476, `artifact` 467, `evaluator` 312, `digest` 274, `canonical` 235, `lifecycle` 204, `schema` 171, `accountable` 144, `deterministic` 120 occurrences |
| Glossary | 21 terms; `digest`, `canonical`, `deterministic`, `schema` and `accountable` are not among them; no requirement links to it |
| Explorer | shows the `statement`; shows nothing from the body |

## Findings

### The template asks for the wrong amount of text

The current template has five sections and two Given/When/Then examples. The
older template, which two thirds of the corpus still carries, has seven
sections: Rationale, Preconditions and trigger, Required response, Failure
and boundary behavior, Constraints, Acceptance examples, Open decisions.
Authors fill every section. A one-obligation requirement becomes a document
of four hundred words, and the reader has to find the obligation inside it.

The median requirement, `REQ-ADS-004`, is a fair example. It is well written
sentence by sentence. It is still 270 words to say: when a pull-request body
carries a carriage return in the trailer, or a ready record points at a
commit no longer reachable, the validator warns and names the fix.

### Rationale sections have become investigation reports

`REQ-DST-065` has a seven-paragraph rationale. It cites a tuple name, a
module name, two diagnostic codes and the count of placeholders in a released
version. That is the material of an investigation note or an ADR. The
authoring guide already says: "Rationale says why the obligation exists, not
what it does", and "if a requirement needs a diagram or a table to be
understood, the detail belongs in a specification". Nothing enforces either
sentence.

### The statement is overloaded and under-checked

One statement in four is longer than 300 characters. One in five carries
more than one `SHALL`, which the checklist forbids ("split on *and SHALL*").
The three advisories that exist (`W-AUT-001` to `W-AUT-003`) fire only on
drafts, and most of the corpus was approved before they existed, so the
rules were never applied to it.

`WHEN` opens 312 of 328 statements. Many of them are invariants in disguise:
"WHEN the graph is validated, THE SYSTEM SHALL …" says nothing about an event
and everything about an always-true rule. The `THE SYSTEM SHALL` shape, made
for invariants, opens eight statements. A reader who learns the grammar is
misled by it.

### The register is academic

Mean sentence length is close to the ASD-STE100 ceiling of 20 words for
procedural text and one sentence in five is over 25. Passive markers appear
in one sentence in five, where the policy asks for active voice when it
identifies responsibility. Nine-letter words make up a sixth of the text.
The estimated reading grade is 14. The notes in this directory carry a
target-expertise score and aim at grade 8 to 10; the requirements aim at
nothing.

### The vocabulary has no way in

The nine most frequent project terms appear over 2,000 times. The glossary
defines four of them. No requirement links to the glossary. A reader who
does not already know what a candidate, a digest or a canonical byte
sequence is has to infer it from use.

### The one field a reader sees is the statement

The Explorer renders the statement and nothing from the body. So the body's
length is paid by the author, the reviewer and the approving owner, and buys
the everyday reader nothing. The body's job is to justify and exemplify the
statement for the reviewer at approval time. It should be sized for that
job.

### Inconsistency is a cost of its own

Beyond the two template generations, the corpus carries ad hoc headings:
Statement, Problem, Lifecycle, Resolved decisions, Required outcome,
Acceptance criteria. A reader cannot learn one shape and reuse it across
the 328 files.

## Standards worth leaning on

- **EARS** (Mavin et al., 2009) is already the statement grammar and is the
  right one. The template's five shapes are exactly its five. The gap is
  use, not choice.
- **ISO/IEC/IEEE 29148:2018** gives the characteristics to test each
  requirement against: necessary, appropriate, unambiguous, complete,
  singular, feasible, verifiable, correct, conforming. Its list of terms to
  avoid (vague quantities, escape clauses, "and/or", open-ended lists) is
  already in the authoring guide. "Singular" is the one the corpus fails.
- **INCOSE Guide to Writing Requirements** adds the sentence-level rules:
  active voice, one thought per sentence, name the actor, one term for one
  concept, no pronouns without a clear referent, definite articles.
- **ASD-STE100** is already cited by `TECHNICAL_COMMUNICATION.md`. It sets
  the sentence budget at 20 words for procedures and 25 for descriptions,
  one topic per paragraph, and at most six sentences per paragraph.
- **ISO 24495-1:2023 (plain language)** supplies the test that matters most
  here: the intended reader can find what they need, understand it, and use
  it, on first reading.

## Proposal

### 1. A reader-first template of about thirty lines

```markdown
+++
id = "REQ-xxx"
type = "requirement"
title = "<Observable obligation>"
statement = "WHEN <event>, THE <COMPONENT> SHALL <observable response>."
verification_method = ["test"]
priority = "must"
source = "<stakeholder, standard clause, incident, or artifact ID>"
[relations]
derives_from = ["CAP-xxx"]
+++

# Requirement: <title>

## In plain words

<One or two sentences a newcomer understands. Grade 10 or below.>

## Why

<At most five sentences. Why the obligation exists, not what it does.
Detail belongs in the specification that specifies this requirement.>

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| <observable condition> | <what the reader can check> | <what happens instead> |

## Examples

### Normal
**Given** … **When** … **Then** …

### Failure
**Given** … **When** … **Then** …

## Open decisions

None.
```

Constraints, Preconditions and trigger, Required response, Failure and
boundary behavior, and Assumptions and dependencies go. Their content
either fits the Behavior table in one line each or belongs in the
specification. The `In plain words` section is the same "Summary first"
convention the notes already follow, applied to the one artifact a
newcomer meets most often.

### 2. Name the actor

EARS allows a system name in place of `THE SYSTEM`. "THE VALIDATOR SHALL
refuse …" reads better and is more precise than "THE SYSTEM SHALL refuse
…". The validator already accepts this: `W-AUT-001` matches
`THE <Name> SHALL` as an opener. The template comment and the authoring
guide do not say so, and eight statements in 328 use anything but `WHEN`.
The guide should ask for the concrete component when one exists (the
installer, the validator, `check`, the mutation guard) and keep
`THE SYSTEM` for obligations that span components.

### 3. Make the budget mechanical, on drafts

New `W-AUT` advisories, on drafts only:

| Advisory | Fires when |
| --- | --- |
| statement length | the statement exceeds 30 words |
| body length | the body exceeds 250 words |
| rationale length | `## Why` exceeds 120 words or five sentences |
| sentence length | any body sentence exceeds 25 words |
| implementation detail | the body cites more than three code identifiers in backticks |
| disguised invariant | the statement opens `WHEN` and its event is a verb of evaluation (`is validated`, `is evaluated`, `runs`) with no other condition |

Advisory for one release, then blocking at approval through the existing
`QGP-G1-AUTHORING` predicate, if the owner so decides. The `W-AUT-003`
threshold of 300 characters should follow the statement rule down to 30
words, which is about 200 characters.

### 4. Grow this repository's glossary, and point the template at a glossary the repository owns

Two vocabularies meet in a requirement, and the fix differs for each.

- **Harness terms** are the same in every repository that uses the harness:
  work order, verification record, decision right, checkpoint, gate. They
  are defined once, in the managed instructions and policy documents that
  the distribution ships. They need no glossary.
- **Project terms** belong to one repository. `candidate`, `digest`,
  `evaluator`, `canonical` and `deterministic` are se_harness's words; a
  repository that builds a payment service has other words. A glossary is
  the repository's own note, written from that repository's artifacts and
  context. The distribution ships no glossary and no glossary content. The
  se_harness vocabulary must never travel in the templates.

For this repository: add the frequent terms `glossary.md` lacks,
`candidate` and `digest` first, then `canonical`, `deterministic`,
`schema`, `accountable`, `snapshot` (it is there as formal snapshot),
`provenance`, `predicate`. The frequency list in the vocabulary table above
is the seed; the script that produced it can produce the same list for any
repository, so a glossary is generated from the corpus, never copied from
here.

For the template: the `In plain words` guidance points at a glossary the
repository owns, at a path the repository chooses (`docs/notes/glossary.md`
here), and says so. It does not name se_harness's glossary and it does not
assume one exists. A repository without a glossary reads the guidance as an
instruction to write one from its own terms. A term used in a requirement
should then be findable in one hop.

### 5. Forward-only migration

`TECHNICAL_COMMUNICATION.md` forbids a repository-wide or style-only rewrite
of approved artifacts, and rewriting 321 approved files would also bury
their history under one commit. New drafts use the new shape. An approved
requirement changes only when it is amended for another reason, and then it
adopts the new shape in the same amendment. The Explorer can render the
statement and, where present, the `In plain words` line prominently, which
gives the everyday reader most of the benefit without touching history.

## What this changes, and where

The template, the authoring guide and the validator advisories are managed
files. The change lands in the candidate templates under a work order,
ships with the next release, and reaches this repository at its next root
adoption, exactly like the decision artifact (`WO-DCM-001`). Until then only
the candidate benefits. This repository's glossary and this note are notes
and need no work order. The glossary is repository-owned content: the
distribution never carries it, and no work order may move its entries into
a template.

## Decisions that belong to the owner

1. **Migration.** Forward-only, as proposed; or a one-time `In plain words`
   line added to every approved requirement, which is a style edit the
   communication policy currently forbids and would need that policy
   amended first.
2. **Budgets.** Advisory only; or advisory for one release and then
   blocking at approval.
3. **Actor.** Permit a named component beside `THE SYSTEM`, as proposed; or
   replace `THE SYSTEM` outright.

The recommendation is forward-only, advisory then blocking, and permit
rather than replace.

## What this note does not do

It does not change a template, a rule, a requirement or a gate. It does not
measure specifications, architectures or work orders, which have the same
symptoms and deserve the same pass once the requirement shape is settled.
It does not claim that shorter is always better: `REQ-REV-002` at 16 words
of body says too little, not too much, and the template's `Why` and
`Examples` sections exist to prevent that.
