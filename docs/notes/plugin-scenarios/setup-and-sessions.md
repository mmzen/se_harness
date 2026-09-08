# Plugin scenarios: installation and session readiness

<!-- Target expertise: 3.5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

[All scenarios](README.md) · [Operation workflows](../plugin-operation-workflows-2026-09-06.md) · [Scenario template](../plugin-scenario-template.md)

Proposal updated 2026-09-08. **[New]** marks components to build. Current implementation means source at [`aad82a9`](https://github.com/mmzen/se_harness/tree/aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055): candidate 0.16.0, with this repository governed by released evaluator 0.15.0. Interfaces were inspected; the plugin has not been implemented or tested against that released evaluator. This note grants no authority.

`harnessctl` below means the plugin's absolute `scripts/harnessctl` path (`scripts/harnessctl.exe` on Windows), never a command found on `PATH`. `REPO` is the selected absolute project path. See the [shared calling convention](README.md#shared-component-names-and-calling-convention).

## Scenario 1: Install and activate the plugin

### 1. Purpose and starting point

**Purpose:** Install the plugin with its working `harnessctl` command. No manual Python or environment setup.

- **Starts when:** The user installs `verity-plane`.
- **Requires:** A supported host/platform and access to the published plugin package.
- **Successful result:** Skills load, the bundled command passes identity checks, and hook activation is confirmed separately.

### 2. Workflow

```text
User installs plugin → host installs skills, hooks, and bundled runtime
        ↓
User enables hooks → new session → SessionStart
        ↓
scripts/session-context [New] → scripts/harnessctl identity
        ↓
Report readiness; connect the repository next
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → plugin manager | **Codex:** install from **Plugins** or `/plugins`. **Claude Code:** register the published catalog with `/plugin marketplace add MARKETPLACE_SOURCE`, then `/plugin install verity-plane@verity-plane`. These proposed plugin/catalog names are not published yet. |
| 2 | Host | Install the manifest, skills, hooks, and ready-to-run command with its bundled Python and released `se-harness` package. No separate runtime installation is requested. |
| 3 | User → host controls | Enable the plugin and any required hook trust. Codex exposes `/hooks` in the CLI and loads the plugin in a new session. Claude Code supports `/reload-plugins`; start a new session to observe startup. |
| 4 | `SessionStart` → `scripts/session-context` **[New]** | Verify the bundled evaluator's identity. For a governed project, continue with [scenario 3](#scenario-3-start-a-session). Otherwise, report that repository setup is still needed; do not initialize it. |
| 5 | Main agent following `setup` **[New]**, if requested | Explain any failure and the next setup step. If no hook run was observed, report hook activation as **unconfirmed**, even if the command works. |

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/setup/SKILL.md` explains installation and failures. | **New:** setup instructions; no automatic skill invocation. |
| **Hook** | `SessionStart` runs `scripts/session-context`. | **Reuse:** host event. **New:** `hooks/hooks.json` registration. |
| **Script** | `scripts/harnessctl` runs the bundled evaluator; `scripts/session-context` adapts host events. | **New:** packaging and small host adapter. |
| **Tool/interface** | Plugin manager installs the package; the host runs its hook. | **Reuse:** native host interfaces. |
| **Evaluator** | `--version` and `identity` check the installed engine. | **Reuse:** existing CLI and runtime identity checks. |
| **Subagent** | Not used. | **Not used:** installation requires no delegated agent. |
| **Human** | Choose the plugin and complete host trust. | **Reuse:** host installation controls. |
| **External control** | Verify the delivered plugin/runtime package. | **Adapt:** trusted release distribution and platform packaging. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Unsupported platform or damaged package. | No ready claim; never fall back to ambient Python. | Install a supported, verified plugin package. |
| Hook disabled, untrusted, or not observed. | Report its actual status. | Complete host enablement/trust and observe a new session. |
| Bundled version differs from the project's required version. | Normal governed operations stop. | Use a compatible plugin version or explicitly authorize a [repository upgrade](release-and-maintenance.md#scenario-16-upgrade-or-repair-the-installation). |

### 5. Example result

> Plugin loaded. Bundled evaluator identity passed. SessionStart observed.
> This project is not connected yet. Next: use setup to connect it.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

The [CLI](../../../se_harness/cli.py), [runtime identity checks](../../../se_harness/runtime_identity.py), package metadata, and templates already exist. The plugin distribution does not.

```text
harnessctl --version
harnessctl identity --role released-evaluator --expected-version VERSION --expected-root RUNTIME_ROOT --checkout-root REPO --require-isolated-python --json
```

Trusted package metadata supplies the expected version/root. The command runs an absolute bundled interpreter with `-I -m se_harness` and clears inherited `PYTHONPATH`. Verify distribution authenticity before executing it. The package must preserve the metadata and templates used by identity checks; a frozen executable is not automatically equivalent.

**Proposed additions**

Ship `scripts/harnessctl`, portable Python, and one exact published evaluator release together, outside the target repository. Build the Windows entry point as `scripts/harnessctl.exe`. Provide `scripts/session-context` and `scripts/check-tool-action` for each supported platform. No separate public runtime-management commands are needed.

**Inputs, outputs, and writes**

- **Inputs:** Host/platform, trusted plugin package, and selected repository boundary.
- **Outputs:** Plugin, evaluator, and hook status.
- **Writes:** Host plugin installation only; no project files or lifecycle state.

**Host differences**

- **Codex:** Resolve installed paths through `PLUGIN_ROOT`; complete separate [hook trust](https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks).
- **Claude Code:** Use `${CLAUDE_PLUGIN_ROOT}/scripts/harnessctl`. Top-level `bin/` is rejected by [organization distribution](https://code.claude.com/docs/en/plugin-marketplaces#keep-executables-out-of-the-top-level-bin-directory). Manifest `dependencies` names other plugins, not Python packages. [Plugin reference](https://code.claude.com/docs/en/plugins-reference#plugin-manifest-schema).

Claude Code permits Python setup through hooks; bundling is our simpler product choice, not a host restriction. Supported platform packaging still needs implementation.

**Checks that demonstrate the behavior**

Install on a machine without Python; confirm the bundled command works. Reject a modified package and wrong evaluator identity. Verify hook activation independently of command availability.

**Open questions**

Select the portable Python distribution and first supported host/platform matrix. Prove relocation, package identity, and update behavior before release.

</details>

## Scenario 2: Initialize or adopt a repository

### 1. Purpose and starting point

**Purpose:** Connect a project while preserving owner content.

- **Starts when:** The user asks the `setup` skill to connect `REPO`.
- **Requires:** A working plugin and authority for the listed installation effects.
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
| 3 | Agent → `scripts/harnessctl` | Run the selected command with `--dry-run --json`. Show planned paths, preserved owner content, and conflicts. |
| 4 | Agent and owner | Resolve conflicts and any missing authorization. If target content changed since the preview, repeat it. |
| 5 | Agent → `scripts/harnessctl` | Run the same `init` or `adopt` command without `--dry-run`. Then run `doctor`. Report the actual result and continue with [session readiness](#scenario-3-start-a-session). |

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/setup/SKILL.md` selects and explains the installation steps. | **New:** instructions around current commands. |
| **Hook** | No hook initializes a repository. | **Not used:** setup requires an explicit request. |
| **Script** | `scripts/harnessctl` exposes the existing installer. | **New:** bundled entry point. **Reuse:** installer implementation. |
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

Add the setup skill and bundled entry point. Adapt supported installation/migration to establish one active skill-discovery route: today's installer supplies repository-local skills too. Do not delete hash-locked copies manually. Any optional host agent registration is a separately reported phase, not part of an atomic repository installation.

**Inputs, outputs, and writes**

- **Inputs:** Target path, project name, bundled evaluator identity, owner authorization.
- **Outputs:** Installation plan, conflicts, apply result, diagnostics.
- **Writes:** Managed files/fragments, lock, and adoption inventory where applicable; preserve owner content.

**Host differences**

Both hosts call the same bundled CLI. Claude Code discovers plugin agents natively. Optional Codex project-agent registration needs its own supported setup step; it is not required to initialize the repository.

**Checks that demonstrate the behavior**

Exercise empty and existing projects, owner-content preservation, conflicts, and interrupted apply. Test skill migration without duplicate discovery or broken integrity.

**Open questions**

Finish the supported migration from repository-local skills. Preview/apply binding is an installer improvement, not something a prose skill can guarantee.

</details>

## Scenario 3: Start a session

### 1. Purpose and starting point

**Purpose:** Check installation and load the project's governance before governed work.

- **Starts when:** The host emits `SessionStart` for a connected repository.
- **Requires:** Enabled hooks and the exact evaluator version expected by that repository.
- **Successful result:** Verified rules reach the agent in full; readiness is reported.

### 2. Workflow

```text
SessionStart → scripts/session-context [New]
        ↓
identity → doctor → verify and read managed governance
        ↓
Host receives complete rules → agent follows the current workflow
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Host → `scripts/session-context` **[New]** | `hooks/hooks.json` registers one synchronous handler. It identifies the repository; an unconnected project needs setup instead. |
| 2 | Handler → `scripts/harnessctl` | Check the bundled evaluator against the repository's required version and trusted package identity, then run `doctor`. Stop readiness on failure. |
| 3 | Handler | Verify the exact bytes it will return: the complete `se-harness:begin` / `end` block in `AGENTS.md` and full `ENGINEERING_HARNESS.md` router. Reject changes during the read. |
| 4 | Handler → host context | Return those rules verbatim with source/digest information. One handler keeps verification before injection; separate matching hooks can run concurrently. |
| 5 | Main agent | Follow the rules. If the host returns a truncated preview or file reference, use `setup` readiness to obtain and read the complete verified text before governed work. |

For explicit readiness, `setup` tells the agent to call `scripts/session-context --readiness REPO` through the host's shell tool, using the absolute plugin path and `.exe` on Windows. This **[New]** internal adapter option runs the same checks and returns verified context for the agent to read; it does not prove a host hook fired. No startup hook installs, repairs, approves, or starts work.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/setup/SKILL.md` supplies manual retry and full-read fallback. | **New:** readiness instructions. |
| **Hook** | `SessionStart` starts verification and context delivery. | **Reuse:** host event. **New:** registration. |
| **Script** | `scripts/session-context` calls `scripts/harnessctl` and delivers verified text. | **New:** one small host adapter. |
| **Tool/interface** | Host hook context, plus shell/read tools for explicit fallback. | **Reuse:** native host interfaces. |
| **Evaluator** | `identity` and `doctor` check runtime and managed installation. | **Reuse:** existing checks and integrity helpers. |
| **Subagent** | Not used. | **Not used:** rules go to the main session. |
| **Human** | Resolve installation or instruction conflicts. | **Reuse:** owner decisions; session startup grants none. |
| **External control** | Remote effects remain separately protected. | **Not used:** injecting instructions is not remote enforcement. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
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
harnessctl identity --role released-evaluator --expected-version VERSION --expected-root RUNTIME_ROOT --checkout-root REPO --require-isolated-python --json
harnessctl doctor REPO --json
```

**Proposed additions**

`scripts/session-context` performs ordered checks and context delivery. Both event-driven startup and the setup skill's explicit readiness route use this routine. Verify returned bytes against the managed lock and retain their identities for full-read fallback. File existence alone is insufficient.

**Inputs, outputs, and writes**

- **Inputs:** Host event, repository path, exact evaluator identity, lock, managed rules.
- **Outputs:** Full verified governance or a concrete readiness failure.
- **Writes:** No repository/lifecycle writes; temporary context may use plugin data or the host transcript.

**Host differences**

Both hosts support `SessionStart` context. Codex has a configurable context budget; Claude Code can return a file reference for large output. Test complete delivery and fallback using each host's [Codex hooks](https://learn.chatgpt.com/docs/hooks#sessionstart) or [Claude Code hooks](https://code.claude.com/docs/en/hooks#sessionstart) contract. Never assume a success exit code proves the model received all rules.

**Checks that demonstrate the behavior**

Verify execution order, modified policy refusal, concurrent file changes, and oversized context. Explicit readiness must produce the same checks as startup.

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
SessionStart compact/resume → same scripts/session-context [New]
        ↓
Verify installation → restore complete governance
        ↓
Agent inspects current artifact and interrupted effects
        ↓
Continue the permitted next step; no blind replay
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Host → `scripts/session-context` **[New]** | Run the same readiness routine for `compact` or `resume`. Use `SessionStart`, not `PostCompact`, for rule injection. |
| 2 | Main agent following `setup` **[New]**, if needed | If interruption emits no session event, call `scripts/session-context --readiness REPO` and read its verified context completely. |
| 3 | Agent → `scripts/harnessctl` | Run `check` for the explicitly selected artifact to obtain its current state and next action. A conversation summary cannot supply approval. |
| 4 | Agent → existing read/status tools | Inspect actual files, Git state, and any remote workflow/PR result affected by the interrupted operation. Classify effects as completed, incomplete, or unknown. |
| 5 | Agent or accountable human | Follow the current evaluator result. Resolve any pending decision or uncertain effect before a retry; retain authorization that still covers the exact action. |

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/setup/SKILL.md` handles explicit readiness when no hook fires. | **New:** reuse the setup readiness instructions. |
| **Hook** | `SessionStart` sources `compact` / `resume` restore context. | **Reuse:** host events; startup handler is shared. |
| **Script** | `scripts/session-context` repeats checks through `scripts/harnessctl`. | **New:** shared host adapter, no separate recovery engine. |
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

Test manual/automatic compaction, process restart, interruption without a hook event, and an uncertain remote result. None may invent an approval or automatically repeat a mutation.

**Open questions**

Confirm hook delivery and complete context restoration across the supported host versions. Until tested separately, keep delegated recovery out of the initial release.

</details>
