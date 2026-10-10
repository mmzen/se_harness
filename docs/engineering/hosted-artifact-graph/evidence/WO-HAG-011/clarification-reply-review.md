# Review: complete the clarification reply at its current step

The [previous trial](clarification-report-assessment.md) asked the required
outcome questions but omitted its no-attempt statement. It also reopened supplied
scope limits. Its failed verdict remains unchanged.

Move the existing clarification-report rule beside the clarification stop. Use
three short parts: actual attempted changes/failures, known inputs, and unanswered
questions. The later report section points back to that rule instead of
copying it. This makes the existing completion duties visible at the current step.

Only `plugins/verity-plane/common/skills/change/references/hosted-drafts.md` changes. Formal definitions, requested outcomes, criteria, task
template, permissions and post-mutation recovery duties remain unchanged.
The guide changes from 1057 to 1075 words and
7598 to 7735 bytes. No command, file format,
new required fact, checker or dependency is introduced. The three labels are a
writing aid, not new word-matching pass criteria.

Existing WO-HAG-011 authority covers this instruction edit. mmzen's “Ok go” after
the published result requests this correction and the existing one-Claude-first
qualification sequence. No accepted-definition amendment is needed.

Before: `c43079cf9bbecf9d99365be8ab92e80457aa0d7e3d67cef3d51337e389665ac5` at `1250208212f6254da70593d8a6eb275a4f6f5405`.
Proposed: `979ffa4f803da8aae152c55b97d18abaa1f76efc827f8ffd7bfa458462f6c282`.

```diff
--- a/plugins/verity-plane/common/skills/change/references/hosted-drafts.md
+++ b/plugins/verity-plane/common/skills/change/references/hosted-drafts.md
@@ -14,8 +14,17 @@
 Use its requester-confirmation process and reuse an existing matching confirmation.
 An instruction to create a draft does not supply the inputs that procedure requires.
 Do not import, open a draft context or create a template merely to ask a question.
-If the requester is unavailable, report the unanswered questions using the
-clarification branch in **Report and recover**. This adds no lifecycle checkpoint.
+For a clarification stop, include three short parts in the final reply:
+
+- **Actions:** State whether any hosted change was attempted. Include observed
+  failures or denials.
+- **Known inputs:** Keep existing definitions and supplied scope limits.
+- **Questions:** Ask only for missing facts needed now.
+
+This retained reply is the transient report only if no hosted mutation command
+was invoked. Refused or denied mutation commands are still attempts. Missing
+observations do not prove that none occurred. Otherwise use **Report and recover**. The clarification reply
+needs no duplicate file or new lifecycle checkpoint.
 
 For a requested intent, consult `docs/engineering/ARTIFACT_AUTHORING.md#intent`
 when identifying missing content. Read other prerequisites when their stated
@@ -92,15 +101,10 @@
 
 ## Report and recover
 
-For a clarification-only stop before any hosted mutation command was invoked,
-use the retained final reply as the transient report. State the missing inputs
-and questions, that no hosted change was attempted, and any observed failures or
-denials. No duplicate file is needed. A refused or denied mutation command is
-still an attempt; missing observations do not prove that none occurred.
-
-Otherwise retain complete requests/results and one short report outside the
-repository, including after a mutation attempt or uncertain effect. Read required
-omitted findings. The report contains:
+For the clarification reply, use **Select the current step**. Otherwise retain
+complete requests/results and one short report outside the repository, including
+after a mutation attempt or uncertain effect. Read required omitted findings.
+The report contains:
 
 - **Content readiness:** complete, incomplete or blocked against the selected
   type checklist. Give the supported content or exact missing input; saving alone
```

Review result: unchanged content checks and report-form eligibility; one rule
moved to its point of use. Retain actual scope, validation, package and native
results. Stop after a failed first Claude case. Earlier evidence remains intact.

Applied exactly as reviewed at 2026-10-10T09:54:04.409841+00:00.
Native qualification is pending.
