+++
id = "REQ-ECP-022"
type = "requirement"
title = "One read-only evaluator command projects and checks a selected artifact"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-29"
updated = "2026-08-29"
statement = "WHEN an actor asks the evaluator what applies to one selected artifact, THE SYSTEM SHALL answer through `harnessctl check`: without a checkpoint it projects the selected rule, procedure and next step; with a checkpoint it also evaluates the gates, so one command serves both questions."
verification_method = ["test"]
priority = "must"
source = "owner challenge of 2026-08-29 on the relation between focus and check; complexity audit 2026-08 P0-6 (one rule selector)"

[relations]
derives_from = ["CAP-ECP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T11:06:57Z"
decided_by = "requirements-steward"
reason = "Approved on 2026-08-29 by the accountable owner, 'Approve and start WO-ECP-015', for folding focus into check: check without a checkpoint becomes the projection focus returns today, focus remains one release as a byte-identical alias with a deprecation notice, the five procedure steps and WFL-003 name check, the harness-orient skill and the documentation follow; ADR-ECP-007 Option B, with the SPEC-ECP-001 amendment record and the ARCH-ECP-001 amendment that follows this approval. Measured before this transition over branch state e4a3c1b carrying unmoved main 5e5e9d6: validate PASS at 0 errors under the governing 0.10.0 root; start preflight reads the draft signature plus the architecture pincer W018 and W021 that the ADR approval and the ARCH-ECP-001 amendment resolve. Approval of a definition authorizes no work; the work order is approved separately."
+++

# Requirement: One read-only evaluator command projects and checks a selected artifact

## Rationale

`harnessctl focus` and `harnessctl check` share everything but the gates:
both load the validated contracts, project the selected artifact's
governing chain and dependencies, select the first matching rule, resolve
its procedure and render the same schema-2 restitution, and a test pins
that they resolve the same next step for one state. `focus` evaluates no
predicate and takes no checkpoint; `check` is a strict superset. Since
0.9.0 a third read-only projection, `next`, adds the reading manifest and
the next command. Three commands for one rule selection are three surfaces
to document, three names in the procedures (`STEP-WO-START-FOCUS`,
`STEP-FOCUS-SELECTED`, `STEP-FOCUS-RELATED`, `STEP-REMEDIATE-FOCUS`), and a
contract rule (`WFL-003`) that names `focus` as the selector while the
managed gate and the transition engine run `check`. The owner's question of
2026-08-29 — how related are they, and are both necessary — has the
measured answer that `focus` is `check` asked with no checkpoint.

## Behavior

- Trigger: `harnessctl check REPOSITORY --artifact ID` runs with no
  `--checkpoint`.
- Response: the result is the projection `focus` returns today — the
  selected rule, its procedure and current step, the decision required, the
  command or response, the alternatives, the background count — with no
  gate evaluated and nothing written; `--include-background` expands the
  background categories as it does for `focus`.
- With `--checkpoint`, the command behaves exactly as today.
- Compatibility: `harnessctl focus` remains for one release as an alias
  that emits the same bytes it emits today and a deprecation notice on
  standard error; the procedures, `WFL-003`, the shipped skill and the
  documentation name `check`.
- On failure: an unknown artifact or a type `check` does not accept is
  refused as `check` refuses it today (`WEX210`); the alias refuses exactly
  what `focus` refuses today.

## Assumptions and dependencies

- `harnessctl next` is unchanged: it is the agent's first call and carries
  the execution context; `check` is the evaluator.
- `ECP-NXT-004`'s byte-identity between `next`, `focus` and
  checkpoint-less `check` continues to hold, with `check` as the reference.
- The alias is removed by a later work order after one release has shipped
  with the deprecation notice.

## Acceptance examples

### Example: normal behavior

**Given** an `in_progress` work order.

**When** `harnessctl check . --artifact WO-X` runs without a checkpoint.

**Then** the result projects `WFL-WO-IMPLEMENT`, `PROC-WO-IMPLEMENT`, the
`STEP-WO-IMPLEMENT-CHECK` command, no gate, `mutation.writes` empty, and
its restitution equals what `harnessctl focus . --artifact WO-X` returns.

### Example: failure behavior

**Given** a requirement `REQ-X`.

**When** `harnessctl check . --artifact REQ-X` runs.

**Then** the command is refused with `WEX210: check accepts only WO, VREC,
or RLS artifacts`, as today.

## Open decisions

None.
