+++
id = "WO-HAG-011"
type = "work_order"
title = "Simplify hosted authoring instructions and client interaction"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-08"
updated = "2026-10-08"

[assurance]
commit_bound_verification = "required"
rationale = "mmzen confirmed required commit-bound verification because later qualification and release decisions depend on exact client behavior, instructions and retained native evidence."
decided_by = "mmzen"

[execution_scope]
paths = [
  "se_harness/remote.py",
  "se_harness/remote_authoring.py",
  "se_harness/resources.py",
  "se_harness/cli.py",
  "tests/test_remote_client.py",
  "tests/test_resources.py",
  "tests/hosted_artifact_graph/",
  "tests/plugin_integration/test_simple_plugin.py",
  "plugins/verity-plane/common/assets/bootstrap.md",
  "plugins/verity-plane/common/skills/setup/",
  "plugins/verity-plane/common/skills/change/",
  "plugins/verity-plane/common/skills/evidence/",
  "plugins/verity-plane/common/skills/harness-orient/SKILL.md",
  "plugins/verity-plane/common/skills/harness-orient/references/",
  "plugins/verity-plane/codex/README.md",
  "plugins/verity-plane/claude-code/README.md",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/hosted-artifact-graph.md",
  "docs/engineering/hosted-artifact-graph/requirements/REQ-HAG-014.md",
  "docs/engineering/hosted-artifact-graph/specifications/SPEC-HAG-008.md",
  "docs/engineering/hosted-artifact-graph/verification/VER-HAG-008.md",
  "docs/engineering/hosted-artifact-graph/work-orders/WO-HAG-011.md",
  "docs/engineering/hosted-artifact-graph/README.md",
  "docs/engineering/hosted-artifact-graph/risks/RISK-HAG-001.md",
  "docs/engineering/hosted-artifact-graph/risks/RISK-HAG-002.md",
  "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-011/",
]

[relations]
implements = ["REQ-HAG-014"]
specifications = ["SPEC-HAG-008"]
verification = ["VER-HAG-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-08T16:06:05Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"I approve\" to the reviewed REQ-HAG-014, SPEC-HAG-008, VER-HAG-008 and WO-HAG-011 package on 2026-10-08. Approves the bounded client and instruction implementation with required commit-bound verification. Includes ordinary review pushes and updates to draft PR #543 in mmzen/se_harness, source codex/hosted-agent-qualification, target main, its ready verification record and the later separately supplied verification-decision commit. Keep the PR draft while WO-HAG-009/010 qualification remains incomplete. Git remains authoritative. No human verification acceptance, merge, force-push, release, adoption, host-plugin update, permission bypass or changed qualification criterion is granted."
scope_paths = ["se_harness/remote.py", "se_harness/remote_authoring.py", "se_harness/resources.py", "se_harness/cli.py", "tests/test_remote_client.py", "tests/test_resources.py", "tests/hosted_artifact_graph/", "tests/plugin_integration/test_simple_plugin.py", "plugins/verity-plane/common/assets/bootstrap.md", "plugins/verity-plane/common/skills/setup/", "plugins/verity-plane/common/skills/change/", "plugins/verity-plane/common/skills/evidence/", "plugins/verity-plane/common/skills/harness-orient/SKILL.md", "plugins/verity-plane/common/skills/harness-orient/references/", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "docs/notes/harnessctl-reference.md", "docs/notes/hosted-artifact-graph.md", "docs/engineering/hosted-artifact-graph/requirements/REQ-HAG-014.md", "docs/engineering/hosted-artifact-graph/specifications/SPEC-HAG-008.md", "docs/engineering/hosted-artifact-graph/verification/VER-HAG-008.md", "docs/engineering/hosted-artifact-graph/work-orders/WO-HAG-011.md", "docs/engineering/hosted-artifact-graph/README.md", "docs/engineering/hosted-artifact-graph/risks/RISK-HAG-001.md", "docs/engineering/hosted-artifact-graph/risks/RISK-HAG-002.md", "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-011/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-08T16:09:01Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed. Human mmzen answered \"I approve\" to the reviewed REQ-HAG-014, SPEC-HAG-008, VER-HAG-008 and WO-HAG-011 package on 2026-10-08. Approves the bounded client and instruction implementation with required commit-bound verification. Includes ordinary review pushes and updates to draft PR #543 in mmzen/se_harness, source codex/hosted-agent-qualification, target main, its ready verification record and the later separately supplied verification-decision commit. Keep the PR draft while WO-HAG-009/010 qualification remains incomplete. Git remains authoritative. No human verification acceptance, merge, force-push, release, adoption, host-plugin update, permission bypass or changed qualification criterion is granted."
+++

# Simplify hosted authoring instructions and client interaction

## Objective

Reduce instruction length, repeated content, tool calls and elapsed time for
hosted artifact authoring, while preserving exact content, evidence and current
authority. Implement REQ-HAG-014 and assess it through VER-HAG-008.

## In scope

1. Add typed inputs and exact file submission to the existing remote client.
2. Add concise result/evidence handling and focused canonical section views.
3. Shorten skill entry points and move route details to selected references.
4. Adapt the native test boundary to call that installed public interface.
5. Run the focused Claude/Codex comparisons, supporting checks and independent
   review. Preserve historical evidence and prepare commit-bound verification.

The user confirmed the proposal with "Ok" on 2026-10-08. That confirms direction;
this draft presents the exact implementation scope and assurance for approval.
WO-HAG-009/010 retain their existing authority and incomplete qualification.

## Out of scope

Service endpoints, wire schema or persistence changes; lifecycle evaluator policy;
accepted template/checklist meaning; new authentication or database ACLs; real graph
authority; writable MCP tools; host/plugin installation; release, adoption, public
deployment, merge, provider settings, new dependencies, background orchestration,
CI policy and a separate KIS approval or benchmark framework.

## Authorized decision envelope

After approval, the agent may choose internal functions and CLI option spelling,
implement the named behavior, build disposable packages, use existing authorized
accounts for real CLI tests, retain evidence, commit and prepare verification.
It may choose temporary paths and bounded timeouts. No permission bypass or new
credential collection is included. Human verification remains separate.

Proposed review-publication authority: ordinary pushes and updates to existing
draft PR #543 in mmzen/se_harness, source codex/hosted-agent-qualification, target
main, for this work and its four governing drafts/decisions, ready verification
record and later separately supplied verification decision. Keep the PR draft
while WO-HAG-009/010 qualification remains incomplete. No force-push or merge.

Proposed assurance is required: later host qualification and release decisions
depend on exact client behavior, instructions and evidence. Record mmzen's actual
classification decision in metadata only after confirmation of this package.

## Constraints

Git remains authoritative. Use released 0.22.1 outside the checkout as governor;
candidate source is only implementation/test input. Preserve original approved
artifacts, source manifests, operation receipts and all earlier evidence.
RISK-HAG-001 and RISK-HAG-002 remain raised. Add affected-work links only.

The existing client/service boundary is unchanged. No active architecture addresses
REQ-HAG-014, so no architecture relation is fabricated. SPEC-HAG-008 records why
the existing architecture is a constraint and no new decision is needed.

## Expected change surface

| Inspected path/component | Purpose and limit |
| --- | --- |
| se_harness/remote.py; new se_harness/remote_authoring.py | Existing registration, transport and result boundary; typed adaptation and exact file/evidence handling, no parallel workflow |
| se_harness/resources.py; se_harness/cli.py | Extend existing resource views with complete selected sections; preserve identity and raw modes, no evaluator-policy change |
| tests/test_remote_client.py; tests/test_resources.py | Independent wire/content equivalence and meaningful input/output failure boundaries |
| tests/hosted_artifact_graph/ | Existing native boundary, fixture lookup, timing and evidence comparison; delegate new behavior to installed client, no hidden completion |
| tests/plugin_integration/test_simple_plugin.py | Both host packages contain the selected entry/reference files and preserve route behavior |
| plugins/verity-plane/common/assets/bootstrap.md | Route to applicable instructions without restating them; preserve host startup behavior |
| Common skills setup/, change/, evidence/; harness-orient/SKILL.md and references/ | Shorten entry text and move existing details into task references; only Markdown instruction changes in these component paths |
| plugins/verity-plane/codex/README.md; plugins/verity-plane/claude-code/README.md | Accurate candidate interface and qualification limits |
| docs/notes/harnessctl-reference.md; docs/notes/hosted-artifact-graph.md | Discover the actual CLI options and bounded walkthrough |
| REQ-HAG-014, SPEC-HAG-008, VER-HAG-008, this work order | Prepared package, review and later matching lifecycle decisions; no silent amendment after approval |
| Domain README.md; risks/RISK-HAG-001.md and risks/RISK-HAG-002.md | Discover the package; add affected-work links without changing risk state or history |
| evidence/WO-HAG-011/ | Package review, exact checks, comparison, handoff and preparation evidence |

The existing package assembler includes skill references recursively. No assembler,
version, dependency-lock, server, workflow or installer edit is planned. Existing
checks are consumers. The skill directories are narrow existing components needed
to relocate instructions; executable scripts or skill contracts inside them are
not authorized for behavioral changes by this work order.

The actual VREC ID and evaluator sidecar are allocated later. Use the released
generated-output rule only for records directly verifying this work and their
declared evidence; check exact returned destinations at capture. No blanket grant
to the domain evidence/ or verification-records/ directories is inferred.

## Required verification

Run VER-HAG-008 EFF-01 through EFF-04 on the exact installed candidate. Record all
timing goals and failures. Run focused checks, the repository source suite,
distribution checks, CLI smoke, exact package checks, released validation and
scope/handoff checks. Do not rerun unchanged service qualification merely because
guidance changed; justify any reused evidence with byte/component comparisons.

VER-HAG-007 remains required for WO-HAG-009/010. This work's focused results do not
complete those work orders or waive any NQ scenario, independent check or host.

## Evidence to record

Use this work order's evidence directory. Keep one concise assessment and exact
linked command/result evidence, visible native transcripts and component identities.
Retain an explanation of private-reasoning/credential omissions when applicable.
Keep transient plans and helper scripts outside the repository. Preserve historical
evidence bytes; no correction to an old report may erase its original observation.

## Stop and escalate conditions

Stop affected work for a new path/component, changed accepted meaning, missing
selected instructions, failed required check, denied action, unknown write,
unavailable host authentication or a required service/policy change. Inspect
uncertain effects before retrying. Report a missed performance goal and its cause;
do not hide it or declare efficiency established by a passing unit suite.

## Completion report format

Report the actual interface and instruction changes, candidate identity, correctness
findings, per-host timing/context/call comparison, remaining costs and full-qualification
limits. Use the released evaluator's actual next step. No result grants human
verification, release, installation or merge authority.
