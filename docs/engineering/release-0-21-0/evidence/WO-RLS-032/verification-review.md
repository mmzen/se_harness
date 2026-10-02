# VREC-PLG-030 verification review

## Decision requested

Human mmzen, as assurance owner: decide whether VREC-PLG-030 verifies candidate
`967d513d20348ca20f78b4b2d4235c33fc8748d4` for WO-RLS-032 under VER-RLS-031 and
VER-IAR-021. The record is **ready**, and the proposed verification gates pass.
No human verification has been applied.

Suggested decision: **I verify VREC-PLG-030 as assurance owner.**

## Results and accepted gaps

- Plugin 0.2.4 assembly and independent package checks passed with the public
  evaluator 0.21.0 wheel. Package identity:
  `74f0854eadfbe962105d1aba9b594ff2f1697cd038cb27c1a01b802c1fb8d890`.
- Windows and Linux portable qualification each passed 41 steps.
- Native Codex CLI/app-server observations cover startup, activation, manual and
  automatic compaction, resume, separate selections and repeated work. Both
  disposable workflow repositories passed independent readback; neither was pushed.
- Fresh candidate capture ran 45 focused tests: zero failures/errors, two skips.
  The skips are Windows symlink creation and the optional real-wheel setup test.
  Exact-wheel setup and portable qualification are retained separately.
- Claude native qualification for these exact release bytes and Codex Windows
  desktop remain **unverified**. DEC-RLS-002 and RISK-RLS-002 record your acceptance
  for WO-RLS-032/plugin 0.2.4 only. No host pass is inferred from this acceptance.

Revisit the risk before the next plugin release, before claiming either route
verified, or before adoption relying on either route, whichever comes first.
The earlier verified source's 1,215-test Windows/Linux results are reused only
because product source and tests are unchanged; they are not new runs.

## Capture provenance

The first capture stopped on Windows text decoding. The second failed because
its Python environment lacked the installed evaluator required by package-assembly
tests. Neither wrote a verification record. The successful third capture used the
released 0.20.1 interpreter and explicit UTF-8. Candidate source, test assertions
and all 30 selected evidence files remained unchanged. The revised external
capture driver's complete source and SHA-256, all refusals, successful output and
the independent runtime identity check are in [capture-preparation.json](capture-preparation.json).
The generated record binds its test command and output to the full candidate above.

This review and capture-preparation.json are later preparation receipts. They do
not replace or modify the candidate-bound evidence.

## Review sources

- [Ready verification record](../../verification-records/VREC-PLG-030.md)
- [Generated evaluator provenance](../VREC-PLG-030-evaluator.json)
- [Criterion-by-criterion assessment](contract-assessment.md)
- [Accepted decision](../../decisions/DEC-RLS-002.md)
- [Accepted risk](../../risks/RISK-RLS-002.md)

WO-RLS-032 remains implemented. Verification does not authorize marketplace
publication. WO-RLS-033 public-route checks, latest/last and repository adoption
retain their separate conditions and authority.
