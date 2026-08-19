+++
id = "INT-EVK-001"
type = "intent"
title = "Preserve trustworthy evidence attribution across repository layouts"
status = "approved"
owners = ["product-owner", "quality-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[relations]
+++

# Intent: Preserve trustworthy evidence attribution across repository layouts

## Problem

SE Harness requires retained evidence keyed to work-order IDs, but current implementations recognize the key only at the start of the evidence filename. A repository that uses one directory per work order, such as `evidence/WO-MOK-001/check.md`, can retain complete committed evidence and bind those exact paths in a verification record while `capture-verification`, formal validation, inspection, and Harness Explorer report different or incorrect attribution outcomes.

Renaming established evidence is not a safe general remedy. Verification records retain exact repository-relative paths and bind them to candidate commits, so rewriting historical evidence or records would weaken rather than restore provenance. Extending the same filename-only assumption to single-work-order records would make the incompatibility more severe.

## Desired outcomes

- Existing flat filenames and directory-per-work-order layouts receive correct, deterministic attribution.
- Capture, validation, inspection, and Harness Explorer agree on the work-order keys carried by a path.
- Existing evidence files, verification records, release records, and candidate bindings remain unchanged.
- Expanded attribution does not weaken containment, normalization, symlink, regular-file, or untrusted-input controls.
- Standalone repository-local scripts remain independent from candidate package code while their observable behavior stays aligned.

## Actors and stakeholders

- Repository engineers organize and retain implementation evidence.
- Quality and assurance owners assess evidence and exact candidate provenance.
- Engineering owners prepare aggregate verification proposals.
- Technical and security owners govern path semantics and execution-plane boundaries.
- Maintainers distribute one portable standard installation to consumer repositories.

## Success measures

| Measure | Baseline | Target | Observation window |
|---|---:|---:|---|
| Harness surfaces recognizing `evidence/WO-ID/file` | 0 of 4 | 4 of 4 | focused acceptance run |
| Existing flat-layout regression cases preserved | current suite | 100% | complete regression run |
| Shared attribution contract cases agreeing across execution planes | not explicit | 100% | every CI run |
| Historical evidence or VREC/RLS paths rewritten | 0 | 0 | implementation review |
| New path-safety exceptions introduced | 0 | 0 | security verification |

## Non-goals

- Enforcing keyed evidence for single-work-order VRECs; that is separately governed by issue 49.
- Judging whether evidence content is sufficient, correct, or worthy of verification.
- Renaming consumer evidence or automatically migrating repository-owned records.
- Changing lifecycle, release, publication, governor, or operating authority.
- Adding installation profiles, runtime dependencies, or new formal artifact types.

## Principles and immutable constraints

- Formal artifacts and accountable decisions retain authority; evidence presence remains an observation.
- Historical commit-bound records are immutable facts and are not rewritten to follow a newer convention.
- Existing accepted flat filenames remain valid.
- Repository paths and content remain untrusted and must pass existing independent safety checks.
- Repository-local validation must remain standard-library-only and independently executable.
- Candidate source and packages do not replace the exact released self-hosting governor.

## Risks and assumptions

- A loose search of every ancestor component could create false attribution; matching must be explicitly bounded to the current filename or descendants of a literal `evidence` component.
- Multiple exact work-order keys may occur in one explicit path. The proposed specification associates the path with every unique exact key rather than allowing tools to choose different components.
- The active aggregate and Explorer definitions previously named a filename-only convention; `WO-EVK-001` reconciles them to the approved evidence-path convention before implementation completion.
- Resolving this packet before single-work-order enforcement is assumed to be the safest compatibility sequence.
