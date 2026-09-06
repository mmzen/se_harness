# Define and authorize a change

<!-- Target expertise: 3.5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

Scenarios 5–8 in the [scenario index](README.md), using the [scenario template](../plugin-scenario-template.md). See the [operation workflows](../plugin-operation-workflows-2026-09-06.md) for the overall component model.

**Review date:** 2026-09-06. **Implementation baseline:** [`aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055`](https://github.com/mmzen/se_harness/tree/aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055), candidate source **0.16.0**. The repository's installed governing version is **0.15.0**. Source interfaces below were inspected; they were not integration-tested against that released evaluator. The plugin components are proposals. This note grants no authoring, approval, or execution authority.

## Scenario 5: Inspect the project and identify the next action

### 1. Purpose and starting point

**Purpose:** Explain where the project stands and what the selected work needs next.

- **Starts when:** The user asks for status or selects an existing work order, verification record, release record, or decision.
- **Requires:** An unambiguous repository and its trusted external evaluator; a selected artifact when the question concerns specific work.
- **Successful result:** A read-only explanation of current state, relevant blockers, and the evaluator's next action.

### 2. Workflow

```text
User asks for status
        ↓
Verify evaluator and installation
        ↓
Inspect the graph and selected work
        ↓
Explain the result and next action
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Status skill | Establish the repository and selection. Ask for an exact selection if the request is ambiguous. |
| 2 | Launcher and orient helper | Check evaluator identity and installation integrity before trusting repository helpers. |
| 3 | Evaluator | Inspect the graph and project the selected scope. Run preflight only for an explicitly selected work order and requested phase. |
| 4 | Agent | Explain the returned result. Keep unrelated observations separate from blockers for the selected work. |

Reading and analysis do not require a started work order. A status request does not authorize the next lifecycle action it reveals.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | Guide read-only orientation. | **Adapt:** package `harness-orient` with plugin discovery and runtime resolution. |
| **Hook** | None; the user invokes status. | **Not used:** session preparation is a separate scenario. |
| **Script** | Collect and structure observations. | **Adapt:** retain `orient.py` checks; pass the plugin's verified launcher. |
| **Tool/interface** | Expose status in the host. | **New:** a thin interface to the orient helper. |
| **Evaluator** | Supply facts and the next action. | **Reuse:** `doctor`, `validate`, `inspect`, and selected `check`. |
| **Subagent** | None. | **Not used:** today's orient contract requires one agent. |
| **Human** | Clarify the selection when needed. | **Reuse:** inspection requires no lifecycle decision. |
| **External control** | None; no protected external effect occurs. | **Not used:** this operation writes nothing. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Runtime or integrity check fails. | The helper stops; it does not install or repair anything. | Complete the separate repair scenario, then repeat status. |
| Selection is ambiguous. | The agent reports the ambiguity and leaves state unchanged. | The user selects the intended artifact. |
| Required output is malformed or state changes during inspection. | Orientation stops without claiming a reliable result. | Correct the underlying problem and obtain a fresh observation. |

### 5. Example result

Illustrative response:

> WO-DEMO-101 is approved. Its next step is the start procedure, including its required checks and decision.
> Inspection changed no files or lifecycle state.
> Next: run the evaluator's start procedure for WO-DEMO-101.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

- The [orient contract](../../../.agents/skills/harness-orient/SKILL.md) and [helper](../../../.agents/skills/harness-orient/scripts/orient.py) define identity checks, supported outputs, and the read-only boundary.
- Example: `harnessctl check . --artifact WO-DEMO-101 --json`. Without a checkpoint, `check` projects scope and evaluates no gate.
- Baseline and inspection status are recorded above. `harnessctl` means the verified external invocation, not an executable found in the checkout or on `PATH`.

**Proposed additions**

- Connect plugin discovery and runtime resolution to the existing helper. Display its result without calculating another next action.

**Inputs, outputs, and writes**

- **Inputs:** Repository, expected evaluator identity, optional artifact and requested phase.
- **Outputs:** Structured orientation and an explanation for the user.
- **Writes:** None, including no saved receipt in the repository.

**Host differences**

- **Codex:** Package the existing portable skill; verify invocation in the supported host version.
- **Claude Code:** Adapt the current wrapper to locate the plugin's core instead of a fixed repository-local copy. See the [host comparison](../plugin-installation-proposal-2026-09-06.md#native-capabilities-and-their-limits).

**Checks that demonstrate the behavior**

- **Success:** Select one existing WO → report its actual state and next action with no writes.
- **Refusal:** Wrong evaluator identity → no repository helper runs.
- **Recovery:** Restore the matching evaluator → repeat orientation successfully.

**Open questions**

- Which released evaluators support each optional output? Verify the compatibility matrix before promising uniform status features.

</details>

## Scenario 6: Create an artifact package

### 1. Purpose and starting point

**Purpose:** Turn a requested change into a connected set of artifacts ready for review.

- **Starts when:** The user requests preparation of the change's definitions and work order.
- **Requires:** Clear authoring scope, applicable repository authorization, and the installed authoring rules.
- **Successful result:** Validated proposals with pending decisions identified. A package means related artifacts, not a new artifact type.

### 2. Workflow

```text
Requested outcome
        ↓
Find reusable definitions and plan additions
        ↓
Create and complete individual artifacts
        ↓
Validate the package and present it for review
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Change skill and agent | Read existing definitions and authoring rules. Select necessary additions. |
| 2 | Optional investigator | Find related definitions and report reuse candidates without editing or deciding. |
| 3 | Bridge and evaluator | Scaffold a domain if needed. Create artifacts and return their paths and IDs. |
| 4 | Agent | Complete content, relationships, owners, acceptance criteria, and work scope. |
| 5 | Evaluator and agent | Validate the proposed graph and present remaining issues and decisions. |

Authoring follows repository policy. It cannot require a started implementation WO merely to draft that same WO. Ordinary definitions begin `draft`; decision artifacts begin `open`. Neither means approved.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | Guide reuse, drafting, and review preparation. | **New:** a change skill loading existing authoring rules. |
| **Hook** | Check covered authoring actions. | **New:** map permitted authoring scope; do not demand a valid graph after every edit. |
| **Script** | Call authoring operations and report progress. | **New:** bridge over existing commands. |
| **Tool/interface** | Create drafts and edit their content. | **Adapt:** structured harness calls plus ordinary host editing tools. |
| **Evaluator** | Scaffold, allocate IDs, and validate. | **Reuse:** `scaffold-domain`, `create-artifact`, and `validate`. |
| **Subagent** | Investigate a bounded question. | **New:** optional read-only investigator; findings remain observations. |
| **Human** | Clarify meaning and authorize required scope. | **Reuse:** existing authority; approval follows in scenario 7. |
| **External control** | None at local draft creation. | **Not used:** later integration has its own boundary. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Meaning or authoring authority is unclear. | Drafting the affected content waits. | The accountable owner clarifies that specific point or scope. |
| An ID collides or creation fails partway. | The bridge reports the files actually created; it claims no package rollback. | Reconcile IDs and resume from existing drafts. |
| The package has validation errors. | It remains a proposal; approval is blocked by applicable gates. | Correct drafts and validate again. |

### 5. Example result

Illustrative response:

> The package reuses INT-DEMO-001 and adds REQ-DEMO-101, SPEC-DEMO-101, VER-DEMO-101, and WO-DEMO-101.
> Graph validation passed. The four new artifacts remain drafts; implementation has not started.
> Next: present the selected definitions to their accountable owners for review.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

- [artifact_layout.py](../../../se_harness/artifact_layout.py) creates one incomplete draft per call. [ARTIFACT_AUTHORING.md](../../engineering/ARTIFACT_AUTHORING.md) supplies content rules.
- Example preview: `harnessctl create-artifact . --domain example-change --type requirement --id REQ-DEMO-101 --dry-run --json`.
- Baseline and inspection status are recorded above. There is no atomic package command or authoring-scope parameter. Automatic IDs examine local refs and the worktree, not remote-tracking refs; dry-run IDs are not reservations.

**Proposed additions**

- Add package planning and recoverable progress reporting. Define authoring-scope enforcement separately; the existing command cannot prove it from a WO argument.

**Inputs, outputs, and writes**

- **Inputs:** Requested outcome, authorized authoring scope, current graph, domain, artifact types, and IDs.
- **Outputs:** Created paths, validation findings, and the review set.
- **Writes:** Authorized domain scaffolding and individual artifacts. No approval or implementation state is granted.

**Host differences**

- **Codex:** Investigator setup may require registering the bundled agent definition in the documented project location.
- **Claude Code:** Use native plugin agent discovery. Test both hosts' tool limits and hook coverage; see the [host comparison](../plugin-installation-proposal-2026-09-06.md#native-capabilities-and-their-limits).

**Checks that demonstrate the behavior**

- **Success:** Existing intent plus requested change → only necessary additions, with valid links.
- **Refusal:** Damaged installation → authoring command refuses the write.
- **Recovery:** Failure after two creations → retain those drafts and resume without duplicates.

**Open questions**

- How will authoring scope include trusted owner exceptions without requiring an already-started WO?

</details>

## Scenario 7: Review and approve the package

### 1. Purpose and starting point

**Purpose:** Make each approval explicit and attributable to the responsible owner.

- **Starts when:** A completed package is ready for review.
- **Requires:** Exact artifacts, current content, applicable passing gates, and identified accountable owners.
- **Successful result:** Only selected artifacts are approved. WO approval does not start implementation.

### 2. Workflow

```text
Present artifacts and required decisions
        ↓
Each accountable owner decides
        ↓
Preview and apply the exact authorized transitions
        ↓
Report changed states and remaining decisions
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Change skill | Present the selected content, relationships, unresolved decisions, and owners. |
| 2 | Accountable owners | Approve their definitions after resolving blocking decisions through the applicable procedure. |
| 3 | Bridge and evaluator | Preview the selected transitions; apply only after the exact decisions and current checks. |
| 4 | Engineering owner | Decide the bounded WO after its governing chain and authorization gate are complete. |
| 5 | Evaluator and agent | Read resulting states and explain the remaining next action. |

The package is a review grouping, with separate artifact approvals. Product, technical, assurance, and engineering owners retain their decisions, even when one person holds several roles.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | Present selected artifacts and distinct decisions. | **New:** change skill using current decision rights. |
| **Hook** | Intervene on covered transition calls. | **New:** preserve the handoff; hooks do not authenticate owners. |
| **Script** | Pass the exact transition packet. | **New:** bridge and decision binding; retain engine checks. |
| **Tool/interface** | Show review content and receive decisions. | **New:** bind the selected content, roles, and requested states to the decision. |
| **Evaluator** | Check and apply selected transitions. | **Reuse:** multi-artifact `transition` planning and application. |
| **Subagent** | Review consistency when useful. | **New:** optional read-only reviewer; it cannot approve definitions. |
| **Human** | Make artifact-specific decisions. | **Reuse:** owners named by `DECISION_RIGHTS.md`. |
| **External control** | None in the current local transition interface. | **Not used:** authenticated decision enforcement remains a design gap; merge controls are separate. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| A required owner has not decided. | The proposed interface holds that transition. | Obtain that owner's explicit decision over the identified content. |
| Content changes after review. | The proposed binding rejects the stale decision. | Present the changed content and refresh the affected decision. |
| A gate fails or blocking decision remains open. | The evaluator refuses the transition. | Resolve the reported blocker and preview again. |

Today's actor-name argument does not prove who decided. Authenticated binding is new work.

### 5. Example result

Illustrative response:

> REQ-DEMO-101, SPEC-DEMO-101, and VER-DEMO-101 were approved by their respective owners.
> WO-DEMO-101 remains draft. No implementation was started.
> Next: the engineering owner reviews and decides WO-DEMO-101.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

- [workflow.py](../../../se_harness/workflow.py) provides `plan_transition()` and `apply_transition()`. [DECISION_RIGHTS.md](../../engineering/DECISION_RIGHTS.md) assigns owners.
- Example preview: `harnessctl transition . --set REQ-DEMO-101=approved --decision REQ-DEMO-101=product-owner --json`. `--apply` requests the write; it does not supply missing human authority.
- Baseline and inspection status are recorded above. Multi-artifact transitions use staged writes and in-process rollback, not a promise of durable crash recovery.

**Proposed additions**

- An authenticated decision interface and binding to reviewed content. Apply-time checks must reject changed inputs rather than reuse a stale approval.

**Inputs, outputs, and writes**

- **Inputs:** Explicit artifact/state selections, actual decisions, roles, reviewed content identity, and current graph.
- **Outputs:** Preview or applied result, blockers, and actual states.
- **Writes:** Selected artifact statuses and lifecycle records when application succeeds.

**Host differences**

- **Codex:** Host tool approval is distinct from an accountable lifecycle decision.
- **Claude Code:** The same distinction applies to tool permissions. Both adapters need the proposed decision binding; see the [authority analysis](../plugin-installation-proposal-2026-09-06.md#architecture-one-engine-two-adapters).

**Checks that demonstrate the behavior**

- **Success:** Approve two explicitly selected definitions → change only those two.
- **Refusal:** Owner absent or reviewed content changed → no application through the proposed interface.
- **Recovery:** Fresh decision on refreshed content → repeat preview and application.

**Open questions**

- Which trusted identity and storage boundary will authenticate decisions when local files and actor strings are writable by the agent?

</details>

## Scenario 8: Revise approved definitions or work scope

### 1. Purpose and starting point

**Purpose:** Change the intended system or permitted work without silently extending an earlier approval.

- **Starts when:** Investigation, implementation, or review reveals a necessary change outside the approved meaning or scope.
- **Requires:** Affected artifacts, reason for change, and responsible owners.
- **Successful result:** An authorized amendment or new draft, followed by re-evaluation of the affected scope; an explicit stop if the requested operation is unsupported.

### 2. Workflow

```text
Discover a needed change
        ↓
Stop the affected operation and inspect its impact
        ↓
Present revised scope to the accountable owners
        ↓
Apply an authorized amendment or create new drafts
        ↓
Recheck affected scope; stop if the requested operation is unsupported
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Agent | Stop affected work. Preserve records and evidence. |
| 2 | Investigator or main agent | Trace affected definitions, verification contracts, and WOs. Report consequences as analysis. |
| 3 | Change skill | Present the change and required decisions. Create a decision artifact when installed rules require one. |
| 4 | Accountable owners | Decide the proposed meaning and remediation scope. Related artifacts remain unchanged. |
| 5 | Agent | Amend selected content under the applicable authoring and decision rules, or create authorized new drafts. |
| 6 | Bridge and evaluator | Recheck the affected graph and work scope. Refuse unsupported lifecycle transitions. |

The plugin cannot invent an `approved → draft` transition. Existing authoring rules allow amendments to approved definitions; there is no dedicated amendment transaction. Authorized edits follow those rules and the affected owners' decisions. A new WO can cover additional work under unchanged definitions. New reopen or replacement workflows need explicit semantics.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | Explain impact and route the proposed revision. | **New:** change skill with explicit unsupported-path handling. |
| **Hook** | Intervene on covered scope-changing actions. | **New:** mapped checks; broad shell coverage is not established. |
| **Script** | Collect impact and invoke supported commands. | **New:** bridge to existing operations. |
| **Tool/interface** | Present old and proposed meaning together. | **New:** review view with selected artifacts and consequences. |
| **Evaluator** | Check scope and record decisions. | **Reuse:** scope checks, authoring, `decide`, and legal transitions; no revision transaction. |
| **Subagent** | Trace affected relationships. | **New:** optional read-only investigator with a bounded question. |
| **Human** | Decide changed meaning and remediation scope. | **Reuse:** affected owners and `DR-REMEDIATION-SCOPE`. |
| **External control** | Protect subsequent integration. | **New:** independent enforcement; local hooks are insufficient. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Proposed work exceeds approved scope. | The relevant scope check fails; affected work stops. | Obtain remediation authority and a supported path. |
| Amendment needs an undefined lifecycle edge. | The evaluator refuses the transition. | Define and approve amendment rules separately. |
| A decision selects “amend.” | The decision records the answer; its targets remain unchanged. | Perform separately authorized edits through an established procedure, then re-evaluate. |

### 5. Example result

Illustrative response:

> WO-DEMO-101 permits a 30-day export. The requested 90-day export changes SPEC-DEMO-101 and is outside that work scope.
> I prepared the impact proposal. The approved specification and WO are unchanged.
> Next: the technical owner decides the proposed specification change and its supported amendment path.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

- [WORKFLOW.md](../../engineering/WORKFLOW.md#state-model) declares permitted edges. No general reopen or revision command exists; historical `superseded` definition/WO vocabulary adds no transition. [Authoring rules](../../engineering/ARTIFACT_AUTHORING.md) nevertheless permit amendments to approved definitions.
- [decisions.py](../../../se_harness/decisions.py) records a declared answer and leaves blocked artifacts unchanged. Example preview: `harnessctl decide . --artifact DEC-DEMO-101 --option amend --decision technical-owner --reason "Extend the export period to 90 days." --json`. This assumes the illustrative decision declares that option and role.
- Baseline and inspection status are recorded above. A DEC option named `supersede` is not a lifecycle transition for its target.

**Proposed additions**

- Add a structured amendment operation that preserves existing authoring and decision rules. Define reviewed-content binding and any new replacement or approval-invalidation behavior through governed design; the plugin must not invent those semantics.

**Inputs, outputs, and writes**

- **Inputs:** Approved records, proposed changes, impact findings, and exact owner decisions.
- **Outputs:** Amended content or new drafts, re-evaluation results, or an explicit unsupported-path stop.
- **Writes:** None during impact analysis. Authorized definition amendments, new drafts, and selected decision dispositions are separate writes. Historical VREC/RLS facts remain intact; lifecycle states do not change by inference.

**Host differences**

- **Codex:** Present the same unsupported-path stop through its skill and tools.
- **Claude Code:** Follow the same engine result. Neither host supplies amendment rules; see the [shared architecture](../plugin-installation-proposal-2026-09-06.md#architecture-one-engine-two-adapters).

**Checks that demonstrate the behavior**

- **Success:** Additional work within unchanged definitions → separately authorized new WO proposal, with the original scope preserved.
- **Refusal:** Attempt an unsupported reopen transition → no lifecycle write.
- **Recovery:** Owner selects a supported bounded path → create the required drafts and return to review.

**Open questions**

- What exact transaction records amendments and invalidates affected approvals? Which changes require new artifact IDs? These rules need a separate governed design.

</details>
