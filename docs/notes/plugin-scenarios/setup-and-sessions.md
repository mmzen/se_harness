# Plugin scenarios: installation and session readiness

<!-- Target expertise: 3.5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> Proposal, 2026-09-06. This page grants no implementation or decision authority.
> Source baseline: [`aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055`](https://github.com/mmzen/se_harness/tree/aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055), candidate source 0.16.0; this repository is governed by released evaluator 0.15.0.
> The plugin components below are proposed. Existing interfaces were inspected, not exercised against that released evaluator. Host documentation was checked on 2026-09-06; host integration remains untested.

[All scenarios](README.md) · [Operation workflows](../plugin-operation-workflows-2026-09-06.md) · [Scenario template](../plugin-scenario-template.md)

The **launcher** selects the trusted evaluator outside the repository. The **bridge** calls that evaluator with structured arguments. These are proposed shared scripts, not separate policy engines. In command examples, `harnessctl` means this resolved invocation; `REPO` means the selected absolute repository path.

## Scenario 1: Install and activate the plugin

### 1. Purpose and starting point

**Purpose:** Make Verity Plane available in the coding host without manual Python environment setup.

- **Starts when:** The user chooses to install the plugin and prepare its runtime.
- **Requires:** A supported host and platform, a trusted plugin source, and an approved runtime source or preloaded cache.
- **Successful result:** Skills and hooks are discoverable, and the selected external evaluator is available. Repository setup remains a separate operation.

### 2. Workflow

```text
User installs the native plugin
        ↓
Host loads components and presents required trust decisions
        ↓
User invokes setup; launcher prepares the trusted runtime
        ↓
Report component availability and repository setup action
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User and host | Install the native package in the selected host scope. |
| 2 | User | Complete host trust requirements for the actual hook definitions. |
| 3 | Setup skill and launcher | Select the required release and show any runtime download before performing the authorized setup. |
| 4 | Runtime manager | Verify distribution bytes, install into an isolated cache, and validate the evaluator identity. |
| 5 | Setup skill | Report runtime and component readiness, including missing or unsupported components. |

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | Guide explicit installation follow-up. | **New:** setup instructions; existing orient forbids installation. |
| **Hook** | Report unavailable setup in later sessions. | **New:** session registration; it performs no installation. |
| **Script** | Obtain and select the runtime. | **New:** trusted bootstrap, isolated cache, and platform launcher. |
| **Tool/interface** | Present installation and setup. | **Adapt:** native plugin interface plus a structured setup operation. |
| **Evaluator** | Report the installed evaluator identity. | **Reuse:** released version and runtime identity inspection. |
| **Subagent** | Not used. | **Not used:** installation needs deterministic processing. |
| **Human** | Choose the plugin source and setup effects. | **New:** host installation/trust interaction; no engineering decision is granted. |
| **External control** | Constrain package provenance and protected effects. | **New:** trusted release catalog; remote authorization remains independently enforced. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Required hook is untrusted or unavailable. | Setup reports incomplete readiness. | User resolves trust or selects a supported host. |
| Download or identity check fails. | Launcher refuses to activate that runtime. | Retry from the trusted source or use a verified preloaded cache. |
| Setup is interrupted. | Incomplete cache content remains unavailable for execution. | Runtime manager cleans up its staging area and retries; it preserves the previous working runtime. |

### 5. Example result

Illustrative output:

> Plugin components and the selected evaluator are available.
> No repository files or lifecycle states changed.
> Next: connect the intended repository through setup.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

The baseline ships a Python package and repository installer, without native manifests or a runtime manager. See [package configuration](../../../pyproject.toml) and [runtime identity](../../../se_harness/runtime_identity.py). Source inspection only.

**Proposed additions**

Bootstrap must work without preinstalled Python. Verify the launcher, interpreter, and package before execution; use an absolute isolated interpreter. A repository cannot supply an executable or arbitrary download URL. Select each repository's exact evaluator; plugin updates do not upgrade repositories. See the [runtime trust design](../plugin-installation-proposal-2026-09-06.md#make-runtime-provisioning-a-product-feature).

**Inputs, outputs, and writes**

- **Inputs:** Host/platform, trusted release metadata, and selected release identity.
- **Outputs:** Available components, runtime identity, and unresolved setup steps.
- **Writes:** Host plugin registration and external runtime cache; no repository writes.

**Host differences**

- **Codex:** Native packages use `.codex-plugin/plugin.json`; plugin installation and hook trust are separate. CLI installation needs a new session. [Plugin documentation](https://learn.chatgpt.com/docs/plugins), [hook trust](https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks).
- **Claude Code:** Native packages use `.claude-plugin/plugin.json`; plugin data storage is separate from the changing plugin cache. [Plugin reference](https://code.claude.com/docs/en/plugins-reference).

**Checks that demonstrate the behavior**

- **Success:** Clean machine without Python → verified runtime and discoverable components.
- **Refusal:** Modified runtime bytes → no activation or candidate-source fallback.
- **Recovery:** Interrupted or concurrent installation → one complete runtime; no partial executable selection.

**Open questions**

Choose the interpreter provider and authenticate its release metadata. Prove support on native Windows, Linux, and macOS before publishing the support matrix.

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
