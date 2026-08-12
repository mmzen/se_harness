+++
id = "REQ-DST-028"
type = "requirement"
title = "Retained public value and authority narrative"
status = "approved"
owners = ["product-owner", "documentation-owner"]
created = "2026-08-12"
updated = "2026-08-12"
statement = "WHEN the root README is condensed, THE SYSTEM SHALL retain a persuasive user-centered scenario, a compact lineage visualization, the human-agent-repository responsibility boundary, Harness Explorer value, material known limitations, and a contributor route."
verification_method = "automated-test-and-reader-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Retained public value and authority narrative

## Rationale

A short README that contains only installation commands would explain how to start but not why the harness is valuable. Simplification must preserve its strongest product demonstration and prevent agents or automated checks from appearing to own human decisions.

## Preconditions and trigger

The large practical graph, artifact model, operating workflow, Explorer section, safety section, and contributor sections are consolidated.

## Required response

The resulting README retains:

- a short realistic request-to-release story;
- one compact graph showing approved outcome, defined work, bounded agent implementation, evidence and exact candidate commit, human verification, human release, and Explorer observation;
- a concise responsibility table for human owners, coding agents, and repository policy;
- the practical questions answered by Explorer without reproducing its complete gate model;
- compact disclosure of the two known 0.2.2 policy/checker tensions;
- a route for distribution contributors without embedding the source-development manual.

## Failure and boundary behavior

The visualization must remain understandable as Mermaid source and adjacent prose. Color cannot carry unique meaning. The story must not imply that the agent commits, pushes, verifies, releases, or publishes without separate authority.

## Constraints

- Preserve exact candidate-commit provenance and separate human assurance/release decisions.
- Avoid a complete artifact catalog, directory tree, or command reference in the root.
- Keep links suitable for GitHub and the PyPI-rendered README.

## Acceptance examples

### Example: evaluator understands the value

**Given** a reader scans the README,

**When** they reach the example and graph,

**Then** they can explain how approved purpose becomes bounded work, evidence, exact provenance, and accountable decisions.

### Example: rendering without Mermaid

**Given** a Markdown consumer shows the Mermaid block as source,

**When** the reader follows labels and surrounding prose,

**Then** no authority or provenance distinction is lost.

## Open decisions

Exact visual styling and whether Explorer questions are bullets or compact prose remain delegated within the information budget.
