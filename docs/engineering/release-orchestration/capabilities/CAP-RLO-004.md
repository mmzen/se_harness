+++
id = "CAP-RLO-004"
type = "capability"
title = "Track delivery across all release surfaces"
status = "approved"
owners = ["mmzen"]
created = "2026-09-28"
updated = "2026-09-28"
ability = "A release operator can identify outstanding delivery work across the evaluator, plugin marketplace and current documentation after any release stage."

[relations]
derives_from = ["INT-RLO-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-28T19:38:37Z"
decided_by = "product-owner"
reason = "Human repository owner mmzen: \"I approve\", responding to the seven-artifact release-delivery package and required commit-bound verification request on 2026-09-28. Reviewed SHA-256 f4bdd5e9a19f9b1913336a3d8db6e801a083f2ce976c17bdf119bfddd007abf3; transition input SHA-256 f4bdd5e9a19f9b1913336a3d8db6e801a083f2ce976c17bdf119bfddd007abf3. Legacy evaluator role product-owner records the human decision; Codex applies it. Only the confirmed assurance fields and confirmation text were added to WO-RLO-011. Implementation is bounded by that work order; no external action is authorized."
+++

# Capability: Track delivery across all release surfaces

## In plain words

Publishing the evaluator does not also publish its host plugins or update
their installation instructions. A delivery surface is one place from which
users obtain the release or its current instructions.

## Actor and need

The release operator needs an explicit plan for each surface and an honest
completion report. The human release owner needs to see pending work,
responsible owners and evidence before declaring the delivery complete.

This extends repository-owned operational reporting across existing delivery
surfaces. It does not replace the approved publisher transaction or change
what an existing formal release record authorizes.

## Not decided here

- The plugin version for the next marketplace correction.
- The content of a particular release contract or its publication authority.
- Host credentials, provider-directory submissions or automatic publication.
- Formal artifact lifecycle rules and existing released records.
