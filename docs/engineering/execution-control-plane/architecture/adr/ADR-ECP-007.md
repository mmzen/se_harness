+++
id = "ADR-ECP-007"
type = "adr"
title = "One read-only evaluator command: fold focus into check"
status = "approved"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
decides = ["ARCH-ECP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T11:06:57Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-29 by the accountable owner, 'Approve and start WO-ECP-015', for folding focus into check: check without a checkpoint becomes the projection focus returns today, focus remains one release as a byte-identical alias with a deprecation notice, the five procedure steps and WFL-003 name check, the harness-orient skill and the documentation follow; ADR-ECP-007 Option B, with the SPEC-ECP-001 amendment record and the ARCH-ECP-001 amendment that follows this approval. Measured before this transition over branch state e4a3c1b carrying unmoved main 5e5e9d6: validate PASS at 0 errors under the governing 0.10.0 root; start preflight reads the draft signature plus the architecture pincer W018 and W021 that the ADR approval and the ARCH-ECP-001 amendment resolve. Approval of a definition authorizes no work; the work order is approved separately."
+++

# ADR: One read-only evaluator command: fold focus into check

## Status

Proposed.

## Context

`focus` (0.5.0) projects the selected rule; `check` (0.7.x) evaluates that
rule's gates at a checkpoint; `next` (0.9.0, `WO-ECP-001`) projects the
rule plus the execution context. All three select the rule the same way,
and `check` is a strict superset of `focus`. `WFL-003` names `focus` as the
selector, five procedure steps invoke it, the shipped `harness-orient`
skill calls it, and the CI gate and the transition engine call `check`. The
owner asked on 2026-08-29 whether both are necessary.

## Decision drivers

- `ADR-AEX-008` / complexity audit P0-6: one rule selector, one result
  schema, one precondition engine.
- The command an actor runs to ask "what applies" and the command CI runs
  to enforce it should be the same command, so their answers cannot drift.
- Consumers' scripts and retained results must not break at the upgrade.
- `next` has a distinct purpose (the agent's first call, with context) and
  stays.

## Considered options

### Option A: keep both, document the relation

Cost nothing now; keep three names for one selection; `WFL-003` keeps
naming a command CI never runs. Consequence: the drift the owner noticed
stays possible.

### Option B: fold `focus` into `check` as the checkpoint-less default

`check --artifact ID` projects; `--checkpoint` evaluates. Procedures,
`WFL-003`, the skill and the docs name `check`; `focus` stays one release
as a byte-identical alias with a notice. Consequence: one command, one
name in every contract, no consumer break at the upgrade; a later removal
work order.

### Option C: fold `check` into `focus`

Keep the older name and give it the checkpoints. Consequence: the name
follows the projection rather than the evaluation; every CI workflow, the
transition engine's messages and the 0.9.0/0.10.0 documentation would
rename, for no gain over B.

## Decision

Option B (`SPEC-ECP-011`, `ECP-ONE-001` to `ECP-ONE-008`). `WO-ECP-015`
writes the amendment record on `SPEC-ECP-001` (`ECP-NXT-004`).

## Consequences

- Positive: one selector command; `WFL-003` names what CI runs; the check
  reference describes the whole read-only surface in one place.
- Negative: two names in the CLI help for one release.
- Operational: consumers see `update` on `WORKFLOW.json`, `WORKFLOW.md` and
  the skill at their next `upgrade`; scripts calling `focus` keep working.
- Security: no new authority; the projection writes nothing, as today.

## Validation

`VER-ECP-011`.
