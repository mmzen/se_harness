+++
id = "WO-HAG-011"
type = "work_order"
title = "Simplify hosted authoring instructions and client interaction"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-08"
updated = "2026-10-10"

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
5. Run the separately identified intent missing-input diagnostic and positive
   verification-contract case in the linked revised VER-HAG-008. Preserve all
   historical results and prepare commit-bound verification only after required
   checks and the independent content review pass.

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

Run the linked revised VER-HAG-008 EFF-01 through EFF-04 on the exact installed
candidate. EFF-04A2 requires one Claude and one Codex missing-input diagnostic.
EFF-04B requires a correct initial Claude result, two further correct comparable
Claude attempts and one Codex positive result. No approved performance target,
content obligation, independent review or full NQ qualification is waived. Record all
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

## Bounded clarification-report revision

Implement the linked SPEC-HAG-008 / VER-HAG-008 reporting revision only after
its human approval and recorded activation. Within the existing paths, update
the hosted drafting guide and native task's result instructions. A retained final
reply replaces the duplicate report file only for the defined clarification-only
branch. Keep report/recovery duties after any attempted mutation or uncertain
effect. Preserve content criteria, all earlier verdicts and captured failures.

Make the existing intent questions explicit at the clarification step: identify
the missing agreed user outcome and how the owner will observe success. Reuse
confirmed inputs. Do not add the test answer, new lifecycle gates, driver options,
dependencies or a second report generator.

Rerun the existing sequence: one fresh Claude EFF-04A2; stop if it fails. After a
pass, run Codex EFF-04A2 with its boundary probes, then the existing EFF-04B sequence.
Required commit-bound verification and full WO-HAG-009/010 qualification remain.

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

## Bounded qualification revision

The revised REQ-HAG-014, SPEC-HAG-008 and VER-HAG-008 apply only to subsequent
qualification under this work order after their explicit human authorization
and bounded manual activation have been recorded. Earlier approval/start events
retain their exact meaning. Work remains in_progress; no start is repeated.

Implementation paths and required commit-bound assurance are unchanged. The
next correction uses the full artifact type names in instruction links and the
existing unique Procedure section in released CONTINUE.md when its repeated
title makes the narrower slug ambiguous. This reads the canonical current step
without changing released bytes, silently selecting a duplicate, inventing a
next action or adding a selector API. Keep missing/ambiguous source refusals.
Guide the native task to read applicable instructions before first commentary.
This explicit test setup is not evidence of automatic host startup delivery.

Use the existing plugin Markdown references, native test files and resource
tests already listed in execution_scope. No released resource, service, schema,
lifecycle policy, new dependency or provider setting is changed. Retain exact
before/after definition bytes and the actual human decision/activation evidence.

## Linked qualification revision

This revision replaces the complete accepted WO-HAG-011 file at commit `71bd0751dba3cd5305e8c9a07ec7e49bbc08239a`
with SHA-256 `1075ba9e34396dfca5e4516b84e6b2646d0679e3ec7d8a5f7aeb76fdffb2e911` and recorded state `in_progress`.
The [accepted bytes](../evidence/WO-HAG-011/amendment-20261009/WO-HAG-011.accepted.txt)
remain unchanged. Earlier work and evidence keep that definition reference.
The [activation record](../evidence/WO-HAG-011/amendment-20261009/activation.json)
identifies the actual human decision, before/after digests and effect on selected
WO-HAG-011. This link proposes no new machine relation or lifecycle event.

## Bounded Windows Codex permission amendment

The operator may implement and test the session-only Windows Codex qualification
environment specified in VER-HAG-008's "Windows Codex qualification environment"
section, within the existing native-driver and evidence paths. Its explicit
permission grant applies only after mmzen accepts this proposed amendment.
Current work remains in_progress. Earlier events, failures and verification
criteria are preserved. No host-global configuration, permission bypass, human
verification acceptance, merge or release is authorized.

## Linked Windows qualification revision

This revision preserves the complete accepted WO-HAG-011 at commit `9d4034dc293b6f1de7919400d6f8cc1bda356dbd`
with SHA-256 `893c10a1e3835fd9565202e00ac6aa0c575b1c19d5cd59e88f6568c1c93cfae5` in
`../evidence/WO-HAG-011/codex-permissions-20261010/WO-HAG-011.accepted.txt`.
The matching activation record must identify the actual human decision and exact
before/after digests before this revision is applied. Earlier evidence keeps its
original environment and definition references.

## Complete-input delivery amendment

The proposed bounded continuation adds the complete-input presentation defined by
the linked SPEC-HAG-008 and VER-HAG-008 revisions. It changes the disposable native
test entry inside tests/hosted_artifact_graph/, with matching deterministic tests
and task/tool wording. It may reuse the existing client/resource readers but adds
no endpoint, dependency, scriptable workflow or automatic content assessment.

Use the complete original staged fixture and exact applicable instruction sources.
Do not supply the expected missing input or a finished artifact. No template or
released evaluator policy change is included. Preserve current content criteria,
host/model selection, permission probes, evidence and required commit-bound
verification. Keep WO-HAG-009/010 qualification incomplete until its contract passes.

Existing ordinary publication authority for draft PR #543, source
codex/hosted-agent-qualification and target main, remains bounded to this work.
This amendment does not authorize human verification, merge, release, host-plugin
installation or changed host settings. Approval of this proposal would authorize
manual activation of the three linked revisions, preserving their accepted bytes
and lifecycle history, followed by the bounded implementation and qualification.

## Linked complete-input revision

This revision preserves the complete accepted WO-HAG-011 at commit
`a6d85f8d7431728e13bf39b5c48c90f064cd0656`, SHA-256 `992565fec8044b813a58827ba56b5412c25166567a256f226924ac79c62387e1`, in
`../evidence/WO-HAG-011/input-delivery-20261010/WO-HAG-011.accepted.txt`.
The matching activation record must identify the actual human decision and exact
before/after digests before this revision is applied. Earlier evidence retains
its original definition and input-delivery references. Keep prior lifecycle events
unchanged; this link grants no authority by itself.

## Bounded diagnostic revision

After approval and recorded activation of this linked revision, use VER-HAG-008
EFF-04A2 for new missing-input trials. Preserve EFF-04A as historical evidence;
do not reclassify it, remove its failures or combine its measurements with A2.
The positive task, content requirements, goals, hosts, model, permissions,
independence, evidence and required commit-bound assurance remain unchanged.

Existing plugin Markdown and native test paths cover clarification of local
versus remote command applicability and selection of the exact new task.
No canonical resource, evaluator, server, schema, host setting or build identity
rule may change under this revision. Stop after a failed first Claude A2 trial;
return its observed limitation for review before another task or instruction
variation. Later required native cases proceed only after that diagnostic passes.

The proposed activation is manual because released 0.22.1 has no supported
linked-revision command. It requires mmzen's explicit approval of these exact
three proposed files and this bounded activation, with complete accepted copies,
before/after digests and the human decision retained. Keep existing lifecycle
events and states unchanged. No approval, start or verification is replayed.
The existing draft-PR grant remains unchanged; merge and release are excluded.

## Linked diagnostic revision

This revision preserves the complete accepted WO-HAG-011 at commit
`8ed1ae5391ec1b405b132b9d120ab91a47803cca`, SHA-256 `b40b961ff3c775f8b4afc7335415cf62f63b866858029c890471bd4f92faa05b`, and recorded
state `in_progress` in
`../evidence/WO-HAG-011/diagnostic-review-20261010/WO-HAG-011.accepted.txt`.
The activation record must identify the actual human decision and exact
before/after digests before this revision governs work. Earlier evidence keeps
its original definition and task references. No machine relation or lifecycle
event is invented by this link.

## Linked clarification-report revision

This revision preserves the complete accepted WO-HAG-011 at commit
`7f664d04f69f53fc91287e6c5b71575dfcf9d385`, SHA-256 `b2908dad0135edab3c2d88f963063ab59352832e8102d899c04d0641b0db1e55`, and recorded
state `in_progress` in
`../evidence/WO-HAG-011/clarification-contract-20261010/WO-HAG-011.accepted.txt`.
Before this revision governs work, retain the actual human decision, exact
before/after digests and its effect on WO-HAG-011 in the activation record.
Earlier evidence keeps its original definition and verdict. This link creates
no machine relation or lifecycle event.
