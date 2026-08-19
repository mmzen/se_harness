# SE Harness

## Governed Agentic Software Engineering

> **Autonomy for agents. Authority for humans.**

## The Shift

Software development is moving rapidly from engineers **writing code with AI assistance** to engineers **directing autonomous coding agents**.

Frontier models can increasingly:

* explore large codebases;
* understand existing implementations;
* decompose engineering work;
* modify multiple files;
* implement features and bug fixes;
* generate and execute tests;
* review changes;
* analyze failures;
* gather engineering evidence;
* and work autonomously for extended periods.

The bottleneck is therefore moving.

```text
Yesterday:
Human engineering capacity → coding capacity

Tomorrow:
Human engineering capacity → decision and supervision capacity
```

If every meaningful action performed by an agent must still be manually supervised, reviewed and reconstructed by a human, much of the potential of autonomous software engineering disappears.

The challenge is no longer simply:

> How can AI generate more code?

It becomes:

> **How can we give software-engineering agents meaningful autonomy without losing control, engineering rigor or human accountability?**

---

# The Problem

Increasing agent autonomy creates an uncomfortable trade-off.

```text
MORE AGENT AUTONOMY
        │
        ├── faster engineering
        ├── greater parallelism
        ├── higher development capacity
        │
        └── but potentially:
              unclear intent
              uncontrolled changes
              lost architectural rationale
              weak traceability
              unverifiable decisions
              uncertain test coverage
              ambiguous responsibility
              unclear release authority
```

The natural organizational reaction is to keep humans constantly in the loop:

```text
Agent proposes
      ↓
Human reviews
      ↓
Agent implements
      ↓
Human reviews
      ↓
Agent tests
      ↓
Human reviews
      ↓
Human releases
```

This is safe, but it does not scale.

As one engineer begins operating five, ten or twenty agents simultaneously, **human supervision itself becomes the constraint**.

A different operating model is required.

---

# The SE Harness Proposition

**SE Harness is a repository-native governance layer for agentic software engineering.**

It allows coding agents to operate autonomously within explicit engineering boundaries while humans retain authority over the decisions that carry accountability.

SE Harness connects:

```text
Intent
  ↓
Capabilities
  ↓
Requirements
  ↓
Specifications
  ↓
Architecture
  ↓
Verification expectations
  ↓
Authorized work
  ↓
Agent execution
  ↓
Implementation
  ↓
Evidence
  ↓
Exact Git commit
  ↓
Verification decision
  ↓
Release decision
  ↓
Operational assurance
```

The objective is simple:

> **Make every material software change explainable from human intent to engineering evidence and exact executable code.**

---

# Core Value Proposition

## Autonomy for agents. Authority for humans.

SE Harness separates two concepts that traditional software-engineering processes often mix together:

### Execution

Execution can increasingly be delegated to agents.

Agents can:

* inspect the repository;
* analyze requirements and specifications;
* propose implementation approaches;
* implement authorized changes;
* write and execute tests;
* analyze defects;
* inspect architecture;
* gather verification evidence;
* prepare engineering records;
* review other changes;
* and perform substantial work autonomously.

### Authority

Authority remains explicitly assigned to accountable humans.

Humans decide:

* **why** something should exist;
* **what** outcome is required;
* which requirements become authoritative;
* which architectural risks are acceptable;
* what work agents are authorized to perform;
* what evidence is sufficient;
* whether exceptions are acceptable;
* whether a candidate is releasable;
* and whether operational risk can be accepted.

SE Harness provides the control layer between these two worlds.

```text
                         HUMAN
                  accountable authority
                         │
            What / Why / Risk / Release
                         │
                         ▼
              ┌─────────────────────┐
              │      SE HARNESS     │
              │                     │
              │ intent              │
              │ requirements        │
              │ specifications      │
              │ architecture        │
              │ authorized work     │
              │ constraints         │
              │ verification        │
              │ evidence            │
              │ provenance          │
              │ release gates       │
              └──────────┬──────────┘
                         │
                  bounded autonomy
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
          Codex        Claude       Future
          agents       agents       agents
            │            │            │
            └────────────┼────────────┘
                         │
                         ▼
              implementation + evidence
```

---

# Human Authority Boundaries

The objective is **not** to keep a human involved in every agent operation.

"Human in the loop" is too simplistic for large-scale agentic engineering.

The scalable model is:

> **Humans sit at authority boundaries, not inside every execution loop.**

| Engineering stage | Agent / automation                               | Human authority                                  |
| ----------------- | ------------------------------------------------ | ------------------------------------------------ |
| Intent            | Explore, challenge, structure, draft             | Own desired outcome                              |
| Requirements      | Derive, analyze, identify gaps                   | Approve authoritative obligations                |
| Specification     | Draft, refine, detect inconsistencies            | Own material engineering contracts               |
| Architecture      | Analyze alternatives, draft decisions            | Accept architectural decisions and risk          |
| Work planning     | Decompose work and propose execution plans       | Authorize bounded work                           |
| Implementation    | Execute autonomously within authorization        | Handle exceptions and escalations                |
| Testing           | Generate, execute and analyze tests              | Define required assurance where judgment matters |
| Verification      | Gather evidence and prepare verification records | Decide whether evidence is sufficient            |
| Release           | Prepare release evidence and candidate records   | Authorize promotion                              |
| Operations        | Observe, diagnose and recommend                  | Accept operational risk and accountability       |

The human therefore changes role.

```text
Traditional model

Human = engineer performing execution
AI    = assistant
```

becomes:

```text
Agentic model

Human      = intent + judgment + authority
AI agents  = engineering execution
SE Harness = control + state + evidence + provenance
```

---

# Repository as the Engineering System of Record

Long-running agents cannot depend primarily on conversational memory.

An agent may run for hours and disappear.

Another agent may continue the work tomorrow.

A third agent may verify it.

A fourth may challenge the implementation.

The durable engineering state must therefore live outside the agents themselves.

SE Harness makes the repository the engineering system of record.

```text
intent/
requirements/
specifications/
architecture/
work/
verification/
evidence/
decisions/
release/
```

Agents are therefore **disposable execution capacity**.

Engineering state is persistent.

This gives the system a critical property:

> **Persistent engineering state. Replaceable agents.**

An agent does not need to remember what another agent discussed eight hours earlier.

It can reconstruct the relevant engineering context from authoritative artifacts, Git history, evidence and explicit work authorization.

---

# Bounded Agent Autonomy

SE Harness does not attempt to make autonomous agents safe by restricting them to trivial tasks.

Instead, it defines **bounded autonomy**.

An agent receives:

```text
Authorized Work
      │
      ├── applicable intent
      ├── requirements
      ├── specifications
      ├── architecture
      ├── constraints
      ├── acceptance criteria
      ├── verification expectations
      └── permitted scope
```

Inside those boundaries, the agent can operate with substantial autonomy.

```text
                AUTHORIZED BOUNDARY
        ┌──────────────────────────────┐
        │                              │
        │      Autonomous Agent        │
        │                              │
        │ explore                      │
        │ reason                       │
        │ implement                    │
        │ refactor                     │
        │ test                         │
        │ inspect failures             │
        │ gather evidence              │
        │ prepare verification         │
        │                              │
        └──────────────────────────────┘
                         │
                         ▼
                evidence + code
```

When the agent encounters something outside the authorized boundary, it does not silently expand its own authority.

It escalates.

This is the difference between:

> autonomous coding

and:

> **governed autonomous engineering.**

---

# End-to-End Engineering Traceability

A conventional coding agent often operates approximately like this:

```text
Prompt
  ↓
Repository
  ↓
Code
  ↓
Tests
```

SE Harness introduces an explicit engineering chain:

```text
Human Intent
     ↓
Capability
     ↓
Requirements
     ↓
Specification
     ↓
Architecture
     ↓
Verification Contract
     ↓
Authorized Work
     ↓
Agent Execution
     ↓
Implementation
     ↓
Evidence
     ↓
Exact Git Commit
     ↓
Verification Decision
     ↓
Release Decision
```

This makes it possible to answer fundamental engineering questions:

* Why does this code exist?
* Which requirement required the change?
* Who authorized the work?
* Which specification governed the implementation?
* Which architectural decision applies?
* Which agent or engineer performed the work?
* What evidence demonstrates that the requirement is satisfied?
* Which tests were executed?
* What exact Git commit was verified?
* What exact software candidate was authorized for release?
* Who accepted the remaining risk?

These questions become increasingly important as the amount of software directly written by humans decreases.

---

# Evidence Instead of Trust

Agent-generated output should not be trusted because the agent says the work is complete.

The engineering system should require evidence.

```text
Agent statement:

"I implemented the requirement and all tests pass."

                    ≠

Engineering evidence:

Requirement REQ-042
        ↓
Work Order WO-017
        ↓
Commit 5c71f4...
        ↓
Tests executed
        ↓
Results retained
        ↓
Verification record
        ↓
Human assurance decision
```

The harness therefore distinguishes between:

* execution;
* claims;
* evidence;
* verification;
* authorization.

That separation becomes fundamental when autonomous agents execute increasingly large portions of the software lifecycle.

---

# Multi-Agent Engineering

SE Harness is designed for an environment where multiple specialized agents may collaborate on the same product.

For example:

```text
                         ORCHESTRATOR
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
       REQUIREMENTS       IMPLEMENTER       VERIFIER
       / ARCHITECT            │                │
             │                │                │
             └────────────┐   │   ┌────────────┘
                          ▼   ▼   ▼
                           REVIEWER
                              │
                              ▼
                        RELEASE AGENT
```

The key design principle is that coordination should not depend primarily on agents talking indefinitely to each other.

Instead, agents collaborate through durable engineering state:

```text
Agent A
   │
   └── specification / ADR
               │
               ▼
           repository
               │
               ▼
Agent B ── implementation + evidence
               │
               ▼
           repository
               │
               ▼
Agent C ── independent verification
```

Agent conversations can help execution.

They should not become the authoritative engineering record.

---

# Why This Matters

The software-engineering industry is rapidly commoditizing code generation.

The differentiating question will increasingly become:

> **How much engineering autonomy can an organization safely give to AI?**

Without governance, organizations face two bad choices.

### Option 1 — Restrict autonomy

```text
AI
 ↓
human approval
 ↓
AI
 ↓
human approval
 ↓
AI
 ↓
human approval
```

Safe, but human throughput remains the constraint.

### Option 2 — Allow uncontrolled autonomy

```text
AI agents
 ↓
massive execution capacity
 ↓
unclear decisions
unclear provenance
unclear assurance
unclear accountability
```

Fast, but increasingly unsafe.

SE Harness proposes a third model.

## Governed autonomy

```text
                 GOVERNED AUTONOMY

Human defines                   Agents execute
the boundaries                  inside boundaries

          └──────── SE Harness ────────┘
```

The objective is not to minimize human involvement.

It is to use human judgment **where human accountability actually matters**.

---

# Strategic Positioning

SE Harness should not primarily be positioned as:

> A better development process.

Nor simply as:

> A traceability system.

Nor as:

> Another AI coding platform.

Those markets either undersell the idea or are rapidly becoming commoditized.

The stronger positioning is:

> **SE Harness is the infrastructure that allows organizations to safely increase the autonomy of software-engineering agents.**

The underlying coding agent becomes replaceable.

Today it may be Codex.

Tomorrow Claude Code.

Later it may be another agent runtime entirely.

```text
                   SE HARNESS
                       │
       ┌───────────────┼───────────────┐
       │               │               │
       ▼               ▼               ▼
     Codex          Claude Code       Other
       │               │               │
       └───────────────┼───────────────┘
                       │
                       ▼
               software repository
```

The durable value is above the model:

* engineering intent;
* authoritative requirements;
* architecture;
* constraints;
* authorization;
* provenance;
* verification;
* evidence;
* decision rights;
* and release authority.

Models change.

Agents change.

The engineering governance system remains.

---

# Product Positioning

## Category

**Repository-native governance layer for agentic software engineering.**

A more ambitious category definition is:

**Agentic Software Engineering Control Plane.**

The second positioning becomes increasingly appropriate as the harness expands into:

* multi-agent coordination;
* policy enforcement;
* authorization;
* independent verification;
* concurrency control;
* enterprise governance;
* assurance;
* and release management.

---

# Core Message

> **SE Harness turns autonomous coding agents into accountable software engineering.**

It enables agents to execute substantial engineering work independently while preserving explicit human control over intent, engineering decisions, risk, verification and release.

---

# Short Value Proposition

> **SE Harness gives coding agents the autonomy to build software while keeping engineering authority with humans. It connects human-approved intent and requirements to agent execution, verification evidence and exact Git commits, making autonomous software engineering controlled, traceable and accountable.**

---

# Executive Pitch

Software development is moving from humans writing code with AI assistance to humans directing autonomous engineering agents.

The opportunity is enormous, but so is the governance problem: when an agent can perform hours or days of engineering work autonomously, organizations need to know what authorized the work, which requirements governed it, what changed, how it was verified and exactly what software they are releasing.

**SE Harness is a repository-native governance layer for agentic software engineering.**

It lets agents autonomously explore, implement, test and gather evidence inside explicit engineering boundaries, while humans retain authority over intent, architecture, risk, verification and release.

Every material change remains connected from intent and requirements through authorized work and evidence to an exact Git commit.

**The result is not simply faster code generation. It is governed engineering at agent speed.**

---

# 15-Second Pitch

> **SE Harness lets autonomous coding agents build software without giving them engineering authority. It connects every change from human-approved intent and requirements through implementation and verification to exact code, allowing agents to operate autonomously while humans retain accountability for risk and release.**

---

# One-Liners

**Primary**

> **SE Harness turns autonomous coding agents into accountable software engineering.**

**Alternative**

> **Autonomy for agents. Authority for humans.**

**Alternative**

> **Governed engineering at agent speed.**

**Alternative**

> **Delegate execution. Keep accountability.**

---

# Vision

As coding agents become capable of executing increasingly complex engineering work, the competitive advantage will no longer come simply from having access to the best model.

It will come from an organization's ability to **delegate more engineering execution safely**.

```text
Frontier models
      ↓
More capable agents
      ↓
More autonomous execution
      ↓
Human supervision becomes the bottleneck
      ↓
Governed delegation becomes necessary
      ↓
SE Harness
```

The long-term proposition is therefore larger than development-process automation.

> **SE Harness provides the engineering control system required for a world in which most software execution is performed by autonomous agents but engineering accountability remains human.**
