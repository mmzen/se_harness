+++
id = "INT-DST-001"
type = "intent"
title = "Make the engineering harness repeatably available"
status = "approved"
owners = ["product-owner", "engineering-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
+++

# Intent: Make the engineering harness repeatably available

## Problem

The existing harness demonstrates repository-native traceability and visualization, but adopting it in another repository requires manual copying and knowledge of its internal file contract. Manual variants would drift, omit assurance behavior, and make upgrades unsafe.

## Outcome

A user can install one complete, versioned harness into a new or existing repository, operate it consistently, and inspect upgrades without replacing repository-owned customizations or inventing product authority.

## Principles

- There is one standard installation, not a matrix of profiles.
- Target-repository files are untrusted and repository-owned customizations are preserved.
- Adoption inventories observable signals but never manufactures approved intent or requirements.
- The target repository remains the source of engineering truth after installation.

