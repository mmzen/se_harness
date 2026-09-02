+++
id = "REQ-ECP-024"
type = "requirement"
title = "The projection has exactly one command name"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-29"
updated = "2026-08-29"
statement = "WHEN the alias window that REQ-ECP-022 opened closes with the release after 0.10.0, THE SYSTEM SHALL offer the selected-artifact projection under the single name check, refuse focus with a message naming check, orient through check in its shipped skill, and retain every earlier skill identity as history, so that an operator, an agent and a consumer's script meet one name for one operation."
verification_method = ["test"]
priority = "must"
source = "harnessctl command audit of 2026-08-29 (P1); ECP-ONE-007 deferred at WO-ECP-015's completion"

[relations]
derives_from = ["CAP-ECP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T12:27:21Z"
decided_by = "requirements-steward"
reason = "Approved by the requirements steward on 2026-08-29 with the words 'Approve and start WO-ECP-017': the projection has exactly one command name once the alias window of REQ-ECP-022 closes."
+++

# Requirement: The projection has exactly one command name

## Rationale

`REQ-ECP-022` folded `focus` into `check` and kept `focus` for one release
as a byte-identical alias with a deprecation notice (`ECP-ONE-004`). The
alias exists so that a consumer's script written against 0.10.0 keeps
working through the next upgrade; it is not a second command. Keeping it
longer would leave three names for one projection (`focus`, `next`,
`check`) — the most confusing thing on the command list for a newcomer —
and a shipped skill (`harness-orient`) still invoking the alias, which
`WO-ECP-015` had to defer because the skill's core is a digest-pinned
surface (`ECP-ONE-007`).

## Behavior

- Trigger: the candidate after 0.10.0 is built.
- Response: `harnessctl focus` is not a subcommand; invoking it exits with
  status 2 and one line on standard error naming `harnessctl check
  --artifact ID`. `harness-orient` invokes `check` where it invoked
  `focus`, reading the same sections. Every retained skill-identity vector
  is unchanged and a later vector row records the new identity with the
  old one as its predecessor. No procedure step, rule, gate, contract file
  or result schema changes.
- On failure: none introduced; `check` fails exactly as it does today.

## Assumptions and dependencies

- `ECP-ONE-001` to `ECP-ONE-006` and `ECP-ONE-008` hold on `main`
  (`VREC-ECP-018`).
- The operation identifier `focus-json` in the skill contracts, the
  frozen profiles and retained receipts is contract vocabulary for "the
  selected-artifact projection as JSON"; it names a capability, not the
  command, and stays. Its renaming is tied to the fate of the Phase 4
  contracts (audit item P0), which is a separate owner decision.

## Acceptance examples

### Example: normal behavior

**Given** the candidate evaluator.

**When** `harnessctl check . --artifact WO-001 --json` runs.

**Then** the projection of `SPEC-ECP-011` is returned, and `harnessctl
--help` lists no `focus`.

### Example: failure behavior

**Given** a script that still runs `harnessctl focus . --artifact WO-001`.

**When** it runs against the candidate.

**Then** the exit status is 2, standard output is empty, and standard error
names `harnessctl check --artifact WO-001`.

## Open decisions

None.

## Amendment record

**The clause "refuse focus with a message naming check" is closed, proposed 2026-09-02 under `WO-ECP-025` (`REQ-ECP-030`, `SPEC-ECP-019` `ECP-TMB-001`).** The refusal described the one-release window after 0.10.0; three releases have shipped, the pre-parse guard is gone, and the parser refuses `focus` as it refuses any unknown command. Everything else in this requirement is unchanged.
