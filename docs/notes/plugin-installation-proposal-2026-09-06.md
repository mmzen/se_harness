# Proposal: install Verity Plane as a plugin

<!-- Target expertise: 3.5/10. This score describes the knowledge expected from the reader. -->

> Revised 2026-09-08. Proposal only; this note authorizes no implementation or lifecycle decision.
> Shared baseline: main `560973cf`, candidate source 0.17.0, governing released evaluator 0.16.0. The proposed plugin has not been built or integration-tested.
> This replaces the [earlier exploration](agentic-execution-plugin-distribution.md).

The [16 implementation packets](../engineering/plugin-integration/README.md) turn this proposal into draft contracts and bounded work orders. They use the same baseline and are reviewed with these notes in [PR #416](https://github.com/mmzen/se_harness/pull/416).

Commands target released evaluator **0.16.0**, including its transitional `adopt` alias. Candidate source 0.17.0 uses unified `init`; relative source links are navigation aids, not the executable command contract. The notes originated in PR #360 at `9e894e99` and are now aligned with the packets.

## Recommendation

**Install the plugin. Connect your repository. Start working.**

The plugin supplies the released SE Harness package, skills, and hooks. **Python 3.11 or later must already be available.** Setup checks that prerequisite first; if it is missing, the operator must install or provide Python before continuing installation and using the plugin.

The plugin does not bundle or install Python. Once Python is available, setup automatically prepares an isolated environment for SE Harness. The operator does not create or activate that environment manually.

Ship native Codex and Claude Code packages built from the same engine and skill sources. Keep the existing harness rules, installer, and CI commands. Add a small amount of host integration code.

**Keep the required decisions; reduce the manual steps.** The agent continues through permitted steps under the existing request and authority. The plugin requires no skill invocation at every stage or new approval for each allowed edit. Host trust and tool-permission settings still apply. Ask only when a required decision, input, or correction is missing. Reuse an existing decision while it still covers the exact action and reviewed inputs; preserve the current delegation rules.

## What changes

| Today | Proposed experience |
| --- | --- |
| Install Python, create an environment, and install `se-harness`. | Provide Python; plugin setup checks it and prepares the evaluator environment automatically. |
| Run `harnessctl init` or `adopt` manually. | Ask the new `setup` skill to connect the repository. It uses those same commands. |
| Repository files provide agent instructions. | Session hooks verify the installation and load those instructions automatically. |
| Two existing read-only skills. | Reuse both and add three skills: `setup`, `change`, and `evidence`. |
| No native plugin manifests or hooks. | Add host manifests and two Python scripts: `session-context.py` and `check-tool-action.py`. |

## Architecture: one engine, two adapters

The two host adapters target Codex and Claude Code. Each uses the same two purpose-specific scripts and existing evaluator.

```text
Setup       -> host shell checks Python -> prepare evaluator environment
User request -> skill -> host tool -> environment Python -> evaluator
SessionStart -> host shell guard -> environment Python -> session-context.py
                  missing runtime: report setup required; never declare ready
PreToolUse   -> guarded host binding -> check-tool-action.py -> host response
```

The plugin uses the **existing** CLI through `ENV_PYTHON -I -m se_harness`. `ENV_PYTHON` means the verified environment's absolute Python path. Examples shorten that invocation to `harnessctl`. There is no launcher binary, evaluator lookup on `PATH`, or second command protocol. A thin shell guard in the host hook command is allowed.

```text
verity-plane/
  .claude-plugin/plugin.json       New Claude manifest
  OR .codex-plugin/plugin.json     New Codex manifest
  packages/                       One exact released evaluator wheel
  scripts/session-context.py      New readiness checks and governance loading
  scripts/check-tool-action.py    New checks before supported tool actions
  hooks/hooks.json                 New host event registrations
  skills/setup/                    New
  skills/change/                   New
  skills/evidence/                 New
  skills/harness-orient/           Adapt existing skill
  skills/harness-operator-brief/   Adapt existing skill
  agents/                         Optional host-specific helper definitions
```

Resolve scripts and the wheel from the installed plugin root: `${CLAUDE_PLUGIN_ROOT}` in Claude Code and `${PLUGIN_ROOT}` in Codex. Keep the created environment in persistent plugin data, outside the target repository. Normal commands use its verified interpreter, without a global command lookup. [Claude paths](https://code.claude.com/docs/en/plugins-reference#environment-variables), [Codex packaging](https://developers.openai.com/plugins/build/plugins).

### Use an existing Python installation

The setup skill starts with the host's existing shell. It finds Python, resolves its absolute path, and checks **Python 3.11+, `venv`, and `ensurepip`**. Neither coding host is assumed to include Python. This first check cannot depend on a Python hook script already running.

If the check fails, stop setup, activation, and repository initialization with a clear message:

> Python 3.11 or newer is required to install and use this plugin. Install or provide Python with working venv and ensurepip, then run setup again.

If it passes, setup verifies the plugin's released wheel and runs:

```text
PROVIDED_PYTHON -I -m venv ENV_DIR
ENV_PYTHON -I -m pip install --no-index --no-deps EVALUATOR_WHEEL
```

These uppercase names are absolute path placeholders. The wheel contains **one exact released evaluator**, package metadata, and templates. Its Python dependency list is empty in the inspected source. Installation uses that local wheel, without a package-index download. The environment is created locally from the supplied Python installation; it is not a shipped interpreter. Calling its Python directly requires no activation. [Package definition](../../pyproject.toml), [Python environments](https://docs.python.org/3/library/venv.html), [pip bootstrap](https://docs.python.org/3/library/ensurepip.html).

Before installation, compare the wheel archive digest with independently trusted release metadata. Derive the expected version and payload from that verified wheel. Pass all three expected values to the existing isolated identity check. Plugin readiness additionally requires the observed `evaluator_archive_sha256` to be present and equal to the verified archive digest. A supplied expected value is not proof of what was installed. [Exact readiness contract](../engineering/plugin-integration/specifications/SPEC-PLG-002.md).

Normal operations require that evaluator to match the repository's governing version and identity. On mismatch, stop: install a compatible plugin release, or explicitly upgrade the repository using the target evaluator. Updating the plugin alone never changes the repository lock. The first version does not need a general runtime download manager.

Hooks may be registered before the environment exists. Their host shell guard checks whether the absolute environment interpreter can run. If absent or broken, it reports **setup required** without installing anything; the setup skill remains available. Otherwise it invokes the Python handler, which checks identity and repository integrity before readiness. Test this documented route separately on both hosts, including Windows, trust, reload, and recovery. Interpreter existence alone never establishes readiness.

**Avoid a bootstrap loop.** Registered tool hooks must leave already-authorized setup and repair usable through ordinary host permissions. While the runtime is unavailable, report setup required and absent governance coverage; never return checked success or override permissions. The guard cannot enforce the distinction between setup and governed work. Governed automation remains unavailable until readiness succeeds. If a declared governed effect can run without its required check, that route fails qualification unless independent host controls refuse it. The live probes test both real setup and a disposable governed-write attempt.

### Keep skills small

| Skill | Responsibility |
| --- | --- |
| `setup` — **New** | Check supplied Python, prepare the environment, connect a repository, and guide readiness, upgrade, or repair. |
| `change` — **New** | Draft artifacts, present decisions, and guide the authorized work order. |
| `evidence` — **New** | Retain results, prepare verification and release records, and present required decisions. |
| `harness-orient` — **Adapt** | Inspect current state and explain the evaluator's next step. |
| `harness-operator-brief` — **Adapt** | Explain a supplied result when explicitly requested. |

A skill instructs the agent to use existing commands. The evaluator determines what is allowed. Preserve its blockers, actual writes, and required decisions; a successful command does not approve the next action.

The `change` and `evidence` skills refuse governed writes until current verified context is established, and direct recovery to `setup`. This instruction is tested separately from deterministic host enforcement.

Skill commands in the scenarios are optional ways to enter a workflow. They are not additional approval stops. The agent can move from `change` to `evidence` when the existing workflow and authority permit it. Keep the contracts of the existing read-only skills; `harness-operator-brief` still requires an explicit request.

The main agent implements the work. Optional `investigator` and `evidence-reviewer` subagents provide read-only findings. Neither replaces the accountable human's verification or release decision.

## Hooks: useful intervention, incomplete enforcement

Use two scripts with explicit responsibilities. Both call the same `harnessctl` evaluator:

| Event | Script | Action |
| --- | --- | --- |
| `SessionStart` | Shell guard → `scripts/session-context.py` | Report setup required if the runtime is absent; otherwise verify runtime identity and installed content with `doctor`, then inject the verified `se-harness:begin` / `end` block from `AGENTS.md` and the full `ENGINEERING_HARNESS.md` router. |
| `SessionStart` after compact or resume | `scripts/session-context.py` | Repeat those checks and load fresh governance and selected work context. |
| `PreToolUse` | `scripts/check-tool-action.py` | For explicitly supported actions, run the corresponding existing checkpoint and return the host's supported allow/deny response. |

After its shell guard, invoke each script as `ENV_PYTHON -I ABS_SCRIPT`, with absolute paths and separate arguments. A missing runtime reports unready; a covered tool event uses that host's demonstrated refusal format. Host failure behavior must be observed rather than assumed. Keep verification and injection together, in order, inside **`session-context.py`**: matching hooks can run concurrently. The setup skill can also call `ENV_PYTHON -I ABS_PLUGIN/scripts/session-context.py --readiness REPO` for a manual retry. If context is truncated or spills to a file, require a complete read before declaring readiness. Use the documented `SessionStart` recovery path; do not assume `PostCompact` output restores context. [Codex hooks](https://learn.chatgpt.com/docs/hooks), [Claude hooks](https://code.claude.com/docs/en/hooks).

Hooks do not initialize repositories, upgrade locks, or make human decisions. In an unrelated repository, startup writes nothing. A missing or untrusted hook is a readiness failure for the proposed workflow, not proof that the host has blocked every tool.

**A timeout is not a refusal.** Give the tool-check handler an internal deadline shorter than the host's configured timeout, allowing time to stop evaluator subprocesses and return a supported denial. Test the deadline and actual denied effect on each supported host. If the host stops waiting or the guard never starts, inspect what happened before retrying; no handler response means no demonstrated protection. Claude explicitly documents non-blocking command-hook timeouts and launch failures. Codex failure behavior still needs observation on each claimed profile. [Claude timeout behavior](https://code.claude.com/docs/en/hooks#timeouts), [contract and live checks](../engineering/plugin-integration/specifications/SPEC-PLG-008.md).

### The merge boundary must stand on its own

**A plugin cannot be the only authorization control.** Hooks can be disabled, miss tool paths, or fail without blocking an action. An actor name passed to `transition --decision` is an assertion, not authenticated human approval.

Keep the existing human decisions for verification, integration, and publication. Deterministic controls must bind the actual owner's decision to the reviewed artifacts and candidate, reject changed inputs, and protect every merge or publication route—including alternate credentials and APIs. This remains separate implementation work tracked in [#347](https://github.com/mmzen/se_harness/issues/347).

The owner decides; an authorized agent or human may execute through the project's existing tools when the exact action is authorized, required checks pass, and independent enforcement is demonstrated. The plugin adds no rule requiring the owner personally to click Merge or dispatch publication. If enforcement is missing or unproven, agent execution of that effect stays blocked and the gap is reported. A human may use the project's existing permitted route; this fallback is a control limitation, not a new workflow stage. Verification and release decisions alone never authorize external actions.

## Native capabilities and their limits

Keep the two Python scripts in `scripts/` and reference them through the plugin root. Distribution through **claude.ai Organization settings rejects top-level `bin/`**; this proposal needs no such directory. [Script placement](https://code.claude.com/docs/en/plugin-marketplaces#keep-executables-out-of-the-top-level-bin-directory).

In Claude's manifest, `commands` means Markdown skills and `dependencies` means other plugins. Neither installs Python. Setup uses `CLAUDE_PLUGIN_DATA` for its locally created environment; the operator or host supplies the base interpreter. Use Codex's `PLUGIN_DATA` equivalent. [Manifest schema](https://code.claude.com/docs/en/plugins-reference#plugin-manifest-schema), [Claude persistent data](https://code.claude.com/docs/en/plugins-reference#persistent-data-directory), [Codex packaging](https://developers.openai.com/plugins/build/plugins).

| Host | Installation and component loading |
| --- | --- |
| Claude Code | Native manifest, skills, hooks, and `agents/`. Use `/reload-plugins` when required after changes. Plugin-root `CLAUDE.md` is not automatically loaded. [Plugin guide](https://code.claude.com/docs/en/plugins). |
| Codex desktop / CLI | Native manifest, skills, and hooks; confirm hook trust separately and start a new session where required. Native plugin-agent loading is not established. Qualify packaged helper loading, or use the main agent; these packets do not authorize writing project `.codex/agents/` files. [Plugins](https://learn.chatgpt.com/docs/plugins), [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents). |

Test each host independently, including Windows. Identical component names do not imply identical permissions or hook coverage.

## Distribution, updates, and migration

Build both host packages from one release source. Keep artifacts and evidence in the repository, outside disposable plugin caches. Preserve the existing pip/CLI route for CI and non-plugin use.

Adapt the two skill cores for plugin paths and identity checks. Select one active discovery route during migration; remove duplicates only through an ownership-aware, authorized change. **DEC-PLG-004 is a critical prerequisite:** released 0.16.0 has no demonstrated ownership-aware migration for this route. If the technical owner selects migration, separate evaluator work, its release, and repository adoption must precede package 09. Retaining repository skills instead requires revising the conflicting plugin scope. Reuse `init`, `adopt`, and `upgrade`, including conflict checks. Repository setup and host registration are separate operations, not one atomic transaction. [Installer](../../se_harness/installer.py).

## Delivery and open choices

1. **Prove setup:** on each supported platform, missing or outdated Python must stop setup with operator guidance. With suitable Python, create the environment, install the wheel offline, and verify evaluator identity and hook activation. Reject modified packages and mismatched versions; never install Python automatically.
2. **Prove fewer manual steps:** run the same authorized change with and without the plugin. Preserve the required decisions and delegation, require no repeated skill invocation, and ask no duplicate approval for unchanged authorized inputs. Include setup, compaction, and recovery on both hosts.
3. **Measure execution cost:** compare startup, supported tool checks, and total task time on small and large repositories. Record operator interactions as well as processing time, and agree performance limits before release. No performance result is claimed yet.
4. **Prove authority separately:** demonstrate that missing approval, changed candidates, disabled hooks, and alternate access routes cannot authorize protected effects before enabling merge or publication automation. A valid existing decision must not trigger a second approval prompt.

The current [`check` path](../../se_harness/workflow_compliance.py) runs repository validation. Repeating that work before every edit may be expensive. Map each supported action to its required check and measure the cost before finalizing the adapter. Any reuse of prior results must remain in the evaluator, detect changed relevant inputs, and preserve refusals. Performance work must not skip required pre-effect checks, use stale approval, or add approval prompts for routine permitted actions.

Challenge two choices: can one released evaluator version serve the first supported users, and does the documented shell-guard route work on each claimed host/platform? Test Python discovery, paths containing spaces, and environment recovery on supported platforms. Keep the prerequisite explicit; avoid adding a Python installer, runtime download manager, or another command protocol.

Use the [packet delivery plan](../engineering/plugin-integration/README.md#review-and-delivery) for staged definition delivery, then the [operation map](plugin-operation-workflows-2026-09-06.md) and [16 detailed scenarios](plugin-scenarios/README.md), which name the commands, components, events, and decisions for each operation.
