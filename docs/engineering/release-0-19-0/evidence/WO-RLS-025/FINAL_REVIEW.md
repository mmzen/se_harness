# Final verification review for SE Harness 0.19.0

VREC-SEH-028 is ready for the human assurance decision. It covers the 14 work
orders selected by REL-SEH-030 and their 11 verification contracts. It binds
candidate `30d4dba2a088c4f83756c1241b76cdab40f796bd`. WO-RLS-025 remains implemented. No verification, release,
merge, publication or repository adoption is recorded by this preparation.

## Final candidate evidence

- The capture ran the complete 1,122-test suite at this exact candidate on
  Windows with Python 3.14.6, four workers and full scale. It passed with 16
  skips. The generated record retains the actual command and result.
- Candidate CI [36339045183](https://github.com/mmzen/se_harness/actions/runs/36339045183)
  passed all eight jobs. Linux source ran 1,122 tests, with two skips, on
  Python 3.11.16 at full scale. Source and installed-package qualification,
  two upgrades on each host, and both integration-package checks passed.
  The PR merge and C have the same Git tree; final-ci-tree-equivalence.json
  records the comparison.
- Manual rehearsal [36339047270](https://github.com/mmzen/se_harness/actions/runs/36339047270)
  passed both legs. The candidate leg built C twice using the pinned Linux
  recipe. Both wheel hashes match; both source archive hashes match.
  build-final.json retains both observations. bundle-0.19.0.json is the
  permanent manifest for later binding to the release record.
- The release-record leg replayed previously released RLS-SEH-027. It proves
  the existing rehearsal path; it is not a 0.19.0 release-record replay.
  That replay follows preparation of the new RLS after human verification.

## Windows checkout finding

The first full-suite capture failed. A retained retry identified one error:
`InstructionMigrationTests.test_recognized_fragments_preserve_all_owner_bytes`
in its CRLF case. This workstation's Git defaults to `core.autocrlf=true`.
It converts the committed LF fixtures to CRLF during worktree creation. The
test then replaces every LF with CRLF again, creating CR-CR-LF input. The
installer refuses that altered fragment as designed.

fixture-line-endings.json records the exact committed and converted bytes.
windows-converted-checkout-failure.log retains the failed test and traceback.
The first diagnostic omitted stdout; the first logging retry also failed
argument parsing before tests ran. Their invocations and results are retained.

The successful capture used a command-local `core.autocrlf=false` setting to
test the exact committed bytes, consistent with the release build's export.
No source, fixture, test or persistent Git setting changed. No test was
removed or skipped to obtain this pass. The default converted Windows checkout
still has this source-test limitation; this work does not claim to fix it.
The human must consider this disclosed limitation when deciding the VREC.
Changing the fixture or repository byte rules needs separate authorized scope.

## Evidence and claim boundaries

The 58 evidence files selected for capture exist at C. They include earlier
verified records, the reviewed implementation evidence, release membership
and release notes. Historical records retain their original commit bounds.
The final CI summaries and build manifest are later observations about C,
retained beside this review in the governance commit. The fresh test run in
the generated VREC also names C. No earlier result is relabelled as a new run.

The raw CI references, downloaded-file hashes and expiry times are in
candidate-final-ci.json and rehearsal-final-ci.json. Source/package/upgrade
raw evidence expires on 2026-10-11; shorter package-artifact expiries are stated
individually. Permanent build identities remain in this directory. Local raw
source output remains outside the repository at the paths in its summaries.

Native delivery inputs are unchanged from VREC-IAR-011. Its accepted evidence
covers Windows Codex CLI 0.155.0-alpha.16.4 and native app server, and Claude
Code 2.1.273, at startup and after manual compaction. It does not establish
desktop UI, automatic threshold compaction, macOS or later host versions.
The upgrade tests use synthetic delivery receipts, not native-host observations.

Plugin 0.2.0 manifests, assembly-plan entries and host documentation are ready.
Final distributable plugin archives still require the independently obtained
public checker wheel after checker publication. The root remains governed by
the isolated released 0.18.0 evaluator.

## Next decision

The human assurance owner reviews VREC-SEH-028 and this evidence, including the
Windows checkout finding, then decides whether to verify or reject the record.
Only verification of this exact record permits the approved preparation of a
ready RLS and its bound replay. A passing test is not that decision.
