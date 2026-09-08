# Plugin scenarios: installation and session readiness

<!-- Target expertise: 3.5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

[All scenarios](README.md) · [Operation workflows](../plugin-operation-workflows-2026-09-06.md) · [Scenario template](../plugin-scenario-template.md)

**New** marks components to build. Use the [shared baseline and calling convention](README.md#shared-component-names-and-calling-convention): main `fae52e1b`, governing released evaluator 0.16.0. `harnessctl` means the verified absolute `ENV_PYTHON -I -m se_harness` invocation. `REPO` is the selected absolute project path. The plugin remains proposed.

Setup examples show ways to enter the operation. After a concrete setup request is authorized, the agent follows the permitted steps without asking the user to invoke each one. Host installation/trust, missing decisions, changed scope, and unresolved conflicts remain explicit interactions.

## Scenario 1: Install and activate the plugin

### 1. Purpose and starting point

**Purpose:** Use supplied Python to prepare the evaluator, then confirm the installed hooks actually run.

- **Starts when:** The user installs `verity-plane` and requests setup.
- **Requires:** A supported host and **Python 3.11+ with working `venv` and `ensurepip`**, supplied by the user or host.
- **Successful result:** The released evaluator is installed in an isolated environment, its identity passes, and hook activation is confirmed separately.

### 2. Workflow

```text
Host loads skills and guarded hooks → missing environment: setup required
        ↓
User requests setup [New] → host shell finds and checks supplied Python
        ↓
Missing or unusable? STOP → operator installs/provides Python → retry
        ↓
Create isolated environment → install bundled evaluator wheel → identity
        ↓
Complete host trust/reload → new SessionStart → full readiness checks
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → plugin manager | **Codex:** install from **Plugins** or `/plugins`. **Claude Code:** register the catalog with `/plugin marketplace add MARKETPLACE_SOURCE`, then `/plugin install verity-plane@verity-plane`. These proposed names are not published yet. Downloading files does not establish readiness. |
| 2 | User → `setup` **[New]** | Ask Codex to use the setup skill, or invoke `/verity-plane:setup` in Claude Code. The agent reads `skills/setup/SKILL.md`. Hooks may already be registered: their shell guard reports setup required until the environment can run. Setup remains accessible. |
| 3 | Agent → existing host shell | Find supplied Python using shell discovery first, such as PowerShell `Get-Command` or POSIX `command -v`. Resolve its absolute executable, then check Python 3.11+, `venv`, and `ensurepip`. The host is not assumed to supply Python. If missing, too old, or unusable, give the operator the message below and stop. |
| 4 | Agent → supplied Python | Compare the bundled wheel archive SHA-256 with independently trusted release metadata. Reject a mismatch before installation. Under the authorized setup request, create the environment in persistent plugin data using `venv`; install that exact wheel with `pip --no-index --no-deps`. No manual activation is needed. |
| 5 | Agent → environment Python | Run isolated `identity` with expected version, payload digest, and archive digest from the verified wheel, plus expected root and entry point. Require observed `evaluator_archive_sha256` to be present and equal. Reject missing provenance, wrong identity, or repository-local imports. A different repository lock requires a compatible plugin or explicit upgrade. |
| 6 | User/agent → host activation controls | Complete required host trust/reload for the packaged shell-guard bindings. Start a fresh session and observe `SessionStart`: guard → absolute environment Python → `session-context.py` → identity and integrity checks. Follow [scenario 3](#scenario-3-start-a-session) for a connected repository. If no hook run is observed, report activation as **unconfirmed**. |

The live probe must execute setup and repair through actual host tools while hooks are registered. A menu entry is insufficient. Before readiness, the guard reports missing governance coverage without checked success or a permission override; only already-authorized setup may continue under ordinary host permissions. This instruction is not an enforced action classifier. A governed effect that escapes its required refusal makes that route unqualified.

Setup never installs or downloads Python. It does not initialize a repository unless that additional action is requested and authorized. Installation may download plugin files before prerequisites are checked; there is no assumed native pre-install callback.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/setup/SKILL.md` directs prerequisite checks, environment setup, and activation. | **New:** instructions using existing shell/Python commands. |
| **Hook** | `SessionStart` runs a shell guard, then `session-context` when the runtime can run. | **Reuse:** host event and shell. **New:** guarded registration. |
| **Script** | `scripts/session-context.py` delivers verified rules; `scripts/check-tool-action.py` checks supported actions. | **New:** two Python scripts; a thin shell guard lives in the hook command. |
| **Tool/interface** | Host shell discovers Python before any Python script is called. | **Reuse:** `exec_command`, `Bash` / `PowerShell`, plugin manager, `venv`, and `pip`. |
| **Evaluator** | Exact released wheel under `packages/`, including templates and metadata. | **Reuse:** published evaluator and identity checks. **New:** plugin packaging. |
| **Subagent** | Not used. | **Not used:** setup requires no delegated agent. |
| **Human** | Provide Python if absent; choose the plugin and complete host trust. | **Reuse:** operator installation and host controls. |
| **External control** | Verify the plugin and bundled wheel before executing them. | **Adapt:** trusted release distribution; Python remains an operator prerequisite. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Python is missing, older than 3.11, or cannot create a usable environment. | Stop setup/activation and repository initialization; never install Python automatically. | Operator installs or repairs Python with `venv`/`ensurepip`, then reruns setup. |
| Wheel installation or evaluator identity fails. | Report unready; retain the prior verified environment during repair. | Correct the package/environment problem, then rerun setup. |
| Hook is disabled, untrusted, or not observed. | Report actual status separately from evaluator readiness. | Complete host enablement/trust and observe a new session. |
| Evaluator version differs from the repository requirement. | Normal governed operations stop. | Select a compatible plugin or explicitly authorize a [repository upgrade](release-and-maintenance.md#scenario-16-upgrade-or-repair-the-installation). |

### 5. Example result

> Setup stopped: Python 3.11 or newer with working venv and ensurepip is required.
> Install or provide Python, then run setup again. The plugin files are present, but the plugin is not ready to use. No repository was initialized.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

The [CLI](../../../se_harness/cli.py), [runtime identity checks](../../../se_harness/runtime_identity.py), package metadata, and templates already exist. The plugin distribution does not. Setup uses existing Python modules, with absolute, correctly quoted paths:

```text
PROVIDED_PYTHON -I -m venv ENV_DIR
ENV_PYTHON -I -m pip install --no-index --no-deps ABS_WHEEL
ENV_PYTHON -I -m se_harness --version
```

`PROVIDED_PYTHON` is the checked executable; `ENV_DIR` is outside the target repository under persistent plugin data; `ENV_PYTHON` is that environment's Python; `ABS_WHEEL` is the verified released wheel under plugin `packages/`. Failure to create the environment or bootstrap its pip stops setup. Subsequent examples use the existing CLI shorthand:

```text
harnessctl identity --role released-evaluator --expected-version VERSION --expected-root ENV_DIR --checkout-root REPO --entry-point ENV_ENTRY_POINT --evaluator-payload-sha256 PAYLOAD_SHA256 --evaluator-wheel-sha256 WHEEL_SHA256 --require-isolated-python --json
```

`ENV_DIR` is the created environment root. `ENV_ENTRY_POINT` is its existing console command installed by pip: `bin/harnessctl` on POSIX or `Scripts/harnessctl.exe` on Windows. This is not a new plugin wrapper. Passing its absolute path prevents the identity check from selecting an unrelated global command. Trusted release metadata supplies the archive digest; the verified wheel supplies expected version and payload digest. Inspect returned `evaluator_archive_sha256`, the observed digest. Returned `evaluator_wheel_sha256` echoes the expected value and cannot prove installation provenance. Generic identity permits absent provenance; [SPEC-PLG-002](../../engineering/plugin-integration/specifications/SPEC-PLG-002.md) adds the narrower plugin readiness requirement. Clear inherited `PYTHONPATH` and apply the [shared process environment](README.md#commands-in-the-examples). There is no global pip install or shell activation step.

**Proposed additions**

Ship one exact released pure-Python evaluator wheel under `packages/`, skills, and the two `.py` hook scripts. The setup skill prepares the environment from supplied Python. Packaged hook commands include a thin shell guard; it reports setup required when the environment cannot run and never installs dependencies. No Python binary, launcher binary, evaluator lookup on `PATH`, second protocol, or runtime download manager is shipped.

**Inputs, outputs, and writes**

- **Inputs:** Supplied Python, host/platform, trusted plugin/wheel, selected repository boundary.
- **Outputs:** Prerequisite, environment, evaluator, and hook status.
- **Writes:** Plugin files, isolated environment under persistent plugin data, and authorized host hook configuration. No repository or lifecycle changes.

**Host differences**

- **Codex:** Use `PLUGIN_ROOT` / `PLUGIN_DATA` for installed files and persistent environment storage. Complete separate [hook trust](https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks).
- **Claude Code:** Use `CLAUDE_PLUGIN_ROOT` / `CLAUDE_PLUGIN_DATA`. Keep Python scripts under `scripts/`; organization distribution rejects top-level `bin/`. Manifest `dependencies` names plugins, not Python packages. [Plugin reference](https://code.claude.com/docs/en/plugins-reference#plugin-manifest-schema), [organization distribution](https://code.claude.com/docs/en/plugin-marketplaces#keep-executables-out-of-the-top-level-bin-directory).

On Windows, the environment's Python is normally under `Scripts/`; on POSIX, under `bin/`. Those are directories in plugin data, not a top-level plugin `bin/`. Neither host is assumed to install Python for the user. The shell guard can run before Python setup; full readiness cannot. The two host probes must demonstrate trust, quoting, reload, and actual event behavior on claimed versions.

**Checks that demonstrate the behavior**

Missing/old Python or unavailable `venv`/`ensurepip` produces setup guidance without repository writes. Retain guard output before setup, full identity/context after setup, and recovery after interpreter removal. Test wrong payload, different archive, absent archive metadata, tampered wheel, and failed repair preserving the prior environment.

**Open questions**

Does this documented route hold on each claimed host/platform? DEC-PLG-001 and DEC-PLG-002 record the technical owner's decision from the two probes; neither assumes that loading a manifest establishes readiness.

</details>

## Scenario 2: Initialize or adopt a repository

### 1. Purpose and starting point

**Purpose:** Connect a project while preserving owner content.

- **Starts when:** The user asks the `setup` skill to connect `REPO`.
- **Requires:** Python prerequisites and plugin setup from scenario 1 have passed, plus authority for the listed installation effects.
- **Successful result:** Managed files are installed and `doctor` passes.

### 2. Workflow

```text
User → setup [New] → inspect target
        ↓
Existing init/adopt --dry-run → review changes
        ↓
Existing init/adopt → doctor → session readiness
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → `setup` **[New]** | Ask Codex to use the setup skill for `REPO`, or invoke `/verity-plane:setup repository REPO` in Claude Code. The agent reads `skills/setup/SKILL.md`. |
| 2 | Agent → shell/read tools | Resolve the target and check existing installation. Use `init` for an absent or empty directory; use `adopt` for a nonempty directory, including one containing only `.git`. An installed project goes to readiness or maintenance. |
| 3 | Agent → environment Python | Run the selected command with `--dry-run --json`. Show planned paths, preserved owner content, and conflicts. |
| 4 | Agent and owner | Resolve conflicts and any missing authorization. If target content changed since the preview, repeat it. |
| 5 | Agent → environment Python | Run the same `init` or `adopt` command without `--dry-run`. Then run `doctor`. Report the actual result and continue with [session readiness](#scenario-3-start-a-session). |

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/setup/SKILL.md` selects and explains the installation steps. | **New:** instructions around current commands. |
| **Hook** | No hook initializes a repository. | **Not used:** setup requires an explicit request. |
| **Script** | No extra installer script: environment Python runs `-I -m se_harness`. | **Reuse:** installer implementation. |
| **Tool/interface** | Codex `exec_command` or Claude Code `Bash` / `PowerShell` runs the command. | **Reuse:** shell tools. |
| **Evaluator** | `init`, `adopt`, and `doctor` plan, install, and check. | **Reuse:** existing CLI. |
| **Subagent** | Not used. | **Not used:** the main agent follows setup. |
| **Human** | Authorize installation and resolve owner-content conflicts. | **Reuse:** repository ownership. |
| **External control** | No remote action occurs. | **Not used:** setup grants no integration authority. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| A destination conflicts with existing content. | Installer refuses the unsafe write. | Owner resolves the conflict; rerun the preview. |
| Target or requested effects changed after preview. | Agent stops before apply. | Review the new preview; current CLI does not bind the two calls atomically. |
| Installation or separate host registration fails. | Report each phase's actual result. | Inspect and repair the failed phase; do not blindly repeat successful writes. |

### 5. Example result

> Adopt completed. Doctor passed. Existing owner instructions were preserved.
> No work order was approved or started. Next: load the verified session rules.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

[Installer planning and application](../../../se_harness/installer.py) provide these existing commands:

```text
harnessctl init REPO --project-name example --dry-run --json
harnessctl init REPO --project-name example --json
harnessctl adopt REPO --project-name example --dry-run --json
harnessctl adopt REPO --project-name example --json
harnessctl doctor REPO --json
```

Choose one install mode. Neither has an `--apply` flag; `init` does not initialize Git. Preview and apply are separate operations, without reviewed-plan binding.

**Proposed additions**

Add the setup skill and isolated evaluator environment. Adapt supported installation/migration to establish one active skill-discovery route: today's installer supplies repository-local skills too. Do not delete hash-locked copies manually. Optional helpers use qualified plugin loading or the main-agent fallback. These packets do not authorize project agent configuration writes.

**Inputs, outputs, and writes**

- **Inputs:** Target path, project name, installed evaluator identity, owner authorization.
- **Outputs:** Installation plan, conflicts, apply result, diagnostics.
- **Writes:** Managed files/fragments, lock, and adoption inventory where applicable; preserve owner content.

**Host differences**

Both hosts call the same released CLI. Claude Code supports plugin agents; Codex uses qualified packaged loading or the main agent. No project `.codex/agents/` files are written by this setup packet.

**Checks that demonstrate the behavior**

Exercise empty and existing projects, owner-content preservation, conflicts, and interrupted apply. Test skill migration without duplicate discovery or broken integrity.

**Open questions**

DEC-PLG-004 blocks discovery until a supported ownership route exists. Selecting migration requires separate evaluator work, a release, and repository adoption before this scenario can qualify; the alternative requires revising conflicting plugin scope. Preview/apply binding remains an installer improvement.

</details>

## Scenario 3: Start a session

### 1. Purpose and starting point

**Purpose:** Check installation and load the project's governance before governed work.

- **Starts when:** The host emits `SessionStart` for a connected repository.
- **Requires:** A working verified Python environment, enabled hooks, and the exact evaluator version expected by that repository.
- **Successful result:** Verified rules reach the agent in full; readiness is reported.

### 2. Workflow

```text
SessionStart → host shell guard → scripts/session-context.py [New]
        ↓
identity → doctor → verify and read managed governance
        ↓
Host receives complete rules → agent follows the current workflow
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Host → `scripts/session-context.py` **[New]** | `hooks/hooks.json` runs a shell guard. Missing/broken runtime yields setup guidance; otherwise it invokes `ENV_PYTHON -I ABS_PLUGIN/scripts/session-context.py`. The handler identifies the repository; an unconnected project needs repository setup. |
| 2 | Handler → environment Python | Repeat the full [SPEC-PLG-002 identity check](../../engineering/plugin-integration/specifications/SPEC-PLG-002.md), compare the repository lock, then run `doctor`. An existing interpreter or earlier successful setup is insufficient. |
| 3 | Handler | Verify the exact bytes it will return: the complete `se-harness:begin` / `end` block in `AGENTS.md` and full `ENGINEERING_HARNESS.md` router. Reject changes during the read. |
| 4 | Handler → host context | Return those rules verbatim with source/digest information. One handler keeps verification before injection; separate matching hooks can run concurrently. |
| 5 | Main agent | Follow the rules. If the host returns a truncated preview or file reference, use `setup` readiness to obtain and read the complete verified text before governed work. |

For explicit readiness, `setup` tells the agent to call `ENV_PYTHON -I ABS_PLUGIN/scripts/session-context.py --readiness REPO` through the host's shell tool, with absolute paths and appropriate quoting. This **[New]** internal adapter option runs the same checks and returns verified context for the agent to read; it does not prove a host hook fired. No startup hook installs, repairs, approves, or starts work.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/setup/SKILL.md` supplies manual retry and full-read fallback. | **New:** readiness instructions. |
| **Hook** | `SessionStart` starts verification and context delivery. | **Reuse:** host event. **New:** registration. |
| **Script** | `scripts/session-context.py` calls the evaluator through environment Python and delivers verified text. | **New:** one small host adapter. |
| **Tool/interface** | Host hook context, plus shell/read tools for explicit fallback. | **Reuse:** native host interfaces. |
| **Evaluator** | `identity` and `doctor` check runtime and managed installation. | **Reuse:** existing checks and integrity helpers. |
| **Subagent** | Not used. | **Not used:** rules go to the main session. |
| **Human** | Resolve installation or instruction conflicts. | **Reuse:** owner decisions; session startup grants none. |
| **External control** | Remote effects remain separately protected. | **Not used:** injecting instructions is not remote enforcement. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Python was removed or its environment cannot run. | The hook cannot establish readiness; a missing interpreter cannot report its own failure. | Use setup through the host shell to rediscover/repair supplied Python and recreate the environment. |
| Version, identity, or integrity mismatch. | No ready claim and no unverified policy injection. | Explicit setup/maintenance, then retry. |
| Rules conflict or are incomplete in context. | Governed work stops. | Resolve the conflict or complete the verified-read fallback. |
| Hook is skipped or times out. | Readiness is unconfirmed; the hook cannot block every tool. | Restore hook activation and run explicit readiness. |

### 5. Example result

> Identity and doctor passed. Managed AGENTS block and complete harness router verified and loaded.
> No lifecycle state changed. Next: inspect the project and select the intended work.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

Reuse [installation inspection](../../../se_harness/preflight.py), [integrity helpers](../../../se_harness/integrity.py), and the checks already used by [harness-orient](../../../templates/repository/standard/.agents/skills/harness-orient/SKILL.md).

```text
harnessctl identity --role released-evaluator --expected-version VERSION --expected-root ENV_DIR --checkout-root REPO --entry-point ENV_ENTRY_POINT --evaluator-payload-sha256 PAYLOAD_SHA256 --evaluator-wheel-sha256 WHEEL_SHA256 --require-isolated-python --json
harnessctl doctor REPO --json
```

**Proposed additions**

`scripts/session-context.py` performs ordered checks and context delivery. Both event-driven startup and the setup skill's explicit readiness route use this routine. Verify returned bytes against the managed lock and retain their identities for full-read fallback. File existence alone is insufficient.

**Inputs, outputs, and writes**

- **Inputs:** Host event, repository path, exact evaluator identity, lock, managed rules.
- **Outputs:** Full verified governance or a concrete readiness failure.
- **Writes:** No repository/lifecycle writes; temporary context may use plugin data or the host transcript.

**Host differences**

Both hosts support `SessionStart` context. Codex has a configurable context budget; Claude Code can return a file reference for large output. Test complete delivery and fallback using each host's [Codex hooks](https://learn.chatgpt.com/docs/hooks#sessionstart) or [Claude Code hooks](https://code.claude.com/docs/en/hooks#sessionstart) contract. Never assume a success exit code proves the model received all rules.

**Checks that demonstrate the behavior**

Verify execution order, missing/removed Python, a conflicting global `harnessctl`, modified policy refusal, concurrent file changes, and oversized context. Explicit readiness must produce the same checks as startup. Measure startup cost on representative repositories and confirm successful readiness adds no approval prompt.

**Open questions**

Measure startup time and prove full-read fallback on each host. Local hook coverage remains limited; [incident #347](https://github.com/mmzen/se_harness/issues/347) requires independent enforcement of privileged actions.

</details>

## Scenario 4: Restore context after compaction or interruption

### 1. Purpose and starting point

**Purpose:** Restore governance and resume from actual state without repeating an uncertain write.

- **Starts when:** `SessionStart` has source `compact` / `resume`, or the user resumes interrupted work.
- **Requires:** The readiness routine from scenario 3 and access to current results.
- **Successful result:** Rules are restored and one current next step is identified.

### 2. Workflow

```text
SessionStart compact/resume → same scripts/session-context.py [New]
        ↓
Verify installation → restore complete governance
        ↓
Agent inspects current artifact and interrupted effects
        ↓
Continue the permitted next step; no blind replay
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Host → `scripts/session-context.py` **[New]** | Run the same readiness routine for `compact` or `resume`. Use `SessionStart`, not `PostCompact`, for rule injection. |
| 2 | Main agent following `setup` **[New]**, if needed | If interruption emits no session event, call `ENV_PYTHON -I ABS_PLUGIN/scripts/session-context.py --readiness REPO` and read its verified context completely. |
| 3 | Agent → environment Python | Run `check` for the explicitly selected artifact to obtain its current state and next action. A conversation summary cannot supply approval. |
| 4 | Agent → existing read/status tools | Inspect actual files, Git state, and any remote workflow/PR result affected by the interrupted operation. Classify effects as completed, incomplete, or unknown. |
| 5 | Agent or accountable human | Follow the current evaluator result. Resolve any pending decision or uncertain effect before a retry; retain authorization that still covers the exact action. |

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/setup/SKILL.md` handles explicit readiness when no hook fires. | **New:** reuse the setup readiness instructions. |
| **Hook** | `SessionStart` sources `compact` / `resume` restore context. | **Reuse:** host events; startup handler is shared. |
| **Script** | `scripts/session-context.py` repeats checks through environment Python. | **New:** shared host adapter, no separate recovery engine. |
| **Tool/interface** | Shell/read tools and existing GitHub status interfaces inspect effects. | **Reuse:** current host and project interfaces. |
| **Evaluator** | Selected `check` returns fresh artifact state. | **Reuse:** existing workflow projection. |
| **Subagent** | Not used. | **Not used:** main-session recovery does not prove subagent recovery. |
| **Human** | Resolve the exact pending decision. | **Reuse:** accountable boundaries survive interruption. |
| **External control** | Project controls govern any external retry. | **Adapt:** verify existing protection; otherwise hand off to the human operator. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Candidate, policy, or selected artifact changed. | Discard stale context and recheck. | Follow current state and applicable authority. |
| Interrupted action may already have completed. | Report unknown outcome; do not replay it. | Inspect the existing commit, record, workflow run, or destination. |
| An approval was pending. | It remains pending after compaction. | The accountable human makes that exact decision. |
| Restored rules are incomplete. | Readiness remains incomplete. | Complete the full-read fallback from scenario 3. |

### 5. Example result

> Governance restored. VREC-DEMO-001 is still ready for the assurance owner's decision.
> No verification decision was recorded. Next: present its candidate and evidence to that owner.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

The [workflow projection](../../../se_harness/workflow.py) supports current-state inspection:

```text
harnessctl check REPO --artifact VREC-DEMO-001 --json
```

Without a checkpoint, this projects state; it does not prove execution gates or remote effects. After an interrupted commit, inspect `git status --short`, `git log -1`, and the relevant diff. After a remote action, inspect its actual PR or workflow run.

**Proposed additions**

Register the same readiness handler for startup, compaction, and resume. The main agent reconciles operation results after receiving the rules; the hook does not guess whether a write completed.

**Inputs, outputs, and writes**

- **Inputs:** Event or explicit request, current repository state, selected artifact, observed effects.
- **Outputs:** Restored governance and one current recovery or decision handoff.
- **Writes:** No repository or lifecycle writes during recovery checks.

**Host differences**

[Codex](https://learn.chatgpt.com/docs/hooks#sessionstart) and [Claude Code](https://code.claude.com/docs/en/hooks#sessionstart) document `SessionStart` with `compact` / `resume`. `PostCompact` is not the documented context-injection route. Test subagent recovery separately.

**Checks that demonstrate the behavior**

Test manual/automatic compaction, process restart, interruption without a hook event, and an uncertain remote result. None may invent an approval or blindly repeat a mutation. Resume permitted work without requesting an unchanged decision again; retain pending decisions as pending.

**Open questions**

Confirm hook delivery and complete context restoration across the supported host versions, including resumption under unchanged valid authority and the existing delegation rules.

</details>
