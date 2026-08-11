+++
id = "ARCH-DST-005"
type = "architecture"
title = "Metadata-authoritative domain authoring boundary"
status = "implemented"
owners = ["technical-owner", "quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
constrains = ["REQ-DST-015", "REQ-DST-016", "REQ-DST-017", "REQ-DST-018"]
+++

# Architecture: Metadata-authoritative domain authoring boundary

## Components and responsibilities

- **Canonical layout registry**: provides the single formal-type-to-relative-directory mapping, filename convention, reserved-domain rules, and repository-wide aggregate exceptions.
- **Safe authoring service**: validates and plans domain scaffolds and draft artifact creation, then performs bounded exclusive writes.
- **CLI adapters**: expose `scaffold-domain`, `create-artifact`, and domain selection for verification and release preparation without owning governance decisions.
- **Artifact parser and graph**: remain the sole source of artifact identity, type, relations, lifecycle consistency, and Explorer answers.
- **Layout diagnostic**: derives advisory actual-versus-expected path observations after successful metadata parsing.
- **Provenance router**: applies output, explicit-domain, common-domain, and repository-wide precedence before existing provenance serialization.
- **Installer and upgrader**: distribute managed guidance and templates while preserving repository-owned domain content under the lock contract.
- **Temporary-fixture tests**: represent new, canonical, legacy-flat, aggregate, malicious, and conflicting repositories without coupling to a live consumer.

## Dependency direction

```text
canonical layout registry ---> scaffold and artifact plans
canonical layout registry ---> provenance destinations
canonical layout registry ---> advisory expected paths
canonical templates --------> draft artifact renderer
safe-path primitives --------> all planned writes
parsed metadata ------------> graph authority and diagnostics
selected work-order paths ---> optional common-domain inference
managed distribution -------> fresh-install guidance and templates
repository ownership -------> domain indexes and product artifacts
```

Path layout is consumed by authoring and observation. It does not feed authority into the parsed graph.

## Trust and write boundaries

- Treat CLI path components and all repository directory entries as untrusted.
- Normalize and verify containment before opening a destination.
- Reject link, junction, non-directory, reserved-name, and existing-file conflicts.
- Validate the whole operation before mutation and use exclusive creation for new owner files.
- Never reuse upgrade's managed-file authority to mutate repository-owned artifacts.
- Do not infer owners, relations, product statements, approvals, verification outcomes, or release authority.

## State and control flow

```text
request
  -> parse explicit values
  -> resolve canonical mapping and complete destination plan
  -> validate grammar, prefix, containment, parents, links, and conflicts
  -> report dry run OR perform bounded exclusive write
  -> report created draft and required next validation
```

For provenance commands, routing completes before the established clean-tree, candidate-commit, selection, gating, and record-write flow. Only the default destination changes; record semantics and authority do not.

For validation, metadata is parsed first. The graph then performs its existing authoritative checks, while the layout diagnostic independently derives optional advisory observations from the same parsed artifact and source path.

## Compatibility boundary

Recursive discovery remains format-driven and path-agnostic. A legacy flat artifact and its canonical counterpart have identical graph meaning when their metadata is identical. The diagnostic may recommend a move, but it neither rewrites the path nor changes the validation result.

Repository-wide `verification-records/` and `releases/` remain architectural aggregation points for work spanning domains or lacking a safe single-domain attribution. Historical records are never reclassified or moved solely because newer routing is available.

## Required patterns

- One layout registry shared by authoring, provenance routing, diagnostics, tests, and documentation assertions.
- One template source per formal artifact type.
- Dry-run and write paths share destination resolution and safety validation.
- New domain content remains outside the managed distribution lock.
- Warnings identify both actual and expected repository-relative paths deterministically.
- Tests construct disposable layouts rather than touching active repositories.

## Prohibited patterns

- Directory position as an implicit artifact type, lifecycle state, relation, or approval.
- Automatic artifact moves during init, adopt, upgrade, doctor, validate, dashboard, or provenance capture.
- A second drifting map embedded independently in each command.
- Best-effort partial scaffolds, overwrite-on-create, or normalization of unsafe input into a valid-looking target.
- Inferring a domain from ID prefixes or business text.
- Treating a single-domain default as evidence that the selected work is valid, verified, or releasable.

## Quality attributes and conformance

The design prioritizes safety, deterministic behavior, backwards compatibility, navigability, and explainability. `VER-DST-005` verifies mapping completeness, path security, transaction boundaries, owner-content preservation, CLI behavior, provenance routing, advisory semantics, package parity, full graph validation, diagnostics, dashboard generation, and regression behavior.
