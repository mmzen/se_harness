+++
id = "WO-RLS-015"
type = "work_order"
title = "Cut, qualify and build the se-harness 0.9.0 candidate from main"
status = "draft"
owners = ["repository-owner", "release-owner", "quality-owner", "engineering-owner", "security-owner"]
created = "2026-08-28"
updated = "2026-08-28"

[assurance]
commit_bound_verification = "required"
rationale = "Release, package installation, the following evaluator adoption, recipe-bound build replay and credential-free publication rely on the exact candidate, its retained evidence and its reproducible distributions."
decided_by = "release-owner"

[execution_scope]
paths = ["docs/engineering/README.md", "docs/engineering/release-0-9-0/", "docs/notes/developing-se-harness.md"]

[relations]
implements = ["REQ-DST-006"]
specifications = ["SPEC-DST-001"]
architecture = ["ARCH-DST-001", "ADR-DST-001"]
verification = ["VER-DST-001"]
+++

# Work Order: Cut, qualify and build the se-harness 0.9.0 candidate from main

## Lifecycle

This work order requires the accountable owners' approval before start
preflight or any declared work, after `REL-SEH-020` is approved by the
release owner as a distinct decision. Its authoritative state, and the
timestamp and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `required`.

## Objective

Produce the one clean 0.9.0 candidate commit on a branch off `main` at
`effbcbc` or later, prove it with the governing 0.8.0 evaluator and the
candidate's own qualification, build it reproducibly on a Linux host through
the recipe-bound replay, retain the bundle manifest and the evidence, and
maintain the domain and repository indexes. Nothing here verifies, prepares,
releases or publishes.

No version move is needed: `pyproject.toml`, `se_harness/__init__.py` and
the README install line already read 0.9.0 (`WO-HUP-008`). The candidate
commit is therefore the commit that retains this work order's evidence and
the index maintenance; its packaged bytes are those of `main`.

## Aggregate scope

The census this work order carries is `REL-SEH-020`'s: seven work orders in
`gates`, seven verification contracts, a thirteen-requirement union, seven
work-order-keyed evidence paths. At the candidate the derivation
`harnessctl release-unit . --from v0.8.0 --to <candidate> --contract REL-SEH-020`
is re-run and recorded; a difference beyond the contract's nine recorded
exemptions is a stop condition.

## In scope

1. Qualification at the candidate, governing 0.8.0 evaluator outside the
   checkout in isolated mode: `validate`, `doctor`, review preflight, the
   handoff check over the complete changed-path set (the evidence packet
   written by the candidate's `harnessctl evidence` and carrying the legacy
   lines for the 0.8.0 governor); `scripts/validate_release_distributions.py`,
   `scripts/check_portable_release_surface.py` in `--repository`, `--wheel`
   and `--harnessctl` modes; the candidate's `qualify complete-candidate`;
   the full suite on Linux and on Windows; the real upgrade rehearsal 0.8.0
   to 0.9.0 on both platforms (the hosted lanes at the candidate head).
2. Build of record on a Linux host with the pinned producer image:
   `python -m repository_tools.release_build replay --repository . --commit <candidate> --version 0.9.0 --output-directory <dir> --result <replay.json>`,
   then `scripts/create_release_bundle_manifest.py`, retained as
   `docs/engineering/release-0-9-0/evidence/RLS-SEH-018-bundle.json` when the
   record is prepared; the digests recorded in this work order's evidence.
3. Evidence `docs/engineering/release-0-9-0/evidence/WO-RLS-015-verification.md`
   with the formal snapshot, every reading above, the hosted lanes at the
   candidate head, and any deviation.
4. Index maintenance: `docs/engineering/README.md` domain line,
   `docs/engineering/release-0-9-0/README.md`, and the release note in
   `docs/notes/developing-se-harness.md` if a sequence fact changed.

## Out of scope

- Approval of `REL-SEH-020`; preparation, verification or transition of
  `VREC-SEH-018` and `RLS-SEH-018`; the tag, the GitHub Release, PyPI, Pages,
  the maintenance line, the `last` alias; any credential use.
- Any change under `se_harness/`, any managed path, any template, any
  workflow, any test.
- The adoption of 0.9.0 as this repository's governor and the hosted gate
  demonstration; both belong to a later ordinary work order.

## Authorized decision envelope

The branch name, the order of readings, the wording of the evidence and the
index lines; the build host, provided it is a Linux host running the pinned
producer image. It may not change any packaged byte, any managed file, any
lifecycle state, or write outside the listed paths.

## Constraints

- The governing evaluator is exact public 0.8.0 installed outside the
  checkout from the wheel file (the archive pair is recorded), in isolated
  mode; a refusal is a stop.
- The candidate's own code is evidence and never governs.
- LF line endings; digests are quoted only after the hosted replay agrees.
- Stage every deletion before any preflight or check run.

## Expected change surface

The domain index, the repository index line, this work order's evidence, the
note if a sequence fact changed.

## Required verification

`VER-DST-001` for `REQ-DST-006` as `REL-SEH-020` lists under candidate
qualification and build of record; the pull request's lanes green; the
handoff check over the complete changed-path set.

## Evidence to record

`docs/engineering/release-0-9-0/evidence/WO-RLS-015-verification.md`.

## Stop and escalate conditions

A qualification reading that is not `PASS`, a replay whose two producer runs
differ or whose hosted dispatch disagrees, a release-unit difference beyond
the recorded exemptions, any work order reaching `implemented` with packaged
bytes after `REL-SEH-020`'s approval, or a need for authority beyond the
approved stage.

## Completion report format

The evidence file, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
