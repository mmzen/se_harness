+++
id = "ARCH-DST-007"
type = "architecture"
title = "Layered public, operator, and governance documentation"
status = "approved"
owners = ["technical-owner", "documentation-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
addresses = ["REQ-DST-024", "REQ-DST-025", "REQ-DST-026", "REQ-DST-027", "REQ-DST-028"]
conforms_to = ["SPEC-DST-007"]

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "public-interface-or-protocol", "cross-cutting-policy", "material-alternatives"]
rationale = "The change reassigns durable documentation responsibilities across the public package interface, operator and agent notes, repository-owned context, and managed governance sources; multiple materially different information architectures affect discoverability and authority interpretation."
assessed_by = "technical-owner"
+++

# Architecture: Layered public, operator, and governance documentation

## Context and scope

The root README is a public interface rendered by GitHub and PyPI. It currently carries several audiences and procedural depths, causing essential human information to compete with agent mechanics and contributor internals. `WO-DOC-007` established a progressive notes layer; this architecture makes that layer responsible for detail rather than allowing the root to continue as a monolith.

## Components and responsibilities

```text
README.md                          public human entry point (<= 200 lines)
    |
    +--> docs/notes/README.md      explanatory route by audience/expertise
              |
              +--> overview/model/phasing/branching/example
              +--> installation and upgrade operations
              +--> complete harnessctl reference
              `--> SE Harness contributor/self-hosting guide

ENGINEERING_HARNESS.md             authoritative managed router
    `--> managed policy modules    workflow, rights, gates, traceability

REPOSITORY_CONTEXT.md              repository-owned facts and commands
implementation + tests             behavior evidence, never authority
```

The public layer answers why, how to start, who decides, what the Explorer provides, and where to go next. The notes layer answers how concepts and operations work at increasing expertise. Managed policy retains normative procedure and authority. Contributor detail has a dedicated route and cannot dominate adopter onboarding.

## Dependency direction

- README links inward to explanatory notes and the managed entry point.
- Notes link to one another by owned question and route normative matters to managed policy.
- Managed policy must not depend on explanatory wording to remain complete.
- Tests inspect public documentation contracts but do not turn prose into product authority.
- No generated page, remote diagram, or external mutable document is required for comprehension.

## Data and control flow

1. Classify each current README block by audience and responsibility.
2. Keep essential public facts within the root budget.
3. Relocate current reusable detail to its owning note.
4. Retire duplication and obsolete claims explicitly in evidence.
5. Add compact links from root to the correct explanatory or authoritative owner.
6. Validate the public surface, notes graph, CLI synchronization, and protected paths.

## Trust boundaries

- Human readers may mistake command automation for accountable authority; actor and side-effect labels remain explicit.
- PyPI and GitHub render the same root source differently; diagrams retain textual meaning.
- Repository-specific Git, build, and deployment practices cannot be generalized into SE Harness requirements.
- Notes are editable explanatory content and cannot supersede managed policy.
- Agent-run mutations such as repository upgrade application remain subject to explicit owner authorization.

## Required patterns

- One concise root page with a deterministic line and section budget.
- Audience- and expertise-labeled notes with a maintained index.
- One compact public value graph and plain-language fallback.
- Human, agent, and repository-policy responsibility separation.
- Full command coverage in one reference rather than scattered root examples.
- Cross-links instead of duplicated lifecycle, model, and release procedure.

## Prohibited patterns

- A second public README variant for PyPI.
- Hiding advanced operations without a discoverable replacement.
- Treating `docs/notes/` as authoritative workflow.
- Copying managed policy wholesale into explanatory notes.
- Root examples that teach agent-only command syntax.
- Automatic repository upgrade language or implied agent approval.
- Altering behavior or formal policy to make documentation simpler.

## Quality attributes

Prioritize scanability, truthful progressive disclosure, accessibility without diagram rendering, stable public links, CLI synchronization, minimal duplication, and explicit authority boundaries. The line ceiling prevents gradual return to a monolithic root; it does not override safety or factual accuracy.

## Conformance checks

Apply `VER-DST-007`. Measure root line/section budgets, classify fenced commands, inspect graph size and fallback, validate new-note inventory and expertise labels, compare command reference against the CLI parser, resolve local links, run full documentation and repository regression checks, and audit protected surfaces.

## Related ADRs

`ADR-DST-007` decides the concise-root and layered-reference information architecture.
