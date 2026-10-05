+++
id = "WO-RLS-042"
type = "work_order"
title = "Execute and confirm complete 0.22.1 delivery"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-05"

[assurance]
commit_bound_verification = "required"
rationale = "mmzen confirmed required commit-bound verification because release and delivery decisions depend on these exact inputs."
decided_by = "mmzen"

[execution_scope]
paths = ["docs/engineering/release-0-22-1/", "README.md", "release/plugin-marketplace/README.md", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/developing-se-harness.md", "docs/notes/release-delivery-completion.md", "docs/notes/release-publication-rehearsal.md", "docs/notes/harness-installation-and-upgrades.md", "docs/notes/harnessctl-reference.md", "docs/engineering/plugin-integration/README.md", "docs/engineering/README.md", "tests/test_progressive_documentation.py", "tests/plugin_integration/package_assembly/test_refresh_guidance.py"]

[relations]
implements = ["REQ-RLO-019", "REQ-RLO-020", "REQ-RLO-022"]
specifications = ["SPEC-RLO-006", "SPEC-RLO-007"]
verification = ["VER-RLS-038"]
architecture = ["ARCH-RLO-006", "ADR-RLO-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T18:24:52Z"
decided_by = "mmzen"
reason = "mmzen answered \"Approve preparation and review publication\" to the exact seven-artifact evaluator 0.22.1 / plugin 0.2.6 proposal: REL-SEH-035, WO-RLS-040/041/042 and VER-RLS-036/037/038, with required commit-bound verification. This approves bounded preparation and qualification of the two HAG fixes and main already-approved dashboard correction, ordinary review pushes/draft PRs from codex/release-0-22-1 to mmzen/se_harness:main, later verification-decision updates, read-only CI rehearsals and the codex/plugin-0-2-6-staging review ref. Human verification, merge, the exact complete-release decision, adoption and provider-setting changes remain separate. Reviewed draft hashes matched; only the human-confirmed assurance fields were added before preview. Reviewed SHA-256 ece9baac7f27eaea72b19ea5493d67d1c0647606486e94a4e84d49060aa07474."
scope_paths = ["docs/engineering/release-0-22-1/", "README.md", "release/plugin-marketplace/README.md", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/developing-se-harness.md", "docs/notes/release-delivery-completion.md", "docs/notes/release-publication-rehearsal.md", "docs/notes/harness-installation-and-upgrades.md", "docs/notes/harnessctl-reference.md", "docs/engineering/plugin-integration/README.md", "docs/engineering/README.md", "tests/test_progressive_documentation.py", "tests/plugin_integration/package_assembly/test_refresh_guidance.py"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-05T08:39:02Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-05T09:23:42Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. The authorized complete release was delivered. Five surfaces pass independent retained observations, public fresh/update and evaluator setup pass on both claimed Windows CLIs, protected receipt integration passed, and failures/recovery are preserved. The accepted desktop omission remains explicit. This records execution completion only; required commit-bound assurance remains a separate human decision."
+++

# Execute and confirm complete 0.22.1 delivery

## Objective and in scope

Execute and confirm the exact authorized complete release, then reconcile all
five public surfaces: evaluator, marketplace, documentation, demonstration and
markers. No publication begins until REL-SEH-035's frozen plan is ready and the
human supplies its exact complete-release decision.

Use the existing trusted-main resolver/publisher and complete-delivery procedure.
Perform only the immutable actions and permitted receipt integrations listed in
that grant. Independently compare public bytes; run claimed public fresh/update
routes. Update only release-status/current-guidance text and matching existing
documentation expectations. Retain a truthful completion report under
VER-RLS-038. Missing checks are not passed or approved by this work order.

## Expected change surface

The release domain covers approved decision/receipt transport and observations.
The named current docs and their two existing tests cover public state readback
and truthful install guidance. No product, workflow, provider or publisher edit.
The frozen plan must list any narrower receipt integration paths before approval.

## Completion and verification

All five required public observations pass, or the precise outstanding result
is reported. Prepare commit-bound verification of observation/documentation work.
This work remains outside the pre-publication release gates to avoid requiring
public observations before publication. No claim of HAG service verification.

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
