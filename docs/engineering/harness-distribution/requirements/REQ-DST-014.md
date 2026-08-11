+++
id = "REQ-DST-014"
type = "requirement"
title = "Demonstrate governed agent work and its traceability value"
status = "implemented"
owners = ["product-owner", "documentation-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN a prospective user evaluates SE Harness from the public README, THE SYSTEM SHALL demonstrate a representative human-and-coding-agent workflow and SHALL visualize the resulting governed traceability chain from approved outcome through exact verified revision and separately authorized release."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Demonstrate governed agent work and its traceability value

## Rationale

The public README explains installation, artifacts, commands, provenance, and authority in detail, but it does not yet show how those controls feel to a repository owner delegating ordinary engineering work to a coding agent. Readers must assemble the value proposition from separate reference sections before they can see how the harness changes a real interaction.

## Required response

- Place one short representative example immediately after the quick start and before the feature inventory.
- Lead with natural-language requests from a repository owner rather than presenting routine `harnessctl` commands as manual user work.
- Show the coding agent preparing the governed chain, exposing missing decisions, respecting approved scope, running preflight and verification checks, retaining evidence, and binding verification to an exact candidate commit.
- Keep work-order approval, assurance review, and release authorization with accountable humans.
- Visualize the representative chain from intent and requirement through design, authorized work, implementation evidence, candidate commit, verification, and release.
- Use consistent semantic colors, labels, and shapes so product intent, design, work, evidence, provenance, human decisions, and release state remain distinguishable.
- Follow the graph with a concise statement of business value: explainable purpose, bounded execution, retained evidence, exact provenance, visible anomalies, and a separately controlled release path.

## Failure and boundary behavior

The example and graph are explanatory views, not formal artifacts, approvals, verification records, release records, or claims that every repository follows the illustrated topology exactly. They must not imply that the agent grants approval, validates its own evidence accountably, releases software, or replaces human judgment.

If a Markdown renderer does not render Mermaid, the surrounding prose and the labeled diagram source must remain understandable. Color must not be the only carrier of meaning, and the README must not require executable scripts, remote styles, or a second image source to communicate the example.

## Constraints

- Preserve the PyPI-first onboarding order and the root README as the single repository and package-index description.
- Do not change CLI behavior, package metadata, version, installed templates, workflows, baseline pins, lock data, release records, tags, published files, or external configuration.
- Do not present `harnessctl` as a conversational agent or claim that automation creates product or governance authority.
- Keep the section short enough to demonstrate value before the detailed reference material.

## Acceptance examples

A prospective user can read one short interaction, understand what the agent does behind the scenes, see which decisions remain human, and trace the example to an exact verified revision and a separately authorized release without first learning every artifact type or CLI command.

## Open decisions

The packet proposes a narrative plus an inline Mermaid flowchart with textual fallback. Accountable owners must approve that rendering tradeoff before implementation.
