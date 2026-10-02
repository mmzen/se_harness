+++
id = "ADR-RLO-006"
type = "adr"
title = "Extend the existing release flow for one approval"
status = "approved"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"

[relations]
decides = ["ARCH-RLO-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T20:17:28Z"
decided_by = "mmzen"
reason = "Human repository owner mmzen answered \"Approve package, verification and review PR\" to the exact package review for WO-RLO-014/015/016 and their governing definitions, with required commit-bound verification under VER-RLO-011. This authorizes bounded implementation, local checks and commits, completion and verification preparation, ordinary review-branch push and draft PR from work/complete-release-approval to mmzen/se_harness:main, and its later verification-decision update. Human verification acceptance, merge, actual releases and the exact live configuration change remain separate. The selected released evaluator 0.21.0 governs this work. Reviewed draft SHA-256 177e61ee2ea85ec7cb601b0c07cb35c582f699ca0470f42081570d6c441a119a; approved transition input SHA-256 177e61ee2ea85ec7cb601b0c07cb35c582f699ca0470f42081570d6c441a119a. Only the confirmed WO assurance fields were added before this transition."
+++

# Extend the existing release flow for one approval

## Context and drivers

The owner approved the direction of a complete release under one authorization.
The present plugin builder depends on an already public evaluator and the pypi
environment has its own required reviewer. Wording alone cannot remove these waits.

## Considered options

| Option | Consequences |
| --- | --- |
| Combine only the conversational requests | Small edit, but leaves later plugin assurance and platform approval; does not meet the agreed outcome. |
| Extend the current preparation and publisher | Adds staged qualification and bounded continuing authority; reuses existing lifecycle, workflow and completion evidence. |
| Add a separate release orchestration service | Adds deployment, credentials, state and recovery ownership without an agreed need. |

## Decision proposed for approval

Extend the current preparation and publisher. Prepare and verify immutable
deliverables first. Bind one explicit release decision to the frozen delivery
plan. Execute its listed actions under existing rights and required checks.
Make the pypi configuration change a separately reviewed one-time activation.

## Consequences

Keep candidate execution outside credential jobs. Keep exact public readback and
partial failure recovery. Preserve historical grants and the legacy route. The
staging path must separate payload identity from later governance receipts. The
existing plan, result and workflow tests need both new and legacy cases.

This file is a draft decision proposal, not an applied architecture approval.
