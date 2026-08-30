# Phase 2 Agentic Execution Consistency-Correction Proposal

> Historical record from 2026-08-24, at `65244b1`. Kept for the decision trail; it describes the tool as it was then.

<!-- Target expertise: 8/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

- Prepared: 2026-08-24
- Selected artifacts: `ADR-AEX-003` and `WO-AEX-002`
- Correction class: non-semantic, body-only lifecycle consistency
- Current formal state: both artifacts are `approved`
- Proposed lifecycle effect: none
- Current formal-artifact effect: none
- Implementation effect: none

## Purpose and authority boundary

This non-authoritative proposal defines exact wording corrections for
draft-time explanatory prose that became stale when the selected artifacts
were approved. It does not edit a formal artifact, change lifecycle state,
exercise an approval right, start `WO-AEX-002`, or authorize an external
action.

The front-matter `status` and lifecycle events are authoritative and valid.
This proposal concerns only body prose that now disagrees with those fields.

## Observed inconsistency

| Artifact | Current approved-file SHA-256 | Stale body prose |
| --- | --- | --- |
| `ADR-AEX-003` | `29e95f724316b72ce7edd109fa6aef2df6e6fb36016500cdc5364b38a601b987` | The `Status` section says “Proposed” and says the lifecycle remains `draft`. |
| `WO-AEX-002` | `f1976750ca26f584ac445afbdb7044362b439cfcbd59d2f12db092f4007241bc` | The readiness and change-surface sections call the approved work order a proposal or draft, say its governing definition artifacts remain draft, and describe commit-bound verification as merely proposed. |

The work order's later instruction to stop while an artifact is `draft` and to
apply additional stops after approval is conditional lifecycle guidance, so it
is still correct and is excluded from this proposal.

## Governance classification

The managed contract requires an explicit applied transition for a lifecycle
state change. It does not define an “amend” transition for a body-only wording
correction that preserves state. Therefore the recommended path is an exact,
separately authorized content patch under the accountable owners of the two
artifacts, followed by graph and integrity validation.

The correction must not be presented as a new approval, implementation work,
or a lifecycle event. The existing approval events continue to record the
formal decisions; the correction record and repository history retain the
reason for the body-only change.

If the repository owner interprets local policy as forbidding any direct body
edit to an approved formal artifact, stop and select the replacement-artifact
alternative below instead.

## Frozen surface

The following content must remain byte-for-byte unchanged:

- all front matter, including `status`, `updated`, owners, relations,
  assurance, execution scope, and lifecycle events;
- every normative technical and architecture statement;
- all work-order objectives, constraints, paths, verification obligations,
  evidence requirements, stop conditions, and completion reporting;
- `SPEC-AEX-003` and every other formal artifact; and
- executable source, tests, managed files, Git state, and external systems.

Only the exact body replacements below are proposed.

## Exact proposed replacements

### `ADR-AEX-003` — `Status` paragraph

Replace:

```text
Proposed. The formal artifact lifecycle remains `draft`.
```

With:

```text
Option C was accepted during accountable technical-owner review. The
authoritative lifecycle state is recorded in the front-matter `status` and
lifecycle events.
```

This mirrors the state-neutral pattern already used by `ADR-AEX-001` and
`ADR-AEX-002`. It does not change Option C or its consequences.

### `WO-AEX-002` — `Lifecycle and readiness`

Replace the three draft-time paragraphs beginning with “This work order is a
Phase 2 proposal” and ending with “does not itself approve the work order”
with:

```text
The repository owner confirmed commit-bound verification as `required` during
accountable content review. Formal implementation authority is determined by
the front-matter lifecycle state, not by the review record alone. Approval does
not start implementation; implementation starts only after the required focus
and start preflight have been read and the engineering owner gives an explicit
start decision.

`SPEC-AEX-003` and `ADR-AEX-003` formalize and govern the Phase 2 decisions
identified in
`docs/notes/agentic-execution-phase-2-contract-closure.md`. Their authoritative
lifecycle states are recorded in their front matter and lifecycle events. If a
future accountable decision changes the applicable relations, executable
surface, repository-state binding, or authoritative envelope derivation and
persistence boundary, revise or replace the applicable formal artifacts before
implementation continues.

Commit-bound verification is `required` because later skills and mutation
controls will rely on this executable contract layer. The classification does
not start implementation or establish an assurance result.
```

This keeps the start decision separate, preserves the existing assurance
classification, and remains accurate after later lifecycle changes.

### `WO-AEX-002` — `Expected change surface`, first sentence

Replace:

```text
The exact proposed paths are declared in `[execution_scope]`.
```

With:

```text
The exact authorized paths are declared in `[execution_scope]`.
```

No path is added, removed, or reinterpreted.

### `WO-AEX-002` — `Expected change surface`, closing paragraph

Replace:

```text
The proposal and this draft are governance inputs, not implementation changes.
If inspection shows another executable or packaging path is necessary, revise
this work order and obtain accountable approval before touching it.
```

With:

```text
Approval of this work order is bounded implementation authority, not an
implementation change or start decision. If inspection shows another
executable or packaging path is necessary, revise or replace the applicable
formal artifacts and obtain accountable approval before touching that path.
```

The replacement preserves the existing stop on undeclared paths.

## Semantic non-effects

The proposed correction does not change:

- the selection of Option C;
- the pure-contract/evaluator-orchestration boundary;
- any public schema, diagnostic, repository-state algorithm, authority rule,
  or compatibility decision;
- the 13-entry `WO-AEX-002` execution scope;
- commit-bound verification being `required`;
- any implementation or verification obligation; or
- lifecycle state, work-order start authority, Git state, or external state.

## Verification required after separate authorization

Before editing, recheck the two current file digests against this proposal.
After applying only the exact replacements:

1. prove all front matter is byte-for-byte unchanged;
2. prove the diff contains only the four proposed body replacements;
3. recompute and record the two resulting file digests;
4. run evaluator 0.6.0 graph validation and managed-integrity `doctor`;
5. confirm both artifacts remain `approved` with exactly one existing
   `draft` to `approved` lifecycle event;
6. run `git diff --check`; and
7. stop without focus, preflight, implementation, Git action, network use, or
   external action.

## Options

### Option A — exact body-only correction, state preserved

Recommended. Apply only the four replacements above under explicit technical-,
engineering-, repository-, and quality-owner assertions. This removes the
contradiction without changing formal semantics or inventing a lifecycle event.

### Option B — retain the text as historical draft-time context

Make no formal edit and explicitly document that front matter always controls.
This has the smallest mutation surface but leaves misleading prose in the two
documents most likely to be read before implementation.

### Option C — create replacement formal artifacts

Create, review, and approve successor definitions rather than edit approved
bodies. This gives the strongest immutable-history interpretation but is
disproportionate for non-semantic lifecycle wording and would require new IDs,
relations, work-order traceability, and lifecycle decisions.

## Current human decision point

Choose whether to authorize Option A, retain the wording under Option B, or
require the replacement-artifact route in Option C. No implementation start is
part of this decision.

Recommended response:

```text
As technical owner, authorize exactly the proposed body-only correction to
ADR-AEX-003. As engineering owner, authorize exactly the three proposed
body-only corrections to WO-AEX-002. As repository owner, confirm that all
front matter, lifecycle state, relations, assurance, and execution scope must
remain unchanged. As quality owner, accept the corrections as non-semantic.
Apply only those four replacements, validate them, and stop. Do not start
implementation or perform any Git, network, or external action.
```

Alternatives:

- accept Option B and retain the current formal files unchanged; or
- select Option C and prepare replacement-artifact planning only.
