# WO-IAR-036 regression review

Human mmzen approved WO-IAR-036 and its proposed required commit-bound
verification in VREC-IAR-020. Released evaluator 0.20.0 applied approval and
start. The work order remains in progress.

## Changes

- CLI shape: preview shows only the two selection files and writes nothing.
  An explicitly selected conflicting Git block returns failure and preserves
  every observed file. The refusal assertion now always runs.
- Glossary: keep the legacy seed check. Minimal init creates no glossary and
  preserves existing owner bytes, including CRLF, without tracking that file.
- Template drafting: use an explicit external-resource unit origin. Preserve
  completion-authority assertions and check that no template copy appears.
  The domain-creation stage exposes the remaining product defect.
- Onboarding: retain both legacy LF and CRLF commit/doctor scenarios through
  explicit legacy fixture construction. Production CLI dispatch is unchanged.
- Installed wheel: retain legacy skill membership and uniqueness checks. Build
  the complete canonical fixture payload, install it into a disposable environment,
  and use isolated Python outside the checkout. Check the two-file footprint,
  actual resource paths and digests, wheel identity, empty validation, repeat,
  missing Git readiness, and separately previewed Git/CI/PR integrations.

## Review and evidence

Reuse the existing test framework, resource resolver and explicit fixture helpers.
There is no production fallback to source assets. The expected footprint and
integration sets are literal contract expectations. Owner-file and refusal checks
remain active. No test was skipped to make the new layout pass.

The first focused run found two incorrect test assumptions and one product defect.
CI workflow files are editable seeds; the conflict test now selects the managed
Git block. Installer JSON uses the existing action `add`, so the preview assertion
uses that field. Both corrections passed on the second run.

The second focused run executed 81 tests: one failure and two existing skips.
The stable full suite executed 1201 tests: one failure and 19 skips. Both runs
fail only at domain creation after minimal init. Distribution validation passed
for all 18 distribution-bearing records. Formal validation reported zero errors
and 54 existing unrelated warnings. The diff whitespace check passed.

All observed outputs are retained in tests.json, including earlier failures.
These are implementation progress results, not final verification acceptance.

## Remaining work

WO-IAR-037 proposes the required correction in se_harness/artifact_layout.py,
which is outside the active approved scopes. Keep the failing regression and
fix the implementation only after that proposal is approved. The draft creates
and previews missing parents through the existing checked authoring path and
preserves rollback and owner content. Its reviewed SHA256 is
cc5d39fc7371afefaec8b6b27ad29ae4f812a1664a882c8967161ea37639a625.

Final packaged and native qualification, complete handoff, exact candidate capture
and VREC-IAR-020 preparation remain outstanding. The released CI verifier's
old-layout assumptions are a separate integration dependency already recorded
in WO-IAR-030 progress evidence. No release, adoption or external action occurred.
