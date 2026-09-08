+++
id = "WO-PLG-016"
type = "work_order"
title = "Truthful released installation guidance"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"
[assurance]
commit_bound_verification = "required"
rationale = "Later decisions rely on changed plugin behavior or trusted guidance; assurance must bind the exact candidate."
decided_by = "engineering-owner"

[execution_scope]
paths = ["docs/notes/plugin-installation-guide.md", "tests/plugin_integration/onboarding/", "docs/engineering/plugin-integration/work-orders/WO-PLG-016.md", "docs/engineering/plugin-integration/evidence/WO-PLG-016/"]

[relations]
implements = ["REQ-PLG-027"]
specifications = ["SPEC-PLG-016"]
verification = ["VER-PLG-016"]
+++

# Work Order: Truthful released installation guidance

## Lifecycle

Draft proposal; classification and scope await approval. Start, completion, preparation, assurance and integration remain separate accountable decisions. No delegation is proposed.

## Objective

Write and check a focused installation guide after the installation-direction decision and release qualification.

## In scope

Focused guide and command/link/scenario checks against the named available release. Retain only this work order's evidence and lifecycle metadata within its engineering paths.

## Out of scope

README replacement, automatic Python installation, production code, package publication, or amendment of existing approved installation artifacts. No other packet or managed root changes.

## Authorized decision envelope

After approval, choose names, fixtures and wording within SPEC-PLG-016. Scope, acceptance criteria and decision ownership remain accountable-owner decisions.

## Constraints

DEC-PLG-003 blocks approval of REQ-PLG-027. This WO remains ineligible until its governing requirement is approved and the selected installation direction reconciles with existing contracts. Decision closure alone grants no work authority. Obtain the qualified available release and real catalog coordinates before presenting commands as usable.

## Expected change surface

Only declared exact files and component directories. Inspect before editing; coordinate overlapping setup changes.

## Required verification

Execute VER-PLG-016, repository-required checks and Git-derived scope/handoff checks using the governing released evaluator. Record candidate and host versions.

## Evidence to record

Retain inputs, outputs, changed paths, refusals and limitations under `evidence/WO-PLG-016/`. No VREC or RLS is prepared while this work remains draft.

## Stop and escalate conditions

Stop on failed identity, undeclared effects, unsupported required host behavior, unresolved blocking decisions, or scope expansion. Passing checks cannot approve work.

## Completion report format

Report implemented behavior, evidence, material non-effects, limitations and the evaluator's next accountable step. Completion does not decide assurance, merge or publication.
