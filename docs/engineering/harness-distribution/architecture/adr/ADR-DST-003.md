+++
id = "ADR-DST-003"
type = "adr"
title = "Use one PyPI-first README with explicit environment-local commands"
status = "approved"
owners = ["technical-owner", "product-owner", "documentation-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
decides = ["ARCH-DST-003"]
+++

# ADR: Use one PyPI-first README with explicit environment-local commands

## Status

Accepted.

## Context

The distribution now has a production PyPI package and verified GitHub-to-PyPI lineage, while its public README still begins with source-checkout installation. The same README is not currently declared as package long description, and users are not told that pip places `harnessctl` inside the selected virtual environment. The document also hardcodes a conceptual independent-baseline version that can drift from workflow configuration.

## Decision drivers

- Minimize time from project discovery to a working initialized or adopted repository.
- Keep released installation distinct from source development.
- Make virtual-environment launcher discovery predictable on Windows and POSIX.
- Avoid duplicated public documentation and metadata drift.
- Preserve explicit authority and immutable release-history boundaries.
- Keep runtime and verification behavior standard-library-only.

## Considered options

1. **Keep source-first installation**: rejected because ordinary users do not need a checkout and may unknowingly operate candidate code.
2. **Create a separate PyPI README**: rejected because two long-form public entry points would drift and create ambiguous maintenance ownership.
3. **Recommend a global pip installation**: rejected because interpreter ownership and launcher discovery become ambiguous and conflict-prone.
4. **Generate README version and links dynamically during build**: rejected because it introduces nontransparent build behavior and weakens reproducibility.
5. **Use one static root README, declare it as package metadata, and test synchronized facts**: selected.

## Decision

Use the root `README.md` as both repository entry point and package long description. Lead with released PyPI installation in a local virtual environment, show platform-specific launcher locations and module invocation, distinguish package upgrade from repository apply, and keep exact version examples synchronized through deterministic tests. Keep the current CI baseline identity in the workflow rather than duplicating it as conceptual README state.

## Consequences

The README becomes a packaging compatibility surface and must render acceptably on both GitHub and PyPI. Version changes require updating the exact-version example or tests fail. The package gains discoverable license and project URLs. Existing PyPI 0.2.1 metadata remains unchanged, so external visibility waits for a later release. Deep governance content remains longer than a minimal package README, but it is placed after the quick start and continues demonstrating the harness itself.

## Validation

Apply `VER-DST-003`, inspect the rendered Markdown structure and links, run full repository checks, and defer actual wheel/sdist metadata inspection to the next approved release build.

## Revisit conditions

Revisit if PyPI rendering cannot present the shared README safely, if multiple distribution channels require materially different instructions, or if version synchronization can be derived without dynamic build inputs or duplicated authority.
