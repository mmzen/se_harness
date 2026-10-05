```toml
artifact = "WO-RLS-041"
checkpoint = "handoff"
formal_snapshot_sha256 = "4dbdace71258cab952b06bada5d288d7d1f2a689c27ef1dade84f33c7f8e7d66"
rebound_at = "2026-10-05T03:39:08Z"
```

# Preparation handoff

The approved release inputs and corrected implementation are prepared. Actual
checks for source 061307929c94314ccd2beb4a53f174e536fceba8 are retained in
../WO-RLS-043/corrected-qualification-review.md and its immutable archives.
Windows/Linux source, installed packages, both HAG fixes, the original draft
transition defect, deterministic builds, upgrades and native CLI cycles pass.
Original failures and reported skips remain visible.

../WO-RLS-041/preparation-marketplace-commit.json records the checked ordinary
marketplace child and exact 69-file tree. It is local preparation, not a public
marketplace update. Final candidate capture must retain its own exact build,
staging identities and applicable checks; earlier tests are not relabelled.

../WO-RLS-041/desktop-deferral-review.md records mmzen's accepted DEC-RLS-009
and RISK-RLS-007. Codex Windows desktop remains not run / unverified for this
release. CLI/public-route checks and later human verification remain required.
../WO-RLS-040/provider-configuration-applied.json retains the separately
authorized exact GitHub activation and human PyPI binding confirmation.

This handoff supports implementation completion and final verification
preparation. It supplies no human verification, merge, release or adoption.
