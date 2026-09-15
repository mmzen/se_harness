# Release notes: checker 0.18.0 and verity-plane 0.1.0

Prepared for review. Neither version is published by this packet.

## Checker 0.18.0

- Simpler specifications and reviews: start from a current need, prefer the
  smallest useful design, and justify added complexity. The shared guidance is
  carried by the authoring policy and the change/review instructions.
- One routine execution route: approved work proceeds through implementation,
  checks, completion and record preparation. Accountable verification, release
  and external actions retain their own decisions.
- Less repeated checking: local progress, evidence preparation and release
  coverage use the accepted KISS rules. CI runs the useful checks with less
  repeated setup and a much smaller package-job checkout.
- Simpler plugin connection: select the plugin as skill provider, replace the
  old disposable skill copies, and use ordinary retry and repair. Explicit
  checker calls replace automatic blocking hooks.

The release includes other completed authoring, CI and maintenance fixes listed
in [coverage](evidence/WO-RLS-024/coverage.md). Existing installations continue
to use their selected released checker until an explicit upgrade.

## First plugin release: verity-plane 0.1.0

Codex and Claude Code receive the same skills and supplied checker wheel. Setup
uses provided Python in a private environment. The skills cover project setup
and maintenance, change work, evidence, orientation and requested briefings.

Both manifests and the production assembly plan are prepared here. The actual
release archives follow checker 0.18.0 publication and consume that published
wheel. The existing [installation guide](../../notes/plugin-installation-guide.md)
currently demonstrates the development route. It is not evidence that a public
plugin installation has already succeeded.

Current host evidence is Windows native skill discovery and direct setup/checker
commands in disposable projects. Model-driven sessions, Codex desktop
installation and macOS are outside this demonstrated support claim.

## Release sequence

1. Review checker qualification and verify the final aggregate record.
2. Prepare and replay the bound checker release record; obtain the release and
   publication decisions, then publish checker 0.18.0 through the existing path.
3. Select the released checker record and public wheel digest. Use
   scripts/build_plugin_archives.py with release/plugin-assembly.json to build
   and check both native archives. Test the actual extracted outputs before
   selecting their publication.
4. Install in the owner's hosts or upgrade live projects only on that selected
   request. This preparation changes neither.
