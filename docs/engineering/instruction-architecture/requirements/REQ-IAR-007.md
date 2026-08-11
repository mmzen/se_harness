+++
id = "REQ-IAR-007"
type = "requirement"
title = "Enforce readiness with an independent pinned CI checker"
status = "implemented"
owners = ["requirements-steward", "quality-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN a candidate change is evaluated in required CI, THE SYSTEM SHALL execute repository and work-order checks with an exactly pinned harness distribution that is independent from candidate-controlled checker files."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Enforce readiness with an independent pinned CI checker

## Acceptance criteria

- Pull-request CI installs an exact released harness version with an integrity pin, or invokes an action pinned to an immutable commit digest.
- In a target repository, the required check runs managed-file integrity, preflight for exactly one explicitly declared work-order ID, formal validation, and deterministic dashboard generation.
- The GitHub integration obtains the work-order ID from one structured pull-request field; missing, multiple, or malformed declarations fail rather than being inferred from branch names or source changes.
- Push CI without pull-request metadata performs repository-wide integrity, validation, and dashboard checks but does not claim work-order binding.
- Candidate-controlled repository scripts may still be exercised as product tests, but they are not the sole required enforcement mechanism.
- In the harness repository, the last released distribution enforces the prior baseline; unreleased checker behavior is verified by candidate tests and accountable review, then becomes independent only through a separate governed pin update after release.
- A passing structural check does not prove that the code diff is semantically within the declared work order; protected reviewers remain responsible for that judgment.
- The installer documents required status-check, CODEOWNERS, and branch-protection configuration without claiming it can set host governance automatically.
