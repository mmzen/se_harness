+++
id = "WO-PYP-003"
type = "work_order"
title = "Approve and publish PyPI automation verification"
status = "implemented"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-PYP-005"]
specifications = ["SPEC-PYP-001"]
architecture = ["ARCH-PYP-001", "ADR-PYP-001"]
verification = ["VER-PYP-001"]
+++

# Work Order: Approve and publish PyPI automation verification

## Objective

Record the accountable assurance decision for `VREC-PYP-001`, retain the bounded transition in a governance commit, and publish that commit through a new review branch and pull request against `main`.

## Authorization

The accountable repository owner confirmed pull request #13 was merged, reviewed the retained evidence, and explicitly authorized the verification transition, governance commit, normal push, and pull request on 2026-08-11 with the instruction `i merged, then transition and governance commit + PR`.

## In scope

- Confirm pull request #13 merged the candidate and ready record into `main` at merge commit `7884db868d74b4c72786c227d5ba070d90557ca9`.
- Confirm `VREC-PYP-001` is a valid `ready` record for `WO-PYP-001` under `VER-PYP-001`.
- Confirm it names clean candidate commit `01fc231dc1fc4501fd1f74aee9eecfea9c1d9db9` and was retained in ready-record governance commit `8c81c8ae8091d52b62e0998044cacdd888d2989e`.
- Review the retained evidence at `docs/engineering/pypi-publication/evidence/WO-PYP-001-verification.md`.
- Transition only `VREC-PYP-001` from `ready` to `verified` and retain the explicit human-decision note.
- Create one governance commit containing only this work order, its evidence, and the bounded verification-record transition.
- Push `governance/verify-vrec-pyp-001` normally to `origin` and open a pull request targeting `main`.

## Out of scope

Changing the candidate commit, artifact snapshot, evidence path, or typed relations; preparing or transitioning a release record; creating or moving a tag; changing GitHub release assets; dispatching or approving the PyPI workflow; uploading to PyPI; merging the pull request; force pushing; rewriting history; deployment; and any other release or publication action are not authorized.

## Required verification

The artifact graph must validate with zero diagnostics; the candidate and ready-record governance commits must remain locally available and in the checkout ancestry; the retained evidence and immutable captured fields must remain unchanged; the complete test suite must pass on Python 3.11 and the local runtime with only the known conditional Windows symlink skips; CLI help, source doctor, dashboard generation, workflow YAML parsing, Bash syntax, and diff hygiene must pass; and the final commit must contain only the three bounded governance files.

## Completion evidence

Retain the reviewed facts, hashes, commands, outcomes, deviations, and authority boundary in `docs/engineering/pypi-publication/evidence/WO-PYP-003-verification.md`. The resulting commit, remote branch, pull request URL, and CI results remain externally discoverable after publication and are not predicted inside the commit.
