+++
id = "ADR-RLO-004"
type = "adr"
title = "Use one bound declarative recipe and immutable OCI producer"
status = "approved"
owners = ["engineering-owner", "security-owner", "release-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
decides = ["ARCH-RLO-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T12:01:04Z"
decided_by = "engineering-owner"
+++

# ADR: Use one bound declarative recipe and immutable OCI producer

## Status

Proposed for issue #110. It is not accepted until the accountable technical and security owners explicitly approve this packet.

## Context

The 0.6.0 release recorded the candidate epoch and output hashes but not the complete build producer. Tool versions appeared partly in workflow YAML, the runner supplied the OS and architecture, setup-python supplied the runtime, and unrecorded environment and transitive packages could affect bytes. The release could therefore reject a valid candidate when another environment rebuilt it differently.

The correction must make accepted build identity complete and replayable, keep candidate execution away from credentials, preserve one-input publication, leave portable SE Harness format-neutral, and avoid rewriting `RLS-SEH-012` or published 0.6.0 bytes.

## Decision drivers

- One reviewable and machine-readable source for producer and command identity.
- Exact platform, Python, complete toolchain, environment, epoch, normalizer, and output provenance.
- No recipe-supplied arbitrary shell execution.
- Independent hosted replay before release approval.
- Same mechanics in acceptance replay and production reconstruction.
- Candidate execution only in a no-credential boundary.
- Historical replay without concrete-record exceptions or history mutation.
- A clean prerequisite for the later native Linux/Windows rehearsals in issue #111.

## Considered options

1. Keep workflow YAML as the build definition and add more comments or evidence fields.
2. Record an observation of the hosted runner, Python, and `pip freeze` after each build while continuing to execute handwritten workflow commands.
3. Inline a complete command and environment table directly in every RLS and execute it as shell text.
4. Bind one candidate-tree declarative JSON recipe and toolchain lock, interpret a closed schema through repository-owned code, and execute it in one digest-pinned Linux/amd64 OCI producer.
5. Build and operate a custom preloaded release image containing repository source and all tooling.

## Decision

Choose option 4.

Add canonical `release/build-recipe.json` and `release/build-toolchain.lock`. The recipe declares one public immutable OCI image digest, exact Linux/amd64 and CPython identities, a complete hash-locked Python tool inventory, a closed fixed/derived environment, typed argument-array steps, the current deterministic sdist normalizer contract, and exact outputs.

Add a strict repository-owned parser and producer adapter. It rejects unknown fields, unsafe paths, mutable identities, missing tool inventory, inherited environment, and arbitrary commands. It exports the candidate and launches the producer twice with isolated state. It compares declared and observed runtime/toolchain identity before the project build and compares both outputs with each other and with already accepted hashes during replay.

Advance repository bundle and RLS distribution metadata to schema 2 by adding `build_recipe_schema`, `build_recipe`, and `build_recipe_sha256`. New ready records require schema 2. Already released schema-1 records remain readable and replayable through a separate labeled legacy path. The cutover depends on record lifecycle/schema, not a version allowlist or a special case for `RLS-SEH-012`.

Add a read-only hosted pre-release workflow that accepts one ready RLS ID. Make schema-2 production qualification call the same interpreter. Keep workflow YAML responsible only for orchestration and permission boundaries.

## Consequences

- Positive: a release decision can identify exactly what produced accepted bytes, not only what the bytes happened to hash to.
- Positive: local, hosted, and production reconstruction share one parser and command plan, so workflow text cannot silently become a second recipe.
- Positive: image, Python, direct and transitive tools, environment, commands, normalizer, and outputs are explicit and reviewable.
- Positive: the producer is reproducible independently of GitHub hosted image rotation, and candidate code remains outside credentialed jobs.
- Positive: #111 can compare native Linux and Windows paths against one canonical accepted identity.
- Negative: release builds require an OCI runtime and public immutable image/tool downloads.
- Negative: recipe and lock updates become reviewed release-infrastructure changes and require new exact hashes.
- Negative: two fresh producer executions cost more than the current shared-host build.
- Operational: a new release process prepares and binds schema 2, dispatches hosted replay while the RLS is ready, and reviews retained evidence before release decision.
- Security: public image and package registries remain supply dependencies, but all accepted artifacts are content- or hash-addressed; candidate code receives no credentials.
- Migration: `RLS-SEH-012` and schema-1 evidence are preserved; only future ready records use schema 2. No portable package or consumer migration occurs.

## Validation

- Validate canonical recipe, tool lock, candidate-tree binding, bundle schema 2, distribution schema 2, atomic binder behavior, and historical schema-1 compatibility.
- Prove the producer observes the exact image/platform/Python/tool inventory and receives only the closed environment and argument arrays.
- Build twice locally and in a hosted read-only lane and reproduce exact accepted wheel and normalized-sdist hashes.
- Prove schema-2 production qualification calls the shared interpreter and privileged jobs execute no candidate or recipe content.
- Inspect the built wheel and initialized/updated consumer repositories for absence of recipe policy.
- Run failure injection for image, tool, environment, command, normalization, output, timeout, cleanup, and expected-hash mismatch.
