+++
id = "SPEC-IAR-001"
type = "specification"
title = "Instruction routing, preflight, and migration behavior"
status = "implemented"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-21"

[relations]
specifies = ["REQ-IAR-001", "REQ-IAR-002", "REQ-IAR-003", "REQ-IAR-004", "REQ-IAR-005", "REQ-IAR-006", "REQ-IAR-007", "REQ-IAR-008", "REQ-IAR-009"]
+++

# Specification: Instruction routing, preflight, and migration behavior

## Canonical file model

The standard installation remains one profile. Template suffix determines initial ownership, and the lock records the effective mode:

| Installed path | Template mode | Effective ownership |
| --- | --- | --- |
| `AGENTS.md` | fragment | owner file with managed harness block |
| `CLAUDE.md` | fragment | owner file with managed adapter block |
| `ENGINEERING_HARNESS.md` | managed | harness contract and router |
| `docs/engineering/README.md` | seed | repository/domain index owner after installation |
| four shared policy modules | managed | harness distribution |

The managed `AGENTS.md` block is short and stable. It directs the actor only to `ENGINEERING_HARNESS.md`, states that owner content may add but not waive constraints, and repeats only the stop condition necessary before that router is read. The Claude adapter contains only `@AGENTS.md` inside its managed block.

## Managed router

`ENGINEERING_HARNESS.md` owns the following route without duplicating the bodies of its destinations:

1. Always distinguish repository-owned facts, including those in the owner-controlled region of `AGENTS.md`, from formal artifact authority.
2. Before implementation, run preflight for one selected work order and read every returned file.
3. Consult `WORKFLOW.md` for lifecycle sequence and automation boundaries.
4. Consult `DECISION_RIGHTS.md` before approval, transition, release, or other accountable decisions.
5. Consult `QUALITY_GATES.md` when defining or executing verification.
6. Consult `TRACEABILITY.md` when creating, relating, capturing, superseding, or releasing artifacts.
7. Use the owner-maintained engineering README only to find repository-specific domains and local documentation.

A policy module must be linked directly by the managed router. It may not rely on the owner-editable README as its only inbound instruction path.

## Repository-context readiness

The seed uses named placeholder fields rather than a free-form scan. Preflight knows the exact seed schema and reports unresolved required values by field name. Once the owner changes the file, content is not digest-managed. Later schema evolution may add missing fields through a conflict-free proposal, but must not overwrite owner text.

Context completeness is an implementation-readiness condition, not artifact authority. Preflight must not parse context prose into requirements or approvals.

## Preflight interface

The command is:

```text
harnessctl preflight TARGET --work-order WO-ID [--phase start|review] [--json]
```

It resolves `TARGET`, loads configuration and lock data, and returns all independently detectable diagnostics in stable code/path order. It performs these checks:

1. Python/runtime and required-file checks currently owned by `doctor`.
2. Managed and fragment integrity against the lock.
3. Required repository-context field completion.
4. Formal artifact parsing and graph validation.
5. Exact selected ID, `work_order` type, and phase-appropriate status. The default `start` phase accepts `approved` or `in_progress`. The `review` phase accepts those states plus `implemented`, `verified`, or `released`.
6. Complete typed traversal from the work order through specification, architecture and ADR, verification, requirements, capability, and intent.
7. Existence and uniqueness of every linked artifact path.

On success, text output presents the selected phase, an ordered reading manifest, and exact repository commands taken from context. JSON output uses a versioned schema containing `ready`, `phase`, `diagnostics`, `work_order`, `reading_manifest`, `repository_commands`, and `authority_boundary`. Neither mode writes files. Preflight does not execute owner-provided commands and never interpolates input into a shell.

## CI contract

The installed GitHub pull-request workflow obtains exactly one `WO-*` value from a structured pull-request template field. A small parser passes the value as a process argument, never as executable shell text. In a target repository, the required job uses a separately acquired exact harness release protected by package hashes or an immutable action digest, then runs integrity, `preflight --phase review`, validation, and dashboard generation. Candidate-checked-in scripts are additionally tested but cannot replace the independent check.

The harness repository uses a two-lane bootstrap. Its independent lane runs the last released distribution and enforces the previously released contract. Its candidate lane builds and tests unreleased behavior, installation output, and migration fixtures under `VER-IAR-001`. A new preflight rule cannot be called independent until the containing distribution is published and a separate governed change updates the external pin. Release evidence must identify which lane proved each claim and must not describe candidate self-tests as independent assurance.

For push events with no pull-request record, the workflow runs integrity, formal validation, and dashboard generation and labels the result repository-wide rather than work-order-bound. Provider integrations other than GitHub must supply an equivalent explicit work-order input; they are not implemented by this work order.

The installer emits documented host-configuration steps for a required check, protected default branch, and review ownership over workflow, lock, managed instruction, and formal-governance paths. Offline code cannot assert that those remote settings exist.

CI validates a declared work order structurally. It does not infer whether an arbitrary source diff is semantically inside that work order. A protected reviewer makes that scope judgment using the work order, diff, and retained evidence.

## Migration matrix

| Starting state | Planned result |
| --- | --- |
| New repository | Create the standard managed, fragment, and seed files and schema-2 lock entries. |
| Existing owner `AGENTS.md` or `CLAUDE.md`, no markers | Preserve content and append exactly one managed fragment. |
| Existing well-formed managed fragment | Upgrade only when lock comparison proves it unchanged or canonically equivalent. |
| Malformed or duplicate markers | Report conflict; write nothing. |
| Old README is exact/canonical managed content | Install the new seed content, record seed presence, and relinquish content ownership. |
| Old README is customized or ambiguous | Preserve it, report manual reconciliation, and do not silently change its lock mode. |
| Context seed already curated | Preserve content and presence tracking. |
| Self-hosting file absent from lock | Reconcile through a reviewed supported self-upgrade plan before claiming parity. |

Plan generation is deterministic. Apply is transactional within the existing installer contract: a conflict prevents writes, safe changes are idempotent, and customized content is never overwritten.

## Authority and failure behavior

Instructions and checks fail closed on structural ambiguity. They do not attempt natural-language policy adjudication. When repository-owner instructions appear to contradict managed constraints, the actor stops and requests an accountable decision; automation does not choose precedence by rewriting either source.

No command added by this specification commits, pushes, opens a pull request, changes artifact status, captures verification, creates a tag, releases, publishes, or deploys.
