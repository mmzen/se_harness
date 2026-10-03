+++
id = "DEC-RLS-008"
type = "decision"
title = "Use the tested Claude public-installation routes in current claims"
status = "decided"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"

kind = "question"
question = "May current coverage statements cite the passing post-release Claude fresh-install and 0.2.4-to-0.2.5 update routes while retaining every untested scenario?"
raised_by = "Codex"
recommendation = "record-tested-subset"

[[options]]
id = "record-tested-subset"
label = "Use the exact observed passing subset in the supplemental coverage report and current guidance; retain remaining gaps and original records."

[[options]]
id = "wait-for-full-matrix"
label = "Retain the new observations but defer changes to current coverage claims until the remaining host matrix is assessed."

[relations]
concerns = ["DEC-RLS-006", "RISK-RLS-005", "WO-RLS-038", "VER-RLS-002", "SPEC-RLO-006", "VER-RLS-035", "WO-RLS-036", "VREC-PLG-033"]
blocks = ["WO-RLS-038"]

[disposition]
option = "record-tested-subset"
label = "Use the exact observed passing subset in the supplemental coverage report and current guidance; retain remaining gaps and original records."
decided_by = "mmzen"
decided_at = "2026-10-03T09:45:24Z"
reason = "Human mmzen replied \"I approve\" to the prepared package request: choose record-tested-subset for DEC-RLS-007 and DEC-RLS-008; approve WO-RLS-038 and VER-RLS-002 with required commit-bound verification; correct the six scoped guidance files while preserving remaining gaps and historical records; permit ordinary pushes from work/claude-025-evidence-followup and a draft PR to mmzen/se_harness:main, including the later verification-decision push. Verification acceptance and merge remain separate. Codex applies the human decision. Reviewed SHA-256 72e409f86d308c41a2b47a76dd92a2ed0cf944973df6b3ad13e872ac5f6d4d05."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-10-03T09:45:24Z"
decided_by = "mmzen"
reason = "Human mmzen replied \"I approve\" to the prepared package request: choose record-tested-subset for DEC-RLS-007 and DEC-RLS-008; approve WO-RLS-038 and VER-RLS-002 with required commit-bound verification; correct the six scoped guidance files while preserving remaining gaps and historical records; permit ordinary pushes from work/claude-025-evidence-followup and a draft PR to mmzen/se_harness:main, including the later verification-decision push. Verification acceptance and merge remain separate. Codex applies the human decision. Reviewed SHA-256 72e409f86d308c41a2b47a76dd92a2ed0cf944973df6b3ad13e872ac5f6d4d05."
+++

# Use the tested Claude public-installation routes in current claims

## Question and evidence

May current coverage statements cite the passing post-release Claude fresh-install and 0.2.4-to-0.2.5 update routes while retaining every untested scenario?

Claude installed plugin 0.2.5 from the public plugin-marketplace branch in a fresh profile and updated a preserved actual public 0.2.4 installation. Both resolved public commit 7d30907f15bd7e06fb632e1ebf4e88e01b68726c; all 29 installed files matched the qualified package and the package used by the native traces.

The [retained observations](../evidence/WO-RLS-038/README.md) identify Claude Code
2.1.273 on Windows, plugin 0.2.5, evaluator 0.22.0 and the exact public package.
These are later observations, not evidence that the original release tests ran.

## Recommendation

Choose `record-tested-subset`. It replaces the current blanket untested statement
with a dated, bounded account. `wait-for-full-matrix` keeps observations available
but delays their use in current coverage statements.

## Effect and limits

This is a question about reporting the new evidence. It is not a new deviation,
an amendment to a specification, or a replacement of DEC-RLS-006's release-time
authorization. That decided record is preserved byte-for-byte. RISK-RLS-005 remains
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
