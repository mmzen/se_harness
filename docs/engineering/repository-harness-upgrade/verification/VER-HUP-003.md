+++
id = "VER-HUP-003"
type = "verification"
title = "Verify adoption of released 0.21.0 external resources"
status = "approved"
owners = ["mmzen"]
created = "2026-10-01"
updated = "2026-10-02"

[relations]
verifies = ["REQ-REB-027", "REQ-IAR-031"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T07:55:47Z"
decided_by = "engineering-owner"
reason = "Human mmzen: I confirm. Confirms refreshed WO-HUP-003 and VER-HUP-003, required commit-bound verification and the sixteen listed editable-file retirements. Scope includes the 28 managed-copy retirements and Codex CLI native rehearsal. Exact native-delivery trace review remains required before installer apply; verification acceptance and external actions remain separate. Reviewed SHA256 a3a939a248237c77d661aaca5401852a6fe0de401316035d607f81c2b1ff6530; transition input SHA256 a3a939a248237c77d661aaca5401852a6fe0de401316035d607f81c2b1ff6530. Codex applies the human decision with the selected evaluator role-label encoding; mmzen remains the decision-maker."
+++

# Verify adoption of released 0.21.0 external resources

## Independence

Expected behavior comes from REQ-REB-027, REQ-IAR-031, SPEC-REB-012 and
SPEC-IAR-016. Reuse the ordinary upgrade transaction. The accepted external
resource specification defines the successor layout; older schema examples
remain historical. This contract verifies adoption in this repository. It does
not repeat product qualification or grant release authority.

Obtain the target identity from the published v0.21.0 release and its authorized
release record. Match the wheel and installed payload before use. The published release is RLS-SEH-031 at
`4031f0fa4b5c4a95651bd928a110d8b2d94f9775`. The target wheel SHA-256 is
`13d401f5a0c94444dc3cf31c6f2863d23b77beb4b2c33756734b493606ad6789`;
the payload SHA-256 is
`c86a3301491e4ef4188ed98e2fcf8c67bf2c8184bc5e73e97e663f235c7894ac`.

Compare owner files and formal history against the actual pre-apply snapshot.
The preparation base is main at
`695d6773dc86f25691a9799e969bcca014207837`; repeat the preview if the selected inputs change.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-REB-027, REQ-IAR-031 | inspection, test | A0210-01: published identity and plan | An isolated released 0.21.0 evaluator matches the public wheel/payload identities. Its migration preview classifies every affected file against the exact public 0.20.1 wheel. All changes fit the reviewed scope. No customization or unsafe path is unresolved. |
| REQ-IAR-031 | demonstration, inspection | A0210-02: replacement delivery | Before entry retirement, genuine native startup and post-compaction traces identify the selected repository and the target package entry. The receipt matches the exact prior lock and planned entry. The accountable reviewer accepts the traces. A direct hook call or a fixture for another repository is insufficient. |
| REQ-REB-027, REQ-IAR-031 | test, inspection | A0210-03: migration and preservation | Installer apply retains its canonical transaction. Configuration, schema-5 lock and evaluator agree at 0.21.0 with external resources. Only reviewed managed files and explicitly selected stock seeds retire. Owner content, selected integrations, product source assets and prior artifacts/evidence retain their bytes except for this work's exact authorized edits. A repeat preview has no pending content changes. |
| REQ-REB-027, REQ-IAR-031 | test, inspection | A0210-04: usable repository | Target identity, doctor, validation and released-root qualification pass. Resource discovery and artifact-creation preview work without copied instructions/templates. CI selects 0.21.0. Current owner guides use the resource route. Documentation checks, the full source suite, distribution checks, CLI smoke check and predecessor assessment pass. |
| REQ-REB-027, REQ-IAR-031 | inspection, test | A0210-05: exact candidate | Scope and handoff cover the complete change set. The prepared verification record binds the exact clean adoption commit, its work order and this contract. Applicable hosted Linux and Windows checks pass before integration. Human verification acceptance is recorded separately. |

## Execution

Use the selected public 0.20.1 evaluator for authoring, approval and work start.
Use the exact published target evaluator for upgrade preview/apply. Prepare its
environment outside the checkout, without replacing an environment used by
another session. Switch governance only after the installer succeeds.

Use the released target's help to confirm the migration arguments. Preview and
apply must use the same prior wheel, retirement selection and delivery receipt.
Inspect expected version/layout differences in pre-upgrade doctor separately
from unrelated failures. Never edit the lock to make a check pass.

Run `identity`, `doctor`, `validate`, `qualify released-root`, the existing
governor-transition assessment, relevant documentation tests,
`python scripts/run_tests.py --scale full`,
`python scripts/validate_release_distributions.py --root .`, and source CLI help.
Run resource resolution and an artifact-creation dry run through the target
evaluator. Obtain exact arguments from the relevant released command help.
Use existing tests and release evidence for failure behavior; no new product
test framework is required for this adoption.

Native evidence must record the host and plugin versions actually used. Use Codex CLI with released plugin 0.2.4 as the proposed configured
replacement. Retain exact repository-bound native startup and compaction traces.
A temporary registration in the disposable test profile must be restored after
the rehearsal; do not change credentials, hook trust or desktop configuration. CLI or app-server evidence does not
verify the Windows desktop client. If the intended replacement cannot supply
the required native evidence, retain the old entry and report the gap.

## Evidence retention

The linked adoption work order declares the exact transaction, retained review,
trace and verification-record destinations. Retain command arguments, evaluator
identity, public provenance, the complete plan, preservation comparisons, actual
results, failures and candidate identity there. Keep raw test logs outside the
repository and retain concise summaries with retrieval information. Retain the
complete native traces required by the installer receipt.

Prepare the verification record through `capture-verification` only after the
required checks pass at the exact clean candidate. Do not hand-author a result
or reuse the product-release verification record as adoption evidence.

## Residual uncertainty

Public evaluator/plugin identities and the no-write migration preview are
confirmed. This draft records no completed adoption or verification verdict.
Native replacement traces for this exact repository and their human review
remain pending. Accepted release omissions do not waive this adoption criterion.
Codex Windows desktop delivery remains unverified. Adoption does not itself
publish or update a plugin, waive that limitation, authorize a merge or change
release markers. Required commit-bound assurance is proposed for human review.
