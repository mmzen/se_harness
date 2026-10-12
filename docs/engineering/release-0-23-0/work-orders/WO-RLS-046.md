+++
id = "WO-RLS-046"
type = "work_order"
title = "Qualify plugin 0.2.7 and the exact hosted release combination"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-12"
updated = "2026-10-12"

[assurance]
commit_bound_verification = "required"
rationale = "mmzen confirmed required commit-bound verification because release and delivery decisions depend on these exact inputs."
decided_by = "mmzen"

[execution_scope]
paths = ["docs/engineering/release-0-23-0/"]

[relations]
implements = ["REQ-PLG-002", "REQ-IAR-030", "REQ-HAG-008", "REQ-RLO-018", "REQ-RLO-022"]
specifications = ["SPEC-PLG-001", "SPEC-IAR-016", "SPEC-HAG-003", "SPEC-RLO-006", "SPEC-RLO-007"]
verification = ["VER-RLS-040", "VER-IAR-021"]
architecture = ["ARCH-PLG-001", "ADR-PLG-001", "ARCH-IAR-012", "ADR-IAR-012", "ARCH-HAG-001", "ADR-HAG-001", "ARCH-RLO-006", "ADR-RLO-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-12T14:05:21Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"Approve preparation, verification and review publication\" to the exact evaluator/client 0.23.0 and plugin 0.2.7 package: REL-SEH-036, WO-RLS-045/046/047 and VER-RLS-039/040/041, with required commit-bound verification. This approves the bounded build-helper/setup-guide correction, current documentation, qualification, review pushes and a draft PR from codex/release-0-23-0 to mmzen/se_harness:main, later verification-decision pushes, read-only CI rehearsals and codex/plugin-0-2-7-staging review staging. The hosted service remains a private source-built sandbox and Git remains authoritative. Human verification, merge and the exact complete-release approval remain separate; adoption and host updates are excluded. Reviewed byte digests matched; only confirmed assurance fields were added before preview. Reviewed SHA-256 2c00ff992f11047387571ad73efcdd6269d7a23fe4710ca641dba66b7b5e2d88."
scope_paths = ["docs/engineering/release-0-23-0/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-12T14:10:20Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Qualify plugin 0.2.7 and the exact hosted release combination

## Objective and in scope

Qualify both exact plugin 0.2.7 archives and the private hosted combination before
complete-release approval. Stage from the 0.23.0 schema-2 candidate bundle with
the existing builder. The service remains source-built 0.1.0.dev1 with public
evaluator 0.22.1, pinned dependencies and a loopback/private-network boundary.

Run Windows/Linux package checks, applicable native instruction-delivery cases
and the packaged HAG qualification under VER-RLS-040. Use both real CLIs and
independent content/replay assessments. Retain desktop as a separate criterion;
the 0.22.1 omission is historical and supplies no waiver for this release.

Record every component, including the plugin's bundled wheel and the service's
distinct evaluator, client wheel, service image, database image/configuration,
protocol and schema. Retain the verified combination manifest and deployment
conditions with the release bundle. Use no public service or container registry.

Prepare the checked marketplace tree as one child of the observed public tip.
Publish only its approved review staging ref. The final delivery plan freezes
that exact commit/tree and both inventory digests before public approval.

## Expected change surface

Only docs/engineering/release-0-23-0/ changes in the repository. It retains
qualification evidence, immutable manifests, identity/reuse comparisons, native
traces, independent assessments, staging receipts and generated verification.
Source/helper/documentation changes belong to WO-RLS-045. External build and
profile outputs are temporary. The staging ref remains distinct from the public
marketplace. Record IDs and fixed companions are checked after allocation.

## Required verification and completion

VER-RLS-040 and VER-IAR-021 govern. Include results in the final aggregate VREC
at the same candidate as WO-RLS-045. Completion requires the specified candidate
checks and exact staged bytes; public fresh/update observations follow under
WO-RLS-047. Missing required evidence leaves preparation pending.

## Authority and limits

This proposal has not been approved. Required commit-bound verification is
proposed because later release and delivery decisions rely on these outputs.
The human must confirm that classification with work approval. No human
assurance decision is inferred from the request to prepare the release.

Propose ordinary review pushes and draft PRs from `codex/release-0-23-0` to
`mmzen/se_harness:main`, covering this package, evidence, ready records and later
separately given verification decisions. Propose read-only CI qualification and
rehearsal dispatches. Plugin staging may use `codex/plugin-0-2-7-staging` as an
ordinary child of the observed marketplace tip. It must not update the public ref.

After approval, Codex may choose temporary paths and internal helper functions,
run the bounded work, retain checks, commit and prepare verification. Builds and
disposable profiles stay outside the checkout. Use the existing authenticated
hosts without collecting or retaining credentials. This gives no authority to
change host-global settings, kill the current app or bypass provider controls.

Human verification and preparation-PR merge remain separate. A later exact
complete-release approval covers every listed public action and bounded receipt
integration together. This proposal does not supply that approval. Repository
adoption, host-plugin update, changed provider settings, production deployment,
authentication/DB ACL implementation and Git-authority cutover are excluded.

## Stop and report

Stop the affected action on missing required results, changed accepted inputs,
uncovered paths, conflicting public identities or missing controls. Preserve
failed runs and skips. Do not carry forward an earlier release's desktop omission
or silently change a criterion. New product fixes need their own bounded review.
Report exact inputs, actual results, limitations and the evaluator's next step.
