+++
id = "WO-PLG-023"
type = "work_order"
title = "Prepare Verity Plane marketplace publication"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-15"
updated = "2026-09-15"

[assurance]
commit_bound_verification = "required"
rationale = "Users and later publication decisions will rely on the committed packaging, catalog paths and installation instructions."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/plugin-integration/requirements/REQ-PLG-038.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-022.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-023.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-023.md",
  "docs/engineering/plugin-integration/README.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-023/",
  "docs/engineering/plugin-integration/verification-records/",
  "plugins/verity-plane/common/skills/harness-operator-brief/agents/openai.yaml",
  "plugins/verity-plane/codex/README.md",
  "plugins/verity-plane/claude-code/README.md",
  "release/plugin-assembly.json",
  "release/plugin-marketplace/",
  "scripts/build_plugin_marketplace.py",
  "repository_tools/plugin_distribution.py",
  "tests/plugin_integration/package_assembly/",
  "docs/notes/plugin-installation-guide.md",
  "docs/notes/plugin-marketplace-publication.md"
]

[relations]
implements = ["REQ-PLG-001", "REQ-PLG-002", "REQ-PLG-027", "REQ-PLG-038"]
specifications = ["SPEC-PLG-001", "SPEC-PLG-016", "SPEC-PLG-021", "SPEC-PLG-022"]
architecture = ["ARCH-PLG-001", "ADR-PLG-001"]
verification = ["VER-PLG-001", "VER-PLG-016", "VER-PLG-023"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-15T13:40:15Z"
decided_by = "engineering-owner"
reason = "The owner reviewed the four marketplace drafts and replied \"OK i approve the artifacts you can start\" on 2026-09-15. Record approval of this exact reviewed artifact in the named accountable role. This authorizes WO-PLG-023 execution under DR-015, not verification of a future candidate or a provider submission."
scope_paths = ["docs/engineering/plugin-integration/requirements/REQ-PLG-038.md", "docs/engineering/plugin-integration/specifications/SPEC-PLG-022.md", "docs/engineering/plugin-integration/verification/VER-PLG-023.md", "docs/engineering/plugin-integration/work-orders/WO-PLG-023.md", "docs/engineering/plugin-integration/README.md", "docs/engineering/plugin-integration/evidence/WO-PLG-023/", "docs/engineering/plugin-integration/verification-records/", "plugins/verity-plane/common/skills/harness-operator-brief/agents/openai.yaml", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "release/plugin-assembly.json", "release/plugin-marketplace/", "scripts/build_plugin_marketplace.py", "repository_tools/plugin_distribution.py", "tests/plugin_integration/package_assembly/", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-15T13:43:42Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Codex starts the approved scope under DR-015 after the owner said OK i approve the artifacts you can start and the start checkpoint passed."
+++

# Prepare Verity Plane marketplace publication

## Objective and current state

Prepare committed, checked marketplace inputs and complete distributions for
Verity Plane 0.1.0 with the released SE Harness 0.18.0 wheel. This carries the
owner's 2026-09-15 marketplace request through governed implementation and
candidate assurance, toward publication in `mmzen/se_harness` at
`plugin-marketplace` and preparation of provider catalog submissions.

Earlier local packages and tests were produced before an appropriate WO was
selected. Preserve them as preliminary inputs. This draft does not approve
those earlier actions or relabel their output as formally verified.

## In scope

1. Integrate the reviewed operator-brief display metadata and add the existing
   license to the shared assembly plan; preserve skill instructions and setup.
2. Commit the two standard catalogs and concise public installation instructions.
   Compose them with the existing builder's exact-source native output using
   the small command described in SPEC-PLG-022. Make only the compatibility
   changes to the existing assembly module needed for this composition/license.
3. Check final local marketplace installation, contents, ordinary rejection
   cases and the existing setup route in disposable host profiles. Reuse
   unchanged evidence with an explicit comparison of inputs.
4. Prepare OpenAI skills-only and supported Anthropic community submission
   materials. Keep publisher-supplied identity, contact, legal URLs, regions and
   attestations explicit where unavailable. Correct the plugin index and guide
   only where necessary to describe this delivery and its actual baseline.
5. Retain evidence, complete the work and prepare its commit-bound VREC through
   the selected released evaluator. Build all derived archives and disposable
   environments outside the source checkout; retain their identities in evidence.

## Out of scope

No checker release or upgrade, setup algorithm change, PyPI fallback, runtime
bundling, automatic hooks, new service, model-driven support claim, generic
publication framework, new CI lane, or change to historical VREC/RLS/DEC facts.
The verification-record directory is permitted only for newly prepared records
covering this work. Broad directory entries grant no unrelated behavior changes.
Existing source release tags, PyPI releases and the `last` marker are untouched.

## Decision envelope and delivery

The author may prepare this draft package. Only an actual owner decision on its
reviewed inputs approves the definitions and WO. After approval, Codex may start,
implement, test, make local commits, record completion and prepare verification
under DR-015 without repeated execution permission.

The requested publication destination is `mmzen/se_harness:plugin-marketplace`.
The source implementation belongs on `work/plugin-marketplace-publication` for
review. Preserve the owner's existing publication instruction; compare its exact
inputs with the eventual candidate, destination and passing gates. WO approval
does not make an assurance decision or authenticate a different external target.
Obtain the applicable verification and delivery results before push/PR, merge or
publication. Never overwrite a conflicting remote ref. Prepare provider catalog
materials now; no third-party submission or legal attestation is inferred from
this preparation scope. A new external publication record may retain M05 after
the authorized public Git operation, without changing earlier verification facts.

## Verification and evidence

Run VER-PLG-023 M01-M04, applicable VER-PLG-001 package checks, VER-PLG-016
walkthrough checks, and the repository-required suite and distribution checks.
Use the external released evaluator 0.18.0 for doctor, graph validation,
phase-appropriate preflight and schema-2 workflow checkpoints. Inspect the
complete diff against this exact path scope. Read every selected phase manifest
file. Record actual failures and resolve only in-scope causes.

Retain one concise evidence summary with source and wheel identities, final
package hashes, command results, review findings and coverage. Source candidate
and VREC are separate commits. M05 belongs to the later public observation;
implementation completion does not claim it already passed.

## Stop conditions and completion report

Stop the affected action for missing authority, invalid managed integrity or
selected graph, failed required gates, input identity mismatch, conflicting
remote destination or a necessary change outside this scope. Missing publisher
fields stop the dependent portal submission, not local preparation. Use the
installed evaluator's actual next action and preserve existing lifecycle states.

Report what changed, the measured checks and their limits, artifact IDs and
final states, publication/submission status, and the single next accountable
decision from the selected schema-2 workflow result.
