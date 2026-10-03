+++
id = "DEC-RLS-007"
type = "decision"
title = "Use the tested Claude instruction-delivery subset in current claims"
status = "decided"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"

kind = "question"
question = "May current coverage statements cite the passing post-release Claude instruction-delivery subset while retaining every untested scenario?"
raised_by = "Codex"
recommendation = "record-tested-subset"

[[options]]
id = "record-tested-subset"
label = "Use the exact observed passing subset in the supplemental coverage report and current guidance; retain remaining gaps and original records."

[[options]]
id = "wait-for-full-matrix"
label = "Retain the new observations but defer changes to current coverage claims until the remaining host matrix is assessed."

[relations]
concerns = ["DEC-RLS-005", "RISK-RLS-004", "WO-RLS-038", "VER-RLS-002", "SPEC-IAR-016", "VER-IAR-021", "VER-RLS-034", "WO-RLS-035", "VREC-PLG-032"]
blocks = ["WO-RLS-038"]

[disposition]
option = "record-tested-subset"
label = "Use the exact observed passing subset in the supplemental coverage report and current guidance; retain remaining gaps and original records."
decided_by = "mmzen"
decided_at = "2026-10-03T09:44:40Z"
reason = "Human mmzen replied \"I approve\" to the prepared package request: choose record-tested-subset for DEC-RLS-007 and DEC-RLS-008; approve WO-RLS-038 and VER-RLS-002 with required commit-bound verification; correct the six scoped guidance files while preserving remaining gaps and historical records; permit ordinary pushes from work/claude-025-evidence-followup and a draft PR to mmzen/se_harness:main, including the later verification-decision push. Verification acceptance and merge remain separate. Codex applies the human decision. Reviewed SHA-256 97254375cf2cb96002a2871f81a9ba6df409ac810d58c257faf0ac1026330890."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-10-03T09:44:40Z"
decided_by = "mmzen"
reason = "Human mmzen replied \"I approve\" to the prepared package request: choose record-tested-subset for DEC-RLS-007 and DEC-RLS-008; approve WO-RLS-038 and VER-RLS-002 with required commit-bound verification; correct the six scoped guidance files while preserving remaining gaps and historical records; permit ordinary pushes from work/claude-025-evidence-followup and a draft PR to mmzen/se_harness:main, including the later verification-decision push. Verification acceptance and merge remain separate. Codex applies the human decision. Reviewed SHA-256 97254375cf2cb96002a2871f81a9ba6df409ac810d58c257faf0ac1026330890."
+++

# Use the tested Claude instruction-delivery subset in current claims

## Question and evidence

May current coverage statements cite the passing post-release Claude instruction-delivery subset while retaining every untested scenario?

Native startup, activation after cloning, resume, manual and automatic compaction, two-release session isolation, selection switch/clear and unavailable-checkout recovery passed. The complete entry was checked in the native compact hook output, not inferred from model text.

The [retained observations](../evidence/WO-RLS-038/README.md) identify Claude Code
2.1.273 on Windows, plugin 0.2.5, evaluator 0.22.0 and the exact public package.
These are later observations, not evidence that the original release tests ran.

## Recommendation

Choose `record-tested-subset`. It replaces the current blanket untested statement
with a dated, bounded account. `wait-for-full-matrix` keeps observations available
but delays their use in current coverage statements.

## Effect and limits

This is a question about reporting the new evidence. It is not a new deviation,
an amendment to a specification, or a replacement of DEC-RLS-005's release-time
authorization. That decided record is preserved byte-for-byte. RISK-RLS-004 remains
`accepted`; this decision records the partial reduction in uncertainty without
claiming that the full risk is resolved or applying a risk-state transition.

Codex Windows desktop, the full Claude work-order walkthrough and the earlier
long-path case remain unverified. Do not claim the complete Claude contract
passed, extend this result to plugin 0.2.4 or another platform, or resolve
RISK-RLS-006 and local hook-loss limitations from these observations.

mmzen owns follow-up. Before the next plugin release or a broader host-support
claim, assess the remaining cases against exact inputs or obtain the applicable
bounded human decision. Prior revisit triggers and required gates are retained.

## Authority boundary

The human selects the option. Recording it does not approve WO-RLS-038, approve
VER-RLS-002, accept a verification record, authorize publication or merge a PR.
The two question answers and work/verification approval may be supplied in one
explicit package decision. The evaluator writes the disposition.
