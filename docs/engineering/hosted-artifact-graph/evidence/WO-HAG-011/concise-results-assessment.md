# Candidate25: retained instruction reads and report fallback

Candidate `032379d9fb17db5e38ea2de2603f65567041ebdb` improved the clarification
reporting path, but did not establish reliable complete drafting or the efficiency
goals. Historical candidate24 results remain unchanged.

| Trial | Case | Independent result | Seconds | Calls | Peak input tokens |
| --- | --- | --- | ---: | ---: | ---: |
| claude-191 | Clarification | Pass | 173.417 | 3 | 36,710 |
| codex-191 | Clarification | Pass via saved report | 68.543 | At least 5 items | Unavailable |
| claude-192 | Verification draft | Pass | 216.526 | 11 | 56,725 |
| claude-193 | Verification draft | Fail: an asserted condition has no check | 234.264 | 13 | 60,069 |

Codex retained a report that explicitly limits its claims because call capture
is incomplete. This corrects candidate24's missing fallback. It does not repair
Codex telemetry. Both clarification trials left the project at version zero.

The first Claude draft was useful and complete. The next added “no side effects
observed” to its pass condition but planned only a return-value comparison. The
specification mentions external effects, so the issue is the missing check and
the inaccurate complete-content report, not an invented source constraint.
Both drafts were independently read back exactly; all seven imported records
remain byte-identical. No failed or denied native command was observed.

The positive trials missed both duration and context goals. They did not reread
the delivered instruction files. claude-193 did reread the supplied selection,
and both read configuration. Avoiding instruction rereads alone was insufficient.
The compact catalogue view also repeated long absolute evidence paths; pointer
metadata can exceed the small content it replaces. Correct this before the next
candidate. Preserve these observations without combining them with its trials.

The third Claude draft trial and Codex draft trial were not run on candidate25.
The candidate changed to correct the display and make saved-content review match
each pass condition to its planned check. The accepted criteria are unchanged.

Supporting checks passed: 1,337 source tests with 24 skips, focused native/client
and installed-client tests, distributions, CLI smoke, released validation (1,991
artifacts, zero errors, 63 warnings), scope and review preflight. Two pinned builds
matched. Fresh installed EFF-02/03 checks preserved typed/raw equivalence, exact
documents, refusal behavior and original-key recovery after two deliberate faults.
All owned test containers were stopped with volumes retained.

See the per-trial `*-assessment.json`, `*-visible.md`, `*-evidence.zip` and
`*-inventory.json`, plus `candidate25-checks.zip` and its inventory. Private
reasoning and credentials are excluded. The work order remains in progress;
this report makes no verification, merge or complete NQ qualification claim.
