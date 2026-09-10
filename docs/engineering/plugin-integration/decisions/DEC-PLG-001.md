+++
id = "DEC-PLG-001"
type = "decision"
title = "Codex activation route"
status = "decided"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-10"

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

[disposition]
option = "prove-supported-route"
label = "Accept the documented route for combinations demonstrated by the Codex probe."
decided_by = "technical-owner"
decided_at = "2026-09-10T05:53:09Z"
reason = "Accept the tested Windows approach (Recommended)"

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-09-10T05:53:09Z"
decided_by = "technical-owner"
reason = "Accept the tested Windows approach (Recommended)"
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

The authoritative disposition, accountable actor and date are recorded in the metadata above.

The operator answered this question in the Codex task on 2026-09-10:

> DEC-PLG-001 — As technical owner, do you accept the Codex activation approach demonstrated on Codex CLI 0.153.4 on Windows, with other configurations and the remaining prerequisite cases still unqualified?

Their exact answer was:

> Accept the tested Windows approach (Recommended)

### Accepted scope and retained limits

The accepted route installs the plugin through a local marketplace and uses the native hook command reviewed through `/hooks`. The probe observed startup, resume, compaction, missing-runtime guidance, setup and repair, and a specific test-write refusal. The failed script-file and nested-command routes are excluded.

The demonstrated profile used **Codex CLI 0.153.4 on Windows**, provided Python **3.14.6** and released evaluator **0.16.0**. Other versions and platforms remain unqualified by this decision. Linux and macOS were unavailable during the host probe.

Codex C02 established guidance and stopping for an absent selected interpreter; it did not establish an agent-executed prerequisite check. Older or unusable Python variants were not observed. The probe's filesystem-observation limits also remain disclosed.

This accepts the demonstrated activation approach as the basis for implementation. The specific test-write refusal does not establish general production enforcement. Production adapters and their qualification remain separate work, with acceptance tied to observed configurations and behavior.

The [probe report](https://github.com/mmzen/se_harness/blob/a8c880a11e0cece6932695b7951cfa047a9f691c/docs/engineering/plugin-integration/evidence/WO-PLG-003/report.md) retains the exact observations, failures and limits. The later [verified record VREC-PLG-001](https://github.com/mmzen/se_harness/blob/main/docs/engineering/plugin-integration/verification-records/VREC-PLG-001.md) binds that probe candidate and its retained evidence.

Only an accepted supported route satisfies the production specification. A negative choice requires separate rejection or amendment of the affected definition and work.
Selecting an option does not change another artifact's state. Actual deferral uses the evaluator's deferred disposition, with scope and revisit conditions.
