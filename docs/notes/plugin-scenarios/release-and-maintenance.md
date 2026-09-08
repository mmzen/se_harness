# Plugin scenarios: release and maintenance

<!-- Target expertise: 3.5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

[All scenarios](README.md) · [Workflow overview](../plugin-operation-workflows-2026-09-06.md) · [Scenario template](../plugin-scenario-template.md)

Proposal updated 2026-09-08. **[New]** marks components to build. Current implementation means source at [`aad82a9`](https://github.com/mmzen/se_harness/tree/aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055): candidate 0.16.0, governed at that baseline by released evaluator 0.15.0. The [implementation packets](../../engineering/plugin-integration/README.md) use a newer baseline. Interfaces were inspected; the plugin has not been implemented or tested against that released evaluator. This note grants no authority.

`harnessctl` means the absolute verified `ENV_PYTHON -I -m se_harness` invocation, as described in the [shared calling convention](README.md#shared-component-names-and-calling-convention). It is not a custom wrapper or a `PATH` lookup. `REPO` is the selected absolute repository path. `*-DEMO-*` identifiers and version `1.2.0` are illustrative.

The operator or host provides Python 3.11 or later; the plugin ships no Python binary. Setup checks that Python, creates an isolated environment in persistent plugin data outside the repository, and installs the plugin's exact published pure-Python wheel from `packages/` offline. If Python is missing or too old, setup and readiness stop and tell the operator to install it; the plugin never downloads or installs Python. Hooks run `scripts/session-context.py` or `scripts/check-tool-action.py` using verified `ENV_PYTHON -I ABS_SCRIPT` paths.

Continue automatically from an applicable evaluator next step while the request and actual authority cover the action. The skill invocations below are optional direct entry points, not a required prompt at every stage. Reuse decisions that still cover the exact action, content, candidate, and destination; ask only for missing authority or a material change. Neither an evaluator next step nor a reused decision removes any required gate.

## Scenario 14: Prepare and approve a release

### 1. Purpose and starting point

**Purpose:** Give the release owner an exact candidate and its evidence to decide on.

- **Starts when:** Release preparation is the selected next step within the existing request, or it is requested directly for identified work.
- **Requires:** An approved release contract, eligible work orders, verified coverage for one candidate, and authority for preparation.
- **Successful result:** A release record, called an RLS, records the owner's decision. Publication is separate.

### 2. Workflow

```text
Applicable next step or direct request → evidence [New] → release procedure
        ↓
Authorized build/evidence steps → existing prepare-release
        ↓
Ready RLS → remaining project checks → release owner decides
        ↓
Existing transition records that exact decision
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Main agent → `evidence` **[New]** | Continue from the selected release-preparation step within the existing request. Optional direct entry: ask Codex to use the evidence skill, or invoke `/verity-plane:evidence release-prepare` in Claude Code. Read `skills/evidence/SKILL.md` and the project's release procedure. |
| 2 | Agent and preparation owner | Identify the exact REL, WO, VREC, version, candidate, and outputs. Reuse actual preparation and build authority that covers them; ask only if something is missing or changed. Run authorized builds through existing project tools and reuse eligible retained evidence. |
| 3 | Agent → `harnessctl` | Run `prepare-release` with those inputs. It writes immediately, creating a `ready` RLS and evidence if checks pass. Do not use it as a preview. |
| 4 | Agent → project tools | Complete required binding and candidate checks. Present their actual results with the exact ready RLS to the release owner. |
| 5 | Agent and release owner → existing decision process | Reuse the owner's actual decision if it still covers this exact RLS, candidate, and evidence. Otherwise present only the missing or changed release decision. Preparation, tests, and agent recommendations do not decide it. |
| 6 | Authorized actor → `harnessctl` | Run the transition checkpoint and preview for the selected RLS, then apply the applicable owner's decision after current checks. Report the observed state and continue to [publication](#scenario-15-publish-or-deploy-the-release) only when its separate authority and controls are satisfied. No extra skill invocation is required. |

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/evidence/SKILL.md` guides preparation and the release handoff. | **New:** instructions using existing release procedures. |
| **Hook** | `PreToolUse` calls `scripts/check-tool-action.py` for supported actions. | **Reuse:** host event. **New:** adapter; it cannot approve release. |
| **Script** | The existing `se_harness` module runs the evaluator; project scripts build and bind evidence. | **Reuse:** current CLI and project release tools; no custom CLI wrapper. |
| **Tool/interface** | Codex `exec_command` or Claude Code `Bash` / `PowerShell` calls the scripts. | **Reuse:** shell tools and current decision process. |
| **Evaluator** | `prepare-release`, `check`, and `transition` evaluate the selected record. | **Reuse:** existing CLI. |
| **Subagent** | Optional `evidence-reviewer` identifies missing or inconsistent evidence. | **New:** read-only helper; it is not the release owner. |
| **Human** | Retain preparation and release decision rights; provide only missing or changed decisions. | **Reuse:** actual decisions that still cover the selected actions and content. |
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

The evidence skill identifies exact inputs and outputs before writing, reuses applicable authority, and continues through covered steps without duplicate prompts. No extra release API or decision service is introduced. Human authentication and decision-to-content binding remain control gaps to enforce independently; a skill cannot supply that guarantee.

**Inputs, outputs, and writes**

- **Inputs:** Contract, verified candidate coverage, work orders, version, preparation authority, later release decision.
- **Outputs:** Ready RLS and evidence, then the observed decision result.
- **Writes:** RLS and retained evidence; later only its selected lifecycle fields. No publication.

**Host differences**

Both hosts use the installed evaluator and project procedure, automatically following applicable next steps within the request. Direct entry is available as `/verity-plane:evidence release-prepare` in Claude Code or by skill name in Codex. Shell permission and hook success are not release approval.

**Checks that demonstrate the behavior**

Check exact candidate coverage, immediate preparation writes, and reuse of a still-applicable release decision without another prompt. Missing or changed decisions stop the affected action. Verify interrupted preparation is inspected before retry and rejected history remains intact; current gates still run.

**Open questions**

Demonstrate authenticated decision enforcement in each consumer's process before claiming the plugin enforces human approval. Keep the read-only evidence reviewer optional.

</details>

## Scenario 15: Publish or deploy the release

### 1. Purpose and starting point

**Purpose:** Deliver the approved release through the project's controlled publication process.

- **Starts when:** Publication is the selected next step within an existing request, or the accountable owner requests it directly.
- **Requires:** A released RLS, exact deliverables/destination, applicable evidence, and authority for that external action.
- **Successful result:** Each requested external effect is observed and reported accurately.

### 2. Workflow

```text
Applicable next step or direct request → evidence [New] → release procedure
        ↓
Reuse exact external-action authority → check current gates and controls
        ↓
Authorized agent or human runs the existing protected publication workflow
        ↓
Agent reads workflow and destination results → report actual delivery
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Main agent → `evidence` **[New]** | Continue from the selected publication step within the existing request. Optional direct entry: ask Codex to use the evidence skill, or invoke `/verity-plane:evidence publish` in Claude Code. Read the project's publication procedure. |
| 2 | Agent → existing read tools | Identify the released RLS, immutable deliverables, destination, workflow, and required external-action decision. Present those exact effects to the owner. |
| 3 | Agent and accountable owner → existing project controls | Reuse the owner's exact external-action decision while it still covers the deliverables, destination, workflow, and effects. Ask only for missing or changed authority. Release or verification approval and local shell permission do not imply publication authority. |
| 4 | Authorized agent or human → project workflow | Check all current gates and independently enforced external controls. When they are demonstrated, dispatch through the existing protected interface. An agent uses the project's existing tools, with applicable `scripts/check-tool-action.py` checks before covered calls. Missing or unproven external enforcement disables agent automation and produces a specific enforcement blocker. |
| 5 | Existing workflow | Check and publish the approved inputs. For SE Harness, use `publish-pypi.yml` on `main` with the `release_record` input; details below. |
| 6 | Agent → existing GitHub/destination read interfaces | Inspect the run and destination objects. Report each completed, failed, pending, or unknown effect. A green workflow alone is not proof that every destination serves the intended bytes. |

The accountable human keeps the decision right; execution may be performed by an authorized agent or human. Where agent enforcement is missing, a human may use an existing permitted protected route. This is a response to an explicit blocker, not a permanent requirement for a human to operate every publication.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/evidence/SKILL.md` follows the publication procedure and reuses applicable authority. | **New:** instructions for existing project tools. |
| **Hook** | `PreToolUse` calls `scripts/check-tool-action.py` before covered publication requests. | **Reuse:** host event. **New:** required applicable checks; independent controls still protect remote effects. |
| **Script** | Existing project scripts qualify and publish deliverables. | **Reuse:** project publication implementation. |
| **Tool/interface** | An authorized agent uses existing workflow-dispatch tools; a human may use the UI. Both inspect run/destination results. | **Reuse:** project and provider interfaces. |
| **Evaluator** | RLS checks and release contracts supply prerequisites. | **Reuse:** existing evaluator; no generic publish command. |
| **Subagent** | Not used. | **Not used:** publication needs no extra agent. |
| **Human** | Retain the exact external-action decision right; an authorized agent may execute the decision. | **Reuse:** existing accountability, with no added delegation waiver. |
| **External control** | Workflow permissions, protected environments, and credentials enforce publication boundaries. | **Adapt:** verify every privileged route and bypass setting. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Exact external-action authority is missing. | Stop before dispatch. | Obtain the accountable decision over those effects. |
| Independent external controls are missing or unproven. | Disable agent dispatch and report the specific enforcement blocker. | Demonstrate the controls, or use an existing permitted protected human route. Human execution does not waive that route's required controls. |
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

Once exact authority, current gates, and independent controls are satisfied, an authorized agent can dispatch this existing workflow using:

```sh
gh workflow run publish-pypi.yml --repo mmzen/se_harness --ref main --raw-field release_record=RLS-DEMO-001
```

Use the actual release record and preserve the workflow's enforced checks at its privileged effects. This SE Harness example is not a portable default for other projects. Changing the destination, deliverables, or workflow requires checking whether existing authority still covers the action.

**Proposed additions**

The evidence skill follows each project's existing workflow through authorized execution and result inspection. It retains decisions that still apply and requests only missing or changed authority. As [incident #347](https://github.com/mmzen/se_harness/issues/347) showed, local instructions cannot enforce the boundary: agent execution is enabled only after independent checks at privileged effects are demonstrated. No universal publication service or authority waiver is added.

**Inputs, outputs, and writes**

- **Inputs:** Released RLS, immutable deliverables, destination, workflow, external-action decision.
- **Outputs:** Run identifier, observed destination identities, partial failures, pending decisions.
- **Writes:** The authorized agent's or human's dispatch and the workflow's explicitly authorized external effects and evidence. The skill supplies instructions; existing tools execute them.

**Host differences**

Both hosts use the same project publication process. Codex `exec_command` and Claude Code `Bash` / native `PowerShell` can dispatch the existing workflow when execution is authorized and independently controlled. Covered tool calls run the applicable before-effect checks. Tool availability itself confers no publication authority.

**Checks that demonstrate the behavior**

Verify publication refusal for wrong bytes or missing authority with local hooks disabled. Matching existing authority should allow controlled execution without another prompt; changed inputs must be reassessed. Inspect partial and timed-out runs before retry, reusing retry authority only when it covers the remaining effects. Cover direct dispatch, alternate credentials, administrator bypasses, and all current gates.

**Open questions**

Which consumer workflow and credential controls satisfy the required boundary? Name any missing control as an execution blocker; do not claim that the current plugin already enforces it or replace the gap with a blanket human-operator requirement.

</details>

## Scenario 16: Upgrade or repair the installation

### 1. Purpose and starting point

**Purpose:** Restore or update installation using the operator's Python, without silently changing the project's governing version.

- **Starts when:** Maintenance is requested directly, or the applicable next step or readiness diagnostics identify an installation problem within the existing request.
- **Requires:** Operator- or host-provided Python 3.11 or later, current/target identities, a trusted plugin wheel, ownership information, and authority for the changes.
- **Successful result:** Components are compatible, owner content is preserved, and each change is reported.

### 2. Workflow

```text
Applicable next step, diagnostic, or request → setup [New] → check Python
        ↓
Inspect plugin, prepared environment, and required repository version
        ↓
Repair package/environment OR perform an authorized repository upgrade
        ↓
Apply the selected authorized change → repeat readiness
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Main agent → `setup` **[New]** | Continue from applicable diagnostics or a maintenance next step within the request. Optional direct entry: ask Codex to use setup, or invoke `/verity-plane:setup maintain` in Claude Code. First use the host shell to verify provided Python 3.11 or later. If missing or too old, stop and tell the operator to install Python. |
| 2 | Agent → shell tools and existing evaluator | Inspect the provided Python, prepared environment, plugin wheel, and required repository version. Run evaluator identity and `doctor` only when the trusted environment is usable. Report which layer needs attention. |
| 3a | Authorized actor → plugin manager and `setup` | If package files are damaged or incompatible, reinstall a verified compatible plugin version. Reinstallation restores plugin files, not the environment. If the environment needs repair, setup uses the verified provided Python to create an isolated environment outside the repository and install the exact bundled wheel offline. Verify identity before readiness; reload and recheck hook trust where required. |
| 3b | Agent and owner → existing evaluator | For an authorized repository upgrade, select the plugin shipping the target released wheel and prepare its environment through setup. Run `upgrade` without `--apply` and inspect the file plan. Reuse work authority covering that exact change; resolve only missing or changed authority, then run `upgrade --apply`. Retain required installer evidence. |
| 4 | Agent following `setup` | Run `doctor` and the readiness routine from [scenario 3](setup-and-sessions.md#scenario-3-start-a-session). Report the plugin version, repository version, changed files, and actual hook status before resuming work. |

Steps 3a and 3b are alternatives. A plugin update does not authorize changing the repository lock. A startup hook reports problems; it never starts an upgrade. If the provided Python or prepared environment has changed or disappeared, return to setup checks instead of silently choosing another interpreter. The agent handles authorized environment creation; the user does not activate a venv or run global pip.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/setup/SKILL.md` diagnoses and guides the selected maintenance. | **New:** setup maintenance instructions. |
| **Hook** | `SessionStart` can report failure and recheck after repair. | **Reuse:** event. **New:** shared `scripts/session-context.py`; no automatic upgrade. |
| **Script** | `scripts/session-context.py` checks readiness using the prepared environment; the existing `se_harness` module handles upgrade. | **New:** readiness script. **Reuse:** CLI and installer; no Python binary or CLI wrapper. |
| **Tool/interface** | Plugin manager restores plugin files; shell tools verify provided Python, create the environment, and invoke the evaluator. | **Reuse:** host interfaces, Python `venv`, and offline pip. |
| **Evaluator** | `identity`, `upgrade`, and `doctor` inspect and change managed installation. | **Reuse:** current commands and conflict handling. |
| **Subagent** | Not used. | **Not used:** diagnostics and owner review suffice. |
| **Human** | Provide or install Python when needed; choose the change and resolve only missing authority or conflicts. | **Reuse:** operator prerequisites and repository ownership. |
| **External control** | Trusted plugin supply and host installation controls protect delivery. | **Adapt:** release authenticity and compatibility checks. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Python is missing or older than 3.11. | Stop setup and readiness; no automatic Python download or installation. | The operator installs suitable Python, then setup verifies it again. |
| Provided Python or prepared environment changed or disappeared. | Stop using its previously recorded identity. | Recheck provided Python and repair the environment through setup; never silently substitute an interpreter. |
| Required evaluator differs from the plugin's wheel or installed version. | Normal governed operations refuse that pairing. | Install a compatible plugin and prepare its environment, or authorize an explicit repository upgrade. |
| Compatible wheel is missing or damaged. | Offline environment preparation stops; it does not fetch a substitute evaluator. | Restore the verified plugin package through the host's installation route. |
| Managed content conflicts or ownership is unclear. | Installer refuses unsafe application. | Owner resolves the specific conflict; preview again. |
| Apply or host registration fails. | Report actual restored and remaining state. | Inspect before retry; do not assume all layers rolled back. |

### 5. Example result

> A compatible plugin was reinstalled, then setup rebuilt its environment from the operator-provided Python and the bundled wheel. Readiness passed; the repository's selected evaluator version is unchanged.
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

Ship one exact published pure-Python evaluator wheel per plugin release in `packages/`, including package metadata and templates. Setup first checks the operator- or host-provided Python, then automatically performs authorized environment preparation outside the repository:

```text
PROVIDED_PYTHON -I --version
PROVIDED_PYTHON -I -m venv ENV_DIR
ENV_PYTHON -I -m pip install --no-index --no-deps ABS_WHEEL
```

All paths are absolute and verified. `PROVIDED_PYTHON` must be Python 3.11 or later. `ENV_DIR` is the selected environment location in persistent plugin data; `ENV_PYTHON` is its interpreter, and `ABS_WHEEL` is the trusted wheel inside the plugin. Setup verifies installation identity before using that environment. It never installs Python, activates a user shell environment, or installs into global Python.

For repair, `ENV_DIR` must be a fresh empty replacement directory. Reusing a damaged environment can leave already-installed files unchanged. Preserve a usable old environment; switch interpreter and hook references only after the replacement passes identity checks.

Normal evaluator calls require a repository-version match. The existing authorized `upgrade` path may use the selected target evaluator after its environment is prepared; it does not bypass identity or installer checks. A plugin reinstall alone does not repair or create the environment. Report any partial repair truthfully.

Preserve governance and evidence during plugin removal or rollback. Remove duplicate skills or optional Codex agent registrations only through supported ownership-aware migration, never by deleting hash-locked files manually.

**Inputs, outputs, and writes**

- **Inputs:** Verified provided Python, current/target evaluator identities, exact plugin wheel, lock, ownership information, reviewed changes, and applicable authority.
- **Outputs:** Per-layer results and fresh readiness checks.
- **Writes:** Selected plugin/host changes and prepared environment in persistent plugin data; managed files and lock only for authorized repository upgrades. Optional `--evidence-output` retains installer evidence. This repository requires it when changing the governing evaluator; see [Advancing the root evaluator](../developing-se-harness.md#advancing-the-root-evaluator). No separate evaluator-upgrade approval packet is introduced.

**Host differences**

Use Codex **Plugins** / `/plugins` or Claude Code `/plugin` for package changes. Resolve current plugin paths after updates and verify the environment interpreter before running the Python hook scripts. Both hosts depend on operator- or host-provided Python. Claude Code's persistent plugin data survives updates but is normally removed on final uninstall; durable governance stays in the repository. [Plugin data](https://code.claude.com/docs/en/plugins-reference#persistent-data-directory).

**Checks that demonstrate the behavior**

Test missing/old Python refusal without downloading Python, supplied-Python changes, offline environment creation, and a plugin reinstall that still needs environment repair. Also test explicit repository upgrade, wrong-version refusal, owner-content conflicts, and interrupted repair. Reuse applicable authority without duplicate prompts; unrelated repair authority never permits a governing-version change. Preserve truthful installation and historical evidence.

**Open questions**

Publish a clear plugin/evaluator compatibility table and prove supported rollback. Projects needing different governing versions may need different compatible plugin installations; multi-version management is deferred.

</details>
