+++
id = "REQ-RLO-014"
type = "requirement"
title = "Replay the bound recipe before release approval"
status = "approved"
owners = ["quality-owner", "release-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN a ready se_harness release record is proposed for approval, THE SYSTEM SHALL replay its exact bound build recipe in a hosted no-credential lane and require the rebuilt wheel and normalized sdist to equal both the accepted bytes and the release-record hashes."
verification_method = "hosted-exact-recipe-replay"

[relations]
derives_from = ["CAP-RLO-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T12:01:04Z"
decided_by = "release-owner"
+++

# Requirement: Replay the bound recipe before release approval

## Rationale

Two builds in one ad hoc environment prove only local consistency. Release approval needs an independent hosted observation that consumes the same recorded producer recipe and reproduces the already accepted bytes without replacing their hashes.

## Preconditions and trigger

One `ready` RLS on the selected review ref binds a recipe-bearing distribution and exact candidate commit. The candidate and recipe bytes are reachable from that ref. An accountable operator dispatches the repository-owned pre-release replay using only the RLS identifier; the ref selection is supplied by the hosting platform, not copied into release identity.

## Required response

Resolve the candidate, recipe, accepted wheel and sdist hashes, epoch, and output names from the ready RLS and candidate tree. In a job with read-only repository permission and no publication environment, secret, write permission, or OIDC permission:

1. validate the complete ready RLS and recipe binding;
2. create two fresh producer instances from the exact immutable image and architecture;
3. install and prove the complete hash-locked toolchain;
4. export the exact candidate twice;
5. execute the recipe commands with only the declared environment;
6. compare both wheel and normalized-sdist outputs byte-for-byte with each other and by SHA-256 with the accepted RLS identities; and
7. retain a bounded machine-readable replay result containing the candidate, recipe digest, observed producer/toolchain identity, commands, output hashes, and pass/fail state.

The production publication qualifier must use the same repository interpreter and recipe contract for recipe-bearing records. It may keep a visibly separate legacy path only for already released schema-1 history.

## Failure and boundary behavior

Any record, recipe, image, platform, Python, tool inventory, environment, command, normalization, source, filename, or output mismatch fails before release approval or external mutation. The lane must not update accepted hashes, edit the RLS, create a tag or release, publish, deploy, or exercise a lifecycle decision.

Failure to start the exact producer is a failed replay, not permission to fall back to the host runner. Hosted evidence from a different candidate, recipe digest, or RLS is ineligible.

## Constraints

- The pre-release lane accepts one RLS identifier and derives all build identity from it.
- The selected RLS may be `ready`; the lane does not require or imply `released`.
- Candidate code runs only inside the no-credential boundary.
- Native Linux and Windows publication-path parity is deliberately deferred to GitHub issue #111. This requirement establishes one canonical producer replay, not the later cross-platform rehearsal matrix.
- Historical schema-1 publication replay remains available and clearly labeled legacy; new records cannot use it.

## Acceptance examples

### Example: normal behavior

**Given** a ready schema-2 RLS whose recipe and accepted hashes match its candidate

**When** the hosted pre-release lane is dispatched for that RLS

**Then** two fresh recipe executions reproduce the exact accepted wheel and normalized sdist and retain one candidate- and recipe-bound pass result.

### Example: failure behavior

If a direct or transitive tool changes, an inherited variable reaches the build, the image digest differs, or either rebuilt byte stream differs, the lane fails and retains the mismatch without changing any formal or external state.

## Open decisions

None. Native host-runner parity and publication cleanup behavior remain the separately governed scope of issue #111.
