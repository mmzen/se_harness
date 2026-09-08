+++
id = "DEC-ECP-001"
type = "decision"
title = "SPEC-ECP-023 asks repository_tools to import the package across the import barrier"
status = "decided"
owners = ["technical-owner", "engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"
kind = "deviation"
question = "How do ECP-PRM-003, ECP-PRM-005, ECP-PRM-009 and ECP-PRM-015 stand when repository_tools may not import se_harness?"
raised_by = "engineering-owner"
recommendation = "amend"
against = "SPEC-ECP-023#ECP-PRM-003"
observed = "ECP-PRM-003 and ECP-PRM-005 require every Git launch and every front-matter read in repository_tools to call the package's primitives, and ECP-PRM-009 and ECP-PRM-015 require repository_tools/json_bytes.py to re-export them and one environment builder to serve upgrade_rehearsal. ARCH-REB-010, kept by ARCH-REB-013 and SPEC-REB-015 rule 2, fixes that repository_tools imports only the standard library and its own package; tests/test_interpreter_safety.py and tests/test_ci_pipeline.py refuse a repository_tools import of se_harness. The specification's Scope sentence 'and repository_tools, which imports it' was wrong: nothing outside the package imports it, by design. The executor applied the four tool edits on 2026-09-08, saw the barrier tests refuse them, and withdrew them; the package edits stand."

[[options]]
id = "amend"
label = "Amend the four rules by record so they bind the package only; repository_tools keeps its own standard-library launchers, parser, serializers and environment builder behind the barrier, and the duplication the assessment counted there is accepted as the price of ARCH-REB-013."

[[options]]
id = "accept"
label = "Accept the deviation for this wave: the four rules stand as written and are met for the package only, revisited when wave 3 (#378) decides whether repository_tools may share code with the package by another route."

[[options]]
id = "stop"
label = "Stop WO-ECP-031 until the specification and the barrier are reconciled by their owners."

[relations]
concerns = ["SPEC-ECP-023", "WO-ECP-031", "WO-ECP-032", "ARCH-REB-013"]
blocks = ["WO-ECP-031"]

[disposition]
option = "amend"
label = "Amend the four rules by record so they bind the package only; repository_tools keeps its own standard-library launchers, parser, serializers and environment builder behind the barrier, and the duplication the assessment counted there is accepted as the price of ARCH-REB-013."
decided_by = "technical-owner"
decided_at = "2026-09-08T10:23:52Z"
reason = "Amended by record on 2026-09-08, the owner selecting the presented option 'Amend, and widen the scope': ECP-PRM-003, ECP-PRM-005, ECP-PRM-009 and ECP-PRM-015 bind the package only; repository_tools keeps its standard-library launchers, parser, serializers and environment builder behind the import barrier of ARCH-REB-013 and SPEC-REB-015 rule 2, and the copies the assessment counted there are the accepted price of that barrier. The amendment record is written on SPEC-ECP-023 under WO-ECP-031, whose scope names it."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-09-08T10:23:52Z"
decided_by = "technical-owner"
reason = "Amended by record on 2026-09-08, the owner selecting the presented option 'Amend, and widen the scope': ECP-PRM-003, ECP-PRM-005, ECP-PRM-009 and ECP-PRM-015 bind the package only; repository_tools keeps its standard-library launchers, parser, serializers and environment builder behind the import barrier of ARCH-REB-013 and SPEC-REB-015 rule 2, and the copies the assessment counted there are the accepted price of that barrier. The amendment record is written on SPEC-ECP-023 under WO-ECP-031, whose scope names it."
+++

# Decision: SPEC-ECP-023 asks repository_tools to import the package across the import barrier

## Question

`SPEC-ECP-023` was approved on 2026-09-08 with the Scope sentence "The
package `se_harness/` and `repository_tools/`, which imports it." Four rules
follow from it: `ECP-PRM-003` and `ECP-PRM-005` route every Git launch and
every front-matter read of `repository_tools` through the package's
primitives; `ECP-PRM-009` has `repository_tools/json_bytes.py` re-export the
integrity primitives; `ECP-PRM-015` has one environment builder serve
`upgrade_rehearsal`. The premise is false. `ARCH-REB-010`, whose barrier
`ARCH-REB-013` and `SPEC-REB-015` rule 2 keep, fixes that `repository_tools`
imports only the standard library and its own package, and two tests refuse
any crossing. On 2026-09-08 the executor of `WO-ECP-031` applied the four
tool edits, saw `tests/test_interpreter_safety.py` and
`tests/test_ci_pipeline.py` refuse them, and withdrew them. The package's own
launcher and parser are in place and every other rule of group A is met.
The work order's stop condition for a rule that cannot be met as written is
this decision; the implementation did not adjust the rule.

## Options

- `amend`: the four rules are amended by record to bind the package only.
  `repository_tools` keeps its standard-library launchers, parser,
  serializers and environment builder; the copies the assessment counted
  there are the accepted price of the barrier. Group B's `ECP-PRM-009`
  rename of `release_build.canonical_json_bytes` still happens, so recipe
  digests are unaffected either way.
- `accept`: the rules stand as written and are met for the package only
  during this wave; the revisit trigger is wave 3 (#378), which decides the
  engine's import surface and may decide the tools' by the same act.
- `stop`: `WO-ECP-031` waits until the specification and the barrier are
  reconciled by their owners.

## Recommendation

`amend`. The barrier is a security boundary the released-evaluator domain
chose deliberately and reaffirmed twice; a code-health specification does
not override it. Recording that here costs nothing now, and the reduction
the wave promised still lands where it matters, in the package every
consumer runs.

## Disposition

Written by `harnessctl decide`; do not edit by hand. The `[disposition]`
table records the option, its label, the role, the time and the verbatim
reason. An accepted deviation records its revisit trigger and stays visible
on the departed specification, the work order and the records until the rule
changes.
