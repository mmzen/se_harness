+++
id = "ADR-CIP-001"
type = "adr"
title = "Rehearse the release by invoking its definition, not by digesting a copy of it"
status = "approved"
owners = ["technical-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
decides = ["ARCH-CIP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T15:17:28Z"
decided_by = "technical-owner"
reason = "Owner decision 2026-08-26, as technical owner: rehearse the release by invoking its definition, not by digesting a copy of it."
+++

# ADR: Rehearse the release by invoking its definition, not by digesting a copy of it

## Status

Proposed; decided by the technical owner with the packet approval.

## Context

`WO-RLO-005` established that the credential-free last mile is rehearsed
before a release is approved (`CAP-RLO-003`). It did so with a Python copy
of the qualification whose alignment with `publish-pypi.yml` is proven by
parsing the YAML and comparing per-step digests declared in a JSON file.
The mechanism is faithful and expensive: three artefacts to keep in
lockstep by hand, a stdlib-only script that re-implements package helpers,
and a red lane on every workflow edit until the digests are regenerated.

## Decision drivers

Keep the rehearsal's guarantee; remove the copy; keep the privileged jobs
free of anything the rehearsal did not execute; reduce the script surface.

## Considered options

1. Keep the digest mechanism and regenerate digests by a script — same
   three artefacts, less friction; the copy remains.
2. Delete the rehearsal and trust the release run — loses `CAP-RLO-003`.
3. Extract the qualification into a `workflow_call` reusable workflow and
   have both lanes invoke it — one definition; the rehearsal executes the
   exact steps the release will execute; no digest needed.
4. Move the qualification entirely into one package command invoked by both
   lanes — equivalent guarantee, larger change to `repository_tools`.

## Decision

Option 3, with option 4's principle for helpers: scripts import the package
rather than re-implementing it.

## Consequences

`rehearse_publication.py`, its mechanics declaration and the divergence job
are removed; `publication-rehearsal.yml` becomes a caller. `CAP-RLO-003`'s
evidence changes from "digests match" to "the same definition ran". The
rehearsal can no longer detect an edit to the caller's privileged jobs;
those are reviewed as code, which they were already.
