# Plugin 0.2.6 preparation review

Status: required qualification is blocked by a reproduced evaluator defect;
no verification decision. Both release preparation work orders remain in progress.
The staged wheel and source are the exact preparation inputs in
[the evaluator review](../WO-RLS-040/qualification-review.md).

| Criterion | Current observation |
| --- | --- |
| Codex CLI 0.159.2 startup above a future clone, activation, resume | Passed with complete selected entry and exact wheel/resource identities. |
| Codex manual and automatic compaction | Passed with native events. |
| Claude Code 2.1.273 startup, activation, resume, manual compaction | Passed with native events. |
| Claude automatic compaction | First bounded run timed out. Recovery of the same actual session observed trigger `auto`, then resumed successfully. Both observations are retained. |
| Two sessions, different release pins, explicit switch/clear | Passed on both hosts, including legacy 0.20.0 and candidate 0.22.1. |
| Selected checkout missing then restored | Both hosts reported a gap without fallback, then recovered; fixture root files remained unchanged. |
| Codex work-order authoring/execution/delivery walkthrough | Passed on two separate checkouts. Drafts stayed unapproved, exact note tests and handoff passed, local commits were retained, and local bare remotes stayed empty. |
| Claude work-order authoring/execution/delivery walkthrough | Draft prepared and refined after review. Execution blocked by an unhandled missing-evidence exception; the second checkout cycle is not performed. Not a pass. |
| Codex Windows desktop | Unverified; CLI evidence does not substitute. Human availability has been requested. |
| Claude context-size boundary | Exact packaged-hook replay delivers at 10,000 UTF-16 units and refuses at 10,001 without truncation. This is adapter evidence, not another native event. Long combined paths still limit delivery. |
| Public fresh/update routes | Not performed: candidate is not published. WO-RLS-042 owns these later observations. |

Actual CLI calls succeeded with existing authorized test authentication. This
does not promise continued session validity. No credentials are retained here.
The native Codex tests and completed walkthrough restored the disposable
profile's previous marketplace; readback matched the original profile. Claude
used a session-only plugin directory. Normal workstation profiles were not changed.

[Raw native traces](native-initial.zip) and [their byte index](native-archive.json)
retain host/session identities, prompts, hook contexts, events, failures and
adapter commands. The complete package inventory and both host inventory digests
are retained beside this review. Native events are distinct from unit fixtures.

[The walkthrough archive](native-walkthroughs.zip) and
[its byte index](native-walkthroughs-index.json) retain the later native events,
individual command reviews, original failures, guided recovery and independent
assessments. The two Codex assessments pass. The Claude assessment is explicitly
false: the approved fixture work never started or completed, its note remains
unchanged, and no commit, push or verification/release record was produced.

Claude's first draft proposed a directory-wide work-order scope and an
unconfirmed machine assurance table. Review narrowed the path and moved the
proposed required classification into prose. Both attempts are retained; this
was a guided correction, not an unassisted authoring success. An initial native
permission-transport setup failure is also retained, followed by the corrected
documented stdio transport. No persistent permission rule was installed.

## Reproduced release blocker

With a valid unapproved draft declaring future evidence, the candidate's
transition planner reads that absent file before it can plan an unrelated
approved work order. The native preview crashes with FileNotFoundError.
[Windows](missing-evidence-windows.json) and [Linux](missing-evidence-linux.json)
installed-wheel probes reproduce the failure, with valid graphs, passing start
preflight and identical before/after file digests. No apply was attempted.

The failing file belongs to unapproved WO-FLW-002. It must remain absent in
this scenario; creating dummy evidence or removing its declaration would avoid
the case rather than verify it. See [the correction review](correction-review.md).
No product correction has been implemented under the preparation approval.

The earlier long-path report concerns the combined instruction context, not
a filesystem MAX_PATH test. [The current boundary replay](claude-context-bound.json)
measures 9,989 units for its short fixture, exactly 10,000 for a longer path,
and an explicit gap at 10,001. It preserves the limit and all root file bytes.
These measurements do not claim arbitrary paths or desktop support.

These observations do not verify hosted service behavior, accept omitted criteria,
publish the marketplace, authorize a release or adopt a new evaluator.
