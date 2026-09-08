+++
id = "WO-PLG-013"
type = "work_order"
title = "Fresh repair and explicit repository upgrade"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"
[assurance]
commit_bound_verification = "required"
rationale = "Later decisions rely on changed plugin behavior or trusted guidance; assurance must bind the exact candidate."
decided_by = "engineering-owner"

[execution_scope]
paths = ["plugins/verity-plane/common/skills/setup/SKILL.md", "plugins/verity-plane/common/skills/setup/references/maintenance.md", "tests/plugin_integration/maintenance/", "docs/engineering/plugin-integration/work-orders/WO-PLG-013.md", "docs/engineering/plugin-integration/evidence/WO-PLG-013/"]

[relations]
implements = ["REQ-PLG-022", "REQ-PLG-023"]
specifications = ["SPEC-PLG-013"]
verification = ["VER-PLG-013"]
+++

# Work Order: Fresh repair and explicit repository upgrade

## Lifecycle

Draft proposal; classification and scope await approval. Start, completion, preparation, assurance and integration remain separate accountable decisions. No delegation is proposed.

## Objective

Add setup maintenance instructions for fresh environment replacement and explicitly authorized repository upgrades.

## In scope

Maintenance reference, setup skill link, and failure/recovery tests using shared environment operations. Retain only this work order's evidence and lifecycle metadata within its engineering paths.

## Out of scope

Changing initial setup semantics, runtime management, installer code, automatic Python installation, or historical records. No other packet or managed root changes.

## Authorized decision envelope

After approval, choose names, fixtures and wording within SPEC-PLG-013. Scope, acceptance criteria and decision ownership remain accountable-owner decisions.

## Constraints

Prerequisite/environment packets must supply tested operations first. Use existing upgrade semantics and project evidence. No additional approval packet is invented.

## Expected change surface

Only declared exact files and component directories. Inspect before editing; coordinate overlapping setup changes.

## Required verification

Execute VER-PLG-013, repository-required checks and Git-derived scope/handoff checks using the governing released evaluator. Record candidate and host versions.

## Evidence to record

Retain inputs, outputs, changed paths, refusals and limitations under `evidence/WO-PLG-013/`. No VREC or RLS is prepared while this work remains draft.

## Stop and escalate conditions

Stop on failed identity, undeclared effects, unsupported required host behavior, unresolved blocking decisions, or scope expansion. Passing checks cannot approve work.

## Completion report format

Report implemented behavior, evidence, material non-effects, limitations and the evaluator's next accountable step. Completion does not decide assurance, merge or publication.
