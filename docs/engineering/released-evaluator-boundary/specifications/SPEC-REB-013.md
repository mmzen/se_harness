+++
id = "SPEC-REB-013"
type = "specification"
title = "Retired predecessor-bootstrap surface and retained-history contract"
status = "approved"
owners = ["technical-owner", "engineering-owner", "release-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
specifies = ["REQ-REB-029"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T16:43:16Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-27 by the accountable owner, 'I approve the artifacts', on the read-only sweep of 2026-08-27 following issue #190: retires SPEC-REB-007 and the predecessor-view rules of SPEC-REB-003 and SPEC-REB-005, keeping their rejected-succession rules. The six closed 0.6.0 artifacts stay byte-identical and hash-bound, and the hash-locked managed validator is not edited under this specification."
+++

# Specification: Retired predecessor-bootstrap surface and retained-history contract

## Amendment of 2026-08-28 (`WO-REB-030`)

Rule 7 is moot: `se_harness/interpreter_safety.json` no longer exists (`SPEC-REB-015`); the property it protected — no declared site names a deleted file — is now that no code path outside `se_harness/runtime_identity.py` validates an interpreter, which `StaticArchitectureTests` pin.

## Amendment of 2026-08-28

Amended under `WO-ECP-010` for issue #210: where this specification names the governance-migration rehearsal (`se_harness/governance_migration.py`, `rehearse-migration`) as the retained predecessor-to-successor mechanism, read the real upgrade rehearsal of `repository_tools/upgrade_rehearsal.py` instead; `rehearse-migration` is retired and its name reserved, and `qualify` keeps its four typed operations.


## Scope

The removal of the contract-bound predecessor evaluator bootstrap and the
predecessor compatibility view, and the state of the closed 0.6.0 bootstrap
history afterwards. Retires `SPEC-REB-007` and the predecessor-view rules of
`SPEC-REB-003` and `SPEC-REB-005`; the rejected-succession rules of
`SPEC-REB-005` stay, because `REQ-REB-010` and `REQ-REB-011` still require
them.

## Actors and external systems

- The released governing evaluator, run from outside the checkout with `-I`.
- The authorized last mile (`publish-pypi.yml`) and the release-bound Pages
  build (`pages-publication.yml`).
- The dashboard publisher (`.github/scripts/publish_dashboard.py`).
- The governance-migration rehearsal (`se_harness/governance_migration.py`),
  which is the retained mechanism and is not modified here.

## Inputs

- A clean committed governance snapshot.
- A schema-2 release record and its declaring release contract, neither
  carrying an active `[bootstrap]` tuple.
- The six closed 0.6.0 artifacts, unchanged: `REL-SEH-008`, `REL-SEH-009`,
  `REL-SEH-010`, `REL-SEH-011`, `RLS-SEH-009`, `RLS-SEH-012`.

## Outputs

Publication and Pages results produced from the complete governance snapshot;
no exclusion observation; no view directory; no preparation-view or
predecessor-publication evidence document.

## State model

There is no view state. `complete snapshot` → `publish` and
`complete snapshot` → `Pages build` directly. The prior three-state model
(`view applies` / `view excluded` / `no view`) collapses to one.

## Behavioral rules

1. **Deleted modules.** `repository_tools/release_bootstrap.py`,
   `predecessor_preparation.py`, `predecessor_publication.py` and
   `predecessor_assessment.py` are removed with their four test modules. No
   retained module imports them.
2. **Deleted entry points.** `scripts/bind_release_bootstrap.py`,
   `prepare_predecessor_release.py`,
   `validate_predecessor_publication_view.py` and
   `assess_predecessor_evaluator.py` are removed.
3. **Qualification surface.** The `predecessor-view` qualification operation
   and its `PV001` and `PV002` checks are retired; the code values stay
   reserved. `check_portable_release_surface.py` no longer requires
   `predecessor-view` in the installed surface, and continues to require
   `rehearse-migration`, `released-root`, `complete-candidate`,
   `candidate-package` and `public-install`.
4. **Publication.** `publish-pypi.yml` performs no record selection for a
   view, runs no predecessor-view step, and writes no exclusion observation.
   Its acquire-and-prove step for the released evaluator is unchanged.
5. **Pages.** `pages-publication.yml` materializes the complete governance
   snapshot at the view path as a detached worktree of the resolved
   governance commit — the behavior `WO-REB-026` already produces on the
   exclusion branch — with no condition and no alternate branch. The
   dashboard generator's invocation is unchanged.
6. **Dashboard publisher.** `publish_dashboard.py` no longer validates a
   release-bootstrap contract and performs no evaluator or rejected-pair
   cross-check. Its `harness-dashboard-bootstrap-v2` payload is a distinct
   schema and is untouched.
7. **Interpreter safety.** `se_harness/interpreter_safety.json` no longer
   declares the two sites naming `predecessor_assessment.py` and
   `predecessor_preparation.py`. Every remaining declared site still resolves
   to a present file.
8. **Retained history.** The six closed 0.6.0 artifacts keep their bytes,
   their `[bootstrap]` tables, their `preparation_schema` markers and their
   evidence files. `se_harness/hash_bound_classes.json` is unchanged, so
   `evaluator_evidence_sha256`, `preparation_view_evidence_sha256` and
   `from_lock_sha256` stay bound.
9. **Validator, unchanged here.** `scripts/validate_engineering_artifacts.py`
   is a hash-locked managed copy of released 0.6.0 and is not edited. Both of
   its bootstrap entry points are already conditional — one on
   `"bootstrap" in artifact.metadata`, one on an immediate return when
   `preparation_schema` is absent — so the retained rules change no verdict
   and no active artifact reaches them. Their removal from
   `templates/repository/standard/`, and the retirement of `REQ-REB-010`,
   belong to a later work order that a release must carry to the root.
10. **No re-derivation.** After this change the repository contains no code
    able to reconstruct a predecessor view, re-run a predecessor evaluator
    against one, or re-derive the 0.6.0 preparation or publication evidence.
    That evidence is verifiable by digest and is not reproducible.
11. **Governor verdict invariance.** The released governing evaluator's
    artifact, error and warning counts over the closed 0.6.0 history are the
    same before and after, allowing for the packet's own added artifacts.
12. **Determinism.** No step retained by this specification depends on a
    temporary directory name, a clone depth, or a checkout basename.

## Error and recovery behavior

A release record whose contract declares a `[bootstrap]` tuple gains no
authority; nothing selects it, and no step refuses on its account. A
publication or Pages step that cannot resolve the governance commit fails
closed. Because nothing is written to a managed path and no historical byte
changes, recovery from a failed execution is a branch reset.

## Data and interface contracts

Retired schemas: `se-harness-release-bootstrap-v1`,
`se-harness-predecessor-bootstrap-v1` and
`se-harness-predecessor-view-exclusion/v1`. Their names stay reserved and are
never reused. The retained history's stored instances of the first two remain
valid documents on disk; they are data, not an active contract.

Unaffected schemas: `harness-dashboard-bootstrap-v2`,
`se-harness-runtime-identity-v2`, the evaluator-upgrade evidence document,
and the governance-migration report.

## Compatibility and migration

No consumer repository is affected: `repository_tools/` is not packaged, and
`predecessor-view` could never run from an installed evaluator because it
lazily imports that package. Adopters lose one qualification operation from
`harnessctl qualify` and gain nothing to migrate. This repository's own
release notes record the retirement.

## Examples and counterexamples

- Valid: `RLS-SEH-015`'s publication and Pages build re-run on the retired
  surface and produce the same public Explorer.
- Valid: the closed pair validates unchanged under the exact public 0.6.0
  evaluator, and `RLS-SEH-012`'s two evidence digests still verify.
- Invalid: any retained import of a deleted module.
- Invalid: a step that branches on whether a contract declares a
  `[bootstrap]` tuple.
- Invalid: an edit to `scripts/validate_engineering_artifacts.py` or to
  `se_harness/hash_bound_classes.json` under this specification.

## Explicitly unspecified decisions

Whether the retired qualification operation disappears from the subparser or
remains as a refusing stub naming its replacement; where any residual helper
of the deleted modules that a retained caller still needs is re-homed;
whether a future release generalizes the governance-migration rehearsal
beyond its current version boundary.
