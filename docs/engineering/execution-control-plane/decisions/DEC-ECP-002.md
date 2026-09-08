+++
id = "DEC-ECP-002"
type = "decision"
title = "ECP-PRM-027 counts three engine blocks wave 2 may not touch"
status = "open"
owners = ["technical-owner", "engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"
kind = "deviation"
question = "How does ECP-PRM-027 stand when the three cross-file blocks the scan still reports each pair a copy inside se_harness/engine/, which SPEC-ECP-023 and WO-ECP-033 leave to wave 3?"
raised_by = "engineering-owner"
recommendation = "accept"
against = "SPEC-ECP-023#ECP-PRM-027"
observed = "ECP-PRM-027 requires the duplication scan (pylint --enable=duplicate-code, eight-line minimum) to report none of the seven cross-file blocks the assessment of 2026-09-07 recorded. At the completion of WO-ECP-033 the scan reports three: se_harness/artifact_layout.py with se_harness/engine/artifact_layout_registry.py (the layout registry), se_harness/provenance.py with se_harness/engine/validate_engineering_artifacts.py (the standing deviations), and se_harness/engine/generate_harness_dashboard.py with se_harness/engine/validate_engineering_artifacts.py (the body parser). Every one has a side inside se_harness/engine/. The specification's Scope defers the engine to wave 3 (#378) and the three work orders of wave 2 name 'no engine file changes' among their constraints, so no wave 2 execution may remove them. The four package-side blocks are gone: one in wave 1, the atomic writer and DEFINITION_TYPES in WO-ECP-032, the restitution fields in WO-ECP-033."

[[options]]
id = "accept"
label = "Accept the deviation for this wave: the rule stands as written, is met for the four package-side blocks, and is read again when wave 3 (#378) decides the engine's import surface and moves or shares its three copies."

[[options]]
id = "amend"
label = "Amend the rule by record to name the four package-side blocks as its subject and assign the three engine blocks to wave 3, so the rule reads met now and wave 3 inherits its own rule."

[[options]]
id = "stop"
label = "Stop WO-ECP-033 until the specification and the wave plan are reconciled by their owners."

[relations]
concerns = ["SPEC-ECP-023", "WO-ECP-033", "WO-ECP-031", "WO-ECP-032"]
blocks = ["WO-ECP-033"]
+++

# Decision: ECP-PRM-027 counts three engine blocks wave 2 may not touch

## Question

`SPEC-ECP-023` `ECP-PRM-027` reads: the duplication scan must report none of
the seven cross-file blocks the assessment recorded. The assessment counted
seven on 2026-09-07; wave 1 removed one before wave 2 began; `WO-ECP-032`
removed the atomic writer and `DEFINITION_TYPES`; `WO-ECP-033` removed the
restitution fields. The scan at the completion of `WO-ECP-033` reports three
blocks, and each has one side under `se_harness/engine/`: the layout registry,
the standing deviations and the body parser. The specification's Scope leaves
the engine to wave 3 (#378), and the constraints of `WO-ECP-031`, `WO-ECP-032`
and `WO-ECP-033` each forbid an engine file in the change set. The rule
cannot be met by the wave it belongs to; the implementation did not adjust
the rule, and this decision is the work order's stop condition for it.

## Options

- `accept`: the rule stands as written and is met for every block wave 2 may
  touch. The deviation stays visible on `SPEC-ECP-023`, on `WO-ECP-033` and on
  the records until wave 3 removes the three engine copies or decides that the
  engine keeps them; the revisit trigger is the merge of wave 3 (#378).
- `amend`: the rule is amended by record to name the four package-side blocks
  as its subject and to assign the three engine blocks to wave 3, whose
  specification then carries its own rule. The rule reads met now; the cost is
  a rule that names the blocks it was written to count.
- `stop`: `WO-ECP-033` waits until the specification and the wave plan are
  reconciled by their owners.

## Recommendation

`accept`. The rule is right and the timing is wrong: the blocks it counts are
real and wave 3 is where they go. Accepting records that fact against the
specification without rewriting a rule to fit the calendar, and wave 3 reads
the same scan and the same seven blocks when it closes.

## Disposition

Written by `harnessctl decide`; do not edit by hand. The `[disposition]`
table records the option, its label, the role, the time and the verbatim
reason. An accepted deviation records its revisit trigger and stays visible
on the departed specification, the work order and the records until the rule
changes.
