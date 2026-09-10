+++
id = "DEC-PLG-002"
type = "decision"
title = "Claude Code activation route"
status = "decided"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-10"

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

[disposition]
option = "prove-supported-route"
label = "Accept the documented route for combinations demonstrated by the Claude Code probe."
decided_by = "technical-owner"
decided_at = "2026-09-10T05:53:15Z"
reason = "Accept the tested Windows approach (Recommended)"

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-09-10T05:53:15Z"
decided_by = "technical-owner"
reason = "Accept the tested Windows approach (Recommended)"
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

The authoritative disposition, accountable actor and date are recorded in the metadata above.

The operator answered this question in the Codex task on 2026-09-10:

> DEC-PLG-002 — As technical owner, do you accept the Claude Code activation approach demonstrated on Claude Code 2.1.266 on Windows, with other configurations and the remaining prerequisite cases still unqualified?

Their exact answer was:

> Accept the tested Windows approach (Recommended)

### Accepted scope and retained limits

The accepted route uses the inline PowerShell command registered through the documented hook shell and command fields. The probe observed startup, resume, compaction, missing-runtime guidance, real setup and repair, and a specific test-write refusal. The script-file route refused by Windows execution policy is excluded.

The demonstrated profile used **Claude Code 2.1.266 on Windows**, provided Python **3.14.6** and released evaluator **0.16.0**. Other versions and platforms remain unqualified by this decision. Linux and macOS were unavailable during the host probe.

Claude Code C02 established missing-Python guidance through the real setup skill and tool. Older Python and unusable venv or ensurepip variants were not observed. The probe's filesystem-observation limits also remain disclosed.

This accepts the demonstrated activation approach as the basis for implementation. The specific test-write refusal does not establish general production enforcement. Production adapters and their qualification remain separate work, with acceptance tied to observed configurations and behavior.

The [probe report](https://github.com/mmzen/se_harness/blob/2f3073bebe607e6fb393fa55a1943c32d3f4b52f/docs/engineering/plugin-integration/evidence/WO-PLG-004/REPORT.md) retains the exact observations, failures and limits. The later [verified record VREC-PLG-002](https://github.com/mmzen/se_harness/blob/main/docs/engineering/plugin-integration/verification-records/VREC-PLG-002.md) binds that probe candidate and its retained evidence.

Only an accepted supported route satisfies the production specification. A negative choice requires separate rejection or amendment of the affected definition and work.
Selecting an option does not change another artifact's state. Actual deferral uses the evaluator's deferred disposition, with scope and revisit conditions.
