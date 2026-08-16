+++
id = "INT-WAC-001"
type = "intent"
title = "Make commit-bound assurance applicability explicit"
status = "approved"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
+++

# Intent: Make commit-bound assurance applicability explicit

## Problem

Every work order defines implementation checks and retained evidence, but the graph does not state whether the resulting candidate must receive commit-bound assurance through a VREC. Inspection therefore cannot distinguish forgotten assurance from governance-only work that correctly stops at `implemented`. Treating every implemented work order as pending verification would report historical approval, publication, and VREC-transition work as false assurance debt and would encourage recursive verification of verification decisions.

## Desired outcomes

- The accountable applicability decision is explicit before bounded execution begins.
- Every work order still carries verification contracts and retained implementation evidence.
- Inspection identifies required commit-bound assurance that has not yet reached a VREC proposal.
- Governance-only work can stop honestly at `implemented` without appearing incomplete.
- A ready VREC continues to require a separate human assurance decision.
- Existing completed artifacts remain valid without date heuristics or inferred retroactive decisions.

## Actors and stakeholders

- Assurance and repository owners decide whether commit-bound assurance is required.
- Engineering owners and coding agents execute the declared boundary but cannot grant an exemption.
- Reviewers use inspection to find assurance follow-up without treating suggestions as authority.
- Release owners continue to rely on exact VREC and release-record coverage rather than the declaration alone.

## Success measures

| Measure | Baseline | Target | Observation window |
| --- | ---: | ---: | --- |
| explicit classification in newly actionable work orders | not represented | 100% | each start preflight |
| implemented required work without a VREC proposal visible to inspection | 0 visible | 100% visible | each inspection |
| governance-only work falsely reported as requiring VREC creation | unbounded if inferred by status | 0 when explicitly classified | regression suite |
| automatic assurance decisions | 0 | 0 | continuous |

## Non-goals

Bulk-classifying historical work orders, changing VREC or release semantics, deciding whether a specific future work order is release-bearing, enforcing retained-evidence completeness beyond existing controls, transitioning work orders automatically, or implementing general artifact-schema versioning.

## Principles and immutable constraints

- Validation evidence is required for every work order; the declaration controls only the additional VREC obligation.
- Absence is never interpreted as `not_required` for work selected for new execution.
- `not_required` is an accountable exception, not an agent convenience.
- A suggestion may identify a possible next step but cannot select aggregate scope, create authority, or transition state.
- If a work order mixes assurance-bearing product change with governance transport, split it or classify the whole work order as required.

## Risks and assumptions

The principal risk is semantic misuse of `not_required`. Clear decision rights, mandatory rationale, preflight visibility, and focused tests reduce but cannot eliminate dishonest human classification. Completed legacy records without the declaration remain intentionally unclassified rather than guessed.
