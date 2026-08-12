+++
id = "REQ-DST-023"
type = "requirement"
title = "Provide realistic end-to-end harness examples"
status = "approved"
owners = ["product-owner", "documentation-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"
statement = "WHEN a 7/10 reader needs to apply SE Harness, THE SYSTEM SHALL provide realistic end-to-end examples that connect formal artifacts, authorized operations, retained evidence, exact commits, validation observations, accountable verification, and release decisions."
verification_method = "manual-walkthrough-and-command-inspection"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Provide realistic end-to-end harness examples

## Rationale

Abstract entity descriptions do not show how repository owners and coding agents use the harness across multiple commits and decisions. Existing examples mix a separate consumer repository's facts with this implementation repository and contain lifecycle ordering ambiguities.

## Required response

- Provide at least one concise end-to-end example from intent through requirement, specification, applicable architecture and ADR, work authorization, implementation, evidence, clean candidate commit, validation, verification record, and release decision.
- Use current `harnessctl` command forms and canonical repository paths.
- Distinguish commands normally run by a coding agent from approvals and decisions made by accountable humans.
- Show why the VREC and RLS live after the candidate while binding the same candidate commit.
- Identify example IDs, branches, commits, and external results as illustrative unless they are verifiable facts from this repository.
- Cross-reference the overview, model, phasing, and branching guides instead of duplicating their full explanations.

## Failure and boundary behavior

Examples must not present fictional identifiers as real repository state, imply that validation grants assurance, place a lifecycle transition after a commit that supposedly already contains it, or claim an external release that did not occur.

## Constraints

Examples may use a realistic fictional product change, but current SE Harness commands and semantics must be exact. No consumer repository is read or modified for this work.

## Acceptance examples

A reader can follow a complete example, identify which file or command appears in each phase, and explain which exact commit is verified and released and which actions require separate human authority.

## Open decisions

None when approved.
