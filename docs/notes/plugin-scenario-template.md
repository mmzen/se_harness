# Plugin scenario template

<!-- Target expertise: 3.5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

Use this template for each detailed scenario linked from [Plugin operation workflows](plugin-operation-workflows-2026-09-06.md). It explains what happens, who does the work, and how the proposed plugin uses the current implementation.

Copy the section below and replace the bracketed text. Keep the six blocks. Mark a component **Not used** when the scenario does not need it. Keep commands and source details in the last block so the main explanation is understandable without them.

This is a documentation template for proposals. It is not a formal engineering artifact and grants no approval or execution authority. Each completed scenario should identify its implementation baseline and distinguish existing behavior from proposed changes.

---

## Scenario: [Action and intended result]

<!-- Example title: Prepare the agent for governed work. Use an action, not an internal component name. -->
<!-- Record the source commit/version and review date in the containing page. -->

### 1. Purpose and starting point

**Purpose:** [Explain the benefit in one sentence.]

- **Starts when:** [User request or host event that starts this scenario.]
- **Requires:** [Conditions and inputs needed before the scenario can proceed.]
- **Successful result:** [Observable result when the scenario succeeds.]

<!-- Keep this block short. Distinguish a successful check from permission to perform work. -->

### 2. Workflow

Show the main sequence in a short diagram:

```text
[Request or event]
        ↓
[First action]
        ↓
[Check or decision]
        ↓
[Result or next handoff]
```

<!-- Replace the outline with the actual sequence. Show a human decision when one is required. If using Mermaid, render the diagram before publishing it. -->

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | [Named component or person] | [One principal action and its result.] |
| 2 | [Named component or person] | [One principal action and its result.] |
| 3 | [Named component or person] | [One principal action and its result.] |

<!-- Add or remove rows as needed. The diagram shows the sequence; the table explains responsibility. Identify when the workflow waits for a decision. Do not hide several independent operations in one step. -->

### 3. Components and implementation mapping

Use **Reuse**, **Adapt**, **New**, or **Not used** in the last column. Name the existing command or implementation when one is available. Explain the missing work when it is not.

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | [Instructions that guide the agent, or Not used.] | [Status, existing behavior, and change needed.] |
| **Hook** | [Host event and automatic action, or Not used.] | [Status, existing behavior, and change needed.] |
| **Script** | [Defined processing or calls performed by code, or Not used.] | [Status, existing behavior, and change needed.] |
| **Tool/interface** | [Operation exposed for invocation, or Not used.] | [Status, existing behavior, and change needed.] |
| **Evaluator** | [Harness checks or transactions used here, or Not used.] | [Status, existing behavior, and change needed.] |
| **Subagent** | [Bounded task and permitted effects, or Not used.] | [Status, existing behavior, and change needed.] |
| **Human** | [Exact decision and accountable person, or Not used.] | [Status, existing decision boundary, and any new interaction needed.] |
| **External control** | [System enforcing a protected effect, or Not used.] | [Status, existing enforcement, and any gap to close.] |

<!-- A hook can invoke a script, and a tool can expose that same script. Explain that relationship instead of inventing another policy implementation. A skill gives instructions; it is not itself an executable program. -->

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| [Required input or installation component is missing.] | [Who detects it, what stops, and what remains available.] | [Concrete corrective step and responsible actor.] |
| [A check fails or the state changes.] | [Which component prevents the operation and what remains unchanged.] | [Repair or new decision required, then the check to repeat.] |
| [An accountable decision is required.] | [What is presented, who decides, and which operation waits.] | [How the exact decision is checked before continuing.] |

<!-- Replace these suggested cases with the cases that apply. Distinguish a displayed warning from an enforced stop. Do not imply that a successful installation check, host tool permission, or actor-name argument supplies a human decision. -->

### 5. Example result

Show one short example of what the agent or user receives:

> [What completed and the observed result.]
> [Any state that changed, or a material effect that did not occur.]
> [The next required action or accountable decision, when applicable.]

<!-- Use clearly illustrative IDs and facts. Report successful operations separately from remaining decisions. Do not present invented evidence as an observed result. -->

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

- [Existing command or function and source link.]
- [Source commit/version used for this mapping.]
- [Whether the interface was inspected, syntax-checked, or exercised.]

**Proposed additions**

- [New script, adapter, or interface required.]
- [How it calls the existing evaluator without creating another set of governance rules.]

**Inputs, outputs, and writes**

- **Inputs:** [Values required and where they come from.]
- **Outputs:** [Result returned and its consumer.]
- **Writes:** [Files, state, cache, or external effects changed; write None when applicable.]

**Host differences**

- **Codex:** [Supported event/interface, limitations, and source.]
- **Claude Code:** [Supported event/interface, limitations, and source.]

**Checks that demonstrate the behavior**

- **Success:** [Input or trigger → expected result.]
- **Refusal:** [Failure or missing decision → expected stop.]
- **Recovery:** [Correction or interruption → expected safe resumption.]

**Open questions**

- [Unresolved design choice and the evidence needed to decide it, or None.]

</details>
