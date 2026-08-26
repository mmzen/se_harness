# Test Suite Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata,
> typed relations, lifecycle state, and accountable decisions—not this directory
> or index.

This domain follows the 2026-08-26 measurement of the candidate test suite
(`docs/notes/ci-pipeline.md`, "The test suite"): 958 tests, 367 seconds
serial, all of it inside the tests; two scale tests worth 29 seconds; a
fixed half-second `harnessctl init` in most fixtures; and a measured 125
seconds at four worker processes with module-level scheduling, a computed
floor near 60 seconds with class-level scheduling. The packet adds a
repository-owned parallel runner, a marker for the scale tests, and a cached
fixture install, and keeps `python -m unittest discover` as the canonical
serial reference.

## Draft definition packet

- `INT-TST-001`: a full suite in about a minute, with the same verdict.
- `CAP-TST-001`: run the candidate suite in parallel with one aggregated verdict.
- `REQ-TST-001`: a repository-owned parallel runner scheduling test classes longest-first across worker processes.
- `REQ-TST-002`: the 1,000-artifact scale tests run at full size only under an explicit marker.
- `REQ-TST-003`: fixtures take a standard repository from a per-session cache instead of running `init` each time.
- `SPEC-TST-001`: the runner's interface, scheduling, aggregation and exit code; the marker; the cache.
- `ARCH-TST-001` / `ADR-TST-001`: a standard-library runner over `unittest`, not a pytest dependency.
- `VER-TST-001`: independent evidence.
- `WO-TST-001`: runner, marker, test command in `AGENTS.md`, candidate-evidence suite step, notes (REQ-TST-001, 002).
- `WO-TST-002`: the cached fixture install (REQ-TST-003).
- `WO-TST-003`: follow-up to WO-TST-001's deviation 1 — the release qualification sets the scale marker (REQ-TST-002). Draft.

Every artifact remains `draft`. This packet authorizes no implementation,
lifecycle transition, Git action, or external action.
