# External actions

Verification, release and external delivery are distinct decisions in the
installed workflow. Before dispatching an external action that changes state,
match the actual supplied authority to the exact action, full candidate or
release identity, evidence digests, and repository/ref or registry destination.
Recheck the selected
procedure's current gates. A changed commit, evidence, action or destination
stops reuse of the earlier decision. Verification alone does not authorize a
merge; a released record alone does not authorize publication.

Agent merge or publication also requires demonstrated independent enforcement
for that action and destination. Inspect the available control evidence and
its coverage of the actual invocation path. A skill, hook configuration, actor
name, token or assertion that a control exists is not that demonstration.
If authority, a required gate or independent enforcement is missing, do not
dispatch that mutation. Name the missing condition as the automation blocker;
leave the action and lifecycle states unchanged. Read-only inspection retains
its existing host and network permissions; it does not require merge or
publication authority.

When the exact authority still applies, gates pass, and the required independent
control is demonstrated, use the project's existing authorized tool with its
original argument boundaries. Do not ask for the same approval again or invent
a harness merge/publication command. After invocation, retain actual results
and inspect the destination before retrying an uncertain effect. A fixture's
intercepted success demonstrates only that fixture, not production enforcement.
