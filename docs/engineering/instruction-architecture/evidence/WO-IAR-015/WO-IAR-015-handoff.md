```toml
artifact = "WO-IAR-015"
checkpoint = "handoff"
formal_snapshot_sha256 = "2461f49364133adb2e8736cb206fa44ddf4ee39889efc53c0fbd28d936ac430a"
rebound_at = "2026-09-27T16:36:53Z"
```

# WO-IAR-015 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Retained observations

Host delivery and skill routes are retained for review.
delivery-final-focused.stderr records 18 tests with two skips.
claude-native-startup-final.assertions.json and the sanitized log record
observed Claude Code startup on Windows. Codex native delivery and native
post-compaction delivery remain unverified. Unit fixtures are not native proof.

This is an interim handoff for the draft PR. The work order remains
in_progress. Native qualification gaps remain open; this packet and a
passing mechanical gate do not establish completion or verification.

## Subsequent native acceptance — 2026-09-27

The earlier paragraph describes the interim PR evidence at that time. The
later evidence in [native-acceptance/README.md](native-acceptance/README.md)
now records actual Codex and Claude startup and manual-compaction delivery,
repository switching between 0.19.0 and the released 0.18.0 installation,
missing/altered/mismatched inputs, and uncertain-write recovery. It preserves
the exact host surfaces, partial attempts and permission limitations.

Codex's completed recovery obtains a fresh evaluator result after compaction
and does not duplicate the persisted risk. Claude inspects the same kind of
persisted effect, does not repeat it, and preserves its denied evaluator call
as a blocker. These are disposable-fixture observations, not source-repository
lifecycle transitions or decisions.

Current-source validation passes: nine focused tests (one skip), the full
1,122-test suite (16 skips), release-distribution validation and CLI help.
Released doctor, graph validation and selected review preflight pass. The six
reading-cost measurements were reproduced exactly. The source entry is 1,191
words; complete selected instruction walks use 2,406–5,049 words versus the
21,888-word review source. Formal artifacts remain separate required inputs.

The report records material review findings and their resolution. No product
files changed in this batch. Subsequent lifecycle completion and verification
preparation, if eligible, are recorded by the released evaluator rather than
inferred from this narrative.
