# Final integrated qualification assessment

The schema-5 verification defect is corrected in committed candidate
3f438bb894e4108fa369a9dc048d69f5e0c2e8ab. The new installed-wheel lifecycle and
assurance checks pass on Windows and Linux. Native Codex CLI and Claude delivery,
including automatic compaction, pass with that exact wheel. Codex desktop remains
unverified. This assessment does not declare complete desktop qualification or
waive its requirement. The human previously directed us to retain that result
as unverified and continue; VREC-IAR-019 records the earlier assurance decision.

## Candidate, coverage and evidence

The wheel SHA-256 is
a27a797bf2763f48006d28166d41e21437c8c4a935615a1b114e9ff278434594.
Its payload SHA-256 is
c86a3301491e4ef4188ed98e2fcf8c67bf2c8184bc5e73e97e663f235c7894ac.
It is a qualification build, not a release artifact. The actual repository still
uses released 0.20.1. No adoption or external action is included.

The selected aggregate scope is WO-IAR-028, WO-IAR-029, WO-IAR-030,
WO-IAR-034, WO-IAR-035, WO-IAR-036, WO-IAR-037, WO-IAR-038 and WO-IAR-039,
with VER-IAR-020, VER-IAR-021 and VER-IAR-022. Later record/evidence commits
must preserve these tested package inputs. Capture will bind the final clean
candidate and every evidence file explicitly, not just this index.

Fresh full commands, outputs, actual native events and driver versions are in
../WO-IAR-039/qualification.json. The regression failures before the fix and
source tests are in ../WO-IAR-039/implementation.json. The earlier Windows/Linux
E012 failure and original migration passes remain in
integrated-lifecycle-and-migration.json. Historical reports describe the stage
when written; they are not rewritten to hide earlier failures or pending work.

## VER-IAR-020: packaged resources and evaluator parity

| Criterion | Assessment and evidence |
| --- | --- |
| Selected resource identity | Passed. Fresh released-0.20.1 candidate-package qualification passes on both platforms with the independent expected manifest. Installed resource/domain checks pass without repository copies. |
| Artifact authoring | Passed. Fresh installed domain/authoring checks run on Linux, with the earlier equivalent Windows domain tests and current source regression suite. Requested drafts use packaged templates. |
| Policy and discovery parity | Passed for tested cases. Current resource/provenance regressions and full suite preserve lifecycle results and discovery. Fresh actual installed lifecycle passes from draft definitions through ready VREC and assurance gates on both platforms. No assurance decision is applied in those fixtures. Earlier WO-IAR-028 reports predate the completed result-wiring correction. |
| Refusal boundaries | Passed for tested boundaries. Current malformed/unknown locks, identity mismatches and copied policy fail without writes. Existing resource/path/evidence safety regressions pass; fresh Linux installed tests exercise an actual symlink. |
| CLI/CI independence | Passed in portable fixtures with the exact same wheel and socket-denying CLI runner. No host plugin is installed in those evaluator environments. This is not a claim that native model sessions ran without network. |

## VER-IAR-021: host delivery

| Criterion | Assessment and evidence |
| --- | --- |
| Bootstrap and activation after cloning | Passed natively in current Codex CLI 0.159.2 and Claude Code 2.1.273. Sessions start in the parent before cloning; activation uses the resulting exact checkout and native session. |
| Native compaction and resume | Passed for both CLI hosts with the corrected wheel. Claude emits trigger=auto in an ordinary data-analysis turn, then resumes with the same entry. A separate actual selected-entry startup/manual-compaction run passes. Codex observes manual compaction, resume and automatic compaction. Full exact entry bytes match the independent wheel entry. |
| Two releases and plugin update | Passed observed historical native cases in ../WO-IAR-029/native-tests.json and native-traces.json; current Windows 41-step adapter replay passes. Reused adapter, resolver, runtime-identity and entry-template Git inputs are unchanged from e79368c677541d7092129a853e8b39157865ace9. This is not a claim of a new native plugin-update run. |
| Parallel sessions and setup | Passed observed historical native interleaving and current portable setup/adapter regressions. Prior event traces are retained; fresh startup/recovery tests use a new native session for each host. No global last-selected repository is introduced. |
| Selection failure, switching and clear | Passed retained native cases and current 41-step adapter replay. Missing, corrupt and conflicting inputs remain refusal cases in the full suite. |
| Offline and unavailable resources | Passed portable resource/adapter checks; current CLI audit blocks socket operations. No offline model-session claim. |
| Repeated work and delivery handoff | Passed retained native Codex walkthrough on two selected releases, including new drafts, approved/resumed work, complete scope and exact push/PR authority boundary. See ../WO-IAR-029/cli-workflow.json and cli-workflow-traces.json. Fresh installed lifecycle now additionally passes verification preparation and gates. No product push or PR is performed. |
| Packaging and ownership | Fresh assembly of both host packages and 41-step adapter replay pass. Current native repositories retain their bytes; the disposable Codex profile is restored. All packaged input files except validation_evidence.py match the preceding candidate exactly. Prior host-input newline equivalence is retained in integration-followup.json; do not call those historical raw bytes identical. |
| Codex Windows desktop | **Not assessed / unverified.** CLI/app-server evidence is not desktop proof. The existing human instruction to continue does not turn this criterion into a pass. |

## VER-IAR-022: installation and migration

| Criterion | Assessment and evidence |
| --- | --- |
| Fresh footprint | Passed on both platforms. Default initialization creates exactly config and lock. Explicit Git preview writes nothing; apply adds the declared attributes only. Current installer regressions cover selected CI/PR integrations and repeat setup. |
| Governed evidence | Passed on both platforms through ready record validation and applicable assurance gates. Bound evidence SHA-256 matches: 30cfd89c1ef54dae2ba88d755be1346584fa3f06675393020d005cf3d7c21c26. The exact implementation-note bytes also match. Fixture commit IDs, timestamps and OS interpreter origins differ as expected. |
| Safe retirement | Fresh installed migration passes from released 0.20.1 with native replacement-delivery receipts. Reviewed managed copies and one selected stock seed retire. Owner binary instructions, notes, formal history and unselected templates retain every byte. Missing receipts and customized seeds refuse without writes; link/identity boundaries remain covered by the integrated suite and installed Linux probes. |
| Recovery | Passed on both platforms. Fault injection at the installed lock-write boundary rolls back every original byte with real authority and receipt checks enabled. Normal apply, doctor and repeat no-op then pass. |
| References and integration | Full source suite passes: 1,211 tests, 20 skips. Distribution validation passes all 20 distribution-bearing records. Current package, documentation, catalogue, guide-heading and installation tests pass. The active guide describes parent startup, clone activation, recovery and parallel sessions. Historical references retain their release provenance. Native limits are as listed above. |

## Corrections and remaining decision

Only one production file changed for WO-IAR-039. The existing lock validator
checks schema 5 before evaluator evidence is compared. Legacy formats and the
ordinary/full-payload inspection distinction are preserved. Two new regressions
failed before the fix and pass afterward; 68 focused tests passed with 3 skips.

The first new Codex probe used an existing log destination; it stopped and
restored the test profile. The retry passed with a new destination. The first
new migration probes had a driver-string indentation error; corrected probes
pass on both platforms. All failures remain in the raw qualification record.

Proceed with the released handoff/completion/capture procedure under existing
work approvals, preserving the desktop gap for the accountable human. Human
verification, external publication and future release/adoption are separate.
