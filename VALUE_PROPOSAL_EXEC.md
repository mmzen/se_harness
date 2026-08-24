# SE Harness — Executive Speech & Demonstration Structure

**Target duration:** 10–15 minutes  
**Audience:** Executives, engineering leaders, product leaders, quality/release leaders  
**Technical depth:** 4/10  
**Objective:** Explain why SE Harness exists, demonstrate how it governs agentic software engineering, and make the value proposition obvious without turning the session into a tooling tutorial.

---

## 1. Core message

> **AI agents are becoming capable of doing a large part of software engineering work. The problem is no longer only whether they can produce code. The problem is whether we can control what they are allowed to do, prove what they changed, verify the result, and keep accountable decisions with humans.**
>
> **SE Harness turns a software repository into that governed engineering environment.**

A useful shorthand:

> **Agents provide execution. SE Harness provides control, evidence, provenance, and decision authority.**

---

# Suggested 12-minute flow

| Time | Section | Purpose |
|---|---|---|
| 0:00–1:30 | 1. The problem | Establish why agentic development creates a new control problem |
| 1:30–3:00 | 2. What SE Harness is | Position the product in one clear sentence |
| 3:00–9:00 | 3. Live demonstration | Show a governed change from authorized work to verified result |
| 9:00–11:00 | 4. Value proposition | Translate the demo into business value |
| 11:00–12:00 | 5. Closing | Leave one memorable message |
| +3–5 min | Q&A | Address likely executive pushback |

---

# 1. Opening — The problem

**Duration: ~1.5 minutes**

## Message

Software development is entering a phase where agents can increasingly:

- understand a repository;
- modify several files;
- write tests;
- fix defects;
- run tools;
- prepare pull requests;
- and potentially work for long periods with limited human intervention.

That creates enormous productivity potential.

But it also creates a new problem:

> **How do we know what the agent was supposed to do, whether it was authorized to do it, whether the result satisfies the requirement, exactly which code was verified, and who made the final decision?**

Traditional repositories answer only part of this.

Git tells us **what changed**.

CI tells us **which automated checks ran**.

A ticket tells us **what somebody intended to work on**.

None of them, by themselves, establish a complete engineering decision chain.

## Suggested talk track

“Today, most discussions about AI development focus on model capability: which model writes the best code, which coding agent is fastest, which IDE is best.

I think that becomes less important over time.

The models will improve. The agents will improve.

The harder problem becomes: how do we let them operate at scale without losing engineering control?

If an agent changes 40 files overnight, I do not want the answer to be: ‘the tests are green.’

I want to know why the change exists, who authorized it, what requirement it satisfies, what evidence was collected, which exact commit was verified, and who has the authority to release it.”

---

# 2. What SE Harness is

**Duration: ~1.5 minutes**

## One-sentence definition

> **SE Harness turns a Git repository into a governed software-engineering workspace for humans and coding agents.**

It adds a repository-native system for:

**Intent → Requirements → Specifications → Authorized Work → Verification → Exact Commit → Release Decision → Operations**

## Important distinction

SE Harness is **not another coding agent**.

It can work with Claude Code, Codex, Cursor, or future agent systems.

The agent provides intelligence and execution.

SE Harness defines:

- what work exists;
- what work is authorized;
- what evidence is required;
- what state the engineering work is in;
- what exact code has been verified;
- and which decisions still require accountable humans.

## Suggested visual

```text
              AI / Coding Agents
        Claude | Codex | Cursor | ...

                    │
                    ▼

        ┌─────────────────────────┐
        │       SE HARNESS        │
        │                         │
        │ Intent                  │
        │ Requirements            │
        │ Architecture            │
        │ Authorized Work         │
        │ Verification            │
        │ Provenance              │
        │ Release Decisions       │
        └─────────────────────────┘
                    │
                    ▼

              Git Repository
          Code | Tests | Evidence
```

## Key sentence

> **The agent can do the work. The harness controls the engineering process around the work.**

---

# 3. Demonstration

**Duration: ~6 minutes**

The demo should use **one very small change**. Do not demonstrate a large feature.

The goal is not to impress the audience with coding speed.

The goal is to demonstrate **control**.

A good example:

> “Add a configurable timeout to an existing service.”

Prepare the repository in advance so the requirement, specification and work order already exist.

---

## Demo step 1 — Show the authorized work

**Time: ~45 seconds**

Show the Work Order in the repository or Harness Explorer.

Point out only four things:

1. what must change;
2. which requirement/specification authorizes it;
3. what verification is expected;
4. current lifecycle state.

### Talk track

“This is not a prompt I typed into an agent.

This is an engineering work order.

It is connected to the requirement and specification, and it defines what evidence will be needed before the work can be considered verified.”

### Executive message

> **The unit of work is governed before the agent starts.**

---

## Demo step 2 — Give the work to an agent

**Time: ~45 seconds**

Start Claude Code, Codex, or another coding agent.

Instead of explaining the entire repository manually, give it the bounded work item.

Use SE Harness to expose the relevant engineering context, for example through the harness focus/check workflow.

### Talk track

“The agent does not need unrestricted interpretation of the whole engineering system.

The harness gives it the bounded work, the governing artifacts and the rules relevant to this task.

The model can change. The engineering contract does not.”

### Executive message

> **SE Harness separates model intelligence from engineering governance.**

---

## Demo step 3 — Let the agent implement the change

**Time: ~1 minute**

Let the agent:

- inspect the relevant code;
- make the change;
- update/add tests;
- run the expected checks.

Do not spend time explaining the code.

If possible, accelerate or pre-stage this part.

### Talk track

“This is the part AI coding tools already do increasingly well.

SE Harness is not trying to replace this capability.

It assumes agents will become very good at execution.”

Then immediately move to:

> “The important part starts when the agent says: ‘I’m done.’”

---

## Demo step 4 — Ask the harness, not the agent, whether the work can progress

**Time: ~1 minute**

Run the relevant `harnessctl check` checkpoint.

Ideally, deliberately prepare one missing condition so the first check returns a blocker.

Examples:

- required verification evidence is missing;
- work is not in the expected lifecycle state;
- required artifact relation is missing;
- the repository is not clean;
- candidate commit/evidence is not yet bound.

### Talk track

“The agent thinks it is finished.

But the agent does not decide that the engineering process is finished.

The harness evaluates the state against the procedure.”

Show the canonical restitution:

```text
STATUS: BLOCKED
...
NEXT STEP: ...
```

Do not dive into every field.

### Executive message

> **A successful agent execution is not the same thing as an accepted engineering result.**

This is one of the most important moments of the demo.

---

## Demo step 5 — Capture verification and provenance

**Time: ~1 minute**

Complete the required evidence and create/capture the verification record.

Show that the verification record binds the result to an **exact Git commit**.

### Talk track

“Now we are doing something stronger than saying ‘the tests passed.’

The verification evidence is attached to a precise candidate state of the repository.

If the code changes afterwards, we no longer pretend that the new code is what was verified.”

### Executive message

> **SE Harness creates provenance between requirement, evidence and exact code.**

Suggested visual:

```text
Requirement
    │
    ▼
Work Order
    │
    ▼
Implementation
    │
    ▼
Verification evidence
    │
    ▼
Exact Git commit
    │
    ▼
Release decision
```

---

## Demo step 6 — Show the human decision boundary

**Time: ~1 minute**

Show the resulting state in the Harness Explorer or artifact.

Point out that the system can prepare the evidence and determine whether prerequisites are satisfied, but the accountable human still owns decisions such as authorization, acceptance or release where required.

### Talk track

“This is where I think the human role changes.

The human does not need to manually supervise every line generated by an agent.

The human owns the decisions for which the organization remains accountable.

SE Harness tries to move humans away from supervising execution and toward governing intent, risk and decisions.”

### Executive message

> **Human-in-the-loop becomes human-at-the-decision-point.**

---

# 4. Value proposition

**Duration: ~2 minutes**

After the demo, translate what was shown into executive outcomes.

Do not list 20 features.

Use four outcomes.

---

## 1. Scale agentic development without scaling chaos

Without governance, more autonomous agents can simply produce more changes, more quickly.

SE Harness gives them a bounded operating model.

> **More agent autonomy without equivalent loss of control.**

---

## 2. Make every material change explainable

For an important change, we should be able to answer:

- Why was this change made?
- Which requirement authorized it?
- What exactly was implemented?
- What verification was performed?
- Which exact commit was verified?
- Who made the accountable decision?

> **From intent to evidence to exact code.**

---

## 3. Keep governance independent from the AI provider

Models and agent products will change rapidly.

Claude today. Codex tomorrow. Something else later.

The engineering system should not have to change every time the model changes.

> **SE Harness makes the governance layer model- and agent-independent.**

---

## 4. Move humans to the right level

The goal is not to put a human approval button after every agent action.

That destroys the productivity benefit.

The goal is to distinguish between:

- execution that can be delegated;
- evidence that can be produced automatically;
- and decisions that remain accountable to humans.

> **Automate execution. Preserve accountability.**

---

# 5. Closing

**Duration: ~1 minute**

## Suggested closing

“The opportunity with coding agents is much larger than faster code generation.

We are moving toward software engineering where agents can execute a significant portion of the lifecycle.

But if we increase autonomy without redesigning control, we will simply create software faster than we can understand or govern it.

SE Harness is an attempt to solve that layer.

It makes the repository itself carry the intent, authorization, verification, provenance and decision state of the engineering process.

So the question is no longer only:

**‘Can an agent build this?’**

The question becomes:

**‘Can we let agents build at scale and still know exactly why the software exists, what was verified, and who is accountable for releasing it?’**

That is the problem SE Harness is designed to solve.”

---

# Optional 15-second final value proposition

> **SE Harness is the control plane for agentic software engineering: agents execute the work, while the repository retains the authoritative intent, constraints, evidence, provenance and human decision rights.**

Alternative, less technical:

> **SE Harness lets software teams use increasingly autonomous AI agents without losing control of what is being built, why it is being built, whether it was verified, or who is accountable for releasing it.**

---

# Demo preparation checklist

The demo should be extremely reliable. Pre-stage everything that does not create value on screen.

- [ ] Use a tiny feature or defect.
- [ ] Start with the requirement/specification/work order already prepared.
- [ ] Keep only the relevant files/windows open.
- [ ] Use one coding agent only.
- [ ] Avoid explaining source code unless asked.
- [ ] Prepare a first `harnessctl check` that intentionally blocks progress.
- [ ] Make the blocker simple enough to understand in five seconds.
- [ ] Then satisfy it and show the successful checkpoint.
- [ ] Show verification bound to an exact Git commit.
- [ ] End in the Harness Explorer or equivalent lifecycle view.
- [ ] Have a pre-recorded fallback or prepared terminal output in case the live agent behaves unpredictably.

---

# What not to demonstrate

For an executive audience, avoid spending time on:

- installation;
- TOML syntax;
- template directory structure;
- Python implementation details;
- every artifact type;
- every lifecycle status;
- how managed-file hashes work;
- detailed CLI help;
- unit test implementation;
- multi-agent architecture that SE Harness does not yet provide.

These are useful technical topics, but they dilute the executive story.

The demo should prove only this:

> **An agent can perform the work, but the engineering system remains in control.**

---

# Q&A — Likely executive pushback

## “Isn’t this just Jira plus Git plus CI/CD?”

**Answer:**

Those systems contain pieces of the information, but they do not create one authoritative engineering chain.

Jira can say what somebody planned.

Git can say what changed.

CI can say what checks ran.

SE Harness connects the engineering intent, authorization, verification evidence, exact code state and release decision in one governed model.

It complements those systems rather than necessarily replacing them.

---

## “Why not simply put this logic in the AI agent?”

**Answer:**

Because the agent should not be the authority that defines whether its own work is acceptable.

Agents and models will also change frequently.

Governance should remain independent from the model executing the work.

The agent can interpret and execute the rules; the harness owns the rules and engineering state.

---

## “Is this another process layer that will slow developers down?”

**Answer:**

It will if we expose all of its internal complexity to developers.

That would be a failure.

The objective is the opposite: encode engineering governance once so agents and automation can perform more of the process automatically.

The complexity should live inside the harness.

For a developer or agent, the experience should increasingly become:

> “Here is the authorized work. Do it. The harness tells you what is needed next.”

---

## “Why do we need this if humans still approve things?”

**Answer:**

Human approval is not the expensive part if it happens at the right level.

The expensive model is humans continuously supervising agent execution.

SE Harness is designed so agents can autonomously perform more analysis, implementation, testing and evidence collection, while humans intervene at accountable decision points.

The objective is not **human-in-every-loop**.

It is **human-at-the-right-decision-point**.

---

## “Can this really scale to thousands of developers and hundreds of repositories?”

**Answer:**

That is exactly why the governance model is repository-native and machine-readable.

But scale will depend on keeping the operating model simple and automating artifact creation and transitions heavily.

The architecture supports scale; usability and integration will determine whether that scale is achieved in practice.

---

## “Do developers really want 12 new types of documents?”

**Answer:**

They should not have to think in those terms most of the time.

The artifact model is the internal engineering structure.

If using the harness requires engineers to manually maintain 12 document types for every small change, the product has failed.

Agents and automation should generate and maintain most of that structure from normal engineering interactions.

---

## “What prevents an agent from modifying the harness rules?”

**Answer:**

The project explicitly separates the engineering work being evaluated from the released evaluator that governs acceptance.

Candidate code cannot silently redefine the rules used to accept itself.

That separation is important for any system that claims to provide meaningful assurance.

---

## “Is this a compliance product?”

**Answer:**

Not primarily.

It is an engineering governance and assurance layer.

But because it creates structured traceability, evidence and provenance, it can become extremely valuable for regulated or high-assurance environments.

Compliance becomes a strong use case of the underlying engineering model rather than the entire product definition.

---

## “Couldn’t GitHub or GitLab build this?”

**Answer:**

Yes, parts of it.

The defensible value is not a particular CLI command or dashboard.

The important asset is the engineering model and execution protocol: how intent, authorization, work, evidence, provenance and accountable decisions interact in an agentic development environment.

If that model is valuable, it can integrate with GitHub, GitLab or other platforms rather than depending on one of them.

---

## “What is the biggest risk in SE Harness?”

**Answer:**

Complexity.

The underlying governance model is powerful, but if humans have to understand all of that machinery to use the system, adoption will fail.

The priority should therefore be:

> **strong governance internally, radically simple interaction externally.**

---

## “What would success look like?”

**Answer:**

A coding agent receives an authorized unit of work, autonomously performs most of the implementation and verification process, and returns only when either:

1. it has produced sufficient evidence for the next accountable decision; or
2. it reaches a genuine decision or ambiguity that requires a human.

At that point, the organization has both higher engineering throughput and stronger traceability than it had with manual development.

---

# Recommended narrative discipline

Throughout the presentation, keep returning to three contrasts:

| Old question | Better question |
|---|---|
| Can AI generate code? | Can AI perform governed engineering work? |
| Did the tests pass? | What exact result was verified against what requirement? |
| Is a human watching the agent? | Is a human controlling the accountable decisions? |

If the audience remembers these three shifts, the presentation has worked.
