+++
id = "ADR-AEX-005"
type = "adr"
title = "Repository-scoped host adapters over one canonical skill core"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
decides = ["ARCH-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T16:49:43Z"
decided_by = "technical-owner"
+++

# ADR: Repository-scoped host adapters over one canonical skill core

## Status

Proposed.

## Context

Phase 3 deliberately implemented provider-neutral single-agent skills without
runtime adapters. The canonical packages are installed under `.agents/skills`,
which Codex discovers directly. Claude Code uses `.claude/skills`, so it does
not discover those packages in a standard installed repository.

The writing skills are explicit-only. Codex and Claude Code expose different
native controls for implicit invocation. A solution must make the skills
visible to both hosts and preserve that activation rule without turning two
provider copies into separate workflow authorities.

This is a narrow availability decision. It does not implement the roadmap's
future worker-profile adapters, autonomy-envelope effect admission, subagent
orchestration, or runtime permission enforcement.

## Decision drivers

- Keep exactly one authoritative procedure and script set for each skill.
- Make fresh and upgraded managed repositories usable from Codex and Claude
  Code without per-session copying or user-home installation.
- Represent explicit-only writing activation with supported host controls.
- Preserve safe package installation and ownership-aware upgrades on Windows
  and POSIX.
- Keep provider configuration non-authoritative and replaceable.
- Preserve the exact `harness-orient` v1 core.
- Fail visibly when discovery metadata and canonical content drift.

## Considered options

### Option A — duplicate the complete skill under both discovery roots

Store complete copies under `.agents/skills` and `.claude/skills`.

This is easy for each host to discover, but it creates two workflow bodies,
two script sets, and two portable identities that can drift or be reviewed
differently.

### Option B — link Claude skill directories to `.agents/skills`

Create symbolic links from `.claude/skills/<name>` to the canonical directory.

Both hosts document link support, but repository checkout, Python wheel, and
Windows privilege behavior is not reliably portable. The existing portable
core contract also rejects links and reparse points.

### Option C — install global user or provider plugins

Place skills in user-wide host directories or distribute provider plugins.

This makes the skills available outside managed repositories, where their
required lock and evaluator may not exist. It also introduces provider plugin
namespaces, separate update channels, and external installation effects before
the repository-scoped MVP is proven.

### Option D — keep canonical `.agents` cores and add thin repository adapters

Keep one complete managed skill core under `.agents/skills`. Codex discovers
that core directly. Add Codex activation metadata only where required. Install
one Claude `SKILL.md` adapter per skill under `.claude/skills`; it contains
Claude discovery and activation metadata and directs Claude to load the exact
same-named canonical core and resolve every resource there.

This preserves one workflow source while using each host's supported discovery
surface.

## Decision

Choose Option D, subject to approval of `REQ-AEX-009`, `SPEC-AEX-005`,
`VER-AEX-003`, and `WO-AEX-004`.

The standard installation remains repository-scoped. Each canonical skill
continues to live at `.agents/skills/<skill-name>/`. Codex uses that location
directly. Each writing core receives bounded Codex invocation metadata that
disables implicit invocation; the read-only `harness-orient` core and v1
identity remain unchanged.

Claude Code receives a managed `.claude/skills/<skill-name>/SKILL.md` adapter.
The adapter contains no copy of the canonical procedure, contract, or script.
It identifies the same-named canonical repository path, establishes the
provider-native invocation policy, requires the complete canonical core to be
loaded, and stops on any missing or invalid binding. Relative procedure
resources resolve from the canonical directory, not the adapter directory.

The three writing adapters disable model invocation and remain explicitly
user-invocable. The `harness-orient` adapter permits normal read-only matching.
Provider metadata does not grant tools, select models, spawn subagents, inject
shell commands, widen repository permissions, or change a harness decision.

The source and wheel may contain canonical cores plus thin host adapters, but
there remains exactly one authoritative body and script set per skill. Every
installed file is ownership-aware and lock-managed. Installation and upgrade
remain atomic, and customized destinations block rather than being overwritten.

## Consequences

### Positive

- Both target hosts discover the same four repository workflows by default
  after an applicable install or upgrade.
- Provider-specific activation controls reinforce the portable explicit-only
  contract for writing skills.
- Skill procedures, contracts, scripts, evaluator checks, and decision stops
  remain centralized.
- Claude adapters are small enough to inspect and test as deterministic
  mappings.
- Repository scope avoids presenting harness-dependent workflows where no
  harness is installed.

### Negative

- Package and managed-lock inventories gain provider-specific files.
- The three writing-core manifests change when Codex policy metadata is added
  and therefore require explicit identity updates and new vectors.
- Actual host behavior must be tested in addition to static package tests.
- A compliant host still executes instructions procedurally; this does not
  create hard enforcement against a hostile runtime.

### Operational

- New top-level discovery directories may require a fresh host session before
  they appear.
- Existing repositories receive the surfaces only through an explicitly
  authorized safe upgrade.
- A later public release is required before public `harnessctl` installs the
  merged candidate behavior by default.
- Global or plugin distribution remains a separate opt-in decision after the
  repository-scoped path is proven.

### Security

- Adapter paths are fixed, repository-relative, same-named, and non-escaping.
- Adapters grant no tools, credentials, network access, model choice, hooks, or
  external action.
- The canonical skill repeats exact evaluator identity, integrity, state, and
  scope checks; adapter discovery cannot substitute for those checks.
- Customized or malformed provider files fail installation or invocation
  without inferred fallback.

### Migration

- Preserve `harness-orient` v1 bytes and digest.
- Version and rebind the three writing cores if their manifests gain Codex
  metadata.
- Add Claude adapters as new managed files; do not migrate or overwrite an
  owner-created `.claude` surface ambiguously.
- Leave published 0.6.0 unchanged. Carry this behavior only in a later
  qualified package and explicit repository upgrade.

## Validation

`VER-AEX-003` verifies package inventory, canonical uniqueness, adapter
mapping, explicit-activation parity, nested-directory discovery, actual-host
listing and invocation, hostile and customized-path failures, safe upgrade,
unchanged `harness-orient` identity, and command/skill behavioral equivalence.
Applicable `VER-AEX-001` and `VER-AEX-002` checks remain required for authority,
portability, evaluator boundaries, and Phase 3 workflow behavior.
