# Review: restore clarification before drafting

**Recommendation:** Route an unconfirmed change through the existing clarification
procedure before loading drafting instructions. Keep the approved EFF-04A2 request
and pass criteria unchanged. No new approval, semantic grader, command or lifecycle
checkpoint is proposed.

## Evidence and diagnosis

The [failed first trial](../new-request-qualification-assessment.md) received nine
canonical sections, but none from DEFINE_CHANGE.md. Its hosted guide selected
DRAFT_DEFINITIONS.md directly. That procedure requires a **confirmed outcome,
scope limits and missing-definition list** as inputs. The request did not identify
the new audience or its agreed outcome and measure.

Released 0.22.1 already provides DEFINE_CHANGE.md / **Describe the intended outcome**.
It requires clarification and requester confirmation before dependent definitions,
allows reuse of an existing confirmation, and creates no formal artifact.
This is an existing prerequisite, not a newly invented gate.

The [visible transcript](../claude-151-visible.md) shows the early commitment:
at event 29 Claude says it needs to import and then create the intent. It later
completes the template without any requester question. The saved report calls all
checklist items complete. This establishes the wrong observed route; it does not
prove that routing is the sole cause or that the proposed correction will pass.

## Concrete change

The [exact proposed guide](hosted-drafts.proposed.txt) and [diff](proposal.patch)
change only **Select the instructions** into **Select the current step** in
`plugins/verity-plane/common/skills/change/references/hosted-drafts.md`.
The remaining input checks, authoring, evidence and recovery text stays byte-identical.

| Situation | Procedure | Result |
| --- | --- | --- |
| Outcome or scope needs clarification | Existing DEFINE_CHANGE.md current step | Questions and transient confirmed context; no dependent artifact write |
| Outcome and scope are already confirmed | Existing DRAFT_DEFINITIONS.md current step | Draft the selected definition |
| A needed answer is unavailable | Retain and report the exact missing input | Wait for the requester; do not invent an answer |

No extra confirmation is requested for information already confirmed. The initial
request can supply known facts and constraints; it cannot supply missing ones.
The change does not require explicit stakeholder input for each agent-chosen
verification method or evidence filename that existing scope permits.

The existing test runner already accepts explicit canonical section selectors.
For the new-change entry, select COMMUNICATION, DEFINE_CHANGE entry conditions,
**Describe the intended outcome**, and the requested intent checklist. Load scope,
artifact-selection and drafting sections only when their inputs and conditions
apply. Keep the entire original source fixture. Do not add expected questions,
an answer, a negative-case label or an operation sequence to the task.

This changes the initial instruction route, not the task or native agent's freedom
to choose operations. The positive verification-contract task remains unchanged;
its supplied outcome, governing requirement and constraints must not trigger a
blanket clarification stop. Its applicable drafting instructions remain required.

## Context and KIS assessment

The proposed initial canonical sections total **4,989 bytes**, compared with
21,262 in the previous entry. These are complete canonical sections, not summaries.
The omitted drafting material stays available and becomes required when its step
applies. Conditions on the artifact/link references are preserved.

The guide grows from 825 to 986 words
(5,996 to 7,129 bytes). That is a real
maintenance cost. It makes the existing stage boundary explicit while allowing
much larger future-stage sections to stay out of the initial context. Total entry
bytes, context tokens and duration require a fresh measurement; the canonical-byte
projection is not a performance result.

No new file, state, dependency, helper layer or test framework is needed in the
product. The runner needs no new option. A missing-input result should avoid the
import, draft-open, create, revise and saved-draft read operations entirely; that
is an expected consequence of no artifact output, not a measured call reduction.
Retain necessary service identity, source reads and truthful observation reporting.

## Scope and validation plan

This fits WO-HAG-011's approved plugin Markdown and native qualification scope.
No REQ/SPEC/VER/WO amendment or new decision right is proposed. This directory is
review evidence only; no product or accepted formal definition has changed.

1. Review the exact guide against the released procedures. Check each destination
   and conditional prerequisite. Do not replace canonical content or test meanings.
2. Apply the in-scope guide edit and current-stage section selection. Run relevant
   package/resource checks; reuse unchanged checks only with exact byte comparison.
3. Build the exact candidate. Run one fresh Claude EFF-04A2 with the **same request**,
   complete original fixture, model, permissions, independent assessment and stop rule.
4. If it fails, retain the result and stop before another variation. If it passes,
   run the required Codex A2 and existing positive sequence. Report costs separately.

The proposal does not qualify the original historical task, waive a criterion,
accept a failed host, complete the work or authorize merge. Full WO-HAG-009/010
qualification remains separate. The change targets one observed discovery defect;
reliability remains unproven until actual tests pass.
