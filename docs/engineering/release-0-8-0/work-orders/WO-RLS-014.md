+++
id = "WO-RLS-014"
type = "work_order"
title = "Cut, qualify and build the se-harness 0.8.0 candidate from main"
status = "in_progress"
owners = ["repository-owner", "release-owner", "quality-owner", "engineering-owner", "security-owner"]
created = "2026-08-28"
updated = "2026-08-28"

[assurance]
commit_bound_verification = "required"
rationale = "Release, package installation, the following evaluator adoption, recipe-bound build replay and credential-free publication rely on the exact candidate, its retained evidence and its reproducible distributions."
decided_by = "repository-owner"

[execution_scope]
paths = ["docs/engineering/README.md", "docs/engineering/release-0-8-0/", "docs/notes/developing-se-harness.md"]

[relations]
implements = ["REQ-DST-006"]
specifications = ["SPEC-DST-001"]
architecture = ["ARCH-DST-001", "ADR-DST-001"]
verification = ["VER-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T15:05:49Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-28 with the words 'approve REL-SEH-019 and WO-RLS-014', as a decision distinct from the approval of REL-SEH-019 taken seconds earlier. Re-measured over the same branch state: every existing member implemented with verified coverage; validate 0 errors; doctor 0 FAIL, governing exact public 0.7.1 evaluator outside the checkout. Approval authorizes start preflight and then only the qualification, recipe-bound Linux build, evidence and index work inside the three declared execution-scope paths. It authorizes no VREC-SEH-016 or RLS-SEH-017 work, no tag, no publication, no deployment, no maintenance-line mutation, no credential use and no root-evaluator upgrade."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-28T15:05:51Z"
decided_by = "engineering-owner"
reason = "Started on 2026-08-28 on the engineering owner's approval and the implementer's announced sequence ('I'll record both and start the candidate'). Start preflight run with the governing exact public 0.7.1 evaluator outside the checkout. REL-SEH-019 is approved, so its ten-work-order gates array is fixed authority and this work order's deferred census resolves to it. Bounded to the three declared execution-scope paths; authorizes no promotable build beyond the declared recipe-bound reproducibility work, no VREC-SEH-016 or RLS-SEH-017 preparation, no tag, no publication, no credential use and no root-evaluator change."
+++

# Work Order: Cut, qualify and build the se-harness 0.8.0 candidate from main

## Lifecycle

This work order requires the accountable owners' approval before start
preflight or any declared work. Its authoritative state, and the timestamp and
reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. It is governed by `REL-SEH-019`, which names it
in `gates`; the contract's approval is a distinct decision from this one.

Commit-bound verification is `required`: the candidate's bytes, its version
identity and its reproducible distributions are what the release record, the
publication and the following governor adoption rely on.

## Objective

Produce the one clean 0.8.0 candidate commit on a branch off `main` at
`ff0e337` or later, prove it with the governing 0.7.1 evaluator and the
candidate's own qualification, build it reproducibly on a Linux host through
the recipe-bound replay, retain the bundle manifest and the evidence, and
maintain the domain and repository indexes. Nothing here verifies, prepares,
releases or publishes.

Unlike `WO-RLS-013`, no version move is needed: `pyproject.toml`,
`se_harness/__init__.py` and the README install line already read 0.8.0
(`WO-HUP-007`), and no migration scenario exists any more (`WO-ECP-010`). The
candidate commit is therefore the commit that retains this work order's
evidence and the index maintenance; its packaged bytes are those of `main`.

## Aggregate scope

The census this work order carries is deferred to `REL-SEH-019`: ten work
orders in `gates`, nine verification contracts, a twelve-requirement union,
eleven work-order-keyed evidence paths. At the candidate the derivation
`harnessctl release-unit . --from v0.7.1 --to <candidate> --contract REL-SEH-019`
is re-run and recorded; any difference from the contract is a stop condition.

## In scope

1. Qualification at the candidate, governing 0.7.1 evaluator outside the
   checkout in isolated mode: `validate`, `doctor`, review preflight, the
   handoff check over the complete changed-path set;
   `scripts/validate_release_distributions.py`,
   `scripts/check_portable_release_surface.py` in `--repository`, `--wheel`
   and `--harnessctl` modes; the candidate's `qualify complete-candidate`;
   the full suite on Linux and on Windows; the real upgrade rehearsal 0.7.1 to
   0.8.0 on both platforms (the hosted lanes at the candidate head).
2. Build of record on a Linux host with the pinned producer image:
   `python -m repository_tools.release_build replay --repository . --commit <candidate> --version 0.8.0 --output-directory <dir> --result <replay.json>`,
   then `scripts/create_release_bundle_manifest.py`, retained as
   `docs/engineering/release-0-8-0/evidence/RLS-SEH-017-bundle.json` when the
   record is prepared; the digests recorded in this work order's evidence.
3. Evidence `docs/engineering/release-0-8-0/evidence/WO-RLS-014-verification.md`
   with the formal snapshot, every reading above, the hosted lanes at the
   candidate head, and any deviation.
4. Index maintenance: `docs/engineering/README.md` domain line,
   `docs/engineering/release-0-8-0/README.md`, and the release note in
   `docs/notes/developing-se-harness.md` if a sequence fact changed.

## Out of scope

- Approval of `REL-SEH-019`; preparation, verification or transition of
  `VREC-SEH-016` and `RLS-SEH-017`; the tag, the GitHub Release, PyPI, Pages,
  the maintenance line, the `last` alias; any credential use.
- Any change under `se_harness/`, any managed path, any template, any
  workflow, any test.
- The adoption of 0.8.0 as this repository's governor and the issue #210
  follow-up deletion; both are later ordinary work orders.

## Authorized decision envelope

The implementation actor may choose the branch name, the evidence wording and
the order of readings. It may not widen `gates`, exempt a further commit, or
change any byte outside `[execution_scope]`; each of those is a stop
condition put to the owner.

## Constraints

- The candidate commit carries the standalone trailer
  `Harness-Work-Order: WO-RLS-014`; the pull request body carries the same.
- The build of record needs a Linux host with the pinned `linux/amd64`
  producer image; a host without it (the drafting workstation has no
  container runtime) cannot produce it, and the hosted
  `release-candidate-replay.yml` dispatch corroborates but does not replace
  the retained local replay.
- Governing evaluator readings come from the exact public 0.7.1 installed
  outside the checkout; the candidate's own readings are labelled candidate.

## Expected change surface

The evidence file, the two index files, and possibly one sentence in the
developer note.

## Required verification

The `VER-DST-001` rows for a candidate build, the repository-required checks,
and the readings listed under In scope; figures labelled per platform.

## Evidence to record

The formal snapshot at the candidate; the census re-derivation at the
candidate against `REL-SEH-019`; every qualification reading; the two
producer runs' digests and the bundle manifest digest; the hosted lane
identifiers at the candidate head; deviations.

## Stop and escalate conditions

Stop if the census at the candidate differs from `REL-SEH-019`'s `gates`, if
any member's coverage is not verified at the candidate, if the two producer
runs differ, if the rehearsal or any lane fails at the candidate head, or if
any path outside scope must change.

## Completion report format

Return the `harnessctl check . --artifact WO-RLS-014 --checkpoint handoff`
schema-2 block verbatim with the complete changed-path set asserted, and its
`result_sha256`.
