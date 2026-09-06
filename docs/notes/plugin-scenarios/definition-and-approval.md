# Define and authorize a change

<!-- Target expertise: 3.5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

Scenarios 5–8 in the [scenario index](README.md), using the [scenario template](../plugin-scenario-template.md). See the [operation workflows](../plugin-operation-workflows-2026-09-06.md) for the overall component model.

**Review date:** 2026-09-06. **Implementation baseline:** [`aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055`](https://github.com/mmzen/se_harness/tree/aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055), candidate source **0.16.0**. The repository's installed governing version is **0.15.0**. Source interfaces below were inspected; they were not integration-tested against that released evaluator. The plugin components are proposals. This note grants no authoring, approval, or execution authority.

**[New]** marks a component or operation to build. The proposed `bin/launcher bridge --request REQUEST_FILE --json` command runs the plugin's `scripts/bridge` with the verified external evaluator. The JSON request names an operation, an absolute `repo` path, and that operation's inputs. It contains no shell command string. Request files stay outside the target repository. `harnessctl` examples below show the existing evaluator arguments that the bridge would invoke.

Use the [shared calling convention](README.md#shared-component-names-and-calling-convention) for launcher calls and optional subagent delegation.

## Scenario 5: Inspect the project and identify the next action

### 1. Purpose and starting point

**Purpose:** Explain where the project stands and what the selected work needs next.

- **Starts when:** The user asks for status or selects an existing work order, verification record, release record, or decision.
- **Requires:** An unambiguous repository and its trusted external evaluator; a selected artifact when the question concerns specific work.
- **Successful result:** A read-only explanation of current state, relevant blockers, and the evaluator's next action.

### 2. Workflow

```text
User invokes existing harness-orient
        ↓
Agent → bin/launcher bridge [New], operation orient [New]
        ↓
Existing --version, identity, doctor → trusted orient.py
        ↓
Existing validate, inspect, selected check → inline result
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → existing `harness-orient` skill | **Codex:** ask “Use harness-orient for WO-DEMO-101 in this repository.” **Claude Code:** `/verity-plane:harness-orient WO-DEMO-101` **[New packaging]**. The main agent reads the skill and its `skill-contract.json`; resolve an ambiguous selection before proceeding. |
| 2 | Agent → existing shell tool | Use Codex `exec_command`, or Claude Code `Bash` / `PowerShell`, to call `bin/launcher bridge --request REQUEST_FILE --json` **[New]** with operation `orient`, repository, and optional artifact/phase. |
| 3 | `bin/launcher` and `scripts/bridge` **[New]** | Resolve the exact external evaluator. Run existing `--version`, released `identity`, and `doctor` before executing the managed helper. A failure returns a stop; no installation or repair starts. |
| 4 | Existing `harness-orient/scripts/orient.py` | Receive the verified evaluator launcher as an argument array plus expected version/root. Repeat identity and integrity checks for its receipt; run `validate --json` and `inspect --json`. |
| 5 | `orient.py` → existing evaluator | For a supported selected scope, call `check --artifact ID --json`. Run `preflight` only when the request explicitly names a WO and phase. Return the structured result and receipt inline. |
| 6 | Main agent following `harness-orient` | Explain actual state, selected blockers, and the evaluator's next action. Invalid formal state remains a reported stop; orientation does not authorize repair or the lifecycle action it identifies. |

Reading and analysis do not require a started work order. A status request does not authorize the next lifecycle action it reveals.

The existing `harness-operator-brief` skill runs only if the user explicitly requests it, using a bounded supplied result. It is not an automatic extra step.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | Existing `harness-orient` guides the main agent. | **Adapt:** package `.agents/skills/harness-orient/SKILL.md`; preserve its read-only procedure. |
| **Hook** | No status-specific hook runs. | **Not used:** `SessionStart` preparation is scenario 3; it does not invoke this skill. |
| **Script** | `orient.py` collects observations; `scripts/bridge` supplies trusted inputs. | **Reuse:** existing helper. **New:** `orient` adapter through `bin/launcher bridge`. |
| **Tool/interface** | `exec_command`, `Bash`, or `PowerShell` invokes the launcher. | **Reuse:** host shell tools. **New:** structured request transport; no new MCP server is required. |
| **Evaluator** | `--version`, `identity`, `doctor`, `validate`, `inspect`, and selected `check` supply results. | **Reuse:** existing CLI; optional `preflight` needs an explicitly requested WO and phase. |
| **Subagent** | No delegation occurs. | **Not used:** today's orient contract requires the complete procedure in one agent. |
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

- Add the `orient` bridge operation. Validate managed helper bytes before execution, then pass the existing helper its required `target`, `--evaluator-launcher-json`, `--expected-evaluator-version`, and `--expected-evaluator-root`; add `--artifact` and `--preflight-phase` only when selected.
- The evaluator argument array contains the absolute external interpreter followed by `-I -m se_harness`. Expected identity comes from trusted runtime resolution. The version call is `harnessctl --version`. Display the helper's result without calculating another next action.
- Package the portable skill and adapt Claude's wrapper. If `harness-operator-brief` is explicitly requested, follow its existing contract and `scripts/check_brief.py` using a current bounded result.

**Inputs, outputs, and writes**

- **Inputs:** `operation: orient`, repository, optional artifact and requested phase; the launcher supplies trusted evaluator identity.
- **Outputs:** Structured orientation and an explanation for the user.
- **Writes:** No repository, Git, lifecycle, runtime, or retained receipt writes. The proposed host transport uses a temporary request outside the target; it must not alter the measured project.

**Host differences**

- **Codex:** Explicitly name `harness-orient`; invoke the launcher through `exec_command`.
- **Claude Code:** Proposed plugin packaging exposes `/verity-plane:harness-orient`; `Bash` or native `PowerShell` invokes the same launcher. Adapt the current repository-local wrapper. See the [host comparison](../plugin-installation-proposal-2026-09-06.md#native-capabilities-and-their-limits).

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
User → change skill [New], draft mode
        ↓
Read current definitions → identify reuse and additions
        ↓
Bridge [New] → existing scaffold-domain / create-artifact
        ↓
Agent edits drafts → existing validate → review set
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → `change` skill **[New]** | **Codex:** ask “Use the verity-plane change skill to draft an artifact package for this change.” **Claude Code:** `/verity-plane:change draft`. The agent reads `skills/change/SKILL.md` and installed `ARTIFACT_AUTHORING.md`. |
| 2 | Main agent | Read definitions and templates with Codex `exec_command`, or Claude Code `Read` / `Bash` / `PowerShell`. List reused IDs, proposed additions, relationships, and authorized authoring paths. Resolve missing meaning or scope before writing affected content. |
| 3 | Main agent → optional `investigator` **[New]** | Delegate “Which requirements cover exports?” with the selected scope, using the [host-specific invocation](README.md#shared-component-names-and-calling-convention). The helper returns matching IDs and source locations. The main agent prepares the proposal; the investigator edits and approves nothing. |
| 4 | Agent → `scripts/bridge` **[New]** | Through `bin/launcher bridge`, submit operation `evaluator` with the argument array for existing `scaffold-domain --dry-run --json` if a domain is needed, then `create-artifact --dry-run --json` for each addition. Show proposed paths and IDs. |
| 5 | Bridge → existing authoring commands | Within authorized scope, repeat each selected command without `--dry-run`. Return actual created paths and IDs after each call. Each artifact is a separate write; a partial package can remain. |
| 6 | Agent → existing editing tool | Use Codex `apply_patch`, or Claude Code `Edit` / `Write`, to fill content, owners, relationships, acceptance criteria, and WO scope. Supported `PreToolUse` events invoke `hooks/handler` **[New]** to check the mapped authoring boundary. |
| 7 | Agent → bridge → existing `validate` | Submit the `validate --json` argument array. Return findings, correct drafts within scope, and validate again. Present the completed review set to scenario 7. |

Authoring follows repository policy. It cannot require a started implementation WO merely to draft that same WO. Ordinary definitions begin `draft`; decision artifacts begin `open`. Neither means approved.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `change`, at `skills/change/SKILL.md`, guides draft mode. | **New:** instructions that read current authoring rules and plan the package. |
| **Hook** | `PreToolUse` invokes `hooks/handler` for covered writes. | **Reuse:** host event. **New:** authoring-scope mapping; incomplete drafts are expected between edits. |
| **Script** | `bin/launcher` runs `scripts/bridge` operation `evaluator`. | **New:** structured dispatch and per-file progress; no atomic package command is claimed. |
| **Tool/interface** | Shell tools invoke the bridge; `apply_patch` or `Edit` / `Write` completes drafts. | **Reuse:** host tools. **New:** binding of those writes to authorized authoring scope. |
| **Evaluator** | `scaffold-domain`, `create-artifact`, and `validate` create and check records. | **Reuse:** existing commands and templates. |
| **Subagent** | `investigator` finds reusable definitions. | **New:** optional read-only agent; findings remain observations. |
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
- Existing previews: `harnessctl scaffold-domain . --domain example-change --dry-run --json` and `harnessctl create-artifact . --domain example-change --type requirement --id REQ-DEMO-101 --dry-run --json`. Existing validation: `harnessctl validate . --json`. [cli.py](../../../se_harness/cli.py) declares these argument forms.
- Baseline and inspection status are recorded above. There is no atomic package command or authoring-scope parameter. Automatic IDs examine local refs and the worktree, not remote-tracking refs; dry-run IDs are not reservations.

**Proposed additions**

- Add `change` draft mode, the shared `evaluator` bridge operation, and per-file progress reporting. Define authoring-scope enforcement separately; the existing command cannot prove it from a WO argument.
- Package `agents/investigator.md` for Claude Code. Provide a separately registered `.codex/agents/investigator.toml` for Codex; do not assume a native Codex plugin agent field. Both definitions are new.

**Inputs, outputs, and writes**

- **Inputs:** Requested outcome, authorized authoring scope, current graph, domain, artifact types, and IDs. Each `evaluator` request contains an `argv` array without the `harnessctl` executable name.
- **Outputs:** Created paths, validation findings, and the review set.
- **Writes:** Authorized domain scaffolding and individual artifacts. No approval or implementation state is granted.

**Host differences**

- **Codex:** `exec_command` invokes the launcher; `apply_patch` edits. Register `investigator` separately if used. Shell execution uses the host's `Bash` hook matcher, not an `exec_command` matcher.
- **Claude Code:** `Bash` / `PowerShell` invokes the launcher; `Read`, `Edit`, and `Write` handle files. Native plugin agent discovery loads `investigator`. Test actual hook coverage in each host; see the [host comparison](../plugin-installation-proposal-2026-09-06.md#native-capabilities-and-their-limits).

**Checks that demonstrate the behavior**

- **Success:** Existing intent plus requested change → only necessary additions, with valid links.
- **Refusal:** Damaged installation → authoring command refuses the write.
- **Recovery:** Failure after two creations → retain those drafts and resume without duplicates.

**Open questions**

- How will authoring scope include trusted owner exceptions without requiring an already-started WO? Direct edits and arbitrary shell commands need a demonstrated control boundary; registering a hook alone does not establish it.

</details>

## Scenario 7: Review and approve the package

### 1. Purpose and starting point

**Purpose:** Make each approval explicit and attributable to the responsible owner.

- **Starts when:** A completed package is ready for review.
- **Requires:** Exact artifacts, current content, applicable passing gates, and identified accountable owners.
- **Successful result:** Only selected artifacts are approved. WO approval does not start implementation.

### 2. Workflow

```text
change skill [New] → review-preview [New]
        ↓
decision-review [New] → each accountable owner decides
        ↓
review-apply [New] checks plan and decision → existing transition
        ↓
Read actual states → separately review the WO
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → `change` skill **[New]** | **Codex:** ask “Use the verity-plane change skill to review these artifact IDs.” **Claude Code:** `/verity-plane:change review`. The agent reads the selected artifacts and installed `DECISION_RIGHTS.md`. |
| 2 | Agent → `scripts/bridge` **[New]** | Use `exec_command`, `Bash`, or `PowerShell` to call `bin/launcher bridge` with operation `review-preview`, selected IDs/target states, and accountable roles. The bridge calls existing `transition` without `--apply`. |
| 3 | Bridge → main agent | Return blockers and a `plan_id` **[New]** bound to selected content and relevant graph inputs. Present the exact proposed changes to each required owner; a failed plan is not ready for approval. |
| 4 | Human → `decision-review` **[New]** | Review selected content and decision meaning. The protected review service authenticates the actor, checks the required role, and stores the exact decision with its plan/content binding. Return a `decision_ref` **[New]** for each required decision. |
| 5 | Agent → bridge operation `review-apply` **[New]** | Submit the `plan_id` and decision references. The bridge verifies them with the protected service, rejects stale content, and reruns evaluator checks. Only then call existing `transition --apply` for the selected approved decisions. |
| 6 | Bridge → main agent | Return actual applied states or failure. Read the resulting selected records and report exactly which approvals occurred. Related artifacts do not change automatically. |
| 7 | Engineering owner → the same review flow | After the governing chain is complete, review the WO through a separate `review-preview` / `decision-review` / `review-apply` cycle. Approval leads to scenario 9 for the distinct start decision. |

The package is a review grouping, with separate artifact approvals. Product, technical, assurance, and engineering owners retain their decisions, even when one person holds several roles.

Reuse an existing explicit decision when the trusted interface establishes that it covers the exact reviewed content. Do not turn each invocation into another confirmation.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/change/SKILL.md` guides review mode. | **New:** presents selected content, evaluator blockers, and separate decisions. |
| **Hook** | `PreToolUse` routes covered transition attempts to `hooks/handler`. | **Reuse:** host event. **New:** mapped checks; the hook does not authenticate an owner. |
| **Script** | `scripts/bridge` implements `review-preview` and `review-apply`. | **New:** content/decision binding around existing evaluator planning and application. |
| **Tool/interface** | Shell tools invoke the bridge; humans use `decision-review`. | **Reuse:** `exec_command`, `Bash`, or `PowerShell`. **New:** protected human review interface. |
| **Evaluator** | `transition` checks and applies selected states. | **Reuse:** `plan_transition()` and `apply_transition()`, including multi-artifact planning. |
| **Subagent** | Optional `investigator` reports consistency findings before review. | **New:** bounded read-only analysis; no approval or use of another owner's identity. |
| **Human** | Make artifact-specific decisions. | **Reuse:** owners named by `DECISION_RIGHTS.md`. |
| **External control** | Protect authenticated decisions from agent modification. | **New:** protected service behind `decision-review`; no such boundary exists in today's local `--decision` argument. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| A required owner has not decided, or the service cannot authenticate the decision. | `review-apply` refuses that transition. | Obtain or establish the exact existing decision through `decision-review`. |
| Content or relevant graph inputs change after review. | `review-apply` rejects the stale plan. | Repeat `review-preview` and refresh affected decisions on the changed content. |
| A gate fails or blocking decision remains open. | The evaluator refuses the transition. | Resolve the reported blocker and preview again. |
| Application is interrupted. | Report an unknown or partial result until actual records are inspected. | Read current states before retrying; do not blindly replay the packet. |

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

- `review-preview` binds selected IDs, requested states, required roles, content hashes, and relevant graph inputs to a `plan_id`. `review-apply` consumes that plan and authenticated `decision_ref` values, then reruns the existing evaluator.
- `decision-review` records the actor, role, exact decision, and reviewed content in a protected service. An agent-created file, arbitrary role string, or unverified reference cannot satisfy it. This service and its integration do not exist yet.

**Inputs, outputs, and writes**

- **Inputs:** Repository, selected artifacts/states, evaluator argument arrays, bound plan, and authenticated owner decisions.
- **Outputs:** Blockers or review plan, authenticated decision references, and actual transition result.
- **Writes:** Protected review records, then only selected artifact statuses and lifecycle records on successful application. No inferred changes to linked records.

**Host differences**

- **Codex:** `exec_command` invokes the bridge. A tool approval permits the command; it does not approve an artifact.
- **Claude Code:** `Bash` / `PowerShell` invokes the same bridge. Tool permission likewise supplies no lifecycle decision. Both adapters need the trusted decision boundary; see the [authority analysis](../plugin-installation-proposal-2026-09-06.md#architecture-one-engine-two-adapters).

**Checks that demonstrate the behavior**

- **Success:** Approve two explicitly selected definitions → change only those two.
- **Refusal:** Owner absent or reviewed content changed → no application through the proposed interface.
- **Recovery:** Fresh decision on refreshed content → repeat preview and application.

**Open questions**

- Which identity provider and storage boundary implement `decision-review`? How will controls prevent direct local edits or CLI calls from bypassing it? Protected integration must reject untrusted approval records; a local wrapper alone is insufficient.

</details>

## Scenario 8: Revise approved definitions or work scope

### 1. Purpose and starting point

**Purpose:** Change the intended system or permitted work without silently extending an earlier approval.

- **Starts when:** Investigation, implementation, or review reveals a necessary change outside the approved meaning or scope.
- **Requires:** Affected artifacts, reason for change, and responsible owners.
- **Successful result:** An authorized amendment or new draft, followed by re-evaluation of the affected scope; an explicit stop if the requested operation is unsupported.

### 2. Workflow

```text
Affected work stops → change skill [New], amend mode
        ↓
Read impact → amendment-preview [New, design pending]
        ↓
Owner decides through decision-review [New]
        ↓
amendment-apply [New, design pending] → validate and scope check
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Main agent | Stop the affected implementation or approval operation. Preserve records and evidence. **Codex:** invoke the named `change` skill for an amendment. **Claude Code:** `/verity-plane:change amend`. These skill modes are **[New]**. |
| 2 | Agent or optional `investigator` **[New]** | Read affected definitions, links, verification contracts, and WOs with existing read/shell tools. Return old meaning, proposed meaning, affected IDs, and scope consequences as analysis. |
| 3 | Agent → `scripts/bridge` **[New]** | Through `bin/launcher bridge`, submit operation `amendment-preview` **[New; design pending]** with affected IDs, exact proposed content changes, and current hashes. Return a bound plan naming required decisions, or an unsupported-path stop. |
| 4 | Agent following `skills/change/SKILL.md` **[New]** | If installed rules require a DEC, use existing `create-artifact --type decision` to draft it under scenario 6. Record the question, blocked IDs, and declared options. It starts `open` and does not change its targets. |
| 5 | Accountable owners → `decision-review` **[New]** | Decide the exact amendment and any revised work scope. For a DEC, use `review-preview` / `review-apply` around existing `decide` with the authenticated decision. Selecting `amend` records the answer and leaves target artifacts unchanged. |
| 6 | Agent → bridge operation `amendment-apply` **[New; design pending]** | Submit the plan and authenticated decisions. Reject stale inputs; apply only reviewed content under established amendment rules, or create separately authorized new drafts. Never invent an `approved → draft` transition. |
| 7 | Agent → bridge → existing evaluator | Run `validate --json`, then the selected WO's applicable `check --checkpoint scope` using actual changed paths. Report the result and remaining decision. Resume affected work only through its permitted procedure. |

The plugin cannot invent an `approved → draft` transition. Existing authoring rules allow amendments to approved definitions; there is no dedicated amendment transaction. Authorized edits follow those rules and the affected owners' decisions. A new WO can cover additional work under unchanged definitions. New reopen or replacement workflows need explicit semantics.

`amendment-preview` and `amendment-apply` name proposed operations for binding edits to reviewed content. Their transaction and any approval-invalidation behavior need a governed design before implementation; the current supported authoring path remains available.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/change/SKILL.md` guides amend mode. | **New:** distinguishes supported authoring from unsupported lifecycle changes. |
| **Hook** | `PreToolUse` invokes `hooks/handler` for covered scope-changing writes. | **Reuse:** host event. **New:** mapping to the reviewed amendment; arbitrary shell coverage is not established. |
| **Script** | `scripts/bridge` previews and applies the bounded amendment. | **New:** `amendment-preview` / `amendment-apply`; transaction and content binding still need governed design. |
| **Tool/interface** | Shell tools call the bridge; `decision-review` shows old and proposed content. | **Reuse:** `exec_command`, `Bash`, or `PowerShell`. **New:** trusted amendment review view. |
| **Evaluator** | `create-artifact`, `decide`, `validate`, and scope `check` handle supported operations. | **Reuse:** existing commands; no general reopen or replacement command exists. |
| **Subagent** | Optional `investigator` traces impact. | **New:** read-only findings with source IDs; no amendment or remediation decision. |
| **Human** | Decide changed meaning and remediation scope. | **Reuse:** affected owners and `DR-REMEDIATION-SCOPE`. |
| **External control** | Protect authentic decisions and subsequent integration. | **New:** protected `decision-review` records and independent integration enforcement; local hooks are insufficient. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Proposed work exceeds approved scope. | The relevant scope check fails; affected work stops. | Obtain remediation authority and a supported path. |
| Amendment needs an undefined lifecycle edge or replacement rule. | The evaluator refuses unsupported transitions; `amendment-preview` reports the missing semantics. | Define the missing rules through separate governed work. Current permitted amendments remain available. |
| A decision selects “amend.” | The decision records the answer; its targets remain unchanged. | Perform separately authorized edits through an established procedure, then re-evaluate. |
| Reviewed content changes before application. | The proposed `amendment-apply` rejects the stale plan. | Read current content, refresh the amendment, and obtain affected decisions. |

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
- Example scope check after authorized edits: `harnessctl check . --artifact WO-DEMO-101 --checkpoint scope --changed-path docs/engineering/example-change/specifications/SPEC-DEMO-101.md --changes-complete --json`. The path is illustrative; actual callers derive the complete change set. Declared paths are evidence, not trusted proof of every effect.
- Baseline and inspection status are recorded above. A DEC option named `supersede` is not a lifecycle transition for its target.

**Proposed additions**

- `amendment-preview` binds current content, exact proposed changes, affected IDs, and required decisions. `amendment-apply` checks that binding and invokes only supported authoring operations. Current manual edits use `apply_patch` or `Edit` / `Write`; their guarded replacement is new work.
- Define replacement, approval-invalidation, and multi-file recovery semantics through governed design. Until supported, return the specific missing operation; this proposal supplies no authority to invent it.

**Inputs, outputs, and writes**

- **Inputs:** Approved records, exact proposed changes, affected work/evidence, current hashes, and authentic owner decisions.
- **Outputs:** Amended content or new drafts, re-evaluation results, or an explicit unsupported-path stop.
- **Writes:** None during impact analysis. Authorized definition amendments, new drafts, and selected decision dispositions are separate writes. Historical VREC/RLS facts remain intact; lifecycle states do not change by inference.

**Host differences**

- **Codex:** `exec_command` invokes the bridge; current authorized content edits use `apply_patch`. Optional `investigator` needs the separate registration described in scenario 6.
- **Claude Code:** `Bash` / `PowerShell` invokes the bridge; current authorized content edits use `Edit` / `Write`. Native plugin discovery supplies the optional investigator. Both hosts return the same unsupported-path result; see the [shared architecture](../plugin-installation-proposal-2026-09-06.md#architecture-one-engine-two-adapters).

**Checks that demonstrate the behavior**

- **Success:** Additional work within unchanged definitions → separately authorized new WO proposal, with the original scope preserved.
- **Refusal:** Attempt an unsupported reopen transition → no lifecycle write.
- **Recovery:** Owner selects a supported bounded path → create the required drafts and return to review.

**Open questions**

- What transaction records amendments and handles affected approvals? Which changes require new IDs? What proves that all writes, including direct edits, respect the transaction? These rules need separate governed design.

</details>
