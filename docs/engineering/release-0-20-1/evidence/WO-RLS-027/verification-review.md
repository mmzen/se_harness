# VREC-SEH-030 assurance review

Status: ready for human mmzen's verification decision. WO-RLS-027 is implemented.
No verification acceptance, merge, release, publication or adoption is recorded.

Candidate: `b9af631b850c495eace9807361ed3ec3e36a10b2`. Work: `WO-RLS-027`. Contract: `VER-RLS-027`.
Record: `../../verification-records/VREC-SEH-030.md`.

The bounded 0.20.1 acceptance-runner correction is complete. It assesses legacy
and minimal candidates without changing the 0.20 installer, packaged instructions,
plugin behavior or the selected 0.19.0 evaluator. The exact clean candidate is
preserved; later commits carry evidence and the generated record only.

## Evidence assessed

- All applicable checks on PR #508 passed at this candidate, including source,
  package, Windows/Linux upgrades and integration-package checks. Their PR merge
  commit identity remains separately recorded in final-candidate-observations.json.
- Committed-candidate capture reran the full-scale suite on the exact candidate:
  1,167 tests passed, 17 Windows skips. The generated record retains that command
  and result. final-capture-source.log retains the output.
- The final sdist was rebuilt and installed on Windows and Linux. Both platforms
  passed 16 operations, including both candidate layouts and independent public
  0.20.0 qualification. All 115 package/template entries match the direct wheel.
- Manual read-only rehearsal 36772527503 replayed the pinned recipe twice for
  this exact candidate. Both wheels and both source archives match. The workflow
  and its existing-release rehearsal both passed.
- Earlier failures, corrections, platform skips and exact test-input identities
  remain in tests.json and hosted-ci.json. No skipped check supplies a required
  layout criterion. Native host behavior is unchanged and not newly qualified.

Pinned wheel SHA256: `300923b4ea800487a7b96822768ff5fbd5c428305ac670948aef404282349764`.
Pinned sdist SHA256: `a4c38a50e3614cfe8b478f7903af3b829e9d605b864d0ba3caca3816f4f2464a`.

## Evidence binding

The released evaluator generated the record and its evaluator companion.
Its evidence_paths name the files retained in candidate b9af631b850c495eace9807361ed3ec3e36a10b2. Observations
obtained after that commit are retained in final-candidate-observations.json;
their SHA256 is `806463b7983be392ff531c7c97944d4e5a1fb7650d3994a59f1dad6b100fa69f`. The capture test checked that digest and all final
candidate/package/build results, then retained the digest and assessment in the
generated record's Candidate test run section. These later observations are not
represented as files that existed in the candidate commit.

## Decision and remaining delivery

The requested decision is verification of VREC-SEH-030 by human mmzen as assurance
owner. That decision covers this exact candidate and retained evidence. The
successor's minimal-layout work is not verified by this record. Release-record
preparation, downstream marketplace/documentation authority, release approval,
publication, latest/last promotion and adoption remain separate.
