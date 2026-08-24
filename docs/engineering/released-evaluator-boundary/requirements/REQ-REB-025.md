+++
id = "REQ-REB-025"
type = "requirement"
title = "Record and verify both the entry path and the resolved interpreter"
status = "draft"
owners = ["requirements-steward", "quality-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN a runtime-identity observation accepts an external or installed interpreter, THE SYSTEM SHALL record the lexical entry path, whether that entry is a terminal link, the position class of the resolved interpreter relative to the declared environment root, and the resolved interpreter's content digest, and shall verify each recorded fact against independently derived expectations without changing the bound evaluator-evidence document."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-REB-001"]
+++

# Requirement: Record and verify both the entry path and the resolved interpreter

## Rationale

Accepting the lexical entry path is necessary but not sufficient. The entry path says which environment was entered; it says nothing about which binary actually executed. A reviewer reading retained identity evidence for a POSIX run currently cannot tell whether `<env>/bin/python` was an ordinary file or a link, and cannot tell what it pointed at. The RCA states the obligation directly: identity checks must record and verify both the lexical path used to enter the environment and, where needed, the resolved binary.

The two facts also answer different questions. The entry path establishes the installed distribution, templates, and entry point that the environment supplies. The resolved binary establishes what code the interpreter itself is, which is what makes an alias or a redirected environment detectable after the fact rather than only at the moment of the check.

## Preconditions and trigger

The trigger is the construction of any runtime-identity observation for the `released-evaluator`, `candidate-source`, or `candidate-package` role, and the construction of any repository-owned identity evidence that reports an interpreter.

## Required response

- The runtime-identity observation shall continue to report the lexical entry path as its interpreter path.
- It shall additionally report whether the entry path is a terminal link.
- It shall additionally report the position of the resolved interpreter as a bounded class: inside the declared environment root, or outside every declared root. It shall not report the resolved interpreter's absolute path.
- It shall additionally report the SHA-256 digest of the resolved interpreter's bytes.
- Each added fact shall be verified rather than merely reported: a boundary that expects a specific environment shall confirm the entry path lexically, confirm the recorded terminal-link property against its own observation of the path, confirm the recorded position class, and confirm the digest against a digest it computes itself.
- Where a boundary already reads the resolved interpreter's bytes for its own evidence, it shall use the same digest definition so that the two records are comparable.

## Compatibility and evidence boundary

The canonical `se-harness-evaluator-evidence-v1` document shall not change. Its `origins` and `environment` objects are closed sets enforced by the installed root validator, and every existing bound `*-evaluator.json` sidecar is hash-bound through the `evaluator-evidence` class in `se_harness/hash_bound_classes.json`. Adding a field to either object would invalidate every existing binding and would be rejected by an immutable root check.

For the same reason the runtime-identity schema identifier shall remain `se-harness-runtime-identity-v3`. The installed root validator and the dashboard publisher accept only `se-harness-runtime-identity-v2` and `se-harness-runtime-identity-v3`, so a fourth schema identifier could not be recorded in a preparation-view binding until a later governed adoption. The addition shall therefore be strictly additive within the existing identifier, and every consumer that validates a required field subset shall continue to accept the observation unchanged.

Introducing a distinct schema identifier for the enlarged observation is deferred to a later governed change that also adopts the corresponding root evaluator.

## Failure and boundary behavior

- A recorded fact that a boundary cannot independently confirm is a refusal, not an omission. Absent facts shall not be treated as satisfied.
- A digest mismatch, a terminal-link mismatch, or a position-class mismatch shall stop the boundary before substantive target validation.
- An interpreter whose bytes cannot be read shall be refused rather than recorded with a null digest.
- Retained identity output shall contain no absolute workstation path for the resolved interpreter, no unrelated environment content, and no credential material.
- Recording these facts grants no authority. Identity output remains evidence only.

## Constraints

- Digest computation shall be bounded and shall not follow a further link from the resolved target.
- Added fields shall be deterministic for an immutable environment so that repeated observations of the same environment produce identical decision-bearing output.

## Acceptance examples

### Example: normal behavior

**Given** a POSIX evaluator environment whose `bin/python` is a terminal link to a system interpreter

**When** the released-evaluator identity observation is produced

**Then** it reports the lexical `<env>/bin/python` path, a true terminal-link property, an outside-every-declared-root position class for the resolved interpreter, and the resolved interpreter's SHA-256 digest, and the calling boundary confirms all four against its own observations.

### Example: failure behavior

**Given** the same environment where the interpreter link is repointed at a different binary between the boundary's own observation and the identity observation

**When** the boundary compares the reported digest with the digest it computed

**Then** the comparison fails, the boundary stops before validating any target, and no passing identity proof is retained.

### Example: unchanged sidecar

**Given** an existing bound `*-evaluator.json` evidence file and its recorded digest

**When** the enlarged runtime-identity observation is used to produce evaluator evidence

**Then** the sidecar's fields and canonical bytes are unchanged and its recorded digest still matches.
