# Verify the README correction

**Decision requested:** Verify VREC-PLG-034 for candidate
`fc5f7356a82f5450fe21438ab8d4419ce10625e3`, covering WO-RLS-037 under VER-RLS-001.

The correction removes only the second duplicated host-limit paragraph. The
README now has **648 words**, below the unchanged 650-word limit. The complete
warning remains beside installation. All unique claims, commands, versions,
links and images remain unchanged. The file exactly matches the approved proposal.

**Checks:** All 44 tests in the three required onboarding/documentation modules
pass on Windows. Capture repeated those checks in a clean checkout of this
exact candidate. Scope, start/review preflight, handoff and capture pass. Formal
validation reports zero errors and 61 separately retained repository warnings.

Read the [verification record](../../verification-records/VREC-PLG-034.md),
[implementation review](implementation-review.md), [test results](implementation-checks.json),
and [checks](checks.json). The original CI failure remains in [ci-failure.json](ci-failure.json).
Fresh full candidate-source CI is required on the corrected PR head before
merge; consult PR #530 for the current result. This frozen record does not claim
a future CI result passed.

VREC-PLG-032 and VREC-PLG-033 retain their existing human decisions and evidence.
Claude Code and Codex Windows desktop remain **not tested / unverified**.
Packages, evaluator selection, provider settings and release markers are unchanged.

If the corrected candidate is accepted, reply:

> I verify VREC-PLG-034 as assurance owner.

The agent will record and push that decision. Merge remains a human action and
requires passing CI. Documentation readback and the already-authorized marker
promotion remain after integration; overall delivery is not yet complete.
