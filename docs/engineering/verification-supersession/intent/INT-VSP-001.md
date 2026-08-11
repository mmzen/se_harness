+++
id = "INT-VSP-001"
type = "intent"
title = "Make verification-record history unambiguous"
status = "approved"
owners = ["repository-owner", "quality-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
+++

# Intent: Make verification-record history unambiguous

## Problem

A ready verification record can remain indefinitely after a later candidate has been verified for the same work. The records are individually valid, but operators and the Harness Explorer cannot distinguish an active candidate awaiting review from an abandoned candidate retained only for audit. The current validator globally recognizes `superseded` yet rejects that status for verification records, and no typed relation identifies the authoritative successor.

## Desired outcomes

- Stale ready verification attempts are retired explicitly without deletion or false verification.
- Every superseded VREC identifies one accountable, eligible successor.
- Verification and release readiness exclude superseded records.
- The dashboard shows the supersession chain and warns about apparently stale ready records.
- Existing VRECs remain valid until an accountable owner chooses a transition.
- `VREC-AGR-001` can later be retired in favor of `VREC-PMI-001` through a separate governance decision.

## Actors and stakeholders

- Assurance owners decide whether one ready record is superseded by another.
- Release owners need an unambiguous eligible verification set.
- Repository owners and engineers need durable audit history.
- Dashboard users need active work separated from historical attempts.
- Automation validates and projects decisions but does not make them.

## Success measures

| Measure | Baseline | Target | Observation window |
|---|---:|---:|---|
| Stale ready VRECs silently presented as active | at least 1 | 0 after authorized cleanup | every dashboard generation |
| Invalid supersession shapes accepted | unspecified | 0 | every validator run |
| Superseded VRECs accepted for release preparation | possible if left ready | 0 | every provenance test |
| Existing valid records broken without transition | 0 | 0 | every upgrade and release |
| Human lifecycle decisions inferred by automation | 0 intended | 0 | every operation |

## Non-goals

- Automatically selecting or approving a successor.
- Rewriting candidate commits, evidence, snapshots, timestamps, or historical verification facts.
- Superseding released verification or release records in this iteration.
- Deleting abandoned records or hiding them from audit views.
- Transitioning `VREC-AGR-001` as part of implementation.
- Adding installation profiles, external services, or repository-specific policy.

## Principles and immutable constraints

Lifecycle status records accountable authority, not confidence. Historical candidate identity is immutable. Supersession must be explicit, typed, acyclic, coverage-preserving, release-safe, deterministic, and visible. Automation may validate or visualize the decision but may not authorize it.

## Risks and assumptions

- Fact: `VREC-AGR-001` and `VREC-PMI-001` bind different commits and overlap on `WO-AGR-001`.
- Fact: the newer verified record covers all work in the older ready record.
- Assumption: the first safe transition should be limited to `ready -> superseded`.
- Risk: coverage alone cannot prove human intent; explicit governance authorization remains mandatory.
- Risk: a future need to retire verified or released records requires a separate lifecycle decision.
