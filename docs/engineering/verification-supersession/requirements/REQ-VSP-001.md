+++
id = "REQ-VSP-001"
type = "requirement"
title = "Permit an explicit ready-record supersession"
status = "implemented"
owners = ["quality-owner", "repository-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN an accountable assurance owner retires a ready verification record, THE SYSTEM SHALL accept an explicit transition from ready to superseded only when all supersession invariants hold."
verification_method = "automated-test-and-review"

[relations]
derives_from = ["CAP-VSP-001"]
+++

# Requirement: Permit an explicit ready-record supersession

## Rationale

An abandoned candidate must be closed without being falsely verified or deleted.

## Preconditions and trigger

A VREC is `ready`, a later authoritative VREC exists, and an accountable assurance owner explicitly authorizes retirement.

## Required response

Allow the old record to become `superseded` when its required successor relation and all validation rules pass. Retain both records.

## Failure and boundary behavior

Reject `draft`, `verified`, `released`, already `superseded`, or `rejected` sources in this iteration. Never infer or apply the transition from overlap, commit ancestry, age, or dashboard findings.

## Constraints

The lifecycle transition is a governance edit, not an automated capture side effect. No Git, tag, release, or publication mutation occurs.

## Acceptance examples

A human-authorized `ready -> superseded` transition with an eligible successor validates. Merely creating a newer verified VREC leaves the old record unchanged.

## Open decisions

None when approved.
