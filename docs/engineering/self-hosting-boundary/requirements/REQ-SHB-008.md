+++
id = "REQ-SHB-008"
type = "requirement"
title = "Provide replayable independent candidate acceptance"
status = "approved"
owners = ["requirements-steward", "quality-owner", "security-owner", "release-owner"]
created = "2026-08-15"
updated = "2026-08-15"
statement = "WHEN candidate source or a candidate package is qualified for future release or governor use, THE SYSTEM SHALL execute a replayable functional acceptance contract with pinned identities, inputs, commands, outcomes, and output hashes that distinguishes candidate-produced evidence from released-governor assessment."
verification_method = "automated-test-and-human-review"

[relations]
derives_from = ["CAP-SHB-001"]
+++

# Requirement: Provide replayable independent candidate acceptance

## Rationale

Candidate source and package tests are necessary but can be changed by the same candidate they assess. A future governor needs a published, verifier-owned black-box contract that can be replayed against an exact candidate wheel without importing candidate source. Candidate checks remain useful evidence; they cannot become their own authority merely because they pass.

## Preconditions and trigger

- Candidate source is identified by one full Git commit.
- Candidate package is identified by the wheel built from that commit and its SHA-256.
- The released governor and its functional acceptance contract are identified independently from candidate metadata.

## Required response

- Run the complete source suite from the exact checkout and label its results candidate-source evidence.
- Install the exact candidate wheel into a fresh environment outside the checkout and exercise it only through its installed module or entry point.
- Execute verifier-owned black-box scenarios covering at least `init`, `adopt`, `doctor`, `validate`, `dashboard`, safe upgrade, customized-content refusal, corrupted-integrity refusal, consumer-workflow upgrade, protected self-hosting upgrade behavior, governor-reconciliation planning and refusal paths, runtime-origin isolation, deterministic output, and authority denial.
- Emit a bounded machine-readable manifest containing governor identity, test-contract identity, candidate commit, wheel digest, Python identity, scenario identifiers, commands or stable command identifiers, outcomes, and deterministic output hashes.
- Make the same retained inputs sufficient for an accountable reviewer to rerun the acceptance contract without relying on mutable network state or an editable candidate checkout.
- Require every non-optional scenario to pass; omission or skip is not success.

## Failure and boundary behavior

- Candidate source cannot supply the only acceptance oracle for candidate package qualification.
- Candidate package acceptance fails on checkout import fallback, editable metadata, inherited candidate `PYTHONPATH`, unexpected entry point, version-only identity, missing test-contract identity, nondeterministic canonical output, or incomplete scenario execution.
- The candidate wheel need not contain its own test source. The released governor or a separately checksum-pinned verifier artifact owns the authoritative black-box contract.
- Candidate evidence never transitions a VREC, releases an RLS, publishes a package, or promotes a governor.

## Constraints

- Preserve Python 3.11+ and standard-library runtime compatibility for shipped harness behavior.
- Keep secrets, tokens, full environment dumps, and repository file bodies out of the replay manifest.
- Bound paths and diagnostics and normalize platform-dependent evidence where exact equality is claimed.
- A newly implemented acceptance runner becomes independently authoritative only after it is published and separately promoted as governor; it cannot retroactively govern its own creation.

## Acceptance examples

### Example: replay the candidate wheel

**Given** a released governor, its acceptance-contract digest, an exact candidate wheel, and the candidate commit,

**When** the contract runs twice in fresh environments,

**Then** required scenarios pass, runtime origins remain isolated, and the canonical evidence manifests agree.

### Example: candidate weakens its own tests

**Given** candidate source removes a candidate-owned failure scenario,

**When** the released governor applies its independently published black-box contract,

**Then** the required scenario still runs and the candidate cannot convert its omission into success.

## Open decisions

The exact module and command names for the runner and the canonical evidence schema are delegated to the specification and implementation. The authority boundary and required scenario categories are not delegated.
