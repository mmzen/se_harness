# Publication compatibility correction proposal

Transient review note outside the repository. This is a proposed correction,
not a work order, approval, or release decision.

PR #490 merged at `523ff825773e05c970c041ecee5c22bfabedaa3f`. Its tree matches
the reviewed branch. RLS-SEH-028 remains released for candidate
`30d4dba2a088c4f83756c1241b76cdab40f796bd`. The released evaluator's external-action
gate passes. No publication workflow has been dispatched.

## Observed blocker

The publication helper `.github/scripts/publish_dashboard.py` assumes lock
schema 3 in two places:

- `_validated_evaluator_binding`, line 406, treats schema 4 as no evaluator.
  Release-plan resolution reports that evidence differs from the standard lock.
- `read_evaluator`, line 560, explicitly rejects schemas other than 3.
  This is also the evaluator-acquisition step at the start of publication.

The repository has an accepted schema-4 lock with plugin ownership. Its
complete evaluator identity equals the RLS sidecar identity, and the sidecar
hash matches the record. The observed error is a reader compatibility issue,
not evidence of different evaluator bytes. The actual failed commands are
retained in `r019-postmerge-publication-diagnosis.json` and
`r019-publication-plan-inspection.json`.

## Proposed bounded work

Prepare a governed correction for both readers to support valid schema-4
plugin ownership while preserving schema-3 support and all existing identity,
hash, provenance and unsupported-schema checks. First select the governing
publication and ownership contracts and define any necessary amendment.

Implementation scope is the shared publication helper and the applicable
existing publication tests (`tests/test_dashboard_publication.py` and, where
needed, `tests/test_release_orchestration.py`), with formal artifacts and
retained evidence for that work. No change to the released RLS, VREC, lock,
bound candidate or archive hashes is proposed.

Verify both accepted schemas, malformed schema-4 ownership, unsupported
schemas, mismatched identities and tampered evidence. Run both read-only
publication entry points against the actual merged governance snapshot and
the applicable publication regressions. The earlier suite and ready-record
recipe replay did not cover these readers with the schema-4 release snapshot.

After review and integration of the correction, recheck the exact publication
plan before requesting authorization to dispatch `publish-pypi.yml` on `main`
with `release_record=RLS-SEH-028`. That workflow creates the GitHub release and
maintenance branch, publishes the checker to PyPI behind its protected
environment, and publishes the release-bound Explorer. Latest promotion,
plugin publication and repository adoption remain separate actions.
