+++
id = "WO-RLS-022"
type = "work_order"
title = "Cut, qualify and build the se-harness 0.16.0 candidate from main"
status = "in_progress"
owners = ["repository-owner", "release-owner", "quality-owner", "engineering-owner", "security-owner"]
created = "2026-09-07"
updated = "2026-09-07"

[assurance]
commit_bound_verification = "required"
rationale = "Release, package installation, the following evaluator adoption, recipe-bound build replay and credential-free publication rely on the exact candidate, its retained evidence and its reproducible build; every consumer that upgrades to 0.16.0 receives the engine relocation, the installer behaviour and the templates this candidate carries."
decided_by = "release-owner"

[execution_scope]
paths = ["docs/engineering/README.md", "docs/engineering/release-0-16-0/", "docs/notes/developing-se-harness.md"]

[relations]
implements = ["REQ-DST-006"]
specifications = ["SPEC-DST-001"]
architecture = ["ARCH-DST-001", "ADR-DST-001"]
verification = ["VER-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T07:26:08Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-09-07 by selecting the presented option 'Approve both (Recommended)', after the release owner approved REL-SEH-027 in the same transaction. WO-RLS-022 carries no delegation class: its start, completion and record preparation are the engineering owner's explicit decisions."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-07T08:21:55Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-09-07, given by selecting the presented option 'Merged; start, complete on green, prepare record'. Start preflight PASS with no diagnostics over the reading manifest; REL-SEH-027 approved by the release owner the same day; branch release/0.16.0 cut from main at 2e46b492."
+++

# Work Order: Cut, qualify and build the se-harness 0.16.0 candidate from main

## Lifecycle

This work order requires the accountable owners' approval before start
preflight or any declared work, after `REL-SEH-027` is approved by the
release owner as a distinct decision. Its authoritative state, and the
timestamp and reason of every decision taken on it, are the front matter
and `[[lifecycle_events]]` above. Commit-bound verification is `required`.

## Objective

Produce the one clean 0.16.0 candidate commit on a branch off `main` at the
re-measured census commit or later, prove the candidate with the governing
0.15.0 evaluator and the candidate's own qualification, take the build of
record from the hosted recipe-bound replay dispatched on the branch at the
candidate head, retain the bundle manifest and the evidence, and maintain
the domain and repository indexes. Nothing here verifies, prepares,
releases or publishes.

No version move is needed: `pyproject.toml` and `se_harness/__init__.py`
already read 0.16.0 (`WO-HUP-016`). The candidate commit is therefore the
commit that retains this work order's evidence and the index maintenance;
its packaged bytes are those of `main`.

## Aggregate scope

The census this work order carries is `REL-SEH-027`'s as re-measured at
approval: the content members in `gates` plus this work order, their
verification contracts, their requirement union, one work-order-keyed
evidence path per member. At the candidate the derivation
`harnessctl release-unit . --from v0.15.0 --to <candidate> --contract REL-SEH-027`
is re-run and recorded; a difference beyond the released `WO-RLS-021`
traced through the #350 merge, the approved `WO-TCM-011` traced through the
#366 merge, and this work order itself is a stop condition.

## In scope

1. Qualification at the candidate, governing 0.15.0 evaluator outside the
   checkout in isolated mode: `validate`, `doctor`, review preflight, the
   handoff check over the Git-derived change set;
   `scripts/validate_release_distributions.py`,
   `scripts/check_portable_release_surface.py` in `--repository`, `--wheel`
   and `--harnessctl` modes; the candidate's `qualify complete-candidate`
   (read from the hosted Linux lane for the `RID018` boundary reason); the
   full suite on Linux (hosted) and on Windows (this workstation); the real
   upgrade rehearsal 0.15.0 to 0.16.0 on both hosted platforms at the
   candidate head.
2. Build of record from the hosted Publication Rehearsal in `candidate`
   mode dispatched on `release/0.16.0` at the bound candidate: two
   byte-identical producer runs on the pinned image; the retained
   `release-build-replay.json` downloaded from that run, its
   `candidate.commit` checked equal to the candidate, its `manifest`
   retained as
   `docs/engineering/release-0-16-0/evidence/RLS-SEH-025-bundle.json` when
   the record is prepared; the digests recorded in this work order's
   evidence as hosted readings.
3. Evidence: this work order's handoff packet under
   `docs/engineering/release-0-16-0/evidence/WO-RLS-022/` with the formal
   snapshot, every reading above, the hosted lanes at the candidate head,
   and any deviation.
4. Index maintenance: `docs/engineering/README.md` domain line,
   `docs/engineering/release-0-16-0/README.md`, and the release note in
   `docs/notes/developing-se-harness.md` if a sequence fact changed.

## Out of scope

- Approval of `REL-SEH-027`; preparation, verification or transition of
  `VREC-SEH-025` and `RLS-SEH-025`; the tag, the GitHub Release, PyPI,
  Pages, the maintenance line, the `last` alias and the latest marker; any
  credential use.
- Any change under `se_harness/`, any managed path, any template, any
  workflow, any test.
- The adoption of 0.16.0 as this repository's root; the start of
  `WO-TCM-011`.

## Authorized decision envelope

The branch name, the order of readings, the evidence and the index lines;
the build host, provided it runs the pinned linux/amd64 producer image
through Docker, which the hosted GitHub runner does. It may not change any
packaged byte, any managed file, any lifecycle state, or write outside the
listed paths.

## Constraints

- Every reading names its evaluator and platform.
- Every commit on the release branch carries the
  `Harness-Work-Order: WO-RLS-022` trailer in its final block, so the
  census at the candidate needs no exemption beyond the four notes-class
  merges the contract names.
- The evidence packet is written in LF bytes; the header parser reads LF at
  offset 0 (`WO-RLS-021`, section 5).
- No promotable distribution leaves this work order; the bundle manifest is
  retained evidence until `RLS-SEH-025` binds it.

## Expected change surface

The domain packet, this work order's evidence, two index files and
possibly one note line.

## Required verification

Execute the candidate-qualification and build-of-record sections of
`REL-SEH-027` in full; repository-required checks; the pull request's
lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/release-0-16-0/evidence/WO-RLS-022/`.

## Stop and escalate conditions

Any work order reaching `implemented` with packaged-surface bytes after
`REL-SEH-027`'s approval; `WO-TCM-011` leaving `approved`; any census
difference beyond the released `WO-RLS-021`, the approved `WO-TCM-011` and
this work order; a hosted producer run that is not byte-identical to its
twin; any hash-locked file in the change set.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
