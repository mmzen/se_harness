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

**Purpose:** Connect a project to Verity Plane without replacing its existing owner content.

- **Starts when:** The user invokes the new `setup` skill for a named repository.
- **Requires:** The plugin and trusted runtime from scenario 1, plus authorization covering the concrete setup effects.
- **Successful result:** Repository installation, host registration, and installation checks each have a reported result.

### 2. Workflow

```text
User invokes setup repository [New]
        ↓
Agent → bin/launcher → scripts/bridge [New]
        ↓
repository-preview → existing init/adopt --dry-run → reviewed plan
        ↓
repository-apply → existing installer → separate host registration
        ↓
Existing doctor → report each setup phase
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → `setup` skill **[New]** | **Codex:** ask “Use the verity-plane setup skill to connect REPO.” **Claude Code:** invoke `/verity-plane:setup repository REPO`. The main agent reads `skills/setup/SKILL.md` and resolves the absolute target. |
| 2 | Agent → `bin/launcher` **[New]** | Call `runtime-status --repo REPO --json` **[New]** to check the target's runtime. If the harness is already installed, select its exact configured version and route to readiness or [upgrade](release-and-maintenance.md#scenario-16-upgrade-or-repair-the-installation). Do not run `init` again. |
| 3 | Agent → existing shell tool | Use Codex `exec_command`, or Claude Code `Bash` / `PowerShell`, to call `bin/launcher bridge --request REQUEST_FILE --json` **[New]**. The request selects `repository-preview`, action `init` or `adopt`, the target, and project name. |
| 4 | `scripts/bridge` **[New]** → existing installer | Confirm that `init` targets an absent or empty directory, or that `adopt` targets a nonempty directory, including one containing only `.git`. Call the selected command with `--dry-run --json`. Return a plan ID, repository changes, conflicts, and any separate host registration changes. |
| 5 | Agent and repository owner | Review the named destinations and effects. Reuse authorization that already covers them; resolve missing authority or conflicts before applying. A successful preview does not authorize writes. |
| 6 | Agent → `scripts/bridge` **[New]** | Send `repository-apply` with the returned `plan_id`. Recheck the target, runtime, file digests, and current authorization. If unchanged and authorized, invoke the existing installer without `--dry-run`. |
| 7 | `scripts/bridge` **[New]** → host registration phase | Apply only the separately listed registration changes. For Codex, this can register plugin-supplied agent definitions under `.codex/agents/`; Claude Code already discovers native plugin `agents/`. Report this phase separately from repository installation. |
| 8 | `scripts/bridge` → existing evaluator; agent | Run `harnessctl doctor REPO --json` with the selected evaluator. Report installation, registration, and diagnostics separately. Once all required setup phases pass, continue with [session readiness](#scenario-3-start-a-session). |

A `SessionStart` hook never invokes repository setup. The `setup` skill instructs the agent; `scripts/bridge` performs the named operations.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `setup`, at `skills/setup/SKILL.md`, guides repository mode. | **New:** explicit setup instructions. Existing `harness-orient` remains read-only. |
| **Hook** | No hook installs or adopts the project. | **Not used:** `SessionStart` can report readiness separately; it cannot authorize setup. |
| **Script** | `bin/launcher` selects the runtime; `scripts/bridge` previews and applies the plan. | **New:** shared entry points and reviewed-plan binding around the existing installer. |
| **Tool/interface** | `exec_command`, `Bash`, or `PowerShell` invokes `bin/launcher bridge --request REQUEST_FILE --json`. | **Reuse:** host shell tools. **New:** `repository-preview` and `repository-apply` structured operations. |
| **Evaluator** | `init` / `adopt` plan and install; `doctor` checks the result. | **Reuse:** `plan_install()`, `apply_changes()`, and existing CLI commands. |
| **Subagent** | Not used. | **Not used:** the main agent handles the review; code inventories the target. |
| **Human** | Repository owner authorizes the listed setup effects. | **Reuse:** existing owner authority. Setup supplies no product or work-order approval. |
| **External control** | No integration or publication occurs. | **Not used:** setup does not configure or satisfy protected remote-action controls. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Required runtime is unavailable. | `bin/launcher` returns the missing version; preview does not install it automatically. | Use the explicit runtime preparation from scenario 1, then repeat repository preview. |
| A managed destination conflicts with existing content. | The installer reports the path and refuses to write the installation. | The owner resolves the conflict; `repository-preview` produces a fresh plan. |
| Reviewed files, target, runtime, or authority changed. | `repository-apply` rejects the stale plan. | Review a fresh preview and resolve any missing authorization. |
| Installation succeeds but host registration fails. | Report partial setup; do not rerun the installer blindly. | Preview the remaining registration changes and repair only that phase, then repeat diagnostics. |

### 5. Example result

Illustrative output:

> Repository installation: complete through adopt. Host registration: complete. Doctor: passed.
> Existing owner instructions were preserved. No work order was approved or started.
> Next: run setup readiness for this repository.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

Inspected [`plan_install()` and `apply_changes()`](../../../se_harness/installer.py), [`_install()`](../../../se_harness/cli.py), and these existing CLI forms:

```text
harnessctl init REPO --project-name example --dry-run --json
harnessctl init REPO --project-name example --json
harnessctl adopt REPO --project-name example --dry-run --json
harnessctl adopt REPO --project-name example --json
harnessctl doctor REPO --json
```

The bridge selects one install mode, not both. `init` does not initialize Git. These examples show evaluator argument lists, resolved through the trusted launcher; they are not instructions to use `harnessctl` from `PATH`. No installation was performed for this note.

**Proposed additions**

`repository-preview` and `repository-apply` are new operations of `scripts/bridge`, invoked through the shared launcher. The request contains an operation, `repo`, and operation-specific fields; preview supplies the install action and project name, while apply supplies its `plan_id`. Request files contain structured values, not arbitrary shell commands.

For an unconnected target, `runtime-status --repo REPO --json` checks the catalog's default runtime; for an installed target it checks the locked version. The target-aware option is **New**.

Preview binds the plan to the repository, evaluator version, input digests, and listed registration effects. Apply rechecks those inputs and current authorization. Today's separate `--dry-run` and apply calls do not provide this binding. Repository writes and host registration remain distinct phases with separate results and recovery.

Today's installer still supplies repository-local skills. Setup must establish one active discovery route through a supported installation or upgrade; it must not delete or rewrite locked skill copies to suppress duplicates.

**Inputs, outputs, and writes**

- **Inputs:** Absolute target, project name, trusted evaluator identity, selected host, reviewed plan ID, and applicable authorization.
- **Outputs:** Plan, conflicts, per-phase results, and `doctor` diagnostics.
- **Writes:** Planned managed files/fragments, lock, adoption inventory where applicable, and explicitly listed host registration. Plans and request files use plugin data storage.

**Host differences**

- **Codex:** Register only the agent resources named in the reviewed plan under `.codex/agents/`. Native plugin-agent loading is not established by the manifest documentation. [Custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents).
- **Claude Code:** Native plugin `agents/` requires no copied project agent definitions. The plugin's root `CLAUDE.md` is not automatically loaded; repository instructions still matter. [Plugin reference](https://code.claude.com/docs/en/plugins-reference).

**Checks that demonstrate the behavior**

- **Success:** Adopt a nonempty project → preserve owner content and report installation, registration, and diagnostics separately.
- **Refusal:** Conflict or changed plan inputs → no installation apply.
- **Recovery:** Host registration fails after installation → repair the remaining phase without reinstalling or overwriting owner files.

**Open questions**

Prove reviewed-plan binding across interrupted phases. Finalize ownership tracking for host registrations and a supported migration that avoids duplicate skill discovery.

</details>

## Scenario 3: Start a session

### 1. Purpose and starting point

**Purpose:** Load verified governance rules and fresh project state before the agent performs governed work.

- **Starts when:** The host emits `SessionStart` with source `startup` or `clear` in a connected repository.
- **Requires:** Enabled trusted hooks, the exact cached evaluator, and readable installed policy.
- **Successful result:** Complete verified governance reaches the agent. Readiness does not approve or start work.

### 2. Workflow

```text
SessionStart startup/clear → hooks/handler [New]
        ↓
bin/launcher bridge → scripts/bridge: session-ready [New]
        ↓
Existing identity + doctor → verify exact policy bytes
        ↓
Existing check for an explicit selection → current state
        ↓
Host receives verified governance and readiness result
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Existing `SessionStart` → `hooks/handler` **[New]** | `hooks/hooks.json` registers one synchronous handler. The host supplies its event, session, source, and working directory. The handler identifies the repository; an unconnected project returns quietly. |
| 2 | `hooks/handler` → `bin/launcher` **[New]** | Build a structured `session-ready` request and invoke `bin/launcher bridge --request REQUEST_FILE --json`. Select the exact trusted cached evaluator for the repository; do not download or substitute another version. |
| 3 | `scripts/bridge` **[New]** → existing evaluator | Run `harnessctl identity` with the trusted version/root expectations, then `harnessctl doctor REPO --json`. A failure returns its diagnostics and no ready claim. |
| 4 | `scripts/bridge` **[New]** | Read the complete managed `se-harness:begin` / `end` block in `AGENTS.md` and the full `ENGINEERING_HARNESS.md` router. Verify the bytes being returned against the lock; reject a concurrent change. |
| 5 | `scripts/bridge` → existing `check` | If the user already selected an artifact, run `harnessctl check REPO --artifact ID --json` without a checkpoint. Return its current state and next action as a projection. With no explicit selection, report that fact. |
| 6 | `hooks/handler` **[New]** → host context interface | Translate the result into the host's `SessionStart` context output. Include the verified rules verbatim, their source/digest information, and the selected-state result. |
| 7 | Main agent | Use the delivered rules and report readiness. If the host returns only a preview/file reference, invoke `setup readiness` and read the complete verified content before governed work; do not treat the preview as complete governance. |

No skill runs automatically in this path. For a manual retry, the user invokes `skills/setup/SKILL.md` **[New]**: ask Codex to “Use the verity-plane setup skill to check readiness for REPO,” or use `/verity-plane:setup readiness REPO` in Claude Code. The agent invokes the same `session-ready` operation through `exec_command`, `Bash`, or `PowerShell`.

Use one handler: separate hooks may run concurrently and cannot guarantee verification before injection.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `setup` readiness mode provides an explicit retry or full-context fallback. | **New:** `skills/setup/SKILL.md`. Neither `harness-orient` nor `harness-operator-brief` runs automatically. |
| **Hook** | Existing `SessionStart` calls the new `hooks/handler`. | **Reuse:** host event and context output. **New:** `hooks/hooks.json` registration. |
| **Script** | `hooks/handler` adapts host input/output; `bin/launcher` resolves the runtime; `scripts/bridge` performs `session-ready`. | **New:** one shared readiness path for automatic and explicit invocation. |
| **Tool/interface** | Hook context delivers rules; `exec_command`, `Bash`, or `PowerShell` supports explicit readiness. | **Reuse:** host interfaces. **New:** structured `session-ready` operation. |
| **Evaluator** | `identity`, `doctor`, and an explicit selected `check` inspect runtime, installation, and state. | **Reuse:** existing CLI and integrity helpers. `check` without a checkpoint evaluates no execution gates. |
| **Subagent** | Not used. | **Not used:** the main session receives the rules; no delegated policy interpretation occurs. |
| **Human** | Resolve missing setup, conflicting instructions, or ambiguous selection. | **Reuse:** existing authority. Starting a session exercises no decision right. |
| **External control** | Protect later remote effects independently of session context. | **Not used:** this readiness operation has no remote effect; the controls in scenarios 13 and 15 remain necessary. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Missing runtime, damaged managed gate, or lock mismatch. | `session-ready` returns a failure and does not inject unverified policy. Evaluator/bridge checks refuse governed operations. | Explicitly prepare the runtime or repair the installation, then repeat readiness. |
| Rules conflict or the full text cannot reach the model. | The agent reports incomplete readiness and stops governed work. | Resolve the conflict, or use the explicit verified-read fallback before continuing. |
| Hook is skipped or times out. | There is no readiness guarantee. A warning cannot block arbitrary host tools. | Restore hook enablement/trust and invoke `setup readiness`; protect external actions separately. |
| Policy changes between verification and context assembly. | `scripts/bridge` rejects the stale context. | Re-read and reverify the complete policy with `session-ready`. |

### 5. Example result

Illustrative output:

> Identity: passed. Doctor: passed. Managed AGENTS block and complete harness router: verified and loaded.
> No work order is selected; no lifecycle state changed.
> Next: inspect the project to select the intended work.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

Inspected [`inspect_installation()`](../../../se_harness/preflight.py), [integrity helpers](../../../se_harness/integrity.py), the [CLI](../../../se_harness/cli.py), and the [orient contract](../../../templates/repository/standard/.agents/skills/harness-orient/SKILL.md). Orient already checks identity and installation before executing managed helpers; automatic context delivery is new.

The bridge invokes these existing forms through the isolated external evaluator:

```text
harnessctl identity --role released-evaluator --expected-version VERSION --expected-root RUNTIME_ROOT --checkout-root REPO --require-isolated-python --json
harnessctl doctor REPO --json
harnessctl check REPO --artifact WO-DEMO-001 --json
```

The final call occurs only for that explicitly selected illustrative work order. `VERSION` and `RUNTIME_ROOT` are trusted expected values, not values accepted from the runtime's own answer. No commands were exercised for this note.

**Proposed additions**

`session-ready` is a read-only operation of `scripts/bridge`. Its request names `repo`, the host event/source, and any explicit selection. `hooks/handler` creates that request automatically; an agent following `setup readiness` submits the same operation explicitly.

Verify the exact text returned, including the managed block markers and complete router. Retain source/digest information and reject changed bytes. If context is too large, the explicit path returns verified file references and requires the agent to read their full content with Codex `exec_command` or Claude Code `Read`, with a matching integrity check. Readiness remains incomplete until complete delivery is established. The host adapter and skill must not reduce this to “the file exists.”

There are no downloads, repairs, full tests, lifecycle mutations, or implicit work selection in `session-ready`.

**Inputs, outputs, and writes**

- **Inputs:** Host event/source, absolute repository path, trusted runtime, lock, managed rules, and optional explicit artifact selection.
- **Outputs:** Verified governance text, current selected-state projection, and readiness or concrete failure.
- **Writes:** No repository or lifecycle writes. Request/context storage may use plugin data and the host transcript.

**Host differences**

- **Codex:** `SessionStart` supports `startup` / `clear` and `additionalContext`. Configure and test the context budget and full-read fallback. Matching hooks can run concurrently. [Hooks](https://learn.chatgpt.com/docs/hooks#sessionstart).
- **Claude Code:** `SessionStart` supports the same sources and context output. Text over 10,000 characters becomes a file reference with a preview; complete the verified-read fallback before declaring readiness. [Hooks](https://code.claude.com/docs/en/hooks#sessionstart).

**Checks that demonstrate the behavior**

- **Success:** Valid installation → identity and doctor finish before exact rules and fresh selected state are delivered.
- **Refusal:** Tamper, missing runtime, or incomplete context delivery → no ready claim or automatic repair.
- **Recovery:** Correct the failure → explicit `setup readiness` and the hook use the same successful checks.

**Open questions**

Measure startup cost and context size for each host. Demonstrate how the adapter detects full delivery and verifies fallback reads. A session hook alone does not enforce checks for uncovered host tools.

</details>

## Scenario 4: Restore context after compaction or interruption

### 1. Purpose and starting point

**Purpose:** Resume from verified repository state without losing a pending decision or repeating an uncertain write.

- **Starts when:** `SessionStart` has source `compact` / `resume`, or the user explicitly resumes interrupted work.
- **Requires:** The readiness operation from scenario 3 and access to current repository and operation results.
- **Successful result:** Governance is restored; actual effects and the current next step are identified.

### 2. Workflow

```text
SessionStart compact/resume → hooks/handler [New]
    OR user → setup readiness [New]
        ↓
bin/launcher bridge → session-ready [New]
        ↓
Existing identity + doctor + selected check → refreshed context
        ↓
Main agent inspects actual interrupted effects
        ↓
Report observed state and pending decision; no automatic write replay
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Existing `SessionStart` → `hooks/handler` **[New]** | For `compact` or `resume`, invoke the same synchronous handler as startup. It calls `bin/launcher bridge --request REQUEST_FILE --json` with `session-ready`. `PostCompact` does not reinject governance. |
| 2 | User → `setup` readiness **[New]**, when no event occurs | An in-session interruption may emit no new `SessionStart`. Ask Codex to use `setup` readiness for the repository, or invoke `/verity-plane:setup readiness REPO` in Claude Code. The agent uses `exec_command`, `Bash`, or `PowerShell` for the same bridge call. |
| 3 | `scripts/bridge` **[New]** → existing evaluator | Repeat `identity` and `doctor`, verify and deliver the full managed gate/router, and run `check --artifact ID --json` for the explicit selection. Read current files; never recover authority from the conversation summary. |
| 4 | Main agent → existing read tools | Inspect the interrupted operation's actual effects. Use Git read commands for local changes/commits, the current artifact record for a transition, or the remote service's status interface for a submitted external action. A selected `check` result alone cannot prove a network action completed. |
| 5 | Main agent following `setup` | Report completed, incomplete, or uncertain effects from those observations. Use the evaluator's current next step for the selected artifact; keep an unconfirmed external effect unresolved until its service reports a result. |
| 6 | Main agent or accountable human | Continue only the permitted next operation. If scope, candidate, or decision changed, resolve that exact boundary first. No handler or skill automatically repeats the interrupted mutation. |

A summary that says “approved” cannot replace an accountable decision or extend it to another candidate. The recovery route restores context; it grants no new authority.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `setup` readiness mode handles explicit recovery when no hook fires. | **New:** `skills/setup/SKILL.md`. Existing `harness-orient` remains a separately requested inspection skill. |
| **Hook** | `SessionStart` with `compact` / `resume` invokes `hooks/handler`. | **Reuse:** existing events. **New:** registration reuses startup code; no `PostCompact` injection. |
| **Script** | `hooks/handler`, `bin/launcher`, and `scripts/bridge` repeat `session-ready`. | **New:** shared readiness path; no separate recovery policy engine. |
| **Tool/interface** | `exec_command`, `Bash`, `PowerShell`, or `Read` inspects current local results; the remote interface reports external results. | **Reuse:** host read/shell tools. **New:** protected-operation status interfaces are defined with scenarios 13 and 15. |
| **Evaluator** | `identity`, `doctor`, and selected `check` return fresh repository state. | **Reuse:** existing diagnostics and projection; they do not attest to an external service's effects. |
| **Subagent** | Not used. | **Not used:** restoring the parent session does not prove a subagent's context was restored. |
| **Human** | Resolve an exact pending decision or changed authority. | **Reuse:** original accountable boundaries remain in force after interruption. |
| **External control** | The protected service checks current authorization before an external retry. | **New:** action-time enforcement from scenarios 13 and 15; conversation memory cannot replace it. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Candidate, branch, policy, or selection changed. | `session-ready` returns current facts; the agent discards stale context and does not replay the prior mutation. | Follow the refreshed evaluator result and resolve any changed authorization. |
| Interrupted operation may have completed. | The agent reports uncertain effects and withholds a blind retry. | Read the relevant files, Git state, or remote operation status; retry only if still needed and authorized. |
| Verification or integration approval was pending. | The selected operation remains at that decision boundary. | The responsible human makes the exact decision; the operation rechecks eligibility. |
| Restored rules are missing or truncated. | Readiness remains incomplete. | Use the full verified-read fallback from scenario 3 before governed work. |

### 5. Example result

Illustrative output:

> Governance restored. VREC-DEMO-001 is still ready for the assurance owner's decision.
> No verification decision was recorded; compaction did not authorize integration.
> Next: present this candidate and its evidence to the assurance owner.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

Inspected the baseline [CLI](../../../se_harness/cli.py) and [workflow projection](../../../se_harness/workflow.py):

```text
harnessctl inspect REPO --json
harnessctl check REPO --artifact VREC-DEMO-001 --json
```

`VREC-DEMO-001` is illustrative. Without a checkpoint, `check` projects state; it does not prove execution gates passed. An explicitly requested broader inspection can use `inspect`; it is not required on every context restoration. No commands were exercised.

**Proposed additions**

Use the same `session-ready` request and response as scenario 3, with source `compact`, `resume`, or explicit readiness. The handler refreshes governance and selected state. The main agent then reads the operation-specific result; the hook does not guess whether a write completed.

For example, after an interrupted commit, the agent can use its shell tool for `git status --short`, `git log -1`, and the relevant diff. After an uncertain integration request, it reads the protected service's operation status before any retry. A transcript or summary is not the authoritative state store.

**Inputs, outputs, and writes**

- **Inputs:** Event or explicit request, verified repository identity, selected artifact, current candidate, and observed operation results.
- **Outputs:** Restored governance, actual effect status, and one current recovery or decision handoff.
- **Writes:** No repository or lifecycle writes. Request/context storage may use plugin data and the host transcript.

**Host differences**

- **Codex:** `SessionStart` source `compact` runs before the root session's next model request. `PostCompact` does not document context injection. Test subagent recovery separately. [Hooks](https://learn.chatgpt.com/docs/hooks#sessionstart).
- **Claude Code:** Use `SessionStart` source `compact` or `resume`. `PostCompact` is a follow-up notification with no decision control. [Hooks](https://code.claude.com/docs/en/hooks#postcompact).

**Checks that demonstrate the behavior**

- **Success:** Manual or automatic compaction → complete rules and fresh selected state arrive before governed continuation.
- **Refusal:** Stale candidate, missing decision, or unknown external effect → no write replay or inferred approval.
- **Recovery:** In-session interruption with no hook event → explicit `setup readiness`, inspect actual effects, then report one current next step.

**Open questions**

Prove behavior across both hosts for manual compaction, automatic compaction, process restart, and in-session interruption. Define separate subagent context propagation before supporting delegated recovery.

</details>
