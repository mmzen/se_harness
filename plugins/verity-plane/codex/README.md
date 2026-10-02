# Verity Plane

Verity Plane 0.2.4 exposes shared skills through the host's native skill discovery.
Use setup to prepare the repository-selected evaluator, harness-orient to inspect
the project, and change/evidence for its explicit workflow commands.

The candidate adapter delivers the selected release's compact entry at startup,
compaction and resume. It restores a checkout selected for that host session,
including one cloned below the host working directory. With no selection it
provides a short bootstrap and the setup skill's activation inputs.

External-resource layouts use the exact installed evaluator's resource command.
Legacy installations retain their validated repository-root delivery. Missing,
changed, incompatible or oversized input reports a delivery gap without fallback.
Setup retains separate immutable evaluator environments outside repositories.
Activation immediately returns the complete entry; it grants no lifecycle authority.

This source is selected for the 0.21.0 release under REL-SEH-033. Plugin 0.2.4
is not published yet; the current public maintenance package is 0.2.3 with
evaluator 0.20.1. WO-RLS-031 checks the final candidate. WO-RLS-032 qualifies
the package after the public 0.21.0 wheel exists. Native delivery, automatic
compaction, resume and parallel sessions require matching VER-IAR-021 evidence.
Codex Windows desktop remains unverified and is a pending release criterion.
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
