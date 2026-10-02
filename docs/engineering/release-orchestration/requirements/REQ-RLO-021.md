+++
id = "REQ-RLO-021"
type = "requirement"
title = "Bind one approval to the complete release plan"
status = "approved"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
statement = "The complete-release route SHALL obtain one explicit human approval for the exact release record and reviewed delivery plan, and SHALL reuse it for matching actions and retries."
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
reason = "Human repository owner mmzen answered \"Approve package, verification and review PR\" to the exact package review for WO-RLO-014/015/016 and their governing definitions, with required commit-bound verification under VER-RLO-011. This authorizes bounded implementation, local checks and commits, completion and verification preparation, ordinary review-branch push and draft PR from work/complete-release-approval to mmzen/se_harness:main, and its later verification-decision update. Human verification acceptance, merge, actual releases and the exact live configuration change remain separate. The selected released evaluator 0.21.0 governs this work. Reviewed draft SHA-256 e260c16044bb3809aee69f738811b5ed27a5eeae07e564f8520f0a4f441a1305; approved transition input SHA-256 e260c16044bb3809aee69f738811b5ed27a5eeae07e564f8520f0a4f441a1305. Only the confirmed WO assurance fields were added before this transition."
+++

# Bind one approval to the complete release plan

## Behavior

For the complete-release route, present one human approval request covering the
exact release record and every required delivery action. Show the evaluator and
plugin versions, candidate and payload identities, destinations, required
release-only integration, verification results and known limitations. Link the
full plan and retain its complete byte digest with the decision.

The human response authorizes only that plan. Reuse it for matching actions,
including exact retries. Do not request a new permission just because the next
step uses another provider or resumes in another agent session.

A missing grant, changed candidate, changed scope or changed destination needs
a new human decision. A failed required check stops the affected action; another
approval alone cannot turn failure into success. A historical RLS approval that
did not cover delivery does not acquire this authority retrospectively.

## Acceptance

Given a verified complete package, one human response covers its listed delivery
actions and no second permission is requested for unchanged valid steps. Given
a changed plan or an old RLS-only decision, the next unmatched action is refused
and the missing authority is identified. Release state alone is never reported
as observed publication.
