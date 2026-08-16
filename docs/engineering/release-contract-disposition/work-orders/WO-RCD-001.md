+++
id = "WO-RCD-001"
type = "work_order"
title = "Reject obsolete draft release proposals"
status = "implemented"
owners = ["repository-owner", "release-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
implements = ["REQ-RCD-001"]
specifications = ["SPEC-RCD-001"]
verification = ["VER-RCD-001"]
+++

# Work Order: Reject obsolete draft release proposals

## Authorization

After reviewing the exact aggregate release lineage and recommended disposition, the accountable repository owner instructed `ok go for rejection` on 2026-08-16. That decision approves this packet and authorizes the exact six transitions and documentation corrections defined by `SPEC-RCD-001`.

## In scope

- Verify the six proposals are unreferenced by RLS records and their complete gated work was released through the stated aggregate lineages.
- Transition exactly those proposals from `draft` to `rejected`.
- Add factual disposition notes and correct the six domain indexes.
- Retain deterministic evidence and stop at an uncommitted implemented state.

## Out of scope

Every release record, aggregate release contract, VREC, tag, release asset, operating contract, validator rule, inspection rule, software behavior, commit, push, pull request, verification transition, release, publication, and deployment.

## Architecture and decision applicability

No architecture or ADR applies. The work records lifecycle disposition and existing graph facts; it introduces no structural choice or architecturally significant requirement driver.

## Stop conditions

Stop if a selected proposal is not draft, an RLS satisfies it, its complete gated work is absent from the mapped released RLS, or disposition requires a new relation or lifecycle rule.

## Completion record

Implementation completed on 2026-08-16 within the authorized boundary. Exactly the six selected proposals are rejected, their domain indexes identify the authoritative aggregate release lineages, and historical release authority remains unchanged. Evidence is retained in `../evidence/WO-RCD-001-verification.md`. This implemented status records completed governance work only; it does not independently verify the candidate or authorize a commit, push, pull request, release, publication, or deployment.
