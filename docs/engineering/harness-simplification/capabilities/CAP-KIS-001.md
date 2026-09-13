+++
id = "CAP-KIS-001"
type = "capability"
title = "Carry out ordinary work with proportionate checks"
status = "approved"
owners = ["product-owner"]
created = "2026-09-13"
updated = "2026-09-13"

ability = "The owner and their coding agent can progress ordinary engineering work under explicit scope and checks proportionate to the action."

[relations]
derives_from = ["INT-KIS-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-13T16:40:43Z"
decided_by = "product-owner"
reason = "The owner accepted all 38 candidates in the retained 2026-09-13 codebase KISS review and requested the work orders: \"OK ! Let's create the work orders to implement all candidates\". Record the product-owner approval of CAP-KIS-001 within that accepted scope and the established delegated route. SPEC-KIS-001 makes the replacement contracts and seven retained protections explicit; the coverage map assigns all candidates. This records definition approval or bounded execution delegation only, not implementation start, completion, verification, release, merge, publication, live adoption or historical evidence deletion."
+++

# Carry out ordinary work with proportionate checks

## In plain words

The owner and their coding agent can do routine work, read the result and make the next decision with a small useful set of checks.

## Actor and need

One repository owner uses the harness and delegates bounded implementation to a coding agent.
They need understandable failures tied to the work being done and evidence they can review without repeating unrelated checks.

## Not decided here

- The exact replacement rules and acceptance checks are in the selected specification and verification contract.
- Actual assurance, release, publication and live installation remain separately accountable actions.
