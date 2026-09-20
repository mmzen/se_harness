+++
id = "SPEC-KIS-005"
type = "specification"
title = "Use the full current checks before completion"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-19"
updated = "2026-09-20"

contract = "Share selected-scope evaluation across handoff, preview, planning and completion, and re-evaluate current inputs before applying completion."

[relations]
specifies = ["REQ-KIS-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-20T06:27:29Z"
decided_by = "technical-owner"
reason = "On 2026-09-20 the owner approved the presented recovery artifact package with \"i approve\". Record approval of this reviewed artifact in the named owner role. Reviewed full-byte SHA-256: d826f11aa6561653be80bfc0fbeff53ee07ab6f556174c9c60916e4226cb85b6. DEC-KIS-001 separately records the explicit owner-review choice. WO approval grants the bounded execution operations in DR-015; this transition records no implementation result, assurance acceptance or external action."
+++

# Use the full current checks before completion

## Scope

Share selected-scope evaluation across handoff, preview, planning and completion, and re-evaluate current inputs before applying completion.
This is the prospective contract for WO-KIS-011; creation does not change installed behavior.

## Rules

**KIS-CMP-001.** Use one existing internal evaluation path for the relevant approval, scope, evidence and integrity checks consumed by handoff and completion. Preview, planning and apply must agree for unchanged selected inputs. Projection alone remains a projection, as specified by SPEC-KIS-004.

**KIS-CMP-002.** Derive changed files from Git against the agreed starting revision, including staged, unstaged, deleted, renamed and non-ignored untracked files when supported. Carry the same baseline through handoff and completion. Refuse missing or ambiguous baseline context. A later baseline cannot silently omit earlier task changes, and a caller-supplied incomplete file list cannot establish completion.

**KIS-CMP-003.** Immediately before applying implemented, re-evaluate the cheap current checks on the selected work, baseline and relevant input identity. If relevant inputs change before the write, refuse and retry evaluation; do not apply a cached pass to different inputs. No completion path may bypass a failed handoff by using fewer predicates.

**KIS-CMP-004.** Use one blocking-error selection rule. Invalid selected records, declared dependencies and shared integrity failures block the operation. Unrelated draft problems are reported separately and do not block it. Ambiguous duplicate identities and an unreadable selected chain remain blockers.

**KIS-CMP-005.** A failed or insufficiently grounded completion attempt leaves the work order and evidence unchanged and identifies the missing input or failed check. Do not add stored handoff certificates, a new state machine, a live-CI prerequisite for local work, or an owner-name bypass. Evidence applicability follows SPEC-KIS-004; the completion command does not automatically rerun every test.

**KIS-CMP-006.** A valid approved executor may complete routine work without renewed permission. Implemented does not mean verified, released or authorized for external delivery. Preserve the single execution route and reserved owner decisions from SPEC-KIS-003.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-KIS-011` | KIS-CMP-001, KIS-CMP-002, KIS-CMP-003, KIS-CMP-004, KIS-CMP-005, KIS-CMP-006 |

## Examples and failure behavior

- **Normal:** An approved task with complete in-scope changes and valid evidence completes offline. An unrelated incomplete draft does not change that result.
- **Failure:** An outside-scope file is present in the real diff. Handoff and direct completion both refuse; the work order stays in progress.

Refusal names the failed criterion or missing input and does not imply an applied state change.
Use an existing diagnostic when its meaning fits; do not reserve new codes in this draft.

## Compatibility and KISS review

This prospectively replaces the weaker implemented transition checks in the current workflow contract. It preserves SPEC-KIS-001 local progress and SPEC-KIS-003 execution authority. The existing architecture of local evaluation and server-side integration is retained; no new approval engine or trust boundary is introduced.

Reuse existing components and remove obsolete tests and instructions with the behavior
they described. No new artifact type, approval service, runtime mode or score is required.
These are repairs within the existing component responsibilities: no new architecture
is introduced and no active architecture addresses this new requirement. If implementation
reveals a material structural or trust-boundary change, obtain a bounded architecture
decision before that change rather than silently expanding this repair.
