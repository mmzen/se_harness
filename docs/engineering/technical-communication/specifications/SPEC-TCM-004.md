+++
id = "SPEC-TCM-004"
type = "specification"
title = "Reader-first intents, operational success measures and the Explorer's outcome line"
status = "draft"
owners = ["technical-owner", "quality-owner"]
created = "2026-09-04"
updated = "2026-09-04"

[relations]
specifies = ["REQ-TCM-009", "REQ-TCM-010", "REQ-TCM-011"]
+++

# Specification: Reader-first intents, operational success measures and the Explorer's outcome line

## Scope

The managed intent template and its authoring guide section; an `outcome`
front-matter field on intents; draft-time authoring advisories of the
candidate validator for intents; a rule separating a success measure from
an acceptance check; the Explorer's projection and rendering of an intent's
outcome and plain words, and the derivation of the G0 `intent_quality`
condition. No approved artifact is rewritten. The proposal is
`docs/notes/assessment-intent-readability-2026-09-04.md`; the requirement
counterpart is `SPEC-TCM-003`.

## Terms

- **Reader-first intent shape:** the intent body of exactly four sections,
  `In plain words`, `Problem`, `Success measures`, `Not this`.
- **Outcome:** the `outcome` front-matter field: one sentence naming who
  can do or observe what after delivery, without naming a solution.
- **Success measure:** a row of the `Success measures` table with the
  columns `Measure`, `Today`, `When reached`, `Observed`.
- **Acceptance check:** a row whose `Observed` cell names a CI run, a test,
  a validator run, a verification or an implementation review.
- **Acceptance vocabulary:** the closed, case-insensitive word list the
  validator matches in an `Observed` cell: `CI`, `test`, `tests`,
  `validator`, `validate`, `verification`, `implementation review`,
  `acceptance run`, `regression run`, `transaction`.

## Behavioral rules

**TCM-RFI-001 (template).** `INTENT.template.md` keeps the common front
matter (`id`, `type`, `title`, `status`, `owners`, `created`, `updated`,
`[relations]`), adds `outcome` with a placeholder and a comment stating its
rule, and carries the reader-first body: `In plain words` (one or two
sentences a newcomer understands), `Problem` (at most five sentences: what
happens today, to whom, and why it is worth changing; evidence cited by
link, not quoted), `Success measures` (the four-column table), `Not this`
(at most five bullets). `Desired outcomes`, `Actors and stakeholders`,
`Principles and immutable constraints`, `Risks and assumptions` and
`Non-goals` are not in the template. The template comment says where each
went: the outcome to the field, the actors to the capability's
`Actor and need`, the principles to a specification rule or an ADR, the
risks to a risk artifact, an open question to a `DEC-` artifact.

**TCM-RFI-002 (outcome field).** `outcome` is a non-empty string of at most
30 words, one sentence, without a code span. The validator accepts it on an
intent and reports `E-AUT-002` when it is present but empty or not a
string, as it does for `source`. An intent without `outcome` validates
without error; the field is additive and every existing intent is
unchanged.

**TCM-RFI-003 (advisories).** On intent drafts only, the validator raises
`W-AUT` advisories on the maintenance plane: `W-AUT-011` when `outcome` is
missing, exceeds 30 words, or contains a code span; `W-AUT-012` when
`Problem` exceeds 120 words or five sentences; `W-AUT-015` when the body
cites a repository path (a code span containing `/` and a file extension)
or a source line range (a code span ending in `:N` or `:N-M`). The shared
budgets reuse their existing codes with intent constants: `W-AUT-005` when
the body exceeds 200 words; `W-AUT-007` when any body sentence exceeds 25
words; `W-AUT-008` when the body cites more than two code identifiers;
`W-AUT-009` when `In plain words` is missing or exceeds two sentences.
Words are counted with code spans removed. Each advisory names the file,
the budget and the measured value. None fires on an approved intent or on
any artifact type other than intent; the requirement constants of
`SPEC-TCM-003` are unchanged.

**TCM-RFI-004 (success measure).** A success measure is observed in
operation, after delivery, by someone who has not read the code; its
`Observed` cell names a place and a cadence an operator recognises. On
intent drafts only: `W-AUT-013` fires once per row whose `Observed` cell
contains a word of the acceptance vocabulary, naming the row's `Measure`
and saying the row belongs in the verification contract; `W-AUT-014` fires
when the `Success measures` section exists and its table has no data row.
A `Today` cell reading `not measured` raises nothing. A target of `0`
raises nothing. A malformed table is not parsed and raises `W-AUT-014`.

**TCM-RFI-005 (checklist and guidance).** The intent section of
`ARTIFACT_AUTHORING.md` is rewritten line by line for the shape above,
each line naming its mechanical counterpart where one exists, as the
requirement section does. The guidance keeps the sentence "write it so
that a reader can tell, years later, whether the outcome was reached" and
adds two: a new intent is warranted when an owner would be asked about a
new outcome in a year; a new thing an actor can do toward an outcome
already stated is a capability under the existing intent.

**TCM-RFI-006 (Explorer).** The dashboard generator projects `outcome`
(the field's text) and `plain_words` (the section's text, by the helper
that already serves requirements) on intent artifacts when present. The
record panel renders the outcome first and the plain words directly
beneath it, before the lifecycle events; the lineage board shows the
outcome under the intent's title in the first stage. The G0 condition
`intent_quality` reads `satisfied` when at least one reachable active
intent carries `outcome` and a `Success measures` table with at least one
data row, and `not_assessable` otherwise. It remains a derived observation
in a derived grouping and is not a gate result; the graph and overview
views are otherwise unchanged.

**TCM-RFI-007 (forward only).** No approved intent is rewritten for shape.
An approved intent adopts the reader-first shape and the `outcome` field
only when it is amended for another reason, in that amendment. The
communication policy's prohibition of style-only rewrites stands.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-TCM-009` | TCM-RFI-001, TCM-RFI-002, TCM-RFI-003, TCM-RFI-005, TCM-RFI-007 |
| `REQ-TCM-010` | TCM-RFI-004 |
| `REQ-TCM-011` | TCM-RFI-006 |

## Failure behaviour

An advisory never fails validation; the `W-AUT` class stays on the
maintenance plane. A malformed `Success measures` table raises `W-AUT-014`
and nothing else. An `outcome` that is present but not a non-empty string
is `E-AUT-002`, a structure error, as for the other optional attributes.
The Explorer renders an intent without the fields exactly as before. The
authoring gate refuses nothing it did not refuse before.

## Compatibility and migration

The template, the authoring guide, the validator, the dashboard generator
and the Explorer template are managed files: they change in the candidate
templates under a work order, ship with the next release and reach this
repository at its next root adoption. The 33 existing intents are
unchanged and none carries `outcome`; the hash-locked root copies are not
edited. The diagnostic-code index regenerates from the source for the five
new codes. The requirement advisories and constants of `SPEC-TCM-003` are
not changed; an implementation may share the counting helpers.

## Explicitly unspecified decisions

The exact wording of each advisory; the tokenizer and sentence splitter,
shared with the requirement advisories; the exact path and line-range
patterns beyond the two shapes named in TCM-RFI-003; the visual placement
of the outcome beyond "beneath the title" and "before the lifecycle
events"; whether the advisories later become blocking at approval, which is
the owner's decision recorded in the proposal; the reading-grade estimate,
which stays a manual measure.
