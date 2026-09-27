+++
id = "DEC-IAR-001"
type = "decision"
title = "Adopt a successor instruction contract without rewriting accepted history"
status = "decided"
owners = ["repository-owner", "technical-owner", "engineering-owner"]
created = "2026-09-20"
updated = "2026-09-27"
kind = "question"
question = "Can the new instruction package govern a future released contract through an explicit versioned applicability boundary while preserving the conflicting accepted definitions?"
raised_by = "Codex drafting agent"
recommendation = "versioned-successor"

[[options]]
id = "versioned-successor"
label = "Approve a versioned future contract and separate adoption, preserving accepted history and explicit rule applicability."

[[options]]
id = "await-revision-capability"
label = "Keep this package in draft until a separately governed linked-revision capability can activate the replacement."

[relations]
concerns = ["SPEC-IAR-014", "WO-IAR-013", "WO-IAR-014", "WO-IAR-015", "CAP-IAR-001", "REQ-IAR-001", "REQ-IAR-003", "REQ-IAR-008", "REQ-IAR-019", "REQ-IAR-020", "REQ-IAR-021", "SPEC-IAR-001", "SPEC-IAR-012", "SPEC-IAR-013", "REQ-ADS-003", "REQ-ADS-007", "REQ-PLG-010", "REQ-PLG-011"]
blocks = ["WO-IAR-013", "WO-IAR-014", "WO-IAR-015"]

[disposition]
option = "versioned-successor"
label = "Approve a versioned future contract and separate adoption, preserving accepted history and explicit rule applicability."
decided_by = "engineering-owner"
decided_at = "2026-09-27T07:33:54Z"
reason = "ok for option 1"

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-09-27T07:33:54Z"
decided_by = "engineering-owner"
reason = "ok for option 1"
+++

# Adopt a successor instruction contract without rewriting accepted history

## Question and facts

The owner has selected the new entry and file split. The remaining question is
how the new formal package displaces conflicting accepted obligations at adoption.
CAP-IAR-001 and REQ-IAR-001 require the AGENTS gate. REQ-IAR-003/008, REQ-IAR-019
through REQ-IAR-021, SPEC-IAR-001/012/013 and REQ-ADS-003/007 contain affected
ownership or reading obligations. REQ-PLG-010/011 are affected by entry delivery;
current plugin sources explicitly say there are no automatic hooks.

The new drafts preserve those records. The selected 0.18.0 evaluator has no
generic linked accepted-definition revision command. New draft IDs alone do
not amend old authority. The complete old-rule disposition map must be reviewed
before applying a conflicting new contract.

## Options

**versioned-successor:** Accept this package as the candidate contract for a
future release, with an explicit old-rule/new-rule applicability map and a
separate released adoption work order. Preserve all accepted records and their
historical meanings. Confirm that this versioned boundary is valid under the
current governance procedure before implementation approval. Do not invent a
supersedes relation or claim the old artifacts were amended by this record.

**await-revision-capability:** Keep this package in draft until an independently
governed linked-revision capability can express and activate the replacement.
This preserves the selected revision objective but delays instruction delivery.

## Recommendation

Use versioned-successor if the accountable human confirms its applicability
under the installed governance rules. It separates candidate implementation from
release/adoption and avoids bundling a generic lifecycle revision feature into
an instruction-discovery change. Otherwise use await-revision-capability.

## Required decision record

The human decision must name the chosen option, the accepted applicability
boundary and any affected formal definitions requiring further disposition.
The agent may apply that recorded decision with the supported decide command.
This draft neither supplies a disposition nor changes any artifact state.
