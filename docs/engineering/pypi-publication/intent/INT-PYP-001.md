+++
id = "INT-PYP-001"
type = "intent"
title = "Make verified harness releases installable from PyPI"
status = "approved"
owners = ["repository-owner", "release-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
+++

# Intent: Make verified harness releases installable from PyPI

## Problem

`se-harness` version `0.2.0` is available as a verified GitHub release, but ordinary `pip install se-harness` cannot discover it. A direct local upload would introduce a long-lived credential, an unreviewed publication path, and a risk that PyPI receives artifacts rebuilt from a different source state.

## Desired outcomes

- Users can install an explicitly authorized `se-harness` version from PyPI.
- PyPI receives the exact wheel and normalized source distribution already identified by the GitHub release and retained checksums.
- GitHub Actions exchanges a short-lived OIDC identity with PyPI instead of storing a PyPI API token.
- A protected GitHub environment and explicit release-owner decision remain the human publication boundary.
- Publication failures are visible and never trigger artifact replacement, tag movement, or an implicit version correction.

## Actors and stakeholders

- Package consumers need a conventional, version-pinned installation path.
- Repository and release owners decide which verified release may reach PyPI.
- Security owners govern credentials, third-party actions, and deployment identity.
- Quality owners require artifact identity and retained post-publication evidence.

## Success measures

| Measure | Baseline | Target | Observation window |
|---|---:|---:|---|
| Long-lived PyPI secrets stored in GitHub | 0 | 0 | every publication |
| Rebuilds in the PyPI publication job | not governed | 0 | every publication |
| Published artifact hash mismatches | not assessable | 0 | every publication |
| Unapproved production uploads | 0 known | 0 | every publication |
| Exact-version installation from PyPI | unavailable | successful after separate publication authorization | each released version |

## Non-goals

- Publishing a package as part of this implementation work order.
- Rebuilding or modifying the existing `0.2.0` artifacts.
- Publishing prereleases, alternate wheel variants, private packages, or another package index.
- Storing a PyPI password or API token.
- Moving `v0.2.0`, changing `RLS-SEH-001`, or rewriting its GitHub-only decision history.

## Principles and immutable constraints

Artifact identity precedes distribution convenience. Publication uses least privilege, a separately approved environment, an immutable third-party action revision, exact hashes, and the existing release assets. PyPI immutability is respected: correction means a new verified version.

## Risks and assumptions

- Fact: the accountable owner created the PyPI account and `se-harness` project before this work order.
- Fact: `RLS-SEH-001` authorized GitHub publication only, so PyPI requires a new authorization rather than revisionist editing.
- Assumption: the PyPI project will be configured to trust the exact workflow and `pypi` environment before first upload.
- Risk: repository administrators can change workflows or environment rules; branch protection and review remain required external controls.
- Risk: PyPI and GitHub are external services whose availability is not controlled by this repository.
