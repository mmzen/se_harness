+++
id = "WO-PLG-032"
type = "work_order"
title = "Complete the generated evidence scope for plugin 0.2.2 verification"
status = "implemented"
owners = ["mmzen"]
created = "2026-09-29"
updated = "2026-09-29"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification by approving WO-PLG-032 and verification on the reviewed scope correction. Later marketplace publication relies on this binding."
decided_by = "mmzen"

[execution_scope]
paths = [
  "docs/engineering/release-0-20-0/work-orders/WO-PLG-032.md",
  "docs/engineering/release-0-20-0/evidence/WO-PLG-032/",
  "docs/engineering/release-0-20-0/verification-records/VREC-PLG-025.md",
  "docs/engineering/release-0-20-0/evidence/VREC-PLG-025-evaluator.json"
]

[relations]
implements = ["REQ-PLG-002", "REQ-RLO-018"]
specifications = ["SPEC-PLG-001", "SPEC-RLO-006"]
verification = ["VER-PLG-028"]
architecture = ["ARCH-PLG-001", "ADR-PLG-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-29T19:29:45Z"
decided_by = "engineering-owner"
reason = "Human mmzen: \"I approve work order and verification record\", responding to the opened WO-PLG-032 review and required commit-bound verification request. Reviewed draft SHA-256 33bc26e6a401656ddad9c37243ead13e6449a72fcfcd6fc549568b297399e154; approval input after recording the confirmed assurance classification SHA-256 26ea0081796c5cf020b6e5afe47e7a776d1f23c92425ef17a515006b0dd8124e. The approved scope includes the exact generated companion, bounded preparation and ordinary review-branch push/draft PR. Legacy engineering-owner transports the actual human decision; Codex applies it. VREC-PLG-025 did not yet exist, so verification acceptance and marketplace publication remain separate."
scope_paths = ["docs/engineering/release-0-20-0/work-orders/WO-PLG-032.md", "docs/engineering/release-0-20-0/evidence/WO-PLG-032/", "docs/engineering/release-0-20-0/verification-records/VREC-PLG-025.md", "docs/engineering/release-0-20-0/evidence/VREC-PLG-025-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-29T19:30:26Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Codex executes the unchanged mmzen-approved generated-evidence scope correction under passing start preflight."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-29T19:33:31Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed. Exact generated VREC destinations are within approved scope; record ID unused; independent assembly check and byte comparisons pass for all 63 distribution files and both installed package inventories. Evidence reuse and preparation review retained. Handoff passed. Required capture and human verification follow separately."
+++

# Complete the generated evidence scope

## Objective

Prepare the exact-commit verification record for the qualified plugin 0.2.2
without writing outside recorded execution scope. WO-PLG-030 already covers
qualification and its evidence. Its approved paths omit the evaluator companion
that capture-verification always creates beside the work-order evidence folders.
The retained scope result reports WEX201 / QGP-G4I-PATHS for that exact path.

## In scope

1. Check the retained WO-PLG-030 qualification, the unused VREC-PLG-025 identity,
   and the released evaluator's actual output paths.
2. Retain a bounded path and evidence review under evidence/WO-PLG-032/.
3. Run the required scope, review and handoff checks and record completion.
4. Prepare VREC-PLG-025 for WO-PLG-030 and this work order together, conforming
   to VER-PLG-028, at one clean qualification commit. Use the released capture
   command to write the named record and its evaluator companion.
5. Inspect the generated candidate, selected work orders, evidence digests,
   evaluator identity and ready state. Present the record for human verification.

## Confirmed assurance

Commit-bound verification is **required**, confirmed by human mmzen with
"I approve work order and verification record" in response to the opened
WO-PLG-032 review and required-verification request. The later publication
decision relies on this record and its evidence binding. VREC-PLG-025 did not
exist at that decision; no future assurance acceptance is inferred.

## Expected change surface

The only additional functional destination is
`docs/engineering/release-0-20-0/evidence/VREC-PLG-025-evaluator.json`.
The record path is already covered by WO-PLG-030; it is repeated here to make
this preparation scope explicit. This work order and its own evidence carry
review and lifecycle results. No historical evidence may be rewritten.

## Constraints and required verification

Use the repository's selected released 0.19.0 evaluator. Keep the qualified
plugin source, public wheel, 63-file assembly and prepared distribution commit
unchanged. The distribution commit is
`5662817f42994bd0dc9aabaa56891f9c298ab965`; its parent is
`86d75e56e28c0c34819c0079b41dc67075f58490`.

Apply VER-PLG-028. Reuse the retained native observations only after confirming
that package inputs and installed-byte inventories still match their qualified
identities. Run capture's required committed-candidate checks; assess the exact
candidate, complete evidence inputs and generated outputs. Preserve failures.
Use existing accepted definitions and architecture; this changes no design.

## Decision envelope

After human approval and start, Codex may perform this bounded preparation,
retain evidence, make local commits, record completion and prepare the required
VREC. Approval also confirms required commit-bound verification and permits the
existing 0.19.0 engineering-owner transport label, with mmzen and the actual
human decision retained in the transition reason.

Ordinary pushes to the already selected work/plugin-0-2-2 branch and its draft
PR to mmzen/se_harness main may include this correction and verification package.
No force push, merge, verification acceptance or marketplace publication is
included. Exact human verification and distribution publication remain separate.

## Out of scope and stops

No product code, test, hook, package, host configuration, root adoption, marker
or public marketplace change. Do not edit WO-PLG-030's approval or history.
Stop on a changed candidate/package identity, occupied VREC ID, another required
output path, failed check, changed accepted definition or missing authority.
The later public-route work and documentation remain WO-PLG-031's responsibility.

## Completion report

Report the actual scoped outputs, review/check results, unchanged package
identity, exact candidate and the evaluator's next accountable step. A ready
verification record is not a verified record or a publication authorization.
