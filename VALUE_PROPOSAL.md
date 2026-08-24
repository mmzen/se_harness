# SE Harness — Executive Speech and Demonstration

**Target duration:** 10–15 minutes
**Audience:** Executives, engineering leaders, product leaders, and quality or release leaders
**Technical depth:** 4/10
**Objective:** Explain the control problem created by coding agents, demonstrate the current product honestly, and show how humans can move from continuous supervision to accountable decision points.

This is a presentation brief, not an authoritative engineering contract. The repository's formal artifacts, managed workflow, released evaluator, retained evidence, and accountable decisions remain authoritative.

## Core message

> Coding agents are becoming capable of doing more software-engineering work. The harder question is whether an organization can authorize that work, assess what changed, retain evidence, identify the exact source candidate that was checked, and keep accountable decisions with humans.

> SE Harness adds a repository-native governance and assurance layer for that problem.

A useful shorthand is:

> **Agents provide execution. SE Harness connects intent, bounded work, evidence, provenance, and decision authority.**

“Control plane” can be a useful metaphor, but it is not a security claim. SE Harness does not sandbox an agent, grant or deny operating-system permissions, or replace repository and hosting controls.

## Product reality: current, roadmap, and vision

Keep these states separate throughout the presentation.

| State | What can be said |
| --- | --- |
| **Current — shipped** | Repository-native formal artifacts; explicit lifecycle transitions and decision rights; released-evaluator integrity; graph, preflight, and selected-scope checks; retained evidence; exact Git candidate provenance through VREC and RLS records; a read-only Explorer; and the read-only, single-agent `harness-orient` skill with delegation disabled. |
| **Roadmap — approved or planned, not shipped** | Delegated mutation, stronger execution receipts, additional skills, runtime adapters, and multi-agent orchestration. |
| **Vision — intended outcome, not demonstrated** | Organizational-scale governed delegation across many agents, repositories, and engineering systems. |

The current product governs repository state and detects violations in the evidence it receives. Selected-scope checking depends on the caller declaring the complete change set. A process with write access can still modify files; agent-runtime permissions, code review, required CI, and hosting rules provide the surrounding enforcement.

SE Harness is not a coding agent, agent runtime, sandbox, permission system, standalone security boundary, compliance certification, or replacement for Git hosting and deployment controls.

## Suggested 12-minute flow

| Time | Section | Purpose |
| --- | --- | --- |
| 0:00–1:30 | The problem | Establish the new control and evidence problem |
| 1:30–3:00 | What SE Harness is | Position the current product and its boundary |
| 3:00–9:00 | Demonstration | Show one governed change and its human decisions |
| 9:00–11:00 | Value | Translate the demonstration into outcomes |
| 11:00–12:00 | Closing | Leave one memorable message |
| Optional 3–5 min | Q&A | Address likely executive objections |

## 1. Opening — the problem

Software development is entering a phase where agents can inspect a repository, change several files, write tests, run tools, and prepare work for integration. This creates productivity potential and a control problem.

Ask:

> How do we know what the agent was authorized to do, whether the result satisfies the requirement, what evidence was collected, which exact source commit was assessed, and who made the accountable decision?

Git records changes. CI records automated checks. A ticket records an intention. Each is useful, but none alone creates a complete engineering decision chain.

Suggested talk track:

“Most AI-development discussions focus on model capability: which model writes better code or which agent is faster. Those capabilities will keep changing.

The durable problem is governance. If an agent changes 40 files overnight, ‘the tests are green’ is not enough. I want to know why the work exists, who authorized it, what scope was assessed, which evidence was retained, which exact candidate was verified, and who has authority over the next decision.”

## 2. What SE Harness is

> **SE Harness turns a new or existing Git repository into a governed software-engineering workspace for humans and coding agents.**

It connects:

```text
Intent → Requirement → Specification → Authorized work
       → Evidence → Exact source candidate → Verification decision
       → Separate delivery or release decision
```

It complements coding agents. The agent interprets and executes work; the repository carries the engineering contract and evidence; accountable owners exercise decision rights.

Suggested visual:

```text
Coding agent or human implementation
                 │
                 ▼
┌───────────────────────────────────────┐
│ SE Harness repository layer           │
│ intent • definitions • bounded work   │
│ evidence • provenance • decisions     │
└───────────────────────────────────────┘
                 │
                 ▼
     Code • tests • Git • hosting
```

Key sentence:

> **The model can change. The repository's engineering contract does not change with it.**

## 3. Demonstration — one small governed change

Use a tiny prepared change, such as “add a configurable timeout to an existing service.” Use one coding agent only. The purpose is to demonstrate governance, not coding speed or multi-agent coordination.

### Step 1 — show approved work

Start with an approved requirement, specification, verification contract, and work order. Show:

1. the intended outcome;
2. the authorized paths or component scope;
3. the required verification;
4. the current `approved` lifecycle state.

Talk track:

“This is not only a prompt. It is a bounded engineering work order connected to the definitions and verification contract that govern it.”

Message:

> **The work is defined and approved before implementation starts.**

### Step 2 — show the start decision

Use `focus` and start preflight to show the selected context and readiness. Then show the engineering owner's explicit start decision and the work order transition from `approved` to `in_progress`.

Talk track:

“Readiness checks prepare information. They do not authorize work. The accountable start decision is separate.”

Message:

> **Automation can prepare a decision; it does not exercise the decision right.**

### Step 3 — let the agent implement

Give the agent the bounded work. Let it inspect code, make the small change, update tests, run the repository checks, and retain evidence. Accelerate or pre-stage this part if timing is uncertain.

Be precise about scope:

“The agent declares the complete changed-path set, and SE Harness assesses that set against the approved scope. The harness detects a mismatch; external permissions and repository controls determine whether an unauthorized write can occur.”

Message:

> **A checked scope is an assurance input, not a sandbox.**

### Step 4 — show a real blocked checkpoint

Prepare one understandable missing condition, such as absent required evidence. Run the bound checkpoint and show the canonical restitution fields. Use actual output from the prepared repository; do not invent a `STATUS: BLOCKED` banner.

An abbreviated, structurally accurate example is:

```text
Outcome
Blocked.

Done
- Evaluated the selected work order and its current evidence.

Not done
- The implementation-evidence gate has not passed.

Blocked by
- Required retained evidence is missing.

Current lifecycle state
- WO-DEMO-001 remains in_progress.

Decision required
None until the reported blocker is resolved.

Next
Resolve the missing evidence and rerun the same checkpoint.

Command or response
harnessctl check . --artifact WO-DEMO-001 --checkpoint handoff
```

Talk track:

“The agent may believe its coding task is finished. That is not the same as an accepted engineering result. A failed gate leaves the formal state unchanged.”

### Step 5 — complete implementation, then bind assurance

Resolve the missing evidence and rerun the checkpoint. The lifecycle then proceeds through separate steps:

```text
in_progress work
  → engineering-owner completion decision
implemented work
  → clean candidate commit
  → capture evidence and exact candidate in a ready VREC
ready VREC
  → assurance-owner decision
verified VREC
  → separately selected repository-integration or release path
```

Preparing a VREC leaves it `ready`; it does not verify itself. The assurance owner reviews the exact candidate and retained evidence, then changes only the VREC to `verified` or rejects it. The referenced work order is not changed by that decision.

The Git identity proves which source candidate was assessed. Do not call it the “exact executable” unless a separate release record binds the built distribution identity.

Message:

> **Evidence and assurance are bound to one exact source candidate; later changes are a different candidate.**

### Step 6 — show the human decision boundary

Finish in the read-only Harness Explorer or with `focus`. Point to the next accountable decision and the actions that have not occurred.

Talk track:

“The aim is not a human approval after every agent action. The human owns the decisions for which the organization remains accountable: intent, risk, implementation completion, assurance, release, and external action as policy requires.”

Message:

> **Human-in-the-loop becomes human-at-the-decision-point.**

## 4. Value in four outcomes

### 1. Increase delegated execution without hiding accountability

More capable agents can produce more changes. SE Harness gives governed changes a bounded work definition, explicit state, retained evidence, and named decisions.

> **Delegate execution while preserving accountable authority.**

This is a product direction, not a claim that today's shipped skill autonomously mutates repositories or coordinates agents.

### 2. Make correctly governed material changes explainable

When the required chain is complete, reviewers can answer:

- Why does this work exist?
- What was approved?
- What scope and evidence were assessed?
- Which exact source candidate was verified?
- Who made the accountable decisions?

> **From intent to evidence to exact source.**

### 3. Keep governance independent of the AI provider

Models and agent products will change rapidly. Repository-native contracts and evidence reduce dependence on one model or agent interface.

> **Change the executor without silently changing the engineering rules.**

Runtime adapters still need implementation and verification for each supported environment.

### 4. Move humans to the right level

The objective is to automate routine execution and evidence preparation while reserving accountable decisions for humans.

> **Automate preparation and execution. Preserve decision authority.**

Role separation matters. One person may hold every role, but that provides accountability without independent assurance. Using different models or sessions does not by itself create independence.

## 5. Challenge the proposition

The story is credible only with these limits visible:

- **Control is conditional.** SE Harness validates repository evidence and lifecycle rules; it does not physically restrain a process with write access.
- **Completeness is an input.** Selected-scope assessment relies on a caller-declared complete change set. CI and hosting configuration determine whether that assertion is required and reviewed.
- **Multi-agent maturity is roadmap, not current product.** The shipped skill is read-only, single-agent, and has delegation disabled.
- **Scale is unproven.** Repository-native, machine-readable governance is compatible with scale, but usability, concurrency, integration, and operating evidence will determine whether scale is achieved.
- **Artifact burden is the adoption risk.** If people manually maintain every artifact for routine work, the product has failed. Skills and automation must simplify interaction without taking decision rights.
- **Compliance is not conferred.** The harness can supply traceability and evidence for a control system; an organization must define, operate, and audit that system.
- **A malicious privileged maintainer is outside the standalone boundary.** Integrity checks can detect governed-content changes under the released evaluator; access controls and independent review must prevent or respond to unauthorized changes.

## 6. Closing

Suggested close:

“The opportunity with coding agents is larger than faster code generation. Agents may execute a growing part of engineering, but increased autonomy without a durable control model can produce software faster than an organization can understand or govern it.

SE Harness makes the repository carry the intent, authorization, evidence, source provenance, and decision state around correctly governed work.

The question is no longer only, ‘Can an agent build this?’

The better question is, ‘Can we delegate more execution and still know why the software exists, what was assessed, and who is accountable for the next decision?’

That is the problem SE Harness is designed to address.”

A concise final value proposition:

> **SE Harness helps teams use increasingly capable coding agents without losing the repository-level chain from intent and authorized work to evidence, exact source provenance, and accountable human decisions.**

## Demo preparation checklist

- [ ] Use a tiny feature or defect.
- [ ] Prepare the requirement, specification, verification contract, and approved work order.
- [ ] Use a disposable repository and one coding agent.
- [ ] Rehearse the explicit start decision and `in_progress` transition.
- [ ] Prepare one real, easy-to-understand blocked gate.
- [ ] Retain the required implementation evidence.
- [ ] Rehearse engineering completion before candidate commit and VREC capture.
- [ ] Show a `ready` VREC before the assurance decision.
- [ ] Show the exact source commit without calling it an executable identity.
- [ ] End at the next decision; do not push, merge, release, or deploy during the core demonstration.
- [ ] Keep prepared output or a recording as fallback.

Do not spend the executive session on installation, TOML syntax, directory structure, Python internals, every artifact type, hash implementation, or CLI help. Do not demonstrate multi-agent orchestration as a current capability.

## Q&A — likely executive pushback

### “Isn't this Jira plus Git plus CI/CD?”

Those systems hold parts of the story. Jira may record intended work, Git records changes, and CI records automated checks. SE Harness connects repository-native intent, definitions, bounded authorization, evidence, exact candidate identity, and accountable decisions. It complements those systems and still depends on their controls where they remain authoritative.

### “Why not put the rules inside the agent?”

The executor should not be the sole authority deciding whether its own work is acceptable. Models and agents also change frequently. Keeping the engineering contract in the repository makes it inspectable and lets an external released evaluator assess candidate state.

### “Does SE Harness prevent an agent changing unauthorized files?”

No. It can detect that a caller-declared complete change set exceeds approved scope and fail a gate. Preventing the write requires agent-runtime permissions, repository access control, review, CI, or hosting rules. A privileged malicious process is not contained by the harness alone.

### “Will this become another process layer?”

That is the main product risk. Strong internal governance needs a simple interaction surface. Routine artifact preparation and evidence collection should be automated, while accountable decisions remain explicit. If every engineer must manually maintain the full model for every small change, adoption will fail.

### “Why keep humans if agents do the work?”

Execution and accountability are different. Humans should not continuously supervise every tool call, but they remain responsible for decisions assigned by organizational policy. The harness aims to present the right evidence at those points.

### “Is multi-agent engineering available now?”

Not as a shipped orchestration capability. The current portable skill is a read-only, single-agent orientation pilot with delegation disabled. Delegated mutation, worker coordination, and stronger execution receipts are roadmap work that require separate implementation and verification.

### “Can it scale to hundreds of repositories?”

That is the vision, not a demonstrated result. The repository-native and machine-readable design avoids a mandatory central service, but real scale still needs evidence about usability, concurrent work, identifier coordination, integration, support, and operations.

### “Does this provide independent assurance?”

Only when accountable roles are genuinely separated according to repository policy. One owner holding all roles still gains traceability and explicit decisions, but not independent assurance. Different agent sessions or models are not proof of independence.

### “Is this a compliance product?”

No. It is an engineering governance and assurance layer. Its traceability and provenance may support a compliance program, but they do not define applicable regulation, certify the organization, or prove controls are operating effectively.

### “What prevents changes to the harness rules?”

Managed-file integrity and an independently installed released evaluator can detect candidate changes or mismatches before governed mutations proceed. That is stronger than letting candidate code accept itself, but it is not physical prevention. Repository permissions, protected checks, and accountable review complete the boundary.

### “What would success look like?”

An authorized work item is executed with minimal supervision. The implementation returns either sufficient evidence for the next accountable decision or a genuine blocker requiring judgment. The organization gains throughput and a clearer decision trail. Achieving that broadly remains the product direction, not a claim already proven at enterprise scale.

## Narrative discipline

Return to three contrasts:

| Old question | Better question |
| --- | --- |
| Can AI generate code? | Can AI perform governed engineering work? |
| Did the tests pass? | What exact candidate was assessed against which requirement? |
| Is a human watching the agent? | Is a human controlling the accountable decisions? |

If the audience remembers those three shifts—and the boundary between current capability and roadmap—the presentation has worked.
