# Engineering Harness for {{PROJECT_NAME}}

This repository uses SE Harness {{HARNESS_VERSION}}.

The keywords **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and
**OPTIONAL** in this document are to be interpreted as described in BCP 14
(RFC 2119 and RFC 8174) when, and only when, they appear in all capitals.

## Goals

This harness makes engineering authority explicit, limits execution to approved
scope, binds assurance and release claims to exact evidence, and gives every
actor the same deterministic next step. These goals are informative; the rules
below and the installed evaluator's machine policy are normative.

## Policy / Global invariants

### HRN-001 — Formal authority

Formal artifacts under `docs/engineering/` are the authoritative
records of product intent, requirements, architecture decisions, work authority,
verification contracts, risks, assurance decisions, and release decisions. Code,
tests, commits, tickets, dashboards, and conversation text are evidence or
observations; they MUST NOT substitute for formal authority.

### HRN-002 — Change control

Formal artifacts MAY be drafted, reviewed, and validated before a work order
is approved. This preparation MUST NOT authorize implementation.

Accepted formal artifacts MUST define the change before implementation starts.
One or more approved work orders MUST authorize implementation. A valid
repository-owned exception MAY remove the requirement for formal definitions,
work orders, or both. It MUST NOT change lifecycle rules or waive required gates.

Any required work orders MUST pass the required validation checks before
implementation starts. The result MUST be verified against the accepted
definitions that apply. All required verification checks remain required.

### HRN-003 — Lifecycle authority

Artifacts and the work itself MUST follow a strict lifecycle.
`harnessctl` MUST be the only source of truth for lifecycle states, allowed
state changes and the next action. Actors MUST use its results when reporting
or taking lifecycle actions. Agent text, prompts, Skills, dashboards, and
repository notes MUST NOT work out their own answers or change those results.

### HRN-004 — Bounded scope

An actor MUST select one clearly defined set of artifacts before
acting. This set defines the scope. Findings from unrelated work orders MUST
NOT be presented as findings about the selected scope. An issue outside the
scope MAY be reported only as an observation that has not been assessed, with
its artifact ID. It MUST NOT block the selected work unless a recorded
dependency or gate connects it to that work.

### HRN-005 — Explicit decisions

Each decision MUST identify the accountable human or agent and the authority
used. Being a human or an agent does not by itself authorize an action.

Preparing, inspecting, validating, or collecting evidence MUST NOT
count as an authorized decision. A state change requires the exact artifact,
the intended state, and the accountable actor. The required gates MUST pass,
and an explicit state transition MUST be applied.

### HRN-006 — Targeted transitions

A state transition MUST change only the artifacts explicitly
selected by the accountable actor. The states of related artifacts MUST NOT
change just because they are linked.

### HRN-007 — Repository ownership

`AGENTS.md` MUST belong entirely to the repository owner and contain
no harness instructions. Repository-specific facts and commands belong in
that file. The harness MUST NOT generate, track, or require that owner content.

### HRN-008 — Rule precedence

Repository instructions MAY add stricter rules. They MUST NOT grant authority
for product, engineering, assurance, release, or external actions. They MUST
NOT remove, weaken, or contradict the harness rules.

Repository owners MAY define exceptions through the supported exception
capability described in [EXCEPTIONS.md](docs/engineering/harness/EXCEPTIONS.md#availability). This changes only the obligations the capability permits
them to configure: whether formal definitions and work orders are required.
Lifecycle rules and required gates remain fixed. Repository prose alone MUST
NOT waive a harness rule.

### HRN-009 — Required checks

Managed-file integrity checks, artifact graph checks, scope checks, and required
gates MUST all pass before the affected action can proceed. Warnings MUST NOT
count as approval or acceptance of a risk.

## Scope of these rules

The bounded-scope, lifecycle-reporting, and stop rules apply when a human or
agent performs or reports a governed lifecycle action. Reading, analysis, and
answering questions need no work order when they change no lifecycle state,
exercise no decision right, and present no finding as a formal verdict.

Preparing a proposed artifact package does not require an approved work
order. A human or agent MAY create and edit drafts, record risks and open
questions, review the proposed content, and validate the package. These
actions MUST follow the authoring procedure and required checks. They MUST
NOT change an accepted definition, approve a work order, or start
implementation. Decisions and lifecycle transitions follow their separate
authority rules.

Before a lifecycle action, select the exact artifacts and read the governing
files returned by the evaluator. A checkpoint-free `check` reports lifecycle
context. It does not evaluate checkpoint gates or authorize work.

## Using these instructions

A human is a person; an agent is an automated system acting under granted
authority. Approval, verification acceptance and release decisions require an
authorized human. Agents may apply a matching recorded decision. Resolve the
identity and right in [AUTHORITY.md](docs/engineering/harness/AUTHORITY.md#decision-rights)
before obtaining or applying a decision.

`harnessctl` means this repository's selected released evaluator, invoked through
its absolute Python path with `-I -m se_harness`, from outside the checkout.
`REPO` is the absolute repository path. Replace uppercase placeholders with actual
inputs. Keep each `ID=value` assignment as one argument. If the executable or
identity is unknown, use [SETUP.md](docs/engineering/harness/SETUP.md#procedure).

Transient working material stays in the conversation or temporary storage outside
the repository, at the agent's discretion. It has no formal authority and SHALL
NOT be persisted in the repository. This rule covers working notes, not formal
artifacts or evidence required at a contract's prescribed durable location.

## Read by task

Read the selected file's entry conditions and current step. Read its required
references before the action they govern. A link alone does not require reading
its target. Do not load all procedures or future stages in advance.

| Current need | Read first |
| --- | --- |
| Discuss or explain without a lifecycle action | Only the source sections needed to answer. |
| Define a new change | [DEFINE_CHANGE.md](docs/engineering/harness/DEFINE_CHANGE.md#read-this-when) |
| Continue selected work or recover after compaction | [CONTINUE.md](docs/engineering/harness/CONTINUE.md#read-this-when) |
| Resolve decision authority | [AUTHORITY.md](docs/engineering/harness/AUTHORITY.md#decision-rights) |
| Report a lifecycle result, failed check or uncertain write | [RESULTS.md](docs/engineering/harness/RESULTS.md#read-this-when) |
| Assess an owner-defined exception | [EXCEPTIONS.md](docs/engineering/harness/EXCEPTIONS.md#availability) |
| Prepare or repair the evaluator | [SETUP.md](docs/engineering/harness/SETUP.md#read-this-when) |

Before the first eligible English explanation in a fresh context, read
[COMMUNICATION.md](docs/engineering/harness/COMMUNICATION.md#communication).
Reuse it while retained in context. This applies to ordinary answers too.
Machine WORKFLOW.json and QUALITY_GATES.json are evaluator inputs; read them only
when changing or investigating their contracts. Use evaluator results in normal
work. Missing instructions or an unknown returned procedure stop the affected
action: report the exact discovery gap in RESULTS.md.

## After compaction

Recover the repository, selected IDs, objective, existing authority and pending
action from the summary. For governed work, obtain fresh context through
CONTINUE.md and reread the current procedure and prerequisites lost from context.
A summary preserves pointers and decisions, not current lifecycle truth. Inspect
uncertain writes or external effects before retrying. Resume only unapplied work.
