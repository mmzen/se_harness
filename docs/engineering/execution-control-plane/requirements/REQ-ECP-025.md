+++
id = "REQ-ECP-025"
type = "requirement"
title = "The execution context is the projection, and no closed alias stays on the command list"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-29"
updated = "2026-08-29"
statement = "WHEN an actor asks for the selected artifact's execution context, THE SYSTEM SHALL return it as the checkpoint-less check projection with the single in_progress work order as the default artifact, keep next as a one-release alias that announces its removal, and carry no accept-candidate subcommand, so that one name serves one operation."
verification_method = ["test"]
priority = "must"
source = "harnessctl command audit of 2026-08-29 (P2 and P3); REQ-REB-022's one-cycle alias boundary"

[relations]
derives_from = ["CAP-ECP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T18:39:39Z"
decided_by = "requirements-steward"
reason = "Approved by the requirements steward on 2026-08-29 with the words 'Approve and start WO-ECP-019': the execution context is the checkpoint-less check projection with the single in_progress work order as the default artifact, next is a one-release alias announcing its removal, and accept-candidate leaves the command list; audit items P2 and P3 of 2026-08-29."
+++

# Requirement: The execution context is the projection, and no closed alias stays on the command list

## Rationale

`REQ-ECP-001` introduced `next` as the agent's first call: the checkpoint-less
projection plus a `context` object (reading manifest, governing chain,
declared scope, state, the next command) and a default artifact. `REQ-ECP-022`
then made `check` without a checkpoint the projection itself, and
`REQ-ECP-024` removed `focus`. What remains is two names for one read-only
operation, differing only by an additive object and a default: `next` is
`check` with more. The audit of 2026-08-29 ranked the fold P2: the command
list is where a newcomer meets the harness, and each name on it that is
another name's superset costs a paragraph of explanation and a row in every
table. The context is cheap to compute, writes nothing and is useful to every
caller of the projection, so the projection carries it.

`accept-candidate` is the other case. `REQ-REB-022` allowed the pre-namespace
entry point to remain "for one compatibility cycle only" as an alias of
`qualify candidate-package`; the alias shipped in 0.8.0 and is still in
0.11.0. The audit ranked its retirement P3. The candidate-evidence workflow's
legacy branch is not affected: it runs only when the released verifier has no
`qualify` namespace, and such a verifier is one that still carries the
bootstrap command itself (`SPEC-REB-012` rule 6).

## Behavior

- Trigger: the candidate after 0.11.0 is built.
- Response: `harnessctl check` without `--checkpoint` returns the projection
  with the `context` object `SPEC-ECP-001` defined for `next`; when
  `--artifact` is absent it selects the single `in_progress` work order and
  otherwise blocks with `WEX-ECP-001`. `harnessctl next` returns the same
  bytes and prints a deprecation notice on standard error naming `check`.
  `harnessctl accept-candidate` is not a subcommand. Every corrective that
  named `harnessctl next` names `harnessctl check`.
- On failure: `check` with a checkpoint still requires `--artifact`; the
  projection refuses what it refuses today.

## Assumptions and dependencies

- `ECP-ONE-001` to `ECP-ONE-003` hold on `main` (`VREC-ECP-018`); the
  `focus` alias is gone (`VREC-ECP-020`).
- `qualify candidate-package` is unchanged, and so is the candidate-evidence
  workflow.
- The alias `next` is removed by a later work order after one release has
  shipped with the notice, as `REQ-ECP-024` did for `focus`.

## Acceptance examples

### Example: normal behavior

**Given** a repository with exactly one `in_progress` work order.

**When** `harnessctl check . --json` runs.

**Then** the result is the projection of that work order with a `context`
object whose `next.argv` equals `restitution.command_or_response.argv`, and
`harnessctl next . --json` returns the identical bytes.

### Example: failure behavior

**Given** a script that runs `harnessctl accept-candidate --wheel x.whl`.

**When** it runs against the candidate.

**Then** the exit status is 2, standard output is empty, and standard error
names `harnessctl qualify candidate-package`.

## Open decisions

None.

## Amendment record

**The `next` alias is removed before it ships, proposed 2026-08-29 under
`WO-ECP-020`.** The statement keeps `next` "as a one-release alias that
announces its removal"; the owner decided on 2026-08-29 ("we remove next
now") that no release ships the alias: the managed `WORKFLOW.md` and the
evaluator always travel together, so no root instruction names `next`
against an evaluator that lacks it, and the alias would only have served
consumer-owned content. The required response is read as: `harnessctl
next` is not a subcommand and is refused with a message naming
`harnessctl check`. The failure example for a script on `accept-candidate`
applies equally to one on `next`. Nothing else in this requirement changes.
