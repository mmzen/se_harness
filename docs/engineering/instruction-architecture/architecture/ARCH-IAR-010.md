+++
id = "ARCH-IAR-010"
type = "architecture"
title = "Role-aware temporal finding classification"
status = "implemented"
owners = ["technical-owner", "engineering-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
addresses = ["REQ-IAR-018"]
conforms_to = ["SPEC-IAR-010"]

[decision_assessment]
outcome = "adr_required"
triggers = ["cross-cutting-policy", "responsibility-or-dependency-direction", "public-interface-or-protocol", "material-alternatives"]
rationale = "The correction changes a public finding's trigger semantics and must separate mutable dependency review from immutable provenance without moving rule authority into inspection presentation."
assessed_by = "technical-owner"
+++

# Architecture: Role-aware temporal finding classification

## Lifecycle

Approved on 2026-08-16 through the repository owner's implementation instruction; `ADR-IAR-010` records the accountable design choice.

## Context and scope

Harness Explorer owns the derived finding snapshot reused by `dashboard` and `inspect`. The current generic date loop ignores artifact role, lifecycle, relation meaning, and declared-versus-derived authority. The correction belongs in that single producer so every presentation receives the same finding.

## Components and responsibilities

- **Temporal policy constants:** define supported source-type/relation pairs and terminal work-order states as reviewed code, not repository input.
- **Eligibility predicate:** decides whether one existing relation has temporal reassessment meaning.
- **Finding producer:** compares eligible source and target dates and emits `W-HEX-003` with relation evidence.
- **Inspection projector:** continues to display the snapshot and apply the already governed suggestion catalog without recreating the predicate.
- **Distribution boundary:** keeps root and canonical generator sources and integrity metadata equal.

## Dependency direction

```text
declared artifact relation
          |
          v
typed eligibility predicate ---> date comparison ---> W-HEX-003
                                                        |
                              +-------------------------+------------------+
                              v                                            v
                         dashboard                                    inspect
```

The projector depends on the finding producer; the producer never depends on presentation or suggestion code.

## Trust and authority boundary

Artifact type, status, relation name, authority, and normalized dates are data. The allowlist is implementation-owned policy. Titles and prose cannot select a rule. The resulting warning is observational and cannot mutate lifecycle state or historical provenance.

## Required patterns

- One explicit fail-closed predicate before date comparison.
- No duplicated trigger logic in `inspect`.
- Focused positive and negative fixtures independent of the current repository snapshot.
- Root/canonical equality and deterministic output.

## Prohibited patterns

- Blanket comparison of all graph relations.
- Treating a derived projection as a declared dependency.
- Reopening completed work or commit-bound records through generic staleness advice.
- Inferring new provenance or lifecycle rules from dates.

## Related ADR

`ADR-IAR-010` selects a typed, fail-closed predicate over blanket comparison, post-processing suppression, and immediate provenance redesign.
