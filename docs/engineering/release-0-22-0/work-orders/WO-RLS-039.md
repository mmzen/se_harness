+++
id = "WO-RLS-039"
type = "work_order"
title = "Restore the README size limit after the Claude follow-up"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed that integration and public guidance rely on correct presentation and coverage claims; the corrected candidate requires commit-bound verification."
decided_by = "mmzen"

[execution_scope]
paths = [
  "README.md",
  "docs/engineering/release-0-22-0/work-orders/WO-RLS-039.md",
  "docs/engineering/release-0-22-0/verification/VER-RLS-003.md",
  "docs/engineering/release-0-22-0/evidence/WO-RLS-039/"
]

[relations]
implements = ["REQ-DST-069", "REQ-RLO-020"]
specifications = ["SPEC-DST-024", "SPEC-DST-029", "SPEC-RLO-006"]
verification = ["VER-RLS-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-03T10:20:02Z"
decided_by = "mmzen"
reason = "Human mmzen replied I approve to the reviewed WO-RLS-039 and VER-RLS-003 request: shorten only the new README paragraph from 690 to 644 total words, preserve its evidence link and unverified areas, run unchanged documentation tests and the full suite, and prepare required commit-bound verification. Approval also covers correction and later verification-decision pushes to existing PR 533, mmzen/se_harness, work/claude-025-evidence-followup to main. Human acceptance of the corrected candidate and merge remain separate. Codex applies this decision. Reviewed SHA-256 56110b77e01ef8c6dc85189fe45e3d98d53e0b9b9ced43a280e065aecba6031c; transition input SHA-256 4daea4da74b806d8da9132d0b2d27144192e2c06a640173e1dc75cb9c6031048. Only confirmed WO assurance metadata was added."
scope_paths = ["README.md", "docs/engineering/release-0-22-0/work-orders/WO-RLS-039.md", "docs/engineering/release-0-22-0/verification/VER-RLS-003.md", "docs/engineering/release-0-22-0/evidence/WO-RLS-039/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-03T10:20:38Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed. Codex starts the bounded approved README correction; approved scope and required verification are unchanged."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-03T10:34:05Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Completed the exact approved README paragraph correction: 644 words, retained evidence link and limits; unchanged focused and full source tests, released validation, review preflight and complete Git-derived handoff passed. Original records and evidence are preserved. Codex records implementation completion under mmzen approval; human verification remains separate."
+++

# Restore the README size limit after the Claude follow-up

## Objective

Keep the README within its accepted 650-word budget while linking the current
Claude evidence and retaining the unverified host/workflow limits.

## In scope

Replace only the Claude follow-up paragraph in README.md with the prepared
644-word-file proposal. Keep its detail in the existing linked evidence report.
Run the unchanged onboarding checks and full source suite. Retain the CI failure,
corrected checks and combined verification of WO-RLS-038/039 at the new candidate.

## Out of scope

No test weakening, budget increase, other guide changes, new host tests, code,
CI configuration, package changes, risk closure, release or merge. Preserve
WO-RLS-038, VREC-RLS-001, its evidence, decisions and historical records.

## Authorized decision envelope

This draft grants no implementation authority. Approval permits this paragraph
correction, required checks, evidence, local commits and new verification capture.
The agent may not accept verification or merge.

Proposed review grant: publish this correction and its ready record in existing
PR #533, using ordinary pushes from work/claude-025-evidence-followup to
mmzen/se_harness with base main. Include the later recorded verification decision
and marking the PR ready after that decision is remote and the CI failure is
resolved. No force push, release or merge authority is requested.

## Assurance proposal

Required commit-bound verification: future readers and integration decisions
rely on truthful coverage claims and compliance with the accepted README budget.
The human must confirm this classification; metadata does not invent a decision.

## Constraints

Reuse selected evaluator 0.22.0. Apply SPEC-DST-024 PUB-BUDGET-001 and the current
plugin-first presentation in SPEC-DST-029. Preserve commands, links, images and
all text outside the selected paragraph. Keep the existing 650-word test intact.
The implementation baseline is f8f318008b99499af553e4400fdf59d938588b2d.
The complete PR baseline remains 7b6c969a7e6217ae41ff11a45cf584d48960461b.

## Expected change surface

| Path | Reason |
| --- | --- |
| README.md | Replace one paragraph; reduce the file from 690 to 644 words. |
| This work order | Record the separately approved correction and execution history. |
| verification/VER-RLS-003.md in this domain | Define checks for the budget and retained claims. |
| evidence/WO-RLS-039/ in this domain | Retain the proposed patch, CI failure, checks and review. |

The future verification record ID is selected at capture after checking local
refs. A record directly verifying this work and its declared evaluator JSON are
admitted by existing generated-output rules; check their exact returned paths.
No runtime or architecture changes apply. Existing tests need no edits.

## Required verification

Follow VER-RLS-003. Reuse unchanged native evidence under VER-RLS-002 and reassess
its current-claim criterion for the shortened paragraph. Capture a fresh record
covering WO-RLS-038/039 and both verification contracts at the new clean commit.
This does not rewrite or extend the existing VREC-RLS-001 decision.

## Evidence to record

Under evidence/WO-RLS-039/, retain actual commands, runtimes, results, input/output
hashes, the failure and its correction, diff review and full changed paths.

## Stop and escalate conditions

Stop affected work for changed scope, failing required checks, altered historical
evidence, unsupported coverage claims or an unauthorized decision. Keep all prior
unverified areas visible. A broader failure needs its own bounded assessment.

## Completion report format

Report the word count, preserved limits, actual checks, exact candidate, ready
record and PR link. Human verification and merge remain separate decisions.
