+++
id = "VER-PLG-001"
type = "verification"
title = "Independent package contents and shared-source evidence"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-001","REQ-PLG-002"]
+++

# Verification Contract: Independent package contents and shared-source evidence

## Independence

Derive expected wheel bytes from the selected published release and its trusted digest.
Use SPEC-PLG-001 for inventory expectations, not the packager's generated manifest.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-001 | Test, inspection | Valid wheel; replaced wheel; forbidden runtime | Exact published bytes included; replacements and runtimes refused. |
| REQ-PLG-002 | Test, inspection | Both host outputs; divergent common files; unsafe path | Shared files agree with source; divergence and path escape refused. |

## Acceptance scenarios

Assemble both fixture packages from one revision.
Repeat with a wrong wheel digest, missing shared asset, and escaping destination; no usable output survives failure.

## Property and invariant tests

Compare every shared file across outputs.
Neither output contains a Python runtime or top-level executable directory.

## Static and architecture checks

Inspect the source/output inventories against ARCH-PLG-001 and ADR-PLG-001.

## Security and privacy checks

Retained inventories contain no local credentials or environment values.

## Performance and resilience checks

Interrupt assembly; incomplete output cannot be reported usable.

## Manual assessments

Record Windows, Linux, and macOS results where the build runs.
Name unavailable lanes; do not infer host activation support.

## Evidence retention

Retain commands, source revision, selected evaluator version, trusted digest reference, inventories, and results under `evidence/WO-PLG-001/`.

## Residual uncertainty

Fixture assembly does not prove native host discovery or authorize package publication.
