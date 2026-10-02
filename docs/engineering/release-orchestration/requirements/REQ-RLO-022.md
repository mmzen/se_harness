+++
id = "REQ-RLO-022"
type = "requirement"
title = "Prepare every release deliverable before approval"
status = "approved"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
statement = "The complete-release route SHALL complete required preparation and human verification before release approval and SHALL publish only the approved payloads after checking public evaluator identity."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "2026-10-02 owner-approved complete-release proposal"

[relations]
derives_from = ["CAP-RLO-005"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T20:17:28Z"
decided_by = "mmzen"
reason = "Human repository owner mmzen answered \"Approve package, verification and review PR\" to the exact package review for WO-RLO-014/015/016 and their governing definitions, with required commit-bound verification under VER-RLO-011. This authorizes bounded implementation, local checks and commits, completion and verification preparation, ordinary review-branch push and draft PR from work/complete-release-approval to mmzen/se_harness:main, and its later verification-decision update. Human verification acceptance, merge, actual releases and the exact live configuration change remain separate. The selected released evaluator 0.21.0 governs this work. Reviewed draft SHA-256 de834769dda665532c833e2998fe34008067a17e7e133a45cbcfdd549309d0a4; approved transition input SHA-256 de834769dda665532c833e2998fe34008067a17e7e133a45cbcfdd549309d0a4. Only the confirmed WO assurance fields were added before this transition."
+++

# Prepare every release deliverable before approval

## Behavior

Before requesting complete-release approval, prepare the evaluator distributions,
plugin payloads, documentation changes and demonstration inputs. Complete required
checks and human verification for their exact source and payload identities.
Record any accepted limitations before the final approval request.

Plugin preparation must be possible from the retained verified evaluator candidate
without requiring the wheel to have been published. This preparation is local and
grants no permission to publish. After evaluator publication, independently fetch
the public wheel and compare its digest with the approved candidate before plugin
publication. A different wheel cannot be substituted or silently rebuilt.

The plan must distinguish known payload identities from post-publication receipts.
Final commit IDs that include a recorded release decision may be derived after
approval only by an explicit reviewed rule; their payload content may not change.

## Acceptance

A prepared candidate can qualify both host plugin packages before a public RLS
or public wheel exists. Missing verification or required credentials prevents a
ready claim. A public-wheel mismatch prevents marketplace publication. A ready
to released lifecycle event changes governance evidence without changing approved
plugin payloads or manufacturing a new assurance decision.
