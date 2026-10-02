+++
id = "WO-HUP-003"
type = "work_order"
title = "Adopt released 0.21.0 and retire copied harness resources"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-01"
updated = "2026-10-02"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed the reviewed adoption package; later lifecycle, CI and repository decisions depend on the exact evaluator migration and resource retirement."
decided_by = "mmzen"

[execution_scope]
paths = [
  ".engineering-harness.toml",
  ".engineering-harness.lock",
  "ENGINEERING_HARNESS.md",
  "docs/engineering/QUALITY_GATES.json",
  "docs/engineering/WORKFLOW.json",
  "docs/engineering/harness/AMEND_DEFINITIONS.md",
  "docs/engineering/harness/ARTIFACTS.md",
  "docs/engineering/harness/AUTHORITY.md",
  "docs/engineering/harness/AUTHORIZE_WORK.md",
  "docs/engineering/harness/COMMUNICATION.md",
  "docs/engineering/harness/CONTINUE.md",
  "docs/engineering/harness/DEFINE_CHANGE.md",
  "docs/engineering/harness/DEFINITION_LINKS.md",
  "docs/engineering/harness/DELIVER_RESULT.md",
  "docs/engineering/harness/DRAFT_DEFINITIONS.md",
  "docs/engineering/harness/DRAFT_WORK_ORDERS.md",
  "docs/engineering/harness/EXCEPTIONS.md",
  "docs/engineering/harness/EXECUTE_WORK.md",
  "docs/engineering/harness/PULL_REQUEST.md",
  "docs/engineering/harness/RECORD_STATE.md",
  "docs/engineering/harness/RELEASE.md",
  "docs/engineering/harness/RESULTS.md",
  "docs/engineering/harness/RISKS_AND_DECISIONS.md",
  "docs/engineering/harness/SETUP.md",
  "docs/engineering/harness/SKILL_PROVIDER.md",
  "docs/engineering/harness/UPGRADE.md",
  "docs/engineering/harness/VERIFY_OUTCOME.md",
  "docs/engineering/harness/WORK_AND_EVIDENCE.md",
  "docs/engineering/harness/migration/IMPLEMENTATION_PLAN.md",
  "docs/engineering/harness/migration/REFERENCE_MAP.md",
  "docs/engineering/ARTIFACT_AUTHORING.md",
  "docs/engineering/templates/ADR.template.md",
  "docs/engineering/templates/ARCHITECTURE.template.md",
  "docs/engineering/templates/CAPABILITY.template.md",
  "docs/engineering/templates/DECISION.template.md",
  "docs/engineering/templates/INTENT.template.md",
  "docs/engineering/templates/OPERATING_CONTRACT.template.md",
  "docs/engineering/templates/README.md",
  "docs/engineering/templates/RELEASE_CONTRACT.template.md",
  "docs/engineering/templates/RELEASE_RECORD.template.md",
  "docs/engineering/templates/REQUIREMENT.template.md",
  "docs/engineering/templates/RISK.template.md",
  "docs/engineering/templates/SPECIFICATION.template.md",
  "docs/engineering/templates/VERIFICATION.template.md",
  "docs/engineering/templates/VERIFICATION_RECORD.template.md",
  "docs/engineering/templates/WORK_ORDER.template.md",
  "README.md",
  ".github/workflows/engineering-harness.yml",
  "docs/notes/developing-se-harness.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/engineering/README.md",
  "docs/engineering/self-hosting-boundary/SELF_HOSTING.md",
  "docs/engineering/repository-harness-upgrade/README.md",
  "docs/engineering/instruction-architecture/README.md",
  "tests/test_progressive_documentation.py",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-003.md",
  "docs/engineering/repository-harness-upgrade/verification/VER-HUP-003.md",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-003/",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-003-evaluator-upgrade.json",
  "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-025.md",
  "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-025-evaluator.json",
]

[relations]
implements = ["REQ-REB-027", "REQ-IAR-031"]
specifications = ["SPEC-REB-012", "SPEC-IAR-016"]
verification = ["VER-HUP-003"]
architecture = ["ARCH-REB-011", "ADR-REB-011", "ARCH-IAR-012", "ADR-IAR-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T07:55:47Z"
decided_by = "engineering-owner"
reason = "Human mmzen: I confirm. Confirms refreshed WO-HUP-003 and VER-HUP-003, required commit-bound verification and the sixteen listed editable-file retirements. Scope includes the 28 managed-copy retirements and Codex CLI native rehearsal. Exact native-delivery trace review remains required before installer apply; verification acceptance and external actions remain separate. Reviewed SHA256 af45f1183a249cb3e9188699cbaca582c03e9cd38fe14111f0eef3ae856e6f6a; transition input SHA256 0f4884f3bffb7cee9885a413b0c10b603cf1e35f38c4127ffc559296b02acbba. Codex applies the human decision with the selected evaluator role-label encoding; mmzen remains the decision-maker."
scope_paths = [".engineering-harness.toml", ".engineering-harness.lock", "ENGINEERING_HARNESS.md", "docs/engineering/QUALITY_GATES.json", "docs/engineering/WORKFLOW.json", "docs/engineering/harness/AMEND_DEFINITIONS.md", "docs/engineering/harness/ARTIFACTS.md", "docs/engineering/harness/AUTHORITY.md", "docs/engineering/harness/AUTHORIZE_WORK.md", "docs/engineering/harness/COMMUNICATION.md", "docs/engineering/harness/CONTINUE.md", "docs/engineering/harness/DEFINE_CHANGE.md", "docs/engineering/harness/DEFINITION_LINKS.md", "docs/engineering/harness/DELIVER_RESULT.md", "docs/engineering/harness/DRAFT_DEFINITIONS.md", "docs/engineering/harness/DRAFT_WORK_ORDERS.md", "docs/engineering/harness/EXCEPTIONS.md", "docs/engineering/harness/EXECUTE_WORK.md", "docs/engineering/harness/PULL_REQUEST.md", "docs/engineering/harness/RECORD_STATE.md", "docs/engineering/harness/RELEASE.md", "docs/engineering/harness/RESULTS.md", "docs/engineering/harness/RISKS_AND_DECISIONS.md", "docs/engineering/harness/SETUP.md", "docs/engineering/harness/SKILL_PROVIDER.md", "docs/engineering/harness/UPGRADE.md", "docs/engineering/harness/VERIFY_OUTCOME.md", "docs/engineering/harness/WORK_AND_EVIDENCE.md", "docs/engineering/harness/migration/IMPLEMENTATION_PLAN.md", "docs/engineering/harness/migration/REFERENCE_MAP.md", "docs/engineering/ARTIFACT_AUTHORING.md", "docs/engineering/templates/ADR.template.md", "docs/engineering/templates/ARCHITECTURE.template.md", "docs/engineering/templates/CAPABILITY.template.md", "docs/engineering/templates/DECISION.template.md", "docs/engineering/templates/INTENT.template.md", "docs/engineering/templates/OPERATING_CONTRACT.template.md", "docs/engineering/templates/README.md", "docs/engineering/templates/RELEASE_CONTRACT.template.md", "docs/engineering/templates/RELEASE_RECORD.template.md", "docs/engineering/templates/REQUIREMENT.template.md", "docs/engineering/templates/RISK.template.md", "docs/engineering/templates/SPECIFICATION.template.md", "docs/engineering/templates/VERIFICATION.template.md", "docs/engineering/templates/VERIFICATION_RECORD.template.md", "docs/engineering/templates/WORK_ORDER.template.md", "README.md", ".github/workflows/engineering-harness.yml", "docs/notes/developing-se-harness.md", "docs/notes/harness-installation-and-upgrades.md", "docs/engineering/README.md", "docs/engineering/self-hosting-boundary/SELF_HOSTING.md", "docs/engineering/repository-harness-upgrade/README.md", "docs/engineering/instruction-architecture/README.md", "tests/test_progressive_documentation.py", "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-003.md", "docs/engineering/repository-harness-upgrade/verification/VER-HUP-003.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-003/", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-003-evaluator-upgrade.json", "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-025.md", "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-025-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-02T07:56:19Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-02T08:57:30Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed."
+++

# Adopt released 0.21.0 and retire copied harness resources

## Objective

Adopt public SE Harness 0.21.0 in mmzen/se_harness and its CI. Read harness
instructions, machine policy and artifact templates from the selected released
package. Retire the reviewed repository copies, including ENGINEERING_HARNESS.md,
while preserving owner content, formal history and product source assets.

Reuse the accepted upgrade and external-resource contracts. One work order and
one verification contract cover adoption. No new requirement or architecture
decision is needed. DEC-IAR-003 preserves the future-release boundary.

## Existing authority and readiness

Human mmzen said, "I approve adoption", after confirming that the repository
root ENGINEERING_HARNESS.md will retire during separately authorized v0.21.0
adoption. Retain that authorization; do not request the same general decision
again. It does not authorize public release actions or imply a verification
result. This new bounded package remains draft while its exact inputs are missing.

Readiness refreshed on 2026-10-02 against main at
`695d6773dc86f25691a9799e969bcca014207837`:

- RLS-SEH-031 is released. Public evaluator 0.21.0 comes from candidate
  `4031f0fa4b5c4a95651bd928a110d8b2d94f9775`.
- Target wheel SHA-256:
  `13d401f5a0c94444dc3cf31c6f2863d23b77beb4b2c33756734b493606ad6789`.
- Target payload SHA-256:
  `c86a3301491e4ef4188ed98e2fcf8c67bf2c8184bc5e73e97e663f235c7894ac`.
- Released plugin 0.2.4 is available at marketplace commit
  `7e366438165a40a14783bac650a2887e7ec8bc75`.
- The current 0.20.1 identity and doctor pass. The public 0.21.0 identity passes.
  The target migration preview succeeds without writing: 28 managed copies
  and 16 explicitly selected stock seeds retire; configuration and lock update.
  Every changed path is already in this work order's scope.
- Human mmzen said "Ok go adoption" after publication and marker promotion.
  Preserve that direction. The concrete package still needs confirmation of
  required commit-bound assurance and the sixteen editable-file retirements.

Propose Codex CLI with released plugin 0.2.4 as the configured replacement
for this adoption. Use a disposable profile and the existing trusted native
probe route. A temporary plugin registration changes only that test profile;
restore its prior registration after the rehearsal. Do not change credentials,
hook trust, or the user's desktop plugin configuration.

The exact repository-bound startup and compaction traces, their receipt and
human review remain required before installer apply. Earlier product traces
and the accepted release test omissions do not satisfy this adoption criterion.
Claude and Codex Windows desktop remain unverified; this package claims no
replacement delivery on either host.

## In scope

1. Prepare the published target evaluator outside the checkout. Keep the current
   0.20.1 environment usable by other sessions. Prove the target identity through
   the released evaluator before selecting it for upgrade.
2. Preview external-resource migration using the exact prior public 0.20.1
   wheel. Its SHA-256 is
   300923b4ea800487a7b96822768ff5fbd5c428305ac670948aef404282349764.
   Classify every leaving file before any installer write.
3. Remove the 28 recognized managed files named in execution_scope through the
   reviewed installer transaction. These include ENGINEERING_HARNESS.md, the
   instruction collection and the two machine-policy JSON files.
4. Propose explicit retirement of the following 16 editable resource copies.
   All match the public 0.20.1 wheel after canonical line-ending normalization
   at the refreshed main base. The current preview recognizes them as stock.
   Recheck their actual bytes before apply. Pass one
   --retire-file argument for each selected file; select no other owner file.

- `docs/engineering/ARTIFACT_AUTHORING.md`
- `docs/engineering/templates/ADR.template.md`
- `docs/engineering/templates/ARCHITECTURE.template.md`
- `docs/engineering/templates/CAPABILITY.template.md`
- `docs/engineering/templates/DECISION.template.md`
- `docs/engineering/templates/INTENT.template.md`
- `docs/engineering/templates/OPERATING_CONTRACT.template.md`
- `docs/engineering/templates/README.md`
- `docs/engineering/templates/RELEASE_CONTRACT.template.md`
- `docs/engineering/templates/RELEASE_RECORD.template.md`
- `docs/engineering/templates/REQUIREMENT.template.md`
- `docs/engineering/templates/RISK.template.md`
- `docs/engineering/templates/SPECIFICATION.template.md`
- `docs/engineering/templates/VERIFICATION.template.md`
- `docs/engineering/templates/VERIFICATION_RECORD.template.md`
- `docs/engineering/templates/WORK_ORDER.template.md`

5. Validate and review native replacement delivery before removing the old entry.
   Retain the exact repository, prior lock, planned entry and complete startup/
   compaction traces. Apply only the matching reviewed plan and receipt.
6. Pin owner-maintained CI to 0.21.0. Update current adoption statements and
   resource-discovery links in the named owner guides/indexes. Preserve historical
   release accounts. Adjust the named existing documentation test only where a
   current example or required repository-copy assertion changes with adoption.
7. Run VER-HUP-003, record completion and prepare the adoption verification record
   at one exact clean candidate. Report real results and unresolved host limits.

## Out of scope

Product source, source templates under templates/repository/standard/, new
installer or workflow behavior, broad test changes, accepted-definition changes,
credential changes, release preparation/publication, marketplace publication,
release-marker changes, push/PR and merge. Publishing a compatible plugin remains
separate work. Installing that already released plugin for the exact adoption
rehearsal is a prerequisite whose host effects must be disclosed before execution.

Do not remove AGENTS.md, GLOSSARY.md, domain indexes, formal artifacts or evidence.
Preserve any CLAUDE.md owner content and existing integrations. No new repository
integration is selected. Preserve owner settings except the target version/layout
and the named current documentation and CI changes.

## Proposed assurance and decision envelope

Propose required commit-bound verification because later lifecycle decisions
will rely on the changed evaluator, lock, resource discovery and CI. The human
has not yet reviewed this classification for this new package. Omit assurance
metadata until that decision is recorded; do not invent decided_by.

Within the approved scope and satisfied prerequisites, the agent may prepare
local environments, rehearse migration, apply the reviewed installer plan,
update the named owner files, run checks, retain evidence, commit the candidate,
record completion and prepare verification. Native-retirement review, human
verification acceptance and external actions remain distinct decisions. Existing
adoption approval does not turn this draft into an approved work order.

## Constraints and expected change surface

The reviewed main base is 695d6773dc86f25691a9799e969bcca014207837. Repeat the
preview if any selected file, lock, target identity or retirement choice changes. Use public 0.20.1 for governance
until successful installer apply; use public 0.21.0 for the upgrade operation
and subsequent governance. Never hand-edit the lock or invoke checkout source
as the governing evaluator.

Only the declared selection files, installer removals, current owner-reference
updates, one existing documentation test and this work's formal/evidence paths
may change. Historical links in retained artifacts remain provenance. The
repository's product templates must remain available for distribution builds.
A customized resource, unexpected affected path or incompatible host blocks
that affected step until a reviewed resolution exists.

## Required verification and evidence

Meet A0210-01 through A0210-05 in VER-HUP-003. Retain the target's public provenance,
identities, complete preview, exact seed selection, native receipt and traces,
file comparisons, transaction, check results, failures and candidate identity.

Keep this adoption's review and evidence under
`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-003/`.
The installer transaction belongs at
`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-003-evaluator-upgrade.json`.
The planned record is VREC-HUP-025 with its exact evaluator companion named in
execution_scope. Recheck ID availability before capture; do not overwrite another
record. These destinations do not represent evidence already collected.

Run target identity, doctor, validation, resource discovery, released-root
qualification, no-op replay, preservation comparisons, predecessor assessment,
relevant documentation checks, the full source suite and distribution/CLI checks.
Bind the VREC to the clean adoption candidate. Applicable hosted Linux and Windows
checks remain required before integration. Codex Windows desktop delivery remains
unverified; CLI evidence must not be described as desktop evidence.

## Stop and escalate conditions

Stop the affected action if the published release or identity is missing, the
native delivery receipt is absent or stale, a selected file is customized,
the preview exceeds scope, a required check fails, or a protected environment
is in use. Rehearsal success cannot replace public release provenance. Do not
weaken gates, invent receipts or delete files manually to bypass a refusal.

## Completion report

Report the selected public evaluator, actual retired files, preserved owner and
source content, native host/version limits, transaction, checks and exact VREC.
State the remaining human verification and delivery decisions. Until apply,
this repository remains on 0.20.1 and ENGINEERING_HARNESS.md stays in place.
