# Assessment of intent readability, 2026-09-04

<!-- Target expertise: 4/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> Point-in-time. Measured on `main` at `09047aa`. This note is an operator
> analysis. It has no authority. The managed contract, the formal artifacts
> and the accountable decisions stay authoritative. This note changes no
> rule. It proposes.

## Summary

An intent is the first artifact in the chain and the one that should outlive
the rest. It says what outcome an accountable owner wants and how anyone will
know, later, that the outcome was reached. Every work order in the repository
is checked against one condition at its first gate: an approved intent is
reachable. A reader who follows that link should find the outcome in a
minute.

Today the reader finds a document of three hundred words at college level,
in one of three template generations, whose seven sections repeat what the
capability, the specification and the work order say elsewhere. The
authoring checklist asks for four paragraphs; the template asks for seven
sections. The success measures, which are the one part of an intent that
matters years later, are in most files acceptance checks observed "every
CI run". Thirty of the thirty-three intents were written on the same day as
their domain's first work order. Nothing mechanical reads an intent: no
advisory fires on one, and the Explorer shows its title, its status and its
body.

The result in two sentences. The intents are honest and well argued; they
are written as packet preambles, not as durable statements of outcome. The
template invites downstream content, nothing pushes back, and the one line
a reader needs, the outcome, has no home.

This note measures the 33 intents, names the causes, and proposes a
shorter template with an `outcome` field, a success-measure rule that
separates outcome from acceptance, draft-time advisories, a reconciled
checklist, an Explorer line, and a forward-only migration. It ends with the
three decisions that belong to the owner.

## Terms

Terms used below, in plain words. The [glossary](../../GLOSSARY.md) has the rest.

- **Intent.** The `INT-` artifact: why an initiative exists and what outcome
  it wants. Capabilities `derive_from` it; nothing derives from anything
  else into it.
- **Outcome.** A change in the world that someone can observe after
  delivery, written without naming the solution.
- **Success measure.** A row in the intent's table: a measure, its baseline,
  its target and when it is observed.
- **Acceptance check.** A test or gate that proves an implementation meets
  its specification. It belongs to the verification contract, not to the
  intent.
- **Advisory.** A validator message that informs but does not fail
  validation. The `W-AUT` family fires only on drafts and, today, only on
  requirements.
- **Reading grade.** The Flesch-Kincaid estimate of the school year a reader
  needs. Grade 8 to 10 is plain language for a technical audience; grade 14
  is college level.

## Method

Every file under `docs/engineering/*/intent/` was read by a script. The body
was measured for words, sentence length, passive markers, long words,
second-level headings, code spans, path and line-number citations, and
project vocabulary; each `Success measures` table was read row by row. The
reading grade is an estimate over the body prose with code spans, tables
and headings removed. Each intent's `created` date was compared with the
earliest requirement and the earliest work order of its domain. Five files
were read in full: the shortest (`INT-RCD-001`), the median (`INT-VSP-001`),
the longest (`INT-ECP-001`), and two that use no template at all
(`INT-REV-001`, `INT-DST-001`). The template, the authoring guide
(`ARTIFACT_AUTHORING.md`), the communication policy
(`TECHNICAL_COMMUNICATION.md`), the validator, the dashboard generator and
the Explorer record panel were read against the corpus. The method is the
one used for the [requirement assessment](assessment-requirement-readability-2026-09-04.md)
so the two can be read side by side.

## What the corpus looks like

| Measure | Value |
| --- | --- |
| Intents | 33; all `approved`; none in `draft` |
| Body length | median 312 words; mean 381; longest 1,293 words (`INT-ECP-001`); shortest 54 words (`INT-RCD-001`) |
| Sentences | mean 15.9 words; 12 percent over 25 words; 15 percent with a passive marker |
| Long words | 22 percent of words have nine letters or more |
| Reading grade | about 16 |
| Template shapes in use | 18 with the current seven sections; 4 with an earlier five (Problem, Outcome, Scope boundary, Accountable product owner, Success measure); 2 with no headings; 9 in seven other ad hoc sequences |
| Section sizes | Problem median 81 words, longest 473; Risks and assumptions 80; Desired outcomes 73; Principles 67; Success measures 56; Actors 51; Non-goals 49 |
| Success measures | 12 intents have no table; 101 rows in the other 21; 47 targets are `0`; 10 baselines read `not measured`, `unspecified` or `not defined`; the most frequent observation windows are `every CI run`, `every publication`, `packet verification`, `implementation review` |
| Implementation detail | 355 code spans; 21 intents cite more than three; 7 cite file paths; `INT-ECP-001` cites 16 source line ranges |
| Timing | 30 of 33 intents share their `created` date with the domain's first requirement and first work order |
| Graph | no intent declares a relation; 37 capabilities derive from 33 intents; `INT-HUP-004` has no capability deriving from it |
| Front matter | the six common fields and nothing else; no field holds the outcome |
| Vocabulary | `release` 136, `repository` 105, `candidate` 67, `decision` 66, `evidence` 63, `owners` 59, `harness` 54, `managed` 50, `evaluator` 47, `authority` 44, `exact` 44, `accountable` 43 occurrences |
| Validator | no authoring rule reads an intent beyond the placeholder and `Open decisions` checks at approval; every `W-AUT` advisory is restricted to requirements |
| Explorer | renders title, status, owners, lifecycle events and the body; nothing intent-specific; the G0 condition `intent_quality` is fixed at `not_assessable` |

## Findings

### The template and the checklist describe two different artifacts

The authoring guide's intent checklist has three lines: problem, outcome,
scope boundary and accountable product owner are each one paragraph; the
success measure is observable after delivery; no solution language. That is
a four-paragraph artifact with one measure. The template has seven
sections: Problem, Desired outcomes, Actors and stakeholders, Success
measures, Non-goals, Principles and immutable constraints, Risks and
assumptions. Four intents follow the checklist; eighteen follow the
template; nobody can follow both. The guide says "each one paragraph" and
nothing in the corpus is checked against that.

### Three of the seven sections belong downstream

The template asks the author of a *why* document to also write who the
actors are, which principles bind later decisions, and which risks and
assumptions apply. Each has a home elsewhere in the chain:

- *Actors and stakeholders* is the capability's `Actor and need` section.
  `INT-TCM-001` lists five actor groups; `CAP-TCM-001`, approved the same
  minute, lists the same actors in its own words.
- *Principles and immutable constraints* is the material of a specification
  rule or an ADR's decision. `INT-VSP-001` writes "supersession must be
  explicit, typed, acyclic, coverage-preserving, release-safe, deterministic,
  and visible", which is a specification in one sentence.
- *Risks and assumptions* asks the author to "separate facts, assumptions,
  and open decisions". Since `WO-DCM-001` an open decision is a `DEC-`
  artifact, and `REQ-TCM-008` retired the inline section from every other
  definition; the intent template still invites the same inline prose under
  a different heading. Risks have their own artifact and command
  (`raise-risk`).
- *Non-goals* is useful and short (median 49 words). It stays.

The three sections that go carry a median of about 200 words per intent,
two thirds of the median body. They are also where the college-level
register lives: a principle is written as a rule, a risk as a clause.

### The success measures are acceptance checks

The checklist asks for a measure "observable after delivery"; the guidance
asks that "a reader can tell, years later, whether the outcome was
reached". The tables say otherwise. Forty-seven targets are `0`, which is
the shape of a defect count, not an outcome. The observation windows are
`every CI run`, `every validator run`, `packet verification`,
`implementation review`, `this transaction`. `INT-OCA-001` measures "draft
release proposals changed: baseline 0, target 0, this transaction", which
is a stop condition of a work order. `INT-EVK-001` measures "harness
surfaces recognizing `evidence/WO-ID/file`: 0 of 4, 4 of 4, focused
acceptance run", which is a verification-contract row.

An acceptance check is observed once, at the moment the work order closes,
and is then true forever. A success measure should be observable by an
operator in a later year without reading the code: how often a thing
happens, how long a thing takes, how many repositories, how many
refusals. Twelve intents have no table at all, and ten rows admit that no
baseline exists. The one measure a future reader needs is the one the
corpus is least sure of.

### The Problem section has become an investigation report

`INT-ECP-001` opens with a 473-word Problem that cites sixteen source line
ranges, two audits by item number, and nine diagnostic or module names.
`INT-HBI-001` opens with a root-cause identifier, a release identifier and
an ADR. That material is right and traceable, and it is the material of a
review note, an RCA or an ADR context section, all of which exist and are
cited. An intent should state the problem in a sentence a product owner
would say. Twenty-one intents cite more than three code identifiers; seven
cite file paths. The checklist's "no solution language" has no mechanical
counterpart and is not met.

### The register is academic

Sentences are shorter than in the requirements, 15.9 words against 18.9,
because bullets are short. Words are longer: 22 percent have nine letters
or more, against 17 percent in requirements, and the estimated reading
grade is about 16. `accountable`, `authoritative`, `deterministic`,
`provenance`, `supersession` and `repository-owned` are ordinary words
here. The intent is the artifact a newcomer, a stakeholder or an auditor
meets first, and it is the hardest to read.

### The intent is written with the work order, not before it

Thirty of thirty-three intents share their `created` date with their
domain's first requirement and first work order. Thirty-seven capabilities
derive from thirty-three intents, close to one each. The chain
intent → capability → requirement → work order is produced in one sitting,
as one packet, and the intent is its preamble. That is not wrong for a
repository that governs its own tool, where each initiative is small. It
does mean the artifact is sized and worded as the first page of a packet,
and it explains why the same content appears in three artifacts: the
author wrote them together and had nothing to point to.

The guide does not say when a new intent is warranted and when a new
capability under an existing intent is enough. Forty-eight domains, thirty-
three intents, one initiative each.

### Nothing reads an intent

The validator applies no rule to an intent beyond the placeholder check and
the `Open decisions` check at approval. Every `W-AUT` advisory is guarded
by `artifact_type == "requirement"`. The dashboard generator projects a
`statement` and `plain_words` for requirements and nothing type-specific
for intents. The Explorer's G0 gate carries a condition named
`intent_quality`, "outcome quality and stakeholder agreement", fixed at
`not_assessable` in code. The record panel shows the title, the status,
the owners and the body. A reader who opens an intent in the Explorer
reads three hundred words or nothing.

### Inconsistency is a cost of its own

Three generations and nine ad hoc sequences in thirty-three files. Two
intents (`INT-REV-001`, `INT-RCD-001`) have no headings at all; one has no
title in its H1. The headings `Outcome`, `Desired outcome`, `Desired
outcomes`, `Success measure`, `Success measures` and `Success indicators`
all occur. A script cannot find the outcome in an intent, and neither can
a reader who learned the shape from the previous one.

## Standards worth leaning on

- **ISO/IEC/IEEE 29148:2018** places the intent at the business and
  stakeholder level: business purpose, scope, stakeholder needs, measures
  of effectiveness. Its rule that needs are stated without reference to a
  solution is the checklist's "no solution language". Its measures of
  effectiveness are observed in operation, which is the distinction the
  success-measure tables miss.
- **Impact Mapping** (Adzic, 2012) gives the four questions in order: why
  (the goal, with a measure), who (the actors whose behaviour changes),
  how (the behaviour change), what (the deliverable). An intent is the
  first two. The third belongs to the capability and the fourth to the
  work order, which is where the template's Actors and Principles sections
  drift.
- **Goal-Question-Metric** (Basili, 1994) gives the test for a success
  measure: it answers a question about the goal, and the question is one
  an operator would ask after delivery. "How many CI runs failed" is a
  question about the implementation, not about the goal.
- **INCOSE Guide to Writing Requirements** supplies the rule "avoid
  stating implementation" and the vocabulary rules already applied to
  requirements: active voice, one thought per sentence, one term per
  concept.
- **ASD-STE100** is already the basis of `TECHNICAL_COMMUNICATION.md`:
  20 words per procedural sentence, 25 per descriptive, one topic per
  paragraph, six sentences per paragraph.
- **ISO 24495-1:2023 (plain language)** supplies the test that matters
  most for the first artifact in the chain: the intended reader can find
  what they need, understand it, and use it, on first reading.

## Proposal

### 1. A reader-first template of about twenty-five lines

```markdown
+++
id = "INT-xxx"
type = "intent"
title = "<Outcome-oriented title>"
status = "draft"
owners = ["<accountable product or domain role>"]
created = "YYYY-MM-DD"
updated = "YYYY-MM-DD"
outcome = "<WHO> can <observable result> — one sentence, no solution named."

[relations]
+++

# Intent: <title>

## In plain words

<One or two sentences a newcomer understands. Grade 10 or below.>

## Problem

<At most five sentences. What happens today, to whom, and why it is
worth changing. No file, identifier or command. The evidence belongs
in a note, an RCA or an ADR, cited by link.>

## Success measures

| Measure | Today | When reached | Observed |
| --- | --- | --- | --- |
| <what an operator can count or time after delivery> | <baseline or "not measured"> | <target> | <where and how often, in operation> |

## Not this

- <what this initiative deliberately leaves alone; at most five bullets>
```

`Desired outcomes` becomes the `outcome` field, one sentence, which is to an
intent what `statement` is to a requirement. `Actors and stakeholders` goes
to the capability, which already has `Actor and need`. `Principles and
immutable constraints` goes to the specification or ADR that will bind
them. `Risks and assumptions` goes: facts belong in the Problem, risks in a
risk artifact, open decisions in a `DEC-`. `Non-goals` stays as `Not this`.
The `In plain words` section is the convention the notes and, since
`WO-TCM-005`, the requirements already follow.

### 2. One rule for a success measure

A success measure is observed in operation, after delivery, by someone
who has not read the code. Its `Observed` cell names a place and a cadence
an operator would recognise: a dashboard field, a release review, a
quarterly count. A row whose `Observed` cell names a CI run, a test, a
validator run, a verification or an implementation review is an acceptance
check and belongs in the verification contract; the template comment says
so, and an advisory says so on the draft.

A `Today` cell may read `not measured`. That is honest and it is a fact the
reader needs. A target of `0` is allowed when the measure is a count of
incidents in operation, and is suspect when the row would be true the
moment the work order closes.

### 3. Make the budget mechanical, on drafts

New `W-AUT` advisories on intent drafts only, in the same family and on
the same maintenance plane as the requirement ones:

| Advisory | Fires when |
| --- | --- |
| outcome | `outcome` is missing, exceeds 30 words, or contains a code span |
| body length | the body exceeds 200 words |
| problem length | `Problem` exceeds 120 words or five sentences |
| sentence length | any body sentence exceeds 25 words |
| implementation detail | the body cites more than two code identifiers, or any file path or line range |
| acceptance in disguise | a success-measure `Observed` cell names a CI run, test, validator, verification or implementation review |
| no measure | the `Success measures` table has no row |
| plain words | `In plain words` is missing or exceeds two sentences |

Advisory for one release, then blocking at approval through the existing
`QGP-G1-AUTHORING` predicate, if the owner so decides, exactly as proposed
for requirements. The word budgets in the guide (`W-AUT-005` to
`W-AUT-009`) generalise from requirement to definition with one constant
per type; the code change is a type table, not a second implementation.

### 4. Reconcile the checklist with the template

The intent checklist is rewritten for the shape above, line by line, with
the mechanical counterpart named after each line as the requirement
checklist now does. It gains two sentences the guide lacks: when a new
intent is warranted (a new outcome an owner would be asked about in a
year) and when a capability under an existing intent is enough (a new
thing an actor can do toward an outcome already stated). The guidance
paragraph keeps its one good sentence: write it so that a reader can
tell, years later, whether the outcome was reached.

### 5. Give the Explorer the one line

The dashboard generator projects `outcome` and `plain_words` on intents as
it does `statement` and `plain_words` on requirements. The record panel
renders the outcome first, the plain words beneath it, before the lifecycle
events. The lineage board's first stage shows the outcome under the title.
The G0 condition `intent_quality` stops being a constant: it reads
`satisfied` when the reachable intent carries an `outcome` and at least
one success-measure row, `not_assessable` otherwise. It stays a derived
observation, not a gate result, as the operational-phasing note requires.

### 6. Forward-only migration

`TECHNICAL_COMMUNICATION.md` forbids a style-only rewrite of approved
artifacts, and all thirty-three intents are approved. New intents use the
new shape. An approved intent adopts it only when amended for another
reason. The Explorer renders the outcome where present and the title where
not, so the everyday reader gains most of the benefit as the corpus turns
over.

## What this changes, and where

The template, the authoring guide, the validator advisories, the dashboard
generator and the Explorer template are managed files. The change lands in
the candidate templates under a work order in the technical-communication
domain, ships with the next release, and reaches this repository at its
next root adoption, like `WO-TCM-005`. The `outcome` field is additive
front matter: the validator does not reject an unknown top-level key
today, and no existing intent needs to change. This note needs no work order.

## Decisions that belong to the owner

1. **Where the outcome lives.** A front-matter `outcome` field the
   Explorer can render, as proposed; or a body section only, which keeps
   the front matter unchanged and leaves the Explorer reading prose.
2. **Success measures.** Observed in operation only, with acceptance checks
   refused by advisory, as proposed; or both kinds allowed in one table
   with a column naming which is which.
3. **Budgets.** Advisory only; or advisory for one release and then
   blocking at approval, in step with the requirement decision.

The recommendation is a front-matter field, operation-only measures, and
advisory then blocking.

## What this note does not do

It does not change a template, a rule, an intent or a gate. It does not
measure capabilities, which sit between the intent and the requirement and
duplicate part of both; that is the next pass. It does not claim that a
short intent is a good one: `INT-RCD-001` at 54 words states a problem and
no outcome, and the `outcome` field and the measures table exist to
prevent that.
