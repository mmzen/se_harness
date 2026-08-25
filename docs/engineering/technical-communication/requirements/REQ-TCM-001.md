+++
id = "REQ-TCM-001"
type = "requirement"
title = "Distribute one managed ASD-STE100-based communication policy"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN SE Harness installs, upgrades, or routes a supported coding agent, THE SYSTEM SHALL provide one integrity-protected technical-communication policy that applies selected ASD-STE100-based clarity principles to eligible English prose, explicitly disclaims compliance or ASD endorsement, and requires no download or bundled copy of the external standard."
verification_method = "automated-test-and-manual-review"

[relations]
derives_from = ["CAP-TCM-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T07:53:59Z"
decided_by = "requirements-steward"
+++

# Requirement: Distribute one managed ASD-STE100-based communication policy

## Rationale

The rules affect ordinary operator responses and several current or future
skills. Putting them only in a skill, prompt, adapter, or note would create
activation gaps and competing owners. The policy must be managed and portable,
but it must not imply that the product reproduces or certifies the standard.

## Preconditions and trigger

- A standard repository is installed or upgraded, or a supported agent follows
  the installed managed router.
- Output contains agent-authored English prose eligible under the policy.
- The installed policy is available; network access is not a precondition.

## Required response

- Provide the canonical source at
  `templates/repository/standard/docs/engineering/TECHNICAL_COMMUNICATION.md`.
- Install it as managed content at
  `docs/engineering/TECHNICAL_COMMUNICATION.md` and bind its normalized digest
  in the managed lock.
- Route it from `ENGINEERING_HARNESS.md` without copying detailed rules into the
  router, `AGENTS.md`, a skill, an adapter, or a note.
- Include it in the required managed-policy reading manifest and integrity checks.
- State that it is ASD-STE100-based or follows selected ASD-STE100 principles,
  not that it is compliant, certified, approved, or endorsed.
- State that agents must not download, search for, bundle, reproduce, or parse
  the standard or its controlled dictionary.
- Treat an ASD-STE100 issue reference as design provenance only. Installed
  repository policy remains the complete runtime instruction source.

## Failure and boundary behavior

- A missing, damaged, customized, ambiguous, or identity-mismatched policy fails
  through existing integrity and upgrade behavior.
- The agent does not retrieve the external standard as recovery.
- If the policy cannot be read reliably, a communication skill stops before it
  presents a result as policy-governed.
- Conflicting skill or adapter prose is non-authoritative and cannot override it.

## Constraints

- The policy introduces no lifecycle state, decision right, gate, or relation.
- The self-hosting root managed copy remains bound to its exact installed
  released evaluator. Candidate work changes the canonical template and
  installation behavior instead of overwriting that root copy directly.
- No logo, complete rule catalog, controlled dictionary, or copied standard
  content is included.
- Updating selected principles requires governed policy work; an external page
  change cannot silently change installed behavior.

## Acceptance examples

### Example: standard installation

**Given** a new standard repository installation

**When** the installer applies managed content

**Then** the policy is installed once, lock-bound, routed, and available without
network access.

### Example: policy is missing

**Given** an installed repository whose lock requires the policy

**When** the policy file is removed

**Then** integrity and preflight report the exact missing path, and the agent does
not download the standard as recovery.

### Example: unsupported claim

**Given** public or installed product text

**When** the capability is described

**Then** it contains no claim of ASD approval, certification, endorsement, or
strict ASD-STE100 compliance.

## Open decisions

Before approval, the product and technical owners must accept the canonical
path, managed ownership, route, no-download boundary, and permitted public claim
defined by `SPEC-TCM-001`.
