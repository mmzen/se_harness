+++
id = "WO-REB-014"
type = "work_order"
title = "Normalize Windows Git-Bash release paths"
status = "implemented"
owners = ["engineering-owner", "quality-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[assurance]
commit_bound_verification = "required"
rationale = "The retained Windows producer must receive one bounded POSIX temporary path in every unprivileged Git-Bash release step without weakening exact-byte or privilege gates."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-REB-015"]
specifications = ["SPEC-REB-007"]
architecture = ["ARCH-REB-006", "ADR-REB-006"]
verification = ["VER-REB-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T21:01:21Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-22T21:01:22Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-22T21:06:40Z"
decided_by = "engineering-owner"
+++

# Work Order: Normalize Windows Git-Bash release paths

## Lifecycle

This bounded corrective work is implemented with exact qualification retained in `../evidence/WO-REB-014-windows-bash-path.md`. Commit-bound assurance remains required before another publication retry.

## Objective

Convert the Windows runner's native temporary directory to one Git-Bash POSIX path in each unprivileged qualification step so Git, tar, shell tools, and Python share the same bounded files.

## In scope

- Retain run `32598292643`, job `97092604303`, and exact `tar: D:\a\_temp/source-a: Cannot open` refusal.
- Derive `temp_root` with `cygpath -u "$RUNNER_TEMP"` in the four Bash steps that access temporary files.
- Replace only direct native `$RUNNER_TEMP/...` shell references in those steps.
- Assert all four conversions exist and no direct native temporary-path reference remains in qualification.

## Out of scope

- Changing the retained runner/runtime/toolchain, C6, RLS, distributions, resolver, build commands, upload destination, downstream jobs, credentials, or external policy.

## Required verification

- Run focused workflow policy, complete release-orchestration, complete isolated suite, current/predecessor graph, distribution, portable-surface, whitespace, and clean-checkout checks.
- Prove upload still reads `${{ runner.temp }}/release-bundle/` through the action interface and every shell consumer uses only `temp_root`.
- Prepare and verify a later commit-bound VREC before retry.

## Evidence

Retain results in `../evidence/WO-REB-014-windows-bash-path.md`.
