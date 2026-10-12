+++
id = "WO-RLS-047"
type = "work_order"
title = "Deliver and confirm evaluator 0.23.0 and plugin 0.2.7"
status = "approved"
owners = ["mmzen"]
created = "2026-10-12"
updated = "2026-10-12"

[assurance]
commit_bound_verification = "required"
rationale = "mmzen confirmed required commit-bound verification because release and delivery decisions depend on these exact inputs."
decided_by = "mmzen"

[execution_scope]
paths = ["docs/engineering/release-0-23-0/", "README.md", "release/plugin-marketplace/README.md", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/developing-se-harness.md", "docs/notes/release-delivery-completion.md", "docs/notes/release-publication-rehearsal.md", "docs/notes/harness-installation-and-upgrades.md", "docs/notes/harnessctl-reference.md", "docs/notes/hosted-artifact-graph.md", "docs/engineering/plugin-integration/README.md", "docs/engineering/hosted-artifact-graph/README.md", "docs/engineering/README.md", "server/README.md", "tests/test_progressive_documentation.py", "tests/plugin_integration/package_assembly/test_refresh_guidance.py"]

[relations]
implements = ["REQ-RLO-019", "REQ-RLO-020", "REQ-RLO-023"]
specifications = ["SPEC-RLO-006", "SPEC-RLO-007"]
verification = ["VER-RLS-041"]
architecture = ["ARCH-RLO-006", "ADR-RLO-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-12T14:05:21Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"Approve preparation, verification and review publication\" to the exact evaluator/client 0.23.0 and plugin 0.2.7 package: REL-SEH-036, WO-RLS-045/046/047 and VER-RLS-039/040/041, with required commit-bound verification. This approves the bounded build-helper/setup-guide correction, current documentation, qualification, review pushes and a draft PR from codex/release-0-23-0 to mmzen/se_harness:main, later verification-decision pushes, read-only CI rehearsals and codex/plugin-0-2-7-staging review staging. The hosted service remains a private source-built sandbox and Git remains authoritative. Human verification, merge and the exact complete-release approval remain separate; adoption and host updates are excluded. Reviewed byte digests matched; only confirmed assurance fields were added before preview. Reviewed SHA-256 854eaa7df9f5a0d7ba0c006e84998e7a8b482e78aa43c7962669390e618e1f54."
scope_paths = ["docs/engineering/release-0-23-0/", "README.md", "release/plugin-marketplace/README.md", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/developing-se-harness.md", "docs/notes/release-delivery-completion.md", "docs/notes/release-publication-rehearsal.md", "docs/notes/harness-installation-and-upgrades.md", "docs/notes/harnessctl-reference.md", "docs/notes/hosted-artifact-graph.md", "docs/engineering/plugin-integration/README.md", "docs/engineering/hosted-artifact-graph/README.md", "docs/engineering/README.md", "server/README.md", "tests/test_progressive_documentation.py", "tests/plugin_integration/package_assembly/test_refresh_guidance.py"]
+++

# Deliver and confirm evaluator 0.23.0 and plugin 0.2.7

## Objective and in scope

After the exact complete-release decision, execute its frozen plan and confirm
all five public surfaces: evaluator, marketplace, documentation, demonstration
and release markers. Use the existing trusted-main resolver and publisher.
This work order does not itself authorize any public action.

Reconcile GitHub v0.23.0 and its assets, PyPI se-harness 0.23.0, release/0.23,
both 0.2.7 marketplace packages, current instructions and Pages. Independently
install the public wheel and test fresh installation and update from plugin
0.2.6 on both claimed CLIs. Publish latest/last only after required observations.
Reuse the one matching complete-release grant for these actions and exact retries.

Update only current release-status guidance and its existing documentation
tests. Verify that the tagged private-sandbox source and guide match the frozen
combination's source. No public service or production claim is permitted.

## Expected change surface

The exact named current docs and their existing two test files in execution_scope
cover truthful installation/status guidance. The release domain retains public
observations, authorized receipt transport, verification and closeout. No runtime,
workflow, builder or provider-setting edit is included. The later frozen plan
must name narrower receipt integration paths and allowed effects before approval.

## Required verification and completion

Apply VER-RLS-041. Retain original failed attempts and remote readbacks. Run the
existing five-surface completion check and prepare commit-bound verification of
the observations/documentation. A pending or deferred surface prevents complete
delivery. This post-publication work is excluded from REL-SEH-036.gates so it is
not its own publication precondition. Adoption and local host updates follow
separately if requested.

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
