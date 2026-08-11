+++
id = "CAP-PMI-001"
type = "capability"
title = "Evaluate managed integrity consistently across platforms"
status = "approved"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
derives_from = ["INT-PMI-001"]
+++

# Capability: Evaluate managed integrity consistently across platforms

## Actor and need

Repository owners and automation need to distinguish safe platform representation differences from actual customization before validation, upgrade, verification, and release decisions.

## Capability statement

`A repository operator can evaluate and migrate managed-file integrity deterministically across supported LF and CRLF environments without losing customization protection.`

## Boundaries

The capability applies only to harness-owned UTF-8 managed files and bounded managed fragments. Seed files, owner-controlled content outside fragments, binaries, Git configuration, lifecycle approvals, and release actions remain outside the automation boundary.

## Outcomes

- Portable and explainable doctor results.
- Safe upgrade classification and lock migration.
- One shared hashing contract across all harness surfaces.
- Reproducible source, template, wheel, and installation evidence.

## Candidate requirements

`REQ-PMI-001` through `REQ-PMI-007` define canonical hashing, explicit schema semantics, safe legacy migration, customization preservation, shared implementation, distribution parity, and unchanged security boundaries.
