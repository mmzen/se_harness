```toml
artifact = "WO-HAG-003"
checkpoint = "handoff"
formal_snapshot_sha256 = "14ad8b13c41b05d9489f53eef0049c83cfcdd684c0a6c24cc86e5541183e1707"
rebound_at = "2026-10-04T17:25:14Z"
```

# WO-HAG-003 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

WO-HAG-003 implements REQ-HAG-010 and SPEC-HAG-005 under the approved
ARCH-HAG-002, ADR-HAG-002 and VER-HAG-003. The correction records the human
separately from an explicitly selected existing owner label. Preview and apply
share validation and the existing atomic writer. Invalid claims refuse.

Tested and packaged source: `99a8c53f6a2e253c20737d5985223ea0c25c79d9`.
Correction implementation base: `fcfb02b3a8ff041023e0d85d7bc2af0524559f8a`.
This is the approved-input baseline for this correction, not a replacement for
PR #535's target or the whole hosted-change comparison with main.

- [Requirement assessment](verification-results.json): all eight contract
  cases pass; source and build tree identities and limitations are recorded.
- [Implementation review](implementation-review.md): bounded design, diff
  findings and their resolution.
- [Actual commands and results](commands.zip): includes original failures,
  final successful reruns and an internal digest manifest.
- [Pinned build replay](build-replay.json): two equal builds of both archives.
- [Installed probe](installed_probe.py): real installed-wheel operations on
  disposable fixtures on Windows and Linux; 14 CLI observations per platform.

The final source suite reports 1,305 tests, 22 skips and exit 0. Distribution
checks pass for 22 records. Released validation reports zero errors and 61
existing warnings. The installed probes pass on both required platforms.

Human verification remains pending. The live DEC-HAG-001, governor 0.22.0,
hosted evaluator pin, VREC-HAG-001 and its historical evidence remain unchanged.
No hosted service scenario has been run. Release and adoption remain separate.
