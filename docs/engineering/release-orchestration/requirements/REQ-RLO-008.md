+++
id = "REQ-RLO-008"
type = "requirement"
title = "Observe and attest the complete publication transaction"
status = "approved"
owners = ["quality-owner", "release-owner", "service-owner"]
created = "2026-08-18"
updated = "2026-08-18"
statement = "WHEN release orchestration completes or stops, THE SYSTEM SHALL retain a machine-readable result and human summary that distinguish authorization, derived checks, external mutations, public observations, and any incomplete stage."
verification_method = "automated-result-schema-and-public-smoke-test"

[relations]
derives_from = ["CAP-RLO-001"]
+++

# Requirement: Observe and attest the complete publication transaction

## Rationale

A green job without connected commits, hashes, URLs, environment decisions, and public observations is insufficient for operating review and later diagnosis.

## Preconditions and trigger

Every orchestration run, including preflight refusal and post-publication failure, reaches result reporting.

## Required response

Report the RLS, VREC, release contract, candidate and governance commits, version, tag, distribution and manifest hashes, build results, GitHub Release and workflow URLs, PyPI deployment approval and file URLs, attestations, Pages URL and provenance hashes, public Python 3.11 install identity, and the status of each stage. Upload a bounded JSON result as run evidence and render the same authoritative fields in the job summary.

## Failure and boundary behavior

Missing or unobservable evidence is reported as unavailable or incomplete, never as satisfied. Result generation must not conceal the original failure or turn observation into a formal artifact transition.

## Constraints

The workflow does not commit publication evidence automatically. Repository retention, if required, remains a later bounded governance action.

## Acceptance examples

A successful run links every public outcome and proves `harnessctl --version`. A failed Pages stage reports package publication as complete and Pages as failed rather than assigning one aggregate health score.

## Open decisions

None.
