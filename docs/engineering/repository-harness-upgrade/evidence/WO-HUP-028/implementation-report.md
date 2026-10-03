# Adoption implementation and current verification status

WO-HUP-028 is **in_progress**. Its reviewed 12-file implementation is committed
at `e5bdb392ea97120ff950c9e160675418cd35fab8`; the exact diff matches the reviewed
proposal. The repository and CI select released evaluator **0.22.0**. Source
reports unpublished **0.22.1**. The installer changed only configuration and
lock, preserved other tracked bytes, and a repeat proposes no writes. The
session activation helper returns the selected 0.22.0 instructions.

## Observed checks

| Check | Result |
| --- | --- |
| Full source suite | Pass: 1,259 tests, 22 skips. |
| Focused adoption suites | Pass: 127 tests, 2 skips. |
| Released identity, doctor and root qualification | Pass. |
| Formal graph validation | Zero errors; 61 existing warnings. |
| Distribution validation | Pass: 22 release records. |
| Source/released version derivation and CLI help | Pass. |
| Real upgrade rehearsal using the CI helper | Pass: trusted baseline 0.21.0 to public 0.22.0. |
| Repository predecessor assessment | Blocked by the obsolete literal release-owner assumption. |

RLS-SEH-032 correctly records human mmzen. The separate
[WO-HUP-029 review](../WO-HUP-029/review.md) proposes the checker/test correction.
No historical release bytes were changed. The prototype is evidence for the
proposal; it is not the repository implementation or completed verification.

## Requirement assessment and limits

REQ-REB-027: actual installer transaction, target identity and repeat behavior
pass. Acceptance remains pending the predecessor correction and final checks.
REQ-IAR-031: owner-file preservation, external-resource resolution and exact
reviewed change surface pass. Hosted CI and combined commit-bound capture remain
pending. Claude and native Codex desktop tests were not run. Direct activation
does not establish native startup or compaction behavior.

The first full-suite invocation overrode the fixtures' line-ending configuration;
one test failed. Removing only that process override restored the fixture's
normal environment. Its focused retry and the full rerun pass. All attempts,
including helper-argument and line-ending preparation failures, are retained.

See [check details](implementation-checks.json) and the [raw outputs](implementation-raw.zip).
Human verification, review publication, and merge have not occurred. Existing
adoption and publication authority remains valid for WO-HUP-028; the two new
checker/test paths require approval of the separate correction.
