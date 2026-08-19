+++
id = "CAP-EVK-001"
type = "capability"
title = "Attribute retained evidence across supported repository layouts"
status = "approved"
owners = ["product-owner", "quality-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[relations]
derives_from = ["INT-EVK-001"]
+++

# Capability: Attribute retained evidence across supported repository layouts

## Actor and need

Repository engineers and assurance owners need retained evidence to remain attributable to its work order whether the repository uses flat work-order-prefixed filenames or one work-order-keyed directory containing multiple evidence files.

## Capability statement

`A repository owner can organize retained evidence by filename or directory while SE Harness attributes exact work-order keys consistently and preserves provenance and path safety.`

## Boundaries

The capability determines structural attribution only. It does not evaluate evidence content, approve verification, modify historical paths, relax filesystem controls, or infer work scope. It applies to normalized repository-relative evidence paths consumed by record preparation, formal validation, inspection, and Harness Explorer.

## Outcomes

- Directory-per-work-order repositories no longer receive false missing-evidence findings.
- Aggregate verification preparation and formal validation accept the same safe keyed paths.
- Flat layouts retain existing behavior.
- Attribution is deterministic across supported platforms and independent execution planes.

## Candidate requirements

- Recognize exact work-order keys in supported evidence path components.
- Apply one attribution contract across every harness surface.
- Preserve historical compatibility and existing path-safety controls.
- Keep platform and execution-plane behavior deterministic and independently assessable.
