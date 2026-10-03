+++
id = "WO-RLS-038"
type = "work_order"
title = "Retain Claude follow-up evidence and correct current coverage claims"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification because current support and risk-assessment claims rely on the correctness of the retained evidence and its interpretation."
decided_by = "mmzen"

[execution_scope]
paths = [
  "README.md",
  "docs/engineering/plugin-integration/README.md",
  "docs/engineering/release-0-22-0/README.md",
  "docs/notes/plugin-installation-guide.md",
  "docs/notes/plugin-marketplace-publication.md",
  "docs/notes/release-delivery-completion.md",
  "docs/engineering/release-0-22-0/work-orders/WO-RLS-038.md",
  "docs/engineering/release-0-22-0/verification/VER-RLS-002.md",
  "docs/engineering/release-0-22-0/decisions/DEC-RLS-007.md",
  "docs/engineering/release-0-22-0/decisions/DEC-RLS-008.md",
  "docs/engineering/release-0-22-0/evidence/WO-RLS-038/"
]

[relations]
implements = ["REQ-IAR-030", "REQ-RLO-019", "REQ-RLO-020"]
specifications = ["SPEC-IAR-016", "SPEC-RLO-006"]
verification = ["VER-RLS-002"]
architecture = ["ARCH-IAR-012", "ADR-IAR-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-03T09:45:54Z"
decided_by = "mmzen"
reason = "Human mmzen replied \"I approve\" to the prepared package request: choose record-tested-subset for DEC-RLS-007 and DEC-RLS-008; approve WO-RLS-038 and VER-RLS-002 with required commit-bound verification; correct the six scoped guidance files while preserving remaining gaps and historical records; permit ordinary pushes from work/claude-025-evidence-followup and a draft PR to mmzen/se_harness:main, including the later verification-decision push. Verification acceptance and merge remain separate. Codex applies the human decision. Reviewed SHA-256 12bd86c9d8961be17f19ca318eeefefe41267526fc21086ea5be250f76227f82; transition input SHA-256 c630022b9a96600763a13139d16f886c6ba8aad244a91f1aefb7d8d8a379a2f5. Only confirmed assurance metadata was added to the WO."
scope_paths = ["README.md", "docs/engineering/plugin-integration/README.md", "docs/engineering/release-0-22-0/README.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/release-delivery-completion.md", "docs/engineering/release-0-22-0/work-orders/WO-RLS-038.md", "docs/engineering/release-0-22-0/verification/VER-RLS-002.md", "docs/engineering/release-0-22-0/decisions/DEC-RLS-007.md", "docs/engineering/release-0-22-0/decisions/DEC-RLS-008.md", "docs/engineering/release-0-22-0/evidence/WO-RLS-038/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-03T09:48:16Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed. Codex starts the bounded follow-up under mmzen approval recorded on 2026-10-03; scope and verification remain unchanged."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-03T09:53:30Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Completed six scoped guidance updates and retained exact Claude observations. VER-RLS-002 assessments, 28 documentation tests, validation, review preflight and complete Git-derived handoff pass; historical authority and remaining gaps are preserved."
+++

# Retain Claude follow-up evidence and correct current coverage claims

## Objective

Readers can distinguish the Claude checks that passed after release from the
remaining gaps for exact plugin 0.2.5 and evaluator 0.22.0.

## In scope

1. Retain and independently assess the 2026-10-03 observations already collected
   at the human's request. Preserve the raw files and their byte identities.
2. Record DEC-RLS-007 and DEC-RLS-008 only after their matching human decisions.
3. Update the six current guidance files listed below to link this supplement.
   State the Windows/host/version boundary and each remaining gap.
4. Prepare verification of the exact evidence/documentation commit. Publish the
   review PR before requesting that verification, if the proposed review grant
   is approved. Transport the later decision on the same review branch.

## Out of scope

Product code, package bytes, plugin manifests, harness rules, CI configuration,
credentials, host settings, release publication, tags, PyPI, Pages and adoption.
Do not rerun a full native matrix without a new relevant failure or evidence gap.
Do not change earlier decisions, risks, verification/release records or evidence.
No complete Claude workflow, long-path or Codex desktop support claim is permitted.

## Authorized decision envelope

This draft grants no execution authority. After approval, the agent may retain
observations, assess the stated subset, edit the scoped guidance, run checks,
make local commits and prepare a verification record. The agent cannot decide
DEC-RLS-007/008, accept verification, close a risk or merge a PR.

Proposed review-publication grant: ordinary pushes from
`work/claude-025-evidence-followup` to `mmzen/se_harness`, a draft PR targeting
`main`, and the later verification-decision push on that branch. This grant
needs explicit confirmation with work approval; it is not inherited from the
completed release work.

## Assurance proposal

Propose **required commit-bound verification**. Current support and risk
assessment claims will rely on the correctness of this retained evidence and
its interpretation. The human must confirm this classification before approval;
no assurance decision or accountable identity is fabricated in metadata.

## Constraints

Use selected released evaluator 0.22.0. Reuse SPEC-IAR-016 and SPEC-RLO-006
without amendment. The earlier release deviations remain historical authority
for the original release; the two new question decisions only bound the
supplemental claims. All remaining requirements and gates stay in force.

Tested inputs: Claude Code 2.1.273 on Windows; plugin 0.2.5; evaluator 0.22.0;
public marketplace commit `7d30907f15bd7e06fb632e1ebf4e88e01b68726c`.
Native runs used short disposable paths and `--plugin-dir`; the package files
exactly match both public installation routes. Do not turn this into a claim
that every installed-profile workflow or supported platform was tested.

## Expected change surface

| Path | Reason |
| --- | --- |
| `README.md` | Correct the current blanket Claude-untested statement. |
| `docs/engineering/plugin-integration/README.md` | Link current plugin coverage. |
| `docs/engineering/release-0-22-0/README.md` | Add dated post-release coverage and distinguish its stale preparation status from retained delivery receipts. |
| `docs/notes/plugin-installation-guide.md` | Correct both current coverage notices. |
| `docs/notes/plugin-marketplace-publication.md` | Distinguish public route passes from remaining host gaps. |
| `docs/notes/release-delivery-completion.md` | Link the supplement without rewriting historical closeout. |
| `docs/engineering/release-0-22-0/decisions/DEC-RLS-007.md` and `DEC-RLS-008.md` | New decisions linking the earlier risk/decision pairs. |
| `docs/engineering/release-0-22-0/verification/VER-RLS-002.md` | Verification of evidence retention and bounded claims. |
| This work order | Approval, execution and completion history. |
| `docs/engineering/release-0-22-0/evidence/WO-RLS-038/` | Raw observations, digest index, assessment, review and relevant check results. |

The future VREC ID and its fixed evaluator JSON path are unresolved until
capture. The supported scope rules admit a record directly verifying this WO
and that record's declared evaluator evidence. Check the returned exact paths;
do not invent an ID or admit the whole verification-record directory.

No runtime, packaging or CI file changes are needed. Existing documentation/link
tests have been inspected and do not require an assertion that Claude remains
untested. Use those checks unchanged; return any unexpected correction to scope
review. Architecture is referenced for the reused instruction-delivery boundary,
not changed by this work.

## Required verification

VER-RLS-002: raw digest/identity comparisons; exact compaction hook checks;
current-claim and link review; focused existing documentation tests; selected
scope and handoff gates. Human verification is a separate decision.

## Evidence to record

Retain observations.json, observations-raw.zip and the coverage assessment under
this WO's evidence directory. Record the actual checks, complete changed paths,
original-record hashes, candidate commit and any material failed observations.
No credential material belongs in this evidence.

## Stop and escalate conditions

Stop the affected action for a package/hash mismatch, missing or inconsistent
trace, a claim exceeding observed coverage, changed historical authority, an
uncovered file, failed required gate, or a decision not supplied by the human.
Keep Codex desktop, the full Claude work-order walkthrough and the earlier
long-path scenario unverified. Keep RISK-RLS-006 unchanged.

## Completion report format

Report the exact observed passes, remaining gaps and owner/next action, files
changed, checks, candidate/review link and the evaluator's next human decision.
This supplement does not re-release the product or retrospectively change a
test result in an earlier verification record.
