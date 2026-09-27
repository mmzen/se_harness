+++
id = "SPEC-IAR-014"
type = "specification"
title = "Progressive discovery of harness instructions"
status = "approved"
owners = ["repository-owner", "technical-owner"]
created = "2026-09-20"
updated = "2026-09-27"
contract = "Provide a compact released entry, action-selected instruction files and evaluator-owned discovery while safely retiring the AGENTS managed gate."

[relations]
specifies = ["REQ-IAR-022", "REQ-IAR-023", "REQ-IAR-024", "REQ-IAR-025", "REQ-IAR-026", "REQ-IAR-027"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T07:37:39Z"
decided_by = "technical-owner"
reason = "User instruction: so let's start the work orders. Apply the reviewed package under DEC-IAR-001 versioned-successor; selected 0.18.0 governance remains installed until separate release/adoption."
+++

# Progressive discovery of harness instructions

## Contract and release boundary

This contract changes how instructions are owned, packaged and delivered. It
does not change lifecycle transitions, decision-right IDs or command authority,
or waive required lifecycle gates. Instruction integrity and readiness checks
are updated to the new versioned ownership and discovery model. The repository remains governed by its selected 0.18.0
evaluator until a separately authorized release and installation adopts the
new contract. Candidate behavior is tested separately from that released baseline.

The two immutable review inputs beside this package in
`../proposals/progressive-discovery/` are design provenance. They are not an
installed contract or evidence that the future implementation passed tests.
The source draft's 0.18.0 header does not make its proposed behavior available.

## Rules

**IAR-DIS-001.** Entry. Inject the repository-root ENGINEERING_HARNESS.md at
startup and after compaction on each supported host. It owns the RFC language,
Goals, HRN-001 through HRN-009 with their agreed names and meanings, applicability,
the brief authority boundary, command convention, transient-material rule and
reading router. The 1,000–1,300-word target is a writing budget, not a hard limit.

**IAR-DIS-002.** Conditional reading. The root selects the first file by task
condition. Each action names exact required file/heading references and when
they apply. Read the current step and its prerequisites; do not require every
linked file or later stage. Governing formal artifacts remain required inputs.

**IAR-DIS-003.** Procedure structure. Each action file contains Read this when,
Before this action, Procedure and Read next when. Each procedural step states
Inputs, Output, Actions, Harness commands, Completion and Later use. Output
names created or modified artifacts/files, or says none. No harness command is
invented for an action carried out by ordinary editing or discussion. Human
clarification may iterate before dependent definitions are written. All 31 main
steps in the review source become descriptive, stable Markdown headings.

**IAR-DIS-004.** Discovery contract. Update evaluator reading results to separate
agent instructions, governing formal artifacts and evaluator-only inputs.
For every returned procedure and typed step, provide its exact file/heading and
conditional prerequisites. Keep a single mapping that released packaging and
conformance checks can use; its implementation format is not prescribed here.
The mapping translates evaluator-selected identifiers into reading locations.
It does not select lifecycle states, transitions or next actions. Maintain
compatibility with existing result consumers or report an explicit version
mismatch; do not silently reinterpret an existing field.

**IAR-DIS-005.** Machine boundary. WORKFLOW.json and QUALITY_GATES.json stay
evaluator inputs and retain their required checks. Normal agent procedures
consume evaluator results. Reading machine contracts is conditional on work
on those contracts or a diagnostic investigation, not ordinary lifecycle use.
Checkpoint-free check remains context only, not a gate assessment or approval.
Supported record types keep their existing inspection/check distinctions.

**IAR-DIS-006.** Owner file. A fresh installation neither generates AGENTS.md
nor requires its existence or contents as harness authority. An existing owner
file can still supply applicable repository instructions. Remove the legacy
managed fragment, including both markers, only after matching the recognized
installed fragment and validating the replacement instruction delivery. Do not
leave a migrated repository with neither the old entry nor a usable new entry. Retire its lock and readiness requirements in the same
successful migration. Preserve every other byte, including original encoding
and line endings. If no owner bytes remain, the migration may remove the empty
harness-created file. Refuse ambiguous or customized fragments before writes.

**IAR-DIS-007.** Adoption boundary. This repository also has harness instructions
outside the old block. The installer must not delete them as though they were
managed. Prepare a reviewed owner-edit map covering Commands, Ungoverned paths,
scope, ownership/version notes, Traps and the opening hook. A separate adoption
work order applies those exact edits after a compatible release is selected.
Preserve project facts and project commands. Retire CLAUDE.md's harness adapter
or change its role through the same explicit migration; AGENTS.md cannot remain
an indirect harness entry. Preserve unrelated owner content in every adapter.

**IAR-DIS-008.** Fresh context. The host integration reads the selected
repository and released root, not a cached copy from another repository or
the plugin's default version. After compaction, the agent recovers selection,
authority and pending action; obtains fresh evaluator context where supported;
and rereads required instructions no longer in context. A summary preserves
pointers and known decisions, not lifecycle truth. Inspect uncertain writes or
external effects before retrying. Do not replay completed actions automatically.

**IAR-DIS-009.** Availability. Advertise automatic delivery only for hosts whose
startup and compaction behavior has been demonstrated. Report missing or
incompatible input and the affected action. No success claim, automatic upgrade,
or return to an AGENTS managed gate is a fallback for unavailable delivery.
Host-specific configuration is outside AGENTS.md and outside real user settings
during development tests.

**IAR-DIS-010.** Canonical policy. Every detailed rule has one canonical
destination. Short reminders and links may repeat the obligation at its action
point. COMMUNICATION.md owns communication policy; any retained old guide is a
compatibility pointer, not a second normative copy. Required harness instruction
content and its discovery mapping have an explicit released ownership/integrity
record. Existing customized editable guides require an explicit migration plan;
do not silently overwrite or delete them to install the new managed guides.

**IAR-DIS-011.** Preserved semantics. Retain the agreed Human/Agent distinction,
human-reserved approvals, verification acceptance and release decisions, and
agents' ability to apply recorded decisions. Keep actual identity and authority
separate from profile names. Explain legacy machine labels without rewriting
history or changing the evaluator's rights in this package. Preserve exact
command operands, IDs, hashes and evidence. Instruction prose describes what
the agent does, not implementation requirements for harnessctl.

**IAR-DIS-012.** Unsupported capabilities. EXCEPTIONS.md states whether the
selected release supports owner-configured exceptions and gives the governed
fallback when it does not. Configurable exceptions may concern definitions and
work orders only; lifecycle and required gates remain fixed. AMEND_DEFINITIONS.md
preserves the linked-revision objective and reports the selected release's
limitation. This package implements neither exception evaluation nor a generic
accepted-definition revision mechanism. It invents no schema, command or relation.

**IAR-DIS-013.** Coverage. Produce a complete source heading and rule map with
dispositions: moved, retained, corrected by recorded review, or deferred with
reason. Historical rule references retain their versioned meaning. Resolve
the three stale Lifecycle meaning links and the decision-right annotation;
do not ship review markers or an empty exception procedure as usable guidance.
Preserve applicable authoring checklists at their existing path and link exact
type headings. No policy change is authorized merely by a relocation label.

**IAR-DIS-014.** Reading cost. Measure root words and complete additional
instruction reads for new drafting, resumed execution, verification decision,
PR preparation, blocker recovery and evaluator setup. Count COMMUNICATION.md
before the first eligible English explanation in a fresh context and all
required reference sections. Report unique instruction words, formal-artifact
reading separately, methodology and optional token counts with their tokenizer.
Every representative action must avoid loading the full instruction collection.

## Destination layout

The root is ENGINEERING_HARNESS.md. All remaining paths below are relative to
docs/engineering/harness/. This table is the proposed content allocation.

| Destination | Contents / trigger |
| --- | --- |
| CONTINUE.md | Selected work or compaction; complete returned procedure/step index. |
| DEFINE_CHANGE.md | New request; outcome, limits and existing-artifact selection. |
| DRAFT_DEFINITIONS.md | Missing definitions, verification, release or operating contracts. |
| AMEND_DEFINITIONS.md | Changed meaning of an accepted definition; supported limitation. |
| RISKS_AND_DECISIONS.md | Risk/question creation and its small model. |
| DRAFT_WORK_ORDERS.md | Proposed definitions ready for bounded work orders. |
| AUTHORIZE_WORK.md | Package review and human authorization. |
| EXECUTE_WORK.md | Evaluator-selected start, implementation and completion. |
| VERIFY_OUTCOME.md | Evidence review, VREC preparation, human decision and rebase recovery. |
| DELIVER_RESULT.md | Delivery selection, external authority, action and readback. |
| RELEASE.md | Selected RLS preparation or decision. |
| PULL_REQUEST.md | Exact governed pull request preparation or check. |
| RECORD_STATE.md | Separate selected definition or WO state change. |
| RESULTS.md | Lifecycle reporting, refusal and uncertain-operation recovery. |
| AUTHORITY.md | Actor identities, decision rights, delegation and execution grants. |
| ARTIFACTS.md | Artifact introduction, types and locations. |
| DEFINITION_LINKS.md | Definition links, coverage and architecture applicability. |
| WORK_AND_EVIDENCE.md | WO, verification, release and operating coverage. |
| COMMUNICATION.md | Eligible communication and protected content. |
| EXCEPTIONS.md | Exception availability and governed fallback. |
| SETUP.md | Missing or mismatched evaluator. |
| UPGRADE.md | Explicitly requested/authorized upgrade. |
| SKILL_PROVIDER.md | Requested provider selection or discovery repair. |
| migration/REFERENCE_MAP.md | Maintaining or reviewing rule migration. |
| migration/IMPLEMENTATION_PLAN.md | Migration dependencies and deferred capabilities. |

This is 26 files including the root, not 26 required startup reads.
The existing ARTIFACT_AUTHORING.md and machine contracts are not new files.

## Failure behavior and example

A missing guide or unknown returned procedure stops the affected governed
action and reports the discovery gap. Unrelated work stays separate.
For example, resuming implementation selects CONTINUE.md, obtains a fresh
result for the exact WO, then reads the returned EXECUTE_WORK.md step and its
required formal inputs. It does not load release preparation or guess a start
transition from the WO's remembered status.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-IAR-022 | IAR-DIS-001, IAR-DIS-002, IAR-DIS-014 |
| REQ-IAR-023 | IAR-DIS-002, IAR-DIS-003, IAR-DIS-013 |
| REQ-IAR-024 | IAR-DIS-004, IAR-DIS-005, IAR-DIS-009 |
| REQ-IAR-025 | IAR-DIS-006, IAR-DIS-007, IAR-DIS-010 |
| REQ-IAR-026 | IAR-DIS-008, IAR-DIS-009 |
| REQ-IAR-027 | IAR-DIS-010, IAR-DIS-011, IAR-DIS-012, IAR-DIS-013, IAR-DIS-014 |

## Not decided here

- Release number and separately authorized self-adoption.
- Host event APIs and the smallest compatible delivery implementation.
- A new lifecycle, generic revision system or repository exception engine.
