+++
id = "DEC-PLG-001"
type = "decision"
title = "Codex activation route"
status = "open"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"

kind = "question"
question = "Does the documented shell-guard activation route satisfy the contract on the assessed Codex versions and platforms?"
raised_by = "implementation-planner"
recommendation = "prove-supported-route"

[[options]]
id = "prove-supported-route"
label = "Accept the documented route for combinations demonstrated by the Codex probe."

[[options]]
id = "exclude-codex"
label = "Decline Codex support if no supported route meets the contract."

[relations]
concerns = ["WO-PLG-003", "WO-PLG-005", "SPEC-PLG-005"]
blocks = ["SPEC-PLG-005"]
+++

# Decision: Codex activation route

## Question

Does the documented shell-guard activation route satisfy the contract on the assessed Codex versions and platforms?

The documented route registers a shell hook command before the private interpreter exists. It reports setup required if the interpreter cannot run; otherwise the Python handler checks identity and readiness. The probe tests this route, including hook trust and Windows quoting. No cache editing or pre-install callback is needed.

## Options

**prove-supported-route.** Accept the documented route for combinations demonstrated by the Codex probe.

**exclude-codex.** Decline Codex support if no supported route meets the contract. This supplies no production activation route.

## Recommendation

WO-PLG-003 may record a supported sequence or an incompatibility. Its evidence must name host version, setup access, registration, trust, reload, and observed events.

## Disposition

Pending. Only the evaluator records a disposition after the accountable owner's explicit decision.

Only an accepted supported route satisfies the production specification. A negative choice requires separate rejection or amendment of the affected definition and work.
Selecting an option does not change another artifact's state. Actual deferral uses the evaluator's deferred disposition, with scope and revisit conditions.
