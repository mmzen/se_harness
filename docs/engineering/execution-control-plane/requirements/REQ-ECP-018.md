+++
id = "REQ-ECP-018"
type = "requirement"
title = "No envelope apparatus in the product surface"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-27"
updated = "2026-08-28"
statement = "THE SYSTEM SHALL expose no autonomy-envelope, nonce-ledger, lifetime, or revocation interface in the product CLI or the public Python API."
verification_method = ["analysis", "test"]
priority = "must"
source = "complexity audit P1-3; review section 5, weakness 3"

[relations]
derives_from = ["CAP-ECP-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "requirements-steward"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Requirement: No envelope apparatus in the product surface

## Rationale

The authority envelope defends a token that never crosses a trust boundary: a
five-minute `MAX_ENVELOPE_LIFETIME`, a nonce ledger, `revoked` passed by product
code zero times, `retry_ordinal` always 0, and a two-observation stability rule
(se_harness/delegated_authority.py:25, :206, :262, :343;
se_harness/runtime_state.py:368-434; se_harness/repository_state.py:375-418;
docs/notes/complexity-audit-2026-08.md:260). `se_harness/cli.py:1259-1304`
accepts no envelope input (docs/notes/agentic-execution-review-2026-08.md:
214-222). Phase 4 is 8,766 lines, 39% of the package, never activated in any
target (docs/notes/complexity-audit-2026-08.md:46-54). With delegation moved to
a work-order attribute (REQ-ECP-011), the apparatus has no purpose left.

## Behavior

- Trigger: always: an invariant over the CLI's `--help` tree and the public
  `se_harness` API.
- Response: no subcommand, option, module-level function, or class exported by
  `se_harness` accepts or produces an autonomy envelope, a nonce, an envelope
  lifetime, or a revocation entry; `delegated-workflow` and its envelope
  constructors are absent; the journaled apply of REQ-ECP-017 and
  `resolve_delegation` scope narrowing remain.
- On failure: the portable-surface check fails a pull request that reintroduces
  any of the names `envelope`, `nonce`, `revocation`, or `lifetime` into the CLI
  help or the public API inventory.

## Assumptions and dependencies

- The public API inventory is the packaged surface the release lane already
  projects (docs/notes/complexity-audit-2026-08.md:136-137 names the checker).
- ADR-AEX-006 and ADR-AEX-007 receive amendment records under the work order
  that delivers this; the artifacts stay as history.
- Replay protection is re-added only when an externally supplied envelope
  exists, which is out of scope here.

## Acceptance examples

Executable scenarios live in `acceptance/REQ-ECP-018.feature` and are named by
the verification contract that covers this requirement.

### Example: normal behavior

**Given** the candidate wheel is installed in a clean environment.

**When** `harnessctl --help` and every subcommand's `--help` are captured, and
the public API inventory is generated.

**Then** none contains `envelope`, `nonce`, `revocation`, or `lifetime`, and
`harnessctl delegated-workflow` is an unknown command.

### Example: failure behavior

**Given** a pull request adds `--envelope FILE` to `transition`.

**When** the surface check runs.

**Then** the check fails and names `se_harness/cli.py` and the option.

## Open decisions

None.
