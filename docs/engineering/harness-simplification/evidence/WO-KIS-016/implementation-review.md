# Implementation review for WO-KIS-016

The common grant reader now selects the recorded approval event without
requiring the decision-maker to be named engineering-owner. It rejects an
absent, empty or non-string identity and leaves the scope comparison and both
legacy grant paths unchanged. Transition reasons use work-order approval.

The correction uses the existing record and common consumer; it adds no role
registry, authentication mechanism, lifecycle edge or gate. Supplying a name
remains attribution under the existing authority model. Human decisions and
all required checks still apply. The installed 0.19.0 evaluator is unchanged.

Six added tests cover named approval with separate human/agent executors,
invalid identity, unavailable historical scope, explicit named legacy grant,
completion after handoff, and aggregate verification preparation. Existing
scope/approval/gate and reserved-right failures remain covered. Expected
values are fixture identities and accepted states, not candidate output.
The completion unit test supplies the existing synthetic successful preflight;
actual repository start/review/handoff checks use released 0.19.0 separately.

Before the fix, all three consumer regressions failed on the role-name lookup.
Afterward, the 129 focused tests passed with two existing skips. Full-suite
results are retained separately when available. No full-suite result is claimed
by this review alone.

No accepted definition or historical adoption artifact changed. Diff whitespace
checks pass. The execution note now points to the installed 0.19.0 procedures
and distinguishes candidate behavior from the still-installed evaluator.

Two operational retries are retained: the first planned scope input mistakenly
listed the evidence directory itself as a file; the corrected input enumerated
files and passed without changing scope. The first distribution validation lacked
Git's trust setting for this sandbox-owned checkout; repeating it with a
command-local safe.directory for this exact repository passed all 16 records.
Neither retry weakened a check or changed the approved work.

The first full suite ran 1,131 tests and found three diagnostic-index failures:
a separate missing-identity raise increased the generated diagnostic entry count.
Missing approval and invalid approval identity now share the existing unusable-
approval refusal. Both conditions remain rejected. No diagnostic catalogue edit,
new code or test relaxation was needed. The focused grant and diagnostic checks
pass after the correction; the full corrected result is retained separately.
