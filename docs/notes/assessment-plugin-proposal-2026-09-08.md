# Assessment of the plugin proposal and its 16 packets, 2026-09-08

<!-- Target expertise: 3/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> Point-in-time. Read on [PR #416](https://github.com/mmzen/se_harness/pull/416)
> at `3575f727`, whose base is `main` at `fae52e1b` (candidate source 0.17.0,
> released evaluator 0.16.0). This note is an operator analysis. It has no
> authority: it approves nothing, changes no rule, and answers no open
> decision. It challenges, scores, and proposes. It follows the
> [review of PR #360](https://github.com/mmzen/se_harness/issues/367), which
> the proposal says it incorporates.

> **Revised the same evening**, after the author's reply on
> [discussion #418](https://github.com/mmzen/se_harness/discussions/418).
> Four points were corrected: the offline exact-wheel install is already a
> rule, so the identity gap is narrower; "covers" is half defined by
> PLG-CHANGE-004; the hosted build of record is the route when there is no
> Docker engine, not a mandatory step; and the count of verification cases
> without an observable depends on the reading, so both readings and the
> case list are now given. One measurement was added: a bounded first
> delivery fails validation with 41 errors. The carrier and packet-count
> items of the proposal were rewritten. Two scores moved.
>
> **Reassessed at `c5c3c7c4`** the same night, after the author revised
> PR #416 in answer. The [reassessment](#reassessment-at-c5c3c7c4) at the end
> re-scores the ten axes, lists what still blocks approval apart from what
> only reads badly, and answers whether the two probe packages are ready
> for their owners. The body above is left as written at `3575f727`.

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

1. **The wheel digest is still not compared.** Installing the supplied
   wheel offline is a rule; checking its digest against release metadata is
   not, and the evaluator passes a missing digest by design. This was the
   second blocking finding on PR #360.
2. **No work order can carry the packet onto `main`.** Every scope lists only
   its own work order file, evidence directory, and code paths. The 79
   definitions, the domain index, and the glossary are in no scope, and a
   bounded first delivery fails validation with 41 errors because the shared
   records reference most other packages.
3. **Two host probes and two decisions answer a question the vendor
   documentation already answers.** Both hosts document a session-start hook
   that prepares dependencies in a persistent plugin data directory on first
   run. A one-line shell guard is a hook command, not a launcher.

Scores run from 3 (mergeability) to 9 (honesty of claims); the table is
below. The proposal at the end is: start with the two probe packages, then
assembly and setup, hold the other twelve as drafts, and choose one of two
carrier orderings, each costed below.

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
- A bounded first delivery was assembled in a scratch worktree and validated.
- After the author's reply, each of their corrections was checked against
  the code and artifacts they cite.

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

1. **The wheel digest is not compared.** [SPEC-PLG-002](../engineering/plugin-integration/specifications/SPEC-PLG-002.md)
   already requires the offline install of the supplied wheel (PLG-ENV-004),
   and SPEC-PLG-013 requires repair from the bundled wheel with
   `--no-index --no-deps` (PLG-MNT-002), so an index install is outside the
   contract. What no rule requires is the comparison. PLG-ENV-005 says
   "verify the installed release and payload through existing evaluator
   identity checks"; PLG-ENV-011 names `--expected-root` and
   `--entry-point` but not `--expected-version`, which the command
   requires, nor `--evaluator-wheel-sha256` and
   `--evaluator-payload-sha256`. The flags alone would not close the gap:
   the evaluator raises `RID022` only when an installed archive digest
   exists and differs, and passes an installation with no recorded digest
   by design (REQ-REB-028, `runtime_identity.py`). An install from a local
   wheel file records that digest in `direct_url.json`; the 0.16.0
   environment on this machine shows it. So the plugin contract has to
   require that the observed archive digest is present and equal to the
   independently verified wheel, with expected values taken from release
   metadata rather than from the installation under check.
   [VER-PLG-002](../engineering/plugin-integration/verification/VER-PLG-002.md)
   mentions "wheel provenance" under evidence retention but has no case for
   a wrong payload, a different archive, missing archive metadata, or a
   tampered bundled wheel.
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
   detail; it is the absence of a route to `main`. The route is also harder
   than "deliver bounded subsets". The CI selector accepts exactly one work
   order per pull request and checks the whole diff against its scope. The
   shared records reference artifacts in most packages: ARCH-PLG-002
   addresses requirements from five packages and conforms to five
   specifications, and each decision concerns a specification and a work
   order from another package. Measured in a scratch worktree at
   `3575f727`: a first delivery of the Codex probe package together with
   the domain index, both architecture records, both ADRs, and all five
   decisions validates with 41 errors, 39 of them `E006` unknown relation
   target and 2 `E016` addressed requirement without a conforming
   specification.
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
   each host, including Windows and Codex hook trust, remains prudent, and
   two host-specific evidence sets are a defensible shape. What does not
   hold is the question the two decisions ask, "which mechanism", which the
   documentation answers. Once a guard exists, the "no custom command
   wrapper" sentence that the notes repeat on many pages also needs
   re-scoping to what it means: no launcher binary, no `PATH` lookup, no
   second protocol.
4. **"A decision that still covers the action" is half defined.** The
   phrase appears in the proposal, the operation map, and fourteen of the
   sixteen scenarios. Rule PLG-CHANGE-004 in SPEC-PLG-010 names the
   dimensions whose change invalidates a continuation: scope, content,
   candidate, destination, gates, and required authority. It does not say
   how each is compared (content by digest, candidate by commit,
   destination by address), nor which dimensions apply to which kind of
   decision: a definition approval, a work-order start, an assurance
   decision, and an external action are not invalidated by the same
   changes. Decision right DR-003 forbids inferring authority across
   actions. One shared table would close this; the author has proposed
   one.
5. **The release scenario still diverges from the authoritative sequence.**
   [Scenario 14](plugin-scenarios/release-and-maintenance.md) now lists the
   replay build, the bundle manifest, `harnessctl prepare-release`, the
   distribution binding, the candidate replay workflow, and the owner's
   decision. Against [Release sequences](developing-se-harness.md#release-sequences)
   it still omits the release unit derived from the release contract, the
   publication rehearsal as the build of record when the workstation has no
   Docker engine, the merge of the released record to `main` before
   publication, and the two latest markers.
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
9. **The verification contracts are the weak layer, by either reading.**
   Two readings of the same 78 cases were made. A reader applying the
   rubric "names a command, a file, a digest, a version, or a unit" found 21
   observable and 57 not. A mechanical rule over the same text, stated in
   the appendix, is more generous: it also accepts a lifecycle state in
   backticks, the words "unchanged", "identical", "sentinel", "bytes",
   "hash", and any tool name, and finds 46 observable and 32 not. The 32
   are listed in the appendix. Under either reading, VER-PLG-005 and
   VER-PLG-006 have no observable in any of their four cases, VER-PLG-001
   and VER-PLG-002 have none in half of theirs, six contracts share four
   sentences verbatim, no case names an exit code or a diagnostic code, and
   one names a command. A verifier working from these contracts would have
   to invent the observable, which is the independence the contract exists
   to remove.
10. **Copied columns.** REQ-PLG-006 and REQ-PLG-007 differ in 8 of 50
   lines: the host name and one sentence. Their specifications have
   identical rules under two prefixes, and the same holds for REQ-PLG-008
   and REQ-PLG-009 with their adapters. Three specifications carry the same
   rule that a plugin update cannot change the repository lock. Four
   specification rules restate their requirement's statement. Sixteen
   packets were the design choice; the copies suggest fewer would carry the
   same content.
11. **Size.** The notes are 24,568 words; the packet is 26,795. That is
   51,000 words to review before one line of plugin code, at a declared
   target of 3.5/10. The specifications keep rules short, which helps; the
   scenarios repeat the calling convention and the "no claims" banner on
   every page, which does not.

## Risks

- **Effort before value.** Sixteen work orders, each needing a definition
  merge and an implementation merge, plus five decisions, precede the first
  user. The bounded spike that the PR #360 review asked for exists as
  packets 3 and 4. The index lists them after assembly and setup, but they
  depend on neither and can go first.
- **Hook latency.** Measured here, warm, on 1,512 artifacts: a state
  projection takes 3.8 s, a scope check 2.0 s, `harnessctl doctor` 2.4 s,
  `harnessctl validate` 12.3 s. A before-tool hook that runs a scope check
  costs about two seconds per covered edit on this repository; larger
  repositories cost more. DEC-PLG-005 defers the budget. The numbers exist
  now.
- **Qualification needs its counting rules first.** VER-PLG-015 requires
  passing evidence for a complete host matrix including "operator prompts
  per operation". Prompt counts depend on model behaviour and vary between
  runs, so the profile has to say what is counted, how many repetitions,
  and which aggregate and threshold apply before the contract can be passed
  or failed. Until then it blocks the packet it qualifies.
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
| Authority and trust boundary | 7 | Honest about every gap and points at the right issue. Loses points for the uncompared wheel digest and the half-defined "covers". |
| Host-platform accuracy | 7 | Every checked vendor fact is right. Misses the documented first-run bootstrap pattern that would dissolve two decisions. |
| Absorption of the PR #360 review | 6 | Finding 1 fixed; finding 4 mostly; findings 2, 3, 5, and 6 partly: the offline exact wheel is a rule, its digest is never compared. |
| Packet quality | 6 | Requirements and specifications are strong: complete traceability, clean validation, short numbered rules in the repository's current shape. Verification contracts are weak: between 32 and 57 of 78 cases name nothing observable depending on the reading, and four artifact columns are copies. |
| Decomposition and delivery plan | 4 | Sixteen packets with four copied columns, three on one file, two decisions for one documented question, a hidden evaluator-release dependency, and no way to express order. |
| Mergeability and process conformance | 3 | No trailer can carry it; the PR says so and offers no route. A bounded first delivery fails validation with 41 errors because the shared records reference other packages. |
| Readability and size | 4 | 51,000 words at a 3.5/10 target, two baselines, banners repeated on every page. |
| Honesty of claims | 9 | Every figure reproduces. Nothing is claimed that was not done. |

## Proposal

1. **Choose a carrier, knowing the cost of each.** One work order per pull
   request is fixed by the CI selector, so the definitions land in stacked
   pull requests either way. Two orderings validate. In the first, the
   first package's work order names the whole domain directory,
   `docs/engineering/README.md`, and `GLOSSARY.md` in its scope, so the 79
   drafts land together and each later package approves and implements its
   own. Drafts confer no authority, but that first trailer covers the
   domain while it is selectable, and reviewers carry that. In the second,
   packages land one by one, each work order naming its own files, with
   the shared architecture records and decisions trimmed to the artifacts
   already delivered and amended as each package lands, and each decision
   travelling with the specification it blocks rather than with the
   probe. The second respects the small-packet preference at the price of
   about ten amendments to records that will be approved partway through,
   some under a repair work order. As drafted today the second ordering
   fails with 41 errors. Either is workable; the packet has to say which.
2. **Start with the probes.** WO-PLG-003 and WO-PLG-004 depend on no
   production adapter and may end in an evidenced incompatibility. Approve
   them first, then WO-PLG-001 and WO-PLG-002. Hold the other twelve as
   drafts until the probes report. This is the bounded experiment the
   PR #360 review recommended.
3. **Compare the wheel.** Add to SPEC-PLG-002 and SPEC-PLG-013 that the
   identity check passes `--expected-version`,
   `--evaluator-wheel-sha256`, and `--evaluator-payload-sha256` from
   release metadata the installation cannot influence, and that readiness
   requires the observed archive digest to be present and equal, since the
   evaluator passes a missing digest by design. Add cases to VER-PLG-002
   and VER-PLG-013 for a wrong payload, a different archive, missing
   archive metadata, a tampered bundled wheel, and a failed replacement
   that preserves the previous environment. Keep this inside the plugin
   contract; the generic rule for index installs stays as it is.
4. **Use the documented bootstrap.** Register a shell-form `SessionStart`
   hook that runs the Python handler when the environment interpreter
   exists and reports that setup is required when it does not. The handler
   still performs the identity and installation checks; an interpreter's
   existence is not readiness. Write that route into ARCH-PLG-002 and the
   two activation specifications, re-word DEC-PLG-001 and DEC-PLG-002 from
   "which mechanism" to "does the documented route hold on this host", and
   re-scope the "no custom command wrapper" sentence to no launcher binary,
   no `PATH` lookup, no second protocol. Keep both probes if two evidence
   sets are wanted.
5. **Finish "covers".** Add one shared table to SPEC-PLG-010 naming, for
   each kind of decision (definition approval, work-order start and
   continuation, assurance, external action), which of scope, content,
   candidate, destination, gates, and authority invalidate it and how each
   is compared. Add tests for invalidated decisions. Ordinary edits inside
   an approved scope do not re-open the approval.
6. **Align scenarios 14 and 15 with Release sequences.** Add the release
   unit, the publication rehearsal as the build of record when there is no
   Docker engine, the merge of the released record, and the latest
   markers.
7. **Re-baseline the notes** to `fae52e1b`, or add a short delta box to each
   of the four note pages listing what changed between the two baselines.
8. **Seed DEC-PLG-005 with the numbers above, as a baseline, not a
   limit.** Single warm runs on one repository: two seconds per covered
   edit and three at session start. The profile sets the repetitions, the
   conditions, and the aggregate.
9. **Merge only where the work is one change.** The copied columns
   (REQ-PLG-006 and 007, REQ-PLG-008 and 009, with their specifications,
   contracts, and work orders) can become one artifact each with a host
   parameter; the three specifications restating the lock rule can cite
   one; WO-PLG-013 and WO-PLG-002 edit one skill file and one procedure.
   How many packets remain is the owner's call. The duplication is not.
10. **Give every verification case an observable.** For the 32 cases in
   the appendix, and for any of the further 25 a reader judges vague, add
   the starting fixture, the action, the observable result, and the
   retained evidence. Use a diagnostic code where the evaluator defines
   one; a host demonstration names the host's denial and the unchanged
   target hash instead. A contract that cannot be failed cannot be passed
   either.

## How the PR #360 review findings fared

| Finding on PR #360 | Status in PR #416 |
| --- | --- |
| 1. Approve, verify, and decide flows assumed a protected decision service that does not exist. | Fixed. The service is gone; each scenario names the gap and issue #347. |
| 2. Runtime provisioning must bind the wheel digest and record the archive pair. | Partly fixed. The offline install of the supplied wheel is a rule; comparing its digest is not, and the evaluator passes a missing digest by design. |
| 3. The release scenario omitted the release unit, the build of record, the merge to `main`, and the latest markers. | Partly fixed. The candidate replay and publication workflow are named; the release unit, the rehearsal as build of record without Docker, the merge to `main`, and the latest markers are still absent. |
| 4. Two proposals edited a hash-locked skill and wrote under `.codex/agents/`. | Mostly fixed. The adapted skills live in the plugin. Codex registration in the repository is still described. |
| 5. Smaller factual points (delegation recheck, undefined "covers", supersession, LF header, candidate commit, stop tables). | Partly fixed. "Covers" has its dimensions in PLG-CHANGE-004 but not their comparison; the rest are corrected or removed. |
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
| Index and glossary edits | 4 | 23 | n/a |

## Appendix: verification cases naming no observable

Method: every case in the sixteen contracts was inventoried, 51 items from
the requirement-to-evidence matrices of VER-PLG-001 to 010 and 27 numbered
acceptance scenarios from VER-PLG-011 to 016. A case counts as observable
when its text or pass condition names a tool or command word, a path or
filename, a byte, digest, hash, version, or payload comparison word or
"unchanged", "identical", "sentinel", an exit or diagnostic code, a numeric
unit, or a lifecycle state in backticks. That rule is generous on purpose.
It finds 46 observable and 32 not. The 32 follow; the pass condition is the
matrix column, empty for numbered scenarios.

| Contract | Requirement | Case text | Pass condition |
| --- | --- | --- | --- |
| VER-PLG-001 | REQ-PLG-002 | Both host outputs | Shared files agree with source; divergence and path escape refused. |
| VER-PLG-001 | REQ-PLG-002 | divergent common files | Shared files agree with source; divergence and path escape refused. |
| VER-PLG-001 | REQ-PLG-002 | unsafe path | Shared files agree with source; divergence and path escape refused. |
| VER-PLG-002 | REQ-PLG-003 | Supported Python | Supported setup proceeds; every missing prerequisite produces guidance without Python installation. |
| VER-PLG-002 | REQ-PLG-003 | missing, old, or incomplete Python | Supported setup proceeds; every missing prerequisite produces guidance without Python installation. |
| VER-PLG-002 | REQ-PLG-004 | Offline setup | Supplied wheel installs externally; no network request or checkout mutation; incomplete environments stay unav |
| VER-PLG-002 | REQ-PLG-004 | network disabled | Supplied wheel installs externally; no network request or checkout mutation; incomplete environments stay unav |
| VER-PLG-002 | REQ-PLG-004 | interrupted installation | Supplied wheel installs externally; no network request or checkout mutation; incomplete environments stay unav |
| VER-PLG-005 | REQ-PLG-008 | Accepted activation | Shared skills and scripts run through accepted bindings; invalid or incomplete integration never reports readi |
| VER-PLG-005 | REQ-PLG-008 | malformed event | Shared skills and scripts run through accepted bindings; invalid or incomplete integration never reports readi |
| VER-PLG-005 | REQ-PLG-008 | absent binding | Shared skills and scripts run through accepted bindings; invalid or incomplete integration never reports readi |
| VER-PLG-005 | REQ-PLG-008 | script failure | Shared skills and scripts run through accepted bindings; invalid or incomplete integration never reports readi |
| VER-PLG-006 | REQ-PLG-009 | Accepted activation | Shared skills and scripts run through accepted bindings; invalid or incomplete integration never reports readi |
| VER-PLG-006 | REQ-PLG-009 | malformed event | Shared skills and scripts run through accepted bindings; invalid or incomplete integration never reports readi |
| VER-PLG-006 | REQ-PLG-009 | absent binding | Shared skills and scripts run through accepted bindings; invalid or incomplete integration never reports readi |
| VER-PLG-006 | REQ-PLG-009 | script failure | Shared skills and scripts run through accepted bindings; invalid or incomplete integration never reports readi |
| VER-PLG-007 | REQ-PLG-012 | Output limit | Changed content is rejected and reverified before readiness. |
| VER-PLG-009 | REQ-PLG-015 | customized managed file | Only the reviewed authorized installer operation changes the target; conflicts preserve files. |
| VER-PLG-010 | REQ-PLG-018 | Covered continuation | No duplicate prompt for covered work; affected unauthorized work stops. |
| VER-PLG-010 | REQ-PLG-018 | changed scope | No duplicate prompt for covered work; affected unauthorized work stops. |
| VER-PLG-010 | REQ-PLG-018 | missing authority | No duplicate prompt for covered work; affected unauthorized work stops. |
| VER-PLG-011 | - | Retain actual successful and failed results, including the exact candidate. |  |
| VER-PLG-011 | - | Dirty-candidate capture fails. Successful required-assurance capture binds the earlier clean committed candidate; a later governance commit retains the VREC without rebinding it. |  |
| VER-PLG-012 | - | Implicit briefing stays inactive; valid explicit input produces existing schemas. |  |
| VER-PLG-012 | - | File, lifecycle, network and credential effect sentinels remain empty. |  |
| VER-PLG-013 | - | Provided Python prepares an empty replacement before selecting it. |  |
| VER-PLG-014 | - | Bounded investigation returns sources and uncertainty; unrelated findings do not become blockers. |  |
| VER-PLG-014 | - | Host controls deny file mutation, privileged tools, credential access and publication. |  |
| VER-PLG-014 | - | Findings cannot approve a VREC or replace the assurance owner. |  |
| VER-PLG-015 | - | Missing coverage or samples remain visible; untested combinations gain no support claim. |  |
| VER-PLG-015 | - | A closed decision selecting preview-only cannot produce qualification acceptance; the governing artifacts require appropriate disposition or amendment. |  |
| VER-PLG-016 | - | Unavailable releases and untested hosts remain prospective or unsupported. |  |

## Reassessment at c5c3c7c4

PR #416 was revised to `c5c3c7c4` in answer to this note and the discussion
under it. This section judges that commit alone. Its base is still `main` at
`fae52e1b`; `main` has since moved 33 commits to `560973cf`, and the two merge
without conflict or overlapping files.

### What was checked again

- The released 0.16.0 evaluator on the head: 1,512 artifacts, 0 errors, 44
  warnings, 0 advisories; 97 doctor checks; the 17 documentation tests pass.
- The delivery note's groups D01 to D04 were rehearsed here in scratch
  worktrees, on `fae52e1b` and on live `main`, each group as a real commit
  over the previous one: `harnessctl validate` and the scope checkpoint of
  the selected work order against the prior commit. Both bases: 0 errors,
  no scope blocker, changed paths 8, 4, 13, and 27.
- The 130 verification rows were inventoried with the same mechanical rule
  as the appendix: 96 name an observable in the result cell, 34 do not, and
  no evidence cell is empty. Six probe rows carry an "or the probe records
  the incompatibility" escape.
- The vendor pages for hooks were read again for what a host does when a
  hook times out or fails to start.

### Scores, previous to revised

| Axis | Before | Now | Why |
| --- | ---: | ---: | --- |
| Problem fit and value | 8 | 8 | Unchanged. |
| Architecture | 8 | 8 | The activation route is now in ARCH-PLG-002 and two adapter rules; the unready guard is fail-open by rule, which matches the host's documented default. New: the host proceeds when a before-tool hook times out or cannot start, so the hook layer is best-effort in a second way the contracts do not yet name. |
| Authority and trust boundary | 7 | 8 | The wheel digest is compared and the observation must be present (PLG-ENV-005, ENV08); "covers" has its comparison table; the fail-open window is stated, not hidden. The #347 gap is unchanged by design. |
| Host-platform accuracy | 7 | 8 | The documented bootstrap is adopted and the two decisions ask the right question. VER-PLG-008 C03 still expects a timed-out check to prevent the effect, which the host does not do. |
| Absorption of the PR #360 review | 6 | 8 | Finding 2 is now a rule with cases; finding 3's four items are in scenarios 14 and 15; the repository `.codex/agents/` writes are gone; "covers" is defined; one baseline. |
| Packet quality | 6 | 7 | Every contract is a fixture, action, observable, evidence table with a named evidence file; the share of rows without a named observable fell from 41% to 26%. What remains is self-report: about a dozen rows whose observable is the handler's own statement about coverage or readiness. The copied host columns stay by choice. |
| Decomposition and delivery plan | 4 | 6 | A route exists, is written down, and rehearses clean here on both bases. Its price is one 27-artifact group and a WO-PLG-007 scope that spans five packages for its lifetime. The evaluator-release dependency behind DEC-PLG-004 is now visible and the setup sequence is stated. |
| Mergeability and process conformance | 3 | 6 | Closed groups with one selected work order each, scopes naming exact files, index and glossary carried by D01. Not yet shown end to end: review preflight needs the approvals, and the umbrella PR stays unmergeable by design. |
| Readability and size | 4 | 4 | One baseline, less repeated setup prose, the lock rule in one place. Against that, 61,000 words to review, up from 51,000; the verification tables account for most of the growth and earn it. |
| Honesty of claims | 9 | 9 | Every figure reproduced again, including the rehearsal. The reply names its own limits before being asked. |

### Blockers, apart from readability

Each item names the artifact and the change that would clear it.

1. **A timed-out or unstarted before-tool hook does not block.** Claude
   Code documents that a command hook on `PreToolUse` defaults to 600
   seconds, and that a hook which reaches its timeout, or fails to start
   (a missing interpreter exits 127), renders no decision: the call
   continues through the normal permission flow. VER-PLG-008 C03 expects
   "times out, or is interrupted" to end with "no target effect occurs";
   PLG-HOOK-002 says "translate failure into host refusal". Neither holds
   on a timeout unless the handler owns the deadline. Fix: a rule in
   SPEC-PLG-008 that the handler enforces an inner deadline shorter than
   the host's and exits 2 with a reason when the evaluator has not
   answered; a case in VER-PLG-008 with a deliberately slow check that
   still ends in a host refusal; and a rule in SPEC-PLG-005 and 006 that
   the registered guard command must start on every supported platform,
   since a mistyped path leaves the gate silently disabled. Blocks the
   adapter and tool-hook contracts (D04), not the probes.
2. **Self-report observables.** VER-PLG-008 C05 and C07, VER-PLG-015 C01
   and C08, and VER-PLG-011 EVD02 to EVD04 pass when the handler's output
   says the right thing about itself. Pair each with the external state:
   the effect count and target hash for coverage claims, the lifecycle
   state read back by `harnessctl check` for readiness claims. Blocks
   approval of those contracts.
3. **Governed writes during the unready window are stopped by nobody in
   the rules.** PLG-CDXA-008 and PLG-CLCA-008 make the guard fail-open,
   correctly. SPEC-PLG-010 and SPEC-PLG-011 have no rule that the skill
   refuses governed writes while readiness is unestablished; the notes say
   it, the contracts do not. One rule in each closes the window at the only
   level available.
4. **The probe contracts cannot fail on host behaviour.** VER-PLG-003 and
   004 C01, C03, and C04 accept "or records the incompatibility" as a pass.
   That is right for a probe, and it should be said: the pass condition is
   completeness of the observation record, judged against PLG-CDXP-006 and
   007, not the host's answer. One sentence in Independence. Blocks
   nothing; fix before the owners read D01.
5. **The engineering index will link to notes that are not on `main`.**
   `docs/engineering/plugin-integration/README.md` links to the proposal,
   the operation map, and the scenarios; D01 carries only the delivery
   note. Land the four proposal notes first under the notes-only exception,
   or trim the D01 slice of the index. Small.
6. **Merge `main` into the umbrella before cutting D01.** Thirty-three
   commits behind, clean merge, no overlapping files. Routine.

### Readability, not blocking

- Sixty-one thousand words. The delivery note and the 130 rows are worth
  their cost; the seven explanations of the shell guard in one scenario
  file are not.
- The comparison table in SPEC-PLG-010 is normative and sits under Terms.
  The repository's shape puts what a verifier tests under Rules.
- The two probe columns and the two adapter columns still differ only in
  host names. The author keeps them for separate evidence sets; that is a
  defensible choice and the duplication is now a known cost rather than an
  accident.

### The 11-group route and its 27

The route is sound and reproduces. Its cost is real and bounded: WO-PLG-007
carries 27 files for its lifetime, including the definitions of four sibling
packages, and WO-PLG-001 carries WO-PLG-002's. That is the ordering this note
called "the first" applied to two subgraphs instead of the whole domain, and
it is a fair trade for closed groups with no relation surgery. One
alternative is worth pricing: ARCH-PLG-002 spans host-neutral scripts
(packages 07 and 08) and host-specific adapters (05, 06, 14). Splitting it
along that seam, which the proposal itself draws as one engine and two
adapters, would give two groups of about 14 and 15 and halve the largest
scope, at the cost of a second architecture record and ADR. Whether the seam
is real enough to carry an architecture boundary is the technical owner's
call.

### Are the two probe packages ready for their owners?

Yes, with the two small edits above. REQ-PLG-006 and 007 are one EARS
sentence each and derive from an existing capability. SPEC-PLG-003 and 004
have seven rules apiece including the guard before and after setup and
after interpreter removal. VER-PLG-003 and 004 have seven cases with named
evidence files, and C07 requires real setup through host tools with hooks
registered and a governed write attempted while unready, which is the
right test of the fail-open choice. WO-PLG-003 and 004 depend on no other
packet and may end in an evidenced incompatibility. Start preflight on
WO-PLG-003 reports only the expected draft-state diagnostics. Before the
owners read them: add the one-sentence pass-condition statement (item 4)
and, if the four proposal notes have not landed, trim the D01 slice of the
engineering index (item 5). A better score is not approval; the owners
decide.
