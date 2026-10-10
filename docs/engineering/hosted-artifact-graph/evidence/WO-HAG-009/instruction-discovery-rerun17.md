# Focused instruction-discovery rerun

**Discovery improved, but the drafting procedure still did not pass.** The next
proposal is implemented in candidate `bfaa062cec1b993f4b212d51b307486fdc5a756a`.
The fresh Claude run was stopped after it skipped a required template inspection.
WO-HAG-009 and WO-HAG-010 remain in progress. No real VREC is ready.

## Change assessed

The [proposal](instruction-discovery-proposal17.md) adds one current-task drafting
entry, exact file lookup, operation-specific schema views and bounded exact
result fields. The original files, schemas and receipts remain available.
No service behavior, lifecycle rule, required gate or accepted definition changed.

## Observed run: Opus08

Claude Code 2.1.273 used `claude-opus-4-6` and the exact session-local candidate
plugin 0.2.7. Authentication passed a live probe. The diagnostic used a fresh
private project, released evaluator 0.22.1, normal hooks and existing narrow tool
permissions. It received a 4,149-byte task limited to definition drafting.
No completed artifacts, requests or workflow sequence were supplied.

| Area | Actual finding |
| --- | --- |
| Instruction discovery | Setup led to change, then DRAFT_DEFINITIONS.md, ARTIFACTS.md and ARTIFACT_AUTHORING.md before template creation. This resolves the earlier absence of these reads in this run. |
| Procedure execution | The first template-read attempt incorrectly supplied `--key` to `remote read`. The helper refused it. Claude then created three more templates without reading/completing the first. This violates the drafting sequence it had read. The operator stopped the exact disposable process. |
| File lookup | Claude guessed `source/greeting.py`; the exact-name lookup correctly refused it. Claude then loaded the full inventory to find `source/src/greeting.py`. The proposed lookup did not reduce inventory load in this run. |
| Schema loading | Claude read four selected operation views, rather than the complete v1/v2 schemas. It still loaded multiple operations ahead of their use. |
| Result reading | Bounded exact result fields were used. Two successful `read-json` calls inspected actual instruction-discovery and incomplete-authoring fields. Original stdout and command records are retained. |
| Permission boundary | One `ls` attempt was denied. No alternate listing command or outside write was observed. This was an attempted non-helper action, not an executed directory listing. |
| Effects | Six accepted operations: import, draft-context creation, and INT/CAP/REQ/SPEC template creation. All six match independent receipt lookups exactly. No completed draft content, revisions, lifecycle decisions or exports were produced. |
| Duration | Stopped after 546.991 seconds; not a timeout. No automatic compaction or dropped lifecycle reply occurred. |

DEFINITION_LINKS.md was not read, but no authored links were submitted before the
stop. This run does not establish that later prerequisite either way. The failure
reported here is the observed template-reading sequence, not an unperformed stage.

Peak host-reported input context was **96,952 tokens**. The previous Opus07 run
reached 125,505, but the task and stopping point differ. This is **not evidence of
an efficiency percentage**. Full inventory loading and early loading of several
schema views remain concrete context costs. There was no transient progress note.

The real checkout and selected non-credential host settings matched before and
after. The independent observer saw no MCP calls. Six receipt matches establish
the recorded draft effects; they do not establish independent lifecycle replay.

## Checks and exact evidence

- 13 focused helper/schema tests passed.
- Plugin tests: 11 tests, 1 skip, exit 0.
- Source suite: 1,323 tests, 23 skips, exit 0.
- Distribution checks: 23 records, pass; CLI smoke passed.
- 214 JSON Schema checks passed in the service image, including all selected
  operation shapes and observed v1 requests with required-field/extra-field refusals.
- Reproducible client and exact plugin/service packages built successfully.
- Released validation: 1,987 artifacts, zero errors, 63 existing warnings.
- 183 runtime source files match the previously qualified Phase 3 runtime.
  This permits evidence reuse for that runtime; it does not qualify changed guidance.

The first schema unit-test attempt failed because an optional JSON Schema library
was absent from the host. Structural unit checks now need no such dependency;
actual validator checks ran in the service image. Both results are retained.

[Assessment and exact source/component tuple](opus08-assessment.json),
[evidence inventory](opus08-inventory.json), and
[native transcript, inputs, results and supporting checks](opus08-evidence.zip).
Earlier trials remain unchanged in [the previous report](instruction-discovery-rerun.md).

## Recommended next correction

1. Make the hosted template-read route directly discoverable at the creation
   step, including its request shape or read-only MCP entry. Show operation-specific
   help; `--key` belongs to receipt lookup, not an artifact read.
2. Support a bounded filename search when an exact path is unknown. Return
   candidate paths/hashes, never the entire inventory and never an inferred choice.
3. Re-run only create → inspect → complete one draft before another full lifecycle
   trial. Keep the required procedure and failure visible; add no hidden workflow.

These are recommendations, not additional implementation or qualification claims.
The full Claude lifecycle and current-tuple Codex qualification remain outstanding.
No verification, merge, release, deployment, host-plugin update or risk acceptance
is requested or recorded. PR #543 remains an explicitly authorized unfinished draft.
Its known missing final-handoff evidence remains disclosed.

Released continuation remains `PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`.
Complete the missing qualification and evidence before final handoff; the successful
scope-only check does not establish that the work is complete.
