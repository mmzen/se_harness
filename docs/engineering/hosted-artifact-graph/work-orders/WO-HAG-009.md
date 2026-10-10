+++
id = "WO-HAG-009"
type = "work_order"
title = "Qualify native Codex and Claude hosted workflows"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-07"
updated = "2026-10-07"

[assurance]
commit_bound_verification = "required"
rationale = "mmzen confirmed required verification because the native qualification claim depends on the exact candidate instructions, drivers, component identities and retained host evidence."
decided_by = "mmzen"

[execution_scope]
paths = ["docs/engineering/hosted-artifact-graph/verification/VER-HAG-007.md", "docs/engineering/hosted-artifact-graph/work-orders/WO-HAG-009.md", "docs/engineering/hosted-artifact-graph/README.md", "docs/engineering/hosted-artifact-graph/risks/RISK-HAG-001.md", "docs/engineering/hosted-artifact-graph/risks/RISK-HAG-002.md", "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-009/", "tests/hosted_artifact_graph/", "tests/plugin_integration/test_simple_plugin.py", "plugins/verity-plane/common/skills/setup/SKILL.md", "plugins/verity-plane/common/skills/change/SKILL.md", "plugins/verity-plane/common/skills/evidence/SKILL.md", "plugins/verity-plane/common/skills/harness-orient/SKILL.md", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "server/README.md", "server/contracts/lifecycle-v2.md", "docs/notes/hosted-artifact-graph.md", "docs/notes/harnessctl-reference.md"]

[relations]
implements = ["REQ-HAG-011", "REQ-HAG-012", "REQ-HAG-013"]
specifications = ["SPEC-HAG-007"]
architecture = ["ARCH-HAG-003", "ADR-HAG-003"]
verification = ["VER-HAG-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-07T01:50:55Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"I approve\" to the reviewed WO-HAG-009 and VER-HAG-007 package at 540bd9fb3a79cf7d8cfaccf01c52b9e8f7b0f133 in PR #543, confirming required commit-bound verification and bounded local Codex CLI/Claude Code qualification. The grant includes ordinary review pushes and PR updates in mmzen/se_harness from codex/hosted-agent-qualification to main, the ready record and the later separately supplied human verification decision, and marking the same PR ready only after that decision is recorded and remote. Git remains authoritative. This grants no verification acceptance, merge, release, public deployment, host-plugin update or risk acceptance."
scope_paths = ["docs/engineering/hosted-artifact-graph/verification/VER-HAG-007.md", "docs/engineering/hosted-artifact-graph/work-orders/WO-HAG-009.md", "docs/engineering/hosted-artifact-graph/README.md", "docs/engineering/hosted-artifact-graph/risks/RISK-HAG-001.md", "docs/engineering/hosted-artifact-graph/risks/RISK-HAG-002.md", "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-009/", "tests/hosted_artifact_graph/", "tests/plugin_integration/test_simple_plugin.py", "plugins/verity-plane/common/skills/setup/SKILL.md", "plugins/verity-plane/common/skills/change/SKILL.md", "plugins/verity-plane/common/skills/evidence/SKILL.md", "plugins/verity-plane/common/skills/harness-orient/SKILL.md", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "server/README.md", "server/contracts/lifecycle-v2.md", "docs/notes/hosted-artifact-graph.md", "docs/notes/harnessctl-reference.md"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-07T01:52:57Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Qualify native Codex and Claude hosted workflows

## Objective

Qualify Codex CLI and Claude Code on Windows for the complete private hosted
lifecycle, with separate native evidence and a clear pass or gap for each host.
Git remains authoritative. DEC-HAG-004's test-copy boundary is unchanged.

## In scope

1. Freeze the exact client, plugin guidance, service, evaluator and fixture
   identities. Reuse the qualified Phase 3 runtime where its bytes match.
2. Prepare separate private test projects and session-local candidate guidance.
   Check provider authentication through normal host interfaces and a small live
   request; do not infer validity from a stored login status.
3. Run all five VER-HAG-007 scenarios independently through each real host. The
   agent chooses the workflow commands; an opaque scripted walkthrough is not
   sufficient. Record procedural help, failures and final unassisted reruns.
4. Make bounded corrections to test drivers and explanatory guidance when needed.
   Clarify existing behavior without changing its protocol, lifecycle policy,
   decision rights or actual authority boundary.
5. Correct stale Phase 3 status text in the listed documentation. Preserve
   historical package snapshots, records and evidence. Separate present facts
   from the observations recorded by earlier packages.
6. Run supporting checks, assess each host and prepare required verification
   bound to the exact final candidate.

## Out of scope

New service/client behavior, evaluator changes, wire schema or persistence changes,
new writable MCP tools, authentication or database ACL implementation, authoritative
graph use, public access/deployment, production durability, releases/tags/registry
or marketplace publication, updating the owner's actual host plugin, Codex desktop,
automatic startup/compaction/resume qualification, CI policy changes, and merge.
No rewriting of accepted definitions or historical VREC evidence is permitted.

## Existing authority and proposed decision envelope

The user requested this follow-up after reviewing the proposal for an agent-driven
pilot: "Next tasks: qualify codex and claude". Preparation and early draft review
publication follow that request and the existing preference for an accessible
branch/PR. These draft artifacts do not record implementation approval.

Proposed approval of WO-HAG-009 and VER-HAG-007 authorizes bounded local execution,
test drivers/guidance edits, disposable private containers, local qualification
packages, actual Codex CLI and Claude Code sessions using existing accounts,
checks, evidence, local commits, completion recording and VREC preparation.
The executor may choose internal test-driver layout, bounded timeouts and
temporary paths, and use supported session-local configuration. Native sessions
remain part of this qualification work; they receive no real human decision right.

The proposed review-publication grant names `mmzen/se_harness`, source
`codex/hosted-agent-qualification`, target `main`, and the matching draft PR.
It includes ordinary pushes and PR updates for this bounded work and its ready
verification record, plus the later decision-only push and **marking that same PR
ready after separate human verification is recorded and remote**. It permits no
force-push, merge, release, deployment, provider-setting change or risk acceptance.
Human verification remains a separate decision. Retain the PR in draft until then.

## Proposed assurance classification

Propose `commit_bound_verification = "required"`: later qualification and delivery
decisions depend on the exact host evidence, test drivers and instructions. Ask
mmzen to confirm this classification with the reviewed package. The `[assurance]`
decision fields will be recorded only after that actual human confirmation;
draft authorship does not supply `decided_by`.

## Constraints

- Reuse INT-HAG-002, CAP-HAG-002, REQ-HAG-011/012/013, SPEC-HAG-007 and
  ARCH-HAG-003/ADR-HAG-003 unchanged. No new architecture or requirement is needed:
  this work assesses native use of the already-defined behavior.
- Keep released evaluator 0.22.1 separate from the candidate remote client.
  Preserve the source/component binding behind VREC-HAG-005.
- Use one fresh disposable project per host with matching initial fixture bytes.
  Keep real repository artifacts read-only to the tested agents. Allow writes
  only in their declared temporary test area and the selected private service.
- Keep normal permission checks. Do not bypass sandboxing, approval review or
  hook trust. A denied action is evidence, not permission to switch routes.
- Use existing authentication without exposing or copying credentials into
  prompts, transcripts or the repository. An unavailable live login blocks that
  host; it does not make its tests optional. Request only genuinely needed human
  sign-in assistance. Do not change account or machine security configuration.
- Each long-running session has a recorded time limit and visible progress.
  Stop an unproductive loop; preserve partial results instead of inventing a pass.

## Expected change surface

| Inspected path | Purpose and bounds |
| --- | --- |
| `tests/hosted_artifact_graph/` | Existing qualification component: reuse fixture/parity/export/fault helpers and add native transcript orchestration and comparison; no replacement workflow engine or hidden scripted completion |
| `tests/plugin_integration/test_simple_plugin.py` | Focused checks for packaged instruction changes, if any |
| `plugins/verity-plane/common/skills/setup/SKILL.md` | Clarify exact private-test selection and component identities when native runs reveal ambiguity |
| `plugins/verity-plane/common/skills/change/SKILL.md` | Clarify supported rehearsal commands and test-only decisions |
| `plugins/verity-plane/common/skills/evidence/SKILL.md` | Clarify receipt recovery, exact export and synthetic versus actual VREC claims |
| `plugins/verity-plane/common/skills/harness-orient/SKILL.md` | Clarify native MCP reading and incomplete-response reporting |
| `plugins/verity-plane/codex/README.md`, `plugins/verity-plane/claude-code/README.md` | Accurate candidate/host qualification statements, without public-install or desktop claims |
| `server/README.md`, `server/contracts/lifecycle-v2.md` | Existing operator/wire guidance only; correct stale status and explain current bounded operations |
| `docs/notes/hosted-artifact-graph.md`, `docs/notes/harnessctl-reference.md` | Discoverable operator procedure and supported CLI examples |
| This domain's `README.md` | Discover the proposed work and distinguish completed Phase 3 verification from the new native qualification |
| `verification/VER-HAG-007.md`, `work-orders/WO-HAG-009.md` | Reviewed drafts and later explicit lifecycle decisions; accepted meaning is preserved |
| `risks/RISK-HAG-001.md`, `risks/RISK-HAG-002.md` | Add this affected work to existing raised-risk links; no acceptance, changed owner, disposition or historical event |
| `evidence/WO-HAG-009/` | Review assessment, exact run evidence, failures, native transcripts, independent comparisons, handoff and actual VREC preparation |

Repository-relative paths above are controlled by `[execution_scope].paths`.
The qualification component is a narrow existing directory because native runs
share its transport, fixture and replay helpers. No service implementation, client
implementation, package assembler, hook/activation code, root versions, dependency
locks or CI workflow changes are planned or authorized. Their existing checks are
consumers. If those paths need correction, prepare a bounded scope proposal first.

The actual VREC and evaluator-sidecar paths are unresolved until released capture
allocates them. The existing generated-output rule for a record directly verifying
WO-HAG-009 and its declared evaluator evidence is expected to apply. Assess the
returned paths then; do not admit the parent directories or invent an ID now.
Temporary host directories, source projections, private credentials and container
volumes remain outside Git. Only required bounded evidence is retained here.

## Required verification

Run VER-HAG-007: NQ-01 through NQ-05 for both hosts, with actual native calls and
independent evidence checks. Both must pass for completion. Run applicable full
source, distribution, CLI and focused driver/package tests, released validation,
scope and handoff checks. A scripted, assisted, skipped or unavailable scenario
is not the required final pass. Preserve VREC-HAG-005's exact earlier observations.

## Evidence to record

Use `docs/engineering/hosted-artifact-graph/evidence/WO-HAG-009/`. Retain the concise
per-host assessment and all inputs required by VER-HAG-007, including package/source
identities and command arrays. Use a small selected transcript/export archive with
digests when needed, not entire run directories. Preserve failures and compare
real checkout/host state before and after each test. Real VREC preparation follows
the released command on a clean candidate; no host's test VREC verifies this work.

## Stop and escalate conditions

Stop the affected action for an expired/unavailable login, denied host operation,
incorrect component identity, missing required transcript, protocol/runtime defect,
new path, changed accepted behavior or authority, failed required check, or any
write outside the test boundary. Preserve the observation and continue only
independent work. A changed qualification criterion or accepted omission requires
a separate human decision; this work cannot silently waive a failing host.

## Completion report format

Give the exact candidate and component tuple, a Codex/Claude scenario table,
instruction discovery and intervention findings, independent replay results,
repository checks, evidence links, exclusions and raised risks. Report the
released evaluator's actual next step. Completion does not verify, merge,
publish, deploy or change real artifact authority.
