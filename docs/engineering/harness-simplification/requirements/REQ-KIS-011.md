+++
id = "REQ-KIS-011"
type = "requirement"
title = "Make verification requests understandable"
status = "approved"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
statement = "When implementation is ready for human verification, the agent shall present a concise request that explains the delivered result, supporting evidence, material gaps, and the exact decision being requested."
verification_method = ["inspection", "demonstration", "test"]
priority = "must"
source = "CAP-KIS-001; mmzen accepted the verification-request proposal with 'Ok go' on 2026-10-02"

[relations]
derives_from = ["CAP-KIS-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T14:21:23Z"
decided_by = "mmzen"
reason = "mmzen explicitly approved REQ-KIS-011, SPEC-KIS-005, VER-KIS-005 and WO-KIS-012 with \"Approve implementation and required verification\". Reviewed SHA-256: 0d1833ba03db58f0d9fa21fcf5d9cbb2990fb791577edc9fa7530f5d7c01aace. This authorizes the two instruction edits, local checks, commits, completion and preparation of required commit-bound verification under VER-KIS-005. WO assurance metadata records that actual decision. Human acceptance and push/PR remain separate."
+++

# Make verification requests understandable

## In plain words

The human can understand what was delivered, how it was checked, what remains
uncertain, and what accepting the result means. The exact verification record
and candidate remain available in the review details.

## Why

The implementation-approval request now uses a concise decision card.
Verification requests need the same clarity at the existing human decision.
A list of test counts, artifact IDs and commit hashes does not by itself show
whether the agreed outcome was achieved.

## Acceptance

1. The request leads with the delivered outcome. It summarizes results against
   the agreed requirements and links the evidence. Test counts support that
   explanation; they do not replace it.
2. Material failures, skipped or unavailable checks, unassessed criteria and
   residual uncertainty are visible. A blocked decision is reported as blocked.
   The request never treats an evidence gap as a pass or a risk as accepted
   without its actual decision.
3. The request explains that verification accepts the selected candidate
   against the agreed requirements. It identifies the exact verification
   record (VREC), full candidate commit, governing work orders and verification
   contracts in review details. Merge and release remain separate decisions.
4. The human may choose "Verify result" or "Request corrections" without
   typing IDs or commands. An unambiguous reply binds to the displayed record,
   candidate and evidence. Changed inputs require reassessment before reuse.
5. A request for corrections is not a terminal rejection or authority to begin
   new implementation. Existing correction, rejection and supersession
   procedures remain available.
6. The guidance appears in the existing verification-decision procedure.
   Implementation completion points to it after required preparation.
   No extra approval stage or startup instruction load is introduced.

## Limits

This changes agent instructions. It adds no artifact type, command, gate,
lifecycle transition, decision right, renderer, approval service or scoring
framework. It does not change evidence capture or required checks.
Existing approved definitions remain unchanged.
