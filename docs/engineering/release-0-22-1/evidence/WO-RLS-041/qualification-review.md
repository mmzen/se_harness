# Plugin 0.2.6 preparation review

Status: required qualification remains in progress; no verification decision.
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
| Work-order authoring/execution/delivery walkthrough | In progress in disposable fixtures. |
| Codex Windows desktop | Unverified; CLI evidence does not substitute. Human availability has been requested. |
| Claude earlier long-path limitation | Unverified in this release; short-path native results do not close it. |
| Public fresh/update routes | Not performed: candidate is not published. WO-RLS-042 owns these later observations. |

Actual CLI calls succeeded with existing authorized test authentication. This
does not promise continued session validity. No credentials are retained here.
The native Codex tests restored the disposable profile's previous marketplace.
The subsequent walkthrough uses the same disposable profile and will restore it
on completion. The normal workstation profiles were not changed.

[Raw native traces](native-initial.zip) and [their byte index](native-archive.json)
retain host/session identities, prompts, hook contexts, events, failures and
adapter commands. The complete package inventory and both host inventory digests
are retained beside this review. Native events are distinct from unit fixtures.

These observations do not verify hosted service behavior, accept omitted criteria,
publish the marketplace, authorize a release or adopt a new evaluator.
