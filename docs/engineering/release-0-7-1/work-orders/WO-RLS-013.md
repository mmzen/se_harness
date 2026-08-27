+++
id = "WO-RLS-013"
type = "work_order"
title = "Cut, qualify and build the se-harness 0.7.1 candidate from main"
status = "approved"
owners = ["repository-owner", "release-owner", "quality-owner", "engineering-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[assurance]
commit_bound_verification = "required"
rationale = "Release, package installation, the following evaluator adoption, recipe-bound build replay and credential-free publication rely on the exact candidate, its retained evidence and its reproducible distributions."
decided_by = "repository-owner"

[execution_scope]
paths = ["pyproject.toml", "se_harness/__init__.py", "README.md", "tests/fixtures/governance_migration/", "tests/test_ci_pipeline.py", "tests/test_governance_migration.py", "docs/notes/developing-se-harness.md", "docs/engineering/README.md", "docs/engineering/release-0-7-1/"]

[relations]
implements = ["REQ-DST-006"]
specifications = ["SPEC-DST-001"]
architecture = ["ARCH-DST-001", "ADR-DST-001"]
verification = ["VER-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T16:06:39Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-27 with the words 'Approve and start', as a decision distinct from the approval of REL-SEH-018. Re-measured immediately before this transition over branch state f022e5c carrying unmoved main f605e58: the four existing members WO-REB-024 through WO-REB-027 all implemented with verified coverage VREC-REB-021 through VREC-REB-024; no work order reached implemented since the packet was drafted; no ready record beyond the two canonical templates; validate PASS at 978 artifacts, 0 errors, 53 pre-existing maintenance warnings; doctor 0 FAIL, governing exact public 0.6.0 evaluator outside the checkout. Approval authorizes start preflight and then only the declared version move, scenario, qualification, recipe-bound Linux build, index-maintenance and retained-evidence work inside the nine declared execution-scope paths. It authorizes no contract approval, no VREC-SEH-015 or RLS-SEH-016 work, no tag, no publication, no deployment, no maintenance-line mutation, no credential use and no root-evaluator upgrade. Start preflight has not been run."
+++

# Work Order: Cut, qualify and build the se-harness 0.7.1 candidate from main

## Lifecycle

This work order requires the accountable owners' approval before start
preflight or any declared work. Its authoritative state, and the timestamp and
reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. It is governed by `REL-SEH-018`, which names it
in `gates`; the contract's approval is a distinct decision from this one.

Commit-bound verification is `required`: the candidate's bytes, its version
identity and its reproducible distributions are what the release record, the
publication and the following governor adoption rely on.

## Objective

Produce the one clean 0.7.1 candidate commit on a branch off `main` at
`f605e58` or later, prove it with the governing 0.6.0 evaluator and the
candidate's own qualification, build it reproducibly on a Linux host through
the recipe-bound replay, retain the bundle manifest and the evidence, and
maintain the domain and repository indexes. Nothing here verifies, prepares,
releases or publishes.

## Aggregate scope

The census this work order carries is deferred to `REL-SEH-018`: five work
orders in `gates`, four verification contracts, six requirements, five
work-order-keyed evidence paths. At the candidate the derivation
`harnessctl release-unit . --from v0.7.0 --to <candidate> --contract REL-SEH-018`
is re-run and recorded; any difference from the contract is a stop condition.

## In scope

1. Version identity: `pyproject.toml` and `se_harness/__init__.py` to `0.7.1`;
   the README install line to `se-harness==0.7.1`.
2. Governance-migration scenario: write
   `tests/fixtures/governance_migration/candidate-0.6.0-to-0.7.1.json` with
   `python -m repository_tools.predecessor_facts write-scenario --repository . --template tests/fixtures/governance_migration/candidate-0.6.0-to-0.7.0.json`
   and retire the 0.7.0 pair; move the tests that pin the candidate version
   (`tests/test_ci_pipeline.py`, `tests/test_governance_migration.py`).
3. Qualification at the candidate, governing 0.6.0 evaluator outside the
   checkout in isolated mode: `validate`, `doctor`, review preflight, the
   handoff check over the complete changed-path set;
   `scripts/validate_release_distributions.py`,
   `scripts/check_portable_release_surface.py`; the candidate's
   `qualify complete-candidate`; the full suites on CPython 3.14 and 3.11;
   `rehearse-migration` on the new scenario.
4. Build of record from WSL Ubuntu: `python -m repository_tools.release_build replay --repository . --commit <candidate> --version 0.7.1 --output-directory <dir> --result <replay.json>`,
   then `scripts/create_release_bundle_manifest.py`, retained as
   `docs/engineering/release-0-7-1/evidence/RLS-SEH-016-bundle.json` when the
   record is prepared; the digests recorded in this work order's evidence.
5. Evidence `docs/engineering/release-0-7-1/evidence/WO-RLS-013-verification.md`
   with the formal snapshot, every reading above, the hosted lanes at the
   candidate head, and any deviation.
6. Index maintenance: `docs/engineering/README.md` domain line,
   `docs/engineering/release-0-7-1/README.md`, and the release note in
   `docs/notes/developing-se-harness.md` if a sequence fact changed.

## Out of scope

- Approval of `REL-SEH-018`; preparation, verification or transition of
  `VREC-SEH-015` and `RLS-SEH-016`; the tag, the GitHub Release, PyPI, Pages,
  the maintenance line, the `last` alias; any credential use.
- Any change under `se_harness/` other than `__init__.py`'s version string,
  any managed path, any template, any workflow.
- The adoption of 0.7.1 as this repository's governor; that is a later
  ordinary work order.

## Authorized decision envelope

The implementation actor may choose the branch name, the evidence wording and
the order of readings. It may not widen `gates`, exempt a further commit, or
change any byte outside `[execution_scope]`; each of those is a stop
condition put to the owner.

## Constraints

- The version and the scenario move in one change (`MIG211`, `SPEC-REB-008`
  rule 4); the scenario is written by the canonical writer, never by hand.
- The candidate commit carries the standalone trailer
  `Harness-Work-Order: WO-RLS-013`; the pull request body carries the same.
- The build of record is produced on a Linux host; a Windows-produced bundle is
  never bound.
- The candidate branch is merged into `main` by a merge commit, never rebased,
  because `VREC-SEH-015` binds the candidate commit.

## Expected change surface

`pyproject.toml`, `se_harness/__init__.py`, `README.md`, one scenario added
and one removed under `tests/fixtures/governance_migration/`, the two version
pinning tests, `docs/engineering/README.md`, and the files of
`docs/engineering/release-0-7-1/`.

## Required verification

`VER-DST-001` applies. Handoff check `Completed` on the governing 0.6.0
evaluator and on the candidate over the complete changed-path set; the
readings listed under In scope, item 3; two byte-identical Linux producer runs
under item 4; all pull-request lanes `success` at the candidate head.

## Evidence to record

`docs/engineering/release-0-7-1/evidence/WO-RLS-013-verification.md`: formal
snapshot, evaluator identities, every command and its result, the wheel and
sdist digests, the hosted run identifiers, the re-run release-unit derivation,
deviations and their owner answers.

## Stop and escalate conditions

- A work order reaches `implemented` with packaged-surface bytes after
  `REL-SEH-018`'s approval.
- The release-unit derivation at the candidate differs from the contract.
- The two producer runs differ, or the hosted replay differs from the
  workstation build.
- Any reading above fails on the candidate.

## Completion report format

The evidence file above, the candidate commit, and the handoff `check`
restitution; the completion decision is the engineering owner's.
