+++
id = "REQ-DST-008"
type = "requirement"
title = "Seed repository-owned engineering context"
status = "implemented"
owners = ["product-owner", "engineering-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN the standard harness is first installed or an older installation is upgraded, THE SYSTEM SHALL add an absent repository-context scaffold, preserve any existing context, and treat the resulting file as repository-owned rather than inferred product authority."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Seed repository-owned engineering context

## Rationale

Shared harness rules cannot supply repository-specific purpose, commands, architecture, or constraints. Those facts require explicit repository-owner curation.

## Required response

- Seed `docs/engineering/REPOSITORY_CONTEXT.md` when the installation has never accounted for that path and the path is absent.
- Render only bounded installation facts such as the selected project name.
- Mark all substantive repository fields for human completion.
- Preserve pre-existing content during adoption and all later edits or removal during upgrade.
- Do not hash repository-owned context as immutable managed content.

## Boundary behavior

Observed ecosystems and files may be reported as non-authoritative observations but may not populate purpose, commands, architecture, or approval fields.
