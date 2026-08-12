+++
id = "ADR-DST-006"
type = "adr"
title = "Use layered expertise-based documentation with one authority direction"
status = "approved"
owners = ["technical-owner", "product-owner", "documentation-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
decides = ["ARCH-DST-006"]
+++

# ADR: Use layered expertise-based documentation with one authority direction

## Status

Accepted on 2026-08-12 when the accountable repository owner approved the packet and instructed `go for implementation`.

## Context

The public README is useful but dense. Three draft explanatory notes add depth, yet they duplicate policy, use a prior consumer repository's facts, and describe the obsolete 0.2.1 architecture model. SE Harness needs material for readers from conceptual orientation to operational use while keeping managed policy singular and authoritative.

The same root README is rendered by GitHub and PyPI, while notes are repository documentation. The solution must remain readable without a generated documentation site or source inspection.

## Decision drivers

- Give human readers a progressive 4/10-to-7/10 learning path.
- Keep the README's accepted PyPI-first structure and public-package role.
- Make current entity relationships, lifecycle timing, Git mapping, and commands understandable visually and concretely.
- Prevent explanatory prose from becoming a competing policy source.
- Keep branching strategy repository-configurable.
- Correct copied or obsolete material without rewriting historical formal records.
- Make future drift detectable through focused tests and explicit source ownership.

## Considered options

1. **Put every explanation in README.md**: rejected because the public entry becomes too long and cannot serve multiple expertise levels cleanly.
2. **Create independent exhaustive manuals for each audience**: rejected because workflow, gates, relations, and commands would be duplicated and drift independently.
3. **Generate all documentation from source and artifact metadata**: rejected because current prose semantics, human explanations, and policy distinctions are not derivable safely; generation would also add behavior outside this documentation change.
4. **Keep the existing draft notes with local corrections only**: rejected because their responsibilities overlap and the legacy model would remain structurally easy to reintroduce.
5. **Use one public README plus layered expertise-labeled notes that link to singular managed policy**: selected because it supports progressive learning, preserves renderer portability, and maintains one-way authority.

## Decision

Adopt option 5. Preserve the README as the 6/10 public and operational entry point. Add a 4/10 notes index and Tier-0 overview, a 6/10 conceptual UML model and operational-phasing guide, one 6.5/10 illustrative branching model, and 7/10 practical examples.

Each surface owns one reader question and cross-references deeper or authoritative material. Managed policy and formal artifacts remain authoritative; repository context remains owner-controlled guidance; notes remain non-authoritative; implementation and tests remain evidence of behavior. Expertise labels identify expected reader knowledge only.

Document one main-plus-short-lived-work-branch workflow as an example, but state explicitly that SE Harness is branching-model-independent. Report the current G0-G5 policy/Explorer semantic discrepancy without changing either behavior or policy in this work.

## Consequences

Readers gain a clear progression without source inspection. The README remains longer than a minimal package page but can delegate depth to notes. Notes become maintainable because they do not each restate the complete policy. The repository gains three additional documentation files: a notes index, operational phasing, and branching example.

The chosen model requires disciplined links and terminology tests. GitHub/PyPI link behavior must be reviewed because relative repository links may render differently. A future behavior work order remains necessary if owners decide to align Explorer's G0-G5 computation with authoritative quality gates.

## Validation

Apply `VER-DST-006`. Review every in-scope document at its declared expertise level, verify current terminology and commands against implementation, verify policy claims against the managed router and policies, run focused and full tests, validate the formal graph, run doctor and preflight, generate Explorer, check links, and retain the unresolved gate-semantic discrepancy explicitly.

## Revisit conditions

Revisit if the README becomes unusable on PyPI, if note responsibilities again overlap materially, if a stable generated documentation system becomes an approved product capability, if SE Harness adds configurable branch-policy enforcement, or if a future work order resolves the quality-gate versus Explorer-readiness model.
