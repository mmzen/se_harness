# One execution route

This note describes the execution route adopted by this repository with
released SE Harness 0.18.0 under WO-HUP-019. The installed policy owner is
[DECISION_RIGHTS.md](../engineering/DECISION_RIGHTS.md#approved-execution),
and the procedure is [WORKFLOW.md](../engineering/WORKFLOW.md#approved-execution).
Other repositories follow their own installed release until an authorized upgrade.
The filename is retained for existing links; no delegation class or root
`.engineering-harness.delegation.toml` setting is needed for this route.

Approve the work once. Its selected executor then starts, implements, tests,
records completion and prepares required verification within the approved scope.
A person and an agent use the same commands. No route setting, separate
delegation table, preliminary merge or live CI response authorizes local work.
No second agent is required.

The owner still accepts or rejects the result. Scope changes and external
delivery need their actual authority; reuse a decision already supplied for the
same action. A failed local check is repaired within scope, not bypassed through
an owner execution route. Work classified `not_required` needs no new VREC.

Historical delegation fields and events keep their original meaning. Existing
execution grants remain usable. Older approvals without that grant need an
explicit approval of remaining execution through the existing amendment process.
Do not rewrite historical evidence or add a legacy execution mode.

The existing CLI keeps `delegated-executor` as an example executor identity and
stable operation IDs for compatibility. They are not separate authorization
routes. Supply the actor actually performing the work.
