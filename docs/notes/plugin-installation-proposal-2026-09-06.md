# Proposal: install Verity Plane as a plugin

<!-- Target expertise: 3.5/10. This score describes the knowledge expected from the reader. -->

> Revised 2026-09-08. Proposal only; this note authorizes no implementation or lifecycle decision.
> Source baseline: [`aad82a9`](https://github.com/mmzen/se_harness/tree/aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055), candidate source 0.16.0; this repository uses released evaluator 0.15.0. The proposed plugin has not been built or integration-tested.
> This replaces the [earlier exploration](agentic-execution-plugin-distribution.md).

## Recommendation

**Install the plugin. Connect your repository. Start working.**

The plugin supplies `harnessctl`, its Python runtime, skills, and hooks. The user does not install Python, create a virtual environment, or learn another command layer.

Ship native Codex and Claude Code packages built from the same engine and skill sources. Keep the existing harness rules, installer, and CI commands. Add a small amount of host integration code.

## What changes

| Today | Proposed experience |
| --- | --- |
| Install Python and `se-harness` separately. | Install one plugin containing a ready-to-run evaluator. |
| Run `harnessctl init` or `adopt` manually. | Ask the new `setup` skill to connect the repository. It uses those same commands. |
| Repository files provide agent instructions. | Session hooks verify the installation and load those instructions automatically. |
| Two existing read-only skills. | Reuse both and add three skills: `setup`, `change`, and `evidence`. |
| No native plugin manifests or hooks. | Add host manifests and two scripts: `session-context` and `check-tool-action`. |

## Architecture: one engine, two adapters

The two host adapters target Codex and Claude Code. Each uses the same two purpose-specific scripts and existing evaluator.

```text
User request -> skill -> agent's tool -> scripts/harnessctl -> repository
SessionStart -> scripts/session-context -> verify installation and load rules
PreToolUse   -> scripts/check-tool-action -> evaluate action -> host response
```

`scripts/harnessctl` is the packaged entry point to the **existing** CLI. On Windows, ship `scripts/harnessctl.exe`. It starts the included Python interpreter and package; its arguments remain the current `harnessctl` arguments.

```text
verity-plane/
  .claude-plugin/plugin.json       New Claude manifest
  OR .codex-plugin/plugin.json     New Codex manifest
  scripts/harnessctl[.exe]         New packaging of the existing CLI
  scripts/session-context[.exe]    New readiness checks and governance loading
  scripts/check-tool-action[.exe]  New checks before supported tool actions
  runtime/                        Bundled Python + released package + templates
  hooks/hooks.json                 New host event registrations
  skills/setup/                    New
  skills/change/                   New
  skills/evidence/                 New
  skills/harness-orient/           Adapt existing skill
  skills/harness-operator-brief/   Adapt existing skill
  agents/                         Optional host-specific helper definitions
```

Use the installed plugin's absolute paths: `${CLAUDE_PLUGIN_ROOT}/scripts/harnessctl` in Claude Code, `${PLUGIN_ROOT}/scripts/harnessctl` in Codex. Do not depend on a globally installed command or a copy inside the target repository. [Claude paths](https://code.claude.com/docs/en/plugins-reference#environment-variables), [Codex packaging](https://developers.openai.com/plugins/build/plugins).

### Bundle the runtime

Start with **one exact released evaluator per plugin release**, including portable Python, package metadata, and templates. Keep it outside the target checkout. Use the existing identity checks and an absolute interpreter with isolated imports (`-I`); reject ambient Python and candidate-source imports. Preserve the published Python package rather than assuming a frozen executable satisfies today's identity contract. [Runtime identity](../../se_harness/runtime_identity.py).

Normal operations require that evaluator to match the repository's governing version and identity. On mismatch, stop: install a compatible plugin release, or explicitly upgrade the repository using the target evaluator. Updating the plugin alone never changes the repository lock. The first version does not need a general runtime download manager.

Packaging still needs proof: select a redistributable Python build, verify release contents, and test each supported OS and architecture on a machine without Python. Validate platform selection and package size against each host's distribution mechanism.

### Keep skills small

| Skill | Responsibility |
| --- | --- |
| `setup` — **New** | Connect a repository, check readiness, and guide an explicit upgrade or repair. |
| `change` — **New** | Draft artifacts, present decisions, and guide the authorized work order. |
| `evidence` — **New** | Retain results, prepare verification and release records, and present required decisions. |
| `harness-orient` — **Adapt** | Inspect current state and explain the evaluator's next step. |
| `harness-operator-brief` — **Adapt** | Explain a supplied result when explicitly requested. |

A skill instructs the agent to use existing commands. The evaluator determines what is allowed. Preserve its blockers, actual writes, and required decisions; a successful command does not approve the next action.

The main agent implements the work. Optional `investigator` and `evidence-reviewer` subagents provide read-only findings. Neither replaces the accountable human's verification or release decision.

## Hooks: useful intervention, incomplete enforcement

Use two scripts with explicit responsibilities. Both call the same `harnessctl` evaluator:

| Event | Script | Action |
| --- | --- | --- |
| `SessionStart` | `scripts/session-context` | Verify runtime identity and installed content with `doctor`, then inject the verified `se-harness:begin` / `end` block from `AGENTS.md` and the full `ENGINEERING_HARNESS.md` router. |
| `SessionStart` after compact or resume | `scripts/session-context` | Repeat those checks and load fresh governance and selected work context. |
| `PreToolUse` | `scripts/check-tool-action` | For explicitly supported actions, run the corresponding existing checkpoint and return the host's supported allow/deny response. |

Keep verification and injection together, in order, inside **`session-context`**: matching hooks can run concurrently. The setup skill can also call `session-context --readiness REPO` for a manual retry. If context is truncated or spills to a file, require a complete read before declaring readiness. Use the documented `SessionStart` recovery path; do not assume `PostCompact` output restores context. [Codex hooks](https://learn.chatgpt.com/docs/hooks), [Claude hooks](https://code.claude.com/docs/en/hooks).

Hooks do not initialize repositories, upgrade locks, or make human decisions. In an unrelated repository, startup writes nothing. A missing or untrusted hook is a readiness failure for the proposed workflow, not proof that the host has blocked every tool.

### The merge boundary must stand on its own

**A plugin cannot be the only authorization control.** Hooks can be disabled, miss tool paths, or fail without blocking an action. An actor name passed to `transition --decision` is an assertion, not authenticated human approval.

Keep human handoffs for verification, integration, and publication. Deterministic controls must bind the actual owner's decision to the reviewed artifacts and candidate, reject changed inputs, and protect every merge or publication route—including alternate credentials and APIs. This remains separate implementation work tracked in [#347](https://github.com/mmzen/se_harness/issues/347).

The initial plugin prepares review material and hands off to the owner through the project's existing process. It does not automatically merge or publish. Automation of those effects waits for demonstrated enforcement.

## Native capabilities and their limits

Claude Code supports bundled executables. However, distribution through **claude.ai Organization settings rejects top-level `bin/`**. Put executables in `scripts/` and reference them through the plugin root. [Executable placement](https://code.claude.com/docs/en/plugin-marketplaces#keep-executables-out-of-the-top-level-bin-directory).

In Claude's manifest, `commands` means Markdown skills and `dependencies` means other plugins. Neither installs Python. Hooks may prepare Python dependencies in `CLAUDE_PLUGIN_DATA`; bundling the runtime is our product choice to avoid that setup on first use. [Manifest schema](https://code.claude.com/docs/en/plugins-reference#plugin-manifest-schema), [persistent data](https://code.claude.com/docs/en/plugins-reference#persistent-data-directory).

| Host | Installation and component loading |
| --- | --- |
| Claude Code | Native manifest, skills, hooks, and `agents/`. Use `/reload-plugins` when required after changes. Plugin-root `CLAUDE.md` is not automatically loaded. [Plugin guide](https://code.claude.com/docs/en/plugins). |
| Codex desktop / CLI | Native manifest, skills, and hooks; confirm hook trust separately and start a new session where required. Native plugin-agent loading is not established: optional agents may need project registration under `.codex/agents/`. [Plugins](https://learn.chatgpt.com/docs/plugins), [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents). |

Test each host independently, including Windows. Identical component names do not imply identical permissions or hook coverage.

## Distribution, updates, and migration

Build both host packages from one release source. Keep artifacts and evidence in the repository, outside disposable plugin caches. Preserve the existing pip/CLI route for CI and non-plugin use.

Adapt the two skill cores for plugin paths and identity checks. Select one active discovery route during migration; remove duplicates only through an ownership-aware, authorized change. Reuse `init`, `adopt`, and `upgrade`, including conflict checks. Repository setup and host registration are separate operations, not one atomic transaction. [Installer](../../se_harness/installer.py).

## Delivery and open choices

1. **Prove packaging:** install on a clean supported machine; run the bundled evaluator; reject a mismatched or modified installation. Confirm marketplace acceptance and offline use after installation.
2. **Prove workflows:** implement the three skills and two hook scripts; test setup, governance restoration, work, evidence, and human handoffs on both hosts.
3. **Prove authority separately:** demonstrate that missing approval, changed candidates, disabled hooks, and alternate access routes cannot authorize protected effects before enabling merge or publication automation.

Challenge two choices: can one bundled version serve the first supported users, and does portable Python fit the host's distribution limits? Change packaging if testing shows it is needed. Avoid adding a runtime manager or another command protocol in advance.

Continue with the [operation map](plugin-operation-workflows-2026-09-06.md) and [16 detailed scenarios](plugin-scenarios/README.md), which name the commands, components, events, and decisions for each operation.
