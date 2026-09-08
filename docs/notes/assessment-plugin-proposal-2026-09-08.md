# Assessment of the plugin proposal and its 16 packets, 2026-09-08

<!-- Target expertise: 3/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> Point-in-time. Read on [PR #416](https://github.com/mmzen/se_harness/pull/416)
> at `3575f727`, whose base is `main` at `fae52e1b` (candidate source 0.17.0,
> released evaluator 0.16.0). This note is an operator analysis. It has no
> authority: it approves nothing, changes no rule, and answers no open
> decision. It challenges, scores, and proposes. It follows the
> [review of PR #360](https://github.com/mmzen/se_harness/issues/367), which
> the proposal says it incorporates.

## Summary

PR #416 proposes shipping SE Harness as a native plugin for two coding hosts,
Codex and Claude Code. A plugin is a package the host loads to add
instructions (skills), event handlers (hooks), and helpers. The PR carries
the [proposal](plugin-installation-proposal-2026-09-06.md), an
[operation map](plugin-operation-workflows-2026-09-06.md), 16
[scenarios](plugin-scenarios/README.md), and a formal
[packet](../engineering/plugin-integration/README.md) of 27 requirements,
16 specifications, 16 verification contracts, 16 work orders, 2 architecture
records, 2 ADRs, and 5 open decisions. Everything is `draft` or `open`.

The direction is right and the honesty is exemplary. The packet shape is the
problem. Three things need fixing before any work order is approved:

1. **The wheel digest is still not a rule.** The identity check the plugin
   relies on accepts two digest flags; no rule requires them, and no rule
   requires installing from the exact wheel file. This was the second
   blocking finding on PR #360.
2. **No work order can carry the packet onto `main`.** Every scope lists only
   its own work order file, evidence directory, and code paths. The 79
   definitions, the domain index, and the glossary are in no scope.
3. **Two host probes and two decisions answer a question the vendor
   documentation already answers.** Both hosts document a session-start hook
   that prepares dependencies in a persistent plugin data directory on first
   run. A one-line shell guard is a hook command, not a launcher.

Scores run from 3 (mergeability) to 9 (honesty of claims); the table is
below. The proposal at the end is: approve the package assembly and
environment setup packets plus one merged host spike, let those three work
orders carry the definitions, and hold the other thirteen until the spike
reports.

## What the proposal is

The operator provides Python 3.11 or newer. Plugin setup creates a private
Python environment outside the repository and installs one exact released
evaluator wheel into it, offline. Skills tell the agent to run the existing
command line through that environment. Two hook scripts run at session start
(verify the installation, then load the repository's rules) and before
supported tool actions (run the matching existing check). Nothing in the
plugin decides a lifecycle transition; the evaluator keeps that role, and the
accountable human keeps the decision. The plugin adds three skills (`setup`,
`change`, `evidence`), adapts two read-only ones, and offers two optional
read-only helper agents.

## How this was checked

- Every changed file was read: 97 files, 7,388 added lines.
- The released 0.16.0 evaluator was run on the PR head. `harnessctl validate`
  reports 1,512 artifacts, 0 errors, 44 warnings, 0 advisories;
  `harnessctl doctor` passes with the same 44 pre-existing location warnings.
  Both match the PR body exactly.
- The four vendor pages the proposal cites were fetched and compared with the
  proposal's host claims.
- The evaluator commands a hook would run were timed on this repository.
- Each finding of the PR #360 review was traced into the new text.
- The 79 formal artifacts were surveyed for traceability, rule shape, test
  wording, and scope overlap.

## Strengths

1. **One engine, two adapters, no second lifecycle.** Hooks, skills, and
   helpers all call the same installed evaluator. The architecture record
   ARCH-PLG-002 forbids an approval store, a lifecycle API, and merge
   authority in the plugin. That is the right shape, and it was already right
   on PR #360.
2. **Hooks are intervention, not enforcement, and the text never forgets
   it.** The "protected service" that the earlier scenarios assumed is gone.
   Every scenario names the external-control gap and points at issue #347
   rather than claiming the plugin closes it.
3. **The host facts check out.** Against the vendor pages: Claude Code
   exposes a persistent plugin data directory that survives updates; a
   plugin-root `CLAUDE.md` is not loaded; organization distribution rejects
   a top-level `bin/` directory; Codex refuses to run plugin hooks until the
   user trusts them; Codex's plugin manifest documents skills, hooks, and MCP
   servers but not agents; both hosts fire `SessionStart` for compaction and
   resume. The proposal states each of these correctly.
4. **Open questions are artifacts.** Five decision records name an owner,
   list options, and block a definition through the `blocks` relation. A
   negative option authorizes nothing. This is the decision artifact used as
   intended.
5. **A probe may fail honestly.** WO-PLG-003 and WO-PLG-004 may end with a
   documented incompatibility, and that result cannot authorize the
   production adapter.
6. **The claims reproduce.** The validation figures in the PR body were
   re-measured here and match to the artifact. No implementation, host
   test, or performance result is claimed.
7. **Traceability is complete.** Each of the 27 requirements derives from
   an existing capability and has exactly one specification, one
   verification contract, and one work order. All 90 referenced identifiers
   resolve. The 106 specification rules average 17 words; none exceeds 30.
   Every work order proposes commit-bound verification.
8. **Provided Python is the right call.** ADR-PLG-001 weighs shipping an
   interpreter, installing into the global Python, and a private environment
   from provided Python, and picks the last. The trade-offs are stated.

## Weaknesses

1. **The wheel digest is not bound.** [SPEC-PLG-002](../engineering/plugin-integration/specifications/SPEC-PLG-002.md)
   rule PLG-ENV-005 says "verify the installed release and payload through
   existing evaluator identity checks"; rule PLG-ENV-011 names
   `--expected-root` and `--entry-point`. The 0.16.0 `harnessctl identity`
   command also accepts `--evaluator-wheel-sha256` and
   `--evaluator-payload-sha256`; no rule names them, and no rule says the
   install must come from the exact wheel file. An install from a local
   wheel file records the archive hash in the package's `direct_url.json`
   (the 0.16.0 environment on this machine shows it); an index install
   records none, and release preparation then refuses with `MG004`. A
   "repair" that reinstalls from an index satisfies every PLG-ENV rule and
   fails months later. [VER-PLG-002](../engineering/plugin-integration/verification/VER-PLG-002.md)
   mentions "wheel provenance" under evidence retention but has no case for
   it. Rule PLG-ENV-011 also omits `--expected-version`, which the command
   requires.
2. **No scope carries the packet.** Compare
   [WO-DST-026](../engineering/harness-distribution/work-orders/WO-DST-026.md),
   which lists every requirement, specification, and verification file it
   introduces plus the domain index. Here, [WO-PLG-001](../engineering/plugin-integration/work-orders/WO-PLG-001.md)
   lists two code paths, a test directory, itself, and its evidence
   directory. The same holds for all sixteen. The 79 definitions, the two
   architecture records, the two ADRs, the five decisions,
   `docs/engineering/README.md`, and `GLOSSARY.md` are outside every scope.
   [AGENTS.md](../../AGENTS.md#ungoverned-paths) exempts only `docs/notes/`,
   `docs/rca/`, `docs/images/`, and the roadmap. The PR body says the managed
   check will reject the head and calls that expected. It is not a review
   detail; it is the absence of a route to `main`.
3. **The activation problem is self-inflicted.** The proposal requires every
   hook to run as `ENV_PYTHON -I ABS_SCRIPT` with "no custom command wrapper".
   Before setup has created `ENV_PYTHON`, no such hook can run, so
   [DEC-PLG-001](../engineering/plugin-integration/decisions/DEC-PLG-001.md)
   and [DEC-PLG-002](../engineering/plugin-integration/decisions/DEC-PLG-002.md)
   ask which mechanism keeps setup available first, and two probe work
   orders exist to find out. Yet a hook command on both hosts is a shell
   command string. Claude Code's plugin reference documents a `SessionStart`
   hook that compares a bundled manifest with a copy in the persistent data
   directory and installs dependencies when they differ. Codex hands hook
   commands `PLUGIN_DATA`, and sets `CLAUDE_PLUGIN_DATA` too for
   compatibility. "If the environment interpreter exists, run the script;
   otherwise print a not-ready message" is one line of hook command. It is
   not a launcher, a policy engine, or a second protocol. A live check on
   each host, including Windows and Codex hook trust, remains prudent; two
   decisions and two work orders to reach a documented pattern do not.
4. **"A decision that still covers the action" is undefined.** The phrase
   appears in the proposal, the operation map, and fourteen of the sixteen
   scenarios. Nothing says what "covers" means: the same artifact IDs, the
   same content digest, the same candidate commit, the same destination?
   Decision right DR-003 forbids inferring authority across actions. The
   skills in SPEC-PLG-010 and SPEC-PLG-011 will have to answer this in
   prose, which is the place least suited to it.
5. **The release scenario still diverges from the authoritative sequence.**
   [Scenario 14](plugin-scenarios/release-and-maintenance.md) now lists the
   replay build, the bundle manifest, `harnessctl prepare-release`, the
   distribution binding, the candidate replay workflow, and the owner's
   decision. Against [Release sequences](developing-se-harness.md#release-sequences)
   it still omits the release unit derived from the release contract, the
   hosted build of record in the publication rehearsal, the merge of the
   released record to `main` before publication, and the two latest
   markers.
6. **Two baselines in one review.** The notes analyse `aad82a9`, candidate
   0.16.0, released evaluator 0.15.0. The packet is built on `fae52e1b`,
   candidate 0.17.0, released evaluator 0.16.0. The notes say "revised
   2026-09-08" and keep the older baseline. A reader meets the `adopt` alias
   in the notes and unified `init` in the packet.
7. **Three work orders share one file.** `plugins/verity-plane/common/skills/setup/SKILL.md`
   is in the scope of WO-PLG-002, WO-PLG-009, and WO-PLG-013. The graph has
   no dependency relation between work orders, so the order is a convention
   in prose. One work order for the setup skill would remove the question.
8. **A hidden critical path.** [DEC-PLG-004](../engineering/plugin-integration/decisions/DEC-PLG-004.md)
   recommends "an ownership-aware evaluator migration" that the 0.16.0
   evaluator does not have. That is a new work order in another domain, a
   release, and a root adoption before WO-PLG-009 can connect any
   repository. The prerequisites table in the packet index does not show
   it.
9. **The verification contracts are the weak layer.** Of 78 cases across
   the sixteen contracts, 21 name a command, a file, a digest, a version, or
   a unit. The other 57 read like "invalid or incomplete integration never
   reports readiness" or "verify clear restitution of actual effects". No
   case names an exit code or a diagnostic code; one names a command. Six
   contracts share four sentences verbatim. A verifier working from these
   contracts would have to invent the observable, which is the independence
   the contract exists to remove.
10. **Copied columns.** REQ-PLG-006 and REQ-PLG-007 differ in 8 of 50
   lines: the host name and one sentence. Their specifications have
   identical rules under two prefixes, and the same holds for REQ-PLG-008
   and REQ-PLG-009 with their adapters. Three specifications carry the same
   rule that a plugin update cannot change the repository lock. Four
   specification rules restate their requirement's statement. Sixteen
   packets were the design choice; the content supports about eight.
11. **Size.** The notes are 24,568 words; the packet is 26,795. That is
   51,000 words to review before one line of plugin code, at a declared
   target of 3.5/10. The specifications keep rules short, which helps; the
   scenarios repeat the calling convention and the "no claims" banner on
   every page, which does not.

## Risks

- **Effort before value.** Sixteen work orders, each needing a definition
  merge and an implementation merge, plus five decisions, precede the first
  user. The bounded spike that the PR #360 review asked for is present but
  buried as packets 3 and 4 behind packets 1 and 2.
- **Hook latency.** Measured here, warm, on 1,512 artifacts: a state
  projection takes 3.8 s, a scope check 2.0 s, `harnessctl doctor` 2.4 s,
  `harnessctl validate` 12.3 s. A before-tool hook that runs a scope check
  costs about two seconds per covered edit on this repository; larger
  repositories cost more. DEC-PLG-005 defers the budget. The numbers exist
  now.
- **Qualification may be unreachable.** VER-PLG-015 requires passing
  evidence for a complete host matrix including "operator prompts per
  operation". Prompt counts depend on model behaviour and vary between runs.
  A verification contract that can never be satisfied blocks the packet it
  qualifies.
- **Two skill routes at once.** Until DEC-PLG-004 is resolved and its
  evaluator work shipped, a connected repository carries the hash-locked
  `.agents/skills/harness-orient` and the plugin's copy. Two discoverable
  skills with one name is the confusion the host adapters note was written
  to avoid.
- **One wheel per plugin release.** The plugin ships one evaluator version.
  An operator with three repositories at three locks needs three plugin
  versions, or three upgrades. The proposal names this as a question to
  challenge; it is the operating-model risk of the whole design.
- **Codex helpers.** Codex's plugin manifest does not document agents, so the
  optional helpers are Claude Code features until proven otherwise. The
  scenarios still mention registering them under `.codex/agents/` inside the
  governed repository, a path no work order owns.
- **A qualification lane on hosted runners.** WO-PLG-015 adds
  `.github/workflows/plugin-qualification.yml`. Running Codex or Claude Code
  on a runner needs the host binary and a credential; neither is discussed.

## Scores

Scale: 0 is bad, 10 is perfect. Each score judges the PR as it is today,
not the idea.

| Axis | Score | Why |
| --- | --- | --- |
| Problem fit and value | 8 | Manual environment creation and repository adoption are real friction; the plugin route matches how both hosts are used. |
| Architecture | 8 | One engine, two thin adapters, no second lifecycle, hooks as intervention. Loses points for the self-inflicted activation problem. |
| Authority and trust boundary | 6 | Honest about every gap and points at the right issue. Loses points for the unbound wheel digest and the undefined "covers". |
| Host-platform accuracy | 7 | Every checked vendor fact is right. Misses the documented first-run bootstrap pattern that would dissolve two decisions. |
| Absorption of the PR #360 review | 5 | Finding 1 fixed; finding 4 mostly fixed; findings 3 and 5 partly; finding 2 not fixed in any rule; finding 6 partly. |
| Packet quality | 6 | Requirements and specifications are strong: complete traceability, clean validation, short numbered rules in the repository's current shape. Verification contracts are weak: 57 of 78 cases name nothing observable, and four artifact columns are copies. |
| Decomposition and delivery plan | 4 | Sixteen packets where the content supports eight, three on one file, two probes for one question, a hidden evaluator-release dependency, and no way to express order. |
| Mergeability and process conformance | 3 | No trailer can carry it; the PR says so and offers no route. The precedent packet in PR #410 shows the shape that merges. |
| Readability and size | 4 | 51,000 words at a 3.5/10 target, two baselines, banners repeated on every page. |
| Honesty of claims | 9 | Every figure reproduces. Nothing is claimed that was not done. |

## Proposal

1. **Give the packet a carrier.** Either draft it as stacked pull requests
   from the start, one work order per pull request, each work order's scope
   naming its own requirement, specification, and verification files, with
   WO-PLG-001 also naming the index, the architecture records, the ADRs, the
   decisions, `docs/engineering/README.md`, and `GLOSSARY.md`. Or, the lighter
   route below.
2. **Approve three work orders, not sixteen.** Package assembly (WO-PLG-001),
   environment setup (WO-PLG-002), and one merged host spike replacing
   WO-PLG-003 and WO-PLG-004. Let those three scopes carry the whole
   definition set. Hold the other thirteen as drafts until the spike
   reports. This is the bounded experiment the PR #360 review recommended,
   now with the definitions it needs.
3. **Bind the wheel.** Add two rules to SPEC-PLG-002: install from the exact
   wheel file so the package records its archive hash; pass
   `--expected-version`, `--evaluator-wheel-sha256`, and
   `--evaluator-payload-sha256` from the release's locked digests on every
   identity check. Add one case to VER-PLG-002: an index-installed
   environment is refused.
4. **Use the documented bootstrap.** Register a shell-form `SessionStart`
   hook that runs the Python script when the environment interpreter exists
   and prints a not-ready message when it does not. Fold DEC-PLG-001 and
   DEC-PLG-002 into one decision whose recommended option names that route,
   and let the spike confirm it on both hosts, on Windows, and behind Codex
   hook trust.
5. **Define "covers" or drop it.** If a decision is reusable, say for which
   artifact IDs, which content digest, which candidate, and which
   destination. If that cannot be said, the agent asks again.
6. **Align scenarios 14 and 15 with Release sequences.** Add the release
   unit, the publication rehearsal as build of record, the merge of the
   released record, and the latest markers.
7. **Re-baseline the notes** to `fae52e1b`, or add a short delta box to each
   of the four note pages listing what changed between the two baselines.
8. **Seed DEC-PLG-005 with the numbers above.** Two seconds per covered edit
   and three seconds at session start are a measured starting budget on a
   1,512-artifact repository.
9. **Fold the skill packets.** WO-PLG-010, WO-PLG-011, and WO-PLG-012 ship
   three skill files each; one work order can. WO-PLG-013 belongs in
   WO-PLG-002. WO-PLG-014 waits for a host that can load the helpers. That
   takes sixteen packets to eight without losing a requirement.
10. **Give every verification case an observable.** For each of the 57
   cases that name none, add the command, the expected exit code or
   diagnostic code, the file, or the threshold. Where the observable does
   not exist yet, say which work order creates it. A contract that cannot
   be failed cannot be passed either.

## How the PR #360 review findings fared

| Finding on PR #360 | Status in PR #416 |
| --- | --- |
| 1. Approve, verify, and decide flows assumed a protected decision service that does not exist. | Fixed. The service is gone; each scenario names the gap and issue #347. |
| 2. Runtime provisioning must bind the wheel digest and record the archive pair. | Not fixed. No rule, no verification case, no flag. |
| 3. The release scenario omitted the release unit, the build of record, the merge to `main`, and the latest markers. | Partly fixed. The candidate replay and publication workflow are named; the four items are still absent. |
| 4. Two proposals edited a hash-locked skill and wrote under `.codex/agents/`. | Mostly fixed. The adapted skills live in the plugin. Codex registration in the repository is still described. |
| 5. Smaller factual points (delegation recheck, undefined "covers", supersession, LF header, candidate commit, stop tables). | Partly fixed. "Covers" is still undefined; the rest are corrected or removed. |
| 6. Terms used before definition; five components in one paragraph. | Partly fixed. A component table opens the operation map; the glossary gained six terms; the scenarios remain dense. |

## Measurements

All figures were taken on this checkout, on Windows, with the released
0.16.0 evaluator, warm cache, one run each.

| Command | Time |
| --- | --- |
| `harnessctl validate` | 12.3 s |
| `harnessctl check` projection of one work order | 3.8 s |
| `harnessctl doctor` | 2.4 s |
| `harnessctl check` scope checkpoint, one changed path | 2.0 s |
| `harnessctl preflight` start phase | 1.9 s |

| Content | Files | Lines | Words |
| --- | --- | --- | --- |
| Notes (proposal, map, template, scenarios) | 8 | 2,186 | 24,568 |
| Formal packet (`docs/engineering/plugin-integration/`) | 85 | 5,179 | 26,795 |
| Index and glossary edits | 4 | 23 | — |
