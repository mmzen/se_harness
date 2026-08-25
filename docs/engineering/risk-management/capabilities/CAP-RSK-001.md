+++
id = "CAP-RSK-001"
type = "capability"
title = "Identify anywhere, raise by policy, dispose by role, mitigate through governed work"
status = "draft"
owners = ["product-owner", "domain-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
derives_from = ["INT-RSK-001"]
+++

# Capability: Identify anywhere, raise by policy, dispose by role, mitigate through governed work

## Description

A governed repository can record a risk at any stage, compute from repository
policy whether it exceeds the acceptance level, put a raised risk in front of
the owner of the threatened stage, block that stage until disposition, trace
mitigation to work orders, requirements, verification contracts, or operating
contracts, and list the risks a release ships with.

## Users

Coding agents and engineers who notice a risk; the product, technical,
engineering, assurance, release, and service owners who dispose; assurance
and release reviewers who read the register.

## Boundaries

Identification and scoring are preparation. Disposition is a decision. The
harness enforces mechanics; the acceptance level is repository policy.

## Derived requirements

`REQ-RSK-001` through `REQ-RSK-006`.
