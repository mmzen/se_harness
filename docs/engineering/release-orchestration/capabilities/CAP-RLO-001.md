+++
id = "CAP-RLO-001"
type = "capability"
title = "Complete an authorized release from one governed identity"
status = "approved"
owners = ["product-owner", "release-owner"]
created = "2026-08-18"
updated = "2026-08-18"

[relations]
derives_from = ["INT-RLO-001"]
+++

# Capability: Complete an authorized release from one governed identity

## Actor and need

A release owner needs to turn a released RLS already delivered to `main` into exact public GitHub, PyPI, and demonstration outcomes without manually reconstructing the governed release identity at each boundary.

## Capability statement

`A release owner can initiate, observe, and safely replay the complete SE Harness last mile by selecting one released release record, while protected environments retain their independent decisions.`

## Boundaries

- The capability begins only after the released RLS governance commit is present in `main`.
- It qualifies and materializes the already authorized candidate; it does not create or modify product intent, verification, release authority, source, or version.
- It is repository-specific automation for publishing SE Harness and is not installed into consumer repositories.
- PyPI environment approval and any required external configuration remain human-controlled.

## Outcomes

- The selected RLS uniquely resolves the candidate, version, tag, VREC, release contract, distribution hashes, and governance snapshot.
- Deterministic builds and independent controls fail before credentials when provenance or bytes disagree.
- GitHub Release, PyPI, and Pages either reach the exact declared state or retain an explicit diagnosable failure.
- A final machine-readable result and human summary connect all resulting URLs, hashes, commits, and checks.

## Candidate requirements

`REQ-RLO-001` through `REQ-RLO-008` define selection, distribution identity, qualification, GitHub publication, PyPI promotion, Pages deployment, replay behavior, and result observation.
