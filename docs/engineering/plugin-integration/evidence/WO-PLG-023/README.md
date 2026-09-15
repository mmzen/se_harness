# Marketplace implementation evidence

## Inputs and authority

The owner approved REQ-PLG-038, SPEC-PLG-022, VER-PLG-023 and WO-PLG-023
on 2026-09-15: "OK i approve the artifacts you can start". The released
evaluator recorded those exact approvals and started WO-PLG-023 under DR-015.
This evidence covers that work only. Earlier prototype packages remain preliminary.

The accepted marketplace was built from source commit
`041e2584e8ed91d05af0ade13b92ab07cfbeea3b`. Its inventories and archives are
unchanged native-builder output under `packages/`. The later candidate contains
this source, the independently exercised acceptance-parser correction and these
records; it does not change a packaged input. The VREC names that clean candidate.

The governing evaluator is the isolated released SE Harness 0.18.0. See
[its runtime identity](evaluator-identity.json), [build result](marketplace-build.json)
and [complete distribution identity](PACKAGE-IDENTITY.json).
The supplied wheel archive SHA-256 is
`a683dbdf485d42aa20ea8502122c171a4c61c7d60f85db5b5f264bd336371c54`;
payload SHA-256 is
`cf28e03f21a0e474af8c415499c69193ab2a20e08a95c0ad3514758a84cff54d`.
The same released wheel is installed with `--no-index --no-deps`; plugin
installation alone does not install the checker or fetch it from PyPI.

## Measured coverage

| Contract / method | Observed result |
| --- | --- |
| VER-PLG-023 M01; VER-PLG-001 C01, C04-C05 | Exact-source build and independent check passed. Both native plugins contain their own manifest, shared skills, setup helper, license and unchanged released wheel. Native validators accepted both packages; Claude accepted the catalog, and Codex accepted it during native installation. |
| VER-PLG-023 M02; applicable VER-PLG-001 boundaries | All 22 focused assembly tests passed, including the six new composition tests. Fixtures cover missing, escaping and wrong-host sources, incomplete packages, altered outputs, extra directories, existing destinations, hardlinks and interruption; existing package tests cover wheel and shared-source boundaries. |
| VER-PLG-023 M03; VER-PLG-016 walkthrough | 26 native commands completed with their expected results in fresh Windows profiles. Each host's 24 installed package files matched the accepted distribution byte for byte. All five skills were packaged; Codex's implicit discovery exposes the four ordinary skills and preserves explicit-only operator briefing. |
| VER-PLG-023 M04; VER-PLG-016 guide review | Listing copy, logo, five positive and three negative reviewer scenarios identify the complete package, offline setup, host data-policy boundary and outstanding publisher inputs. Scenarios describe expected agent behavior, not measured model evaluations. |
| Repository checks | Full source suite: 1,068 tests, 15 skips, exit 0. Distribution validation: 15 records, exit 0. Candidate CLI help: exit 0. Governing doctor: 70 passing checks. Governing graph: 1,647 artifacts, zero errors, 48 existing maintenance warnings. Review preflight passed without diagnostics. |
| VER-PLG-023 M05 | Not run: the public distribution branch has not been published. This observation belongs after authorized external delivery. |

See [native results](native-summary.json), [command evidence](commands.json),
[focused checks](focused-retained.json) and [full suite output](full-suite.log).
The general source discovery does not descend into the separate assembly test
directory; the focused run is additional coverage. The full suite began with the
implementation uncommitted and continued across its source commit; tested files
were unchanged throughout. The sole later code edit is in the separately run
native acceptance script, not the packaged implementation or discovered suite.

Native versions were Codex CLI 0.154.0-alpha.6.2 and Claude Code 2.1.269, with
Python 3.13.3 on Windows. Both installed from the local marketplace, discovered
skills, installed the bundled checker, observed the expected missing-project
doctor result, previewed/applied initialization and plugin ownership, passed
doctor, and repeated setup successfully. Real user profiles and credentials
were not used. No model calls, native macOS/Linux runs, public Git installation,
provider scanner or portal submission are claimed.

## Ordinary review and resolved findings

- Composition reuses the existing native builder, inventory checks and archive
  validation. A fixed asset map and two fixed catalog paths add the necessary
  packaging behavior; no generic manifest language, hook, installer or CI lane
  was introduced. The existing assembly module needed no change.
- Packaging LICENSE through the shared plan and display metadata through source
  removes the prototype's post-build overlays. The committed source remains the
  oracle, and root identity hashes include native archives and wrapper files.
- The first native run installed Codex successfully but the new test script
  attempted to parse setup's entire stdout as JSON. Actual setup includes pip
  progress before the doctor's JSON. The parser now separates that prefix and
  still requires the explicit missing ENGINEERING_HARNESS.md result. The original
  failure is retained; the corrected script passed the full fresh two-host run.
- A temporary evidence wrapper hit a Windows console UnicodeEncodeError after
  three successful checks. Their results were already saved. The remaining
  Claude catalog validation ran separately and passed; no package change was
  made for that display error.
- A repeat of the separate assembly suite was mistakenly launched with system
  Python, which lacks the released package required by its isolated payload
  hashing tests. Its six new composition tests passed, but dependent existing
  tests failed. That run is retained; the corrected invocation uses the released
  evaluator environment specified by the test directory's README.
- Installer, setup script and skill instructions are unchanged. Host READMEs,
  the plan's license entry and operator-brief display fields are the only shared
  package-source changes from the previous baseline. Native setup was rerun;
  no preliminary prototype success substitutes for the committed composition.
- The installation guide explicitly distinguishes local acceptance, future Git
  delivery and provider review. Publisher identity/contact, legal URLs, regions
  and attestations remain owner inputs in the submission drafts. The supported
  Anthropic route is its community marketplace; an official curated listing is
  not promised.

Raw outputs remain in the local workspace at
`work/plugin-publication-governance/` and
`work/plugin-marketplace-governed-acceptance-retry/`. `commands.json` retains
actual arguments, exit codes, relevant output excerpts and raw byte digests;
short test logs and package identity are retained here. No CI artifact upload,
remote retention period or public availability is asserted. Later verification,
Git delivery and provider decisions are separate from these observed checks.
