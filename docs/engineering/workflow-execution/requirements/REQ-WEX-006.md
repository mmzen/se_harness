+++
id = "REQ-WEX-006"
type = "requirement"
title = "Validate lifecycle changes against a trusted base"
status = "rejected"
owners = ["requirements-steward", "quality-owner"]
created = "2026-08-20"
updated = "2026-08-20"
statement = "WHEN a candidate repository change is evaluated against a caller-selected trusted base revision, THE SYSTEM SHALL reject illegal lifecycle transitions, missing or premature decision metadata, forbidden coupled mutations, immutable provenance changes, and direct-edit bypasses of the active lifecycle contract."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-WEX-001"]
+++

# Requirement: Validate lifecycle changes against a trusted base

## Disposition

Rejected on 2026-08-20 by explicit product direction because trusted-base transition-diff enforcement is not needed in the current workflow-execution stage. `SPEC-WEX-001`, `VER-WEX-001`, and the first implementation packet must not specify, verify, or implement this obligation. A later initiative may propose it again through a new or explicitly revised requirement if direct-edit enforcement becomes necessary.

## Rationale

Safe transition commands are insufficient when an agent or contributor can directly edit formal files into a state that snapshot validation accepts. Enforcement must assess the transition represented by the candidate diff, not only the validity of its final snapshot.

## Preconditions and trigger

## Required response

## Failure and boundary behavior

## Constraints

## Acceptance examples

### Example: normal behavior

**Given** a trusted base containing a ready VREC and a candidate containing the same VREC as verified with complete accountable decision metadata

**When** the candidate diff is evaluated

**Then** the transition is accepted only if no immutable provenance or related artifact was changed and every verification-transition rule is satisfied.

### Example: failure behavior

## Open decisions

The specification must define trusted-base resolution inputs, protected fields by artifact type, permitted multi-artifact governance commits, and compatibility treatment before this requirement is approved for implementation.
The caller supplies a resolvable trusted base revision and candidate repository state through the governed validation or CI interface.
- Compare relevant formal artifact identities and protected fields between base and candidate states.
- Evaluate every lifecycle state change against the artifact-type transition contract.
- Detect coupled changes that an allowed selected transition could not produce.
- Detect changes to immutable commit, evidence, work coverage, snapshot, supersession, and decision provenance as applicable to the artifact type and lifecycle phase.
- Return deterministic findings that identify the artifact, old state, new state, and violated rule.
- Fail closed when the trusted base cannot be resolved or read without ambiguity.
- Reject a valid-looking final snapshot when its diff represents an illegal or bypassed transition.
- Do not infer approval or authority from a commit author, branch name, pull-request text outside the governed selector, or the presence of decision metadata alone.
- Base selection remains caller-controlled under repository and CI policy; the validator does not invent a trust anchor.
- Historical facts unchanged between base and candidate remain subject to snapshot compatibility rules rather than retroactive transition rejection.
- The diff evaluator is read-only and never repairs the candidate.
**Given** a trusted base containing an approved work order and a candidate that directly changes it to verified while also approving a VREC

**When** the candidate diff is evaluated

**Then** the system rejects the illegal or coupled transitions even if each candidate file is independently schema-valid.
