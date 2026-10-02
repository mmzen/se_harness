+++
id = "SPEC-RLO-007"
type = "specification"
title = "Single approval for complete release delivery"
status = "approved"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
contract = "One recorded human decision covers the exact prepared release and listed delivery actions; required checks and public observations determine execution and completion."

[relations]
specifies = ["REQ-RLO-021", "REQ-RLO-022", "REQ-RLO-023"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T20:17:28Z"
decided_by = "mmzen"
reason = "Human repository owner mmzen answered \"Approve package, verification and review PR\" to the exact package review for WO-RLO-014/015/016 and their governing definitions, with required commit-bound verification under VER-RLO-011. This authorizes bounded implementation, local checks and commits, completion and verification preparation, ordinary review-branch push and draft PR from work/complete-release-approval to mmzen/se_harness:main, and its later verification-decision update. Human verification acceptance, merge, actual releases and the exact live configuration change remain separate. The selected released evaluator 0.21.0 governs this work. Reviewed draft SHA-256 878250c45356d9439584c858cc2c72b9e107e30121879f98e1cd0e8288c9f7a9; approved transition input SHA-256 878250c45356d9439584c858cc2c72b9e107e30121879f98e1cd0e8288c9f7a9. Only the confirmed WO assurance fields were added before this transition."
+++

# Single approval for complete release delivery

## Scope and compatibility

This is the prospective complete-release route selected by INT-RLO-002. It adds
explicit bundled authority to existing release preparation and delivery. Older
RLS, REL, work orders and evidence keep their original authority and procedure.
It neither edits accepted definitions nor activates a linked definition revision.
Current legacy deliveries remain subject to their selected contracts.

Use the existing REL, RLS, delivery plan and completion report. No additional
formal artifact type, lifecycle state, authorization service or portable network
publisher is required. Version an existing data format only where its validation
semantics change; keep old input handling explicit and testable.

Select this route explicitly in the release contract and reviewed delivery plan.
Require a declared complete-release scope before offering the combined approval.
An absent selection retains the legacy route; a new software version or an RLS
state must not silently widen an existing grant.

## RLO-ONE-001 — Approval envelope

For this route, the release review identifies the exact ready RLS, REL, verified
candidate, evaluator and plugin versions, artifact digests, destinations and
complete delivery plan. The plan records each action's prerequisites and recovery
rule. Include release-only pushes and PR integration needed to record the decision
and public receipts, with allowed paths, content rules and protected destinations.
Unrelated code changes and adoption are outside this envelope.

The same human response may exercise DR-RLS-DECIDE and the exact listed external
rights when the human holds them. Record the actual human, decision reference,
RLS and reviewed plan SHA-256 using existing decision/evidence mechanisms.
An agent applies that decision; no result, plan file or actor string authenticates
a human grant. Do not parse arbitrary prose into permission.

The plan is frozen after review. Store observed public results separately. Any
post-approval governance commit must be derived only from approved base content
plus the recorded decision or specified receipts. Record that derivation rule
in the plan, verify the diff before integration and stop on other changes.

## RLO-ONE-002 — Human request and continuing authority

Lead the request with "Approve the complete release", the versions and observable
delivery. Summarize verification and limitations, then link the exact plan and
candidate. Do not require the owner to assemble authority from separate prompts.

Machine workflow results and instructions must agree: an external action still
requires its right, but an existing matching grant is reused rather than requested
again. A check or transition does not publish. When authority is absent or narrower,
identify the exact missing action instead of assuming release state grants it.
An old release-only decision cannot be promoted to complete-release authority.

## RLO-ONE-003 — Prepare the exact deliverables

Prepare the evaluator archives, both claimed host plugin payloads, versioned
documentation and demonstration inputs before final approval. Complete required
candidate checks and human verification at this point. Resolve required credential
and provider-control readiness before calling the plan executable. List accepted
limitations explicitly; approval must not silently accept missing evidence.

Add a distinct staging path to the existing plugin builder. It consumes retained
candidate provenance and the verified evaluator archive, not an invented released
RLS. Keep the existing released-input path's checks. Staged output is not public
availability evidence. Existing inventory fields that hash the changing RLS file
must not cause payload rebinding after approval: retain candidate qualification
provenance separately from the later release-decision/publication receipt, and
verify their shared immutable payload identity.

Do not create a new registry or change plugin host installation formats to solve
this dependency. Use inert staged files and the current deterministic builder.

## RLO-ONE-004 — Publish the approved bytes

Extend the existing trusted-main publication workflow and repository tooling.
The sequence is: apply and integrate the approved release decision; qualify the
retained inputs; publish the version tag, GitHub assets and PyPI; compare an
independently obtained public evaluator wheel with the approved wheel; publish the
qualified plugin tree as an ordinary descendant of its expected marketplace ref;
deploy the planned pages and integrate approved documentation; observe all required
public routes; then promote latest/last and retain their readback.

Preserve existing maintenance-line reconciliation. Independent steps may run in
parallel, but none may pass an unmet dependency. Pin trusted workflow tools and
actions. Candidate source executes only without publication credentials. Credential
jobs consume checked inert bytes and trusted main tooling. Portable harness code
must not contain GitHub, PyPI, Pages or marketplace-specific publication policy.

## RLO-ONE-005 — Resume and completion

Before a repeat external write, classify observed state as absent, exact, partial,
conflicting or unknown. Exact completed work is checked and retained, not recreated.
Resume missing steps under the original grant. Unknown results are inspected first.
Conflicting immutable state, unexpected ref movement, changed approved inputs or
missing required controls stop the affected step. Failed checks are not approval
requests; changed work needs a bounded correction decision.

Report authorized, published and complete as distinct facts using the existing
completion report. Overall completion requires all five delivery surfaces and
their components, including markers, to pass their required observations. An
unavailable required public host test keeps completion pending; approval of an
unobserved result must not be invented. Accepted limitations are assessed only
within the exact criteria reviewed before approval.

## RLO-ONE-006 — Provider configuration

Before enabling this route in mmzen/se_harness, review the live pypi environment,
Trusted Publisher binding, allowed ref policy, workflow permissions, and main
protections. The intended one-time change removes only the redundant required
reviewer for pypi after released-record/plan checks and restricted credential jobs
are verified and integrated. Preserve OIDC, allowed refs, least privilege and main
checks. Do not broaden secrets, add an admin bypass or disable unrelated controls.

Retain the exact before/after configuration and recovery procedure. A human reviews
that concrete change before apply. If the approved one-time configuration cannot
be established, report the remaining platform gate and do not promise unattended
complete delivery. No individual release may silently bypass a provider gate.

## RLO-ONE-007 — Rollout and historical behavior

Implement and verify the product instructions and repository automation first.
Activate the portable behavior through a released evaluator/plugin and separate
repository adoption. The release that carries this feature remains governed by
the currently selected release and its explicit authority; candidate instructions
cannot govern their own rollout. The first complete release must select this
contract explicitly and have all required operational prerequisites recorded.

## Design simplicity

Combining prompts alone leaves the plugin's later assurance dependency and GitHub's
reviewer gate intact. A new orchestration service would add deployment and authority
state without solving a distinct need. Extending existing preparation, publishing
and readback paths is the smallest complete solution. The new staging mode and
one-time control change address the two concrete dependencies.

## Checkable example

The owner approves prepared evaluator X and plugin Y with plan digest P. Publication
reaches PyPI and then a marketplace upload is interrupted. A resumed agent checks
the immutable public wheel and current marketplace ref, then completes the missing
approved action without another permission request. A different wheel or ref stops
that action. Completion is reported only after pages, documentation, installation
checks and latest/last also match the plan.
