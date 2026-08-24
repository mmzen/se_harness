+++
id = "REQ-AEX-009"
type = "requirement"
title = "Expose managed skills to supported repository agent hosts"
status = "approved"
owners = ["product-owner", "requirements-steward", "technical-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN a standard SE Harness repository is initialized, adopted, or explicitly upgraded with supported outcome skills, THE SYSTEM SHALL install managed repository-scoped discovery and activation surfaces that make the same authoritative skill cores available to Codex and Claude Code, preserve each skill's declared invocation policy and evaluator boundary, and fail without partial writes or duplicated workflow authority when a surface is missing, invalid, stale, or customized."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T16:49:43Z"
decided_by = "requirements-steward"
+++

# Requirement: Expose managed skills to supported repository agent hosts

## Rationale

Phase 3 packages four portable skill cores under `.agents/skills`, which is the
repository discovery location used by Codex. Claude Code discovers project
skills under `.claude/skills`, so the same installed repository does not
currently expose the MVP to both target hosts. The three writing skills also
declare explicit-only activation, but that declaration must be represented in
each host's supported activation mechanism rather than relying only on prose.

The repository needs a small host-availability layer before the MVP can be
tested as a user-facing workflow. That layer must not duplicate the skill
procedure, move lifecycle authority into provider configuration, or install
repository-dependent skills globally on an operator's machine.

## Preconditions and trigger

- The target is a standard SE Harness repository undergoing `init`, `adopt`, or
  an explicitly authorized ownership-aware upgrade.
- The candidate package contains valid managed cores for `harness-orient`,
  `harness-draft-change`, `harness-execute-work-order`, and
  `harness-prepare-assurance`.
- Codex and Claude Code are the initially supported repository hosts. A host is
  supported only for the versions exercised by the applicable verification
  contract.
- The target's exact released evaluator remains external to the checkout and
  authoritative for installed integrity and governed state.

## Required response

- Install each portable core once at `.agents/skills/<skill-name>/` as the
  authoritative managed procedure package.
- Make Codex discover those canonical repository cores directly.
- Install one managed thin discovery adapter at
  `.claude/skills/<skill-name>/SKILL.md` for each canonical core. The adapter
  may contain only Claude-specific discovery, activation, canonical-path, and
  fail-closed loading instructions; it must not copy the canonical workflow.
- Allow implicit or explicit invocation of the read-only `harness-orient`
  skill in both hosts.
- Disable host-initiated implicit invocation of each writing skill in both
  hosts while preserving explicit user invocation.
- Bind every adapter name and path to exactly one same-named canonical core and
  require the canonical contract, installed integrity, and evaluator checks
  before the procedure continues.
- Record canonical cores, host metadata, and Claude adapters as managed files
  in the repository lock. Apply their installation or upgrade as one atomic
  ownership-aware transaction.
- Package all required files in source and wheel distributions without adding
  a second authoritative skill body.
- Preserve owner content and stop before overwriting a customized managed
  core, host policy, or adapter.

## Failure and boundary behavior

- A missing, malformed, mismatched, escaping, case-colliding, or customized
  adapter fails installation or invocation without falling back to an inferred
  workflow.
- A Claude adapter that cannot load its exact canonical core stops before
  invoking a helper or changing repository state.
- A writing skill proposed through implicit matching performs no write and
  directs the operator to invoke the exact skill explicitly.
- Missing host-native discovery support is reported as unsupported or
  degraded; it does not change the canonical skill, lifecycle state, or
  authority model.
- An upgrade conflict leaves the complete prior installation and lock intact.
- Host availability, listing, or runtime permission is never presented as
  work approval, verification, release, or external-action authority.

## Constraints

- The default installation scope is the managed repository. User-wide,
  organization-wide, plugin-marketplace, cloud-account, or unrelated-repository
  installation is outside this requirement.
- No symbolic link, junction, hard link, or reparse-point dependency is used;
  supported package and repository behavior must remain portable across
  Windows and POSIX filesystems.
- Claude-specific front matter remains in the thin Claude adapter. Codex
  invocation policy remains bounded provider metadata. Neither becomes a
  second workflow or evaluator.
- The exact `harness-orient` v1 portable core and behavior remain unchanged.
- Any changed identity of a Phase 3 writing core is explicit, versioned, and
  covered by new canonical vectors and commit-bound evidence.
- The already published 0.6.0 distribution is immutable. Default availability
  through public `harnessctl` requires a separately governed later package
  version and does not follow merely from merging candidate source.

## Acceptance examples

### Example: fresh repository installation

**Given** a qualified candidate distribution containing the four canonical
skills and supported host adapters

**When** an operator initializes a standard repository

**Then** Codex and Claude Code each list the same four skill names from their
repository discovery locations, while the managed lock records one canonical
core and the applicable host surface for each name.

### Example: explicit writing invocation

**Given** both hosts discover `harness-draft-change`

**When** an operator explicitly invokes that exact skill in either host

**Then** the host loads the same canonical `.agents` core and the procedure
performs its normal contract, evaluator, state, and scope checks.

### Example: implicit writing match

**Given** an operator discusses a possible work-order implementation without
explicitly invoking `harness-execute-work-order`

**When** either host evaluates available skills

**Then** its host-native policy prevents implicit invocation and no writing
procedure or helper effect begins.

### Example: customized adapter during upgrade

**Given** a repository owner changed a managed Claude adapter after installation

**When** a later harness upgrade proposes a replacement

**Then** the ownership-aware plan reports the customization and writes none of
the canonical, adapter, or lock changes.

## Open decisions

Before approval, the specification and ADR must close the exact canonical-to-
host mapping, host-native activation policy, adapter content boundary, package
inventory, integrity checks, upgrade behavior, supported-host test method, and
migration from repositories that contain only `.agents/skills`.
