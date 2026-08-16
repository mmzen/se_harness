+++
id = "REL-WLC-001"
type = "release_contract"
title = "Release work-order lifecycle consistency"
status = "rejected"
owners = ["release-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-16"

[relations]
gates = ["WO-WLC-001"]
+++

# Release Contract: Release work-order lifecycle consistency

## Entry criteria

A separately captured and human-verified VREC binds `WO-WLC-001` and retained evidence to one clean candidate commit; graph, full tests, installation, upgrade, doctor, dashboard, and distribution checks pass.

## Authority boundary

This draft does not authorize a release record, tag, publication, or deployment.

## Disposition

This per-feature proposal was never selected as release authority. `WO-WLC-001` was released in `0.2.1` under aggregate contract `REL-SEH-002` and released record `RLS-SEH-002` at tag `v0.2.1`. The rejected status disposes of this unused proposal; it does not reject the released implementation.
