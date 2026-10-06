+++
id = "REQ-HAG-013"
type = "requirement"
title = "Preserve test provenance and export reproducible records"
status = "draft"
owners = ["mmzen"]
created = "2026-10-06"
updated = "2026-10-06"
statement = "A selected hosted test snapshot can be exported with exact artifact and evidence bytes and the Git history needed to check its verification and release bindings."
verification_method = ["test", "demonstration"]
priority = "must"
source = "INT-HAG-002; DEC-HAG-004; mmzen: Git remains authoritative"

[relations]
derives_from = ["CAP-HAG-002"]
+++

# Preserve test provenance and export reproducible records

## In plain words

The operator can take the rehearsal records out of the graph, inspect their
history and check them with the same released evaluator.

## Why

The released evaluator binds verification to Git commits. A hosted baseline is
not a Git commit, and a test-projection commit is not the real product candidate.
The pilot must preserve these identities without inventing new evaluator policy.

## Behavior and acceptance

1. Every generated test VREC/RLS retains the unmodified released-evaluator
   binding to a real commit in a disposable test repository.
2. A manifest distinguishes the hosted input baseline, source fixture commit,
   test-projection commit and evaluator identity. No test result claims assurance
   for the real implementation candidate.
3. Export reconstructs selected record and evidence bytes and the referenced Git
   objects. An independent clean import/check reproduces the relevant states,
   relations, candidate bindings and gate outcomes.
4. Missing or corrupt evidence/history and an existing export destination cause
   explicit refusal; the operator's files are not overwritten.
5. The packaged walkthrough completes authoring through a test release decision,
   receipt recovery and export. Unperformed host checks remain unverified.

## Examples

**Normal:** An exported test VREC names commit P. The export contains P and its
required history. The released evaluator verifies that binding independently.

**Failure:** An export missing P is incomplete and cannot be reported as a
successful replay. The service does not replace P with a convenient current HEAD.
