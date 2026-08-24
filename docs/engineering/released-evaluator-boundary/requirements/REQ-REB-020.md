+++
id = "REQ-REB-020"
type = "requirement"
title = "Bind release qualification to explicit evaluator roles"
status = "approved"
owners = ["requirements-steward", "repository-owner", "quality-owner", "release-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN a repository, candidate, candidate package, predecessor view, or public installation is qualified for release, THE SYSTEM SHALL expose a closed role-specific operation that binds the permitted evaluator, target, checks, and independence claim before execution."
verification_method = "automated-interface-and-adversarial-test"

[relations]
derives_from = ["CAP-REB-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T08:15:39Z"
decided_by = "requirements-steward"
+++

# Requirement: Bind release qualification to explicit evaluator roles

## Rationale

Issue #109 and RCA root cause `RC-060-09` identify a recurring class of release failure: individually valid low-level commands were applied to the wrong trust boundary. During release 0.6.0, the released 0.5 governor was pointed at the complete successor graph, the candidate doctor was pointed at a root still owned by 0.5, and a root validator was run inside a candidate archive. Command success or failure did not say which evaluator role had actually been exercised.

Release qualification must therefore express the intended role as part of the operation, not as an informal combination of executable paths, script paths, and workflow comments.

## Required response

The public CLI shall provide exactly these release-qualification operations:

- `released-root`: verify a repository root with the released evaluator that owns that root;
- `predecessor-view`: verify a deterministic successor-prepared view with the exact external predecessor evaluator declared by the transition contract;
- `complete-candidate`: verify the complete candidate graph with candidate code and label the result non-independent;
- `candidate-package`: let an exact released verifier assess a candidate distribution without importing candidate code into the verifier process;
- `public-install`: verify the identity and installed behavior of the exact publicly acquired distribution.

Each operation shall have a closed argument schema, fixed evaluator/target rules, fixed required checks, and a fixed independence classification. A caller shall not be able to select an arbitrary evaluator role with a free-form flag or combine the arguments of two roles.

Before substantive validation, every operation shall prove that its running evaluator and target satisfy the role contract. It shall fail closed on an absent, ambiguous, unsupported, or mismatched runtime, lock, predecessor declaration, commit, wheel digest, package identity, or target kind.

## Failure and boundary behavior

- A candidate evaluator cannot produce independent `released-root`, `predecessor-view`, or `candidate-package` evidence merely because it can execute the same validator.
- A released-root operation cannot validate a candidate archive or successor compatibility view as though that target were its owned root.
- A predecessor-view operation cannot import successor or candidate code into the predecessor interpreter.
- A complete-candidate result must remain explicitly candidate-controlled even when all checks pass.
- A public-install result cannot stand in for candidate acceptance, predecessor compatibility, or root governance.
- Low-level `doctor`, `validate`, `identity`, and validator-script entry points may remain available for diagnostics and general validation, but their output alone is not role-bound release-qualification evidence.
- No operation may grant lifecycle, assurance, release, publication, deployment, or root-upgrade authority.

## Constraints

- Qualification is read-only except for an explicitly named evidence output outside the inspected repository.
- The operations perform no network access, credential use, Git-ref mutation, package publication, or environment adoption.
- Evaluator provenance is established before repository-controlled Python is imported or executed.
- The root managed workflow and root evaluator remain controlled by the current lock until a separate adoption transaction.

## Acceptance examples

### Example: correct independent candidate-package qualification

**Given** an exact released verifier, a candidate wheel bound to a commit, and declared verifier/candidate digests

**When** `qualify candidate-package` runs

**Then** it verifies its own released identity first, assesses the candidate in isolation, and reports an independent pass or a deterministic failure.

### Example: candidate substitution

**Given** a workflow invokes candidate code while claiming the `candidate-package` role

**When** runtime identity is checked

**Then** qualification fails before candidate validation and cannot emit a passing independent result.
