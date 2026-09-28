+++
id = "REQ-RLO-018"
type = "requirement"
title = "Declare every delivery surface and outstanding handoff"
status = "approved"
owners = ["mmzen"]
created = "2026-09-28"
updated = "2026-09-28"
statement = "Before publication, the repository release procedure SHALL declare the disposition of every existing delivery surface and retain an owner and next action for each outstanding delivery item."
verification_method = ["test", "inspection"]
priority = "must"
source = "2026-09-28 marketplace audit and approved release-procedure correction plan"

[relations]
derives_from = ["CAP-RLO-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-28T19:38:37Z"
decided_by = "product-owner"
reason = "Human repository owner mmzen: \"I approve\", responding to the seven-artifact release-delivery package and required commit-bound verification request on 2026-09-28. Reviewed SHA-256 c793c7622ef3c4fd666d5e6d43f2def577a41a2c5d98df12ac8366a7f01b3ce4; transition input SHA-256 c793c7622ef3c4fd666d5e6d43f2def577a41a2c5d98df12ac8366a7f01b3ce4. Legacy evaluator role product-owner records the human decision; Codex applies it. Only the confirmed assurance fields and confirmation text were added to WO-RLO-011. Implementation is bounded by that work order; no external action is authorized."
+++

# Requirement: Declare every delivery surface and outstanding handoff

## In plain words

The plan says what will change, what can remain unchanged, and what is deferred.
Publishing the evaluator leaves later plugin work visible and owned.

## Why

The 0.19.0 evaluator publication did not update the public plugin marketplace.
The release sequence described the separate steps but had no overall closeout.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| A release is planned | Identify evaluator distribution, plugin marketplace, current documentation, demonstration and moving release markers; assign update, unchanged or deferred to each. | Missing surfaces or unexplained dispositions leave the plan incomplete. |
| A surface remains unchanged | Record its existing identity and the compatibility justification. | A missing justification cannot count as completion. |
| Work is deferred or awaits an earlier publication | Retain an owner, reason, governing work reference and next action or revisit trigger. | Unowned or untracked work prevents closeout. |
| Evaluator publication succeeds | Continue the declared plugin assembly, verification and separately authorized publication handoff. | Report remaining work; do not infer plugin delivery from evaluator success. |

## Examples

### Normal

**Given** plugin assembly needs the independently published evaluator wheel,
**when** evaluator publication finishes, **then** plugin work remains pending
with an owner and its next action. Evaluator publication need not wait for the
dependent plugin to exist.

### Failure

**Given** a plan omits the marketplace or labels it unchanged without a
compatibility justification, **when** it is checked, **then** the report names
the missing item and does not claim complete delivery.
