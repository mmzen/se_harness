+++
id = "ARCH-RCA-001"
type = "architecture"
title = "Separate retrospective documentation from lifecycle authority"
status = "draft"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
addresses = ["REQ-RCA-003"]
conforms_to = ["SPEC-RCA-001"]

[decision_assessment]
outcome = "no_significant_decision"
triggers = []
rationale = "The work adds supporting Markdown and a formal authorization packet while preserving the existing standard-repository trust boundary, dependency direction, public interfaces, persistence, deployment model, and cross-cutting policy; no controlled architecture trigger changes."
assessed_by = "technical-owner"
+++

# Architecture: Separate retrospective documentation from lifecycle authority

## Context and scope

The incident arose from a blurred authority boundary. The RCA must explain that boundary without becoming a second authority system. This architecture applies the existing standard-repository model: formal artifacts under `docs/engineering/` govern the bounded publication work, while the retrospective under `docs/rca/` remains supporting documentation.

## Components and responsibilities

- `docs/engineering/root-cause-analysis/` owns formal intent, definition, architecture assessment, verification, and work authorization for publishing the RCA.
- `docs/rca/` owns the human-readable retrospective and contains no formal lifecycle metadata.
- GitHub issue #81 tracks recommendations but grants no implementation authority.
- Immutable Git commits, Actions runs, GitHub releases, and PyPI distributions provide technical observations referenced by the RCA.
- The released external evaluator validates formal structure and preflight; candidate source and packages remain evidence only.

## Dependency direction

The approved formal chain may authorize creation and review of the RCA. The RCA may cite formal artifacts and evidence but cannot change their state or authorize later work. Issue #81 may link the RCA and future governing packets; neither the issue nor RCA is upstream authority for those packets.

## Data and control flow

`incident evidence -> accountable causal review -> approved WO-RCA-001 -> RCA implementation and retained evidence -> reviewed candidate -> separately authorized PR -> merged supporting document -> separately governed prevention work`

## Trust boundaries

- Candidate code, candidate packages, source prose, public APIs, and workflow output are untrusted observations until reconciled.
- Only the released `0.5.0a1` evaluator outside the checkout provides root validation evidence for this work.
- Human owners retain product, technical, assurance, engineering, commit, PR, and merge decisions.
- The emergency bypass is historical context and grants no continuing authority.

## Required patterns

- Separate formal governing artifacts from retrospective prose.
- Use immutable identities for material evidence.
- Label completed controls, recommendations, and residual uncertainty independently.
- Require later preventive changes to name their own approved work orders.
- Preserve historical facts and abandoned drafts without silent lifecycle transitions.

## Prohibited patterns

- Formal TOML front matter or lifecycle status in the RCA.
- Treating issue #81, the RCA, a workflow result, or a public package as approval authority.
- Candidate-source or candidate-package execution as the root evaluator.
- Code, workflow, managed-template, release-record, package, tag, or deployment changes in this work order.
- Reintroducing self-hosting data or a repository-specific installation profile.

## Quality attributes

- **Auditability:** material facts connect to exact immutable evidence.
- **Clarity:** the primary cause is distinct from contributing factors.
- **Safety:** the retrospective cannot be confused with lifecycle authorization.
- **Durability:** the record remains readable without private conversation history or generated tooling.
- **Minimality:** the change is documentation-only and preserves product/runtime boundaries.

## Conformance checks

- Validate the complete formal graph with released `0.5.0a1`.
- Inspect the RCA for required sections, exact identities, non-authority wording, and absence of formal front matter.
- Reconcile public links and distribution hashes.
- Inspect changed paths and prove no executable, managed, workflow, release, or package surface changed.
- Run start and review preflight at their phase-appropriate lifecycle states.

## Related ADRs

No ADR is proposed. This architecture applies the existing standard-repository and authority boundaries without introducing or changing a controlled significant-decision trigger. The accountable technical owner must accept this assessment before approval.
