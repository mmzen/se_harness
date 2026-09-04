+++
id = "SPEC-TCM-005"
type = "specification"
title = "Reader-first capabilities, the ability field and the graph-read derivation"
status = "approved"
owners = ["technical-owner", "quality-owner"]
created = "2026-09-04"
updated = "2026-09-04"

[relations]
specifies = ["REQ-TCM-012", "REQ-TCM-013"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-04T19:45:21Z"
decided_by = "technical-owner"
reason = "Approved by the accountable repository owner on 2026-09-04 with the instruction 'i apprive' (approve), after reviewing PR #342 (REQ-TCM-012, REQ-TCM-013, SPEC-TCM-005, VER-TCM-005, WO-TCM-008), carrying the owner's four decisions on the capability assessment of the same day."
+++

# Specification: Reader-first capabilities, the ability field and the graph-read derivation

## Scope

The managed capability template and its authoring-guide section; the
capability row of the per-type advisory table that `SPEC-TCM-004`
introduces for intents; an additive `ability` field; the retirement of the
requirement list from the template and the checklist; the Explorer's
rendering of a capability and of what derives from it. No approved artifact
is rewritten. The proposal is
`docs/notes/assessment-capability-readability-2026-09-04.md`; the owner
decided its four points as recommended on 2026-09-04.

## Terms

- **Ability.** The one sentence a capability exists for: an actor, `can`,
  an achievement, `under` conditions.
- **Reader-first shape.** The capability body of exactly three sections,
  `In plain words`, `Actor and need`, `Not decided here`.
- **Deriving requirements.** The requirements whose `derives_from` names
  the capability; the authoritative record of what the capability leads to.
- **Type table.** The per-artifact-type budget constants that
  `SPEC-TCM-004` rule `TCM-RFI-003` establishes so the shared advisory
  codes fire with the constants of the type being validated.

## Behavioral rules

**TCM-RFC-001 (template).** `CAPABILITY.template.md` keeps the common front
matter (`id`, `type`, `title`, `status`, `owners`, `created`, `updated`,
`[relations]` with `derives_from`), adds `ability` with a placeholder and a
comment stating its rule, and carries the reader-first body: `In plain
words` (one or two sentences a newcomer understands), `Actor and need` (at
most three sentences: who the actor is and what they need, in their words;
the outcome is the intent's and is not restated), `Not decided here` (at
most five bullets naming what is left to a requirement, a specification or
another capability). `Capability statement`, `Boundaries`, `Outcomes` and
`Candidate requirements` are not in the template. The template comment says
where each went: the statement to the field, the boundaries to `Not decided
here`, the outcomes to the intent's success measures and the requirements'
statements, the requirement list to the graph.

**TCM-RFC-002 (ability field).** `ability` is a non-empty string of at most
30 words, one sentence, containing the word `can` and the word `under`,
without a code span. The validator accepts it on a capability and reports
`E-AUT-002` when it is present but empty or not a string, as it does for
`source` and for an intent's `outcome`. A capability without `ability`
validates without error; the field is additive and every existing
capability is unchanged.

**TCM-RFC-003 (advisories).** On capability drafts only, the validator
raises `W-AUT` advisories on the maintenance plane: `W-AUT-016` when
`ability` is missing, exceeds 30 words, lacks `can`, lacks `under`, or
contains a code span; `W-AUT-017` when `Actor and need` exceeds 60 words or
three sentences; `W-AUT-018` when the body carries a `Candidate
requirements` or `Derived requirements` heading. The shared budgets reuse
their existing codes with capability constants in the type table:
`W-AUT-005` when the body exceeds 150 words; `W-AUT-007` when any body
sentence exceeds 25 words; `W-AUT-008` when the body cites more than two
code identifiers; `W-AUT-009` when `In plain words` is missing or exceeds
two sentences. Words are counted with code spans removed. Each advisory
names the file, the budget and the measured value. None fires on an
approved capability or on any other artifact type; the requirement and
intent constants are unchanged.

**TCM-RFC-004 (checklist and guidance).** The capability section of
`ARTIFACT_AUTHORING.md` is rewritten line by line for the shape above,
each line naming its mechanical counterpart where one exists. The line
"lists its derived requirements" goes. The guidance gains two sentences: a
capability is warranted when an intent needs more than one actor ability,
or when a requirement set needs an actor it can be read against; a
capability never contains an outcome, which is the intent's, or a
behavior, which is a requirement's.

**TCM-RFC-005 (the list is the graph).** No template or checklist asks a
capability to list its requirements. The dashboard generator projects
`derived_requirements` on capability artifacts: the ids of the
requirements whose `derives_from` names the capability, sorted, taken from
the declared relations the bundle already carries. A legacy list in a
body is retained prose and draws `W-AUT-018` on a draft only.

**TCM-RFC-006 (Explorer).** The dashboard generator projects `ability` (the
field's text) and `plain_words` (by the helper that serves requirements and
intents) on capability artifacts when present. The record panel renders
the ability first, the plain words beneath it, then the deriving
requirements as linked ids under a `Derives` label, all before the
lifecycle events; the lineage board shows the ability under the
capability's title in its second stage. The graph and overview views are
otherwise unchanged.

**TCM-RFC-007 (forward only).** No approved capability is rewritten for
shape. An approved capability adopts the reader-first shape and the
`ability` field only when it is amended for another reason, in that
amendment. The communication policy's prohibition of style-only rewrites
stands.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-TCM-012` | TCM-RFC-001, TCM-RFC-002, TCM-RFC-003, TCM-RFC-004, TCM-RFC-007 |
| `REQ-TCM-013` | TCM-RFC-005, TCM-RFC-006 |

## Failure behaviour

An advisory never fails validation; the `W-AUT` class stays on the
maintenance plane. A malformed `ability` that is a non-empty string raises
`W-AUT-016` on a draft and nothing on an approved capability; only an
empty or non-string value is the structural error `E-AUT-002`. A capability
with no deriving requirement projects an empty `derived_requirements` list.
The record panel falls back to the title when no ability is present.

## Compatibility and migration

The template, the authoring guide, the validator, the dashboard generator
and the Explorer template are managed files: they change in the candidate
templates under a work order, ship with the next release, and reach this
repository at its next root adoption, like `WO-TCM-005`. This
specification depends on the type table `WO-TCM-007` introduces for
intents; its work order stacks on `WO-TCM-007` so the table is written
once and gains one row. The 36 existing capabilities are unchanged. Until
the adoption, drafts in this repository still end with `Open decisions`
reading `None`, as the root gate of 0.14.0 requires.

## Explicitly unspecified decisions

The exact wording of each advisory; the tokenizer's treatment of the words
`can` and `under` inside longer words; the visual placement of the
`Derives` list beyond "beneath the plain words and before the lifecycle
events"; whether the advisories later become blocking at approval, which
the owner decided as "advisory for one release, then blocking", to be
executed in step with the requirement and intent families; whether the
capability layer stays mandatory, which the owner decided to keep and
revisit after one release of the new shape.
