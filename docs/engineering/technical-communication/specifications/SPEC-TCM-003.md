+++
id = "SPEC-TCM-003"
type = "specification"
title = "Reader-first requirements, graph-read decisions and the repository-owned glossary"
status = "approved"
owners = ["technical-owner", "quality-owner"]
created = "2026-09-04"
updated = "2026-09-04"

[relations]
specifies = ["REQ-TCM-006", "REQ-TCM-007", "REQ-TCM-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-04T16:14:37Z"
decided_by = "technical-owner"
reason = "Approved by the accountable repository owner on 2026-09-04 with the instruction 'i approve the packet, the work orders can be start with execution delegation', after reviewing PR #335 (REQ-TCM-006..008, SPEC-TCM-003, VER-TCM-003, WO-TCM-005, WO-TCM-006)."
+++

# Specification: Reader-first requirements, graph-read decisions and the repository-owned glossary

## Scope

The managed requirement template and its authoring guide section; the
draft-time authoring advisories of the candidate validator; the Explorer's
rendering of a requirement; the retirement of the `Open decisions` section
from every definition template and from the authoring gate; a glossary seed
installed once per repository; a vocabulary report in `inspect`; the
distribution boundary that keeps every glossary term out of the templates.
No approved artifact is rewritten. The proposal is
`docs/notes/assessment-requirement-readability-2026-09-04.md`.

## Terms

- **Reader-first shape:** the requirement body of exactly four sections,
  `In plain words`, `Why`, `Behavior`, `Examples`.
- **Harness term:** a word defined in the managed instructions and policy
  documents the distribution ships, identical in every repository.
- **Project term:** a word whose meaning belongs to one repository and its
  artifacts.
- **Seed:** a template file installed once under its target name and never
  rewritten by the harness, the mode the domain indexes already use.

## Behavioral rules

**TCM-RFR-001 (template).** `REQUIREMENT.template.md` keeps its front
matter (`statement`, `verification_method`, `priority`, `source`,
`measure`, `derives_from`) and carries the reader-first body: `In plain
words` (one or two sentences a newcomer understands), `Why` (at most five
sentences, why the obligation exists), `Behavior` (a table with the columns
Trigger, Response, On failure), `Examples` (one `Normal` and one `Failure`
scenario as Given, When, Then). `Rationale`, `Assumptions and
dependencies`, `Acceptance examples`, `Constraints`, `Preconditions and
trigger`, `Required response`, `Failure and boundary behavior` and `Open
decisions` are not in the template. The acceptance cases live in the
verification contract that `verifies` the requirement; the method lives in
the specification that `specifies` it.

**TCM-RFR-002 (actor).** The statement opener accepts a concrete component
in place of `THE SYSTEM` (`THE VALIDATOR SHALL`, `THE INSTALLER SHALL`),
as `W-AUT-001` already does. The authoring guide asks for the concrete
component when one exists and keeps `THE SYSTEM` for obligations that span
components.

**TCM-RFR-003 (advisories).** On requirement drafts only, the validator
adds to the `W-AUT` family: `W-AUT-003` fires when the statement exceeds
30 words (replacing the 300-character threshold); `W-AUT-005` when the body
exceeds 250 words; `W-AUT-006` when `Why` exceeds 120 words or five
sentences; `W-AUT-007` when any body sentence exceeds 25 words; `W-AUT-008`
when the body cites more than three code identifiers in backticks;
`W-AUT-009` when `In plain words` is missing or exceeds two sentences;
`W-AUT-010` when a statement opening `WHEN` names an event of evaluation
(`is validated`, `is evaluated`, `runs`) with no other condition. Words are
counted with code spans removed. Each advisory names the file, the budget
and the measured value. None fires on an approved artifact.

**TCM-RFR-004 (Explorer).** The dashboard generator projects the text of
`In plain words`, when present, as `plain_words` on requirement artifacts.
The record panel renders the statement first and `plain_words` directly
beneath it, before the lifecycle events. The lineage and graph views are
unchanged.

**TCM-RFR-005 (forward only).** No approved requirement is rewritten for
shape. An approved requirement adopts the reader-first shape only when it
is amended for another reason, in that amendment. The communication
policy's prohibition of style-only rewrites stands.

**TCM-RFR-006 (Open decisions retired).** Every definition template drops
the `Open decisions` section. The authoring gate `authoring_ready` no
longer requires the section; where a legacy artifact still carries it, the
section must read `None` or list `DEC-` identifiers, and prose there stays
`E-DCM-004`. `SPEC-DCM-001` rule 11 is amended by record to say so. The
pending state of a definition is read only from the decision artifacts
naming it in `blocks`, through the decision predicate of its gate.

**TCM-RFR-007 (glossary seed).** The template `GLOSSARY.md.seed` at the
template root is installed by `init` and `adopt` as `GLOSSARY.md` at the
repository root in seed mode: written when absent, never
rewritten, never hashed in the lock, ignored by `upgrade`. The seed carries
a Summary, the two-vocabulary rule, an empty `Terms` section and the
instruction that entries cite the artifact that fixes their meaning. It
carries no term.

**TCM-RFR-008 (vocabulary report).** `inspect` gains a `vocabulary`
section, read-only and deterministic. It tokenizes the statements and
bodies of every formal artifact with code spans removed, drops a common
English stoplist and the harness-term stoplist shipped with the script, and
reports: project terms whose occurrence count is at or above a threshold
(default 50, flag `--vocabulary-threshold`) and that have no entry in
`GLOSSARY.md`; glossary entries whose term occurs in no
artifact. Both are informational findings on the maintenance plane.
A missing glossary file is reported once, not treated as an error.

**TCM-RFR-009 (pointer and upkeep).** The requirement template's
`In plain words` guidance points at `GLOSSARY.md` at the repository root as
a file the repository writes, and says so. The authoring guide adds two sentences: a
glossary entry may cite the artifact that fixes its meaning; an amendment
that changes a term's meaning names the entry. The glossary is a note,
changed by pull request and review, never by a work order.

**TCM-RFR-010 (distribution boundary).** No file under
`templates/repository/standard/` carries a glossary term or definition. A
test asserts that the seed's `Terms` section is empty and that the
templates do not contain this repository's project vocabulary list. The
harness-term stoplist in the `inspect` script is the only vocabulary that
ships, as exclusions.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-TCM-006` | TCM-RFR-001, TCM-RFR-002, TCM-RFR-003, TCM-RFR-004, TCM-RFR-005 |
| `REQ-TCM-007` | TCM-RFR-007, TCM-RFR-008, TCM-RFR-009, TCM-RFR-010 |
| `REQ-TCM-008` | TCM-RFR-006 |

## Failure behaviour

An advisory never fails validation; the `W-AUT` class stays on the
maintenance plane. A malformed `Behavior` table is not parsed; the body
word budgets still apply. The vocabulary report degrades to a single
informational finding when the glossary file is absent or unreadable. The
authoring gate refuses nothing it did not refuse before, except that it
stops requiring a section.

## Compatibility and migration

The template, the authoring guide, the validator, the inspection script and
the Explorer template are managed files: they change in the candidate
templates under work orders, ship with the next release and reach this
repository at its next root adoption. Until then this repository's root
gate keeps requiring `Open decisions` on new drafts, and the drafts of this
packet carry the line for that reason only. The 328 existing requirements
are unchanged. The threshold `W-AUT-003` moves from 300 characters to 30
words; the diagnostic-code index regenerates from the source.

## Explicitly unspecified decisions

The exact wording of each advisory; the contents of the two stoplists; the
tokenizer's treatment of hyphenated terms; the visual placement of
`plain_words` beyond "beneath the statement"; whether the advisories later
become blocking at approval, which is the owner's decision recorded in the
proposal; the reading-grade estimate, which stays a manual measure and is
not mechanized.

## Amendment record

- 2026-09-04, under `WO-TCM-006`, by the delegated executor on the
  repository owner's instruction "This repository's glossary moves to
  /GLOSSARY.md, and the notes index and the two notes that link it follow",
  recorded for the owner's verification of the record. Rules `TCM-RFR-007`,
  `TCM-RFR-008` and `TCM-RFR-009` name `GLOSSARY.md` at the repository root
  where they named `docs/notes/glossary.md`; the seed is `GLOSSARY.md.seed`
  at the template root. The reason is discoverability: a newcomer meets the
  glossary beside the README. `REQ-TCM-007`'s Behavior row still reads the
  old path; its obligation is unchanged and the row is not rewritten. The
  requirement template shipped by `WO-TCM-005` is repointed under this work
  order.
