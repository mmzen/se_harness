+++
id = "REQ-RLO-023"
type = "requirement"
title = "Finish and resume every approved delivery step"
status = "approved"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
statement = "The repository complete-release route SHALL execute and reconcile every listed delivery action under the original approval and SHALL report complete only after every required public observation passes."
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
reason = "Human repository owner mmzen answered \"Approve package, verification and review PR\" to the exact package review for WO-RLO-014/015/016 and their governing definitions, with required commit-bound verification under VER-RLO-011. This authorizes bounded implementation, local checks and commits, completion and verification preparation, ordinary review-branch push and draft PR from work/complete-release-approval to mmzen/se_harness:main, and its later verification-decision update. Human verification acceptance, merge, actual releases and the exact live configuration change remain separate. The selected released evaluator 0.21.0 governs this work. Reviewed draft SHA-256 291490d95ee43565cdf7079156ca2048354cd0c174afed5fb35542f57fbf644c; approved transition input SHA-256 291490d95ee43565cdf7079156ca2048354cd0c174afed5fb35542f57fbf644c. Only the confirmed WO assurance fields were added before this transition."
+++

# Finish and resume every approved delivery step

## Behavior

The existing repository publication path must deliver all required outputs under
the approved complete-release plan. This includes GitHub release assets and the
version tag, PyPI, plugin marketplace, current documentation, demonstration pages,
maintenance-line reconciliation and the declared latest/last targets.

Run the required checks at each boundary. Inspect actual remote state before
retrying an uncertain write. Preserve successful stages and resume only missing
ones. Conflicting immutable bytes or unexpected mutable-ref movement stop the
affected step. Promote moving markers only after required delivery checks pass.

GitHub and registry controls must support this route without a second per-release
human approval. Configure that boundary in a separately reviewed one-time change;
do not bypass an existing required reviewer at execution time.

## Acceptance

A dry publication rehearsal covers all outputs, partial failure and exact replay.
One final report lists observed destinations and identities and is complete only
when all required outputs and observations pass. Any deferred or unavailable
required public check leaves delivery incomplete. A resumed run requests no new
authorization when the approved inputs and conditions still match.
