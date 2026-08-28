+++
id = "ADR-AEX-008"
type = "adr"
title = "Phase 4 is product, reduced to its guarantee: delegation at the Git boundary, journaled apply, no broker or envelope"
status = "approved"
owners = ["product-owner", "technical-owner", "repository-owner", "security-owner"]
created = "2026-08-28"
updated = "2026-08-28"

[relations]
decides = ["ARCH-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T20:03:17Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'Approve', recording the product owner's disposition of issue #211 given the same day: Phase 4 agentic execution is product, reduced to its guarantee \u2014 delegation as a work-order attribute unlocking start, completion and record preparation behind the mandatory pull-request gate, the journaled apply with rollback and human-recovery-stop kept, the broker, the envelope, delegated-workflow, the Phase 2 machinery, the unread contracts and the three writing skills removed under WO-ECP-006 and WO-ECP-007. Consistent with REQ-ECP-011, REQ-ECP-017, REQ-ECP-018 and SPEC-ECP-006 approved on 2026-08-28. Measured before this transition over branch state a58bbdf carrying unmoved main b460085 under the governing exact public 0.8.0 root: validate PASS at 0 errors; Phase 4 at 8,766 of 20,937 package lines with no activation in any target. This decision authorizes no work order, code change, release or publication; issues #215 to #219 close as superseded by it."
+++

# ADR: Phase 4 is product, reduced to its guarantee

## Status

Proposed. Records the owner decision issue #211 asked for. Supersedes the
broker and envelope selections of `ADR-AEX-006` and `ADR-AEX-007` for the
product surface; `ADR-AEX-001` through `ADR-AEX-005` and `ARCH-AEX-001`
(harness-owned authority, non-authoritative skills, thin state-gated skills)
stand. `ARCH-AEX-002` (the evaluator-owned effect broker) is superseded by
`ARCH-ECP-001` and amended by date.

## Context

The Phase 1→4 agentic chain is 8,766 of 20,937 package lines (42% at `main`
`b460085`), built 2026-08-24 to 08-26, and has never been activated in any
target: no `[agentic_delegation]` table exists outside the work-order
template, nothing in CI, release qualification or the installer invokes
`delegated-workflow`, and `resolve_delegation` refuses every real work order
(`AEXAUTH003`). The five shipped skills (22 managed files) are installed in
every consumer by `init` and `upgrade`; three of them route through the
inert subcommand and inject a stub client while saying they invoke the
evaluator. The 2026-08 complexity audit (P0-5) asked the owner to decide
between product and experiment before any of its five [AEX] sub-items
(P1-3 to P1-7, issues #215–#219) is worked, because each is a change inside
a design that may not survive.

On 2026-08-28 the owner approved the execution-control-plane definitions,
among them `REQ-ECP-011` (a delegation class unlocks `DR-WO-START`,
`DR-WO-COMPLETE` and `DR-VREC-PREPARE` only while the pull-request gate is
passing), `REQ-ECP-017` (every harness-owned multi-file write is one
journaled apply with rollback and a human-recovery stop), `REQ-ECP-018` (no
envelope, nonce-ledger, lifetime or revocation interface in the product)
and `SPEC-ECP-006`, whose `ECP-DLG-008` takes `delegated-workflow` and
`[agentic_delegation]` out of the product surface. The independent
agentic-execution review (`docs/notes/agentic-execution-review-2026-08.md`,
§10–11) recommends the same shape.

## Decision drivers

- Keep the guarantee Phase 4 was built for: an agent cannot start, complete
  or prepare assurance for a work order that is not approved, in scope and
  green at the gate; and a harness-owned multi-file write cannot half-land.
- Enforce at boundaries the harness controls (the diff, the pull-request
  gate, the decision record), not with a token that never leaves the
  process that minted it.
- Stop maintaining two execution models agents must recognise and ignore.
- Decide once, so the [AEX] sub-items are closed or scheduled as a unit.

## Considered options

1. **Product as built.** Keep the broker, envelope, contracts and skills and
   fix P1-3 to P1-7 in place. Rejected: it conflicts with `REQ-ECP-018` and
   `ECP-DLG-008`, already approved, and keeps ~8,000 lines defending a token
   against threats that do not exist inside one process.
2. **Experiment, quarantined.** Move `delegated-workflow` and the three
   writing skills behind a feature boundary, out of the managed manifest and
   the portable surface, and freeze the domain. Rejected: it preserves the
   design's cost for consumers who already carry the skills, defers the
   same decision, and leaves the delegation guarantee unshipped.
3. **Product, reduced to its guarantee.** Selected.

## Decision

Phase 4 is product. What it guarantees is kept and what it defends against
is removed:

- **Kept**: delegation as a work-order attribute (`[delegation]`, one
  class) that unlocks `DR-WO-START`, `DR-WO-COMPLETE` and `DR-VREC-PREPARE`
  only while the mandatory pull-request gate for the candidate is passing,
  writing a decision record per transition (`REQ-ECP-011`,
  `SPEC-ECP-006` `ECP-DLG-*`); the journaled apply with rollback and
  `human-recovery-stop` for every harness-owned multi-file write
  (`REQ-ECP-017`, `ECP-JNL-*`); the `resolve_delegation` narrowing;
  `mutation_guard` gating; the read-only `harness-orient` and
  `harness-operator-brief` skills.
- **Removed from the product**: the effect broker and bundle pipeline, the
  autonomy envelope with its nonce ledger, lifetime, revocation store,
  retry ordinal and two-capture stability, the `delegated-workflow`
  subcommand and `[agentic_delegation]`, the Phase 2 admission and packet
  machinery, `agent_contract.json` and the `skill_contract` schema
  generations with zero product callers, and the three writing skills that
  invoke the removed subcommand (`REQ-ECP-018`, `ECP-DLG-008`).
- **Executing work orders**: `WO-ECP-006` (reduce Phase 4 to its guarantee
  and introduce the delegation class), after `WO-ECP-003` (the mandatory,
  scope-aware pull-request gate) which it depends on; `WO-ECP-007` for the
  product-surface evictions it already names. No work is authorized by this
  record; each work order is approved and started separately.
- **Disposition of the [AEX] sub-items**: #215 (envelope apparatus), #217
  (dead Phase 2 machinery and `agent_contract.json`), #218
  (`skill_contract.py`) and #219 (stub-client skill helpers) are superseded
  by this decision and closed; their proposals are absorbed where the kept
  parts need them (#215's narrowing and single fresh observation, #217's
  retained bounded walk and portable-path validation, #218's SHA-256 pin per
  shipped contract for the two surviving skills). #216 (observation cost)
  is superseded with the broker; the one observation before and after that
  survives is `WO-ECP-006`'s to keep cheap.

## Consequences

- Positive: one execution model; the guarantee ships instead of staying
  inert; consumers stop receiving three skills that cannot do what they say;
  about 8,000 lines and 50-odd artifacts' worth of design stop moving under
  the P1 work.
- Negative: the broker's isolation-by-proposal and receipt trail, which the
  review rated the strongest part of the design, are replaced by Git's
  branch and the pull-request gate; a retained journal is the only harness
  artefact of a write. Multi-agent and child delegation (Phase 5) stay
  out of harness machinery, as `ARCH-AEX-001` already allowed.
- Domain: `agentic-execution`'s Phase 4 artifacts are retained as history;
  the ones `WO-ECP-006` retires are amended by date under it, as
  `REQ-REB-016` and `REQ-REB-026` were.

## Validation

`VER-ECP-006` under `WO-ECP-006`; the acceptance of issue #211 — an approved
ADR stating the disposition and every P1-3…P1-7 issue scheduled or closed —
is met by the approval of this record and the closing comments it
authorizes.
