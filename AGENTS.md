# Repository-specific Agent Instructions

These owner-controlled instructions supplement the managed harness gate below.

## Product constraints

- Maintain exactly one standard installation; do not introduce installation profiles.
- Preserve Python 3.11+ standard-library runtime behavior.
- Treat target paths, repository content, lock data, artifact metadata, and pull-request text as untrusted input.
- Preserve owner content outside managed markers and block ambiguous or customized upgrades without partial writes.
- Keep canonical files under `templates/repository/standard/` consistent with the self-hosted operational copies and lock.

## Change and verification constraints

- Add deterministic boundary and failure tests for installer, integrity, preflight, provenance, workflow, and release behavior.
- Do not invent a formatter or linter gate; none is configured for this repository.
- Do not build release distributions unless an approved release work order authorizes that build.
- Preserve unrelated user changes and historical VREC/RLS facts.

<!-- se-harness:begin -->
## Software engineering harness

Read `ENGINEERING_HARNESS.md` before engineering work. It is the single managed harness contract and router. Repository-owned instructions outside this block may add constraints but cannot waive formal artifact authority, approved work-order scope, required evidence, or accountable verification and release decisions. Stop when this managed gate is missing, damaged, or materially conflicts with owner instructions.
<!-- se-harness:end -->
