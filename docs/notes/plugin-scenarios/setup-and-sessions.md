# Plugin scenarios: installation and session readiness

<!-- Target expertise: 3.5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> Proposal, 2026-09-06. This page grants no implementation or decision authority.
> Source baseline: [`aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055`](https://github.com/mmzen/se_harness/tree/aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055), candidate source 0.16.0; this repository is governed by released evaluator 0.15.0.
> The plugin components below are proposed. Existing interfaces were inspected, not exercised against that released evaluator. Host documentation was checked on 2026-09-06; host integration remains untested.

[All scenarios](README.md) · [Operation workflows](../plugin-operation-workflows-2026-09-06.md) · [Scenario template](../plugin-scenario-template.md)

The **launcher** selects the trusted evaluator outside the repository. The **bridge** calls that evaluator with structured arguments. These are proposed shared scripts, not separate policy engines. In command examples, `harnessctl` means this resolved invocation; `REPO` means the selected absolute repository path.

## Scenario 1: Install and activate the plugin

### 1. Purpose and starting point

**Purpose:** Install `verity-plane`, load its skills and hooks, and prepare Python plus `se-harness` without manual environment commands.

- **Starts when:** The user installs the plugin for their account, before connecting a repository.
- **Requires:** Codex or Claude Code, access to the published plugin catalog, and network access or a preloaded runtime.
- **Successful result:** The `setup` skill is available, the evaluator's identity passes, and hook status is reported separately.

**New** below means a proposed Verity Plane component or command that must be built. The proposed plugin and marketplace are both named `verity-plane`; they are not published yet. `MARKETPLACE_SOURCE` means the catalog URL or repository supplied by its publisher.

### 2. Workflow

```text
User installs verity-plane → host loads its manifest
        ↓
SessionStart → hooks/handler [New] → cached runtime check
        ↓
User invokes setup [New] → agent calls bin/launcher [New]
        ↓
Preview → authorized runtime preparation → existing identity check
        ↓
Report plugin, runtime, and hook status
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → existing plugin manager | **Codex:** open **Plugins**, or `/plugins` in the CLI, and install `verity-plane` from its configured catalog. **Claude Code:** register the catalog with `/plugin marketplace add MARKETPLACE_SOURCE`, then run `/plugin install verity-plane@verity-plane` in user scope. |
| 2 | Host → plugin manifest | Read `.codex-plugin/plugin.json` or `.claude-plugin/plugin.json` **[New]**. Discover `skills/setup/SKILL.md` and register `hooks/hooks.json` **[New]**. Codex loads the plugin in a new session; Claude Code applies changes with `/reload-plugins`. |
| 3 | User → host hook controls | In Codex, review and trust the hook definition; the CLI exposes `/hooks`. Start a fresh session after enablement/trust to exercise `SessionStart`. A skipped first event is not replayed by the setup skill. |
| 4 | `SessionStart` → `hooks/handler` **[New]** | Call `bin/launcher runtime-status --json` **[New]**, using cached files only. Record whether the runtime is available. In an unconnected project, return quietly; do not install anything or invoke a skill. |
| 5 | User → `setup` skill **[New]** | **Codex:** ask “Use the verity-plane setup skill to prepare its runtime.” **Claude Code:** invoke `/verity-plane:setup runtime`. The main agent reads `skills/setup/SKILL.md`. |
| 6 | Agent → existing shell tool | Use Codex `exec_command`, or Claude Code `Bash` / native `PowerShell`, to call `bin/launcher runtime-preview --json` **[New]**. Return the exact version, downloads, cache destination, and plan ID. |
| 7 | Agent → `bin/launcher` **[New]** | Present those effects and resolve any missing authorization. Call `runtime-prepare --plan-id PLAN_ID --json` for that plan. The launcher downloads verified Python and wheel files, installs into staging, checks identity, then activates the completed runtime. |
| 8 | Agent following `setup` | Call `runtime-status` again. Report runtime availability from its result and hook status from observed host evidence. If no hook run was observed, say **unconfirmed**. |

Installation never starts `setup` automatically. Repository initialization is [scenario 2](#scenario-2-initialize-or-adopt-a-repository); governance injection is [scenario 3](#scenario-3-start-a-session).

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `setup`, at `skills/setup/SKILL.md`, guides steps 5–8. | **New:** runtime setup mode. Existing `harness-orient` and `harness-operator-brief` are not invoked; they require an installed repository. |
| **Hook** | `SessionStart` invokes `hooks/handler` through `hooks/hooks.json`. | **Reuse:** host event. **New:** registration and handler; cached checks only. |
| **Script** | `bin/launcher` performs runtime preview, preparation, and status. | **New:** platform executable, usable before Python exists. `scripts/bridge` is not used in this scenario. |
| **Tool/interface** | Plugin manager installs; `exec_command`, `Bash`, or `PowerShell` runs the launcher. | **Reuse:** host interfaces. No new MCP server is needed. |
| **Evaluator** | `harnessctl --version` and `harnessctl identity` check the installed package. | **Reuse:** existing CLI and `inspect_runtime_identity()`. No `doctor` call before repository setup. |
| **Subagent** | Not used. | **Not used:** the main agent follows `setup`; executable code installs the runtime. |
| **Human** | Select the plugin, complete hook trust, and authorize setup effects. | **Reuse:** existing host controls and user authorization. |
| **External control** | No merge, release, or publication occurs. | **Not used:** this scenario establishes no external-action authority. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Hook is untrusted, disabled, or not observed. | Report that status; runtime success does not prove hook activation. | Resolve host enablement/trust, then observe a fresh `SessionStart`. |
| Download, digest, or `identity` check fails. | `bin/launcher` does not activate the staged runtime. | Correct the source/cache problem and retry setup. |
| Preparation is interrupted or the reviewed plan changes. | Keep incomplete files inactive; reject stale plan IDs. | Run `runtime-preview` again and resume only the current authorized plan. |

### 5. Example result

Illustrative output:

> Plugin: loaded. Runtime: installed; version and identity checks passed. SessionStart: observed.
> No repository files changed.
> Next: connect the repository using setup.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

The baseline ships [`harness-orient` and `harness-operator-brief`](../../../pyproject.toml), plus the [identity CLI](../../../se_harness/cli.py) and [identity implementation](../../../se_harness/runtime_identity.py). It ships none of the components marked **New** above.

The launcher executes the installed package through an absolute interpreter with `-I -m se_harness`; it clears inherited `PYTHONPATH`. These existing CLI forms were inspected:

```text
harnessctl --version
harnessctl identity --role released-evaluator --expected-version VERSION --expected-root RUNTIME_ROOT --checkout-root WORKSPACE --require-isolated-python --json
```

`VERSION` and `RUNTIME_ROOT` come from the trusted catalog and authorized setup plan. `WORKSPACE` is the current project path, used to prove the evaluator is outside it. These checks do not substitute for verifying downloaded bytes before execution.

**Proposed additions**

`bin/launcher` and `hooks/handler` are proposed native executables, with `.exe` builds on Windows. Their names describe functions, not Python scripts. The launcher reads `runtime/catalog.json` **[New]**: the default evaluator version and platform-specific interpreter/wheel identities from trusted release metadata.

The three proposed commands are `runtime-preview`, `runtime-prepare --plan-id PLAN_ID`, and `runtime-status`. `runtime-preview` returns the plan ID; `runtime-prepare` checks that the plan and its inputs still match before writing. All support `--json`. The handler invokes the same `runtime-status` operation as the skill. Existing-repository version selection belongs to scenario 2; this first-install example uses the catalog's default.

**Inputs, outputs, and writes**

- **Inputs:** Host/platform, installed plugin root, trusted catalog, workspace boundary, and authorized plan ID.
- **Outputs:** Plan and runtime results as JSON; separate plugin/runtime/hook status for the user.
- **Writes:** User-level plugin registration and its persistent data directory, including setup plans, staging, and completed runtimes. No repository writes.

**Host differences**

- **Codex:** [Plugins](https://learn.chatgpt.com/docs/plugins) documents installation and new sessions; [hooks](https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks) documents `/hooks` and separate trust. Resolve executable paths from the installed plugin, using `PLUGIN_ROOT` / `PLUGIN_DATA` in hooks.
- **Claude Code:** [Installation](https://code.claude.com/docs/en/discover-plugins) documents `/plugin` and `/reload-plugins`; [tools](https://code.claude.com/docs/en/tools-reference) names `Bash` and native Windows `PowerShell`. Hooks use `CLAUDE_PLUGIN_ROOT` / `CLAUDE_PLUGIN_DATA`. [Plugin paths](https://code.claude.com/docs/en/plugins-reference#environment-variables) describe their resolution.

Always invoke the resolved absolute launcher path, with host-appropriate quoting. Do not rely on `PATH`. Reloading plugin definitions is not evidence that a particular hook ran.

**Checks that demonstrate the behavior**

- **Success:** No Python installed → explicit `setup` installs and verifies the runtime; host evidence confirms hook execution.
- **Refusal:** Untrusted hook or modified download → no false activation claim.
- **Recovery:** Interrupted installation → retry without selecting partial files or damaging a working runtime.

**Open questions**

Select the interpreter provider and catalog authentication method. Test launcher builds and hook-status observation on each supported host/platform. These remain implementation decisions; the named files and commands above are the proposed interface.

</details>

## Scenario 2: Initialize or adopt a repository

### 1. Purpose and starting point

**Purpose:** Add the harness to a project while preserving its existing content.

- **Starts when:** The user asks to connect a named repository.
- **Requires:** A trusted evaluator and authorization covering the concrete setup effects.
- **Successful result:** Managed content is installed, host registration is reported, and installation checks pass.

### 2. Workflow

```text
User selects a project
        ↓
Installer previews files and conflicts
        ↓
Review effects and resolve missing authorization
        ↓
Apply unchanged plan → register host components → check installation
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Setup skill | Select `init` for an empty/absent directory or `adopt` for an existing project. |
| 2 | Bridge and installer | Preview the target, runtime identity, file changes, and conflicts. |
| 3 | Repository owner | Resolve conflicts and supply any setup authorization not already established. |
| 4 | Bridge and installer | Recheck the reviewed effects, then apply only the authorized plan. |
| 5 | Host adapter | Register any required host resources as a separately reported step. |
| 6 | Bridge | Run installation diagnostics and report the actual result. |

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | Explain setup and its remaining work. | **New:** setup procedure; do not extend orient into a writer. |
| **Hook** | Recognize an unconfigured project. | **New:** optional setup notice; no automatic adoption. |
| **Script** | Present and apply a bounded plan. | **Adapt:** bridge wraps existing installer with reviewed-effect binding. |
| **Tool/interface** | Preview and invoke setup. | **Adapt:** structured interface over `init`/`adopt`. |
| **Evaluator** | Plan, apply, and inspect installation. | **Reuse:** installer and `doctor`. |
| **Subagent** | Not used. | **Not used:** automatic inventory is enough here. |
| **Human** | Authorize concrete repository setup. | **Reuse:** repository owner's existing authority; no product approval is inferred. |
| **External control** | Protect later merge/publication effects. | **Not used:** this setup does not configure or satisfy those controls. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Existing content conflicts with a managed destination. | Installer refuses the installation without writing the planned files. | Owner resolves the conflict; rerun the preview. |
| Reviewed effects changed. | Proposed bridge refuses apply. | Present the refreshed plan and resolve its authorization. |
| Repository installation succeeds but host registration fails. | Report partial setup; do not claim one atomic transaction. | Repair only the failed registration, then repeat diagnostics. |

### 5. Example result

Illustrative output:

> The harness is installed and the installation check passed.
> Existing owner instructions were preserved. No work order was approved or started.
> Next: record the project's engineering facts and prepare its first definition package.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

Inspected [`plan_install()` and `apply_changes()`](../../../se_harness/installer.py), [`_install()`](../../../se_harness/cli.py), and the baseline CLI interface:

```text
harnessctl init REPO --project-name example --dry-run --json
harnessctl init REPO --project-name example --json
harnessctl doctor REPO --json
```

For an existing project use `adopt` in the first two commands. A directory containing only `.git` is nonempty. `init` does not initialize Git. Commands illustrate inspected source; no installation was performed for this note.

**Proposed additions**

Bind apply to the reviewed effects at action time. Today's separate dry-run/apply calls do not supply that guarantee. Define recoverable host registration and one active skill-discovery route: today's installer still supplies repository-local skills.

**Inputs, outputs, and writes**

- **Inputs:** Resolved target, project name, runtime identity, installation plan, and applicable authorization.
- **Outputs:** Written files, diagnostics, conflicts, and unfinished host steps.
- **Writes:** Planned managed files/fragments, lock, adoption inventory where applicable, and explicitly selected host registration.

**Host differences**

- **Codex:** Initial setup may need to register agent resources under `.codex/agents/`; native plugin-agent loading is not established by the manifest documentation. [Custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents).
- **Claude Code:** The plugin supports an `agents/` directory. Its root `CLAUDE.md` is not automatically loaded; repository instructions still matter. [Plugin reference](https://code.claude.com/docs/en/plugins-reference).

**Checks that demonstrate the behavior**

- **Success:** Adopt an existing project → preserve owner content and pass diagnostics.
- **Refusal:** Conflict or changed reviewed effects → no apply.
- **Recovery:** Failed host registration → repository state remains correctly reported and repairable.

**Open questions**

Decide where reviewed-plan binding belongs and how setup removes duplicate discovery without rewriting managed files outside an authorized upgrade.

</details>

## Scenario 3: Start a session

### 1. Purpose and starting point

**Purpose:** Give the agent verified governance rules and current project context before governed work.

- **Starts when:** The host starts or clears a session in an activated repository.
- **Requires:** Enabled trusted hooks, the exact cached evaluator, and readable installed policy.
- **Successful result:** Complete verified governance reaches the agent. No work order is authorized.

### 2. Workflow

```text
SessionStart event
        ↓
Check repository activation and trusted cached runtime
        ↓
Verify installation → read and verify the exact governance text
        ↓
Inject governance plus fresh selected-work context
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Session hook | Invoke one synchronous session-readiness script. |
| 2 | Launcher | Select the repository's exact cached evaluator without downloading anything. |
| 3 | Script and evaluator | Check identity and installation; refuse a readiness result on failure. |
| 4 | Script | Verify the text it will inject: the managed `AGENTS.md` block and full `ENGINEERING_HARNESS.md`. |
| 5 | Bridge | Read the current selected artifact's state and next action, when a selection exists. |
| 6 | Host adapter | Inject the verified rules and bounded current-state result; report any missing context. |

Use one handler: separate hooks may run concurrently and cannot guarantee verification before injection.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | Explain readiness or invoke a manual retry. | **Adapt:** reuse orient's read-only principles; startup is a separate procedure. |
| **Hook** | Trigger the readiness procedure. | **New:** `SessionStart` registration. |
| **Script** | Verify first, then assemble context. | **New:** shared synchronous session-readiness handler. |
| **Tool/interface** | Deliver rules to the model. | **Adapt:** host context output; manual invocation calls the same handler. |
| **Evaluator** | Check integrity and project state. | **Reuse:** identity, `doctor`, and selected `check` projection. |
| **Subagent** | Not used. | **Not used:** no delegated policy interpretation. |
| **Human** | Resolve setup, selection, or conflicting instructions. | **Reuse:** existing accountable roles; session startup makes no decision. |
| **External control** | Enforce protected effects independently. | **New:** required effect-boundary controls remain separate from context injection. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Missing runtime, damaged gate, or lock mismatch. | No ready result or injection of unverified policy; governed operations remain refused through evaluator/bridge checks. | Explicit setup/repair, then repeat readiness. |
| Rules conflict or their full text cannot reach the model. | Report incomplete readiness and stop governed work. | Resolve the conflict or context delivery, then retry. |
| Hook is skipped or times out. | No readiness guarantee exists. A warning alone cannot block arbitrary host tools. | Restore the hook and rerun checks; external authorization stays protected separately. |

### 5. Example result

Illustrative output:

> Installation and governance text verified. The complete managed gate and harness contract are loaded.
> No work order is selected; no lifecycle state changed.
> Next: inspect the project to select the intended work.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

Inspected [`inspect_installation()`](../../../se_harness/preflight.py), [integrity helpers](../../../se_harness/integrity.py), and [orient contract](../../../templates/repository/standard/.agents/skills/harness-orient/SKILL.md). Orient checks identity and installation before executing managed helpers; startup delivery is new.

**Proposed additions**

Inject the verified `se-harness:begin`/`end` block and full router verbatim. Check the injected bytes against the lock; reject concurrent changes. Include bounded state and source/digest information. For oversized output, require an integrity-checked read of verified file references before readiness. No downloads, repairs, full tests, or implicit work selection.

**Inputs, outputs, and writes**

- **Inputs:** Host event, repository path, trusted runtime, lock, managed rules, and optional selected artifact.
- **Outputs:** Verified governance context or a concrete failure.
- **Writes:** No repository writes; host transcript/context storage only.

**Host differences**

- **Codex:** `SessionStart` supports `startup`/`clear` and `additionalContext`; configure a tested output budget. [Hooks](https://learn.chatgpt.com/docs/hooks#sessionstart).
- **Claude Code:** `SessionStart` supports the same sources and context output. Text over 10,000 characters becomes a file reference with preview; complete the verified-read fallback before declaring readiness. [Hooks](https://code.claude.com/docs/en/hooks#sessionstart).

**Checks that demonstrate the behavior**

- **Success:** Valid installation → complete verified gate/router and fresh state delivered in order.
- **Refusal:** Tamper, missing runtime, or oversized rules → no ready claim or automatic repair.
- **Recovery:** Correct installation → rerun the same handler successfully.

**Open questions**

Measure startup cost and context size per supported release. Define enforcement for uncovered host tools; a session hook alone does not close that gap.

</details>

## Scenario 4: Restore context after compaction or interruption

### 1. Purpose and starting point

**Purpose:** Continue from verified repository state after context loss or interruption.

- **Starts when:** A session resumes, compaction finishes, or the user resumes interrupted work.
- **Requires:** The readiness procedure from scenario 3 and access to the current repository state.
- **Successful result:** The agent knows completed effects, pending decisions, and the current next step.

### 2. Workflow

```text
Compaction, session resume, or explicit continuation
        ↓
Repeat installation verification and governance injection
        ↓
Read actual selected-work state and observed effects
        ↓
Return current next step; preserve any pending decision
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Session hook or orient skill | Call the same session-readiness handler used at startup. |
| 2 | Script | Refresh runtime and policy checks. |
| 3 | Bridge | Query the selected artifact and interrupted operation's effects. |
| 4 | Main agent | Report actual state and partial progress. |
| 5 | Main agent or accountable human | Follow the returned next step, retaining any decision boundary. |

An “approved” summary cannot replace an accountable decision or extend it to another candidate.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | Request explicit recovery and explain findings. | **Adapt:** read-only orient path; no hidden replay of writes. |
| **Hook** | Refresh after compaction or session resume. | **New:** `SessionStart` with `compact`/`resume`, reusing startup code. |
| **Script** | Restore verified context and reconcile observed state. | **Adapt:** shared readiness handler plus operation-specific read-only inspection. |
| **Tool/interface** | Deliver refreshed rules and current results. | **Adapt:** host context output or manual structured invocation. |
| **Evaluator** | Return actual state and next action. | **Reuse:** installed diagnostics and selected `check` projection. |
| **Subagent** | Not used. | **Not used:** recovering the parent session does not prove subagent context is restored. |
| **Human** | Resolve changed scope or a pending decision. | **Reuse:** original accountable decision boundaries remain in force. |
| **External control** | Reject stale or absent external-action approval. | **New:** action-time authorization checks remain independent of conversation memory. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Candidate, branch, policy, or selected artifact changed. | Discard stale readiness and do not replay the prior mutation. | Inspect the new state and follow its returned next step. |
| Interrupted action may have completed. | Report uncertain effects; do not retry blindly. | Read files, records, or the external operation result before deciding on a retry. |
| Verification or integration approval was pending. | Work remains at that boundary. | The responsible human makes the exact decision; the operation rechecks current eligibility. |

### 5. Example result

Illustrative output:

> Governance context restored. The verification record is still ready for the assurance owner's decision.
> Compaction did not verify the record or authorize integration.
> Next: present the existing candidate and evidence to the assurance owner.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

Inspected baseline [CLI](../../../se_harness/cli.py) and [workflow projection](../../../se_harness/workflow.py):

```text
harnessctl inspect REPO --json
harnessctl check REPO --artifact WO-DEMO-001 --json
```

`WO-DEMO-001` is illustrative. Without a checkpoint, `check` projects state; it does not prove execution gates passed. No commands were exercised.

**Proposed additions**

Reuse the startup handler and re-read state after interruption. An in-session interruption may have no session-start event; the recovery skill covers explicit continuation. Host transcripts are not an authoritative state store.

**Inputs, outputs, and writes**

- **Inputs:** Verified repository identity, current artifact, candidate, and observed operation results.
- **Outputs:** Restored governance and current recovery/decision handoff.
- **Writes:** No repository or lifecycle writes; host context storage only.

**Host differences**

- **Codex:** `SessionStart` source `compact` runs before the root session's next model request. `PostCompact` does not document context injection. Test subagent recovery separately. [Hooks](https://learn.chatgpt.com/docs/hooks#sessionstart).
- **Claude Code:** Use `SessionStart` source `compact` or `resume`. `PostCompact` is a follow-up notification with no decision control. [Hooks](https://code.claude.com/docs/en/hooks#postcompact).

**Checks that demonstrate the behavior**

- **Success:** Manual and automatic compaction → complete rules restored before continuation.
- **Refusal:** Stale candidate or pending approval → no write replay or inferred decision.
- **Recovery:** Resume after a partially completed operation → report observed effects and exactly one current next step.

**Open questions**

Prove behavior for both hosts across manual compaction, automatic compaction, process restart, and in-session interruption. Specify separate subagent context propagation before supporting delegated recovery.

</details>
