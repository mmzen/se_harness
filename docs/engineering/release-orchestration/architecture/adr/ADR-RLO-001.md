+++
id = "ADR-RLO-001"
type = "adr"
title = "Preserve the trusted publisher identity in one release orchestrator"
status = "approved"
owners = ["engineering-owner", "security-owner", "release-owner"]
created = "2026-08-18"
updated = "2026-08-18"

[relations]
decides = ["ARCH-RLO-001"]
+++

# ADR: Preserve the trusted publisher identity in one release orchestrator

## Status

Accepted on 2026-08-18 as part of the approved `WO-RLO-001` packet.

## Context

SE Harness already has separate manual workflows for exact PyPI promotion and release-bound Pages deployment, while candidate qualification, tag creation, GitHub Release creation, public smoke checks, and recovery remain manually composed. A single workflow should derive and execute the last mile from one released RLS without merging candidate and credential boundaries.

The initial proposal was to add `publish-release.yml` and call the PyPI workflow as a reusable workflow. Authoritative PyPI guidance states that reusable workflows cannot currently be the configured GitHub Trusted Publisher. PyPI binds publisher configuration to a top-level workflow filename and optional environment. The repository's working identity is `.github/workflows/publish-pypi.yml` plus environment `pypi`.

## Decision drivers

- One normal operator input and one connected run.
- No PyPI token or new stored workflow-trigger credential.
- No candidate execution in credential-bearing jobs.
- Preserve the already proven PyPI Trusted Publisher identity where possible.
- Keep the `pypi` and `github-pages` environment protections.
- Exact deterministic package and GitHub release state.
- Honest resumability across non-atomic external mutations.
- Bounded migration and recovery behavior.

## Considered options

1. Keep the current manual sequence and add documentation only.
2. Add a new orchestrator that invokes the current workflow through a stored PAT or GitHub App credential.
3. Make the current PyPI workflow reusable and call it from a new top-level workflow.
4. Add a new top-level workflow and migrate PyPI Trusted Publisher configuration to its filename.
5. Preserve `publish-pypi.yml` as the top-level trusted filename and evolve it into a multi-job released-record orchestrator, while retaining Pages as a bounded main-only recovery workflow.

## Decision

Choose option 5.

Keep `.github/workflows/publish-pypi.yml` as the top-level workflow identity registered with PyPI, change its normal manual interface to one released RLS ID, and add distinct resolve, qualify, GitHub, PyPI, Pages, and observe jobs with job-scoped permissions. The workflow display name may describe complete SE Harness publication even though the stable filename retains its historical PyPI identity.

The PyPI job stays directly in that top-level workflow. It receives resolved hashes through trusted job outputs, independently downloads final GitHub assets, uses the protected `pypi` environment, and executes no checkout, build, or candidate code. The existing Pages workflow becomes an explicit main-only recovery entry point; automatic Pages deployment occurs inside the main-context orchestrator so no tag-ref deployment reaches the environment.

Use repository scripts and versioned JSON schemas to keep workflow YAML declarative. The workflow may observe complete exact prior state and continue, but partial or mismatched immutable state always fails.

## Consequences

- Positive: no new stored trigger credential or PyPI publisher migration; one input drives the whole transaction; the proven OIDC filename/environment identity remains; privileges stay job-scoped.
- Positive: the `v0.4.1` Pages tag-ref failure mode is removed from normal releases.
- Negative: the stable filename `publish-pypi.yml` describes only one part of its expanded responsibility; the display name and documentation must make this explicit.
- Negative: the workflow contains several jobs and requires strong static tests plus supporting scripts to remain reviewable.
- Operational: a protected PyPI approval remains required. Pages-only recovery remains a separate explicit run. Existing production workflows must stay available until the new path is verified.
- Security: workflow-file changes are publisher-identity changes in practice and require security review; only the PyPI job receives OIDC.
- Migration: update the existing PyPI and dashboard specifications where trigger mechanics change, retain their underlying controls, and verify external environment/publisher configuration before the first orchestrated production release.

## Validation

- Validate the PyPI workflow remains top-level and matches the externally configured filename and `pypi` environment.
- Prove no reusable workflow or stored PAT is involved in OIDC publication.
- Statistically verify every job permission, environment, action pin, checkout, and executable boundary.
- Exercise exact state and failure matrices with fixtures, then verify a later separately authorized real release.
- Reconfirm the external limitation against [PyPI Trusted Publisher troubleshooting](https://docs.pypi.org/trusted-publishers/troubleshooting/) before implementation; if PyPI gains reusable-workflow support, reconsideration is a new governed decision rather than implicit scope expansion.
