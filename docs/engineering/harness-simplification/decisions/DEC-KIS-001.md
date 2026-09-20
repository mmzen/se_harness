+++
id = "DEC-KIS-001"
type = "decision"
title = "Choose a feasible repository review guarantee"
status = "decided"
owners = ["engineering-owner"]
created = "2026-09-19"
updated = "2026-09-20"

kind = "question"
question = "Should the recovery use explicit owner-controlled acceptance or require a separate qualified human reviewer for integration and publication?"
raised_by = "artifact-author"
recommendation = "owner-review"

[[options]]
id = "owner-review"
label = "Keep explicit owner acceptance with required tests and honestly stated administrative bypasses; do not claim independent review."

[[options]]
id = "independent-review"
label = "Require a real qualified reviewer separate from the author or initiator and configure current-review and publishing controls accordingly."

[relations]
concerns = ["REQ-KIS-012", "SPEC-KIS-006", "VER-KIS-006", "WO-KIS-012"]
blocks = ["WO-KIS-012"]

[disposition]
option = "owner-review"
label = "Keep explicit owner acceptance with required tests and honestly stated administrative bypasses; do not claim independent review."
decided_by = "engineering-owner"
decided_at = "2026-09-20T06:26:25Z"
reason = "Owner review (recommended): you accept the result; no claim of independent review."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-09-20T06:26:25Z"
decided_by = "engineering-owner"
reason = "Owner review (recommended): you accept the result; no claim of independent review."
+++

# Choose a feasible repository review guarantee

## Question and facts

The recovery plan offers owner review when only one human is available and
independent review when a second qualified person exists. These are different
guarantees. INT-KIS-001 describes a one-user project; current reviewer availability
has not been confirmed. A human GitHub account cannot provide an independent
approval of its own authored PR. Do not solve that limit with a second identity
for the same person or with an unexplained administrative bypass.

## Options

**owner-review:** keep required acceptance tests and an explicit owner decision
for the exact candidate. Record any owner bypass and control-change review
limits. This serves the existing one-owner context without a new service, but
does not establish independent approval or protection against that owner.

**independent-review:** name a real second qualified person and the roles they
may exercise. Require their current review at integration and the applicable
publication boundary. This adds a staffing and coordination dependency; if
the person or supported host control is unavailable, the affected action waits.

## Recommendation and effect

Prefer owner-review for the existing one-user context unless the owner now needs
and can staff independent assurance. The engineering owner resolves this WO
policy choice in agreement with the repository/release owners responsible for
later external actions. Selection does not grant those external action rights.

The open decision blocks WO-KIS-012. Its related definitions remain drafts
and describe both choices without selecting one. It does not block
WO-KIS-010, WO-KIS-011 or their definition review. Only the protection-dependent
portion of WO-KIS-013 waits for the chosen wording.

No disposition has been recorded. Use the released decide command only after
the actual owner chooses an option. Do not edit disposition or lifecycle history.
