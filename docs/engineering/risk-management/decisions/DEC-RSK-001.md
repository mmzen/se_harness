+++
id = "DEC-RSK-001"
type = "decision"
title = "RSK-MGT-034 names a retired command"
status = "decided"
owners = ["technical-owner", "assurance-owner"]
created = "2026-09-08"
updated = "2026-09-07"
kind = "deviation"
question = "How does RSK-MGT-034 stand now that harnessctl renumber-artifacts is retired?"
raised_by = "delegated-executor"
recommendation = "amend"
against = "SPEC-RSK-010#RSK-MGT-034"
observed = "WO-ECP-030, merged to main as edeb4f8 on 2026-09-08 while WO-RSK-010 was in progress, retired harnessctl renumber-artifacts. The rule's first clause names that command, so no test can show it treats RISK- like every other prefix; its second clause holds, since no command deletes or rewrites a terminal risk."

[[options]]
id = "amend"
label = "Amend RSK-MGT-034 to drop the retired command and keep the clause that a terminal risk is never deleted or rewritten."

[[options]]
id = "accept"
label = "Accept the deviation: the first clause stands vacuously until SPEC-RSK-010 is next amended; revisit at that amendment."

[[options]]
id = "stop"
label = "Stop the work order until the specification is repaired."

[relations]
concerns = ["SPEC-RSK-010", "WO-RSK-010"]
blocks = ["WO-RSK-010"]

[disposition]
option = "amend"
label = "Amend RSK-MGT-034 to drop the retired command and keep the clause that a terminal risk is never deleted or rewritten."
decided_by = "technical-owner"
decided_at = "2026-09-07T22:13:55Z"
reason = "Amended by record on 2026-09-08, the owner selecting the presented option: RSK-MGT-034 drops the retired command renumber-artifacts (WO-ECP-030) and keeps the clause that a terminal risk is never deleted or rewritten; the text is repaired under a repair work order."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-09-07T22:13:55Z"
decided_by = "technical-owner"
reason = "Amended by record on 2026-09-08, the owner selecting the presented option: RSK-MGT-034 drops the retired command renumber-artifacts (WO-ECP-030) and keeps the clause that a terminal risk is never deleted or rewritten; the text is repaired under a repair work order."
+++

# Decision: RSK-MGT-034 names a retired command

## Question

`RSK-MGT-034` reads: "`renumber-artifacts` MUST treat `RISK-` like every other
prefix, and a terminal risk MUST NOT be deleted or rewritten." `SPEC-RSK-010`
was approved on 2026-09-07. On 2026-09-08, while `WO-RSK-010` was in progress,
`WO-ECP-030` merged to `main` and retired `harnessctl renumber-artifacts`
together with `rehearse-recovery`, the journal and two contract entries. The
command the first clause names no longer exists, so the clause cannot be shown
by a test. The second clause holds: no command deletes or rewrites a risk in
`accepted`, `avoided`, `mitigated` or `withdrawn`, and
`tests/test_risk_management.py` shows every transition out of a terminal state
refused. `WO-RSK-010`'s stop condition for a rule that cannot be met as written
is this decision; the implementation did not adjust the rule.

## Options

- `amend`: the rule is amended by record to name no command; the second
  clause stays. The amendment itself is written under a repair work order.
- `accept`: the deviation stands, time-bounded to the next amendment of
  `SPEC-RSK-010`; the rule's first clause is vacuously met until then.
- `stop`: the work order waits until the specification is repaired first.

## Recommendation

`amend`. The clause was overtaken by a decision the owner already took in
`WO-ECP-030`; recording that here and repairing the text later costs nothing
now and leaves no vacuous rule standing.

## Disposition

Written by `harnessctl decide`; do not edit by hand. The `[disposition]`
table records the option, its label, the role, the time and the verbatim
reason. An accepted deviation records its revisit trigger and stays visible on
the departed specification, the work order and the records until the rule
changes.
