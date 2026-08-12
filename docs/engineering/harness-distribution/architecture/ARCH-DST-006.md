+++
id = "ARCH-DST-006"
type = "architecture"
title = "Progressive documentation responsibility architecture"
status = "approved"
owners = ["technical-owner", "documentation-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
addresses = ["REQ-DST-019", "REQ-DST-020", "REQ-DST-021", "REQ-DST-022", "REQ-DST-023"]
conforms_to = ["SPEC-DST-006"]

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "public-interface-or-protocol", "cross-cutting-policy", "material-alternatives"]
rationale = "The change assigns durable responsibilities across the public package README, non-authoritative learning notes, managed policy, repository-owned guidance, and implementation observations; it changes a public documentation interface and selects among materially different duplication and generation strategies."
assessed_by = "technical-owner"
+++

# Architecture: Progressive documentation responsibility architecture

## Context and scope

SE Harness needs a progressive human learning path without creating another copy of its governing policy. The root README is a public package interface, `docs/notes/` is explanatory, managed policy defines authority, repository context defines local facts, and source plus tests expose implementation behavior. This architecture assigns clear dependency direction among those surfaces.

## Components and responsibilities

- **Public README, expertise 6/10**: value, release installation, quick start, compact current reference, and navigation to deeper notes.
- **Notes index, expertise 4/10**: expertise scale, ordered learning path, and non-authoritative boundary.
- **Tier-0 overview, expertise 4/10**: why and what, using simple language.
- **Conceptual UML model, expertise 6/10**: what relates to what under the current typed model.
- **Operational phasing, expertise 6/10**: when artifacts, checks, commits, and decisions occur.
- **Branching example, expertise 6.5/10**: one possible repository policy mapping, never a universal rule.
- **Practical examples, expertise 7/10**: how the complete lifecycle is operated with current commands.
- **Managed contract and policy**: authoritative workflow, decision rights, quality gates, and traceability; linked, not copied.
- **Repository context**: current owner-confirmed commands and conventions; informative but non-authoritative.
- **Implementation and tests**: inspected evidence for behavior, never product or governance authority.
- **Focused documentation tests**: protect stable structural and terminology contracts without freezing prose unnecessarily.

## Dependency direction

```text
managed policy + formal artifacts --------> authority statements
current implementation + tests ----------> behavior statements
release evidence + public services ------> external release facts
repository context ----------------------> local commands and conventions
                                            |
                                            v
README -------------------------------> notes index
                                            |
                   +------------------------+----------------------+
                   v                        v                      v
              overview                 UML model              phasing
                                                                    |
                                                                    v
                                                        branching example
                                                                    |
                                                                    v
                                                         practical examples
```

Explanatory documents depend on authoritative and observable sources. No explanatory document feeds authority back into the formal graph.

## Data and control flow

1. Inventory current documentation, managed policy, implementation, tests, templates, release facts, and existing branch draft.
2. Classify each claim as harness authority, implemented behavior, repository policy, external fact, or illustration.
3. Assign the claim to one owning document and replace large repetition elsewhere with a cross-reference.
4. Render the current typed entity model and lifecycle ordering consistently across diagrams.
5. Run static, executable, formal-graph, integrity, link, and manual reader-level checks.
6. Retain evidence and report unresolved policy/implementation discrepancies without changing behavior.

## Trust boundaries

- Existing Markdown, examples, branch names, release text, and diagrams may be stale or copied from another repository and must be treated as untrusted documentation input.
- Source and tests demonstrate behavior but cannot override managed policy or formal approvals.
- Public service state is external evidence and must be independently checked before being stated as current fact.
- Branching examples are repository-policy illustrations and never formal SE Harness authority.

## Required patterns

- One expertise label per in-scope document.
- One owner question per document and cross-links for depth progression.
- One current typed traceability vocabulary.
- One explicit separation between automated observations and accountable decisions.
- One branching model labeled illustrative.
- Concrete commands and repository paths only after checking current implementation.
- Text remains understandable when a diagram renderer is unavailable.

## Prohibited patterns

- Mokiterions-specific facts presented as `se_harness` state.
- Legacy `ARCH.constrains` presented as the current authoring relation.
- The validator, Explorer, tests, or CI presented as governance authority.
- Duplicating complete managed policy in every explanatory note.
- Presenting branch prefixes or merge strategy as universal harness requirements.
- Editing behavior, historical evidence, formal records, or public state to simplify a narrative.
- Hiding the known authoritative-gate versus Explorer-readiness discrepancy.

## Quality attributes

The documentation shall prioritize accuracy, progressive disclosure, navigability, renderer independence, auditability, terminology consistency, and maintainability. Concision means avoiding duplicated policy, not omitting boundaries needed to prevent unsafe interpretation.

## Conformance checks

Apply `VER-DST-006`. Validate expertise labels and the required document set, compare documented commands to CLI parsing, compare relations to managed traceability, inspect diagrams as source and rendered Mermaid where available, run public-onboarding and full regression tests, validate the formal graph, run `doctor` and preflight, generate Explorer deterministically, verify links, and inspect the diff for unrelated changes.

## Related ADRs

`ADR-DST-006` decides the progressive layered documentation model and its authority boundary.
