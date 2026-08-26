+++
id = "ADR-TST-001"
type = "adr"
title = "Schedule unittest classes with a repository-owned runner rather than adopting pytest-xdist"
status = "draft"
owners = ["technical-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
decides = ["ARCH-TST-001"]
+++

# ADR: Schedule unittest classes with a repository-owned runner rather than adopting pytest-xdist

## Status

Proposed; decided by the technical owner with the packet approval.

## Context

The suite is plain `unittest` (958 tests, 52 modules, 111 classes) with no
test dependency. The release qualification runs it inside the pinned
producer environment, and `AGENTS.md` forbids inventing a required gate.

## Decision drivers

No new dependency in the qualification path; the same verdict as the serial
run; class-level scheduling because module-level leaves a 120-second
critical path; something a maintainer can read in one sitting.

## Considered options

1. `pytest` with `pytest-xdist` — mature, `--dist loadscope` gives
   class-level scheduling; adds two dependencies to every environment that
   runs the suite, including the pinned producer, and a second test
   convention.
2. `unittest` with a hand-written parallel loader — fragile; no scheduling
   by cost.
3. A repository-owned scheduler script over `unittest` (about 150 lines,
   standard library): class-level, longest-first from recorded timings,
   aggregated report. The serial `unittest discover` stays canonical.

## Decision

Option 3.

## Consequences

One script to maintain; timings as derived output; the release
qualification is untouched. If the suite ever migrates to `pytest`, the
script is deleted, not extended.
