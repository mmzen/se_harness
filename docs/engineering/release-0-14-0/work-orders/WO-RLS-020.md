+++
id = "WO-RLS-020"
type = "work_order"
title = "Cut, qualify and build the se-harness 0.14.0 candidate from main"
status = "draft"
owners = ["repository-owner", "release-owner", "quality-owner", "engineering-owner", "security-owner"]
created = "2026-09-02"
updated = "2026-09-02"

[assurance]
commit_bound_verification = "required"
rationale = "Release, package installation, the following evaluator adoption, recipe-bound build replay and credential-free publication rely on the exact candidate, its retained evidence and its reproducible build; every later decision binds the exact commit."
decided_by = "release-owner"

[execution_scope]
paths = ["docs/engineering/README.md", "docs/engineering/release-0-14-0/", "docs/notes/developing-se-harness.md"]

[relations]
implements = ["REQ-DST-006"]
specifications = ["SPEC-DST-001"]
architecture = ["ARCH-DST-001", "ADR-DST-001"]
verification = ["VER-DST-001"]
+++

# Work Order: Cut, qualify and build the se-harness 0.14.0 candidate from main

## Lifecycle

This work order requires the accountable owners' approval before start
preflight or any declared work, after `REL-SEH-025` is approved by the
release owner as a distinct decision. Its authoritative state, and the
timestamp and reason of every decision taken on it, are the front matter
and `[[lifecycle_events]]` above. Commit-bound verification is `required`.

## Objective

Produce the one clean 0.14.0 candidate commit on a branch off `main` at
`d005b98` or later, prove the candidate with the governing 0.13.0 evaluator
and the candidate's own qualification, take the build of record from the
hosted recipe-bound replay dispatched on the branch at the candidate head,
retain the bundle manifest and the evidence, and maintain the domain and
repository indexes. Nothing here verifies, prepares, releases or
publishes.

No version move is needed: `pyproject.toml`, `se_harness/__init__.py` and
the README install line already read 0.14.0 (`WO-HUP-014`). The candidate
commit is therefore the commit that retains this work order's evidence and
the index maintenance; its packaged bytes are those of `main`.

## Aggregate scope

The census this work order carries is `REL-SEH-025`'s: two work orders in
`gates`, two verification contracts, a three-requirement union, two
work-order-keyed evidence paths. At the candidate the derivation
`harnessctl release-unit . --from v0.13.0 --to <candidate> --contract REL-SEH-025`
is re-run and recorded; a difference beyond the released `WO-RLS-019`
traced through the #313 merge and this work order itself is a stop
condition.

## In scope

1. Qualification at the candidate, governing 0.13.0 evaluator outside the
   checkout in isolated mode: `validate`, `doctor`, review preflight, the
   handoff check over the Git-derived change set;
   `scripts/validate_release_distributions.py`,
   `scripts/check_portable_release_surface.py` in `--repository`, `--wheel`
   and `--harnessctl` modes; the candidate's `qualify complete-candidate`
   (read from the hosted Linux lane for the `RID018` boundary reason); the
   full suite on Linux (hosted) and on Windows (this workstation); the real
   upgrade rehearsal 0.13.0 to 0.14.0 on both hosted platforms at the
   candidate head.
2. Build of record from the hosted Publication Rehearsal in `candidate`
   mode dispatched on `release/0.14.0` at the bound candidate: two
   byte-identical producer runs on the pinned image; the retained
   `release-build-replay.json` downloaded from that run, its
   `candidate.commit` checked equal to the candidate, its `manifest`
   retained as
   `docs/engineering/release-0-14-0/evidence/RLS-SEH-023-bundle.json` when
   the record is prepared; the digests recorded in this work order's
   evidence as hosted readings.
3. Evidence: this work order's handoff packet under
   `docs/engineering/release-0-14-0/evidence/WO-RLS-020/` with the formal
   snapshot, every reading above, the hosted lanes at the candidate head,
   and any deviation.
4. Index maintenance: `docs/engineering/README.md` domain line,
   `docs/engineering/release-0-14-0/README.md`, and the release note in
   `docs/notes/developing-se-harness.md` if a sequence fact changed.

## Out of scope

- Approval of `REL-SEH-025`; preparation, verification or transition of
  `VREC-SEH-023` and `RLS-SEH-023`; the tag, the GitHub Release, PyPI,
  Pages, the maintenance line, the `last` alias and the latest marker; any
  credential use.
- Any change under `se_harness/`, any managed path, any template, any
  workflow, any test.
- The adoption of 0.14.0 as this repository's root.

## Authorized decision envelope

The branch name, the order of readings, the evidence and the index lines;
the build host, provided it runs the pinned linux/amd64 producer image
through Docker, which the hosted GitHub runner does. It may not change any
packaged byte, any managed file, any lifecycle state, or write outside the
listed paths.

## Constraints

- Every reading names its evaluator and platform.
- Every commit on the release branch carries the
  `Harness-Work-Order: WO-RLS-020` trailer in its final block, so the
  census at the candidate needs no exemption.
- No promotable distribution leaves this work order; the bundle manifest is
  retained evidence until `RLS-SEH-023` binds it.

## Expected change surface

The domain packet, this work order's evidence, two index files and
possibly one note line.

## Required verification

Execute the candidate-qualification and build-of-record sections of
`REL-SEH-025` in full; repository-required checks; the pull request's
lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/release-0-14-0/evidence/WO-RLS-020/`.

## Stop and escalate conditions

Any work order reaching `implemented` with packaged-surface bytes after
`REL-SEH-025`'s approval; any census difference beyond the released
`WO-RLS-019` and this work order; a hosted producer run that is not
byte-identical to its twin; any hash-locked file in the change set.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
