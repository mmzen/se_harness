+++
id = "WO-REB-005"
type = "work_order"
title = "Enforce LF-stable evaluator evidence and qualify successor candidate"
status = "implemented"
owners = ["engineering-owner", "repository-owner", "quality-owner", "security-owner", "release-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[assurance]
commit_bound_verification = "required"
rationale = "Release decisions will rely on the correctness of versioned Git policy, canonical evidence bytes, installer/template behavior, and successor-candidate provenance."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-REB-009", "REQ-REB-010"]
specifications = ["SPEC-REB-004"]
architecture = ["ARCH-REB-003", "ADR-REB-003"]
verification = ["VER-REB-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T17:46:21Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-21T17:48:51Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-21T21:41:30Z"
decided_by = "engineering-owner"
+++

# Work Order: Enforce LF-stable evaluator evidence and qualify successor candidate

## Lifecycle

Bounded implementation is complete at exact candidate `2ab1c1fffd2c0a2f462e7affcb9ea6f426b202e5`, with local and hosted qualification retained at `docs/engineering/released-evaluator-boundary/evidence/WO-REB-005-verification.md`. This implemented state does not prepare or transition a VREC or RLS and does not authorize another push, tag, publication, deployment, maintenance mutation, credential use, external-policy change, or root-evaluator upgrade.

## Objective

Preserve canonical evaluator-evidence bytes across supported Git checkouts without weakening raw-byte assurance, permit exact rejected predecessor-bootstrap history without retaining active authority, then produce complete local evidence for a successor 0.6.0 candidate C3.

## In scope

- Add the exact narrow LF attribute to candidate source and the canonical standard template.
- Update candidate template/lock/package surfaces required to deliver that policy while leaving the operational released-0.5 configuration and lock unchanged.
- Add deterministic attribute-precedence, fresh-clone, cross-configuration, tamper, installer, package, and parity tests from `VER-REB-003`.
- Reproduce and retain the default-Windows C2 failure and LF-control pass.
- Confirm raw evidence hashing and canonical JSON validation are unchanged.
- Update candidate and canonical-template validation so only an exact `rejected RLS + rejected declaring contract` pair is accepted as terminal bootstrap history.
- Keep binder, preparation, release, and publication paths restricted to an exact approved contract; add the complete mixed-state and authority-negative matrix.
- Update bounded operator/release documentation and 0.6.0 notes needed to describe the correction.
- Run full local C3 source, package, dual-runtime, released-evaluator, bootstrap, reproducibility, bundle, graph, inspection, dashboard, doctor, distribution, archive, lock, recovery, diff, and secret/path qualification.
- Retain one `WO-REB-005` evidence file suitable for the later twelve-work-order aggregate authorized by the successor release-scope amendment.

## Out of scope

- Editing, amending, repointing, or deleting C2, `VREC-SEH-009`, `RLS-SEH-009`, or its evaluator evidence.
- Rejecting `RLS-SEH-009` or `REL-SEH-008` without their separate accountable lifecycle decisions.
- Changing the operational `.engineering-harness.toml`, schema-2 lock, installed released evaluator, or maintenance state.
- Normalizing evidence in the validator, adding a missing-evidence exception, or depending on local Git configuration.
- Using a rejected bootstrap contract for any operational action or accepting a mixed ready/rejected pair.
- Creating a candidate commit, pushing, dispatching hosted lanes, preparing/transiting VREC or RLS records, tagging, publishing, deploying, or using credentials without separate authority.

## Authorized decision envelope

After approval, the implementation actor may choose test-helper names, isolated temporary-clone layout, and deterministic diagnostic detail. The exact attribute rule, evidence semantics, trust direction, historical preservation, successor release scope, and authority boundaries are not delegated.

## Constraints

- Preserve Python 3.11+ and standard-library runtime behavior.
- Maintain one standard installation and candidate/template parity.
- Treat Git configuration, attributes, paths, repository bytes, JSON, hashes, and environments as untrusted.
- Fail closed and preserve recursive before/after state on every negative case.
- Any material change beyond the approved rule and required delivery/tests stops for renewed scope.

## Expected change surface

- Candidate-root Git attributes and canonical standard-template Git attributes.
- Candidate and canonical-template artifact validation for the closed rejected-bootstrap historical state.
- Canonical template lock/manifest/package surfaces strictly required to ship the new file.
- Checkout, installer, provenance, validator-negative, package, and release-bootstrap tests.
- Bounded operator guidance, release notes, and `WO-REB-005` evidence.

The operational root evaluator configuration and lock are not an expected change surface.

## Required verification

- Execute every method in `VER-REB-003` and unchanged `VER-REB-002` regression coverage.
- Prove the full RLS/contract lifecycle matrix and rejected-contract binder/publication refusal.
- Run isolated fresh clones across the complete Git configuration matrix and prove exact evidence SHA-256.
- Run full tests on Python 3.11 and the current qualification runtime.
- Build twice from exact C3 at its commit epoch; require identical wheels, normalized sdists, bundle manifests, and offline reconstruction.
- Run exact released-0.5 identity/doctor/validation and candidate source/package identity/validation.
- Run formal graph, inspection, dashboard, distribution, parity, archive, recovery, diff, and secret/path checks.
- Run hosted candidate-source/package and released-evaluator lanes only after separate branch/credential authority.

## Evidence to record

- Triggering commit, expected/CRLF hashes, Git configuration, and `E012` diagnostic.
- Failed zero-write disposition transaction and its approved-contract diagnostic.
- Approved preflight manifest and exact changed paths.
- Attribute bytes and `git check-attr` output for every matrix case.
- Historical byte-preservation assertions.
- Complete test/build/package/bundle/evaluator/hosted identities and deviations.
- Exact list of unperformed lifecycle, external, maintenance, credential, and root actions.

## Stop and escalate conditions

- Git attributes cannot force LF under a supported checkout configuration.
- The fix requires validator normalization, a broad policy, operational root upgrade, historical rewrite, or external configuration.
- Terminal history cannot be accepted without enabling reuse of rejected authority.
- Candidate/template/package parity fails.
- Any required local or hosted qualification fails or distributions are nondeterministic.
- The requested action exceeds separately granted authority.

## Completion report format

Report exact attribute bytes, checkout matrix and hashes, changed surfaces, root preservation, C3 commit/tree/build identities when separately authorized, complete qualification, retained evidence, lifecycle state, stopped historical records, and the single next accountable decision.
