+++
id = "ARCH-PMI-001"
type = "architecture"
title = "Single integrity boundary for managed text"
status = "implemented"
owners = ["engineering-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
constrains = ["SPEC-PMI-001"]
+++

# Architecture: Single integrity boundary for managed text

## Context and scope

Installer lock writing, upgrade classification, and doctor currently consume raw SHA-256 values at separate call sites. Portable integrity requires one semantic boundary so a change to newline handling cannot leave stale or contradictory digests.

## Components and responsibilities

- **Integrity component:** validates schema and mode, canonicalizes strict UTF-8 text, hashes tracked content, and returns typed comparison outcomes.
- **Fragment boundary component:** extracts only uniquely marked managed blocks before delegating bytes to integrity logic.
- **Installer and upgrade planner:** render desired templates, request integrity comparisons, preserve customizations, apply validated plans atomically, and request complete schema-2 lock generation.
- **Doctor:** reads lock evidence, delegates comparisons, and renders bounded read-only diagnostics.
- **Distribution verification:** asserts source/canonical parity, self-lock consistency, wheel contents, and fresh-install behavior.

## Dependency direction

CLI orchestration, installer, upgrade, and doctor depend inward on the integrity component. The integrity component depends only on standard-library hashing, JSON-neutral data, and supplied bytes; it does not depend on CLI parsing, Git, filesystem traversal, artifact bodies, or lifecycle logic.

## Data and control flow

1. A caller resolves and bounds a target path through existing safety controls.
2. The caller reads tracked bytes or extracts the managed fragment.
3. The integrity component interprets the recorded schema/mode and returns exact, canonical, customized, or invalid state.
4. Read-only commands render the state. Mutating commands first validate the complete plan, apply safe file operations, then atomically write a complete schema-2 lock.

## Trust boundaries

Target files and locks are untrusted inputs. They may contain malformed UTF-8, unsafe paths, invalid JSON, forged modes, duplicate markers, or large content. No target content executes, and diagnostics never reproduce bodies.

## Required patterns

- One canonical digest implementation used by producers and consumers.
- Explicit schema and hash-mode dispatch.
- Strict UTF-8 and exact line-terminator normalization.
- Typed outcomes rather than boolean fall-through for legacy cases.
- Atomic complete-lock replacement only after successful file application.
- Deterministic tests at helper, command, repository, and wheel boundaries.

## Prohibited patterns

- Raw `sha256(path.read_bytes())` at managed-integrity call sites outside the shared component.
- Global whitespace, Unicode, or case normalization.
- Editing `.gitattributes` or user Git configuration as the integrity mechanism.
- Treating arbitrary schema-1 mismatches as canonical matches.
- Rewriting customized content or locks during doctor.
- Mixing lifecycle transition, release, or publication authority into integrity results.

## Quality attributes

Portability, determinism, explainability, conservative migration, customization safety, standard-library operation, and auditability take precedence over maximizing automatic migration.

## Conformance checks

Static search for unmanaged hash call sites; unit properties for canonicalization; command integration tests for all lock states; path/fragment/security regressions; source/canonical byte parity; self-doctor; wheel inspection; and fresh LF/CRLF installation checks.

## Related ADRs

`ADR-PMI-001` selects a versioned canonical UTF-8 LF digest and explicit schema-2 migration instead of Git-policy enforcement or implicit raw-hash reinterpretation.
