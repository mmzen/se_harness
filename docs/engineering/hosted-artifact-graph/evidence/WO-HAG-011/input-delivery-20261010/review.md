# Proposal: deliver the complete selected inputs once

**Decision requested:** Approve the linked SPEC-HAG-008, VER-HAG-008 and WO-HAG-011
amendment for a bounded complete-input trial, with required commit-bound
verification. This includes manual activation with preserved accepted versions.
The live formal records have not changed. No new decision is requested for work
or publication already covered by WO-HAG-011.

## Why change the structure

The latest [diagnostic](../fact-grounding-assessment.md) failed despite shorter,
more explicit prose. Claude made nine separate Read calls and still invented a
benefit. More reminders have not established a reliable fix.

The current contract allows mechanical file discovery and grouped instruction
views, but prohibits the adapter from preselecting source content. The proposed
revision explicitly permits the complete operator-selected fixture. It keeps the
prohibition on semantic selection and supplying the answer. This is a test-input
change, not a waiver of the content review.

## Smallest implementation

1. Extend the existing qualification entry builder with an explicit complete-input
   option. Copy the entire selected source fixture from its validated inventory.
   Include the selected setup/tool references and existing canonical sections once.
2. Keep native skill loading and original source paths. Adjust the task so content
   already delivered with identity can be reused. No new reader or workflow layer.
3. Keep the entry under 64 KiB. Fail on mismatched, missing, unsafe or oversized
   inputs. Add tests of content identity and these boundaries.
4. Run one fresh missing-input Claude diagnostic first. Stop if content still
   fails. Only a correct result justifies the remaining approved native sequence.

The existing driver, native support tests and task/tool Markdown are already in
WO-HAG-011's paths. The changes are to their approved behavioral constraint.
See [exact proposed changes](proposal.patch), [identities](proposal.json), and the
full accepted/proposed copies in this directory. No source implementation is in
this proposal commit.

## Expected effect and limits

| Problem | Proposed response | What must be measured |
| --- | --- | --- |
| Many discovery reads | Deliver selected setup, tool reference and the complete small fixture together | Calls and wall time; no assumed speedup |
| Repeated content | Deliver each selected section/source once; retain original paths for recovery | Actual duplicate reads and payloads |
| Instruction length | Keep all required sections exact in this trial; avoid another restatement | Initial and peak context, instruction/source bytes |
| Unsupported claims | Put all existing definitions in the initial inspected input | Independent original EFF-04A content review; no guarantee of success |

The fixture contains twelve small source files, including seven formal records.
The builder copies all of them without choosing a relevant subset. More source
content is delivered upfront; context may increase. The expected benefit is fewer
discovery turns and fewer opportunities to miss existing definitions. This is a
testable hypothesis, not a qualification claim.

Shrinking the released artifact-type catalogue is a separate product-policy and
release change. This proposal does not silently remove its required sections.
It also adds no semantic grader, extra agent, new approval framework or hidden
mutation sequence. If complete input still fails, preserve the result and return
the unresolved content limitation for a human decision before further variations.

## Acceptance and authority

Keep the model, original tasks, source bytes, tool capability, permissions,
released governor, independent readback and all content criteria. The goals stay
below 180 seconds, at most 15 calls and below 40,000 peak input-context tokens.
Report new results separately from historical pointer-based trials. No failed,
skipped or unperformed case becomes a pass.

The selected 0.22.1 evaluator has no supported accepted-definition amendment
operation. Apply this linked revision only after the exact human decision, with
the accepted copies and before/after digests retained. No lifecycle event is
rewritten or invented. Human verification, merge and release remain separate.

## Preparation checks

The proposed copies were checked in a disposable exported checkout using released
0.22.1: 1,991 artifacts, zero errors and 63 warnings. The active records
still match the accepted digests. [Review checks](review-checks.json) and
[actual commands/results](proposal-checks.zip) are retained. The existing fixture
contains 12 files (5,490 bytes). A first content-only entry estimate is
58,194 bytes before framing/deduplication; the implemented entry must still enforce
its 64 KiB limit. This is no content, timing or context qualification.
