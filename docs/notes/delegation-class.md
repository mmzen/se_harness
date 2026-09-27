# One execution route

This repository uses released SE Harness 0.19.0 under WO-HUP-021. The
installed policy owner is
[AUTHORITY.md](../engineering/harness/AUTHORITY.md#authority-from-work-approval),
and the procedure is [EXECUTE_WORK.md](../engineering/harness/EXECUTE_WORK.md#procedure).
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

## Approval identity correction

WO-KIS-016 corrects candidate grant checks to recognize the human identity in
the recorded approval event. The approver need not be named `engineering-owner`.
The executor's identity remains separate. Both identities are attribution;
neither proves authority by itself. The existing human decision, scope, gate
and legacy-grant requirements still apply. Role-labelled historical approvals
remain readable without rewriting them.

The installed 0.19.0 evaluator still requires the literal `engineering-owner`
for its execution-grant lookup. WO-HUP-022 exposed this mismatch. WO-KIS-016
uses the human-approved compatibility encoding, retaining the actual human in
the approval reason. Candidate tests do not upgrade the installed evaluator;
release and adoption are separate governed actions.
