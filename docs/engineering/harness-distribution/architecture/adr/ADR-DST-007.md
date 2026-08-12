+++
id = "ADR-DST-007"
type = "adr"
title = "Concise root with audience-layered reference notes"
status = "approved"
owners = ["technical-owner", "documentation-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
decides = ["ARCH-DST-007"]
+++

# ADR: Concise root with audience-layered reference notes

## Status

Accepted.

## Context

The root README has grown to 523 lines across 16 level-two sections. It successfully captures current behavior but makes first-use value and human responsibility difficult to scan. The progressive notes added by `WO-DOC-007` now provide a durable place for conceptual depth, yet the root still duplicates model, lifecycle, command, layout, release, CI, and contributor material.

The repository owner agreed that the root should contain only important human-facing knowledge, that agent-only command examples should move out of Quick Start and the five-minute workflow, and that upgrades must remain safely discoverable.

## Decision drivers

- Make value and first use understandable without source inspection.
- Keep human authority visible while reducing agent mechanics.
- Preserve advanced operational and contributor knowledge.
- Avoid creating a second governance source.
- Keep GitHub and PyPI public presentation synchronized.
- Prevent documentation size from regrowing without review.

## Considered options

1. **Keep the comprehensive README and add a table of contents**: preserves all detail but leaves audience mixing and duplication unresolved.
2. **Delete advanced content without relocation**: produces the shortest root but removes practical safety and contributor knowledge.
3. **Maintain separate user and contributor root documents**: separates audiences but creates competing public entry points and PyPI synchronization risk.
4. **Keep a concise human-facing root and layer current detail into indexed notes**: preserves one public entry, supports progressive expertise, and routes authority explicitly.
5. **Generate the README from many source fragments**: could enforce reuse but adds build machinery and makes raw repository editing less transparent.

## Decision

Adopt option 4. Limit the root README to 200 physical lines and at most nine level-two sections. Keep installation, start, product value, compact lineage, responsibility, Explorer value, known limitations, and deeper routes. Limit routine root harness subcommand examples to `init`, `adopt`, `doctor`, `validate`, and `dashboard`.

Move platform and upgrade detail, full CLI reference, and distribution development/self-hosting guidance into three expertise-labeled notes. Reuse existing model, phasing, branching, and practical-example notes for the responsibilities they already own. Route normative questions to `ENGINEERING_HARNESS.md` and managed policy.

## Consequences

The public page becomes substantially faster to scan and better aligned with repository-owner needs. Humans still see what the agent is expected to do and who makes decisions, without learning agent-only syntax. Operators and contributors take one additional link to reach detail, so link quality and index structure become tested contracts.

The 200-line limit creates maintenance pressure toward concise phrasing and explicit relocation. Some facts will be intentionally retired because they duplicate policy or existing notes; evidence must record those decisions. The command reference requires synchronization tests when CLI subcommands change.

No runtime, governance, installer, release, or self-hosting behavior changes. Existing formal packet history remains immutable.

## Validation

Apply `VER-DST-007`. Verify the public information budget and human command allowlist, ensure every relocated responsibility has one discoverable owner, compare the command reference to the CLI parser, inspect value and authority comprehension at 6/10, resolve links, and run the complete harness regression and integrity checks.
