# Assessment of capability readability, 2026-09-04

<!-- Target expertise: 4/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> Point-in-time. Measured on `main` at `fef29a4`. This note is an operator
> analysis. It has no authority. The managed contract, the formal artifacts
> and the accountable decisions stay authoritative. This note changes no
> rule. It proposes. It is the third pass after the
> [requirement](assessment-requirement-readability-2026-09-04.md)
> assessment and the intent assessment of the same day (pull request
> #338), and it uses their method and their vocabulary.

## Summary

A capability says what an actor can do, under which conditions, and what it
does not decide. It sits between the intent, which states an outcome, and
the requirements, which state obligations. Today the reader finds that
ability inside a body of about 160 words at college reading level, in one
of seven template shapes, with a statement the template asks for present in
29 of 36 files and written in the template's form in six. The one section a
reader would use to navigate, the list of requirements, is stale in 22 of
30 files because the graph, not the list, records what derives from what.

The result in two sentences. The capability layer is leaner than the
requirement layer and its statement form is the right one; the layer earns
its place by naming the actor, which no other artifact does. Its bodies
restate the intent's outcomes above and the requirements' behaviors below,
nothing mechanical checks any of it, and the requirement list duplicates
the graph.

This note measures the 36 capabilities, names the causes, and proposes an
`ability` field, a body of three short sections, draft-time advisories, the
retirement of the requirement list in favour of the graph, and a
forward-only migration. It ends with the four decisions that belong to the
owner.

## Terms

Terms used below, in plain words. The [glossary](../../GLOSSARY.md) has
the rest.

- **Ability.** The one sentence a capability exists for: who can do what,
  under which conditions. The template writes it as `<Actor> can <perform
  or achieve something> under <important conditions>`.
- **Body.** Everything below the front matter.
- **Advisory.** A validator message that informs but does not fail
  validation. The `W-AUT` family fires only on drafts.
- **Reading grade.** The Flesch-Kincaid estimate of the school year a
  reader needs. Grade 8 to 10 is plain language for a technical audience;
  grade 14 is college level.
- **Fan-out.** How many capabilities derive from one intent, and how many
  requirements derive from one capability.

## Method

Every file under `docs/engineering/*/capabilities/` was read by a script.
The body was measured for words, sentence length, passive-voice markers,
code identifiers in backticks, section headings and vocabulary, with code
spans removed. The `Capability statement` section was measured for
presence, form and length. The `Candidate requirements` and `Derived
requirements` sections were compared with the requirements that actually
name the capability in `derives_from`. Three files were read in full: the
shortest (`CAP-RCD-001`), a median one (`CAP-HUP-003`) and the longest
(`CAP-LRE-001`). The template, the checklist in `ARTIFACT_AUTHORING.md`
and the Explorer's record panel were read against the corpus.

## What the corpus looks like

| Measure | Reading |
| --- | --- |
| Capabilities | 36, all `approved`, one intent each |
| Intents behind them | 32; 30 have exactly one capability, the largest has three |
| Requirements per capability | median 5, from 1 to 68 |
| Body length | median 157 words, from 27 to 393 |
| Reading grade | median 15.7, highest 21.2 |
| Sentence length | 31 files carry a sentence over 25 words; 10 carry one over 40 |
| Passive voice | 43 markers; 6 files with three or more |
| Code identifiers | median 4 per body; 20 files over three |
| Statement present | 29 of 36; missing in 3 files with no headings and 4 in an older shape |
| Statement in the template's form (`can` and `under`) | 6 of 36 |
| Statement length | median 27 words, longest 87; 14 over 30 |
| Template shapes in use | 7: the current five sections in 23 files; an older `Description, Users, Boundaries, Derived requirements` in 4; `Capability statement, Observable outcomes, Exclusions` in 3; no headings in 3; two with an `Approval` or `Amendments` section appended; one partial |
| Requirement lists | 30 files list 79 requirement ids; none is stale, 139 deriving requirements are unlisted; 8 lists match the graph |
| Explorer | shows the title, then the body as rendered Markdown; no field is lifted out |

## Findings

### The ability is there, but not in a form a reader can find

The template's form, an actor, `can`, an achievement, `under` conditions,
is the right sentence for a capability: it is the definition of the word in
the capability-based planning literature, one thought long, and readable
by the actor it names. Six files write it that way. Fourteen write a
backticked sentence without conditions, nine write prose, one writes 87
words, and seven have no statement at all. `CAP-RCD-001` is one sentence
of 27 words and nothing else; it is closer to the template's intent than
most, and the validator has no way to know.

The statement is in the body, so nothing mechanical sees it and the
Explorer cannot lift it out. A requirement's `statement` and, since
`WO-TCM-005`, its `In plain words` line are fields; the capability's
ability is a backticked line in a section.

### The body restates its neighbours

`Outcomes` restates the requirements below. `CAP-HUP-003`'s three outcome
bullets are the behaviors of `REQ-HUP-008` and `REQ-HUP-009`, written a
second time in different words. `Boundaries` restates the specification.
`CAP-LRE-001`'s seven boundary bullets name `CAP-REB-001`, `REQ-REB-008`
and `SPEC-REB-003` and read as rules. `Actor and need` restates the
intent's Problem. What is left that only the capability says is the actor,
the ability and what the capability does not decide. That is about forty
words, and the median body is 157.

### The requirement list duplicates the graph, and has drifted

Thirty capabilities end with a list of requirement ids. The graph records
the same fact authoritatively in each requirement's `derives_from`, and the
validator checks it. The lists were written when the packets were drafted
and never updated: 139 requirements that derive from a capability are not
in its list, and only 8 of 30 lists match the graph. No list names a
requirement that does not exist, which is the one error the validator
would catch. This is the `Open decisions` situation again: a section that
can only repeat or contradict the graph. The checklist asks for it: "lists
its derived requirements".

### The checklist and the template describe two different artifacts

The checklist has three lines: what an actor can do, derives from an
intent and lists requirements, boundaries state what is not decided. The
template has five sections, two of which, `Actor and need` and `Outcomes`,
the checklist never mentions, and one of which, the requirement list, the
checklist demands and the graph makes redundant. No line of either is
mechanical. Like every definition type except the requirement, the
capability has no `W-AUT` advisory at all.

### The layer is almost always one-to-one

Thirty of 32 intents have exactly one capability, and every capability has
exactly one intent. When the ratio is one, the capability tends to become a
second draft of the intent: five titles share half their words with the
intent's title, and the `Actor and need` section carries the intent's
Problem again. The layer earns its place by naming the actor, which the
intent does not do and the requirement does only through `THE SYSTEM`.
Whether it should be mandatory when an intent has one ability is a
question for the owner, not for this note; the proposal below makes the
layer cheap enough that the question loses most of its cost.

### Inconsistency is a cost of its own

Seven shapes across 36 files. A reader cannot learn one shape and reuse it.
Two files carry an `Approval` section that records in prose what the
lifecycle events record authoritatively.

## Standards worth leaning on

- **Capability-based planning** defines a capability as the ability to
  achieve an effect under specified conditions. The template's sentence
  form is that definition. The gap is use, not choice.
- **ISO/IEC/IEEE 29148:2018** separates stakeholder needs from system
  requirements. A capability is a need statement: who, what they must be
  able to do, under which conditions. The same characteristics apply,
  necessary, unambiguous, singular, verifiable, and "singular" is the one
  an 87-word statement fails.
- **Job stories and user stories** (Cohn; Klement) are the everyday form of
  the same sentence: an actor, a situation, an ability, an outcome. They are
  one sentence long by rule.
- **INCOSE Guide to Writing Requirements** supplies the sentence rules
  already adopted for requirements: active voice, one thought per
  sentence, name the actor, one term for one concept.
- **ASD-STE100** sets the sentence budget at 25 words for descriptive text
  and one topic per paragraph; `TECHNICAL_COMMUNICATION.md` already cites
  it.
- **ISO 24495-1:2023 (plain language)** supplies the test: the intended
  reader can find what they need, understand it, and use it, on first
  reading.

## Proposal

### 1. A reader-first template of about twenty lines

```markdown
+++
id = "CAP-xxx"
type = "capability"
title = "<Actor ability>"
status = "draft"
owners = ["<product owner>"]
created = "YYYY-MM-DD"
updated = "YYYY-MM-DD"
ability = "<Actor> can <perform or achieve something> under <important conditions>."

[relations]
derives_from = ["INT-xxx"]
+++

# Capability: <title>

## In plain words

<One or two sentences a newcomer understands. Grade 10 or below.>

## Actor and need

<At most three sentences. Who the actor is, and what they need, in
their words. The outcome the need serves is the intent's; do not
restate it.>

## Not decided here

- <what this capability leaves to a requirement, a specification or
  another capability; at most five bullets>
```

`Capability statement` becomes the `ability` field, one sentence of at
most 30 words with one `can` and one `under`, which is to a capability
what `statement` is to a requirement and `outcome` is to an intent.
`Outcomes` goes: the outcome is the intent's and the behaviors are the
requirements'. `Candidate requirements` goes: the graph records what
derives from the capability and the Explorer lists it. `Boundaries` stays
as `Not decided here`. `Actor and need` stays, three sentences, and is
where the intent proposal sends `Actors and stakeholders`. The `In plain
words` section is the convention requirements and the proposed intents
follow.

### 2. Make the budget mechanical, on drafts

New `W-AUT` advisories on capability drafts only, in the same family and on
the same maintenance plane as the requirement ones:

| Advisory | Fires when |
| --- | --- |
| ability | `ability` is missing, exceeds 30 words, lacks `can`, lacks `under`, or contains a code span |
| body length | the body exceeds 150 words |
| need length | `Actor and need` exceeds three sentences or 60 words |
| sentence length | any body sentence exceeds 25 words |
| implementation detail | the body cites more than two code identifiers |
| legacy list | a `Candidate requirements` or `Derived requirements` heading is present |
| plain words | `In plain words` is missing or exceeds two sentences |

Advisory for one release, then blocking at approval through the existing
`QGP-G1-AUTHORING` predicate, if the owner so decides, in step with the
requirement and intent decisions. The word budgets generalise from
requirement to definition with one constant per type, as the intent
assessment says; the code change is a type table, not a third
implementation.

### 3. Retire the requirement list in favour of the graph

The `derives_from` relation on each requirement is the authoritative
record, the validator checks it, and the Explorer's record panel can list
the deriving requirements from the bundle's relations with no new data.
The checklist line "lists its derived requirements" goes; a legacy list
draws the advisory above and is otherwise left alone. The record panel
gains the list under a `Derives` heading so the reader loses nothing.

### 4. Reconcile the checklist with the template

The capability checklist is rewritten for the shape above, line by line,
with the mechanical counterpart named after each line. It gains the two
sentences it lacks: when a capability is warranted (an intent needs more
than one actor ability, or a requirement set needs an actor it can be
read against) and what a capability never contains (an outcome, which is
the intent's, and a behavior, which is a requirement's).

### 5. Give the Explorer the one line

The dashboard generator projects `ability` and `plain_words` on
capabilities as it does `statement` and `plain_words` on requirements. The
record panel renders the ability first, the plain words beneath it, then
the deriving requirements, before the body. The lineage board's second
stage shows the ability under the title.

### 6. Forward-only migration

`TECHNICAL_COMMUNICATION.md` forbids a style-only rewrite of approved
artifacts, and all 36 capabilities are approved. New capabilities use the
new shape. An approved capability adopts it only when amended for another
reason. The Explorer renders the ability where present and the title where
not.

## What this changes, and where

The template, the authoring guide, the validator advisories, the dashboard
generator and the Explorer template are managed files. The change lands in
the candidate templates under a work order in the technical-communication
domain, ships with the next release, and reaches this repository at its
next root adoption, like `WO-TCM-005`. The `ability` field is additive
front matter: the validator does not reject an unknown top-level key
today, and no existing capability needs to change. The intent and
capability proposals share the advisory table mechanism and should ship in
one work order or two stacked ones, so the type table is written once.
This note needs no work order.

## Decisions that belong to the owner

1. **Where the ability lives.** A front-matter `ability` field the Explorer
   can render and the validator can measure, as proposed; or a body section
   only, which keeps the front matter unchanged and leaves both reading
   prose.
2. **The requirement list.** Retired in favour of the graph with the
   Explorer listing deriving requirements, as proposed; or kept and made
   mechanical, with a validator error when the list and the graph differ.
3. **Budgets.** Advisory only; or advisory for one release and then
   blocking at approval, in step with the requirement and intent decisions.
4. **The layer.** Keep the capability mandatory between intent and
   requirement, as today; or allow a requirement to derive from an intent
   directly when the intent states one ability. The recommendation is to
   keep it and make it cheap, because the actor has no other home, and to
   revisit after one release of the new shape.

The recommendation is a front-matter field, the graph, advisory then
blocking, and keep the layer.

**Decided.** On 2026-09-04 the repository owner took the four decisions as
recommended, with the words "i follow your recommendation": an `ability`
front-matter field; the requirement list retired in favour of the graph,
with the Explorer listing deriving requirements; advisory for one release,
then blocking at approval; the capability layer kept and made cheap,
revisited after one release of the new shape. The decision is recorded
here because the decision artifact is not yet usable in this repository;
the packet that implements it carries the decision into its work order's
approval reason.

## What this note does not do

It does not change a template, a rule, a capability or a gate. It does not
measure specifications, architectures or work orders, which are the next
passes. It does not claim that shorter is always better: `CAP-RCD-001` at
27 words names an actor and an ability and no condition, and the `under`
rule exists to ask for the condition.
