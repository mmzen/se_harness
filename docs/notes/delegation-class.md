# One execution route

This note describes candidate behavior under SPEC-KIS-003. A repository follows
its installed release until an authorized upgrade; this source repository still
uses 0.17.0. The policy owner is the candidate
[DECISION_RIGHTS.md](../../templates/repository/standard/docs/engineering/DECISION_RIGHTS.md#approved-execution),
and the procedure is [WORKFLOW.md](../../templates/repository/standard/docs/engineering/WORKFLOW.md#approved-execution).

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
