# Plugin scenarios: release and maintenance

<!-- Target expertise: 3.5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

[All scenarios](README.md) · [Workflow overview](../plugin-operation-workflows-2026-09-06.md) · [Scenario template](../plugin-scenario-template.md)

Design proposal, reviewed 2026-09-06. Current implementation means source at [`aad82a9`](https://github.com/mmzen/se_harness/tree/aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055): candidate source 0.16.0, with a repository governed by released 0.15.0. These identities are different. Interfaces below were inspected; the plugin integration has not been implemented or exercised against the released evaluator.

Names marked **[New]** are proposed components, not available commands. The [shared component names and calling convention](README.md#shared-component-names-and-calling-convention) apply throughout this page. Existing `harnessctl` examples mean calls through the bridge to the selected external evaluator. `REPO` means the selected absolute repository path; `*-DEMO-*` identifiers and version `1.2.0` describe a fictional consumer project.

## Scenario 14: Prepare and approve a release

### 1. Purpose and starting point

**Purpose:** Give the release owner an exact candidate and its evidence to decide on.

- **Starts when:** The release owner selects release preparation for identified work.
- **Requires:** An approved release contract, eligible work orders, verified coverage for one candidate commit, and the applicable preparation checks.
- **Successful result:** One release record, called an RLS, records the owner's decision. Publication remains a separate operation.

### 2. Workflow

```text
User invokes evidence release-prepare [New]
        ↓
Read the project procedure → Retain any required candidate build
        ↓
scripts/bridge [New] previews inputs → Owner authorizes preparation
        ↓
Existing prepare-release creates a ready RLS → Project checks run
        ↓
decision-review [New] records the owner's decision
        ↓
scripts/bridge rechecks inputs → Existing transition records the decision
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → `evidence` skill **[New]** | **Codex:** ask “Use the verity-plane evidence skill to prepare this release.” **Claude Code:** invoke `/verity-plane:evidence release-prepare`. The agent reads `skills/evidence/SKILL.md` and collects the exact REL, WO, VREC, version, and candidate identifiers. |
| 2 | Agent following `evidence` → project build process | Read the project's release procedure and retain any prerequisite build. In SE Harness, an authorized release WO permits existing `repository_tools.release_build replay`, followed by `scripts/create_release_bundle_manifest.py`. Reuse eligible retained results; preparation authority alone does not authorize a build. |
| 3 | Agent → shell tool → `scripts/bridge` **[New]** | Use Codex `exec_command`, or Claude Code `Bash` / `PowerShell`, to invoke `bin/launcher bridge --request REQUEST_FILE --json` **[New]**. A `review-preview` request for `prepare-release` returns the selected inputs, proposed record/evidence paths, and `plan_id`. It does not run the writing command. |
| 4 | Release owner → `decision-review` **[New]** | Inspect that preparation plan. The interface records the exact authorized action and returns `decision_ref`. Reuse an existing decision if it covers these effects and inputs. This authorizes preparation, not release. |
| 5 | Agent → `scripts/bridge` → existing `prepare-release` | Send `review-apply` with `plan_id` and `decision_ref`. The bridge verifies their binding and calls the evaluator. Passing prerequisites creates a `ready` RLS and retained evaluator evidence; a refusal is returned unchanged. |
| 6 | Agent → project binding and verification process | Complete the contract's authorized evidence steps. In SE Harness, existing `scripts/bind_release_distribution.py` binds the retained bundle to the ready RLS; `release-candidate-replay.yml` then replays it before the release decision. Retain the actual results. |
| 7 | Agent → bridge → release owner | Request `review-preview` for the selected RLS transition. The bridge runs the existing transition checkpoint and transition preview, then presents the resulting record, candidate, and evidence through `decision-review`. The owner decides this exact release or rejection. |
| 8 | Agent → bridge → existing `transition` | Send `review-apply` with the new plan and decision references. After fresh checks, invoke the selected transition with `--apply`. Report the RLS's observed state; publication continues in [scenario 15](#scenario-15-publish-or-deploy-the-release). |

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/evidence/SKILL.md` guides `release-prepare` and `release-review`. | **New:** named entry points to the current release procedure. |
| **Hook** | `PreToolUse` → `hooks/handler` checks supported shell calls before the bridge runs. | **Reuse:** host event. **New:** `hooks/hooks.json` registration and handler; neither approves release. |
| **Script** | `bin/launcher` runs `scripts/bridge`; project scripts produce additional release evidence. | **New:** launcher and bridge. **Reuse:** SE Harness build replay, bundle-manifest, and distribution-binding scripts where this is the consumer project. |
| **Tool/interface** | `exec_command`, `Bash`, or `PowerShell` invokes the launcher; `decision-review` presents exact inputs to the owner. | **Reuse:** shell tools. **New:** authenticated review interface. |
| **Evaluator** | Validate coverage, prepare the record, and evaluate transitions. | **Reuse:** `prepare-release`, `check`, and `transition`. |
| **Subagent** | Optional `evidence-reviewer` reports missing or inconsistent evidence to the main agent. | **New:** read-only role; use the [host-specific registrations](README.md#shared-component-names-and-calling-convention). Its report is not the release decision. |
| **Human** | The release owner authorizes preparation, then decides the exact RLS. | **Reuse:** existing decision rights. **New:** `decision-review` binds the actor to each reviewed action. |
| **External control** | Existing CI protects any selected remote build; the protected decision service backs `decision-review`. | **Reuse:** project controls where present. **New:** authenticated decision binding; publishing uses `publication-gate` in scenario 15. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Coverage is incomplete or names different commits. | The evaluator refuses preparation. | Supply eligible coverage for one candidate and recheck. |
| The version is already reserved. | Preparation refuses a conflicting record. | Inspect the existing RLS; the owner selects the appropriate next action. |
| The RLS is ready but no release decision exists. | The proposed decision interface withholds apply. An actor-name argument alone is not authenticated authority today. | Obtain the owner's decision over the exact record, then recheck it. |
| Evidence changes or the owner rejects the release. | Release does not proceed; history remains visible. | Follow the evaluator's remediation route with authorized scope. |

### 5. Example result

Illustrative handoff before the release decision:

> RLS-DEMO-001 is ready for version 1.2.0. Its verification records cover the selected candidate.
> Preparation created the record and its evidence. No release decision or publication occurred.
> The release owner must decide RLS-DEMO-001.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

The baseline above provides [`prepare_release()`](../../../se_harness/provenance.py), [decision rights](../../engineering/DECISION_RIGHTS.md), and [release procedures](../../engineering/WORKFLOW.json). Inspected command forms:

```text
harnessctl prepare-release REPO --id RLS-DEMO-001 --release-contract REL-DEMO-001 --verification-record VREC-DEMO-001 --work-order WO-DEMO-001 --version 1.2.0 --owner release-owner --json
harnessctl check REPO --artifact RLS-DEMO-001 --checkpoint transition --target released --json
harnessctl transition REPO --set RLS-DEMO-001=released --decision RLS-DEMO-001=release-owner --json
```

Preparation writes immediately; it has no preview flag. The transition shown only previews; authorized application adds `--apply`. The command's `--owner` or `--decision` value does not authenticate a human. The RLS follows the candidate commit it records; it cannot bind its own commit. Only the selected RLS changes state.

**Proposed additions**

The `evidence` skill's `release-prepare` mode builds the preparation request; `release-review` resumes with an existing ready RLS. The new bridge operations are `review-preview` and `review-apply`. The first records exact inputs and intended effects; it must not simulate preview by running `prepare-release`. The second authenticates the decision and rechecks the inputs before the evaluator writes. `decision-review` is the proposed human interface; an agent-supplied `--owner` or `decision_ref` is not proof by itself.

Consumer-specific build and binding remain in the project's release process. For **SE Harness itself**, [Release sequences](../developing-se-harness.md#release-sequences) defines this order: authorized `repository_tools.release_build replay` and `scripts/create_release_bundle_manifest.py` produce the candidate bundle; `prepare-release` creates the ready RLS; `scripts/bind_release_distribution.py` binds that bundle; `release-candidate-replay.yml` supplies the replay evidence before the release decision. An earlier retained build can satisfy the build step. The skill reads this procedure instead of inventing generic build commands. These are existing project components, not portable plugin defaults.

**Inputs, outputs, and writes**

- **Inputs:** Exact contract, verification records, work orders, version, preparation authority, and later release decision.
- **Outputs:** Ready RLS, retained evidence, then the observed decision result.
- **Writes:** New RLS and evaluator evidence; later selected lifecycle fields. No tag, upload, deployment, or inferred changes to included records.

**Host differences**

- **Codex:** Explicitly request the `evidence` skill; the agent calls the launcher with `exec_command`. `PreToolUse` uses the documented `Bash` matcher for this shell tool.
- **Claude Code:** `/verity-plane:evidence release-prepare` or `release-review` selects the proposed mode. The agent calls the launcher with `Bash` or native `PowerShell`. In both hosts, shell permissions and hook success do not prove a release decision. See the [host comparison](../plugin-installation-proposal-2026-09-06.md#native-capabilities-and-their-limits).

**Checks that demonstrate the behavior**

- **Success:** Authorized exact inputs produce one ready record; a later release decision changes only that record.
- **Refusal:** Missing coverage, duplicate version, or missing owner decision prevents the corresponding operation.
- **Recovery:** After interruption, inspect whether the RLS exists before retrying. Preserve rejected and historical records.

**Open questions**

Choose the protected service behind `decision-review` and prove its actor/content binding before enabling `review-apply`. Define how each consumer registers its release-build and evidence operations; the plugin must not assume SE Harness's own scripts exist everywhere.

</details>

## Scenario 15: Publish or deploy the release

### 1. Purpose and starting point

**Purpose:** Deliver the approved release through the project's protected publication process.

- **Starts when:** The accountable owner requests a specific publication or deployment.
- **Requires:** The selected released RLS, exact destination and candidate, applicable evidence, and authority for that external action.
- **Successful result:** The requested effect is observed at its destination, with a truthful report of completed and pending steps.

### 2. Workflow

```text
User invokes evidence publish [New]
        ↓
publication-preview [New] → Owner reviews the exact external action
        ↓
publication-submit [New] → publication-gate [New] checks authority
        ↓
Existing project workflow runs → publication-status [New] reports results
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → `evidence` skill **[New]** | **Codex:** ask “Use the verity-plane evidence skill to publish this release.” **Claude Code:** invoke `/verity-plane:evidence publish`. The agent reads the project's publication procedure and selects the released RLS and destinations. |
| 2 | Agent → shell tool → `scripts/bridge` **[New]** | Invoke the launcher with a `publication-preview` request. The bridge asks `publication-gate` **[New]** to resolve the approved record, immutable deliverables, configured workflow, and destinations. Return these exact effects with `plan_id`; nothing is dispatched. |
| 3 | External-action owner → `decision-review` **[New]** | Review the plan and authorize its external effects. Return an authenticated `decision_ref`, or reuse one that already covers them. A released RLS alone does not supply this decision. |
| 4 | Agent → bridge → `publication-gate` **[New]** | Send `publication-submit` with `plan_id` and `decision_ref`. The protected service rechecks current authority and identities, then dispatches only the configured project workflow. Return `operation_id` and, when available, the provider's run ID. |
| 5 | Existing project publication workflow | Run its protected jobs and environment decisions. In SE Harness, `publish-pypi.yml` on `main`, with input `release_record`, qualifies and publishes the bound release; see the concrete mapping below. |
| 6 | Agent → bridge `publication-status` **[New]** | Query `operation_id`. Read workflow results and destination observations, then report each completed, failed, pending, or unknown effect. A dispatched or green workflow is not enough to assert that every destination serves the expected bytes. |

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/evidence/SKILL.md`, `publish` mode, guides the handoff. | **New:** named entry point to the configured project process. |
| **Hook** | `PreToolUse` → `hooks/handler` inspects supported local bridge calls. | **Reuse:** host event. **New:** local handler; it does not protect remote credentials. |
| **Script** | `bin/launcher` runs `scripts/bridge` for `publication-preview`, `publication-submit`, and `publication-status`. | **New:** bounded client operations. **Reuse:** existing project publication scripts. |
| **Tool/interface** | `exec_command`, `Bash`, or `PowerShell` calls the launcher; the gate uses the provider's workflow API. | **Reuse:** host tools and provider API. **New:** `decision-review` and the gate's configured dispatch mapping. |
| **Evaluator** | Check the RLS and applicable external-action prerequisites. | **Reuse:** selected `check` and existing release contracts. |
| **Subagent** | Not used. | **Not used:** publication credentials stay outside reviewer roles. |
| **Human** | Decide the specific external action in `decision-review`; complete any required environment review. | **Reuse:** accountable owner and existing environment decisions. **New:** exact plan binding. |
| **External control** | `publication-gate` enforces authority at dispatch and each privileged effect. | **New:** protected service binding. **Adapt:** project credentials, environments, and bypass controls. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| There is no authority for the exact destination. | The proposed protected service refuses dispatch or publication. | Obtain the applicable decision; a local tool grant is insufficient. |
| Deliverable identity differs from the record. | The publication process rejects those bytes. | Investigate through authorized remediation; preserve existing records. |
| Some destinations succeeded and others failed. | The result reports each observed effect. There is no blanket rollback claim. | Inspect remote state, then use the project's authorized retry or repair path. |
| A request times out after dispatch. | Its outcome is unknown. | Find the existing run or remote object before retrying; avoid duplicate effects. |

### 5. Example result

Illustrative partial result, where retry is outside the original authorization:

> Version 1.2.0 is available in the approved package registry with the expected digest. Documentation deployment failed.
> The package remains published. The release is not reported as fully delivered.
> The deployment owner must authorize retrying the failed documentation deployment.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

At the stated baseline, [PROC-EXTERNAL-ACTION](../../engineering/WORKFLOW.json) describes the decision boundary. There is no generic `harnessctl publish` operation. The inspected [`publish-pypi.yml`](../../../.github/workflows/publish-pypi.yml) is this repository's implementation, not a portable consumer default. It resolves a released record on `main`, calls [release qualification](../../../.github/workflows/release-qualification.yml), and declares a `pypi` environment. Its live reviewer and bypass settings require separate verification; the YAML does not prove them.

**Proposed additions**

`publication-gate` is a proposed protected service, not an existing host hook or `harnessctl` command. The bridge exposes three named client operations: `publication-preview` returns `plan_id`; `publication-submit` verifies that plan and `decision_ref`, then returns `operation_id`; `publication-status` reads the existing operation. Workflow, permitted ref, destinations, and credential policy come from the service's protected project configuration. The agent cannot submit an arbitrary workflow or destination as an approved replacement.

For **SE Harness itself**, the dispatch mapping is the existing `.github/workflows/publish-pypi.yml`, ref `main`, with the sole workflow input `release_record=RLS-ID`. Its `resolve` job reads committed authority; `qualify` calls `release-qualification.yml`; `github_release`, `pypi`, and `pages` perform the separate effects; `observe` retains `release-result.json` and public observations. The new gate must cover every privileged path, including direct workflow dispatch and alternate credentials. A `pypi` environment alone does not establish protection for GitHub or Pages. This mapping names existing workflow behavior; it does not claim its live controls already satisfy the proposal.

Until that protection is demonstrated, the skill hands the reviewed request to the human operator. See [incident #347](https://github.com/mmzen/se_harness/issues/347). A local bridge refusal cannot prevent another client from using unprotected credentials.

**Inputs, outputs, and writes**

- **Inputs:** Released RLS, destination, approved action, immutable deliverable identities, and workflow reference.
- **Outputs:** Run identifier, per-destination results, observed identities, and remaining decisions.
- **Writes:** Only authorized external effects and their retained evidence. This repository also has separately controlled latest markers described in [Release sequences](../developing-se-harness.md#release-sequences).

**Host differences**

- **Codex:** `exec_command` invokes `bin/launcher`; request the `evidence` skill by name.
- **Claude Code:** `Bash` or `PowerShell` invokes the same launcher after `/verity-plane:evidence publish`. Both hosts use the same remote gate. [Local hook coverage](../plugin-installation-proposal-2026-09-06.md#hooks-useful-intervention-incomplete-enforcement) does not protect calls made elsewhere.

**Checks that demonstrate the behavior**

- **Success:** Approved immutable inputs produce the expected destination objects and verifiable results.
- **Refusal:** Missing authority or wrong digests are denied even with local hooks disabled.
- **Recovery:** A timed-out dispatch is reconciled against its existing run before any retry. Partial publication never triggers an automatic destructive undo.

**Open questions**

Choose the service behind `publication-gate`, its authenticated decision store, and its project configuration format. Verify all credential, direct-dispatch, and administrator routes before claiming enforcement; test status reconciliation for partial or timed-out publication.

</details>

## Scenario 16: Upgrade or repair the installation

### 1. Purpose and starting point

**Purpose:** Restore or update the plugin without silently changing a project's governing version.

- **Starts when:** A user requests an upgrade, or diagnostics identify a missing or incompatible installation component.
- **Requires:** The selected host, repository lock, current and target component identities, trusted distribution metadata, and authority for the proposed changes.
- **Successful result:** The selected components work together, owner content remains intact, and the report identifies every version or file change.

### 2. Workflow

```text
User invokes setup maintain [New]
        ↓
bin/launcher runtime-status [New] → Existing identity / doctor checks
        ↓
Select plugin update, runtime repair, or repository upgrade
        ↓
Owning component previews → Authorized apply → Fresh readiness check
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → `setup` skill **[New]** | **Codex:** ask “Use the verity-plane setup skill to inspect and maintain this installation.” **Claude Code:** invoke `/verity-plane:setup maintain`. The agent reads `skills/setup/SKILL.md`; it does not invoke `harness-orient` while installation may be broken. |
| 2 | Agent → shell tool → `bin/launcher` **[New]** | Use `exec_command`, `Bash`, or `PowerShell` to call `runtime-status --repo REPO --json`. Inspect the repository lock and host registration. Where a trusted runtime is available, the bridge runs existing `identity` and `doctor`. Report which layer needs attention. |
| 3 | Agent following `setup` → owner | Present separate plugin, runtime, and repository changes, with current and target identities. Resolve missing authority for only the selected changes; repository policy determines whether a work order is required. |
| 4a | User → existing plugin manager | For a **plugin update**, use Codex **Plugins** / `/plugins` or Claude Code `/plugin`. Select the intended plugin version, then reload as in [scenario 1](setup-and-sessions.md#scenario-1-install-and-activate-the-plugin). This does not authorize changing the repository's governing version. |
| 4b | Agent → `bin/launcher` **[New]** | For a **runtime repair**, call `runtime-preview --repo REPO --json` to plan the exact locked runtime. After authorization, call `runtime-prepare --plan-id PLAN_ID --json`. Verify staged bytes and identity before activation; repository files remain unchanged. |
| 4c | Agent → launcher → `scripts/bridge` **[New]** | For a **repository upgrade**, first prepare the explicitly selected target released runtime. Send `repository-preview` with action `upgrade` and that target identity; it calls existing `upgrade` without `--apply`. Review the returned file plan. `repository-apply` rechecks `plan_id` and authority, then calls `upgrade --apply`, retaining installer evidence where required. |
| 5 | Agent following `setup` → host controls and bridge | Inspect host registration and hook trust separately. Then call `session-ready` **[New]** to recheck the resulting runtime and managed files and reload governance using [scenario 3](setup-and-sessions.md#scenario-3-start-a-session). Report each layer's observed result. Resume the selected work only when its applicable readiness checks pass. |

Steps 4a–4c are alternatives; a runtime repair does not require a repository upgrade. A `SessionStart` hook may report a problem, but it never starts maintenance automatically.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/setup/SKILL.md`, `maintain` mode, diagnoses and guides the selected repair. | **New:** setup mode. Existing `harness-orient` is used only after readiness is restored, if inspection is requested. |
| **Hook** | `SessionStart` → `hooks/handler` can report a readiness failure. | **Reuse:** host event. **New:** handler; no automatic update or download. |
| **Script** | `bin/launcher` owns runtime repair; `scripts/bridge` owns reviewed installer invocation and readiness checks. | **New:** named wrappers around the existing evaluator and installer. |
| **Tool/interface** | Host plugin manager changes the plugin; `exec_command`, `Bash`, or `PowerShell` runs the launcher. | **Reuse:** host interfaces. **New:** runtime and repository plan binding. |
| **Evaluator** | Plan and apply managed-file changes; check integrity. | **Reuse:** `upgrade`, `doctor`, identity checks, and installer conflict handling. |
| **Subagent** | Not used. | **Not used:** deterministic diagnostics suffice. |
| **Human** | Authorize the selected changes and resolve conflicts. | **Reuse:** installation or repository owner; normal repository work authority still applies. |
| **External control** | Control plugin supply and runtime downloads. | **Adapt:** host installation controls; **New:** trusted release metadata and compatibility checks. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| A compatible runtime is missing offline. | The launcher refuses governed operations; it does not use ambient Python. | Restore the trusted cache or authorize downloading the exact supported runtime. |
| A managed file is customized or its ownership is unclear. | The installer refuses the unsafe apply. | The owner resolves the conflict with a reviewed repair; the plugin does not overwrite it. |
| The plugin update is incompatible with the locked evaluator. | The proposed compatibility check blocks that pairing. | Select a compatible plugin build, or separately authorize a repository upgrade. |
| An apply or host registration fails. | Report the actual restored and remaining state. | Inspect before retrying. Do not assume all layers rolled back together. |

### 5. Example result

Illustrative runtime repair:

> The missing runtime was restored and installation checks passed. This repository still uses evaluator 0.15.0.
> No managed project files or lifecycle states changed.
> Reload the session context before resuming the selected work.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

The inspected baseline has [`plan_install()` and `apply_changes()`](../../../se_harness/installer.py) and the [simple upgrade contract](../../engineering/released-evaluator-boundary/specifications/SPEC-REB-012.md). There is no generic repair command. For a repository upgrade, the launcher selects the explicitly chosen target released evaluator, then uses:

```text
harnessctl upgrade REPO --json
harnessctl upgrade REPO --apply --json
harnessctl doctor REPO --json
```

The first command plans; the second writes. Ordinary operations continue to use the repository's locked evaluator. The installer has snapshot restoration for caught failures and reports incomplete rollback. This does not prove recovery from every process crash or atomicity across the host, cache, and repository.

**Proposed additions**

The `setup maintain` mode routes each repair to its owner. The proposed launcher extends `runtime-preview` and `runtime-status` with `--repo REPO` for the locked runtime; preview also accepts `--version TARGET_VERSION` for an explicitly selected upgrade target. These are **New** options. Selecting a target for preparation does not change the repository lock or the runtime used for ordinary work. `runtime-prepare` consumes the exact returned plan as in scenario 1.

The bridge's `repository-preview` / `repository-apply` operations from scenario 2 also accept action `upgrade`. Their plan binds the target runtime, prior lock, managed/owner bytes, changes, evidence path, and applicable authority. Separate existing dry-run/apply calls do not provide that binding. If a prior digest fails, diagnostics may report it, but ordinary mutation remains blocked; only an explicitly authorized repair route may address it.

Plugin rollback selects a compatible build; repository downgrade is not an assumed repair method. Remove duplicate skill or Codex `.codex/agents/` registrations only through an ownership-aware migration. Preserve governance and evidence on disconnect or plugin removal; uninstalling the host plugin does not prove project registrations were cleaned up.

**Inputs, outputs, and writes**

- **Inputs:** Exact current/target identities, lock, ownership information, repair plan, and relevant authorization.
- **Outputs:** Per-layer result and fresh health checks.
- **Writes:** Selected host registration/cache changes; managed files and lock only for authorized repository changes. Optional `--evidence-output` retains installer evidence. This repository requires that evidence for a governor transition; see [Advancing the root evaluator](../developing-se-harness.md#advancing-the-root-evaluator). No separate evaluator-upgrade approval packet is reintroduced.

**Host differences**

- **Codex:** **Plugins** / `/plugins` owns plugin management; `exec_command` calls the launcher. Use persistent `PLUGIN_DATA` for cached runtimes and resolve the current `PLUGIN_ROOT` after an update. Recheck hook trust and project agent registrations.
- **Claude Code:** `/plugin` owns plugin management and `/reload-plugins` reloads definitions; `Bash` or `PowerShell` calls the launcher. Use `CLAUDE_PLUGIN_DATA` and the current `CLAUDE_PLUGIN_ROOT`, not a remembered cache path. Consult the [host differences](../plugin-installation-proposal-2026-09-06.md#native-capabilities-and-their-limits) and [migration plan](../plugin-installation-proposal-2026-09-06.md#distribution-updates-and-migration).

**Checks that demonstrate the behavior**

- **Success:** Updating the plugin or repairing its runtime leaves repository policy unchanged; an authorized repository upgrade changes only its reviewed owned content.
- **Refusal:** Wrong identity, owner-content conflict, or incompatible versions prevent the selected operation.
- **Recovery:** Interrupt each layer independently; preserve owner bytes and historical evidence, then demonstrate retry or compatible plugin rollback.

**Open questions**

Which host versions and evaluator releases will the first plugin support? Demonstrate plan binding, crash recovery, and ownership-aware registration cleanup for that matrix.

</details>
