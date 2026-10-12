# Command discovery and draft review: correction19 / Opus10

The correction reduced command count and elapsed time in this trial, but did
**not reduce context load or fix final reporting**. Claude created and revised
one intent draft successfully. It then reported zero failures despite four
recorded errors or denials. The draft also retains a writing-guidance gap.
This is a partial diagnostic, not completed native qualification.

## Change and authority

Tested/package candidate: `5f3b8499a5342d38dcce900d395b022039762e50`.
WO-HAG-009 covers the setup/change guidance, the short native tool index,
this focused test and the authorized update of draft PR #543. WO-HAG-010
continues to cover the earlier startup-routing correction.

The setup skill directs restricted tests through their selected helper and
metadata-only identity check. The change skill adds a final content/evidence
review. `tests/hosted_artifact_graph/native-tools.md` lists existing commands,
file naming rules and operation-specific schema locations. The task links that
index instead of scattered tool hints. The helper, schemas, service, permissions,
evaluator policy and requested outcome are unchanged from correction18.
[Proposal](instruction-discovery-proposal19.md) records the bounded correction.

## Actual test

Fresh Claude Code 2.1.273 / `claude-opus-4-6`, session-local candidate plugin
0.2.7, installed client 0.22.2, released evaluator 0.22.1 and a new private
Memgraph project. The live authentication probe passed. The requested outcome,
fixture, model and tool boundary match Opus09. No mid-run coaching, permission
relaxation or operator completion of the native workflow occurred.

| Observation | Independent result |
| --- | --- |
| Component identity | Claude used `identity`; no whole-wheel base64 output. Six reported fixture/component/document identities match their actual sources. |
| Discovery | Ten filename-search attempts: seven returned no matches, two found files, one was denied. It then read the inventory in two calls. Five operation-specific schema views were read. |
| Drafting reads | DRAFT_DEFINITIONS and the design-simplicity/intent checklist were read before authorship. ARTIFACTS was not read; the task had already selected the intent type. No links were authored. |
| Source inspection | Native Read at events 103–104 read `source/src/greeting.py` before authorship. No assertion was executed. |
| Template | Created at 202–203; read at 228–229; exact template decoding at 266–267 precedes authorship at 284–285. Its digest matches the envelope. |
| Draft | `INT-P3-001`, one creation and one revision; final admission has zero errors and zero incomplete fields, with one existing background advisory. |
| Exact readback | Independent service read returns the same 1,283 bytes as the submitted request. Status is `draft`, with no lifecycle history. |
| Receipts | All four accepted mutation receipts exactly match independent operation-key lookup. Project version advances 0 to 4. |
| Boundary | No outside writes; selected checkout and host configuration snapshots are unchanged. The denied call did not execute. |
| Session | Exit 0, 673.18 seconds, no timeout, no compaction. Exit 0 is not a qualification verdict. |

Final document SHA-256:
`526749ab08ee31e1d14b8d8b8365f4d00470a0cd6955ce5f0eb841ec9cce8cdf`.

## Unresolved findings

1. **Failure reporting remains incorrect.** Both final native files omit four
   results: a guessed missing `source/conftest.py`; a denied filename search
   whose helper path used a different slash spelling; and two JSON-pointer
   quoting errors. The native report says "None. All operations returned
   outcome: accepted." The original trace and reports are preserved. The later
   accepted remote mutations do not erase earlier errors.
2. **Content review remains incomplete.** The success measure is
   `greeting() == "Hello rehearsal"`, observed through source inspection.
   The decoded template distinguishes operational success measures from
   acceptance checks or code review. Claude marks its checklist complete
   without reporting this gap. Its claim that no traceable link exists is
   also unsupported by a content read of the imported governing records.
   These are review findings, not fabricated evaluator failures.
3. **Context management did not improve.** The agent read the tool index but
   mixed input-relative names with an `inputs/` prefix and used stems/extensions
   where exact filenames were required. The resulting searches led to loading
   the large inventory. It also initially ignored the documented JSON-string
   quoting and later corrected it. No new service failure was observed.

| Observed metric | Opus09 | Opus10 |
| --- | ---: | ---: |
| Tool calls | 72 | 56 |
| Elapsed seconds | 862.454 | 673.18 |
| Peak input context tokens | 105,696 | 112,326 |
| Peak before first draft-content write | 90,017 | 96,012 |
| Errors or denials | 6 | 4 |

Opus10 used 19 Read, 1 Skill, 26 Bash and 10 Write calls. Input-context values
are the maximum observed sum of input and cached-input fields, not total billed
tokens. This is one observation per version with model variability, not a
general benchmark or proof that the guidance caused every difference.

## Checks and review

- Plugin checks: 11 tests, one skip, exit 0.
- Full source suite: 1,323 tests, 23 skips, exit 0.
- Distribution checks: 23 records, passed. CLI smoke passed.
- Exact candidate packages built through the pinned build route.
- Released validation: 1,987 artifacts, zero errors, 63 existing warnings.
- Scope and diff checks passed. 183 runtime source files match the previously
  qualified Phase 3 source; this reuses that evidence, not a new runtime claim.

No service or schema change was needed. The helper stayed byte-identical to
correction18. The previous 239 schema checks are historical evidence, not a
newly executed check in this correction. The added index has some value for
identity and operation selection, but adding more general prose is not justified
by this result. The new review paragraph was read and did not prevent the two
remaining review/reporting errors.

## Recommended next focus

Make discovery and reporting more direct, without extending the workflow engine:

- Provide exact task-relevant file pointers with the selection, using one path
  convention. Keep file search for genuinely unknown files; keep the full
  inventory as evidence. Do not supply authored content or completed requests.
- Make the report reconcile the actual failed-call evidence before it states
  a failure count. Preserve an independent comparison with the native trace.
- Keep the short template review adjacent to the final draft action. A request
  that supplies no operational success measure should expose that gap rather
  than invent a claim or equate a test assertion with operational benefit.

These are next correction recommendations, not implemented behavior or waived
criteria. Repeat this bounded diagnostic before expanding the full lifecycle.

## Evidence and current state

- [Independent assessment and exact component identities](opus10-assessment.json)
- [Content review, template bytes and reported identity comparison](opus10-review.json)
- [Independent final revision readback](opus10-draft-readback.json)
- [Archive inventory and hashes](opus10-inventory.json)
- [Native transcript, inputs, command records and actual checks](opus10-evidence.zip)
- [Previous trial](instruction-discovery-rerun18.md)

No native MCP calls, lifecycle completion, unknown-reply recovery or exports
were performed. The full NQ-01–05 claim for both hosts remains incomplete.
Earlier Codex evidence keeps its own component identities. Both work orders
remain `in_progress`; no actual VREC or final handoff exists.

The known draft PR Engineering Harness blocker is `QGP-G4I-EVIDENCE`, confirmed
from the previous head's actual CI log. The new head needs its own CI observation.
The unfinished-work update preserves the full comparison base and main target.
No gate is waived.

Released continuation: `PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK` — retain
required implementation evidence and run the bound handoff check when complete.
Git remains authoritative. No assurance acceptance, merge, release, deployment,
host-plugin update or risk acceptance occurred.
