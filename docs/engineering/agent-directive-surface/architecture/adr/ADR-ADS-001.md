+++
id = "ADR-ADS-001"
type = "adr"
title = "Carry failure renderings and next-step resolution in the workflow contract"
status = "approved"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
decides = ["ARCH-ADS-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T10:36:12Z"
decided_by = "technical-owner"
+++

# ADR: Carry failure renderings and next-step resolution in the workflow contract

## Status

Proposed.

## Context

A blocked checkpoint must tell the agent what to do next. Today the renderer
re-emits the evaluated command. The correction could live in prose (the
router's failure procedure), in skills (each skill's stop conditions), in the
renderer's code, or in the machine contract that already owns steps, effects,
and non-effects.

## Decision drivers

- `HRN-004`: only `harnessctl` computes the canonical next action.
- `WFL-001`/`WFL-003`: the contract is authoritative and ordered; prose must
  not redefine it.
- One owner per subject; no restatement across skills.
- Conformance-testable: a self-loop must be detectable mechanically.
- Portability across hosts and providers.

## Considered options

### Option A: corrective forms in `WORKFLOW.json`, rendered by the evaluator

Each predicate declares its corrective argument array or escalation. The
renderer selects and renders; a conformance test forbids a corrective equal to
the evaluated command. One owner, mechanically checkable, host-neutral. Costs
a contract schema addition and a loader check.

### Option B: corrective guidance in router prose

Cheap to write; unverifiable; the agent must map a predicate ID to a paragraph;
two sources of next action, which `HRN-004` forbids.

### Option C: corrective guidance in each skill

Reaches only agents using that skill; duplicates across five skills; skills are
non-authoritative by the agentic-execution architecture.

### Option D: hard-coded in the renderer

Mechanically checkable but invisible to the installed contract; `WORKFLOW.md`
could not index it and the byte-identity rule between installed and packaged
contract would not cover it.

## Decision

Select Option A. Extend the `WORKFLOW.json` step schema with `corrective` per
predicate. Make `focus` and `check` share one resolver so the same contract
row yields the same step. Keep prose as an index of the contract, never a
second source.

## Consequences

- The contract schema changes additively; installed contracts regenerate on
  the next governor upgrade.
- Conformance tests gain a self-loop check and a focus/check equality check.
- Skills and router prose lose nothing; they already defer to the tool.
- A corrective form is a suggestion carried by the contract; it grants no
  authority.
