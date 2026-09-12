# Preparatory classification review

This is the author's review of proposed criteria, not independent assurance or a completed VER-PLG-019 result.
The expected boundaries derive from REQ-PLG-008/009/013/014, the original accepted local limitation, and the retained host observations.

| Scenario | Required classification | Proposed controlling clause |
| --- | --- | --- |
| Accepted profile; all healthy checks pass; native hook timeout permits an edit; exact evidence and standing deviation retained | May proceed to independent assessment for use with limitation; enforcement fails | VER-PLG-008 conditions 1-8; host C10 |
| Healthy evaluator failure receives late denial or leaves child processes | Ineligible for limited qualification | Host C09; shared condition 2; retained SPEC-PLG-008 rules 007/008 |
| Missing context, wrong evaluator identity, malformed action, or wrong work-order scope | Ineligible; limitation provides no waiver | Shared condition 2 and explicit non-waiver paragraph; host C01-C09 |
| Active asynchronous binding or inadequate production timeout | Ineligible even if a standalone check passes | Shared condition 3; host C12; host specification rule 009 |
| Host executes an unsafe experimental binding | Record actual effects; assessment still rejects the configuration | Shared condition 3; host C12; no claim that the host itself refused execution |
| No accepted standing deviation, or selected WO not concerned | Ineligible | Shared condition 5 |
| Different host/OS/Python/evaluator profile | Ineligible until separately accepted and evidenced | Shared condition 1 |
| Changed relevant source/package/loaded input without renewed assessment | Ineligible | Shared condition 7 |
| Codex literal OS shell-start failure remains unavailable | Permitted exclusion only in the limited claim after express assurance approval; no inferred behavior | VER-PLG-005 qualification classification; shared condition 6 |
| Any other required unavailable subcase, including unavailable Claude launch-failure evidence | Ineligible | Host-specific exhaustive exclusions; shared condition 6 |
| Missing/invalid output, disappeared binding, or earlier READY result | Actual refusal is unproven; retained failures cannot become passes | Host C11; shared condition 4; SPEC-PLG-008 rule 004 |
| Unsupported shell/MCP route, merge or remote action | No new support or authorization | Shared exclusions; SPEC-PLG-008 rule 012 |

Q01 is supported for preparation by scope/integrity checks, not by work authorization.
Q02/Q06/Q07 final applied-state observations await authorized application. Q03-Q05 above are logical counterexamples to review, not live-host reruns.
The source/package/loaded identities recorded in PRs #456/#457 are not the identity of a later combined candidate.
The accepted deviation does not alone establish requirement satisfaction or a qualified adapter.
