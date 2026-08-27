+++
id = "ADR-REB-011"
type = "adr"
title = "Upgrade the root from the installed evaluator's payload identity, without a packet"
status = "approved"
owners = ["technical-owner", "repository-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
decides = ["ARCH-REB-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T15:20:02Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-27 by the accountable owner, 'Approve and start', on the owner's direction that the evaluator upgrade must be simple: the MG007 work-order packet and the MG004 and RID022 archive-digest requirements are retired, the installed evaluator's version and payload digest are its identity, index installs pass the managed lane, and the candidate-evidence lane selects the acceptance operation by the verifier's capability. REQ-REB-005 is superseded under WO-REB-027."
+++

# ADR: Upgrade the root from the installed evaluator's payload identity, without a packet

## Status

Proposed on 2026-08-27 on the repository owner's direction; decides
`ARCH-REB-011`.

## Context

`WO-REB-003` (2026-08-21) made every evaluator identity transition require a
separately approved `[evaluator_upgrade]` work-order packet naming the prior
lock and the target wheel and payload digests (`MG007`), and required the
target evaluator to be installed from a wheel file so that a PEP 610 archive
digest exists (`MG004`). 0.7.0 extended the same idea into `identity`
(`RID022`) and into the managed workflow's `qualify released-root`.

Adopting 0.7.0 (`WO-HUP-006`, 2026-08-27) measured the cost: a seven-artifact
packet, three scope amendments, a wheel-file reinstall after an index install
was refused, and a managed lane that cannot pass for any adopter because the
released workflow itself installs from the index. The owner's judgment: the
wheel-digest check and the work-order binding are too restrictive; the
install process must be simple and straightforward.

## Decision drivers

- An upgrade must be one command after an ordinary `pip install`.
- The boundary must still prove that the evaluator running the write is a
  released one, isolated from the checkout.
- Managed CI must pass from an index install.
- Repository policy, not the tool, decides which change is authorized.

## Considered options

1. **Keep the packet; document the wheel-file install.** Rejected: it keeps
   the cost the owner rejected and leaves the managed lane defective.
2. **Keep `MG007`, drop `MG004`.** Rejected: the packet is the larger cost
   and duplicates the repository's own work-order policy.
3. **Identity by version and payload; archive digest as corroboration;
   no packet** — chosen.
4. **No identity proof at all on upgrade.** Rejected: it would let a
   candidate checkout or a tampered install rewrite the root.

## Decision

Option 3. The installed evaluator's version and installed-payload digest are
its identity; the archive digest is compared only when recorded; the upgrade
applies without a packet; `MG007` and `upgrade_authorization` are retired;
`MG004` remains only for an evaluator that cannot identify itself at all.

## Consequences

- One command upgrades a root; the managed lane passes from an index install.
- The lock may carry `archive_sha256 = null`; consumers treat it as unknown,
  not as absent identity.
- The historical `[evaluator_upgrade]` tables of `WO-HUP-002` and
  `WO-HUP-006` stay as history; `REQ-REB-005` is superseded.
- Tamper resistance rests on the payload digest and the isolation proofs,
  which is what `RID021`, `RID018` and `doctor` already enforce.

## Validation

`VER-REB-011`: index install, wheel install, mismatch and candidate-checkout
cases; the managed template's qualification on an index install; the
candidate-evidence lane on both verifier generations.
