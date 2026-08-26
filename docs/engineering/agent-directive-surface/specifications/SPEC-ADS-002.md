+++
id = "SPEC-ADS-002"
type = "specification"
title = "Closed reading manifest, minimal operating card, and owner region without the retired context file"
status = "approved"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
specifies = ["REQ-ADS-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T11:40:02Z"
decided_by = "technical-owner"
+++

# Specification: Closed reading manifest, minimal operating card, and owner region without the retired context file

## Scope

This specification refines `SPEC-ADS-001` rules `ADS-RDM-001` and
`ADS-RDM-002` and replaces the pointer clauses of `SPEC-IAR-012` (rules 3-4
and the `REPOSITORY_CONTEXT.md` failure case). Every other rule of both
specifications stands.

## Behavioral rules

**ADS-RDS-001:** `se_harness.preflight` derives the reading manifest from a
`READING_PATHS` tuple `("ENGINEERING_HARNESS.md", "docs/engineering/OPERATING_CARD.md", "AGENTS.md")`
followed by the selected chain in the existing artifact order. `POLICY_PATHS`
remains the installation check set and no longer prefixes the manifest.

**ADS-RDS-002:** `render_operating_card` emits, in order: a two-line header
naming the contracts and `harnessctl` as the only legality oracle; `## Stop when`
with the router's stop conditions; `## Traps` with the managed trap list. The
bound is 1,024 bytes. The conformance test compares bytes with the template.

**ADS-RDS-003:** The router's `Scope of these obligations` section keeps its
wording; the card sentence reads "read `docs/engineering/OPERATING_CARD.md`,
the selected work order, and every governing artifact listed by the phase
reading manifest".

**ADS-RDS-004:** The owner region of this repository's `AGENTS.md` replaces
its context-file paragraph with one sentence naming
`docs/notes/developing-se-harness.md#release-sequences`. The region stays
under 6,000 bytes and carries every other `REQ-IAR-020` fact.

**ADS-RDS-005:** `docs/notes/developing-se-harness.md` gains a
`## Release sequences` section carrying the build, release-preparation,
authorized-last-mile, and maintenance-line paragraphs verbatim from the
retired file. `docs/engineering/REPOSITORY_CONTEXT.md` and its line in
`docs/engineering/README.md` are removed.

**ADS-RDS-006:** `REQ-IAR-020` transitions to `superseded` in the same work
order, with its body unchanged, following the `REQ-DST-008` precedent.
`REQ-ADS-007` is the active successor.

**ADS-RDS-007:** Tests follow the rules: `REQUIRED_OWNER_CONTENT` names the
note anchor instead of the retired path; the retirement inventory lists only
historical records and the migration note; the manifest-prefix assertion
compares against `READING_PATHS`; the card test asserts the two sections and
the bound.

## Failure behaviour

Every rule fails closed through its conformance test. No rule creates,
changes, or infers lifecycle state; the `REQ-IAR-020` transition is an
explicit applied transition by the requirements steward.
