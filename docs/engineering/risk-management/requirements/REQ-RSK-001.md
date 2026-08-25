+++
id = "REQ-RSK-001"
type = "requirement"
title = "Provide the risk artifact and its score"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN a formal artifact of type risk exists under docs/engineering/<domain>/risks/, THE SYSTEM SHALL validate its identity, a [risk] table carrying category, stage, raised_by, likelihood and impact on a 1-5 scale, the computed score equal to likelihood times impact, the acceptance_level copied at raise time, cause and effect, and its typed relations, and SHALL reject any risk whose score or stage is inconsistent with its fields or targets."
verification_method = "automated-test"
[relations]
derives_from = ["CAP-RSK-001"]
+++

# Requirement: Provide the risk artifact and its score

## Rationale

A risk must be a formal artifact with a stable identity and declared
relations so that traceability (`TRC-001`) and lifecycle authority apply to
it as to every other artifact. The score is computed, never asserted, so
that raising cannot be gamed by editing a number.

## Preconditions and trigger

Validation of a repository containing at least one `risk` artifact.

## Required response

- Type `risk`, prefix `RISK-`, canonical directory `risks/` under a domain.
- `[risk]` fields: `category` in {safety, security, compliance, process,
  schedule, quality}; `stage` in {definition, architecture, implementation,
  verification, release, operation}; `raised_by`; `likelihood` and `impact`
  integers 1-5; `score`; `acceptance_level`; `cause`; `effect`.
- `score == likelihood * impact` (5x5 scale); a mismatch is a structure error.
- `stage` matches the type of every `threatens` target (definition: INT, CAP,
  REQ; architecture: SPEC, ARCH, ADR; implementation: WO; verification: VER,
  VREC; release: REL, RLS; operation: OPS); a mismatch is a governance error.
- Optional `residual_likelihood` and `residual_impact`, required once the
  risk is `mitigated`.

## Failure and boundary behavior

A malformed risk is an error on the plane named above; it never passes
silently. Risks are optional per domain; a domain with none is valid.

## Constraints

No change to any other artifact type's schema.

## Acceptance examples

### Example: normal behavior

**Given** `RISK-X-001` with likelihood 4, impact 3, score 12, stage
implementation, threatens `WO-X-001`

**When** the validator runs

**Then** it passes.

### Example: failure behavior

**Given** the same risk with score 11

**When** the validator runs

**Then** it reports a structure error naming the computed score.

## Open decisions

None. The scale is 5x5 by owner decision on 2026-08-25.
