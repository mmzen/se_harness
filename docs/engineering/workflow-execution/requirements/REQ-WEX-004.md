+++
id = "REQ-WEX-004"
type = "requirement"
title = "Separate preparation provenance from decision metadata"
status = "approved"
owners = ["requirements-steward", "quality-owner"]
created = "2026-08-20"
updated = "2026-08-20"
statement = "WHEN a ready verification or release record is prepared or later decided, THE SYSTEM SHALL record preparation provenance separately from accountable decision provenance and shall not populate verification, release, rejection, or supersession decision actors or times before the corresponding accountable decision occurs."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-WEX-001"]
+++

# Requirement: Separate preparation provenance from decision metadata

## Rationale

A prepared proposal and an accountable decision are different events performed under different authority. Premature decision fields make a ready record look partly verified or released and prevent reliable audit of who decided what and when.

## Preconditions and trigger

## Required response

## Failure and boundary behavior

## Constraints

## Acceptance examples

### Example: normal behavior

**Given** a valid implemented candidate and authorized verification-record preparation

**When** the ready VREC is written

**Then** it records preparation provenance and contains no verification decision actor or verification decision time.

### Example: failure behavior

## Open decisions

The specification must define the canonical preparation and decision fields plus legacy-read behavior before this requirement is approved for implementation.
The system prepares a new ready VREC or RLS, or applies an explicit accountable decision to an existing eligible record.
- On preparation, record the preparation actor and time using fields whose meaning does not claim the later decision.
- On verification, release, rejection, or supersession, record the applicable accountable actor and UTC decision time as part of the same atomic transition.
- Preserve the captured candidate identity, work coverage, evidence identity, and other immutable provenance throughout later decisions.
- Reject ready record content that pre-populates a later decision actor or decision time.
- Reject a decision transition without the applicable accountable actor and a valid decision time.
- Do not rewrite legacy records solely to adopt the new provenance distinction.
- Field names and compatibility treatment are specified downstream; their semantics must remain unambiguous.
- Automation may capture the identity supplied by an authorized actor but may not claim that actor made a decision merely because preparation was requested.
**Given** that ready VREC and an explicit assurance-owner verification decision

**When** the verification transition is applied

**Then** the VREC atomically records verified state, assurance-owner identity, and verification time while retaining its preparation and candidate provenance.
