# Failed content diagnostic and next proposal — 10 October 2026

**The wording trial failed.** The three guidance files have been restored to their
previous exact bytes. Failed candidate and evidence remain in history. WO-HAG-011
is **in progress**. No completion, verification or merge readiness is claimed.

Tested candidate: `0d896137bca8791e7d4b17002c1e814915f184a8`.
Restoration commit: `a6d85f8d7431728e13bf39b5c48c90f064cd0656`.
Restored source: `7387bead4d2483650042f8a26a0aec0a55f99ccb`.

## What was tried

Move the distinction between existing records, their status and unknown facts
before mutation. Make the content review check claims against inspected sources.
Ask for grouped reads and replace repeated report prose with a pointer.
The three Markdown files decreased by 803 bytes and 116 words in total. The
released rules, original task, model, permissions and test criteria did not change.
This small reduction was not a solution to context or duration.

## Observed native result

| Trial | Case | Content result | Seconds | Native calls | Peak input tokens |
| --- | --- | --- | ---: | ---: | ---: |
| [Claude101](claude-101-assessment.json) | EFF-04A, missing input | Fail | 256.740 | 18 | 55,067 |

The agent claimed “Complete” with no required content findings. It invented
“rehearsal confidence” as an operational benefit and asserted that downstream
activities could not establish a known baseline without recorded confirmation.
Those claims were not supplied by the request or inspected definitions. It treated
the binary fixture-output confirmation as an operational observation, which does
not satisfy the accepted missing-input criterion.

There were nine Read calls, one Skill call, six Bash calls and two Write calls
across fourteen model turns. No failed native call or repeated read path was
observed. The requested grouped read was not used. It read the code and existing
intent, but did not read the requirement, specification or verification record.
This absence matters when assessing its coverage claims.

The independent service read matches the submitted document exactly. All seven
imported records are unchanged; final project version is four. Correct storage
does not establish correct content. Exact saved revision, document digest and
findings are in the assessment and retained archive.

The [visible transcript](claude-101-visible.md), [native evidence archive](claude-101-evidence.zip)
and [inventory](claude-101-inventory.json) retain public actions and results.
Eleven private reasoning blocks and 106 non-message events were omitted from the
visible export; raw host events remain local. No credentials are published.

## Comparison limits

The [previous candidate](inputs-qualification-assessment.md) took 304.362 seconds,
19 calls and 59,565 peak input tokens for its negative Claude diagnostic. It also
failed, but reported incomplete input. The latest trial regressed to a false
complete claim. These are individual runs on different candidates; their lower
costs are not an efficiency success or a repeated-run benchmark.

The reference goals remain below 180 seconds, at most 15 calls and below 40,000
peak input tokens. The diagnostic exceeds all three, but those positive-authoring
goals do not make a refusal equivalent to a complete draft. No positive repetitions
or Codex trial were run on this failed candidate. Previous Codex CLI results remain
bound to their candidate and environment.

## Supporting checks and evidence

- Native support tests: 25 passed.
- Source suite: 1,336 tests reported, 24 skips, exit zero. The expected negative
  worker-count diagnostic appears in stderr; it is not a suite failure.
- Distribution checks, CLI smoke, review preflight and bounded scope passed.
- Released validation: 1,991 artifacts, zero errors and 63 warnings.
- Exact reproducible producer build and installed candidate packaging passed.
- Nine delivered canonical sections match their selected released source. Both
  plugin packages contain the tested guidance. An ambiguous selector was refused.
- Client/server/dependency implementation bytes match candidate15. The new wheel
  has a different archive digest; all 127 member payloads match, while 127 timestamps
  differ. Earlier EFF-02/03 evidence is reused only for unchanged runtime contents.
- The owned trial containers were stopped and their volume retained. No active
  desktop app was terminated or restarted.

Actual commands, exits, outputs, component identities, restore proof and failed
assumptions are in [candidate16-checks.zip](candidate16-checks.zip), with the
[digest inventory](candidate16-checks-inventory.json). Restoration changes only
the three files to already-tested prior bytes. No accepted definition was changed.

## Concrete next proposal

Review the [complete-input proposal](input-delivery-20261010/review.md): assemble
the entire operator-selected small fixture with exact applicable instructions
and tool references into one bounded initial entry. Keep the answer and all
workflow choices with the native agent. This may reduce discovery turns; it does
not guarantee semantic correctness or lower context. The linked SPEC/VER/WO copies
are proposed and unapplied. No positive criterion, permission or governor changes.

## Delivery and current lifecycle

Draft PR #543 remains targeted at main. At remote head `7387bead`, completed source,
package, Windows/Linux upgrade and integration, publication rehearsal and CodeQL
checks passed. Release rehearsal legs were skipped. The harness validate check
failed; the prior full-base check reports `WO-HAG-009: QGP-G4I-EVIDENCE` for missing
handoff evidence at formal snapshot
`0c071d984c25a89347428d3476346c12385e221b336e629fed1abd99ecf5141e`.
Keep that blocker visible; this diagnostic does not complete host qualification.

The released checkpoint-free result for WO-HAG-011 reports `in_progress`, procedure
`PROC-WO-IMPLEMENT`, next step `STEP-WO-IMPLEMENT-CHECK`. Required native content
checks still fail, so no completion or verification decision is requested.
