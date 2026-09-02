# Assessment of the instruction chain, 2026-09-02

<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> Point-in-time, measured on `main` at `19b6819`. Non-authoritative operator
> analysis: the managed contract, the formal artifacts and accountable
> decisions remain authoritative. This note grants nothing and changes no
> rule; it proposes.

## Contents

1. [What the chain is](#1-what-the-chain-is)
2. [Method](#2-method)
3. [Measurements](#3-measurements)
4. [Assessment by axis](#4-assessment-by-axis)
5. [Catalogue of confusions met in the field](#5-catalogue-of-confusions-met-in-the-field)
6. [Scores](#6-scores)
7. [Improvement plan](#7-improvement-plan)
8. [Know what is authoritative](#8-know-what-is-authoritative)

## 1. What the chain is

The "instruction chain" is every document a human or an agent is told to
read before acting in this repository, in the order the documents route to
one another:

```text
entry            CLAUDE.md ─imports─▶ AGENTS.md (owner region + managed block)
                                          │
router           ENGINEERING_HARNESS.md ◀─┘   "read this before engineering work"
                     │ routing table (one policy owner per subject)
policies         WORKFLOW.md + WORKFLOW.json      DECISION_RIGHTS.md
                 QUALITY_GATES.md + .json         TRACEABILITY.md
                 ARTIFACT_AUTHORING.md            TECHNICAL_COMMUNICATION.md
                 templates/README.md              docs/engineering/README.md (index)
per-stage        OPERATING_CARD.md  + the phase reading manifest that `check`
                 and `preflight` return (governing chain of the selected WO)
skills           .agents/skills/*/SKILL.md, .claude/skills/*/SKILL.md
learning         docs/notes/  (35 notes, 14 history documents)
tool output      the schema-2 restitution block every workflow command prints
```

Three layers have different authority: the managed contract and policies
(hash-locked, evaluator-owned), the owner region of `AGENTS.md` and the
notes (repository-owned, no authority), and the tool's own output (the one
thing `HRN-004` says may compute the next step). The chain is well designed
on paper: one router, one owner per subject, a closed reading manifest per
phase, and a machine-rendered next step. The question this note answers is
how it behaves when used for a full day.

## 2. Method

Two sources.

- **Measurement** on `main` at `19b6819`: size, rule count and
  cross-reference count of every document in the chain; the weight of a real
  phase reading manifest; how many times the same rule is restated.
- **A field test**: the governed work of 2026-09-02 in this repository,
  executed by a coding agent with the owner deciding: releases 0.13.0 and
  0.14.0 (`REL-SEH-024`, `REL-SEH-025`), two root adoptions (`WO-HUP-014`,
  `WO-HUP-015`), a Pages repair (`WO-DPG-002`), two delegated-route work
  orders (`WO-ECP-025`, `WO-CIP-006`), and one ungoverned notes change
  (#318). Every place the chain was followed and produced the right outcome,
  and every place it did not, is evidence here. The three assessments of
  August (functional, complexity, agentic-execution) are cited where they
  reached the same finding earlier.

Scores are 1 to 5, where 5 means "no change needed".

## 3. Measurements

### 3.1 The documents

| Document | Lines | Bytes | MUST/SHALL | Rule IDs |
| --- | ---: | ---: | ---: | ---: |
| `CLAUDE.md` | 9 | 402 | 0 | 0 |
| `AGENTS.md` (owner 5,912 B + managed 1,087 B) | 80 | 6,999 | 0 | 2 |
| `ENGINEERING_HARNESS.md` | 126 | 6,396 | 29 | 8 |
| `OPERATING_CARD.md` | 24 | 1,006 | 0 | 0 |
| `WORKFLOW.md` | 286 | 20,113 | 46 | 6 |
| `WORKFLOW.json` | 384 | 32,698 | 0 | 0 |
| `DECISION_RIGHTS.md` | 89 | 6,822 | 24 | 15 |
| `QUALITY_GATES.md` | 166 | 13,150 | 29 | 12 |
| `QUALITY_GATES.json` | 127 | 10,513 | 0 | 0 |
| `TRACEABILITY.md` | 152 | 13,792 | 29 | 33 |
| `ARTIFACT_AUTHORING.md` | 139 | 5,793 | 7 | 3 |
| `TECHNICAL_COMMUNICATION.md` | 147 | 6,333 | 19 | 0 |
| `templates/README.md` | 28 | 1,618 | 0 | 0 |
| `docs/engineering/README.md` (index) | 61 | 6,723 | 0 | 0 |
| three `SKILL.md` | 161 | 8,135 | 0 | 0 |
| **Managed chain total** | | **≈134 KB** | **183** | |
| `README.md` (public entry) | 199 | 15,552 | 0 | 0 |
| `docs/notes/` (35 notes) | 6,447 | ≈300 KB | | |
| `docs/notes/history/` (14) | 3,261 | | | |
| `docs/engineering/templates/` (13) | 573 | | | |

### 3.2 What one work order asks you to read

The phase reading manifest `check` and `preflight` returned for
`WO-CIP-006` (review phase) names nine files, 36,117 bytes:

| Bytes | File | Nature |
| ---: | --- | --- |
| 6,999 | `AGENTS.md` | 85% owner narrative, 15% managed block |
| 6,396 | `ENGINEERING_HARNESS.md` | the contract |
| 6,390 | the work order | governing |
| 4,474 | `REQ-CIP-007` | governing |
| 3,868 | `SPEC-CIP-002` | governing |
| 2,944 | `INT-CIP-001` | governing |
| 2,471 | `VER-CIP-002` | governing |
| 1,545 | `CAP-CIP-001` | governing |
| 1,030 | `OPERATING_CARD.md` | derived summary |

Roughly 40% of the mandatory read is the two front files; the routed
policies (WORKFLOW, DECISION_RIGHTS, QUALITY_GATES, TRACEABILITY,
≈54 KB of Markdown plus 43 KB of JSON) are reference an agent "is not
required to read to act", and in the field test they were consulted only
when a gate refused.

### 3.3 Restatement

| Rule | Where it is stated | Count |
| --- | --- | ---: |
| The lifecycle handoff (preserve IDs, one typed next step, no unrelated findings) | `CLAUDE.md`, `AGENTS.md` managed block, `ENGINEERING_HARNESS.md` "Lifecycle handoff", `WORKFLOW.md` "Lifecycle handoff procedure" | 4 |
| The stop conditions | `ENGINEERING_HARNESS.md`, `OPERATING_CARD.md` (declared derived) | 2 |
| "Traps" lists | `AGENTS.md` owner region (4 items), `OPERATING_CARD.md` (4 items, overlapping but not identical) | 2 |
| The pull-request `Harness-Work-Order` line | `AGENTS.md`, `OPERATING_CARD.md`, `WORKFLOW.md`, the PR template, the notes | 5 |

## 4. Assessment by axis

### 4.1 Effectiveness: does following the chain produce correct governed outcomes?

**Yes, for the lifecycle itself.** Every transition of the day was taken on
the tool's own restitution, every gate that should refuse refused (the
mutation guard on in-tree writes, the handoff gate before the packet was
committed, `QGP-G1-AUTHORING` on a `<base>` placeholder, the delegation gate
until the check was green), and no decision was taken by anyone but the
named role. The `check` block is the single most effective document in the
repository: 48 lines, one shape, the next command spelled out.

**No, for the operations around the lifecycle.** The chain routes the
lifecycle exhaustively and the surrounding operations thinly. The day's
mistakes were all in that gap:

- The release contract said the public demonstration regenerates after the
  root adoption merges; it does not, because the Pages publication is
  release-bound to the integration commit (`SPEC-DPG-001` rules 5 to 7). No
  document on the release route says so; the fact lives in the
  dashboard-publication specification, which the release route never names.
- The owner region says an ungoverned change merges with "the owner accepts
  the red managed check". The ruleset had no bypass actor, so no one could.
- The release sequence in `developing-se-harness.md` assumed a workstation
  with Docker; the hosted alternative existed but was written down only after
  it was needed.
- The delegated route's operator recipe (merge the packet first because the
  class is read at the base; export a token; the exact `transition` form) is
  recorded only in `WO-ECP-024`'s evidence packet.

### 4.2 Clarity: can a reader tell what is required, by whom, and what is not?

**Strong.** BCP-14 language, one identifier per rule, routing to a single
owner per subject, an explicit "Scope of these obligations" paragraph that
frees reading and analysis from the lifecycle rules, and a glossary since
the 0.12.0 wave. `DECISION_RIGHTS.md` is a model: a role table, a
decision-right catalogue, twelve numbered rules, done.

**Weak points.** The vocabulary is dense for a newcomer even with the
glossary (restitution, projection, handoff, checkpoint, packet, snapshot,
root, candidate, governor). Several rules read as law but are really
operator advice, for example "the rehearsal's PR-event job builds the merge
commit" is not stated anywhere while "MUST NOT redefine the canonical next
action" is stated four times.

### 4.3 Consistency and redundancy

**Structural consistency is good**: the routing table is honoured, the
operating card declares itself derived, the JSON contracts are declared
authoritative over their prose. **Textual redundancy is the problem**: the
handoff rule is written four times in four wordings; the two traps lists
overlap without being the same list; the PR-body rule appears five times.
Each restatement is a place for drift, and two of them drifted this year
already (the "Traps" in `AGENTS.md` mention the live-body lane, the card's
do not).

### 4.4 Cognitive load

Per work order the mandatory read is about 36 KB, of which the two front
files are 13 KB and mostly unchanged from one work order to the next. Of
`AGENTS.md`, 85% is owner narrative that the tool cannot vouch for and that
the agent must not treat as authority, yet it is on the required list. The
agentic-execution review (section 6) measured the same and `WO-ECP-008` is
drafted for it. In the field test the agent read the two front files once
and then relied on the `check` block; the manifest's repetition added
nothing after the first work order.

### 4.5 Route and discoverability

**The lifecycle route is short and correct**: `CLAUDE.md` imports
`AGENTS.md`; the managed block sends you to `ENGINEERING_HARNESS.md`; the
contract names the operating card and the phase manifest; the tool names
the rest. **The operations route is scattered**: how to run a release lives
in one note section (`developing-se-harness.md#release-sequences`), how to
run the delegated route lives in an evidence packet, how to publish the
demonstration lives in a specification, how to rehearse an adoption lives
in the previous adoption's work order. The notes index offers 24 routes and
a 7-step path; a quarter of the notes are point-in-time reviews mixed with
live guides, labelled but interleaved.

### 4.6 Actionability

The best surfaces tell you what to type: the `check` block, `pr-body`, the
corrective forms of a blocked gate. The worst tell you eleven things at once:
the in-tree mutation guard prints 790 characters and eleven `RID` codes to
say "run the released evaluator from outside the checkout", a sentence the
owner region already contains. `doctor` in-tree exits 1 by design after
every release, which `AGENTS.md` explains but which still reads as a failure
to anyone who has not read that paragraph.

### 4.7 Authority boundaries

Clear and enforced: `HRN-001` to `HRN-008`, the managed-versus-owner split
of `AGENTS.md`, the mutation guard, the class read at the pull request's
base. The one crack found today is not in the documents but between a
document and a setting: the owner region promised a merge route the ruleset
did not provide until a bypass actor was added on 2026-09-02.

### 4.8 Maintenance and drift

The managed chain does not drift: it is hash-locked and regenerated by the
installer. The notes drift with every release: after three releases in two
days, nine notes still described an earlier state as current and were
corrected in #318 (install version 0.11.0, orientation examples at 0.6.0,
two notes describing a 0.7.1 feature as future, a retired skill named as
live, a self-contradiction about `rehearse-migration`). The generated
diagnostic-code index, pinned by a test, did not drift; nothing else in the
notes is pinned to the state it describes.

## 5. Catalogue of confusions met in the field

Each item names the surface, what happened, and where the missing sentence
belongs.

| # | Surface | What happened | Belongs in |
| --- | --- | --- | --- |
| 1 | In-tree `doctor` | exits 1 on a candidate checkout by design; reads as a failure | the `doctor` output itself, one line |
| 2 | Mutation guard | 790 characters, eleven codes, one meaning | the guard: one sentence plus the pointer |
| 3 | Release route | Pages regenerates only from a release integration commit | the release-contract template and the release sequences note |
| 4 | Release route | the pull-request rehearsal builds the merge commit, not the head; dispatch on the branch to read the head | the release sequences note (added 2026-09-02) |
| 5 | Release route | a push cancels in-progress candidate-evidence runs at earlier heads; re-run for a green lane at the bound candidate | the release sequences note |
| 6 | Release route | the record-mode lane was red on every release PR before its merge | fixed by `WO-CIP-006` |
| 7 | Adoption route | a rehearsal clone with `core.autocrlf=true` records a CRLF digest of the prior lock | the root-advance paragraph of the developing note |
| 8 | Delegated route | the class is read at the base, so the packet merges first; the operator needs a token in the environment | `WORKFLOW.md` says the first half; nothing says the second |
| 9 | Ungoverned paths | "the owner accepts the red managed check" had no mechanism | the owner region, after the ruleset bypass |
| 10 | Windows suite | the runner's report needs `PYTHONUTF8=1` since the designed page's characters | the `Commands` line of `AGENTS.md` |
| 11 | Reading manifest | the whole `AGENTS.md` is required reading | `WO-ECP-008` |
| 12 | Notes | nine notes described superseded state as current | a drift test or a "live/dated" split |

## 6. Scores

| Axis | Score | One line |
| --- | :---: | --- |
| Effectiveness, lifecycle | 5 | every transition and refusal was right |
| Effectiveness, operations around it | 2 | the day's four mistakes all fell in the gap |
| Clarity of rules | 4 | normative, identified, routed; dense vocabulary |
| Consistency and redundancy | 3 | one rule written four ways; two trap lists |
| Cognitive load | 3 | 36 KB per work order, 13 KB of it constant and 6 KB unvouched |
| Route and discoverability | 3 | lifecycle route short; operations route scattered |
| Actionability | 4 | `check` is exemplary; two messages are not |
| Authority boundaries | 4 | enforced; one document-versus-setting crack |
| Maintenance and drift | 2 | managed chain never drifts; notes always do |

## 7. Improvement plan

Ordered by value per effort. Items 1 to 4 are owner-content or note changes
and need no product release to take effect; items 5 to 7 change managed
files or the product and ship with the next release and root adoption.

### Wave 0, owner content and notes (no work order or one small one)

1. **One operator runbook for the operations the lifecycle does not cover.**
   A single live note, `docs/notes/operator-runbook.md`, with one section per
   route: release day (the sequence, the hosted build dispatch, the
   concurrency cancel, the Pages timing, the latest markers), root adoption
   (rehearsal clone with `core.autocrlf=input`, the evaluator environments),
   the delegated route (packet first, token, the three commands), the
   ungoverned-path merge (the bypass). Each section is the sentences that
   were missing on 2026-09-02, and each names the artifact that governs it.
   The release sequences section of `developing-se-harness.md` moves into
   it; `AGENTS.md` points to it once.
2. **Fix the owner region's three stale or missing facts**: the bypass route
   for ungoverned paths; `PYTHONUTF8=1` on the test line; the in-tree
   `doctor` sentence pointing at the runbook. One small work order, since the
   owner region is governed content.
3. **Split the notes index into "live guides" and "dated assessments"**,
   move the history table's spirit up one level, and add one test that
   pins every version-bearing sentence in the live guides to the lock and
   the candidate version (the way `test_progressive_documentation` already
   pins two of them). The nine corrections of #318 would have been one
   failing test the morning after the 0.12.0 release.
4. **One trap list.** Delete the "Traps" of `AGENTS.md`'s owner region and
   let the operating card own the list, or the reverse; not both.

### Wave 1, managed documents (one work order, ships with the next release)

5. **State the handoff rule once.** `WORKFLOW.md`'s "Lifecycle handoff
   procedure" is the owner. `ENGINEERING_HARNESS.md` keeps one sentence and a
   pointer; the `AGENTS.md` and `CLAUDE.md` fragments keep the two-line
   instruction and the pointer. Same for the PR-body rule: the operating card
   owns it, the others point. This removes about 60 lines and three places to
   drift.
6. **Add the operations pointer to the release-contract template**: a
   "Publication" paragraph naming that the demonstration is generated from
   the release integration commit and that the previous root decides its
   look. Ten lines in `RELEASE_CONTRACT.template.md`.

### Wave 2, product (existing drafts)

7. **`WO-ECP-008`**: the reading manifest lists a generated, bounded command
   block instead of `AGENTS.md`, and the handoff snapshot digest covers the
   selected artifact's chain rather than the whole tree. Drafted, definitions
   approved, waits for the owner's approval.
8. **Two messages**: the mutation guard prints one sentence plus a pointer
   and puts the eleven codes behind `--json`; `doctor` on a candidate
   checkout prints one line explaining that the skew it reports is the
   candidate-versus-released boundary. A small work order in
   released-evaluator-boundary.

### What not to change

The contract's structure (router, one owner per subject, closed manifest,
tool-computed next step) and the `check` restitution block. They are why the
lifecycle half of this assessment scores 5; the plan above is about carrying
the same discipline into the operations around it and about saying each
rule once.

## 8. Know what is authoritative

`ENGINEERING_HARNESS.md` and the policies it routes to are the managed
contract; `WORKFLOW.json` and `QUALITY_GATES.json` govern where their prose
differs; the formal artifacts under `docs/engineering/` carry every decision.
This note is a reading of those on one day, and a proposal. Nothing here
changes a rule, a gate or a decision right until an accountable owner does so
through a governed change.
