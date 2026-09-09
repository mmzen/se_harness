---
name: setup
description: Prepare or check Verity Plane's private released-evaluator environment using provided Python and the wheel supplied with the plugin. Use for first setup or environment reuse, before repository initialization or governed work.
---

# Set up the evaluator

Use the host's shell tool to prepare the checking tool. The operator supplies
Python; the plugin supplies the released wheel. The agent runs the commands.
The operator does not create or activate a virtual environment manually.

Read [the environment procedure](references/environment.md) before acting.
It contains the exact commands, input checks and refusal conditions.

1. Select an actual Python installation through host or shell discovery.
   Check Python 3.11+, `venv` and `ensurepip` before creating anything.
   If a prerequisite is missing, explain what the operator must install and
   stop. Do not download Python or invoke an installer alias.
2. Select the previously verified plugin package and its fixed release
   identity. Choose a private environment in persistent plugin data outside
   the repository. An existing authorization for this setup remains valid.
3. For a new environment, create it at its final location and install the
   supplied wheel offline. For an existing environment, skip installation
   and recheck it. Do not repair, replace or reuse an incomplete installation.
4. Run the installed evaluator's identity command. Require its observed
   archive hash as well as a passing identity result. For an installed
   repository, the release must match its governing lock.

Report the absolute environment Python, selected release, observed identity
and any remaining prerequisite. A successful setup prepares a tool; it does
not initialize or upgrade a repository, authorize a work order, or approve a
verification or release record. Use the existing evaluator for those workflows
when separately authorized.

This skill contains instructions, not a hook or a bundled interpreter.
It introduces no launcher or replacement policy engine. Host activation and
repository initialization are separate parts of the plugin implementation.
