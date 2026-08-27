+++
id = "ARCH-REB-012"
type = "architecture"
title = "One handover mechanism: the migration rehearsal, and no repository view"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
addresses = ["REQ-REB-029"]
conforms_to = ["SPEC-REB-013"]

[decision_assessment]
outcome = "adr_required"
triggers = [
  "system-boundary",
  "cross-cutting-policy",
  "difficult-to-reverse",
  "material-alternatives",
]
rationale = "Deleting the predecessor compatibility view removes a boundary the authorized last mile and the release-bound Pages build both crossed, retires a cross-cutting release-path policy that four release contracts declared, and cannot be undone cheaply: the 0.6.0 preparation and publication evidence becomes verifiable by digest but no longer reproducible."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T16:43:16Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-27 by the accountable owner, 'I approve the artifacts', on the read-only sweep of 2026-08-27 following issue #190: the governance-migration rehearsal is the sole predecessor-successor mechanism, and no projection, view, sparse checkout or omitting clone of this repository is constructed for any evaluator. The decision assessment is adr_required on system-boundary, cross-cutting-policy, difficult-to-reverse and material-alternatives; ADR-REB-012 decides it."
+++

# Architecture: One handover mechanism: the migration rehearsal, and no repository view

## Context and scope

Two mechanisms answered the same question — does a predecessor evaluator and
its successor agree about this repository. One was general and shipped; one
was specific and did not. This architecture keeps the general one and deletes
the specific one, then states what the closed history rests on afterwards.

Scope is the release and publication path of this repository. The evaluator
boundary itself — released governor outside the checkout, candidate source
inside, run with `-I` — is unchanged.

## Components and responsibilities

- **`se_harness/governance_migration.py`** (retained, unmodified): the
  no-network, dual-runtime rehearsal of a predecessor-to-successor handover.
  This is the sole handover mechanism. Reached as
  `harnessctl rehearse-migration`, already required in the installed surface.
- **`se_harness/release_qualification.py`** (edited): keeps `released-root`,
  `complete-candidate`, `candidate-package` and `public-install`; loses
  `predecessor-view` and its `PV001` and `PV002` checks. It stops being the
  one product module that lazily imported an unpackaged repository package.
- **`.github/workflows/publish-pypi.yml`** and
  **`pages-publication.yml`** (edited): both read the complete governance
  snapshot. The selector, the view step and the exclusion observation go.
- **`.github/scripts/publish_dashboard.py`** (edited): loses the
  release-bootstrap contract validation and its cross-checks; keeps the
  `harness-dashboard-bootstrap-v2` payload it also happens to own.
- **`scripts/check_portable_release_surface.py`** (edited): the installed
  qualification surface it pins no longer includes `predecessor-view`.
- **`se_harness/hash_bound_classes.json`** (retained, unmodified): after the
  machinery is gone this is what holds the 0.6.0 evidence in place. Its
  enforcement path, `se_harness/hash_bound.py`, has no bootstrap dependency,
  so the binding survives the deletion untouched.
- **`repository_tools/predecessor_facts.py`** (retained, unmodified): carries
  no bootstrap dependency and runs on every push and pull request. Its name
  is the only thing it shares with the deleted set.
- **`scripts/validate_governor_transition.py`** (retained, unmodified): the
  live governor-transition lane. It is not a bootstrap consumer, which is why
  `predecessor_assessment.py` can be deleted without touching it.

Retired: `release_bootstrap` (the nine-key `[bootstrap]` parser and binder),
`predecessor_preparation` (the sparse view builder), `predecessor_publication`
(the predecessor run inside the view), `predecessor_assessment` (the
transitional hosted qualification), and their four entry-point scripts.

## Control flow

Before, the release path forked on a contract's `[bootstrap]` tuple: build a
sparse view and run the predecessor evaluator in it, or write an exclusion
observation and proceed. After:

resolve governance commit → materialize the complete snapshot → publish and
build Pages from it → the governance-migration rehearsal supplies
predecessor-successor assurance on its own schedule.

One path, no fork, no temporary clone, no sparse-checkout specification.

## Trust boundaries

Unchanged in direction: the released evaluator judges the candidate; the
candidate never judges itself. What is removed is a boundary crossing —
executing a *published* evaluator against a *constructed* projection of the
repository, in a temporary clone, with a sparse specification derived from
artifact metadata. That crossing had its own attack surface (symbolic-link
traversal, sparse-policy substitution, credential leakage into the temporary
clone) which the deleted modules spent substantial code refusing. Deleting
the crossing deletes the surface and the refusals together.

The closed 0.6.0 evidence changes status from *reproducible* to
*digest-verifiable*. That is a deliberate reduction, recorded in
`ADR-REB-012`, and it is the reason this architecture requires an ADR.

## Data ownership

The six closed 0.6.0 artifacts are owned by history and written by no code
after this change. Their digests are owned by the hash-bound classes. The
retired schema names stay reserved so a stored document can never be
reinterpreted by a later mechanism wearing the same name.

## Prohibited patterns

Re-introducing a projection, view, sparse checkout, or omitting clone of this
repository for any evaluator to read; branching a release step on a
contract-declared predecessor evaluator; reusing the retired schema names or
the reserved `PV001` and `PV002` codes; reaching for a repository-only module
from a packaged product module; editing a hash-locked managed path from
candidate source.

## Quality attributes

Fewer moving parts on the least-exercised path. The deleted mechanism ran
only on `workflow_dispatch`, which is why all three of its #190 defects
reached a live release before anyone saw them; one of the three also broke a
test and the per-pull-request candidate qualification. Removing the path
removes a class of defect that ordinary pull-request CI structurally cannot
catch.

## Decision assessment

`ADR-REB-012` records the decision and the alternatives.
