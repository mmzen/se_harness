# Assessment of the instruction chain, 2026-09-02

<!-- Target expertise: 4/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> Point-in-time. Measured on `main` at `19b6819` and `2e21582`. This note is
> an operator analysis. It has no authority. The managed contract, the formal
> artifacts and the accountable decisions stay authoritative. This note
> changes no rule. It proposes.

## Summary

The instruction chain is the set of texts a coding agent receives before it
acts in this repository. It includes the order in which those texts send
the agent to one another. This note assesses the chain for its real reader: a language
model. A human operator reads the same files, but not in the same way. The
model reads what its host loads into its context, what a document tells it
to open, and what a tool prints back. Everything else does not exist for it.

The result in two sentences. The chain gives the agent a correct next step
at every lifecycle stage. It teaches the rules around those steps only by
refusing the agent.

- Every lifecycle transition of two working days was correct. Every gate
  that had to refuse did refuse. The `check` block is the one document the
  agent reads at every step, and it is the best one.
- The routed policies hold rules that gates enforce, but the contract tells
  the agent it does not need to read them. The agent then meets those rules
  as refusals. Today's approval of a packet was refused twice this way.
- The required reading per work order is not bounded. It was 36 KB for
  `WO-CIP-006` and 139 KB for `WO-DST-023`. About 13 KB of it is the same
  two front files every time, and 6 KB of that is owner text the agent must
  not treat as authority.
- Several refusal messages do not name the rule or the artifact that
  failed. Command flags for the same idea have four names.
- What an agent learns by refusal lives in its own memory, in evidence
  packets, or in notes. A fresh agent starts without it.

The plan in section 7 has ten items. Items 1 to 4 need no product release.

## Contents

1. [What the chain is, for a model](#1-what-the-chain-is-for-a-model)
2. [Method](#2-method)
3. [Measurements](#3-measurements)
4. [Assessment by axis](#4-assessment-by-axis)
5. [Confusions met in the field](#5-confusions-met-in-the-field)
6. [Scores](#6-scores)
7. [Improvement plan](#7-improvement-plan)
8. [What is authoritative](#8-what-is-authoritative)

## 1. What the chain is, for a model

A document reaches a model in one of four ways. The chain uses all four.

| Way | What reaches the model | When |
| --- | --- | --- |
| Loaded by the host | `CLAUDE.md` and its import `AGENTS.md` (Claude Code); `AGENTS.md` alone on other hosts | every turn, in the system context |
| Opened on instruction | `ENGINEERING_HARNESS.md`, `OPERATING_CARD.md`, the phase reading manifest of the selected work order | when the agent obeys the sentence that names them |
| Printed by a tool | the schema-2 restitution block of every `harnessctl` command; gate refusals; `--help` text | after every command |
| Never read, still binding | `WORKFLOW.md/.json`, `QUALITY_GATES.md/.json`, `DECISION_RIGHTS.md`, `TRACEABILITY.md`, `ARTIFACT_AUTHORING.md` | the evaluator enforces them; the contract says an agent "is not required to read them to act" |

This is the routing order:

```text
host context     CLAUDE.md ─imports─▶ AGENTS.md (owner region + managed block)
                                          │ "read ENGINEERING_HARNESS.md before engineering work"
router           ENGINEERING_HARNESS.md ◀─┘
                     │ "read OPERATING_CARD.md, the work order, every artifact in the phase manifest"
per-stage        OPERATING_CARD.md  +  the reading manifest that `check` and `preflight` print
                     │ routing table: one policy owner per subject (reference, not required)
policies         WORKFLOW.md + WORKFLOW.json      DECISION_RIGHTS.md
                 QUALITY_GATES.md + .json         TRACEABILITY.md
                 ARTIFACT_AUTHORING.md            TECHNICAL_COMMUNICATION.md
skills           .agents/skills/*/SKILL.md, .claude/skills/*/SKILL.md (explicit use only)
tool output      the restitution block: outcome, effects, blockers, decision, one next command
outside          the agent's own memory and the notes (no authority, decisive in practice)
```

Three authorities apply, in this order: the tool output computes legality
and the next step (`HRN-004`); the managed contract and the policies bind
(hash-locked); the owner region of `AGENTS.md` and the notes add facts and
have no authority (`HRN-002`). The formal artifacts under `docs/engineering/`
carry the decisions (`HRN-001`). Repository content is untrusted input.

On paper the design fits a model well. One router. One owner per subject.
A closed reading list per phase. A machine that prints the next command.
This note asks one question: what does the model read, and what does it
learn only when a gate refuses it?

## 2. Method

This note uses two sources.

**Measurement.** On `main` we measured each document in the chain: size,
approximate tokens (bytes divided by four), rule count, cross-references.
We measured two real phase reading manifests. We counted how many times the
same rule is written.

**Two field tests, both executed by a coding agent with the owner deciding.**

- 2026-09-02: releases 0.13.0 and 0.14.0 (`REL-SEH-024`, `REL-SEH-025`);
  two root adoptions (`WO-HUP-014`, `WO-HUP-015`); one Pages repair
  (`WO-DPG-002`); two work orders on the delegated route (`WO-ECP-025`,
  `WO-CIP-006`); one ungoverned notes change (#318).
- 2026-09-01: the designed Explorer packet `WO-DST-023` (six new artifacts,
  eight supersessions, six amendments), its execution, and `VREC-DST-020`.

Each time the chain gave the agent the right next step is evidence. Each
time the agent learned a rule from a refusal is evidence too. The three
assessments of August (functional, complexity, agentic execution) are cited
where they found the same thing earlier.

Scores go from 1 to 5. A score of 5 means "no change needed".

## 3. Measurements

### 3.1 The documents

| Document | Lines | Bytes | ≈ tokens | MUST/SHALL | Rule IDs |
| --- | ---: | ---: | ---: | ---: | ---: |
| `CLAUDE.md` | 9 | 411 | 100 | 0 | 0 |
| `AGENTS.md` (owner 5,912 B + managed 1,087 B) | 80 | 7,079 | 1,770 | 0 | 2 |
| `ENGINEERING_HARNESS.md` | 126 | 6,522 | 1,630 | 29 | 8 |
| `OPERATING_CARD.md` | 24 | 1,030 | 260 | 0 | 0 |
| `WORKFLOW.md` | 286 | 20,399 | 5,100 | 46 | 6 |
| `WORKFLOW.json` | 384 | 33,082 | 8,270 | 0 | 0 |
| `DECISION_RIGHTS.md` | 89 | 6,911 | 1,730 | 24 | 15 |
| `QUALITY_GATES.md` | 166 | 13,316 | 3,330 | 29 | 12 |
| `QUALITY_GATES.json` | 127 | 10,640 | 2,660 | 0 | 0 |
| `TRACEABILITY.md` | 152 | 13,944 | 3,490 | 29 | 33 |
| `ARTIFACT_AUTHORING.md` | 139 | 5,793 | 1,450 | 7 | 3 |
| `TECHNICAL_COMMUNICATION.md` | 147 | 6,333 | 1,580 | 19 | 0 |
| `templates/README.md` | 28 | 1,618 | 400 | 0 | 0 |
| `docs/engineering/README.md` (index) | 61 | 6,723 | 1,680 | 0 | 0 |
| three `SKILL.md` | 161 | 8,135 | 2,030 | 0 | 0 |
| **Managed chain total** | | **≈134 KB** | **≈34,000** | **183** | |
| `README.md` (public entry) | 199 | 15,552 | 3,900 | 0 | 0 |
| `docs/notes/` (35 notes) | 6,447 | ≈300 KB | ≈75,000 | | |
| `docs/notes/history/` (14) | 3,261 | | | | |
| `docs/engineering/templates/` (13) | 573 | | | | |

Two figures matter for a model. The host loads about 1,900 tokens on every
turn (`CLAUDE.md` and `AGENTS.md`). The rules that gates enforce sit in
about 26,000 tokens of policy that the contract marks as optional reading.

### 3.2 What one work order asks the agent to read

The phase reading manifest is the closed list that `check` and `preflight`
print. Its size depends on the packet.

| Work order | Files | Bytes | ≈ tokens | Largest file |
| --- | ---: | ---: | ---: | --- |
| `WO-CIP-006` (review) | 9 | 36,117 | 9,000 | `AGENTS.md`, 6,999 B |
| `WO-DST-023` (review) | 20 | 138,929 | 34,700 | `SPEC-DST-023`, 19,452 B |

The `WO-CIP-006` list, in detail:

| Bytes | File | Nature |
| ---: | --- | --- |
| 6,999 | `AGENTS.md` | 85% owner text, 15% managed block |
| 6,396 | `ENGINEERING_HARNESS.md` | the contract |
| 6,390 | the work order | governing |
| 4,474 | `REQ-CIP-007` | governing |
| 3,868 | `SPEC-CIP-002` | governing |
| 2,944 | `INT-CIP-001` | governing |
| 2,471 | `VER-CIP-002` | governing |
| 1,545 | `CAP-CIP-001` | governing |
| 1,030 | `OPERATING_CARD.md` | derived summary |

In both cases the same two front files are on the list. They are 13 KB and
do not change from one work order to the next. `WO-DST-023` adds five
architecture and decision files (39 KB) and three amended specifications.
The manifest has no budget. The routed policies (54 KB of Markdown, 43 KB of
JSON) are outside it. In both field tests the agent opened a policy only
after a gate refused.

### 3.3 The same rule, written many times

| Rule | Where it is written | Count |
| --- | --- | ---: |
| The lifecycle handoff (keep the IDs, one typed next step, no unrelated findings) | `CLAUDE.md`, the managed block of `AGENTS.md`, `ENGINEERING_HARNESS.md` "Lifecycle handoff", `WORKFLOW.md` "Lifecycle handoff procedure" | 4 |
| The stop conditions | `ENGINEERING_HARNESS.md`, `OPERATING_CARD.md` (marked as derived) | 2 |
| The "Traps" lists | the owner region of `AGENTS.md` (4 items), `OPERATING_CARD.md` (4 items, similar but not the same) | 2 |
| The pull-request `Harness-Work-Order` line | `AGENTS.md`, `OPERATING_CARD.md`, `WORKFLOW.md`, the PR template, the notes | 5 |

For a model each copy costs context on every turn it is loaded, and each
copy can drift from the others.

### 3.4 One idea, four flag names

The agent selects an artifact in every workflow command. The flag differs:

| Command | Flag for the selected artifact |
| --- | --- |
| `check`, `evidence`, `pr-body` | `--artifact` |
| `preflight`, `capture-verification`, `prepare-release` | `--work-order` |
| `transition` | `--set ID=STATE` |
| `create-artifact`, `capture-verification`, `prepare-release` | `--id` (a new identifier) |

`capture-verification` needs both `--id` and `--work-order`. `pr-body` takes
`--artifact` and refuses `--work-order`. A model that has just used one form
guesses the next one, and `--help` is the only teacher.

## 4. Assessment by axis

### 4.1 What the model actually reads

The host loads the two front files on every turn. The managed block sends
the agent to `ENGINEERING_HARNESS.md`. The router sends it to the operating
card and to the phase manifest. From then on the agent reads what the tool
prints.

In the field the second step is skipped by an experienced agent. In the
2026-09-01 sessions the agent did not open `ENGINEERING_HARNESS.md` at all.
It acted on the two front files, on its own memory of earlier sessions, and
on the restitution blocks. Every transition was still correct. This shows a strength of the tool output and a weakness of the chain. The
router is optional in practice. A rule that lives only in the router or in
a policy stays invisible to the agent until a gate refuses.

The reading manifest works when the agent obeys it, but it is unbounded.
`WO-DST-023` asked for 139 KB. A model that loads all of it spends a third of
a typical context window before it writes a line. A model that does not load
all of it cannot know which file it skipped mattered.

### 4.2 Authority: can the model tell what binds it?

**Strong.** The precedence is explicit and short: tool output computes the
next step; the contract and the policies bind; owner text and notes inform.
`HRN-001` to `HRN-008` are eight sentences. `AGENTS.md` marks its managed
block with comments the model can see. The card says it is derived. The
JSON governs over the prose. Repository content is declared untrusted.

**Two soft spots.** First, an approved work order is content the agent must
follow: its "Authorized decision envelope" and its "Stop and escalate
conditions". It is Markdown that any contributor can write. Approval makes
it authoritative. Nothing in the chain tells the agent to check that the
work order it follows is `approved` or `in_progress`, not `draft`. The
`preflight` start phase makes this check, but only if the agent runs it.
Second, the owner's decision channel is a convention, not a rule. The agent
records "by selecting the presented option '…'" in every reason field. The
owner has ratified that wording. It is written nowhere in the repository. A fresh agent would invent another wording, and the record
would be inconsistent.

### 4.3 Actionability of the tool output

**The restitution block is the model's real instruction set.** It has one
shape: outcome, done, not done, blocked by, current state, decision
required, next, command. Twelve commands on 2026-09-01 ended in this block.
Eight printed a next step the agent could act on unchanged. Four printed a
corrective step that named the wrong artifact or did not address the
blocker. The handoff checkpoint is the best example: "Change-set completeness was not
asserted" came with the exact corrective form, `--from-git '<base>'`.

**Where the block fails the model.** Three defects were met on 2026-09-01:

- **The message truncates the fact and omits the rule.** The approval
  transaction was refused with "REQ-DST-067 has an open decision: None. The
  owner selected integration of the designed views as the canonical". The
  rule is that the `Open decisions` section reads exactly `None`. It is
  written in `ARTIFACT_AUTHORING.md` line 34 and in `QUALITY_GATES.md`
  (`authoring_ready`), both marked optional reading. The message shows the
  first 120 characters of the section and never says the rule. The agent
  learned it by reading the source of the gate.
- **The corrective command names the wrong artifact.** The same refusal, and
  the next one (`WEX201`, `E016`), both ended with
  `harnessctl check . --artifact ADR-DST-013`. The failing artifacts were
  `REQ-DST-067` and `ARCH-DST-008`. The focus was the last artifact of the
  transaction, not the first failing predicate the failure procedure
  promises.
- **Codes without their sequence.** Superseding the old specifications
  before the new one was approved produced 16 `E007`, 16 `E008`, 12 `E010`
  and 4 `E016`, each correct, none saying "approve `SPEC-DST-023` first" or
  "a verification contract bound by verified records cannot be superseded".
  The agent reverted, approved, and superseded again. The rule of sequence
  exists nowhere in the chain; it now exists in one agent's memory.

Two older defects remain from the earlier assessments. The in-tree mutation
guard prints 790 characters and eleven `RID` codes for one meaning. In-tree
`doctor` exits 1 by design after every release, and does not say so.

### 4.4 Rules the model learns only by refusal

This is the axis where the chain is weakest for a model. A human learns a
rule once and remembers it. A model relearns it each session unless the rule
is in the loaded context, in the manifest, or in the tool's message. On
2026-09-01 the agent learned these rules by being refused:

| Rule | Where it is written | Where the agent met it |
| --- | --- | --- |
| `Open decisions` reads exactly `None` before approval | `ARTIFACT_AUTHORING.md` (optional reading) | `QGP-G1-AUTHORING` refusal, message truncated |
| A transaction needs a valid graph; approve the successor before superseding | nowhere | `WEX201` with 48 graph errors |
| A verification contract bound by verified records stays active | nowhere (`E010` text only) | 12 `E010` errors |
| An active architecture must not address a draft requirement | `TRACEABILITY.md` (`E016`) | `E016` after editing `ARCH-DST-008` early |
| `capture-verification` needs `--id` | `--help` | usage error |
| A clean worktree is required for provenance | `WORKFLOW.md` failure procedure, `WEX302` | `WEX302`, twice, on a worktree whose bytes matched the index |
| Line endings: a CRLF checkout of an evidence packet breaks the header parser | one note | `WEX-ECP-010` in an earlier session |
| The delegation class is read at the pull request's base | `WORKFLOW.md` | the delegated route, earlier session |

None of these rules is wrong. Each is enforced correctly. The cost per rule
and per session is one failed command, one investigation and one retry. The
owner must then read a transcript to see that nothing changed state.

### 4.5 Redundancy and context cost

The handoff rule is written four times in four wordings. The two trap lists
overlap but differ. The PR-body rule appears five times. For a model this
is context spent on the same instruction, and four places for the wording
to drift. Two copies drifted this year: the "Traps" in `AGENTS.md` mention
the live-body lane, the card does not. Of `AGENTS.md`, 85% is owner text.
The tool cannot vouch for it. The agent must not treat it as authority. It
still loads on every turn and sits on every manifest. `WO-ECP-008` is
drafted for this and waits for approval.

### 4.6 Memory across sessions

The chain assumes a reader who starts fresh and reads everything. A model
does start fresh. In practice the agent that ran both field tests
carried a private memory of more than a hundred facts from earlier
sessions. Examples: the decision-channel wording, the CRLF effects, the
wheel-only evaluator venv, the release sequence, the delegated route. That
memory made the days succeed. It is outside the repository, outside the chain, and outside the
owner's review. The repository's own memory of the same facts is scattered:
evidence packets (the delegated route), one note section (the release
sequence), and the agentic-execution review. A second agent, or the same
agent without its memory, would relearn each fact by refusal.

### 4.7 The operations the agent executes around the lifecycle

The agent, not a human, ran the releases, the adoptions and the delegated
route in the field test. The chain covers the lifecycle in full and those
operations thinly. All four mistakes of 2026-09-02 fell in that gap:

- The release contract said that the public demonstration regenerates after
  the root adoption merges. It does not. The Pages publication is bound to
  the release integration commit (`SPEC-DPG-001`, rules 5 to 7). No document
  on the release route says this.
- The owner region says an ungoverned change merges when "the owner accepts
  the red managed check". The ruleset had no bypass actor. This one is a
  human action, but the agent wrote the instruction that could not be
  followed.
- The release sequence in `developing-se-harness.md` assumed a workstation
  with Docker. The hosted alternative existed and was written down only
  after the agent needed it.
- The recipe for the delegated route (merge the packet first, export a
  token, the exact `transition` form) lives only in the evidence packet of
  `WO-ECP-024`.

### 4.8 Maintenance and drift

The managed chain does not drift. It is hash-locked and the installer
regenerates it. The notes drift with every release. After three releases in
two days, nine notes described an earlier state as current. #318 corrected
them:

- the install version was 0.11.0;
- the orientation examples were at 0.6.0;
- two notes described a 0.7.1 feature as future;
- one note named a retired skill as live;
- one note contradicted itself about `rehearse-migration`.

The generated diagnostic-code index did not drift, because a test pins it.
Nothing else in the notes is pinned. For a model, a drifted note is worse
than no note: it reads as current.

## 5. Confusions met in the field

Each row names the surface, what happened, who met it, and where the
missing sentence belongs.

| # | Surface | What happened | Met by | Belongs in |
| --- | --- | --- | --- | --- |
| 1 | `QGP-G1-AUTHORING` | "has an open decision: None. The owner…": the rule (`Open decisions` reads exactly `None`) is not stated, the section is truncated at 120 characters | agent | the gate message: the rule in one sentence |
| 2 | Remediate focus | the corrective `check --artifact` named the last artifact of the transaction, not the failing one | agent | the failure procedure's "first failing predicate" |
| 3 | Supersession order | superseding before the successor is approved invalidates the graph and blocks the approval itself | agent | `validate`: a hint on `E007`/`E008` when the successor is a draft; `WORKFLOW.md` |
| 4 | `E010` | a verification contract that verified records bind cannot be superseded | agent | `TRACEABILITY.md` and the `E010` message |
| 5 | Flag names | `--artifact`, `--work-order`, `--set`, `--id` for the selected artifact | agent | one flag across commands |
| 6 | Decision channel | "by selecting the presented option" is ratified but written nowhere | agent | `DECISION_RIGHTS.md` or `WORKFLOW.md` |
| 7 | In-tree `doctor` | exits 1 on a candidate checkout by design; reads as a failure | agent, human | the `doctor` output, one line |
| 8 | Mutation guard | 790 characters and eleven codes for one meaning | agent | the guard: one sentence and a pointer |
| 9 | Release route | Pages regenerates only from a release integration commit | agent | the release-contract template and the release sequences note |
| 10 | Release route | the pull-request rehearsal builds the merge commit, not the head | agent | the release sequences note (added 2026-09-02) |
| 11 | Release route | a push cancels the candidate-evidence runs of earlier heads | agent | the release sequences note |
| 12 | Release route | the record-mode lane was red on every release PR before merge | agent | fixed by `WO-CIP-006` |
| 13 | Adoption route | a rehearsal clone with `core.autocrlf=true` records a CRLF digest | agent | the root-advance paragraph of the developing note |
| 14 | Evidence packets | a CRLF checkout breaks the packet header parser; a worktree can read as dirty with matching bytes | agent | the `Commands` line of `AGENTS.md` |
| 15 | Delegated route | the class is read at the base; the operator needs a token | agent, human | `WORKFLOW.md` says the first half; nothing says the second |
| 16 | Ungoverned paths | "the owner accepts the red managed check" had no mechanism | human | the owner region, after the ruleset bypass |
| 17 | Windows suite | the runner's report needs `PYTHONUTF8=1` | agent | the `Commands` line of `AGENTS.md` |
| 18 | Reading manifest | the whole of `AGENTS.md` is required; the list has no budget (139 KB for `WO-DST-023`) | agent | `WO-ECP-008` |
| 19 | Notes | nine notes described a superseded state as current | agent, human | a drift test, or a "live/dated" split |

## 6. Scores

| Axis | Score | One line |
| --- | :---: | --- |
| Effectiveness, lifecycle | 5 | every transition and every refusal was right, on two days |
| Effectiveness, operations around it | 2 | all four mistakes of 2026-09-02 fell in the gap |
| Authority for a model | 4 | precedence in eight sentences; the decision channel is unwritten |
| Actionability of tool output | 3 | the block is a model; three refusals hid the rule or the artifact |
| Rules learned only by refusal | 2 | eight rules on one day, each costing a failed command |
| Redundancy and context cost | 3 | one rule written four ways; 6 KB of unvouched text loaded every turn |
| Reading manifest | 2 | correct list, no budget: 36 KB to 139 KB |
| Memory across sessions | 2 | the days succeeded on a memory the repository does not hold |
| Maintenance and drift | 2 | the managed chain never drifts; the notes always do |

## 7. Improvement plan

The items are in order of value for a model. Items 1 to 4 change owner
content or notes and take effect without a product release. Items 5 to 10
change managed files or the product and ship with the next release and root
adoption.

### Wave 0: owner content and notes (no work order, or one small one)

1. **Write one operator runbook for what the lifecycle does not cover.** One
   live note, `docs/notes/operator-runbook.md`, one section per route:
   release day (the sequence, the hosted dispatch, the cancel on push, the
   Pages timing, the latest markers); root adoption (the rehearsal clone
   with `core.autocrlf=input`, the evaluator environments); the delegated
   route (packet first, token, the three commands); the ungoverned merge
   (the bypass); Windows checkouts (CRLF packets, `PYTHONUTF8=1`, the
   worktree that reads dirty). Each section names the artifact that governs
   it. Move the release sequences of `developing-se-harness.md` into it.
   Point to it once from `AGENTS.md`.
2. **Write the learned rules where the agent will meet them.** Add to the
   runbook one section "Rules you meet as refusals", with the eight rows of
   section 4.4 and the exact command that satisfies each. This is the
   repository's copy of the memory that made the two days succeed.
3. **Split the notes index into "live guides" and "dated assessments".**
   Add one test that pins every version-bearing sentence in the live guides
   to the lock and the candidate version, the way
   `test_progressive_documentation` already pins two. The nine corrections
   of #318 would have been one failing test.
4. **Keep one trap list.** Delete the "Traps" of the owner region and let
   the operating card own the list, or the reverse. Not both.

### Wave 1: managed documents (one work order, ships with the next release)

5. **Write the handoff rule once.** `WORKFLOW.md` owns it. The contract
   keeps one sentence and a pointer. The `AGENTS.md` and `CLAUDE.md`
   fragments keep two lines and a pointer. Same for the PR-body rule. This
   removes about 60 lines and three places to drift.
6. **Write the decision channel down.** One paragraph in
   `DECISION_RIGHTS.md`: when a human decides by selecting a presented
   option, the reason field records "by selecting the presented option
   '<label>'" and the label verbatim. The convention exists; make it a rule.
7. **Add a publication paragraph to the release-contract template.** The
   demonstration is generated from the release integration commit. The
   previous root decides how it looks. Ten lines in
   `RELEASE_CONTRACT.template.md`.

### Wave 2: product (one work order in workflow-execution, plus `WO-ECP-008`)

8. **Make every refusal name the rule and the artifact.** `QGP-G1-AUTHORING`
   says "`Open decisions` must read exactly `None`" and quotes the artifact.
   The remediate focus is the first failing predicate's artifact, as the
   failure procedure promises. `E007`/`E008` add "successor `X` is `draft`;
   approve it before superseding" when a superseding relation exists.
   `E010` says "verified records bind this contract; it cannot be
   superseded". The mutation guard prints one sentence and a pointer, with
   the codes behind `--json`. `doctor` on a candidate checkout prints one
   line about the boundary.
9. **One flag for the selected artifact.** `--artifact` everywhere;
   `--work-order` stays as an alias for one release. `--id` stays for a new
   identifier only.
10. **`WO-ECP-008`.** The manifest lists a generated, bounded command block
    instead of `AGENTS.md`, and the handoff digest covers the selected chain,
    not the tree. Add a manifest budget: when the governing chain exceeds a
    stated size, the manifest names the files and marks which sections the
    phase needs. Drafted; waits for the owner's approval.

### What not to change

Keep the structure: one router, one owner per subject, a closed manifest,
a next step the tool computes. Keep the restitution block. Keep the eight
invariants. They are why the lifecycle scores 5 for a model as for a human.
The plan carries the same discipline into two places: the messages the
model reads when it is refused, and the memory the repository keeps of its
own rules.

## 8. What is authoritative

`ENGINEERING_HARNESS.md` and the policies it routes to are the managed
contract. Where their prose differs from `WORKFLOW.json` and
`QUALITY_GATES.json`, the JSON governs. The formal artifacts under
`docs/engineering/` carry every decision. This note is a reading of those
across two days, and a proposal. Nothing here changes a rule, a gate or a
decision right until an accountable owner does so through a governed change.
