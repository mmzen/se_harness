# Instruction discovery correction — native rerun assessment

**The proposal is implemented and locally checked, but Claude qualification still fails.**
The corrected field reader works. Moving the reading rules earlier in the skill
did not reliably cause the agent to read the required authoring instructions.
No work completion, actual VREC, verification, merge or release is claimed.

## What changed

The [initial proposal](instruction-discovery-proposal.md) has three main changes:

1. Put the hosted route and current-procedure reading table before local checkout
   guidance in the setup, change and evidence skills.
2. Add a bounded reader for an agent-selected JSON field. Preserve full original
   results, exact field values and source hashes. It chooses no workflow action.
3. Use a small temporary progress note with pointers to original results. It stays
   outside Git and cannot replace current evaluator checks or authority.

The session also denies the non-helper listing commands observed in a prior run.
Normal plugin loading, hooks and permission checks remain enabled. No provider
settings, installed host plugin, decision rights or acceptance criteria changed.

## Rerun results

Both runs used Claude Code 2.1.273 and reported model `claude-opus-4-6`, with
session-local candidate plugin 0.2.7 and released evaluator 0.22.1. Each started
with its own empty private project and the original fixture. They received no
previous trial output, completed requests or supplied workflow sequence.

| Run | Observed result | Meaning |
| --- | --- | --- |
| Opus06 | Stopped after 431.807 seconds. Windows Bash converted a `/field` JSON pointer into a filesystem path before the helper received it. Four accepted draft/import operations were confirmed by exact receipt lookup. | Test-driver defect; no qualification pass. Failure preserved. |
| Opus07 | Stopped after 648.330 seconds. JSON-encoded pointers worked in four native calls. The agent wrote seven completed draft documents and submitted three accepted revisions without reading `ARTIFACT_AUTHORING.md` or its required type guidance. Twelve accepted import/draft operations matched independent receipt lookups. | Instruction-discovery failure remains. No lifecycle request was attempted. |

Opus07 read the candidate change skill, which explicitly names the authoring
resource in its current-task table. Its complete native trace contains no read of
that resource. It also read no released lifecycle procedure. The latter stages
had not started, so this is not evidence of a later approval or verification
violation. The failure is the missing prerequisite for content already written.
The operator stopped only the exact disposable process after identifying the gap.

| VER-HAG-007 case | Latest result |
| --- | --- |
| NQ-01 — Instructions and selected context | Fail: required authoring read absent before completing draft content |
| NQ-02 — Agent-driven lifecycle | Partial draft preparation; remaining lifecycle stages unperformed |
| NQ-03 — Refusals and bounded reads | Reader works; full required refusal and seven-MCP-tool cases unperformed |
| NQ-04 — Unknown reply recovery | Unperformed; no lifecycle reply was dropped |
| NQ-05 — Export, assessment and honest limits | Unperformed; no native exports or final report |

No outside write or non-helper shell command was observed in these two trials.
The real checkout and the selected non-credential host settings matched before
and after each trial. Receipt lookup confirms the recorded draft effects; it is
not independent released lifecycle replay. Historical Codex observations remain
bound to their earlier package and do not qualify these changed instructions.

## Context findings

Opus07 reached an observed input context of **125,505 tokens during draft
preparation**, before any lifecycle action. It had no automatic compaction before
the stop. Its largest tool response was the complete input inventory: 37,719
UTF-8 bytes. It also loaded both command schemas in full. These measurements
show substantial remaining input load.

The four successful field-reader calls returned an exact scalar type or exit
code. They demonstrate the reader, not complete inspection of lifecycle outcomes,
gates or next actions. Reading only an exit code is insufficient for those claims.
No temporary progress note was observed before the stop.

Earlier trials reached larger contexts, but ran longer and performed different
work. **No percentage improvement or end-to-end efficiency gain is established.**
The [metrics](instruction-context-metrics16.json) retain host-reported context
values, output byte counts, compactions, errors and their comparison limits.

## Recommended next correction

Keep the field reader and its Windows correction. Replace the broad discovery
surface with smaller, task-specific inputs before another native trial:

1. **One current-task entry.** Give the selected task one exact instruction
   destination and heading before command-schema material. Keep the remaining
   procedures linked and available. Do not invent another lifecycle or remove
   required references.
2. **Lookup-sized input inventory.** Keep the full inventory as evidence, but
   provide direct path/hash lookup so discovering one file does not load every
   absolute path. Avoid showing duplicate source, selection and inventory data.
3. **Current-operation schema only.** Read the selected operation's exact schema
   section. Keep the complete closed schema available without loading it upfront.
4. **A small result view.** Expose the actual outcome, failures, completeness,
   current procedure and original-result path. These must be exact evaluator
   fields, not a helper-computed next action. Inspect the decoded stdout file,
   rather than treating the command record's escaped stdout string as an object.

This is a proposal for the next iteration, not an implemented provider or protocol
change. Review its exact implementation paths against WO-HAG-009 before editing.
Repeat the discovery case first. Run dependent lifecycle and final-report cases
only after that prerequisite works; preserve every stopped run.

## Checks and identities

- Packaged source and initial correction: `8126918e7406b9630474f9c933bf66cb9eed6a29`.
- Final tested helper/source checkpoint: `3eb7c0c45636726019a765e05f1bed8c42fe2830`.
  Only two test files differ after the package build; the same package bytes were
  used for Opus07. Its selection records the distinction explicitly.
- Nine focused boundary tests pass, including encoded-pointer equivalence and
  invalid-input refusals. A real Windows Bash call preserves the pointer and
  returns the exact selected value. The failing raw/fragment forms are retained.
- The full source suite passed at both checkpoints: **1,323 tests, 23 skips**.
  Distribution validation and CLI smoke passed. Eleven package tests ran with
  one skip for the instruction correction.
- All 183 previously compared runtime files remain byte-identical to the earlier
  qualified Phase 3 source. This preserves that observation's scope; no service
  scenario or native Codex case is claimed as newly rerun.
- Every client, plugin, image, evaluator, fixture and project identity is retained
  in the per-trial assessment and archive. Neither trial created a test Git
  candidate P; actual source C is not fixture S or hosted baseline B.

## Evidence and lifecycle boundary

- [Opus06 assessment](opus06-assessment.json), [archive inventory](opus06-inventory.json), [exact retained inputs and native output](opus06-evidence.zip).
- [Opus07 assessment](opus07-assessment.json), [archive inventory](opus07-inventory.json), [exact retained inputs and native output](opus07-evidence.zip).
- [Independent instruction-read trace](claude-discovery-read-trace16.json).
- [Supporting-check inventory](instruction-discovery-checks16.json) and [commands, failures, checks and receipt comparisons](instruction-discovery-checks16.zip).

WO-HAG-009 and WO-HAG-010 remain `in_progress`. Final handoff and actual VREC
preparation remain incomplete. The released continuation step remains
`PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`; these observations cannot substitute
for its required evidence. PR #543 remains draft. The known CI failure is
`QGP-G4I-EVIDENCE` for the absent final handoff, not an accepted omission.
Git remains authoritative; RISK-HAG-001 and RISK-HAG-002 remain raised.
