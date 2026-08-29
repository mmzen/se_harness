+++
id = "WO-RLS-016"
type = "work_order"
title = "Cut, qualify and build the se-harness 0.10.0 candidate from main"
status = "in_progress"
owners = ["repository-owner", "release-owner", "quality-owner", "engineering-owner", "security-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[assurance]
commit_bound_verification = "required"
rationale = "Release, package installation, the following evaluator adoption, recipe-bound build replay and credential-free publication rely on the exact candidate, its retained evidence and its reproducible distributions."
decided_by = "release-owner"

[execution_scope]
paths = ["docs/engineering/README.md", "docs/engineering/release-0-10-0/", "docs/notes/developing-se-harness.md"]

[relations]
implements = ["REQ-DST-006"]
specifications = ["SPEC-DST-001"]
architecture = ["ARCH-DST-001", "ADR-DST-001"]
verification = ["VER-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T09:38:48Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-29, 'Approve REL-SEH-021 and WO-RLS-016, start', after the release owner approved REL-SEH-021 seconds earlier as a distinct decision. Authorizes start preflight and then only the declared scope: the candidate's qualification under the governing 0.9.0 root, the recipe-bound build of record, the retained evidence and the index maintenance. It authorizes no verification record, no release record, no tag, no publication and no credential use."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-29T09:38:56Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-08-29, 'Approve REL-SEH-021 and WO-RLS-016, start'. Start preflight PASS with no diagnostics over the approval commit 373959d carrying unmoved main 3139f24, run with the governing exact public 0.9.0 evaluator outside the checkout. Bounded to the declared execution scope. This start authorizes no verification record, no release record and no publication."
+++

# Work Order: Cut, qualify and build the se-harness 0.10.0 candidate from main

## Lifecycle

This work order requires the accountable owners' approval before start
preflight or any declared work, after `REL-SEH-021` is approved by the
release owner as a distinct decision. Its authoritative state, and the
timestamp and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `required`.

## Objective

Produce the one clean 0.10.0 candidate commit on a branch off `main` at
`3139f24` or later, prove it with the governing 0.9.0 evaluator and the
candidate's own qualification, build it reproducibly through the
recipe-bound replay with the pinned linux/amd64 producer image, retain the
bundle manifest and the evidence, and maintain the domain and repository
indexes. Nothing here verifies, prepares, releases or publishes.

No version move is needed: `pyproject.toml`, `se_harness/__init__.py` and
the README install line already read 0.10.0 (`WO-HUP-009`). The candidate
commit is therefore the commit that retains this work order's evidence and
the index maintenance; its packaged bytes are those of `main`.

## Aggregate scope

The census this work order carries is `REL-SEH-021`'s: five work orders in
`gates`, five verification contracts, a six-requirement union, five
work-order-keyed evidence paths. At the candidate the derivation
`harnessctl release-unit . --from v0.9.0 --to <candidate> --contract REL-SEH-021`
is re-run and recorded; a difference beyond the contract's four recorded
exemptions and the traced, released `WO-RLS-015` is a stop condition.

## In scope

1. Qualification at the candidate, governing 0.9.0 evaluator outside the
   checkout in isolated mode: `validate`, `doctor`, review preflight, the
   handoff check over the Git-derived change set (the evidence packet
   written by the released evaluator from an LF clone, issue #256 on this
   root); `scripts/validate_release_distributions.py`,
   `scripts/check_portable_release_surface.py` in `--repository`, `--wheel`
   and `--harnessctl` modes; the candidate's `qualify complete-candidate`;
   the full suite on Linux and on Windows; the real upgrade rehearsal 0.9.0
   to 0.10.0 on both platforms (the hosted lanes at the candidate head).
2. Build of record through the pinned producer image:
   `python -m repository_tools.release_build replay --repository . --commit <candidate> --version 0.10.0 --output-directory <dir> --result <replay.json>`,
   then `scripts/create_release_bundle_manifest.py`, retained as
   `docs/engineering/release-0-10-0/evidence/RLS-SEH-019-bundle.json` when
   the record is prepared; the digests recorded in this work order's
   evidence only after the hosted replay agrees.
3. Evidence `docs/engineering/release-0-10-0/evidence/WO-RLS-016-verification.md`
   with the formal snapshot, every reading above, the hosted lanes at the
   candidate head, and any deviation.
4. Index maintenance: `docs/engineering/README.md` domain line,
   `docs/engineering/release-0-10-0/README.md`, and the release note in
   `docs/notes/developing-se-harness.md` if a sequence fact changed.

## Out of scope

- Approval of `REL-SEH-021`; preparation, verification or transition of
  `VREC-SEH-019` and `RLS-SEH-019`; the tag, the GitHub Release, PyPI, Pages,
  the maintenance line, the `last` alias; any credential use.
- Any change under `se_harness/`, any managed path, any template, any
  workflow, any test.
- The adoption of 0.10.0 as this repository's root; it belongs to a later
  ordinary work order.

## Authorized decision envelope

The branch name, the order of readings, the wording of the evidence and the
index lines; the build host, provided it runs the pinned linux/amd64 producer
image through Docker. It may not change any packaged byte, any managed file,
any lifecycle state, or write outside the listed paths.

## Constraints

- The governing evaluator is exact public 0.9.0 installed outside the
  checkout from the wheel file (the archive pair is recorded), in isolated
  mode; a refusal is a stop.
- The candidate's own code is evidence and never governs.
- Digests are quoted only after the hosted replay agrees.

## Expected change surface

The domain index, the repository index line, this work order's evidence, the
note if a sequence fact changed.

## Required verification

`VER-DST-001` for `REQ-DST-006` as `REL-SEH-021` lists under candidate
qualification and build of record; the pull request's lanes; the handoff
check over the Git-derived change set.

## Evidence to record

`docs/engineering/release-0-10-0/evidence/WO-RLS-016-verification.md`.

## Stop and escalate conditions

A qualification reading that is not `PASS`, a replay whose two producer runs
differ or whose hosted dispatch disagrees, a release-unit difference beyond
the recorded exemptions and the traced, released `WO-RLS-015`, any work order
reaching `implemented` with packaged bytes after `REL-SEH-021`'s approval,
or a need for authority beyond the approved stage.

## Completion report format

The evidence file, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
