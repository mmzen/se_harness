# Verification review: concise Claude follow-up

The README correction changes only the approved Claude follow-up paragraph.
The README now has 644 words, 104 lines and seven level-two headings, within
the accepted limits of 650 words, 200 lines and seven headings. It preserves
the evidence link and all three unverified areas. No product or test change
was needed.

## Requirement assessment

| Requirement | Result and evidence |
| --- | --- |
| REQ-DST-069 | Pass. The actual README matches the approved patch. Counts and links pass; all other content, commands and images are preserved. |
| REQ-RLO-020 | Pass. The paragraph states the observed Windows subset and links the dated report. All remaining gaps and historical authority are explicit. The five other corrected guides are unchanged from WO-RLS-038. |
| REQ-IAR-030 | The passing native instruction-delivery assessment from WO-RLS-038 is reused without changing its observations or inputs. This correction adds no native coverage. |
| REQ-RLO-019 | The matching public fresh/update inventories and independent 29-file package comparison from WO-RLS-038 are reused unchanged. |

[Implementation checks](implementation-checks.json) retain the actual word count,
file digests, focused and full-suite results, validation and preservation checks.
[Raw results](implementation-raw.zip) retain commands, runtimes, output and the
approval/scope results. [The previous CI failure](ci-failure.log) and
[the reviewed patch](proposed-readme.patch) show the defect and its correction.
The failure came from exceeding the existing 650-word limit; the test and
accepted budget are unchanged.

All 44 focused tests pass. The full-suite result is recorded in the linked
checks with its actual skips. Released evaluator 0.22.0 validation has zero
errors and 61 existing warnings. Handoff and completion results are retained
in completion-raw.zip before candidate capture. Hosted CI is assessed after
publication and must pass before reporting the correction as merge-ready.

The first local full run had one release-plan fixture error among 1,262 tests
with 22 skips. The transient test driver forced core.autocrlf=false into every
fixture, preventing the platform-written plan from being normalized to the
LF bytes expected by that fixture. Removing that driver override preserves
the normal workstation configuration and each fixture's own settings. The
specific failing test and full suite were rerun unchanged; both attempts are
retained. No repository code, test or setting was changed to resolve it.

The original [Claude assessment](../WO-RLS-038/verification-review.md), every
WO-RLS-038 evidence file, WO-RLS-038 itself, and VREC-RLS-001 remain unchanged.
VREC-RLS-001 retains its human decision for its original candidate. A fresh
combined record covers WO-RLS-038/039 and VER-RLS-002/003 at the corrected commit.
Its exact record and candidate will be linked in PR #533 before verification.

## Limits and decision

Codex Windows desktop, the full Claude author/work-order execution/delivery
walkthrough and the earlier long-path failure remain unverified. Native tests
used short paths, tools disabled and --plugin-dir; separately observed public
installation profiles had matching package bytes. Existing risks stay accepted
and open for follow-up under DEC-RLS-005/006; DEC-RLS-007/008 bound the supplement.
This review does not add a host test, close a risk or alter the released package.

The correction uses one paragraph and existing tests. Detailed coverage stays
in the linked evidence, avoiding duplication in the public entry. The approved
scope is sufficient; no broader implementation or architecture is needed.

Human verification of the corrected candidate and merge remain separate.
