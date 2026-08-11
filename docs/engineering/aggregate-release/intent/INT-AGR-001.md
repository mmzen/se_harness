+++
id = "INT-AGR-001"
type = "intent"
title = "Make a software version an auditable aggregate release"
status = "approved"
owners = ["product-owner", "quality-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
+++

# Intent: Make a software version an auditable aggregate release

## Problem

The harness can bind verification and release records to an exact commit, but its preparation commands currently accept only one work order and one verification record. A real software version commonly combines multiple independently governed implementation items. Selecting only the latest work order understates release scope, while adding every work order to a release contract merely broadens an allow-list and does not make the release record aggregate them.

## Desired outcomes

- A release owner can see every release-bearing work order intentionally included in a version.
- Assurance can verify the combined behavior at one final candidate commit.
- The release contract, aggregate verification, release record, tag, and wheel agree on scope and commit.
- Governance-only activities remain auditable without being misrepresented as shipped product work.
- Existing single-work-order workflows remain valid.

## Actors and stakeholders

Product and engineering owners define release-bearing work. Quality owners assess aggregate evidence. Release owners authorize promotion. Repository operators create tags and publish packages only after authorization. Consumers rely on the version and provenance claims.

## Success measures

| Measure | Baseline | Target | Observation window |
|---|---:|---:|---|
| Release preparation commands that can enumerate more than one work order | 0 | 100% | implementation verification |
| Released work orders without aggregate verification coverage | possible | 0 | every graph validation |
| Aggregate release records with commit disagreement | rejected | rejected deterministically | every graph validation |
| Existing single-work-order CLI scenarios passing | supported | 100% | every regression run |

## Non-goals

- Automatically infer release scope from Git history, paths, pull requests, or artifact status.
- Treat publication, approval, or verification-transition work orders as release payload.
- Accept ancestor commits as proof of final integrated behavior.
- Create commits, tags, approvals, releases, or published packages.

## Principles and immutable constraints

Release scope is explicit. One release instance names one exact candidate commit. Evidence and authority are separate. Governance records may be committed after the candidate they name. Target repository content remains untrusted, and existing customization-preservation rules remain unchanged.

## Risks and assumptions

The primary risk is a superficially complete manifest whose work, verification, and release sets differ. Deterministic set-consistency rules and final-candidate verification mitigate that risk. The design assumes accountable owners can distinguish product work from governance-only activity.
