```toml
artifact = "WO-DOC-015"
checkpoint = "handoff"
formal_snapshot_sha256 = "93d19c90123bf0488b0bfb8de2d636043d69fda9edde9e582ab3e7227735c6a4"
rebound_at = "2026-09-04T21:09:49Z"
```

# WO-DOC-015 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

# Supplied logo publication

The owner supplied lockup-white-on-red.png and requested adding it as the last-minute update to the README publication. The original PNG is copied unchanged to docs/images/verity-plane-logo.png (2,000 x 800 pixels; 89,842 bytes).

- Logo SHA-256: `38356603c1fe30a53f02d615b988d6c3d150e7894c5988e431287023cda9e870`.
- README SHA-256 (UTF-8 LF): `c31e8325bae8982af8fe09ef3a7e0b0990a169b0a00b595afe6455094f69cdb8`.
- Removing only the new four-line image block exactly reproduces the README from main at 0a38b0d. The prose, heading, tagline and Explorer screenshots are unchanged.
- The browser preview was visually inspected: the left-aligned logo displays at 360 x 144 above the left-aligned title, with its aspect ratio intact.
- Existing onboarding, progressive-documentation and integration-guide tests: 47 passed.
- Isolated released evaluator 0.14.0 doctor and graph validation passed (1,305 artifacts; zero errors; 69 existing maintenance warnings).
- Release-distribution validation passed for 11 records; candidate CLI help and diff whitespace checks passed.
- Review preflight and complete Git-derived scope/handoff checks are required before the completion transition.
- Full-source regression and the hosted package/platform checks are publication gates on this PR. Their authoritative results and the final merge commit are retained by GitHub. Publication must match the hashes above.

This work transports the owner's logo and publication decision only. It claims no new assurance, package release, or deployment decision.
