# Define and authorize a change

<!-- Target expertise: 3.5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

Scenarios 5–8 in the [scenario index](README.md), using the [scenario template](../plugin-scenario-template.md).

**Review date:** 2026-09-08. **Inspected baseline:** [aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055](https://github.com/mmzen/se_harness/tree/aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055), candidate source **0.16.0**. The installed governing evaluator is **0.15.0**. These interfaces were inspected, not integration-tested against that release. **New** means proposed work.

`harnessctl` below means the plugin's exact `scripts/harnessctl` path (`scripts/harnessctl.exe` on Windows), with its bundled runtime. It never means a command found on `PATH`. See the [shared calling convention](README.md#shared-component-names-and-calling-convention). Skills call the existing CLI directly; there is no separate launcher or bridge API.

## Scenario 5: Inspect the project and identify the next action

### 1. Purpose and starting point

**Purpose:** Explain the project's state and the next action for selected work.

- **Starts when:** The user asks for status or selects an artifact.
- **Requires:** The repository and its matching evaluator; a clear artifact selection for a scoped question.
- **Successful result:** A read-only explanation of state, blockers, and the evaluator's next action.

### 2. Workflow

```text
User → existing harness-orient skill
     → verify evaluator and installation
     → existing orient.py → validate / inspect / selected check
     → main agent explains the result
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → existing `harness-orient` skill | Ask “Use harness-orient for WO-DEMO-101.” Claude Code exposes `/verity-plane:harness-orient WO-DEMO-101` through **New** plugin packaging. |
| 2 | Main agent → existing shell tool | Follow the skill's identity and integrity checks using the bundled evaluator. Read the existing `skill-contract.json`; stop if the installation or selection is unsuitable. |
| 3 | Main agent → existing `orient.py` | Supply the verified external interpreter, expected version/root, repository, and selected artifact. The helper runs `validate`, `inspect`, and the supported selected `check`. |
| 4 | Main agent | Explain the returned state, blockers, and next action. Run optional `preflight` only when the user explicitly selected a WO and phase. |

Inspection does not authorize the next action. The existing `harness-operator-brief` skill runs only when explicitly requested, using a bounded supplied result.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `harness-orient` guides the complete procedure. | **Adapt:** package the existing read-only skill. |
| **Hook** | No status-specific hook is needed. | **Not used:** session preparation is scenario 3. |
| **Script** | `harness-orient/scripts/orient.py` collects observations. | **Reuse:** pass the bundled evaluator's verified interpreter and identity. |
| **Tool/interface** | Codex `exec_command` or Claude Code `Bash` invokes commands. | **Reuse:** existing shell tools. |
| **Evaluator** | Identity, installation, graph, and selected scope checks. | **Reuse:** existing `identity`, `doctor`, `validate`, `inspect`, and `check`. |
| **Subagent** | No delegation. | **Not used:** the current skill requires one agent to complete the procedure. |
| **Human** | Select the intended work when ambiguous. | **Reuse:** no lifecycle approval for inspection. |
| **External control** | No external effect. | **Not used:** inspection writes nothing. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Evaluator or installation check fails. | Stop before running the managed helper; do not repair automatically. | Complete scenario 16, then inspect again. |
| Selection is ambiguous. | Leave state unchanged. | The user identifies the intended artifact. |
| Output is invalid or observed state changes. | Report no reliable result. | Obtain a fresh observation after resolving the problem. |

### 5. Example result

Illustrative response:

> WO-DEMO-101 is approved. Its next action is the start procedure, with the required checks and decision. Inspection changed no files or lifecycle state.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

- The [orient skill](../../../.agents/skills/harness-orient/SKILL.md) and [helper](../../../.agents/skills/harness-orient/scripts/orient.py) define the read-only procedure.
- Example: `harnessctl check . --artifact WO-DEMO-101 --json`. Without a checkpoint, `check` projects scope and evaluates no gate. `preflight` is also read-only.

**Proposed additions**

- Package the existing skill and helper. Supply `target`, `--evaluator-launcher-json`, `--expected-evaluator-version`, and `--expected-evaluator-root` from verified plugin paths and release metadata. This existing argument name does not require a new launcher command.
- The argument array contains the absolute bundled interpreter followed by `-I -m se_harness`. Add `--artifact` and `--preflight-phase` only when selected; preserve the helper's checks and receipt.

**Inputs, outputs, and writes**

- **Inputs:** Repository, optional selected artifact/phase, and trusted evaluator identity.
- **Outputs:** Structured observations and an explanation. **Writes:** None to the repository, runtime, or lifecycle records.

**Host differences**

- Codex uses `exec_command`; Claude Code uses its shell tool. Both run the same helper with platform-correct absolute paths.
- If explicitly requested, package `harness-operator-brief` with its existing `scripts/check_brief.py`; it does not become an automatic follow-up.

**Checks that demonstrate the behavior**

- Inspect an existing WO without writes. Reject the wrong evaluator identity before helper execution. Repeat successfully after restoring the matching installation.

**Open questions**

- Which released evaluators support the helper's optional outputs? Verify that compatibility before shipping the plugin.

</details>

## Scenario 6: Create an artifact package

### 1. Purpose and starting point

**Purpose:** Prepare related artifacts for review.

- **Starts when:** The user asks to define a change and its work.
- **Requires:** Clear authoring scope, applicable authorization, and installed authoring rules.
- **Successful result:** Validated proposals with pending decisions identified. A package is a group of artifacts, not a new artifact type.

### 2. Workflow

```text
User → change skill [New]
     → read definitions and templates
     → harnessctl scaffold-domain / create-artifact
     → agent fills drafts → harnessctl validate
     → present the review set
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → `change` skill **New** | Ask the skill to draft the package, or use `/verity-plane:change` in Claude Code. The main agent reads installed `ARTIFACT_AUTHORING.md`. |
| 2 | Main agent | Identify existing artifacts to reuse, necessary additions, links, and authorized paths. Optional `investigator` **New** finds relevant IDs and sources without editing. |
| 3 | Main agent → `harnessctl` | Preview `scaffold-domain --dry-run --json` only if a domain is needed. Preview `create-artifact --dry-run --json` for each addition. Show proposed paths and IDs. |
| 4 | Main agent → `harnessctl` | Within authorized scope, repeat the selected commands without `--dry-run`. Record actual created IDs and paths after each call. |
| 5 | Main agent → editing tool | Fill content, owners, relationships, acceptance criteria, and WO scope. The proposed `scripts/check-tool-action` checks supported mapped write events; it does not grant authoring authority. |
| 6 | Main agent → `harnessctl validate . --json` | Correct draft findings within scope, then present the artifacts and pending approvals. |

Ordinary definitions start `draft`; decisions start `open`. Neither authorizes implementation. Drafting a WO cannot require starting that same WO first; follow the repository's authoring rules.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/change/SKILL.md` guides authoring. | **New:** instructions using current rules and templates. |
| **Hook** | `PreToolUse` checks supported write events. | **Adapt:** host event calls **New** `scripts/check-tool-action`; coverage must be demonstrated. |
| **Script** | `scripts/harnessctl` runs the existing CLI. | **New:** bundled entry point; no package transaction engine. |
| **Tool/interface** | Shell and editing tools create and complete drafts. | **Reuse:** Codex `exec_command` / `apply_patch`; Claude Code `Bash` / `Read` / `Edit` / `Write`. |
| **Evaluator** | `scaffold-domain`, `create-artifact`, and `validate`. | **Reuse:** existing authoring commands. |
| **Subagent** | Optional `investigator` locates reusable definitions. | **New:** read-only helper; the main agent authors the package. |
| **Human** | Clarify meaning and authorize required scope. | **Reuse:** approval follows in scenario 7. |
| **External control** | No external effect at local drafting. | **Not used:** integration is a later boundary. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Meaning or authoring scope is unclear. | Pause the affected content. | The responsible owner clarifies it. |
| Creation fails partway or an ID collides. | Report the files actually created; no package rollback is promised. | Reconcile IDs and continue from existing drafts. |
| Validation fails. | The package remains a proposal. | Correct the drafts and validate again. |

### 5. Example result

Illustrative response:

> The package reuses INT-DEMO-001 and adds REQ-DEMO-101, SPEC-DEMO-101, VER-DEMO-101, and WO-DEMO-101. Validation passed. The new artifacts remain drafts; their owners can now review them.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

- [artifact_layout.py](../../../se_harness/artifact_layout.py) creates individual drafts; [ARTIFACT_AUTHORING.md](../../engineering/ARTIFACT_AUTHORING.md) defines their content.
- Existing previews: `harnessctl scaffold-domain . --domain example-change --dry-run --json` and `harnessctl create-artifact . --domain example-change --type requirement --id REQ-DEMO-101 --dry-run --json`.
- There is no atomic package command or authoring-scope parameter. Automatic IDs inspect local refs and the worktree, not remote-tracking refs; previewed IDs are not reservations.

**Proposed additions**

- Add the `change` skill and bundle the existing CLI. Keep creation, content editing, and validation as explicit steps.
- Optionally package `agents/investigator.md` for Claude Code and a separate `.codex/agents/investigator.toml` registration for Codex. Both are new and read-only.

**Inputs, outputs, and writes**

- **Inputs:** Desired outcome, authorized paths, current graph, domain, types, and IDs.
- **Outputs:** Created paths, findings, and review set. **Writes:** Individual authorized drafts and domain scaffolding; no approvals.

**Host differences**

- Both hosts call the same bundled CLI. File editing and optional subagent registration use their native interfaces; see the [calling convention](README.md#shared-component-names-and-calling-convention).

**Checks that demonstrate the behavior**

- Reuse existing definitions. Create only needed additions. Interrupt after two creations and resume without duplicate artifacts. Reject damaged installations before managed authoring.

**Open questions**

- Which write tools can the adapter reliably map to authoring scope? Arbitrary shell writes and incomplete drafts require specific handling; installing a hook does not prove complete enforcement.

</details>

## Scenario 7: Review and approve the package

### 1. Purpose and starting point

**Purpose:** Let each responsible owner decide the exact artifacts being approved.

- **Starts when:** A package is ready for review.
- **Requires:** Selected artifacts, current content, passing applicable gates, and identified owners.
- **Successful result:** Only the selected approvals are recorded. Approving a WO does not start it.

### 2. Workflow

```text
change skill [New] → harnessctl transition (preview)
                  → responsible owner reviews and decides
                  → harnessctl transition --apply
                  → inspect actual selected states
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Main agent following `change` **New** | Read the selected artifacts and installed `DECISION_RIGHTS.md`. Separate definition approvals from the WO approval. |
| 2 | Main agent → `harnessctl transition` | Preview selected target states without `--apply`. Present the exact content, required owners, and blockers. A valid preview is not approval. |
| 3 | Responsible human owner | Review and decide the selected content through the repository's accepted process. The agent stops at a missing decision; an existing explicit decision can be reused if it covers this exact action and content. |
| 4 | Main agent → `harnessctl` | After the required decision, confirm the content still matches the review and rerun applicable checks. Add `--apply` to record only the authorized selected transitions. |
| 5 | Main agent | Inspect actual states and report what changed. Review the WO separately once its governing chain is ready; starting it remains scenario 9. |

**Current control gap:** `--decision ID=ACTOR` records an actor name; it does not authenticate that person or bind approval to reviewed bytes. Skills require the handoff, but cannot enforce it alone. Deterministic controls are separate work tracked in [#347](https://github.com/mmzen/se_harness/issues/347); this plugin proposal does not claim that gap is solved.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `change` presents content, checks, and required decisions. | **New:** explicit human handoff before application. |
| **Hook** | `PreToolUse` checks covered transition commands. | **Adapt:** host event calls **New** `scripts/check-tool-action`; it cannot authenticate an owner. |
| **Script** | `scripts/harnessctl` runs preview and application. | **New:** packaging of the existing CLI; no review service. |
| **Tool/interface** | Shell tool invokes the CLI; human uses the accepted review process. | **Reuse:** host tools and repository review process. |
| **Evaluator** | `transition` plans and applies selected changes. | **Reuse:** existing lifecycle checks, including multi-artifact planning. |
| **Subagent** | No helper is needed for the decision. | **Not used:** an agent cannot supply an owner's approval. |
| **Human** | Make each artifact-specific decision. | **Reuse:** owners assigned by `DECISION_RIGHTS.md`. |
| **External control** | Authenticate authority at protected acceptance boundaries. | **New:** separate deterministic-control work in #347; not provided by this plugin. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| A required owner has not decided. | The agent leaves the selected transition unapplied. | Obtain the missing decision through the accepted process. |
| Reviewed content changes. | The previous decision cannot authorize the changed content by assumption. | Present the changes and refresh affected decisions. |
| A gate fails or a blocking decision stays open. | The evaluator refuses the transition. | Resolve the reported blocker, then preview again. |
| Application is interrupted. | Treat the result as unknown until inspected. | Read actual states before retrying. |

The first two stops are required behavior, not a claim that today's CLI prevents every bypass.

### 5. Example result

Illustrative response:

> REQ-DEMO-101, SPEC-DEMO-101, and VER-DEMO-101 were approved by their respective owners. WO-DEMO-101 remains draft for the engineering owner's review. Implementation has not started.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

- [workflow.py](../../../se_harness/workflow.py) supplies `plan_transition()` and `apply_transition()`; [DECISION_RIGHTS.md](../../engineering/DECISION_RIGHTS.md) assigns authority.
- Preview: `harnessctl transition . --set REQ-DEMO-101=approved --decision REQ-DEMO-101=product-owner --json`. Adding `--apply` requests a write; neither flag proves human approval.
- Preview and application are separate calls. Existing staged writes and in-process rollback do not provide reviewed-content binding or durable crash recovery.

**Proposed additions**

- The `change` skill presents the exact review and calls the existing transition command after the required decision. Do not add a second approval API or lifecycle engine.
- Authenticating the actor and preventing acceptance of forged or stale approvals require the separate controls in #347.

**Inputs, outputs, and writes**

- **Inputs:** Selected artifact IDs/states, current content, and actual owner decisions.
- **Outputs:** Blockers or actual transition results. **Writes:** Selected artifact states and lifecycle records only. Linked records do not change automatically.

**Host differences**

- Both hosts invoke the same CLI through their shell tool. Permission to execute a tool does not supply an artifact approval.

**Checks that demonstrate the behavior**

- Approve two selected definitions and verify only those changed. Verify the skill stops when a decision is absent. Exercise forged-actor and stale-content cases when implementing #347; skill compliance alone is insufficient proof.

**Open questions**

- Which existing identity and protected repository controls will authenticate and enforce exact approvals? Decide that boundary in #347 before describing approvals as deterministically protected.

</details>

## Scenario 8: Revise approved definitions or work scope

### 1. Purpose and starting point

**Purpose:** Change approved meaning or permitted work through an explicit owner decision.

- **Starts when:** New findings require a change outside approved meaning or scope.
- **Requires:** Affected artifacts, reason for change, and responsible owners.
- **Successful result:** Authorized amendments or new drafts, with affected work checked again.

### 2. Workflow

```text
Stop affected work → change skill [New]
                   → compare current and proposed meaning
                   → responsible owners decide
                   → supported edits / new drafts / decide command
                   → validate and check affected scope
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Main agent | Stop affected work and preserve existing records and evidence. Read installed authoring and workflow rules through the `change` skill **New**. |
| 2 | Main agent; optional `investigator` **New** | Identify affected definitions, WOs, links, and verification contracts. Present current meaning, proposed meaning, and scope consequences. The optional helper reads and reports only. |
| 3 | Responsible owners | Decide the exact amendment and revised work scope. If the rules require a DEC, the main agent first drafts it using existing `create-artifact --type decision`. |
| 4 | Main agent → existing `decide`, when applicable | Preview the declared DEC option, then apply only after the responsible owner's decision. Selecting `amend` records that answer; it leaves target artifacts unchanged. |
| 5 | Main agent → editing tools or `create-artifact` | Make separately authorized amendments under existing rules, or create new drafts. A new WO can cover additional work under unchanged definitions. |
| 6 | Main agent → `harnessctl` | Run `validate`, then the affected WO's applicable scope `check` using the actual complete changed paths. Resume affected work only through its permitted procedure. |

There is no general `approved → draft` transition or amendment transaction. The plugin follows supported authoring rules; it does not invent reopen, replacement, or automatic state changes.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `change` guides impact analysis, decisions, and amendments. | **New:** instructions using existing authoring and lifecycle rules. |
| **Hook** | `PreToolUse` checks covered write operations. | **Adapt:** host event calls **New** `scripts/check-tool-action`; it does not create amendment authority. |
| **Script** | `scripts/harnessctl` runs supported operations. | **New:** packaging of existing commands; no amendment API. |
| **Tool/interface** | Shell and editing tools apply authorized changes. | **Reuse:** Codex `exec_command` / `apply_patch`; Claude Code `Bash` / `Edit` / `Write`. |
| **Evaluator** | `create-artifact`, `decide`, `validate`, and scope `check`. | **Reuse:** current behavior; no general reopen command. |
| **Subagent** | Optional `investigator` traces affected artifacts. | **New:** read-only findings; no remediation decision. |
| **Human** | Decide changed meaning and remediation scope. | **Reuse:** affected owners and `DR-REMEDIATION-SCOPE`. |
| **External control** | Enforce authentic approvals at protected acceptance boundaries. | **New:** separate #347 work; local hooks do not supply this boundary. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Proposed work exceeds scope. | Affected work stops; the applicable scope check reports the breach. | Obtain remediation authority and choose a supported path. |
| The requested transition does not exist. | The evaluator refuses it. | Use an allowed amendment path or define new semantics through separate governed work. |
| A DEC selects “amend.” | Only the decision disposition changes. | Perform separately authorized target edits and re-evaluate. |
| Reviewed content changes before editing. | Reassess the affected decision; do not assume it still covers the change. | Present the difference and obtain any missing authority. |

### 5. Example result

Illustrative response:

> WO-DEMO-101 permits a 30-day export. A 90-day export changes SPEC-DEMO-101 and exceeds that scope. The impact proposal is ready; approved records are unchanged. The technical and engineering owners must decide the affected changes.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

- [WORKFLOW.md](../../engineering/WORKFLOW.md#state-model) declares permitted transitions. [ARTIFACT_AUTHORING.md](../../engineering/ARTIFACT_AUTHORING.md) permits amendments to approved definitions; that does not introduce a reopen edge.
- [decisions.py](../../../se_harness/decisions.py) records a declared answer without changing blocked artifacts. Preview: `harnessctl decide . --artifact DEC-DEMO-101 --option amend --decision technical-owner --reason "Extend the export period to 90 days." --json`. This example assumes that option and role exist on the DEC; `--apply` requests the write.
- After authorized edits: `harnessctl check . --artifact WO-DEMO-101 --checkpoint scope --changed-path docs/engineering/example-change/specifications/SPEC-DEMO-101.md --changes-complete --json`. Supply actual complete changed paths. Declared paths are not trusted proof of every effect.

**Proposed additions**

- Add the amendment procedure to `change`. Use existing authoring commands and editing tools. New replacement rules or automatic invalidation of approvals require separate governed design, not plugin-specific shortcuts.

**Inputs, outputs, and writes**

- **Inputs:** Current records, proposed changes, affected work/evidence, and owner decisions.
- **Outputs:** Amended content or new drafts, check results, or a specific unsupported operation.
- **Writes:** None during analysis. Authorized edits and selected DEC dispositions are separate writes. Preserve historical VREC/RLS facts; infer no linked lifecycle changes.

**Host differences**

- The hosts use their native shell and editing tools with the same CLI and rules. Optional investigator registration follows scenario 6.

**Checks that demonstrate the behavior**

- Prepare a new WO under unchanged definitions without enlarging the original WO. Refuse an unsupported reopen transition. Confirm that deciding `amend` leaves its target unchanged.

**Open questions**

- Which changes require new IDs or renewed approvals? Any missing amendment semantics need a governed definition before automation. The actor-authentication gap remains the separate #347 work.

</details>
