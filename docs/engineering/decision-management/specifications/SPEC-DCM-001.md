+++
id = "SPEC-DCM-001"
type = "specification"
title = "Decision artifact contract"
status = "draft"
owners = ["technical-owner", "quality-owner", "product-owner"]
created = "2026-09-03"
updated = "2026-09-03"

[relations]
specifies = ["REQ-DCM-001", "REQ-DCM-002", "REQ-DCM-003"]
+++

# Specification: Decision artifact contract

## Scope

One new formal artifact type, the decision (`DEC-`), in two kinds: a
question met while authoring or planning, and a deviation met while
implementing against one rule of one specification. This contract defines
the artifact's fields, relations, lifecycle, gate, decision right, command,
validator diagnostics, and Explorer projection. It does not define risks,
and it does not change the ADR.

## Actors and external systems

- The raising actor: a human or a coding agent that meets a question above
  the authoring threshold or an implementation deviation.
- The accountable role: the owner of the artifact a decision blocks; for a
  deviation, the owner of the specification departed from.
- The evaluator: `harnessctl` validates, gates, disposes, and projects.
- The Explorer: renders open decisions and standing deviations.

## Inputs

- A decision artifact in TOML front matter plus Markdown body, under
  `docs/engineering/<domain>/decisions/DEC-<DOMAIN>-NNN.md`.
- A disposition request: decision id, option id, accountable role, reason,
  and for `deferred` or `accept` a revisit trigger and, for `deferred`, a
  scope.
- Untrusted repository text in every field.

## Outputs

- Refusals at every checkpoint of a blocked artifact while the decision is
  open (or deferred outside its scope), naming the decision, its options,
  the deciding role and the corrective command.
- A disposition table and a lifecycle event on the decision.
- Validator diagnostics `E-DCM-001` to `E-DCM-004` and `W-DCM-001`,
  `W-DCM-002`.
- Explorer projections: open decisions in the in-flight tile; the decision
  trail on concerned artifacts; standing deviations on the specification,
  the work order, and the records.

## State model

```text
open -> decided
open -> deferred    (scope + revisit)      deferred -> decided
open -> withdrawn                           deferred -> withdrawn
```

`decided` and `withdrawn` are terminal and retained. A `decided` deviation
whose option is `accept` is a standing deviation until a later decision
against the same rule is disposed `amend` or `supersede`.

## Behavioral rules

1. **Type and location.** `type = "decision"`, prefix `DEC-`, canonical
   directory `decisions/` in the domain. The layout registry, the
   templates index and `ARTIFACT_AUTHORING.md` name it.
2. **Kinds.** `kind` is `"question"` or `"deviation"`. Both need `question`
   (one sentence), `raised_by`, at least two `[[options]]` each with `id`
   and `label`, and `recommendation` naming one option id.
3. **Deviation fields.** A deviation also needs `against` (one artifact id
   and one rule reference, for example `SPEC-DST-014#rule-7`) and
   `observed` (the fact that cannot be met). Its options are exactly
   `amend`, `supersede`, `accept`, `stop`, in any subset of at least two
   that includes `stop`.
4. **Relations.** `concerns` names one or more artifacts of any type.
   `blocks` names one or more artifacts of type requirement,
   specification, verification, architecture, adr, or work_order; every
   `blocks` target is also in `concerns`. `produces` is written only by a
   disposition and names one ADR, one amended artifact, or one successor.
5. **Gate.** The predicate `QGP-DECISION-OPEN` (evaluator
   `decision_gate_clear`) joins every gate the workflow contract evaluates
   for a transition of a definition, a work order, a verification record
   or a release record. It fails when any decision in `open` names the
   artifact in `blocks`, or any decision in `deferred` names it and its
   `scope` does not admit the requested transition. The failure message
   names the decision id, the question, each option id with its label, the
   deciding role, and the corrective command `harnessctl decide`.
6. **Disposition.** `harnessctl decide <DEC> --option <id> --decision
   <role> --reason <text>` applies the transition `open|deferred ->
   decided`. `--defer --scope <ARTIFACT:from->to,...> --revisit <text>`
   applies `open -> deferred`. `--withdraw` applies `-> withdrawn`. The
   command writes the `[disposition]` table (option id, label copied from
   the artifact, role, UTC time, reason verbatim, revisit and scope when
   present) and the lifecycle event. A hand-written disposition is
   `E-DCM-003`.
7. **Decision right.** `DR-DECISION-DISPOSE`: the role that holds the
   decision right for the blocked artifact under the existing rights; for
   a deviation, the owner named on the specification in `against`. Any
   other role is refused with no change.
8. **Time bounds.** `deferred` requires `scope` and `revisit`. `accept`
   requires `revisit`. A revisit trigger is free text naming a release, a
   date, or an artifact reaching a state.
9. **Standing deviation.** After `accept`, the validator projects the
   decision onto the specification in `against`, onto every work order in
   `concerns`, and onto every verification or release record whose covered
   work includes one of those work orders. `capture-verification` lists the
   decision ids in the record's evidence section.
10. **Revisit warnings.** `W-DCM-001` on the specification when an accepted
    deviation's `revisit` names a release or state that has occurred and no
    later decision against the same rule is `decided` with `amend` or
    `supersede`. `W-DCM-002` when two or more accepted deviations stand
    against the same rule.
11. **Threshold.** `ARTIFACT_AUTHORING.md` states when a question must be a
    decision artifact: it blocks a transition, it concerns more than one
    artifact, or it must survive approval. The `## Open decisions` section
    of a definition lists decision ids or `None`; prose there is
    `E-DCM-004` once the section is checked at approval.
12. **Retention.** `decided` and `withdrawn` decisions are never deleted or
    rewritten. `renumber-artifacts` treats `DEC-` like every other prefix.
13. **Explorer.** The in-flight tile lists open and deferred decisions with
    age and deciding role; the record panel of a concerned artifact shows
    the decision trail; the proof block of a record and the release
    inherit the standing deviations; the summary `metrics` gain
    `decisions_open`, `decisions_decided`, and raise-to-dispose times.
14. **Validator diagnostics.** `E-DCM-001`: a decision names a `blocks`
    target that does not exist or is not a permitted type. `E-DCM-002`: a
    decision lacks a required field for its kind. `E-DCM-003`: a
    disposition was written without a lifecycle event, or the option id
    is not declared. `E-DCM-004`: an `## Open decisions` section carries
    prose at approval.

## Error and recovery behavior

Every refusal leaves state unchanged and prints one corrective command.
A malformed decision is a graph error and blocks like an open one, since
the graph must be valid for any transition. A missing revisit or scope is
refused at disposition, not discovered later.

## Data and interface contracts

```toml
id = "DEC-DOM-001"
type = "decision"
kind = "deviation"
status = "open"
owners = ["technical-owner"]
question = "Does the Lineage view keep loading every artifact detail on entry?"
raised_by = "implementation-agent"
recommendation = "accept"
against = "SPEC-DST-014#rule-7"
observed = "The designed view fetches 1,224 details to draw its board."

[[options]]
id = "amend"
label = "Amend rule 7 to allow the prefetch"
[[options]]
id = "accept"
label = "Accept now; revisit at the next design round"
[[options]]
id = "stop"
label = "Block completion until the view is lazy"

[relations]
concerns = ["SPEC-DST-014", "WO-DST-023", "VER-DST-014"]
blocks = ["WO-DST-023"]
```

The `[disposition]` table is written by the tool with `option`, `label`,
`decided_by`, `decided_at`, `reason`, and `revisit` or `scope` when
present. The workflow contract gains the lifecycle family `decision`; the
quality-gates contract gains `QGP-DECISION-OPEN`; `TRACEABILITY.md` gains
`concerns`, `blocks` and `produces` with their target types.

## Security and privacy properties

Repository text stays inert: the refusal message and the Explorer render
the question, labels and reasons as text, never as markup or commands. The
disposition is attributed to a role and checked against the decision
right; the tool refuses to write it for any other role.

## Performance and capacity

The gate reads the decisions of the repository once per evaluation; on this
repository that is tens of files. No budget changes.

## Observability

Refusals carry the predicate id. The Explorer shows open decisions and
their age. The summary metrics report counts and raise-to-dispose times.

## Compatibility and migration

Existing `## Open decisions` sections that read `None` are unaffected.
Existing prose deviations (for example in `SPEC-DST-023`) stay as history;
new ones use the artifact. The root managed copies change at the next
release adoption; consumer repositories receive the type through the
ordinary upgrade. No existing artifact is rewritten.

## Examples and counterexamples

- Intended: a refusal reads "DEC-DST-001 is open: Does the Lineage view keep
  loading every artifact detail on entry? Options: amend, accept, stop.
  Decider: technical-owner. Next: harnessctl decide DEC-DST-001 --option
  <id> --decision technical-owner --reason <text>".
- Intended: `decide … --option accept --revisit "the next Lineage design
  round"` records the label verbatim and the deviation appears on
  `SPEC-DST-014`, `WO-DST-023`, and the next record.
- Invalid: a `priority` field that admits a transition; `accept` without
  `revisit`; a disposition by the work order's owner on a deviation; a
  decision with one option; prose in `## Open decisions`.

## Explicitly unspecified decisions

The implementation agent may choose the module layout, the exact wording
of refusal messages within the rule above, the Explorer's visual treatment
of open decisions and standing deviations, the fixture layout of tests,
and the `--scope` syntax details, provided a scope names artifact and
transition pairs.
