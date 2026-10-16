+++
id = "WO-RLS-055"
type = "work_order"
title = "Qualify historical releases without treating them as live delivery"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-16"
updated = "2026-10-16"

[assurance]
commit_bound_verification = "required"
rationale = "mmzen confirmed required commit-bound verification for the release resolver, workflow and qualification correction."
decided_by = "mmzen"

[execution_scope]
paths = [".github/scripts/publish_release.py", ".github/workflows/release-qualification.yml", ".github/workflows/publication-rehearsal.yml", "tests/test_release_orchestration.py", "docs/notes/release-publication-rehearsal.md", "docs/notes/developing-se-harness.md", "docs/engineering/release-0-23-0/"]

[relations]
implements = ["REQ-RLO-022"]
specifications = ["SPEC-RLO-007"]
verification = ["VER-RLS-039"]
architecture = ["ARCH-RLO-006", "ADR-RLO-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-16T12:14:31Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"I approve\" on 2026-10-16 to the explicit WO-RLS-055 request and review at PR #544 head 9c42b4d00e744bc1f3b2461a0819081141dd4c3b. Approves the bounded historical-rehearsal correction, required commit-bound verification under VER-RLS-039, and manual activation of the exact linked REL-SEH-036 membership amendment preserving accepted bytes and lifecycle history. Includes local implementation/checks, actual read-only rehearsal qualification, and ordinary updates to draft PR #544, codex/release-0-23-0 to mmzen/se_harness:main, including the ready aggregate record and a later separately supplied verification decision. Keeps live publication checks, original findings and desktop deferral unchanged. Human verification, merge and exact complete-release approval remain separate. Reviewed WO SHA-256 3b8ce814b940f09615059fd78aaf386907b2a7429d3abe4949be7b72593a064a."
scope_paths = [".github/scripts/publish_release.py", ".github/workflows/release-qualification.yml", ".github/workflows/publication-rehearsal.yml", "tests/test_release_orchestration.py", "docs/notes/release-publication-rehearsal.md", "docs/notes/developing-se-harness.md", "docs/engineering/release-0-23-0/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-16T12:15:28Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Qualify historical releases without treating them as live delivery

## Objective

Let the required read-only historical release rehearsal assess the selected
release's immutable inputs after current documentation has legitimately moved
on. Preserve the live publisher's current-documentation checks and all original
qualification, provenance and authority requirements.

The manual rehearsal at candidate 6fa4d1a645660cd8022dfc5c3ee7ba35bda3d162
failed on RLS-SEH-033 with "approved documentation differs: README.md".
The same refusal reproduces locally against origin/main
4fb5dbc29ffd7a2ccdc9a081c9c9b9f82b99d999. The candidate replay and simulated
complete-delivery/recovery jobs passed. This is open item R23-REHEARSAL-001;
it is not covered by DEC-RLS-010/011 and has not been accepted as a passing check.

## In scope and expected change surface

| Path | Purpose |
| --- | --- |
| .github/scripts/publish_release.py | Share existing release provenance validation with an explicitly read-only historical qualification path. Validate the approved documentation at its recorded commit and integration. Keep current-main documentation checks for live resolution and delivery. Historical qualification must not become an alternate publication authorization path. |
| .github/workflows/release-qualification.yml | Select the appropriate subject-resolution purpose while retaining the one existing qualification/build sequence, exact candidate, hash checks and read-only permissions. |
| .github/workflows/publication-rehearsal.yml | Explicitly select historical qualification for the earlier-record rehearsal. Preserve candidate and complete-delivery fixture legs. |
| tests/test_release_orchestration.py | Regression for legitimate later documentation changes, rejection of tampered historical bindings, and unchanged live-publication refusal. Cover caller defaults and no historical-mode production invocation. |
| docs/notes/release-publication-rehearsal.md | Explain historical qualification versus current live-delivery readiness and their exact inputs. |
| docs/notes/developing-se-harness.md | Correct only the affected release-sequence explanation. |
| docs/engineering/release-0-23-0/ | Proposal, failure evidence, exact linked REL membership revision, checks, final aggregate verification and release records. |

Inspect the current resolver, its complete-delivery validator, both workflow
callers, ready-record replay, publisher caller and regression fixtures. Keep the
production caller unchanged; if a safe correction needs more paths or changed
accepted rules, return that expansion for review. Reuse current validators and
the existing recipe. No parallel build lane, copied policy or new formal type.

## Required verification

Propose **required commit-bound verification** under VER-RLS-039, in the existing
final aggregate VREC. The human must confirm this classification before approval.
Do not fill decided_by from the agent's identity.

1. Reproduce and retain the original CI and local refusal without changing any
   approved record, documentation digest or input merely to obtain a pass.
2. In a disposable history, qualify a released record after a later legitimate
   README change. The historical record, candidate, approved plan, evidence and
   recorded documentation must still match their original bindings.
3. Refuse changed plan/record/evidence bytes, missing history, wrong candidate,
   and mismatched documentation at the approved/integration commits. Preserve
   current resolver and delivery refusal for stale current-main documentation.
4. Confirm the public publisher retains its live defaults. Historical output
   grants no action or readiness claim. Preserve required checks, read-only
   qualification permissions, secret separation and the existing shared build.
5. Run the focused existing regression suite, applicable source/package checks,
   complete PR scope checks, both real read-only rehearsal legs and recovery
   rehearsal. Retain actual failures and skips. Bind the result to the new exact
   candidate; reuse earlier native evidence only after explicit input comparison.

## Linked membership amendment

Only after an explicit human decision, apply the exact proposed REL-SEH-036
revision in this work order's evidence directory, adding WO-RLS-055 to gates.
Preserve the complete accepted bytes and lifecycle history. The installed
evaluator has no generic revision command; request bounded manual activation.
No other accepted definition or prior release record changes.

## Evidence and generated paths

Retain commands, exits, subject identities, comparisons and review under
evidence/WO-RLS-055/. Its fixed handoff/pre-action packets use that directory.
Final package observations stay under evidence/WO-RLS-045 and WO-RLS-046.
The new aggregate VREC and evaluator sidecar are allocated by capture and remain
inside this release domain; inspect the exact returned paths before writing.
No temporary source exports, profiles or credentials enter the repository.

## Authority and limits

This is a draft. Approval is requested for the bounded correction, required
commit-bound verification and exact manual membership amendment. Local edits,
tests, completion and verification preparation follow that approval.
Also request ordinary updates to existing draft PR #544 in mmzen/se_harness,
codex/release-0-23-0 to main, including the ready record and a later separately
given verification decision. Keep the full original comparison base.

No new public release, merge, provider-setting change, host update, permission
expansion or risk acceptance is included. Preserve R23-NATIVE-010/011 as open
and desktop as unverified under DEC-RLS-010/011. Do not repair their product
behavior in this work. Historical releases and their evidence remain unchanged.

## Stop and completion

Stop on uncovered paths, changed accepted obligations, a weakened public guard,
unavailable provenance or failed required qualification. A warning is not a pass.
Completion requires the bounded regression and real rehearsal evidence, normal
scope/handoff checks and an exact candidate. Report completed behavior, observed
checks, remaining limitations and the evaluator's next step. Human verification,
merge and exact complete-release approval remain separate.
