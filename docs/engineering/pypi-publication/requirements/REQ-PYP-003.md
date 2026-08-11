+++
id = "REQ-PYP-003"
type = "requirement"
title = "Use least-privilege Trusted Publishing"
status = "implemented"
owners = ["security-owner", "repository-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN the PyPI publisher authenticates, THE SYSTEM SHALL use GitHub OIDC from a main-only protected pypi environment with job-scoped id-token write and contents read permissions and SHALL store no PyPI credential."
verification_method = "inspection-and-automated-test"

[relations]
derives_from = ["CAP-PYP-001"]
+++

# Requirement: Use least-privilege Trusted Publishing

## Rationale

Short-lived workload identity reduces credential exposure, while the environment remains the accountable human deployment boundary.

## Required response

Configure the GitHub `pypi` environment for deployments from `main` only, require the job itself to run from `refs/heads/main`, grant only `contents: read` and `id-token: write` to the publication job, invoke the official PyPA action at an immutable reviewed commit, and configure the PyPI project to trust the exact owner, repository, workflow filename, and environment.

## Failure and boundary behavior

Missing environment approval, OIDC minting failure, publisher mismatch, or insufficient permission fails closed. No workflow fallback may request a stored password or API token.

## Constraints

Do not checkout or execute repository code in the credential-bearing job. Do not grant OIDC permission globally or to validation jobs.

## Open decisions

None.
