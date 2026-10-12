# Hosted template reading: correction and Opus09 diagnostic

The correction worked for template discovery and revision: Claude read the
generated intent, decoded its exact document, completed it and submitted a
revision that the released evaluator admitted as a draft. The whole diagnostic
is **partial**, because content review and final reporting still have gaps.
Full native qualification remains incomplete.

## Change and authority

Candidate: `a772ea264c7a68cc456a8af7df2ccf3ea3474947`.
WO-HAG-009 permits this bounded guidance/test-driver correction and draft PR
update. WO-HAG-010 continues to cover the earlier bootstrap correction.

- `plugins/verity-plane/common/skills/change/SKILL.md` links creation to an
  exact revision read and completion before the next artifact.
- `plugins/verity-plane/common/skills/harness-orient/SKILL.md` explains the
  versioned read request, exact document decoding and digest comparison.
- `tests/hosted_artifact_graph/native_call.py` adds bounded filename discovery
  and exact selected-field decoding. Neither selects or performs a workflow.
- `tests/hosted_artifact_graph/native_schema.py` exposes the chosen read schema
  branch with its constraints and referenced definitions unchanged.

The service, evaluator policy, protocols and decision rights are unchanged.
[Proposal](instruction-discovery-proposal18.md) records the bounded change.

## Test and independent assessment

Fresh Claude Code 2.1.273 / `claude-opus-4-6`, session-local candidate plugin
0.2.7, installed client 0.22.2, released evaluator 0.22.1 and a fresh private
Memgraph project. Authentication passed a live probe. The task requested one
intent draft only; no other artifacts or lifecycle decisions were requested.
The agent built its own requests. No mid-run procedural coaching or operator
mutation completed work for it.

| Observation | Evidence and result |
| --- | --- |
| Required drafting reads | DRAFT_DEFINITIONS, ARTIFACTS and ARTIFACT_AUTHORING were read before creation and content authorship. No links were added, so DEFINITION_LINKS was not an applicable prerequisite. |
| Fixture inspection | Native Read at event lines 109–110 read `source/src/greeting.py` before drafting. Its staged digest matches. No assertion was executed; this is inspection evidence. |
| Filename discovery | 21 bounded searches; no full inventory read. Five operation-specific schema views were read; no full schema dump. |
| Template reading | Creation at lines 246–247, revision read at 287–288, exact UTF-8 decoding at 294–295, draft authorship at 318–319. The decoded template digest matches its envelope. |
| Draft revision | `INT-P3-001`, one creation and one revision. Admission reports zero errors and zero incomplete items, with one existing background advisory. |
| Independent readback | Final 1,241 bytes exactly match the submitted document and envelope digest. Status remains `draft`, with no lifecycle events. |
| Receipt reconciliation | Independent lookup exactly matches all four accepted receipts: import, draft-open, creation and revision. This is not full lifecycle replay. |
| Boundary | Both outside-prefix shell attempts were denied. No outside write observed. Recorded checkout/host configuration snapshots are unchanged. |
| Native execution | Exit 0, 862.454 seconds, no timeout or compaction. Exit 0 does not establish qualification. |

Final document SHA-256:
`57b267bea065645a6c260f5164c9b11e6be825c9701a700790b406b23030172b`.

The live progress commentary initially missed the source read. The full trace
corrects that observation; source inspection is present. The trace, not that
intermediate statement or the native summary, controls this assessment.

## Remaining findings

1. **Content review:** the intent's success target is “Confirmed by verification”.
   The generated template separates operational success measures from acceptance
   checks. Admission passing does not establish compliance with this writing
   guidance. Its assertion that no formal record exists is also unsupported by
   a content inspection of the imported records.
2. **Incomplete reporting:** the native reports omit six command errors or
   denials. They also give the wrong setup-skill digest: the harness-orient digest
   was copied into that entry. Independent comparison confirms the other five
   reported instruction digests. The original reports remain unchanged evidence.
3. **Setup cost:** peak reported input context was **105,696 tokens**, with
   **90,017** before the first draft-content write. There were 72 tool calls
   (18 Read, 1 Skill, 42 Bash, 11 Write). One wheel-identity attempt encoded the
   entire wheel and produced about 740 KB of tool output, which the host saved
   and previewed. The existing metadata-only `identity` helper was not used.
   The narrower task and different stopping point prevent an efficiency
   percentage comparison with earlier trials. Context reduction is not proven.

The six retained errors/denials are: an unsupported `--sha256-only` option;
a denied direct-client command; denied `ls`/`mkdir`; a missing trailing slash
on `--under`; a nonexistent `/versions` field in status; and `remote read`
without its required request. The last request was `not_sent`. No denied
operation was executed and no permission setting was relaxed.

## Checks and review

- 16 focused helper/schema tests passed.
- 239 schema checks passed against the actual packaged validator.
- Plugin checks: 11 tests, one skip, exit 0.
- Source suite: 1,323 tests, 23 skips, exit 0.
- Distribution and CLI smoke checks passed; exact candidate packages built.
- Released validation: 1,987 artifacts, zero errors, 63 existing warnings.
- 183 runtime source files match the previously qualified Phase 3 source.

Review found no required service or protocol change. The small filename search
and decoder address the observed discovery/read failures without a workflow
engine. Further helper features are not justified by this trial. The remaining
cost is selecting among commands and producing a reliable report.

## Next bounded correction

Reuse the current tools. Replace scattered setup hints with one short tool index
that identifies metadata-only identity checking and the available read/mutation
operation names. Keep exact schema fields outside the initial context. Add a
short completion review to the current drafting route: inspect the requested
source, apply the selected template/checklist, distinguish admission from content
review, and cite observed failures and machine-provided digests in the report.
Do not supply filled requests, artifact content, a workflow script or a hidden
pass. Rerun this one-intent diagnostic before resuming the full lifecycle.

This is the next correction recommendation, not a new implemented claim or a
change to the accepted qualification criteria.

## Evidence and limits

- [Independent assessment and component identities](opus09-assessment.json)
- [Independent review and digest comparison](opus09-review.json)
- [Exact final draft readback](opus09-draft-readback.json)
- [Archive inventory and hashes](opus09-inventory.json)
- [Native transcripts, inputs, command records and checks](opus09-evidence.zip)
- [Earlier trials](report.md)

No native MCP calls, lifecycle completion, unknown-reply recovery or exports
were performed in this focused run. It does not pass NQ-01–05. Prior Codex
evidence keeps its original component identities and does not qualify this
changed package. Both work orders remain `in_progress`; no actual VREC or final
handoff exists. The draft PR's known Engineering Harness blocker is
`QGP-G4I-EVIDENCE`. The authorized unfinished-work update preserves that blocker.

Released continuation: `PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK` — retain
required implementation evidence and run the bound handoff check when complete.
Git remains authoritative. No assurance acceptance, merge, release, deployment,
host-plugin update or risk acceptance occurred.
