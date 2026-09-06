# Plugin scenarios: release and maintenance

<!-- Target expertise: 3.5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

[All scenarios](README.md) · [Workflow overview](../plugin-operation-workflows-2026-09-06.md) · [Scenario template](../plugin-scenario-template.md)

Design proposal, reviewed 2026-09-06. Current implementation means source at [`aad82a9`](https://github.com/mmzen/se_harness/tree/aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055): candidate source 0.16.0, with a repository governed by released 0.15.0. These identities are different. Interfaces below were inspected; the plugin integration has not been implemented or exercised against the released evaluator.

The proposed bridge calls the selected external evaluator with structured arguments. Skills explain its results; they do not supply decision authority. Examples are illustrative. `REPO` means the selected repository; `*-DEMO-*` identifiers and version `1.2.0` describe a fictional consumer project.

## Scenario 14: Prepare and approve a release

### 1. Purpose and starting point

**Purpose:** Give the release owner an exact candidate and its evidence to decide on.

- **Starts when:** The release owner selects release preparation for identified work.
- **Requires:** An approved release contract, eligible work orders, verified coverage for one candidate commit, and the applicable preparation checks.
- **Successful result:** One release record, called an RLS, records the owner's decision. Publication remains a separate operation.

### 2. Workflow

```text
Select exact release inputs
        ↓
Owner authorizes preparation → Evaluator prepares a ready RLS
        ↓
Check release evidence → Owner decides → Record that decision
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Evidence skill and agent | Present the contract, work, verification records, version, and candidate to the release owner. |
| 2 | Release owner | Authorize preparation with those exact inputs. |
| 3 | Bridge and evaluator | Check prerequisites and create the ready RLS with its retained evaluator evidence. |
| 4 | Project release scripts | Produce any additional release evidence required by the contract through the separately authorized project process. |
| 5 | Release owner and bridge | Review the evidence, preview the selected transition, and apply the exact release or rejection decision after rechecking its inputs. |

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | Explain preparation and the decision handoff. | **New:** evidence skill wraps the current release procedure. |
| **Hook** | Check covered record-changing calls. | **New:** host adapter; it cannot approve a release. |
| **Script** | Pass exact inputs and retain returned results. | **Adapt:** existing project release scripts; **New:** bridge. |
| **Tool/interface** | Request preparation or an explicit transition. | **Adapt:** expose existing CLI operations through structured calls. |
| **Evaluator** | Validate coverage, prepare the record, and evaluate transitions. | **Reuse:** `prepare-release`, `check`, and `transition`. |
| **Subagent** | Optional read-only review of release evidence. | **New:** bounded reviewer role; no decision or writes. |
| **Human** | Authorize preparation, then decide the RLS. | **Reuse:** release owner; **New:** trustworthy capture of the exact decisions. |
| **External control** | Protect any separately selected build or remote action. | **Reuse:** project controls where present; publication belongs to scenario 15. |

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

A release-input view and decision interface bound to the reviewed record. The bridge delegates legality to the evaluator. Consumer-specific build and distribution binding remain in project scripts. This repository's example is documented in [Release sequences](../developing-se-harness.md#release-sequences).

**Inputs, outputs, and writes**

- **Inputs:** Exact contract, verification records, work orders, version, preparation authority, and later release decision.
- **Outputs:** Ready RLS, retained evidence, then the observed decision result.
- **Writes:** New RLS and evaluator evidence; later selected lifecycle fields. No tag, upload, deployment, or inferred changes to included records.

**Host differences**

- **Codex:** The proposed evidence skill uses the bridge; host permission prompts are separate from release decisions.
- **Claude Code:** The same evaluator operations apply through its adapter. Its permissions also do not prove a release decision. See the [host comparison](../plugin-installation-proposal-2026-09-06.md#native-capabilities-and-their-limits).

**Checks that demonstrate the behavior**

- **Success:** Authorized exact inputs produce one ready record; a later release decision changes only that record.
- **Refusal:** Missing coverage, duplicate version, or missing owner decision prevents the corresponding operation.
- **Recovery:** After interruption, inspect whether the RLS exists before retrying. Preserve rejected and historical records.

**Open questions**

How will the new decision interface bind the owner's identity to the exact reviewed record and reject changed inputs? Prove this before enabling automated application.

</details>

## Scenario 15: Publish or deploy the release

### 1. Purpose and starting point

**Purpose:** Deliver the approved release through the project's protected publication process.

- **Starts when:** The accountable owner requests a specific publication or deployment.
- **Requires:** The selected released RLS, exact destination and candidate, applicable evidence, and authority for that external action.
- **Successful result:** The requested effect is observed at its destination, with a truthful report of completed and pending steps.

### 2. Workflow

```text
Select released record and destination
        ↓
Owner authorizes the external action
        ↓
Protected service checks authority → Project workflow publishes
        ↓
Observe the destination and report the result
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Evidence skill | Present the record, exact effect, destination, and required publication process. |
| 2 | External-action owner | Authorize that action. Release status alone does not provide this decision. |
| 3 | Protected service | Verify the target, trusted authority, and required evidence before permitting the effect. |
| 4 | Project publication workflow | Publish or deploy the bound deliverables and retain its results. |
| 5 | Agent using read-only tools | Check destination state and report any remaining owner action. |

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | Guide the publication handoff and explain results. | **New:** evidence skill routes to the project's process. |
| **Hook** | Check covered local dispatch calls. | **New:** useful local intervention; remote protection remains necessary. |
| **Script** | Build the exact dispatch request and read results. | **Adapt:** project scripts; **New:** bounded dispatch adapter. |
| **Tool/interface** | Invoke the named workflow and inspect its result. | **Reuse:** host or provider API; **Adapt:** explicit target presentation. |
| **Evaluator** | Check the RLS and applicable external-action prerequisites. | **Reuse:** selected `check` and existing release contracts. |
| **Subagent** | Not used. | **Not used:** publication credentials stay outside reviewer roles. |
| **Human** | Decide the specific external action. | **Reuse:** accountable external-action owner and applicable environment decisions. |
| **External control** | Enforce authority where credentials and effects reside. | **Adapt:** project protection; **New:** any missing approval binding or bypass prevention. |

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

A per-project dispatch mapping, trustworthy approval capture, and enforcement at each protected effect. Reuse the project's release process rather than giving the plugin a universal publishing credential. See [incident #347](https://github.com/mmzen/se_harness/issues/347) for the related authorization gap. The adapter reports raw workflow outcomes without treating a successful dispatch as successful publication.

**Inputs, outputs, and writes**

- **Inputs:** Released RLS, destination, approved action, immutable deliverable identities, and workflow reference.
- **Outputs:** Run identifier, per-destination results, observed identities, and remaining decisions.
- **Writes:** Only authorized external effects and their retained evidence. This repository also has separately controlled latest markers described in [Release sequences](../developing-se-harness.md#release-sequences).

**Host differences**

- **Codex:** A local hook can cover supported tool calls; it does not protect calls made elsewhere.
- **Claude Code:** Its hook adapter differs, but the remote publication boundary is the same. The [proposal](../plugin-installation-proposal-2026-09-06.md#hooks-useful-intervention-incomplete-enforcement) explains that distinction.

**Checks that demonstrate the behavior**

- **Success:** Approved immutable inputs produce the expected destination objects and verifiable results.
- **Refusal:** Missing authority or wrong digests are denied even with local hooks disabled.
- **Recovery:** A timed-out dispatch is reconciled against its existing run before any retry. Partial publication never triggers an automatic destructive undo.

**Open questions**

Which service proves external-action authority for each destination, and which credentials or administrator routes could bypass it? Verify those routes before claiming enforcement.

</details>

## Scenario 16: Upgrade or repair the installation

### 1. Purpose and starting point

**Purpose:** Restore or update the plugin without silently changing a project's governing version.

- **Starts when:** A user requests an upgrade, or diagnostics identify a missing or incompatible installation component.
- **Requires:** The selected host, repository lock, current and target component identities, trusted distribution metadata, and authority for the proposed changes.
- **Successful result:** The selected components work together, owner content remains intact, and the report identifies every version or file change.

### 2. Workflow

```text
Diagnose which layer needs a change
        ↓
Plan plugin / runtime / repository effects separately
        ↓
Review authority → Apply the selected change → Check the result
        ↓
Resume work, or report the remaining repair
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Orient skill and launcher | Inspect host registration, cached runtime identity, and repository health. |
| 2 | Setup skill | Explain whether the repair affects the plugin, runtime cache, or managed repository content. |
| 3 | Owner and bridge | Review exact effects and resolve missing authorization. A changed plan requires review again. |
| 4 | Host manager, runtime manager, or installer | Apply only the selected operation through its owning component. |
| 5 | Launcher and evaluator | Check resulting identities and installation health. Report partial setup instead of resuming governed work prematurely. |

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | Diagnose and present a bounded repair plan. | **Adapt:** orient skill; **New:** setup skill. |
| **Hook** | Detect missing readiness at a session boundary. | **New:** session adapter invokes diagnostics; it does not perform upgrades. |
| **Script** | Resolve runtimes and coordinate selected maintenance. | **New:** runtime manager and bridge. |
| **Tool/interface** | Expose diagnostics, planning, and authorized apply. | **Adapt:** host manager and existing CLI interfaces. |
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

Trusted runtime repair, a tested compatibility matrix, and plan binding between review and apply. Separate dry-run/apply invocations do not currently bind the reviewed plan. Plugin rollback selects a compatible build; repository downgrade is not an assumed repair method. Remove duplicate skill registration only through an ownership-aware migration. Preserve governance and evidence on disconnect or plugin removal.

**Inputs, outputs, and writes**

- **Inputs:** Exact current/target identities, lock, ownership information, repair plan, and relevant authorization.
- **Outputs:** Per-layer result and fresh health checks.
- **Writes:** Selected host registration/cache changes; managed files and lock only for authorized repository changes. Optional `--evidence-output` retains installer evidence. This repository requires that evidence for a governor transition; see [Advancing the root evaluator](../developing-se-harness.md#advancing-the-root-evaluator). No separate evaluator-upgrade approval packet is reintroduced.

**Host differences**

- **Codex:** Use its plugin management surface and persistent plugin data; account for project agent registrations created by setup.
- **Claude Code:** Use its plugin management surface and persistent plugin data. Do not rely on a stable plugin cache path. Consult the documented [host differences](../plugin-installation-proposal-2026-09-06.md#native-capabilities-and-their-limits) and [migration plan](../plugin-installation-proposal-2026-09-06.md#distribution-updates-and-migration).

**Checks that demonstrate the behavior**

- **Success:** Updating the plugin or repairing its runtime leaves repository policy unchanged; an authorized repository upgrade changes only its reviewed owned content.
- **Refusal:** Wrong identity, owner-content conflict, or incompatible versions prevent the selected operation.
- **Recovery:** Interrupt each layer independently; preserve owner bytes and historical evidence, then demonstrate retry or compatible plugin rollback.

**Open questions**

Which host versions and evaluator releases will the first plugin support? Demonstrate plan binding, crash recovery, and ownership-aware registration cleanup for that matrix.

</details>
