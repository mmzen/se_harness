# VREC-RLO-013: ready for human verification

Record: [VREC-RLO-013](../../verification-records/VREC-RLO-013.md).
Candidate: `931945180bbaa0d1932b055a426e5b7e407a83ce`.
Scope: WO-RLO-013 and VER-RLO-010 only.

The selector correction preserves RLS-SEH-030 and its archived copy. It selects
canonical formal records, rejects actual duplicates, and excludes file symlinks.
Its status, distribution and bound-recipe checks are unchanged.

## Evidence assessed

- All 28 release-build tests pass on Linux. Windows passes with three platform
  skips; Linux exercises the symlink test. Pre-correction failures are retained.
- The initial full Windows suite passed 1,215 tests with 21 skips. Capture reran
  that suite in a clean temporary checkout of the exact candidate: 1,215 tests,
  21 skips, exit 0. The result is in the generated record's Candidate test run.
- Manual hosted run [36923985433](https://github.com/mmzen/se_harness/actions/runs/36923985433)
  ran at that same review commit. Both legs passed. RLS-SEH-030 rebuilt released
  candidate b9af631b850c495eace9807361ed3ec3e36a10b2 and reproduced both bound hashes.
  The capture command checked the actual downloaded receipt's SHA-256 and retained
  the exact run, ref, distribution and comparison identities in its output.
- Distribution validation passes for 20 records. Released 0.20.1 reports zero
  validation errors and a passing transition checkpoint for VREC-RLO-013 to verified.
- Only completion and retained evidence differ from the tested implementation
  commit 73f6500bfdfabc3bae2d84974b9f3b9f45ac90b2. Source comparisons are retained.

The record is ready, not verified. The accountable human may verify, reject or
supersede this exact record. Suggested response from the released evaluator:

> I verify VREC-RLO-013 as assurance owner.

This decision covers the repository replay correction. It does not accept the
aggregate v0.21.0 release, its missing Codex Windows desktop evidence, or a release
record. PR #517 remains draft. No release, marketplace or tag was published.

The new preparation receipts preserve the final hosted evidence and readback.
They do not overwrite any evidence already bound by the ready record. Earlier
pending observations remain as historical snapshots alongside their later results.

The default Git whitespace check flagged carriage returns in the evaluator's
embedded Windows command output. The generated record was preserved byte for
byte. An invocation-scoped `core.whitespace=cr-at-eol` check passed; it treats
those CR line endings correctly while preserving other whitespace checks. No
repository Git configuration, captured output or bound evidence was changed.
