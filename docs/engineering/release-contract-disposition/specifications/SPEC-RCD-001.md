+++
id = "SPEC-RCD-001"
type = "specification"
title = "Historical release-proposal disposition"
status = "implemented"
owners = ["release-owner", "quality-owner", "repository-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
specifies = ["REQ-RCD-001"]
+++

# Specification: Historical release-proposal disposition

## Exact scope

Dispose exactly these contracts:

| Proposal | Gated work | Authoritative contract | Release record | Version and tag |
| --- | --- | --- | --- | --- |
| `REL-AGR-001` | `WO-AGR-001` | `REL-DST-001` | `RLS-SEH-001` | `0.2.0`, `v0.2.0` |
| `REL-PMI-001` | `WO-PMI-001` | `REL-DST-001` | `RLS-SEH-001` | `0.2.0`, `v0.2.0` |
| `REL-VSP-001` | `WO-VSP-001` | `REL-DST-001` | `RLS-SEH-001` | `0.2.0`, `v0.2.0` |
| `REL-IAR-001` | `WO-IAR-001` | `REL-SEH-002` | `RLS-SEH-002` | `0.2.1`, `v0.2.1` |
| `REL-PYP-001` | `WO-PYP-001` | `REL-SEH-002` | `RLS-SEH-002` | `0.2.1`, `v0.2.1` |
| `REL-WLC-001` | `WO-WLC-001` | `REL-SEH-002` | `RLS-SEH-002` | `0.2.1`, `v0.2.1` |

## Transition rules

1. Confirm each selected contract is `draft` and no release record satisfies it.
2. Confirm its complete `gates` set is included in the named released RLS.
3. Change only `status` to `rejected` and `updated` to `2026-08-16` in formal metadata.
4. Append a concise disposition section naming the authoritative aggregate lineage and explaining that rejection applies to the unused proposal, not the released implementation.
5. Correct each domain index from an outstanding draft claim to the same factual disposition.
6. Preserve gates, owners, original contract clauses, actual aggregate contracts, VRECs, RLS records, tags, release evidence, OPS records, and software behavior unchanged.

## Exclusions

No release-contract supersession relation, retroactive approval, new RLS, release rewrite, tag change, publication, deployment, validator change, inspection-rule change, or automatic lifecycle action is allowed.
