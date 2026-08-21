+++
id = "SPEC-WEX-001"
type = "specification"
title = "Deterministic scoped workflow operation contract"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
specifies = ["REQ-WEX-001", "REQ-WEX-002", "REQ-WEX-003", "REQ-WEX-004", "REQ-WEX-005"]
+++

# Specification: Deterministic scoped workflow operation contract

## Scope

Define one provider-neutral contract for projecting a selected governance scope, planning and atomically applying formal lifecycle transitions, preparing VREC and RLS proposals, and returning a canonical handoff. The contract is implemented by `harnessctl`; agent instructions and Skills may discover or render it but do not calculate lifecycle legality.

This specification adds scoped and transition-aware interfaces. It preserves repository-wide `harnessctl inspect` as a maintenance view and preserves the conversational fields of `REQ-IAR-019` and `SPEC-IAR-011`. The earlier statement that the IAR packet made no CLI or JSON change describes that packet's implementation boundary; it is not a permanent prohibition on the separately governed WEX interface.

The contract covers formal artifact mutations and the lifecycle effects of `capture-verification` and `prepare-release`. It does not authorize a decision, run an external action, infer accountable identity, or automatically migrate historical artifacts.

## Actors and external systems

- An operator selects scope, requests a plan, and may apply an already-authorized mechanical transition.
- Product, technical, requirements, engineering, assurance, release, and service owners make the decisions reserved to their roles.
- Coding agents and optional Skills invoke the same CLI and render its canonical result.
- Git supplies candidate object identity for provenance records; it supplies no approval authority.
- The filesystem contains untrusted repository content and must retain no partial write after failure.

## Inputs

### Scoped projection

`harnessctl focus [TARGET] --artifact ID [--json] [--include-background]`

- `ID` is exactly one `WO-*`, `VREC-*`, or `RLS-*` identity.
- `--json` selects the canonical structured form; otherwise the human form is rendered from the same result.
- `--include-background` expands unrelated findings after the selected-scope result. It does not turn them into selected-scope actions.

### Lifecycle transition

`harnessctl transition [TARGET] --set ID=STATUS [--set ID=STATUS ...] --decision ID=ACTOR [--decision ID=ACTOR ...] [--reason ID=TEXT ...] [--apply] [--json]`

- Each `--set` selects one artifact and one target state. Duplicate IDs, conflicting targets, missing decisions, and decisions for unselected IDs are invalid.
- Each selected ID has exactly one explicit accountable actor assertion. The tool records the assertion but cannot prove the caller holds that role.
- Without `--apply`, the command is read-only and returns the complete proposed transaction and handoff. With `--apply`, it applies exactly that validated transaction.
- Multi-artifact selection is supported so a mutually dependent definition packet can be activated or completed as one graph-valid transaction. Every selected mutation remains explicit.

### Preparation

- `capture-verification` and `prepare-release` retain their public command shapes but use the same scope, precondition, mutation, and handoff engine.
- Artifact content, actor text, reason text, evidence paths, and relation metadata are untrusted inputs.

## Outputs

Every focus, transition, or preparation operation produces one semantic `WorkflowResult`. Human output uses the managed lifecycle handoff headings. JSON uses this versioned shape:

```json
{
  "schema": 1,
  "operation": {"kind": "focus|transition|capture-verification|prepare-release", "outcome": "planned|completed|failed"},
  "selection": {"primary": "ID|null", "artifacts": ["ID"]},
  "scope": {"governing": ["ID"], "dependencies": ["ID"]},
  "state": {"before": [{"id": "ID", "status": "STATUS"}], "after": [{"id": "ID", "status": "STATUS"}]},
  "findings": {"scoped_blockers": [], "repository_blockers": [], "background_summary": []},
  "mutation": {"writes": [{"id": "ID", "fields": ["FIELD"]}]},
  "handoff": {
    "completed": [],
    "current_lifecycle_state": [],
    "recommended_next_step": {},
    "human_decision_or_approval_required": {},
    "command_or_suggested_response": {},
    "alternative_next_steps": []
  }
}
```

Arrays and findings use stable ordering by declared workflow priority, artifact ID, path, field, and finding code as applicable. JSON keys are emitted in the documented order, strings are escaped as data, timestamps use UTC RFC 3339 seconds, and identical semantic inputs produce byte-identical JSON except for an execution timestamp that is present only in an applied mutation and becomes retained artifact data.

The human form may wrap text for the terminal but preserves the same field values, primary recommendation, authority, and alternatives. It contains no additional lifecycle conclusion absent from JSON.

## State model

### Operation states

1. `focus` is always read-only.
2. A transition without `--apply` ends as `planned` or `failed` and writes nothing.
3. A transition with `--apply` rechecks the repository immediately before writing, then ends as `completed` or `failed`.
4. Preparation creates one new `ready` record only after every precondition passes.

### Supported lifecycle transitions for new mutations

| Artifact family | Allowed explicit transition | Preconditions beyond graph validity |
| --- | --- | --- |
| INT, CAP, REQ, SPEC, ARCH, ADR, VER, REL, OPS | `draft -> approved`; `draft -> rejected`; `approved -> implemented`; `approved -> rejected` | actor is supplied for every selected artifact; the complete proposed graph satisfies active coverage and decision-applicability rules |
| WO | `draft -> approved`; `draft -> rejected`; `approved -> in_progress`; `approved -> rejected`; `in_progress -> implemented`; `in_progress -> rejected` | complete governing chain and assurance classification for approval; start preflight eligibility for in-progress; retained evidence declaration and review eligibility for implemented |
| WO under configured provenance | `implemented -> verified`; `implemented|verified -> released` | a separate explicit transition is requested and direct eligible VREC or RLS coverage proves the target projection |
| VREC | `ready -> verified`; `ready -> rejected`; `ready -> superseded` | assurance actor and decision data for verified/rejected; existing supersession contract for superseded |
| RLS | `ready -> released`; `ready -> rejected` | release actor and decision data; exact eligible verification and work coverage remain unchanged |

`implemented`, `verified`, `released`, `superseded`, and `rejected` are terminal for their artifact family unless the table expressly lists them as a source. Revisions to a terminal definition require a new or formally superseding artifact rather than reopening history. Historical statuses remain readable under compatibility rules, but new operations do not create a `released` VREC or implicitly synchronize related records.

## Behavioral rules

1. Resolve every selected ID through formal metadata, not its filename, conversational mention, branch, or commit message.
2. Build a WO scope from the WO, implemented requirements, selected specifications, applicable architecture and ADRs, selected verification contracts, upstream capabilities and intents, and direct VREC/RLS coverage needed to assess current state.
3. Build a VREC scope from the VREC, its WOs, conforming verification contracts, each WO governing chain, and direct including RLS records.
4. Build an RLS scope from the RLS, satisfied release contract, included VRECs, released WOs, and the governing chains needed to assess eligibility.
5. Mark a finding as a repository blocker only when managed integrity, identity uniqueness, parser safety, or another condition makes every selected-scope result unreliable. Mark a finding as scoped when its artifact or relation is in the working set. Summarize all other findings as background.
6. Never select a substitute when the requested ID is absent, duplicated, malformed, or of the wrong type.
7. Calculate the full in-memory mutation before a write. The plan lists exact files, formal IDs, before/after states, and fields to add, change, or remove.
8. Validate the complete proposed final graph, including every item in a multi-artifact packet, before applying any mutation. This permits mutually dependent REQ/SPEC/VER activation without a transient invalid graph.
9. Re-read and compare every planned input immediately before apply. Concurrent change invalidates the plan and writes nothing.
10. Write through same-filesystem temporary files and atomic replacement with rollback of all already-replaced files if a later replacement fails. An unsuccessful transaction retains every pre-operation byte.
11. A VREC preparation accepts only WOs in `implemented` state, requires the exact declared verification union and evidence coverage, and creates only the selected VREC.
12. Release preparation accepts only `verified` VRECs, requires exact work-set equality, release-contract coverage, and commit identity equality, and creates only the selected RLS.
13. A VREC transition changes only the selected VREC. An RLS transition changes only the selected RLS. Related WOs, VRECs, and RLSs require separate explicit `--set` entries and must independently satisfy their transition rules.
14. Assurance and release projections are calculated from eligible VREC and RLS relations. A related record's status is never synchronized merely to make the projection visible.
15. Ready VRECs and RLSs record `prepared_at` and `prepared_by`. A ready VREC omits `verified_at` and `verified_by`; a ready RLS omits `released_at` and `authorized_by`.
16. Applying VREC verification adds `verified_at` and `verified_by`. Applying RLS release adds `released_at` and `authorized_by`. Rejection adds `rejected_at`, `rejected_by`, and non-empty `rejection_reason`. Supersession retains its existing specific fields and relation.
17. Every transition appends one structured `[[lifecycle_events]]` entry containing `from`, `to`, `decided_at`, `decided_by`, and optional `reason`. Type-specific decision fields must agree with the corresponding event. Preparation provenance is not a decision event.
18. Unchanged legacy records without preparation fields or lifecycle events remain readable and are not rewritten. Any new transition of a compatible legacy record adds the new event and required target-state metadata without changing immutable captured facts.
19. Recommended next actions come from one closed, versioned mapping keyed by operation outcome, final lifecycle state, blockers, and currently satisfied prerequisites.
20. Emit exactly one primary recommendation. Alternatives are emitted only for states whose mapping declares several legal paths and remain subordinate to the primary action.
21. A recommended command includes only known validated arguments and is not executed. When a human decision is next, emit a suggested response rather than an invented approval command.
22. Skills and agent entry files may instruct an agent to call these commands and render `WorkflowResult`; they may not redefine scope rules, transition rules, decision metadata, or next-step selection.

## Error and recovery behavior

- Parse, identity, graph, precondition, authority-input, concurrency, and filesystem failures use stable WEX finding codes and identify the failed artifact or input without exposing sensitive content.
- A failed focus or validation operation performs no mutation and recommends one bounded remediation or escalation step.
- A failed transition plan reports the unchanged current state and no writes.
- A failed apply restores the pre-operation bytes, reports whether rollback succeeded, and escalates if the filesystem cannot prove restoration.
- A stale plan is never silently recalculated and applied; the operator must inspect the new plan.
- Background findings do not change the command exit result unless they are classified as repository blockers by the fixed registry.

## Data and interface contracts

- `WorkflowResult.schema = 1` is the shared semantic contract for human and JSON output.
- Canonical IDs, paths relative to repository root, status names, relation names, and finding codes are emitted as data.
- New VREC preparation fields are `prepared_at` and `prepared_by`; verification decision fields are `verified_at` and `verified_by`.
- New RLS preparation fields are `prepared_at` and `prepared_by`; release decision fields remain `released_at` and `authorized_by`.
- Rejection fields are `rejected_at`, `rejected_by`, and `rejection_reason`.
- `[[lifecycle_events]]` is append-only and ordered chronologically; each event contains `from`, `to`, `decided_at`, `decided_by`, and optional `reason`.
- The validator checks event/state consistency and protects preparation, candidate, evidence, work coverage, commit identity, snapshot, decision, supersession, and release facts according to artifact type and phase.
- `inspect` retains its existing repository-wide schema and non-executable suggestion catalog. `focus` owns the new selected-scope handoff.

## Security and privacy properties

- Normalize and constrain all target and temporary paths to the selected repository; reject traversal, links that escape the repository, aliases, and ambiguous case collisions before writes.
- Treat Git revisions, formal metadata, lifecycle reasons, owners, evidence paths, and repository text as untrusted. Never evaluate them as shell, Python, TOML fragments, format strings, or commands.
- Do not infer authority from actor text. Preserve the assertion for audit and state clearly that the command does not grant the claimed role.
- Do not include secrets or arbitrary evidence bodies in normal focus or handoff output.
- Escape control characters in human output and encode all JSON strings through the standard library encoder.
- Preserve existing managed-integrity, released-evaluator, and candidate-source boundaries.

## Performance and capacity

- Build the artifact index once per operation and project scope through indexed typed relations.
- For 1,000 formal artifacts, scoped focus and transition planning should complete within the same order of magnitude as snapshot validation on the same runtime and filesystem.
- Memory use is bounded by repository formal metadata and planned file content; no network service or new runtime dependency is introduced.

## Observability

- Human and JSON output expose operation kind/outcome, selection, scope membership, blocker class, before/after state, exact mutation plan, authority boundary, and next step.
- Stable finding codes distinguish scope, transition, metadata, diff, concurrency, and rollback failures.
- Tests compare pre/post file digests for every failure path and retain the canonical JSON result.
- Work-order evidence retains evaluator identity, applicable candidate identity, command, findings, and exit status.

## Compatibility and migration

- Existing `validate`, `inspect`, `capture-verification`, and `prepare-release` invocations remain accepted; stricter preparation preconditions can newly reject states that contradicted the normal managed workflow.
- Existing repository-wide inspection remains unchanged. Consumers adopt `focus` explicitly.
- Historical records remain readable without synthetic preparation fields or lifecycle events. Installation and upgrade never rewrite repository-owned artifacts.
- New templates omit decision fields in ready records and include preparation fields. Candidate source and standard repository templates change together through governed implementation.
- Human handoff semantics remain compatible with `REQ-IAR-019`; the machine-readable WEX result is additive and does not turn Inspector suggestions into executable commands.
- One standard installation, Python 3.11+ standard-library runtime, and no-network local operation are preserved.

## Examples and counterexamples

- **Conforming focus:** selecting `WO-WEX-001` returns only its governing chain and direct lifecycle coverage as current scope; 44 unrelated legacy maintenance warnings appear as a background count and are not recommended actions.
- **Conforming packet plan:** a transition plan explicitly selects `INT-WEX-001`, `CAP-WEX-001`, `REQ-WEX-001` through `REQ-WEX-005`, `SPEC-WEX-001`, and `VER-WEX-001` for approval, validates their proposed graph together, and writes nothing without `--apply`.
- **Conforming VREC decision:** verifying `VREC-WEX-001` adds its assurance decision event and fields but leaves every referenced WO at `implemented`.
- **Conforming failure:** capturing a VREC for an `approved` WO reports the required `implemented` state, produces an unchanged-state handoff, and leaves no new file.
- **Nonconforming:** approving each mutually dependent REQ, SPEC, and VER sequentially while leaving the graph invalid between writes.
- **Nonconforming:** preparing an RLS from a ready VREC.
- **Nonconforming:** setting `verified_at` during VREC preparation or `released_at` during RLS preparation.
- **Nonconforming:** changing a WO when its VREC is verified, or changing a VREC when its RLS is released.
- **Nonconforming:** recommending work on an unrelated domain because global inspection found a maintenance warning there.

## Explicitly unspecified decisions

- Internal Python module names, class names, helper decomposition, and cache representation.
- Exact terminal colors, line wrapping, and optional explanatory prose outside canonical handoff values.
- The filesystem locking primitive, provided stale-plan detection and no-partial-write guarantees hold on supported platforms.
- Test fixture organization and whether canonical JSON golden data is stored inline or in fixture files.

The public command shapes, scope classification, transition table, atomic packet behavior, metadata semantics, and `WorkflowResult` fields are not delegated implementation choices. Before approval, technical review must assess the state-machine, public CLI/schema, artifact-metadata, and atomic-write changes for architecture and ADR applicability.
