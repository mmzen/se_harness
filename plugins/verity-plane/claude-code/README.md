# Verity Plane

Verity Plane 0.2.6 exposes shared skills through the host's native skill discovery.
Use setup to prepare the repository-selected evaluator, harness-orient to inspect
the project, and change/evidence for its explicit workflow commands.

The adapter delivers the selected release's compact entry at startup,
compaction and resume. It restores a checkout selected for that host session,
including one cloned below the host working directory. With no selection it
provides a short bootstrap and the setup skill's activation inputs.

External-resource layouts use the exact installed evaluator's resource command.
Legacy installations retain their validated repository-root delivery. Missing,
changed, incompatible or oversized input reports a delivery gap without fallback.
Setup retains separate immutable evaluator environments outside repositories.
Activation immediately returns the complete entry; it grants no lifecycle authority.

Plugin 0.2.6 targets evaluator 0.22.1. mmzen verified candidate
`4f640284ec496b88cd7aa4ba88ca537d9374a2f8` in VREC-SEH-033.
Windows/Linux package checks and native Codex/Claude CLI checks passed.
Codex Windows desktop remains unverified under accepted DEC-RLS-009 / RISK-RLS-007.
Qualification does not establish public installation or update results.

Read the [release review](https://github.com/mmzen/se_harness/blob/main/docs/engineering/release-0-22-1/README.md)
and its delivery evidence for publication status. Compare installed bytes with
the [public identity](https://github.com/mmzen/se_harness/blob/plugin-marketplace/PACKAGE-IDENTITY.json).
Qualified archives keep their original preparation README snapshots; source
documentation corrections do not rewrite those bytes or inventories.

Development archives cannot establish release or marketplace eligibility.
Python 3.11+ must be available to the hook launcher. Codex also requires the
user to trust the plugin's reviewed hooks. Real host settings are not changed by
building or testing this source. Repository-only skills do not install hooks.

The complete context, including paths and metadata, is capped at 20,000 UTF-16
units for Codex and 10,000 for Claude Code. A larger entry is refused with its
measured size; policy is never truncated. Codex's handler keeps its separate
5,000 approximate-token threshold. Native tests must confirm full delivery with
the actual host paths.

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
