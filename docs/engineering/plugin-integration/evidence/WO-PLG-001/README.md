# WO-PLG-001 implementation evidence

**WO-PLG-001 is implemented** following the operator's explicit completion
decision on 2026-09-09. The [applied transition](governance/completion-20260909/completion-applied-01.json)
records that decision. The operator separately authorized ready verification-record
preparation. No assurance, release or publication decision is recorded.

## Implementation and input identity

Two repository-owned entry files assemble shared committed assets into separate
Codex and Claude archives. Wheel verification precedes copying; acceptance
compares the complete output with the committed source, including inventories
and ZIP bytes. See the [usage and boundaries](../../../../../tests/plugin_integration/package_assembly/README.md).

The tested code, fixture plan and manifests are at
`32a0c69d6b08fb8428afe4ec4615b5748bb8bea6`.
[Implementation input hashes](implementation-inputs.json) identify the code.
Later synchronization with main introduces notes only; it does not change the
assembly inputs. Later evidence commits retain these observations.

The selected evaluator is the published `se-harness` **0.17.0** wheel:

- Expected archive SHA-256: `305c7cbc79f87baa76ea3bea939b134999f9cad3bfdfa0b4c9c2fd2d9caacced`.
- Independent canonical payload SHA-256: `dd48b16b69d90a04412f458c756876ec22a687c99282075e69d0f58316c43405`.
- [RLS-SEH-026](../../../release-0-17-0/releases/RLS-SEH-026.md) at
  `cb4255a985c5bb85afeda7c2a5f3ad9d311ac05b` supplies the immutable released record.
- [PyPI metadata](governance/pypi-0.17.0.json), fetched from
  `https://pypi.org/pypi/se-harness/0.17.0/json` on 2026-09-09, independently
  supplies the archive digest. [C01 calculations](C01/independent-calculations.json)
  and both retained inventories agree with it.

The checker used the external released evaluator environment. It did not import
or rebuild the candidate evaluator. No interpreter is included in either archive.

## VER-PLG-001 observations

All eight cases passed on **Windows 11, Python 3.14.6**. Each case retains the
runner and command arguments, exit statuses, raw stdout/stderr, source or fixture
revision, and separate expected/observed values. These are execution observations,
not an assurance-owner decision.

| Case | Observed result | Evidence |
| --- | --- | --- |
| C01 | Exact wheel bytes and shared source match in both packages; repeated archives match. | [Observations](C01/observations.json), [Codex inventory](C01/codex-inventory.json), [Claude inventory](C01/claude-inventory.json) |
| C02 | Missing and single-byte-corrupted wheels return nonzero; no output is accepted. | [Observations](C02/observations.json) |
| C03 | Runtime, candidate wheel, extra dependency and top-level bin inputs are rejected. | [Observations](C03/observations.json) |
| C04 | Missing shared source and divergent host output both fail acceptance. | [Observations](C04/observations.json) |
| C05 | Each host has its own manifest; a shared/host destination conflict is rejected. | [Observations](C05/observations.json) |
| C06 | An escaping path is rejected before output; outside sentinel bytes/listing stay unchanged. | [Observations](C06/observations.json) |
| C07 | Omitting a file from the inventory fails; the diagnostic names that file. | [Observations](C07/observations.json) |
| C08 | One-file partial output and same-directory retry fail; a fresh complete retry passes recheck. | [Observations](C08/observations.json), [interruption trace](C08/interruption-trace.txt) |

PLG-PKG-001–003 map to C01–C03; PLG-PKG-004 maps to C01/C04;
PLG-PKG-005 maps to C05; PLG-PKG-006 maps to C01/C07; PLG-PKG-007 maps
to C05–C08. This preserves ARCH-PLG-001/ADR-PLG-001's shared payload and
separate host packaging. Runtime creation and native adapters are separate work.

## Checks and original failures

- [16 focused boundary tests](repository-checks/focused-tests-02/stderr.txt): pass.
  They include Git executable-mode preservation, host-only scripts, candidate
  import prevention, unsafe names, hard links and source symlinks.
- [Codex fixture layout validation](repository-checks/codex-fixture-layout-02/stdout.txt): pass.
  The original [failure](repository-checks/codex-fixture-layout-01/stdout.txt)
  identified missing author/interface metadata. That fixture was corrected and
  all eight cases rerun. The [first case run](attempts/acceptance-01/) is preserved.
- [Released graph validation](repository-checks/validate-01.json): zero errors.
  [Managed integrity](repository-checks/doctor-01.json),
  [distribution metadata](repository-checks/distribution-check-01/stdout.txt) and
  [candidate CLI help](repository-checks/candidate-help-01/stdout.txt): pass.
- [Repository suite](repository-checks/repository-tests-01/stdout.txt): 1,119 tests,
  initially one failure, one error and 23 skips. The owner-region size failure
  came from CRLF checkout expansion. Restoring **identical committed LF bytes**
  to AGENTS.md left no Git diff and the [targeted recheck passed](repository-checks/owner-region-recheck-01/stderr.txt).
- The remaining Windows `IdentifierAllocationTests` error occurs while deleting
  a read-only Git object in a temporary fixture. It [also reproduces on unchanged
  main](repository-checks/baseline-failures-01/stderr.txt) at `cb4255a9`.
  It is outside WO-PLG-001's declared paths. This is an unresolved repository
  check error, not a passing result or an accepted exception. No test or required
  check has been disabled. The report-capture helper also encountered a console
  encoding error after saving the first suite output; the raw files and command
  exit status were retained, and later helper output uses UTF-8.

## Hosted checks and completion

All seventeen GitHub checks passed for delivery commit
`216726cfbd7920826c7eec02888e3a4a448cae3b`, including the full Linux
regression suite: 1,119 tests, four skips.
[The retained PR snapshot](governance/completion-20260909/completion-ci.json) and
[candidate workflow result](governance/completion-20260909/completion-candidate-ci.json)
identify the runs, head commit and outcomes. These hosted checks do not replace
the separately retained Windows C01–C08 assembly observations.

## Limits and handoff

Linux, macOS and Python 3.11 assembly runs are unavailable. The focused suite
checks Windows reparse-point rejection with a simulated attribute; it does not
claim a live junction-race test. Build into a private directory without concurrent
writers. The file policy is not an arbitrary-code malware scanner.

The sample packages are inert and non-promotable. They establish no production
skills, hooks, bootstrap behavior, native host activation or marketplace support.
Focused tests run explicitly; top-level unittest discovery does not include them.

The operator made the completion decision after these limits were presented.
The local Windows cleanup error remains disclosed; the hosted Linux regression
passed. No failed local run is relabeled as passing. Any out-of-scope fix needs
its own authority. The operator also authorized VREC preparation; assurance
still requires a separate decision against the exact bound candidate.

The `governance/` directory retains the released evaluator's packet readings,
approval/start plans, applied results and independently fetched PyPI metadata.
The reviewed packet source is `be8b4126f6b9147dff8dec2ceaac5a79d59953f7`.
