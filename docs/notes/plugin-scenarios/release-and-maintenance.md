# Plugin scenarios: release and maintenance

<!-- Target expertise: 3.5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

[All scenarios](README.md) · [Workflow overview](../plugin-operation-workflows-2026-09-06.md) · [Scenario template](../plugin-scenario-template.md)

Proposal updated 2026-09-08. **[New]** marks components to build. Current implementation means source at [`aad82a9`](https://github.com/mmzen/se_harness/tree/aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055): candidate 0.16.0, with this repository governed by released evaluator 0.15.0. Interfaces were inspected; the plugin has not been implemented or tested against that released evaluator. This note grants no authority.

`harnessctl` means the plugin's absolute `scripts/harnessctl` path (`scripts/harnessctl.exe` on Windows), as described in the [shared calling convention](README.md#shared-component-names-and-calling-convention). `REPO` is the selected absolute repository path. `*-DEMO-*` identifiers and version `1.2.0` are illustrative.

## Scenario 14: Prepare and approve a release

### 1. Purpose and starting point

**Purpose:** Give the release owner an exact candidate and its evidence to decide on.

- **Starts when:** Release preparation is requested for identified work.
- **Requires:** An approved release contract, eligible work orders, verified coverage for one candidate, and authority for preparation.
- **Successful result:** A release record, called an RLS, records the owner's decision. Publication is separate.

### 2. Workflow

```text
User → evidence [New] → read project release procedure
        ↓
Authorized build/evidence steps → existing prepare-release
        ↓
Ready RLS → remaining project checks → release owner decides
        ↓
Existing transition records that exact decision
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → `evidence` **[New]** | Ask Codex to use the evidence skill to prepare the release, or invoke `/verity-plane:evidence release-prepare` in Claude Code. The agent reads `skills/evidence/SKILL.md` and the project's release procedure. |
| 2 | Agent and preparation owner | Identify the exact REL, WO, VREC, version, candidate, and intended outputs. Confirm applicable preparation authority; separately authorized builds run through the project's existing tools. Reuse eligible retained evidence. |
| 3 | Agent → `scripts/harnessctl` | Run `prepare-release` with those inputs. It writes immediately, creating a `ready` RLS and evidence if checks pass. Do not use it as a preview. |
| 4 | Agent → project tools | Complete required binding and candidate checks. Present their actual results with the exact ready RLS to the release owner. |
| 5 | Release owner → existing decision process | Decide this release. Preparation, passing tests, and an agent's recommendation do not make the decision. |
| 6 | Authorized actor → `scripts/harnessctl` | Run the transition checkpoint and preview for the selected RLS. Apply only the owner's exact decision after fresh checks. Report its observed state; [publication](#scenario-15-publish-or-deploy-the-release) remains separate. |

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/evidence/SKILL.md` guides preparation and the release handoff. | **New:** instructions using existing release procedures. |
| **Hook** | `PreToolUse` calls `scripts/hook-handler` for supported actions. | **Reuse:** host event. **New:** adapter; it cannot approve release. |
| **Script** | `scripts/harnessctl` runs the evaluator; project scripts build and bind evidence. | **New:** packaged entry point. **Reuse:** project release tools. |
| **Tool/interface** | Codex `exec_command` or Claude Code `Bash` / `PowerShell` calls the scripts. | **Reuse:** shell tools and current decision process. |
| **Evaluator** | `prepare-release`, `check`, and `transition` evaluate the selected record. | **Reuse:** existing CLI. |
| **Subagent** | Optional `evidence-reviewer` identifies missing or inconsistent evidence. | **New:** read-only helper; it is not the release owner. |
| **Human** | Authorize preparation, then decide the exact release. | **Reuse:** existing decision rights. |
| **External control** | Existing project controls protect any remote build or decision route. | **Adapt:** verify actor authentication and permissions; no new generic service. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Coverage is incomplete or names different candidates. | Evaluator refuses preparation. | Supply eligible coverage for one candidate. |
| Version or RLS already exists. | Inspect the existing result rather than retrying blindly. | Owner selects the appropriate next action. |
| RLS is ready but the owner's decision is absent. | Stop at the decision handoff. | Owner decides the exact record; recheck before apply. |
| Evidence changed or release was rejected. | Preserve the record and history. | Follow authorized remediation and the evaluator's next step. |

### 5. Example result

> RLS-DEMO-001 is ready for version 1.2.0. Its verification records cover the selected candidate.
> No release decision or publication occurred. Next: the release owner decides this record.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

Reuse [`prepare_release()`](../../../se_harness/provenance.py), [decision rights](../../engineering/DECISION_RIGHTS.md), and the [workflow](../../engineering/WORKFLOW.json):

```text
harnessctl prepare-release REPO --id RLS-DEMO-001 --release-contract REL-DEMO-001 --verification-record VREC-DEMO-001 --work-order WO-DEMO-001 --version 1.2.0 --owner release-owner --json
harnessctl check REPO --artifact RLS-DEMO-001 --checkpoint transition --target released --json
harnessctl transition REPO --set RLS-DEMO-001=released --decision RLS-DEMO-001=release-owner --json
```

Preparation writes immediately. The transition shown previews; an authorized application adds `--apply`. `--owner` and `--decision` do not authenticate a human. The RLS records an earlier candidate commit; it cannot bind its own commit. Only the selected record changes state.

For **SE Harness itself**, read [Release sequences](../developing-se-harness.md#release-sequences) first. The order is: authorized `repository_tools.release_build replay`, then `scripts/create_release_bundle_manifest.py`; `prepare-release`; `scripts/bind_release_distribution.py`; `release-candidate-replay.yml`; release-owner decision. These existing project tools are not portable plugin defaults.

**Proposed additions**

The evidence skill presents the exact inputs and outputs before any writing command and follows the existing decision process. No extra release API or decision service is introduced. Human authentication and decision-to-content binding remain control gaps to enforce independently; a skill cannot supply that guarantee.

**Inputs, outputs, and writes**

- **Inputs:** Contract, verified candidate coverage, work orders, version, preparation authority, later release decision.
- **Outputs:** Ready RLS and evidence, then the observed decision result.
- **Writes:** RLS and retained evidence; later only its selected lifecycle fields. No publication.

**Host differences**

Both hosts use the packaged CLI and project procedure. Claude Code invokes the skill as `/verity-plane:evidence release-prepare`; Codex users request it by name. Shell permission and hook success are not release approval.

**Checks that demonstrate the behavior**

Check exact candidate coverage, immediate preparation writes, and decision handoff. Verify an interrupted preparation is inspected before retry and rejected history remains intact.

**Open questions**

Demonstrate authenticated decision enforcement in each consumer's process before claiming the plugin enforces human approval. Keep the read-only evidence reviewer optional.

</details>

## Scenario 15: Publish or deploy the release

### 1. Purpose and starting point

**Purpose:** Deliver the approved release through the project's controlled publication process.

- **Starts when:** The accountable owner requests a specific publication or deployment.
- **Requires:** A released RLS, exact deliverables/destination, applicable evidence, and authority for that external action.
- **Successful result:** Each requested external effect is observed and reported accurately.

### 2. Workflow

```text
User → evidence [New] → inspect released record and project procedure
        ↓
Present exact release, destination, and workflow to the owner
        ↓
Human operator runs the existing protected publication workflow
        ↓
Agent reads workflow and destination results → report actual delivery
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → `evidence` **[New]** | Ask Codex to use the evidence skill for publication, or invoke `/verity-plane:evidence publish` in Claude Code. The agent reads the project's publication procedure. |
| 2 | Agent → existing read tools | Identify the released RLS, immutable deliverables, destination, workflow, and required external-action decision. Present those exact effects to the owner. |
| 3 | Accountable owner → existing project controls | Authorize the external action. A released RLS or local shell permission alone does not authorize publication. |
| 4 | Human operator → project workflow | Dispatch the existing workflow through its protected interface. The initial plugin hands this action to the human; automated dispatch is deferred until deterministic authority controls are demonstrated. |
| 5 | Existing workflow | Check and publish the approved inputs. For SE Harness, use `publish-pypi.yml` on `main` with the `release_record` input; details below. |
| 6 | Agent → existing GitHub/destination read interfaces | Inspect the run and destination objects. Report each completed, failed, pending, or unknown effect. A green workflow alone is not proof that every destination serves the intended bytes. |

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/evidence/SKILL.md` prepares the publication handoff and reads results. | **New:** instructions for the current project procedure. |
| **Hook** | No hook authorizes or performs publication. | **Not used:** local intervention cannot protect remote credentials. |
| **Script** | Existing project scripts qualify and publish deliverables. | **Reuse:** project publication implementation. |
| **Tool/interface** | Human uses the workflow UI; agent reads existing run/destination interfaces. | **Reuse:** project and provider interfaces. |
| **Evaluator** | RLS checks and release contracts supply prerequisites. | **Reuse:** existing evaluator; no generic publish command. |
| **Subagent** | Not used. | **Not used:** publication needs no extra agent. |
| **Human** | Decide the exact external action and dispatch the workflow. | **Reuse:** accountable owner and operator roles. |
| **External control** | Workflow permissions, protected environments, and credentials enforce publication boundaries. | **Adapt:** verify every privileged route and bypass setting. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Exact external-action authority is missing. | Stop before dispatch. | Obtain the accountable decision over those effects. |
| Deliverable identity differs from the release record. | Publication must refuse the wrong bytes. | Investigate through authorized remediation. |
| Only some destinations succeeded. | Report separate outcomes; no blanket rollback claim. | Inspect remote state and follow the authorized repair/retry procedure. |
| Dispatch or publication times out. | Outcome is unknown. | Locate the existing run/object before any retry. |

### 5. Example result

> Version 1.2.0 is available in the approved registry with the expected digest. Documentation deployment failed.
> The package remains published. Next: inspect the failed deployment and its authorized retry path.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

[PROC-EXTERNAL-ACTION](../../engineering/WORKFLOW.json) owns the authority boundary. There is no generic `harnessctl publish` command.

For **SE Harness itself**, [publish-pypi.yml](../../../.github/workflows/publish-pypi.yml) runs on `main` with sole input `release_record=RLS-ID`. Its `resolve` job reads committed release authority; `qualify` calls [release qualification](../../../.github/workflows/release-qualification.yml); `github_release`, `pypi`, and `pages` perform separate effects; `observe` retains `release-result.json` and public observations. Read [Release sequences](../developing-se-harness.md#release-sequences) for the complete project procedure.

The declared `pypi` environment does not prove live reviewer settings or protect every GitHub/Pages path. Verify those settings and alternate credentials independently.

**Proposed additions**

Add the evidence skill's publication handoff. Reuse each project's actual workflow, without inventing a universal publication service. As [incident #347](https://github.com/mmzen/se_harness/issues/347) showed, local instructions alone cannot enforce the authority boundary. Keep dispatch with the human until checks are enforced where the privileged effects occur.

**Inputs, outputs, and writes**

- **Inputs:** Released RLS, immutable deliverables, destination, workflow, external-action decision.
- **Outputs:** Run identifier, observed destination identities, partial failures, pending decisions.
- **Writes:** Existing workflow's explicitly authorized external effects and evidence; the skill itself reads and presents.

**Host differences**

Both hosts hand off to the same project publication process. Native shell tools or connectors do not gain publication authority merely because they are available.

**Checks that demonstrate the behavior**

Verify publication refusal for wrong bytes or missing authority with local hooks disabled. Inspect partial and timed-out runs before retry. Cover direct dispatch, alternate credentials, and administrator bypasses.

**Open questions**

Which consumer workflow and credential controls satisfy the required boundary? Until proven, describe the plugin as preparing publication, not enforcing or autonomously performing it.

</details>

## Scenario 16: Upgrade or repair the installation

### 1. Purpose and starting point

**Purpose:** Restore or update installation without silently changing the project's governing version.

- **Starts when:** The user requests maintenance or diagnostics identify an installation problem.
- **Requires:** Current/target identities, trusted plugin distribution, repository ownership information, and authority for the changes.
- **Successful result:** Components are compatible, owner content is preserved, and each change is reported.

### 2. Workflow

```text
User → setup [New] → inspect plugin, required version, and doctor result
        ↓
Choose compatible plugin reinstall/update OR explicit repository upgrade
        ↓
Apply the selected authorized change → repeat readiness
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → `setup` **[New]** | Ask Codex to use setup for maintenance, or invoke `/verity-plane:setup maintain` in Claude Code. The agent reads the required repository version and installed plugin identity. |
| 2 | Agent → `scripts/harnessctl` | Run identity and `doctor` where the trusted command is available. Report whether the package, host registration, or repository installation needs attention. |
| 3a | User → plugin manager | For a damaged or incompatible package, reinstall a verified compatible plugin version. This restores the bundled runtime; no separate runtime manager is needed. Reload the plugin and recheck hook trust. |
| 3b | Agent and owner → `scripts/harnessctl` | For an explicitly requested repository upgrade, select the plugin containing the target released evaluator. Run `upgrade` without `--apply`, review the file plan and resolve required work authority, then run `upgrade --apply`. Retain installer evidence where required. |
| 4 | Agent following `setup` | Run `doctor` and the readiness routine from [scenario 3](setup-and-sessions.md#scenario-3-start-a-session). Report the plugin version, repository version, changed files, and actual hook status before resuming work. |

Steps 3a and 3b are alternatives. A plugin update does not authorize changing the repository lock. A startup hook reports problems; it never starts an upgrade.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/setup/SKILL.md` diagnoses and guides the selected maintenance. | **New:** setup maintenance instructions. |
| **Hook** | `SessionStart` can report failure and recheck after repair. | **Reuse:** event. **New:** shared `scripts/hook-handler`; no automatic upgrade. |
| **Script** | `scripts/harnessctl` runs the selected bundled evaluator. | **New:** packaged entry point. **Reuse:** installer implementation. |
| **Tool/interface** | Plugin manager reinstalls/updates; shell tools invoke the CLI. | **Reuse:** host interfaces. |
| **Evaluator** | `identity`, `upgrade`, and `doctor` inspect and change managed installation. | **Reuse:** current commands and conflict handling. |
| **Subagent** | Not used. | **Not used:** diagnostics and owner review suffice. |
| **Human** | Choose the change and resolve conflicts or required work authority. | **Reuse:** installation and repository ownership. |
| **External control** | Trusted plugin supply and host installation controls protect delivery. | **Adapt:** release authenticity and compatibility checks. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Required evaluator differs from the bundled version. | Normal governed operations refuse that pairing. | Install a compatible plugin or authorize an explicit repository upgrade. |
| Compatible package is unavailable offline. | Do not substitute ambient Python or another version. | Restore the verified package through the host's installation route. |
| Managed content conflicts or ownership is unclear. | Installer refuses unsafe application. | Owner resolves the specific conflict; preview again. |
| Apply or host registration fails. | Report actual restored and remaining state. | Inspect before retry; do not assume all layers rolled back. |

### 5. Example result

> A compatible plugin was reinstalled and readiness passed. This repository still uses evaluator 0.15.0.
> No managed project files or lifecycle states changed. Next: resume the selected work.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

Reuse the [installer](../../../se_harness/installer.py) and [simple upgrade contract](../../engineering/released-evaluator-boundary/specifications/SPEC-REB-012.md):

```text
harnessctl upgrade REPO --json
harnessctl upgrade REPO --apply --json
harnessctl doctor REPO --json
```

The first command plans; the second writes using the explicitly selected target released evaluator. No generic repair command exists. Snapshot restoration handles caught installer failures and reports incomplete rollback; it does not prove crash-safe recovery across plugin, host, and repository.

**Proposed additions**

Bundle one exact evaluator per plugin release. Normal calls require a version match. The setup skill allows the existing explicit `upgrade` path to use a selected target evaluator; it must not bypass identity or installer checks. No automatic version resolver or separate runtime cache manager is introduced.

Preserve governance and evidence during plugin removal or rollback. Remove duplicate skills or optional Codex agent registrations only through supported ownership-aware migration, never by deleting hash-locked files manually.

**Inputs, outputs, and writes**

- **Inputs:** Current/target identities, lock, ownership information, reviewed changes, applicable authority.
- **Outputs:** Per-layer results and fresh readiness checks.
- **Writes:** Selected plugin/host changes; managed files and lock only for authorized repository upgrades. Optional `--evidence-output` retains installer evidence. This repository requires it for a governor transition; see [Advancing the root evaluator](../developing-se-harness.md#advancing-the-root-evaluator). No separate evaluator-upgrade approval packet is introduced.

**Host differences**

Use Codex **Plugins** / `/plugins` or Claude Code `/plugin` for package changes. Resolve the current `PLUGIN_ROOT` / `CLAUDE_PLUGIN_ROOT` after updates, rather than remembering an old cache path. Claude Code's persistent plugin data survives updates but is normally removed on final uninstall; durable governance stays in the repository. [Plugin data](https://code.claude.com/docs/en/plugins-reference#persistent-data-directory).

**Checks that demonstrate the behavior**

Test compatible reinstall without lock changes, explicit repository upgrade, wrong-version refusal, owner-content conflicts, and interrupted repair. Verify both the new installation and historical evidence remain truthful.

**Open questions**

Publish a clear plugin/evaluator compatibility table and prove supported rollback. Projects needing different governing versions may need different compatible plugin installations; multi-version management is deferred.

</details>
