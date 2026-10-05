+++
id = "WO-RLS-041"
type = "work_order"
title = "Qualify and stage plugin 0.2.6"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-05"

[assurance]
commit_bound_verification = "required"
rationale = "mmzen confirmed required commit-bound verification because release and delivery decisions depend on these exact inputs."
decided_by = "mmzen"

[execution_scope]
paths = ["docs/engineering/release-0-22-1/"]

[relations]
implements = ["REQ-PLG-002", "REQ-IAR-030", "REQ-RLO-018", "REQ-RLO-021"]
specifications = ["SPEC-PLG-001", "SPEC-IAR-016", "SPEC-RLO-006", "SPEC-RLO-007"]
verification = ["VER-RLS-037", "VER-IAR-021"]
architecture = ["ARCH-PLG-001", "ADR-PLG-001", "ARCH-IAR-012", "ADR-IAR-012", "ARCH-RLO-006", "ADR-RLO-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T18:24:52Z"
decided_by = "mmzen"
reason = "mmzen answered \"Approve preparation and review publication\" to the exact seven-artifact evaluator 0.22.1 / plugin 0.2.6 proposal: REL-SEH-035, WO-RLS-040/041/042 and VER-RLS-036/037/038, with required commit-bound verification. This approves bounded preparation and qualification of the two HAG fixes and main already-approved dashboard correction, ordinary review pushes/draft PRs from codex/release-0-22-1 to mmzen/se_harness:main, later verification-decision updates, read-only CI rehearsals and the codex/plugin-0-2-6-staging review ref. Human verification, merge, the exact complete-release decision, adoption and provider-setting changes remain separate. Reviewed draft hashes matched; only the human-confirmed assurance fields were added before preview. Reviewed SHA-256 2ef493731f5579f18130e7f9793ee8f632e7978f493f71b5e5dc256597f1c46a."
scope_paths = ["docs/engineering/release-0-22-1/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-04T18:44:05Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-05T03:40:55Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Codex records approved local preparation completion. Corrected source 061307929c94314ccd2beb4a53f174e536fceba8 passed retained Windows/Linux, installed-package and native CLI qualification. The checked 69-file marketplace child is prepared locally. Actual mmzen desktop omission/risk acceptance and exact provider activation are retained. Final committed-candidate capture and matching build/staging qualification follow separately; this supplies no verification, merge or release decision."
+++

# Qualify and stage plugin 0.2.6

## Objective and in scope

Qualify and stage both plugin 0.2.6 packages from the exact 0.22.1 candidate
wheel before release approval. Use the existing candidate staging/check commands,
Windows/Linux package tests and native host evidence under VER-RLS-037 and
VER-IAR-021. Prepare the ordinary marketplace-child commit and retain it on the
review staging ref only after the proposed branch grant is approved.

## Expected change surface

Only this release domain changes in the development checkout: manifests,
inventories, native test results, staging comparisons and review evidence.
Plugin source/manifests are prepared by WO-RLS-040. External staging trees are
generated outside this checkout, checked against the retained candidate bundle,
and governed by the exact proposed staging-ref grant. Public marketplace writes
wait for the final frozen-plan decision. No new builder or host behavior.

## Completion and verification

Both exact package identities and required candidate/native evidence are ready
for the final aggregate verification at the same candidate as WO-RLS-040.
Do not require public publication to qualify staged bytes. Preserve every
unperformed criterion as pending. Public route observations are WO-RLS-042.

## Authority and limits

This is a draft. Propose required commit-bound verification; mmzen has not yet
confirmed this new classification or approved these work orders. No prior HAG
verification or draft-PR grant authorizes release preparation implementation.

After approval, Codex may execute local work, checks, bounded commits and record
preparation within this scope. Propose ordinary review pushes and draft PRs from
`codex/release-0-22-1` to `mmzen/se_harness:main`, including later verification
decisions and release receipts, plus existing read-only CI rehearsals. Plugin
staging may use `codex/plugin-0-2-6-staging` as a review ref; it must be an ordinary
child of the observed marketplace tip and must not update the public branch.

Human verification, merge and the final exact complete-release decision remain
separate. The latter may authorize all listed publication actions in one response
once immutable inputs, qualification and provider controls are ready. Until then,
no PyPI, release tag, latest/last, Pages or marketplace mutation is authorized.
No force-push, protection bypass, provider-setting change or adoption is covered.

Use released 0.22.0 outside the checkout as governor. Test candidate 0.22.1 only
in isolated environments. Preserve historical decisions, exact bound evidence,
and actual human attribution. Do not edit DEC-HAG-001, SPEC-HAG-003 or VER-HAG-001.

## Stop and report

Stop the affected action on missing required evidence, changed approved inputs,
uncovered files, conflicting remote state or missing provider controls. Do not
waive a required host test by borrowing a past release's accepted omission.
Report exact candidate, checks and skips, completed surfaces, outstanding work
and the evaluator's next step. No new lifecycle, service or authority format.
