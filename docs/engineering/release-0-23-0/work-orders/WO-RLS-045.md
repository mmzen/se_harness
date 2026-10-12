+++
id = "WO-RLS-045"
type = "work_order"
title = "Prepare evaluator 0.23.0 and the coordinated sandbox release"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-12"
updated = "2026-10-12"

[assurance]
commit_bound_verification = "required"
rationale = "mmzen confirmed required commit-bound verification because release and delivery decisions depend on these exact inputs."
decided_by = "mmzen"

[execution_scope]
paths = ["docs/engineering/release-0-23-0/", "pyproject.toml", "se_harness/__init__.py", "plugins/verity-plane/codex/.codex-plugin/plugin.json", "plugins/verity-plane/claude-code/.claude-plugin/plugin.json", "server/scripts/qualify.py", "tests/hosted_artifact_graph/test_release_combination.py", "plugins/verity-plane/common/skills/setup/references/hosted-context.md", "README.md", "release/plugin-marketplace/README.md", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/developing-se-harness.md", "docs/notes/release-delivery-completion.md", "docs/notes/release-publication-rehearsal.md", "docs/notes/harness-installation-and-upgrades.md", "docs/notes/harnessctl-reference.md", "docs/notes/hosted-artifact-graph.md", "docs/engineering/plugin-integration/README.md", "docs/engineering/hosted-artifact-graph/README.md", "docs/engineering/README.md", "server/README.md", "tests/test_progressive_documentation.py", "tests/plugin_integration/package_assembly/test_refresh_guidance.py", "docs/engineering/hosted-artifact-graph/risks/RISK-HAG-001.md", "docs/engineering/hosted-artifact-graph/risks/RISK-HAG-002.md"]

[relations]
implements = ["REQ-DST-006", "REQ-PLG-002", "REQ-HAG-008", "REQ-RLO-018", "REQ-RLO-021", "REQ-RLO-022", "REQ-RLO-023"]
specifications = ["SPEC-DST-001", "SPEC-PLG-001", "SPEC-HAG-003", "SPEC-RLO-006", "SPEC-RLO-007"]
verification = ["VER-RLS-039"]
architecture = ["ARCH-DST-001", "ADR-DST-001", "ARCH-PLG-001", "ADR-PLG-001", "ARCH-HAG-001", "ADR-HAG-001", "ARCH-RLO-006", "ADR-RLO-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-12T14:05:21Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"Approve preparation, verification and review publication\" to the exact evaluator/client 0.23.0 and plugin 0.2.7 package: REL-SEH-036, WO-RLS-045/046/047 and VER-RLS-039/040/041, with required commit-bound verification. This approves the bounded build-helper/setup-guide correction, current documentation, qualification, review pushes and a draft PR from codex/release-0-23-0 to mmzen/se_harness:main, later verification-decision pushes, read-only CI rehearsals and codex/plugin-0-2-7-staging review staging. The hosted service remains a private source-built sandbox and Git remains authoritative. Human verification, merge and the exact complete-release approval remain separate; adoption and host updates are excluded. Reviewed byte digests matched; only confirmed assurance fields were added before preview. Reviewed SHA-256 4852bdda660b9ee6fa8b1132c3b97106be95732a33af3f87d069053a18b85107."
scope_paths = ["docs/engineering/release-0-23-0/", "pyproject.toml", "se_harness/__init__.py", "plugins/verity-plane/codex/.codex-plugin/plugin.json", "plugins/verity-plane/claude-code/.claude-plugin/plugin.json", "server/scripts/qualify.py", "tests/hosted_artifact_graph/test_release_combination.py", "plugins/verity-plane/common/skills/setup/references/hosted-context.md", "README.md", "release/plugin-marketplace/README.md", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/developing-se-harness.md", "docs/notes/release-delivery-completion.md", "docs/notes/release-publication-rehearsal.md", "docs/notes/harness-installation-and-upgrades.md", "docs/notes/harnessctl-reference.md", "docs/notes/hosted-artifact-graph.md", "docs/engineering/plugin-integration/README.md", "docs/engineering/hosted-artifact-graph/README.md", "docs/engineering/README.md", "server/README.md", "tests/test_progressive_documentation.py", "tests/plugin_integration/package_assembly/test_refresh_guidance.py", "docs/engineering/hosted-artifact-graph/risks/RISK-HAG-001.md", "docs/engineering/hosted-artifact-graph/risks/RISK-HAG-002.md"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-12T14:10:20Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Prepare evaluator 0.23.0 and the coordinated sandbox release

## Objective

Prepare evaluator/client 0.23.0 and plugin 0.2.7 from merged main at
`4fb5dbc29ffd7a2ccdc9a081c9c9b9f82b99d999`, with exact release inputs and a
reproducible private hosted-sandbox combination.

## In scope

1. Reconcile the advisory release census with the previous v0.22.1 candidate.
   Retain the explicit REL-SEH-036 membership and historical verification.
2. Set both core version declarations to 0.23.0. Confirm both plugin manifests
   use the unused 0.2.7 identity. Do not change the installed 0.22.1 governor.
3. Correct only the sandbox preparation helper's fixed development identities.
   Derive the client version from the supplied wheel and check it against the
   candidate source and build replay. Accept the already-staged pair of plugin
   archives for qualification; verify their inventories, source and embedded
   wheel against the selected release bundle. Preserve the original development
   preparation route and refuse incomplete or conflicting inputs before building.
   Keep the hosted evaluator exactly 0.22.1. Test these normal/refusal boundaries.
4. Update current version, install and status guidance. Replace stale claims that
   HAG qualification is pending, while preserving historical reports and bound
   evidence. Distinguish the plugin's bundled 0.23.0 from the service's pinned
   evaluator 0.22.1. Explain a source-built, private sandbox only.
   Update the shared hosted selection guide to permit the exact qualified
   released client as well as a development client in its separate environment.
   Preserve explicit selection, identity checks and all authority boundaries.
5. Run required source/package checks and pinned two-build replay. Combine the
   actual staged-plugin and sandbox evidence from WO-RLS-046 at final candidate C.
   Capture one aggregate VREC covering REL-SEH-036's exact gates and contracts.
6. After human verification, prepare the explicitly tagged ready RLS, bind its
   evaluator archives, replay the binding, and freeze the complete delivery plan.
   Retain the existing combination manifest with image/deployment identities as
   a referenced release-bundle companion. Do not add a registry or new publisher.

## Expected change surface

| Paths | Reason |
| --- | --- |
| pyproject.toml; se_harness/__init__.py; both host plugin.json files | Coordinated release versions. |
| server/scripts/qualify.py; tests/hosted_artifact_graph/test_release_combination.py | Exact release-client and staged-plugin identity checks, including mismatch refusals. |
| plugins/verity-plane/common/skills/setup/references/hosted-context.md | Remove candidate-only wording while preserving the qualified-client selection and private boundary. |
| Named README and docs/notes files in execution_scope | Current release routes, component separation, public status and sandbox limits. |
| tests/test_progressive_documentation.py; tests/plugin_integration/package_assembly/test_refresh_guidance.py | Existing documentation/version expectations. |
| RISK-HAG-001.md and RISK-HAG-002.md | Add this release work as affected scope only; preserve state, owner, action and history. |
| docs/engineering/release-0-23-0/ | Formal proposal, exact build/combination manifests, source comparisons, reviews, checks, generated records, handoff and later decision receipts. |

The release component directory includes the evaluator's fixed VREC/RLS
sidecars. Allocate record IDs only when capture/preparation runs and inspect the
actual destinations. Existing service runtime, database, schemas, protocols,
locks, build recipe, publisher and CI configuration need no change. The helper
correction does not introduce a new service API, lifecycle rule or permission.

## Required verification and completion

Apply VER-RLS-039 and aggregate the independently assessed VER-RLS-040 results.
Keep all relevant prior contracts in the final coverage. Record complete argument
arrays, actual results, platform/host/component identities and digests. Do not
manufacture new native observations from historical logs. Completion means
reviewable release inputs and final-candidate assurance preparation, not publication.

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
