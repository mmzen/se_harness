+++
id = "CAP-RLO-005"
type = "capability"
title = "Authorize complete release delivery once"
status = "approved"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
ability = "A human can authorize the exact complete release once and an agent can finish or resume its listed delivery actions under that decision."

[relations]
derives_from = ["INT-RLO-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T20:17:28Z"
decided_by = "mmzen"
reason = "Human repository owner mmzen answered \"Approve package, verification and review PR\" to the exact package review for WO-RLO-014/015/016 and their governing definitions, with required commit-bound verification under VER-RLO-011. This authorizes bounded implementation, local checks and commits, completion and verification preparation, ordinary review-branch push and draft PR from work/complete-release-approval to mmzen/se_harness:main, and its later verification-decision update. Human verification acceptance, merge, actual releases and the exact live configuration change remain separate. The selected released evaluator 0.21.0 governs this work. Reviewed draft SHA-256 1efd723f295e041c90059c97b8733013aa8d3bd86704dc6606f5dad3cdf02c82; approved transition input SHA-256 1efd723f295e041c90059c97b8733013aa8d3bd86704dc6606f5dad3cdf02c82. Only the confirmed WO assurance fields were added before this transition."
+++

# Authorize complete release delivery once

## Actor and need

The human release owner needs one clear approval request that names the complete
delivery. The executing agent needs a durable link to that decision at every
external step and after interruption.

## Capability

A human can approve the exact release candidate and its bounded delivery plan
in one response. The agent records the decision, carries out the listed actions,
checks their public results and resumes incomplete steps under the same authority.

## Conditions

Required verification and risk decisions are complete before this approval.
Versions, package identities, destinations, marker targets and recovery rules
are fixed or determined by a reviewed rule from immutable approved inputs.
Provider permissions support the declared route before it is offered as ready.

## Boundaries

The release decision and external effects remain separately recorded facts.
One response can supply their distinct rights; it cannot make a failed check
pass or prove publication. Historical decisions keep their original scope.
