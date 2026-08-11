+++
id = "VER-PYP-001"
type = "verification"
title = "Verify governed PyPI Trusted Publishing"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
verifies = ["REQ-PYP-001", "REQ-PYP-002", "REQ-PYP-003", "REQ-PYP-004", "REQ-PYP-005"]
+++

# Verification Contract: Verify governed PyPI Trusted Publishing

## Independence

Static tests inspect the workflow as data rather than executing its commands or relying on the publisher action. Expected `0.2.0` hashes come from retained release evidence and independently downloaded GitHub assets. External configuration is inspected through GitHub/PyPI control planes, not inferred from repository files.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-PYP-001 | static test and GitHub validation | trigger, tag pattern, release-state query | manual only; malformed, draft, and prerelease states stop |
| REQ-PYP-002 | static test and local vector | hash inputs, exact filenames, deterministic manifest | both independent hashes and exact two-line manifest must agree |
| REQ-PYP-003 | static test and API inspection | main-only job/environment, permissions, action pin, secret scan | protected `pypi`; only `main`; job-scoped read/OIDC; no stored-token path |
| REQ-PYP-004 | static test and separately authorized end to end | no checkout/build, `dist/`, publisher options, PyPI files | only existing wheel/sdist uploaded; metadata, hashes, attestations pass; duplicates fail |
| REQ-PYP-005 | artifact and manual review | work-order boundary, publication authorization, retained result | implementation grants no upload; each dispatch has explicit before/after evidence |

## Acceptance scenarios

Executable behavior scenarios are retained in `acceptance/pypi-publication.feature`. The initial implementation verifies configuration and preflight rules without dispatching the irreversible production upload.

## Property and invariant tests

- Only `vMAJOR.MINOR.PATCH` is accepted.
- Expected hash inputs are exactly lowercase 64-character hexadecimal strings.
- Any changed artifact byte or manifest line fails preflight.
- Only exact `se_harness` wheel/sdist filenames derived from the tag enter `dist/`.
- No workflow path contains checkout, build, token secret, password, mutable publisher reference, or duplicate skipping.
- The publication job and environment accept only `main`; OIDC and read permission exist only at that job.

## Static and architecture checks

Inspect the workflow text for the complete normative contract and pin. Run the full repository artifact validator and unit suite. Let GitHub parse the workflow on the review branch. Inspect the environment through the GitHub API.

## Security and privacy checks

Review shell quoting and environment transport for all dispatch inputs. Confirm strict tag/hash regular expressions, no direct expression interpolation in shell commands, no repository checkout, no arbitrary dependency installation, no PyPI secret reference, a full action SHA, and an exact PyPI environment.

## Performance and resilience checks

Use local fixture files to prove deterministic SHA-256 and manifest comparison. External service unavailability must fail the run without retry loops, fallback credentials, artifact changes, or local persistence.

## Manual assessments

The owner confirms the PyPI project trusts owner `mmzen`, repository `se_harness`, workflow `publish-pypi.yml`, and environment `pypi`. The release owner separately confirms the release record, tag, version, hashes, and destination before dispatch.

## Evidence retention

Implementation evidence belongs in `docs/engineering/pypi-publication/evidence/WO-PYP-001-verification.md`. A later publication authorization and result must retain workflow run/deployment URLs, PyPI file URLs, PyPI hashes and attestations, and exact-version installation output.

## Residual uncertainty

Static tests cannot prove PyPI account configuration or an irreversible upload. External environment protection can change after inspection. The first authorized publication remains an explicit human-controlled verification phase.
