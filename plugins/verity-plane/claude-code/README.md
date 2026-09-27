# Verity Plane

Verity Plane 0.2.0 exposes shared skills through the host's native skill discovery.
Use setup to prepare the repository-selected evaluator, harness-orient to inspect
the project, and change/evidence for its explicit workflow commands.

This version includes a SessionStart adapter for startup and post-compaction
instruction delivery. It reads the selected repository's ENGINEERING_HARNESS.md,
compares its bytes with the installation record and checks the selected version.
It neither computes lifecycle authority nor upgrades the repository. Missing,
changed, incompatible or oversized input is reported as a delivery gap.

Native Windows evidence accepted in VREC-IAR-011 demonstrates startup and
post-manual-compaction delivery with Codex CLI 0.155.0-alpha.16.4 and its
native app server, and Claude Code 2.1.273. These results apply to the
tested delivery assets. They do not establish desktop UI, automatic
threshold compaction, macOS or later host versions. Final published plugin
archives require their own package inspection after checker publication.
Python 3.11+ must be available to the hook launcher. Codex also requires the
user to trust the plugin's reviewed hooks. Real host settings are not changed by
building or testing this source. Repository-only skills do not install hooks.

The complete context is bounded to 10,000 characters. A larger entry is refused,
not silently truncated. Codex's handler has a 5,000 approximate-token threshold;
Claude Code's documented character limit remains the shared bound.

API references: [Codex hooks](https://learn.chatgpt.com/docs/hooks) and
[Claude Code hooks](https://code.claude.com/docs/en/hooks).

The setup environment is outside the checkout. Development archives are labeled
DEVELOPMENT.md and cannot establish release eligibility. Installation into the
owner's real host settings is a separate action.

## Setup after native installation

Use Python 3.11+ with venv and ensurepip. Invoke verity-plane:setup with your
project and a persistent data directory outside it. Setup installs the supplied
wheel offline in its private environment. Plugin installation alone does not
download SE Harness from PyPI, initialize a project or approve an upgrade.
An existing project's selected evaluator remains authoritative.

See [setup](skills/setup/SKILL.md) and its shared references for initialization,
connection and repair. Read `assembly-inventory.json` for this package's exact
source and released-wheel identity when using a release assembly.
