+++
id = "DEC-ECP-003"
type = "decision"
title = "Activation route for narrowed consumer-boundary definitions"
status = "decided"
owners = ["engineering-owner"]
created = "2026-10-17"
updated = "2026-10-17"
kind = "question"
question = "How will reviewed linked revisions of the accepted consumer-boundary definitions be recorded and activated before the narrowed WO-ECP-007 is approved?"
raised_by = "Codex"
recommendation = "review-bounded-amendment"

[[options]]
id = "review-bounded-amendment"
label = "Review exact linked revisions and obtain separate explicit authority for a bounded manual activation route."

[[options]]
id = "wait-supported-revision"
label = "Keep the work in draft until a released evaluator supports linked revision creation and activation."

[relations]
concerns = ["WO-ECP-007", "INT-ECP-001", "CAP-ECP-003", "REQ-ECP-012", "REQ-ECP-013", "SPEC-ECP-007", "VER-ECP-007", "ADR-ECP-005", "REQ-IAR-031"]
blocks = ["WO-ECP-007"]

[disposition]
option = "review-bounded-amendment"
label = "Review exact linked revisions and obtain separate explicit authority for a bounded manual activation route."
decided_by = "mmzen"
authority_owner = "engineering-owner"
decided_at = "2026-10-17T11:49:02Z"
reason = "mmzen explicitly approved the seven exact definition replacements and bounded manual activation, preserving accepted bytes, and WO-ECP-007 implementation with required verification and review publication. Reviewed activation plan SHA-256 5b9d646ceb8931b0049a10564bc6198ad5309ce412d0d6536923c8e77efcbde9; actual activation and original-byte links are retained in evidence/WO-ECP-007/definition-revisions/2026-10-17/activation.json. Doctor requires effective Git evidence attributes before passing. Earlier work and verification keep their original meaning; no verification or merge decision is supplied."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-10-17T11:49:02Z"
decided_by = "mmzen"
reason = "mmzen explicitly approved the seven exact definition replacements and bounded manual activation, preserving accepted bytes, and WO-ECP-007 implementation with required verification and review publication. Reviewed activation plan SHA-256 5b9d646ceb8931b0049a10564bc6198ad5309ce412d0d6536923c8e77efcbde9; actual activation and original-byte links are retained in evidence/WO-ECP-007/definition-revisions/2026-10-17/activation.json. Doctor requires effective Git evidence attributes before passing. Earlier work and verification keep their original meaning; no verification or merge decision is supplied."
+++

# Activation route for narrowed consumer-boundary definitions

## Facts

The human confirmed narrowing WO-ECP-007 on 2026-10-17. Its accepted definitions
still call for removals and legacy declarations that later work replaced.
The revised draft also needs a precise package-scan boundary and an installation
criterion consistent with minimal installation.

Evaluator 0.23.0's `docs/engineering/harness/AMEND_DEFINITIONS.md` requires a
linked revision preserving the accepted version, but supplies no supported
command or relation to create and activate it. A new draft cannot silently
replace an accepted definition.

The exact replacement proposals, accepted-file SHA-256 values and linked-work
effects are retained transiently outside the repository. On 2026-10-17, mmzen
answered "doctor: yes, go": keep effective Git evidence attributes as a
prerequisite for `doctor`, including before evidence exists. Explicit Git
integration or an equivalent owner rule satisfies that prerequisite. No accepted
file, lifecycle state or prior decision is changed by recording this clarification.

## Options and recommendation

**review-bounded-amendment:** review the confirmed installation behavior
and seek explicit authority for the exact preserved versions, revision
destinations, link representation and activation effects. This is the recommended
preparation route. Selecting it alone does not approve replacement text, invent
a relation, authorize a manual write or approve the work order.

The concrete proposal retains complete accepted bytes under
`evidence/WO-ECP-007/definition-revisions/2026-10-17/accepted/ID.txt`, applies the
exact reviewed replacements at their existing paths and records actual human
authority plus before/after hashes in `activation.json` in the same revision
directory. Each replacement links its preserved predecessor. Only future work
under WO-ECP-007 uses this revision; earlier work retains its original meaning
and evidence. This proposed manual exception still needs explicit human
authority. Evaluator 0.23.0 does not support linked revision activation.

**wait-supported-revision:** keep the work in draft until a released procedure can
record those effects. This avoids manual activation but leaves the product gap
unresolved in the meantime.

## Required outcome

Resolve this record with an authorized, reviewed activation route and definition
package, or an explicit decision to retain the draft. Keep accepted records and
historical evidence unchanged until that authority exists.

The record blocks only WO-ECP-007. Shared historical definitions do not stop
unrelated work. Scope narrowing is not definition approval, assurance confirmation,
implementation authority or publication authority. No disposition is applied.
