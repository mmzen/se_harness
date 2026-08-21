+++
id = "INT-REB-001"
type = "intent"
title = "Prevent released-evaluator and candidate authority conflation"
status = "approved"
owners = ["product-owner", "repository-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
+++

# Intent: Prevent released-evaluator and candidate authority conflation

## Problem

The 0.5.0 release-governance incident showed that candidate product code and the independently released runtime evaluating the repository can be confused when their roles, identity sources, and lifecycle entry points are not enforced consistently. The root has since been converted to the ordinary standard-repository lifecycle, but active publication code still carries retired `governor` interfaces, installed-root mutators do not uniformly prove locked evaluator identity before writing, and release-readiness records do not bind that identity in one durable observation.

This leaves maintainers and accountable owners exposed to late detection, preventable release failure, and renewed ambiguity about which software produced evidence and which humans exercised authority.

## Desired outcomes

- Every installed-root mutation either proves the locked released-evaluator identity before its first write or fails without changing the repository.
- Active release and Pages workflows resolve the evaluator from the standard installation rather than a special self-hosting descriptor or role.
- Release readiness retains one bounded, reviewable evaluator identity observation tied to the proposed record.
- Evaluator upgrades remain separate from product release authorization unless an explicit governing chain models their dependency and sequencing.
- Conflicting draft chains are visible without gaining authority, and maintainers can rehearse a bounded recovery without improvising publication controls.

## Actors and stakeholders

- Repository maintainers operate root lifecycle and recovery procedures.
- Product and requirements owners decide the intended prevention outcomes.
- Technical and security owners own the trust boundary and standard-lock design.
- Engineering owners authorize bounded implementation work.
- Assurance owners judge independent evidence and evaluator provenance.
- Release owners decide promotion only after evaluator identity and candidate provenance are clear.
- Consumer repositories depend on preservation of one standard installation and compatible upgrade behavior.

## Success measures

| Measure | Baseline | Target | Observation window |
|---|---:|---:|---|
| Installed-root mutators covered by a pre-write identity gate | Not uniformly enforced | 100% of declared mutators | Every candidate-source and package CI run |
| Active publication invocations using retired `governor` CLI or descriptor contracts | Present | 0 | Every pull request and release dispatch |
| New ready release records with bound evaluator identity evidence | Not required | 100% when repository policy requires it | Every release-readiness preparation |
| Negative identity cases that leave the target byte-for-byte unchanged | Partial | All declared source, package, version, digest, path, and ambiguity cases | Every full regression run |
| Disposable standard-root recovery rehearsal | Not defined | Deterministic pass with restoration proof | Before closing issue #81 and periodically thereafter |

## Non-goals

- Retrospectively authorize or reinterpret the emergency 0.5.0a1 or 0.5.0 publications.
- Delete or rewrite historical artifacts, RCA terminology, or fixtures that accurately describe the retired model.
- Introduce an installation profile, repository class, long-lived governor descriptor, or special promotion command.
- Give automation product, assurance, release, publication, deployment, or operating authority.
- Implement any correction outside an approved, bounded work order.

## Principles and immutable constraints

- There is exactly one standard installation and one managed root contract.
- Candidate source and candidate packages are evidence producers only and never substitute for root released-evaluator assurance.
- The released evaluator is immutable, independently published, externally installed, and identified by version, distribution digest, and bounded origins.
- Root mutation fails before any write when identity is missing, ambiguous, or inconsistent.
- Existing repository-owned content and historical facts remain preserved.
- Human decision rights remain separate from automated validation and record preparation.

## Risks and assumptions

- Adding a standard evaluator identity to lock semantics requires a backward-compatible, explicitly verified migration path.
- Runtime distribution metadata differs across installation mechanisms; the specification therefore requires an exact downloaded wheel and an installed archive-hash proof rather than relying on a version string alone.
- Active publication paths may contain historical naming for genuine compatibility; only executable dependencies on the retired model are prohibited.
- Draft-chain detection can identify structural overlap but cannot determine which proposal is semantically correct or authorized.
