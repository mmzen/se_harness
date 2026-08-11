+++
id = "ADR-DST-002"
type = "adr"
title = "Use AGENTS.md as the shared contract and seed repository context once"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
decides = ["ARCH-DST-002"]
+++

# ADR

## Status

Accepted by the accountable human through approval of the proposed harness changes on 2026-08-11.

## Decision

Use root `AGENTS.md` as the canonical cross-agent operating contract. Provide Claude Code compatibility through a checked-in `CLAUDE.md` import rather than duplicating the contract or using a Windows-sensitive symbolic link.

Create repository context from a seed template exactly once per installation lineage. Record seed state in the lock without hashing its content, making repository ownership explicit while retaining deterministic upgrade behavior.

## Consequences

Shared rules have one source, Claude-specific additions can remain outside the managed block, and repository facts can evolve without being reported as distribution drift. Doctor can still diagnose a missing context file or broken Claude import without claiming authority over their substantive contents.
