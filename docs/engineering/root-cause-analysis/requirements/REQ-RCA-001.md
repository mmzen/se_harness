+++
id = "REQ-RCA-001"
type = "requirement"
title = "Publish one complete canonical incident analysis"
status = "approved"
owners = ["product-owner", "repository-owner"]
created = "2026-08-20"
updated = "2026-08-20"
statement = "WHEN the 0.5.0 governance incident is documented for repository maintainers, THE REPOSITORY SHALL provide one canonical Markdown RCA covering impact, detection, root cause, contributing factors, recovery, corrective actions, preventive actions, evidence, and lessons."
verification_method = "static-inspection-and-manual-review"

[relations]
derives_from = ["CAP-RCA-001"]
+++

# Requirement: Publish one complete canonical incident analysis

## Rationale

Fragmented notes cannot provide a stable shared understanding of the incident or its recovery. One structured document makes omissions and contradictions reviewable.

## Preconditions and trigger

- The emergency recovery and final public verification are complete.
- Exact commits, workflow runs, public releases, and distribution hashes are available for inspection.
- The RCA is being prepared for repository publication, not used as release authority.

## Required response

The repository provides exactly one incident-specific Markdown file at `docs/rca/2026-08-20-0.5.0-release-governance-deadlock.md`. It contains an executive summary, impact, detection, explicit root cause, five-whys chain, contributing factors, recovery timeline, risk controls, what worked, completed actions, recommended actions, release evidence, and lessons.

## Failure and boundary behavior

- Missing required sections, contradictory causal claims, or unresolved material facts block review readiness.
- The document must not dilute the primary cause into an unprioritized list of contributing factors.
- The document must not assign personal blame or infer intent unsupported by evidence.

## Constraints

- Use concise Markdown readable without generated tooling.
- Preserve exact identifiers and distinguish completed from recommended work.
- Do not embed secrets, local credentials, private conversation content, or transient filesystem paths.

## Acceptance examples

### Example: normal behavior

**Given** the public release and recovery evidence is available

**When** a maintainer opens the canonical RCA

**Then** the maintainer can identify the primary architectural cause, follow the recovery chronology, and distinguish completed safeguards from proposed follow-up.

### Example: failure behavior

**Given** a retrospective lists several contributing factors

**When** it does not identify the product/evaluator conflation and circular self-hosting dependency as the root cause

**Then** the RCA is not ready for approval or publication.

## Open decisions

None. Wording may be refined during accountable review without changing the required causal meaning or section coverage.
