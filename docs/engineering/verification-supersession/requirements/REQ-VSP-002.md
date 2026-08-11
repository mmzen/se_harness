+++
id = "REQ-VSP-002"
type = "requirement"
title = "Require one typed eligible successor"
status = "implemented"
owners = ["quality-owner", "technical-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN a verification record has status superseded, THE SYSTEM SHALL require exactly one distinct verification record in its superseded_by relation and require that successor to be verified or released."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-VSP-001"]
+++

# Requirement: Require one typed eligible successor

## Rationale

A terminal status without a named authoritative successor leaves the lineage ambiguous.

## Preconditions and trigger

The validator encounters a VREC with status `superseded` or a `superseded_by` relation.

## Required response

Require a one-element, duplicate-free `superseded_by` array. The target must exist, be a different artifact of type `verification_record`, and have status `verified` or `released`.

## Failure and boundary behavior

Reject missing, empty, multi-target, duplicate, unknown, incorrectly typed, self-referential, ready, superseded, rejected, or draft targets. Reject `superseded_by` on a non-superseded VREC.

## Constraints

Successor eligibility is derived only from explicit formal metadata. Naming and paths carry no implied relationship.

## Acceptance examples

`VREC-AGR-001` may name `VREC-PMI-001` only after the latter is formally `verified` or `released`.

## Open decisions

None when approved.
