# WO-HUP-020 implementation evidence

## Result

The existing assessor reads supported schema-4 plugin ownership and accepts a
same-version provider switch only when evaluator identity and unrelated lock
content are preserved. It reads the catalogue from the trusted base as data.
The plugin side has no catalogued entries; restoration reinstates seed entries.
Managed/fragment changes, malformed ownership and unrelated drift still fail.
Real evaluator upgrades retain their existing exact release/evidence checks.

The clean implementation commit passes both the actual CI planner and assessor against the PR base. The assessor reports not_applicable and invokes no evaluator upgrade.

## Observed checks

- Preliminary focused suite: 28 tests pass, two POSIX-only skips on Windows.
- Local source suite: 1,078 tests pass, 15 skips. The final JSON comparison
  refinement is separately checked by the three passing comparison-regression
  tests, including their schema, seed and identity-drift subcases.
- This local full run started before the final comparison refinement. A fresh
  complete source suite and both CI commands run again on the exact final
  committed candidate during capture; their observed output belongs in the VREC.
- Released evaluator 0.18.0 doctor: 64 checks pass. Graph: 1,661 artifacts,
  zero errors, 48 warnings. Review preflight passes. Current WO and combined PR scope pass. The initial combined PR refusal for missing handoff evidence is retained alongside its successful retry.
- Distribution validation: 15 records pass. Candidate CLI help passes.
- Candidate doctor reports the existing source 0.19.0 versus selected 0.18.0
  differences in router, payload and selected version. Released doctor passes.

## Review and reuse

The implementation adds one comparison in the existing script and reuses the
existing tests and catalogue. Review corrected Python's true/1 equality by
comparing canonical JSON; the refusal test now exercises that distinction.
No workflow, dependency, duplicate catalogue or general migration mechanism
was added. The [review](implementation-review.json) records scope and input
comparisons, including all 17 retained cleanup evidence files, unchanged
evaluator/plugin inputs and both 24-file disposable native profiles.

Earlier discovery observations retain their original host versions and package
limitations. No fresh native execution or full installed-package equality is
claimed. VREC-PLG-022 remains verified for its earlier candidate. The marketplace
ref remains ed68b30c88043773be929540b7b10ae537957c2d.

## Evidence and next stage

[Checks](checks.json) retain commands, exit codes, source hashes, local raw-log
references and observed results. [Source suite](source-suite.log) and
[final comparison regressions](comparison-regression.log) retain the local test
output. The [original failure](original-planner-failure.json) remains visible.
The earlier draft review is a historical preparation observation.

Complete the selected handoff and WO, then prepare VREC-HUP-019 for WO-HUP-020
and WO-PLG-025 at the corrected candidate. Owner verification and hosted CI
remain subsequent decisions/checks. No new correction has been pushed yet.
