+++
id = "INT-HUP-003"
type = "intent"
title = "Make governor succession repeatable across released versions"
status = "approved"
owners = ["repository-owner", "engineering-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T20:22:49Z"
decided_by = "repository-owner"
+++

# Intent: Make governor succession repeatable across released versions

## Problem

The 0.6.0 root candidate correctly replaced the configured 0.5.0 governor, but
hosted CI still treated the current checkout as a 0.5.0 predecessor root. A
separate source test also inferred evaluator-role separation from raw byte
inequality and therefore passed on a CRLF checkout while failing on canonical
LF. Hard-coding 0.6.0 into those checks would repair this candidate but repeat
the same failure at the next governor upgrade.

## Desired outcomes

- Ordinary CI validates the repository with its exact currently locked
  governor.
- A governor-changing candidate is assessed through one version-independent
  transition lane using trusted base identity, approved target identity, and
  canonical transaction evidence.
- The predecessor governor is never asked to validate the successor root.
- Historical predecessor behavior remains immutable evidence or an explicit
  fixture, not an always-on interpretation of the current checkout.
- Tests distinguish evaluator roles by lock, origin, path, and authority rather
  than requiring their canonical bytes to differ.

## Actors and stakeholders

- Repository owner: approves the exact transition and target identity.
- Engineering owner: implements and qualifies the bounded CI change.
- Quality owner: assesses cross-platform and hosted evidence.
- Security owner: reviews base/target trust, archive identity, and credential
  isolation.

## Success measures

| Measure | Baseline | Target | Observation window |
| --- | ---: | ---: | --- |
| Hard-coded predecessor versions in the transition assessment | 1 | 0 | corrected candidate |
| Current checkout evaluated as a superseded root | 1 hosted failure | 0 | push and pull-request runs |
| Raw-byte role-separation assertions | 1 failing on LF | 0 | Linux and Windows qualification |
| Future upgrade code changes outside identity/evidence data | required | not required | next governor upgrade rehearsal |

## Non-goals

This intent does not change `se_harness` product or candidate templates,
rewrite 0.6.0 release history, restore a permanent compatibility view, publish
or deploy anything, change branch protection, or decide `VREC-HUP-003`.

## Principles and immutable constraints

- Never download or execute an unverified "latest" evaluator.
- Do not trust target version or hashes merely because they appear in a pull
  request; bind them to the approved upgrade work order and canonical evidence.
- Preserve the managed Engineering Harness workflow as the ordinary current-
  governor gate.
- Preserve checkout immutability and credential-free assessment.

## Risks and assumptions

- GitHub push and pull-request events expose base revisions differently; the
  resolver must fail closed when it cannot establish one exact base.
- The target public wheel must remain available by exact version and digest.
- Required-check continuity must be verified before renaming or deleting any
  workflow or job.
