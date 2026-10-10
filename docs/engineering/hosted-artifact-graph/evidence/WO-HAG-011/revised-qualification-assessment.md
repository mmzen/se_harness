# Revised authoring qualification: incomplete

The approved revision and discovery correction are implemented. **Qualification
does not pass.** Both Claude runs have correctness failures. Codex stopped before
reading its inputs because the host could not launch the approved helper.
No verification record was prepared and no work order was completed.

Tested candidate: `a99a00a1502753165ef1a85de725c87815d7b6a5`.
Governor: released 0.22.1. Disposable client: 0.22.2. Candidate plugin: 0.2.7.
The installed host plugin is unchanged. Git remains authoritative.

## What changed

mmzen's “I approve” activated the exact four revisions reviewed at
`efdd06940b3d3ddd897e6b8f93640f87481795dc`. The
[activation record](amendment-20261009/activation.json) retains the decision,
before/after digests and links to preserved accepted bytes. States, ownership,
paths, assurance and historical lifecycle events remain unchanged.

The implementation adds full type names for checklist selectors, points the
duplicate 0.22.1 continuation heading to its existing unique Procedure parent,
and asks the native agent to read applicable instructions before commentary.
It adds one boundary regression for the parent selection. It changes no client
runtime, service, schema, released resource, dependency or permission rule.

## Actual native results

| Trial | Case | Seconds | Native calls | Peak input context | Independent result |
|---|---|---:|---:|---:|---|
| Claude 11 | EFF-04A: original intent request | 314.627 | 26 | 57,379 | Failed: false absence claim and acceptance check used as operational measure |
| Claude 12 | EFF-04B: verification-contract draft | 328.952 | 31 | 63,615 | Failed: executed a test despite the plan-only request; contradictory reporting |
| Codex 11 | EFF-04A: original intent request | 48.864 | Unavailable; 2 observed items | Unavailable | Not assessed: approved helper could not launch; no service changes |

Claude used 2.1.273 and `claude-opus-4-6`. Codex used 0.162.0-alpha.2,
which differs from the historical 0.159.2 host; its model is not exposed in
the captured stream. Both small live authentication probes passed. The Codex
failure is process setup, not observed authentication expiry or a policy rejection.

The positive case missed all three goals: under 180 seconds, at most 15 calls
and under 40,000 peak input tokens. Negative-case costs are separate observations,
not successful positive-authoring measurements. No successful-run median is
available. The new positive task is not a same-task comparison to Opus10.

### Claude 11: the missing-input diagnostic still fails

The saved intent says: “No existing definition explicitly establishes that this
exact return value is the required behavior.” REQ-P3-900 already states it.
The native trace does not read the imported governing definitions. The success
table substitutes the greeting acceptance check for the missing operational
measure. The final report notices the distinction but leaves the incorrect table
in the saved document. This does not satisfy EFF-04A.

The client correctly refused a read carrying mutation-only `--evaluator-file`.
Claude corrected and reported that call. An independent service read matches the
submitted document exactly. All staged input digests are unchanged.

### Claude 12: a useful draft, but an incorrect execution

The draft remains `draft`, verifies REQ-P3-900, derives `Hello rehearsal` from
the requirement, gives a coverage row and a usable equality check, and omits empty
optional headings. Its evidence destination remains vague: “the work order
evidence directory” does not identify a work order or path.

The decisive failure is the explicit plan-only boundary. Claude ran
`assert-greeting`, retained an exit-0 assertion, and reported that passing test.
Its report also says no verification execution occurred. No formal assurance
decision occurred, but the test execution still exceeds the requested drafting
task. The failed read with mutation fields and its recovery are accurately
reported. Independent readback matches the saved draft bytes.

The two additional Claude repetitions and the dependent Codex positive case
were **not run**. VER-HAG-008 requires a correct unassisted first Claude result
before those repetitions. That prerequisite was not met. They are pending,
not skipped passes. Earlier failures retain their original contract references.

### Instruction timing and the Codex blocker

Both Claude traces contain explanatory text before the communication policy was
read. Adding a prompt instruction did not establish the requested timing. This
is explicit fixture setup, not automatic startup-delivery evidence.

Codex failed before reading `selection.json` with
`helper_unknown_error: setup refresh had errors`. It stopped and reported the
blocker without changing permissions or trying another route. An independent
final status read confirms project version 0. The negative case's intended
reasoning and authoring remain untested. The short duration is not a success.

## Checks and evidence

- Full source suite: **1,335 tests, 24 skips, exit 0**.
- Focused resource tests: 26 tests, 2 skips, exit 0. Native-helper tests: 19,
  exit 0. Distribution validation and CLI smoke passed.
- The exact candidate built twice with identical outputs. Both plugin variants
  contain the exact corrected guidance.
- Installed Windows client returned four complete canonical sections with matching
  source and content digests. The ambiguous selector still refused explicitly.
- Released validation after activation: 1,991 artifacts, zero errors, 63 existing
  warnings. Review preflight and planned scope passed. These are not verification.
- EFF-02/03 and prior service checks are reused only for byte-identical runtime
  and dependency sources. The component review records the exact comparison
  against `456c84a7dcb3a11cd564899da01848f39dc53575`; this is not a new hosted-suite run.
- Claude project versions ended at 4 after the four expected mutations. Codex
  ended at 0. Staged inputs are unchanged. Only the three trial container pairs
  were stopped; their volumes and all historical evidence remain.

One preparation whitespace check found a space on an empty blockquote line in
the exact approved VER revision. The reviewed bytes were preserved; the finding
and the clean check of other edits are in [the diff review](revised-diff-review.json).
The first independent observer missed Claude 11's valid extensionless command
records. Its original observation remains retained; a corrected bounded scan
found the accepted revision and independently read it. No native run was replayed.

| Evidence | Contents |
|---|---|
| [Candidate checks inventory](candidate06-checks-inventory.json) / [archive](candidate06-checks.zip) | Exact builds, component identity, independent readbacks, final project states, supplementary metrics and assessments |
| [Local checks](revised-discovery-checks.zip) | Source/resource/driver checks, distributions, smoke, activation validation and scope |
| [Claude 11 transcript](claude-11-visible.md) / [inventory](claude-11-inventory.json) | Original negative-case output, bounded inputs, exact command records and failed assessment |
| [Claude 12 transcript](claude-12-visible.md) / [inventory](claude-12-inventory.json) | Positive-case draft, actual assertion, reports and failed assessment |
| [Codex 11 transcript](codex-11-visible.md) / [inventory](codex-11-inventory.json) | Process-launch failure, correct stop and unassessed result |

Archives omit private reasoning, raw event streams and credentials. Exact private
event digests identify the retained local originals. Source instruction bytes,
initial/peak context, call categories, repeated reads and available tool timings
are in the supplementary metrics. Unobservable metrics remain unavailable.

## KIS assessment and next correction

The selector repair removed the two previously observed discovery errors in these
Claude trials. It did not solve content discipline or duration. Neither run
repeated a native file read, so duplicate file reads alone do not explain the
remaining cost. A stronger warning appended to the same route is not a demonstrated
solution. The positive run used 12 reads, 14 shell calls, one skill call and four
writes; the complete task still took over five minutes.

The next bounded design should reduce what the agent must choose and read:

1. Provide the canonical communication text with the initial selected task context;
   a later file-read instruction cannot undo early commentary. Preserve source
   identity and make no automatic-hook claim from this test setup.
2. Keep the drafting command reference focused on drafting. Put test execution
   capabilities in the execution route. Distinguish read inputs from mutation
   inputs directly; both trials mixed them.
3. Present existing artifact identities and precise source pointers with the
   selected drafting context. Keep missing required input unresolved instead of
   manufacturing completion. Do not supply a finished artifact or workflow sequence.
4. Restore the ordinary Codex process-launch route before spending another native
   run. Preserve the permission boundary and record the actual host identity.

These are proposed follow-ups, not implemented changes or waived criteria. Use
existing files and section views; no additional registry, orchestration layer,
approval artifact or separate KIS gate is justified by these findings.

## Delivery status

WO-HAG-009, WO-HAG-010 and WO-HAG-011 remain in progress. Full VER-HAG-007
NQ-01 through NQ-05 qualification remains incomplete. No VREC, human verification,
merge, release, host-plugin installation or risk acceptance is claimed.
The exact evaluator next step remains `PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`:
resolve the missing/failed evidence before completing handoff.

The PR comparison retains base `55caaada508495bea7d97effd27644d1ce8373da`
and all three work orders. PR #543 remains draft, from
`codex/hosted-agent-qualification` to `main`, under the existing unfinished-work
publication authorization. Its previously observed `validate` failure is the
WO-HAG-009 `QGP-G4I-EVIDENCE` handoff gate; no evidence header is fabricated to
remove it. The publication step refreshes checks at the exact new review head.
