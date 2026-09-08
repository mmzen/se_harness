+++
id = "ARCH-DST-002"
type = "architecture"
title = "Shared instruction and repository-context ownership boundaries"
status = "implemented"
owners = ["technical-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-09-08"

[relations]
addresses = ["REQ-DST-007"]
conforms_to = ["SPEC-DST-002"]

[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "responsibility-or-dependency-direction", "difficult-to-reverse", "material-alternatives"]
rationale = "ADR-DST-002 chose root AGENTS.md as the cross-agent contract with a CLAUDE.md import, over duplicating the contract and over a Windows-sensitive symbolic link. It also seeds repository context once per installation lineage, a lock fact later installs cannot retract."
assessed_by = "technical-owner"
+++

# Architecture

The installed instruction surface has three ownership classes:

1. Harness-owned bounded fragments provide shared invariants and cross-agent loading.
2. Repository-owned content outside shared-root markers provides local agent rules.
3. A one-time repository-context seed provides a discoverable location for explicit local facts and becomes repository-owned immediately.

The lock distinguishes `fragment`, `managed`, and `seed` modes. Fragment and managed modes retain hashes for safe upgrade classification. Seed mode retains only whether the installation has accounted for the path, preventing the distribution from treating repository facts as immutable or regenerating an intentionally removed file.

No repository scan may author commands, architectural claims, or lifecycle authority in the context file.

## Amendment record

**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-DST-002`).** `REQ-DST-007`
becomes the addressed requirement and `conforms_to` names `SPEC-DST-002`, the
active specification that specifies it. `REQ-DST-008` is left out of
`addresses`: it is `superseded`, and an active architecture may not address an
inactive requirement. `SPEC-DST-002` still specifies it, so the historical
edge remains readable in the graph. The assessment reads the decision and
consequences of `ADR-DST-002`, the one active ADR that decides this
architecture. Title, status, statement and ADR relations are unchanged.
