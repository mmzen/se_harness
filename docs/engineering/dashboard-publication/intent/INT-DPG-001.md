+++
id = "INT-DPG-001"
type = "intent"
title = "Make released SE Harness governance visible"
status = "approved"
owners = ["product-owner", "repository-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
+++

# Intent: Make released SE Harness governance visible

## Problem

Harness Explorer makes the repository's governed engineering graph understandable, but today a prospective user must install the project or clone the repository to see it. Screenshots show isolated views and become stale; they do not let a visitor explore the actual relationships, decisions, evidence, and release lineage produced while developing SE Harness itself.

## Desired outcomes

After an SE Harness release is completed, visitors can open a public, release-bound Explorer demonstration generated from the repository's governed state. The site demonstrates the value of SE Harness using its own development history while remaining visibly derived and non-authoritative.

## Actors and stakeholders

- Evaluators and prospective adopters explore a concrete governed repository without installing anything.
- Maintainers publish and, when necessary, replay a bounded static deployment.
- Accountable assurance and release owners retain all formal decision rights in repository artifacts.
- Security and repository owners control what repository-derived data becomes public.

## Success measures

| Measure | Baseline | Target | Observation window |
| --- | ---: | ---: | --- |
| Completed releases with an accessible release-bound demo | 0 | Each selected release | Per release |
| Published snapshot with resolvable release, governance, and candidate provenance | 0 | 100% | Per deployment |
| Consumer repositories changed by this feature | 0 | 0 | Continuous |
| Publication failures that still report success | Unknown | 0 | Per workflow run |

## Non-goals

- Hosting dashboards for repositories that install SE Harness.
- Making GitHub Pages, GitHub Actions, or a branch strategy mandatory for consumers.
- Replacing repository artifacts, validation, VREC review, or release authorization with a public site.
- Publishing private repositories, unreviewed worktrees, arbitrary branches, or user-supplied HTML.
- Promising an independent availability SLO for a promotional demonstration.

## Principles and immutable constraints

- Publication occurs only after a release decision and binds to an immutable governance snapshot.
- The generated site is derived evidence with no lifecycle or decision authority.
- The deployment is specific to the `mmzen/se_harness` development repository and is not a managed consumer workflow.
- Generation reuses the canonical Explorer contract; publication must not create a second dashboard model.
- Ambiguous release lineage, invalid artifacts, unsafe output, or failed deployment stops publication.

## Risks and assumptions

GitHub Actions and GitHub Pages are external availability and trust dependencies. The Explorer also retains the exact optional CDN dependency accepted by `ADR-DST-008`. The repository is public, but public repository status alone does not authorize publishing arbitrary files; only the bounded generated dashboard payload may be deployed.
