+++
id = "ADR-IAR-001"
type = "adr"
title = "Use a thin adapter, one managed router, and modular policy"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
decides = ["ARCH-IAR-001"]
+++

# ADR: Use a thin adapter, one managed router, and modular policy

## Decision

Use `AGENTS.md` as the universal repository entry with a short managed fragment, `CLAUDE.md` as a thin import adapter, and `ENGINEERING_HARNESS.md` as the only fully managed instruction router. Preserve repository context and the engineering domain index as owner-owned seeds. Keep workflow, decision rights, quality gates, and traceability as focused managed modules directly linked by the router. Back the route with preflight and independent required CI.

## Rationale

A short universal entry is more likely to be consumed consistently and can coexist with local instructions. A fully managed router provides one integrity-protected place to define authority and select relevant policy. Focused modules remain reviewable and independently evolvable. Owner-owned context can change with the repository without causing false managed-file drift. Executable checks address structural enforcement that prose cannot provide.

## Alternatives rejected

- **Put all policy in `AGENTS.md`**: rejected because it makes the managed fragment large, duplicates local guidance, and increases collision risk in existing repositories.
- **Keep several mandatory destinations in the managed AGENTS block**: rejected because ordering and ownership remain ambiguous and adapters repeat navigation.
- **Merge all policy into `ENGINEERING_HARNESS.md`**: rejected because a large monolith reduces focused review and causes every policy change to rewrite the primary entry contract.
- **Use `docs/engineering/README.md` as the managed router**: rejected because the same file is valuable as a repository-owned domain index; combining roles obscures ownership and makes safe customization harder.
- **Use symlinks or duplicated adapter files**: rejected for Windows portability, archive behavior, and drift risk.
- **Automatically adjudicate natural-language conflicts**: rejected because the result would be non-deterministic and could silently infer authority.
- **Rely only on checked-in validators in CI**: rejected because the candidate can modify both the rule and the checker in one change.

## Consequences

The engineering README changes from managed content to an owner seed and needs an explicit safe mode migration. The managed router becomes a stronger compatibility surface. Preflight and CI add implementation and maintenance cost. Host governance still requires owner configuration. The resulting architecture has fewer navigation edges, clearer ownership, and a materially stronger enforcement boundary.

## Revisit conditions

Revisit if a supported agent cannot consume `AGENTS.md`, if policy-module selection becomes materially inconsistent, or if a portable repository-host API can verify protection settings without expanding installation authority.
