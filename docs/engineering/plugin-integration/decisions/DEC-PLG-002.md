+++
id = "DEC-PLG-002"
type = "decision"
title = "Claude Code activation route"
status = "open"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"

kind = "question"
question = "Does the documented shell-guard activation route satisfy the contract on the assessed Claude Code versions and platforms?"
raised_by = "implementation-planner"
recommendation = "prove-supported-route"

[[options]]
id = "prove-supported-route"
label = "Accept the documented route for combinations demonstrated by the Claude Code probe."

[[options]]
id = "exclude-claude"
label = "Decline Claude Code support if no supported route meets the contract."

[relations]
concerns = ["WO-PLG-004", "WO-PLG-006", "SPEC-PLG-006"]
blocks = ["SPEC-PLG-006"]
+++

# Decision: Claude Code activation route

## Question

Does the documented shell-guard activation route satisfy the contract on the assessed Claude Code versions and platforms?

A shell hook command can report setup required before the environment exists, then invoke the Python readiness handler after setup. The probe tests that documented route, including persistent data, reload, and Windows quoting. Dependency installation remains an authorized setup operation.

## Options

**prove-supported-route.** Accept the documented route for combinations demonstrated by the Claude Code probe.

**exclude-claude.** Decline Claude Code support if no supported route meets the contract. This supplies no production activation route.

## Recommendation

WO-PLG-004 supplies observations for the actual host. A manifest that parses does not resolve activation or demonstrate full context delivery.

## Disposition

Pending. Only the evaluator records a disposition after the accountable owner's explicit decision.

Only an accepted supported route satisfies the production specification. A negative choice requires separate rejection or amendment of the affected definition and work.
Selecting an option does not change another artifact's state. Actual deferral uses the evaluator's deferred disposition, with scope and revisit conditions.
