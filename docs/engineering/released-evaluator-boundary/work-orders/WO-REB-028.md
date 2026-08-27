+++
id = "WO-REB-028"
type = "work_order"
title = "Retire the predecessor-bootstrap release path and keep its history as inert facts"
status = "in_progress"
owners = ["engineering-owner", "repository-owner", "release-owner", "quality-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[assurance]
commit_bound_verification = "required"
rationale = "The deleted modules gate the authorized last mile and the release-bound Pages build; the qualification surface they publish is a product contract, and the 0.6.0 history they used to check must stay verifiable after they are gone."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "repository_tools/release_bootstrap.py",
  "repository_tools/predecessor_preparation.py",
  "repository_tools/predecessor_publication.py",
  "repository_tools/predecessor_assessment.py",
  "scripts/bind_release_bootstrap.py",
  "scripts/prepare_predecessor_release.py",
  "scripts/validate_predecessor_publication_view.py",
  "scripts/assess_predecessor_evaluator.py",
  "scripts/check_portable_release_surface.py",
  "se_harness/cli.py",
  "se_harness/release_qualification.py",
  "se_harness/interpreter_safety.json",
  ".github/scripts/publish_dashboard.py",
  ".github/workflows/publish-pypi.yml",
  ".github/workflows/pages-publication.yml",
  "tests/",
  "docs/notes/developing-se-harness.md",
  "docs/notes/harnessctl-reference.md",
  "docs/engineering/released-evaluator-boundary/",
]

[relations]
implements = ["REQ-REB-029"]
specifications = ["SPEC-REB-013"]
architecture = ["ARCH-REB-012", "ADR-REB-012"]
verification = ["VER-REB-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T16:43:16Z"
decided_by = "engineering-owner"
reason = "Approved on 2026-08-27 by the accountable owner, 'I approve the artifacts', on the read-only sweep of 2026-08-27 following issue #190: authorizes only the declared work inside the execution scope: twelve deletions, eight edited files, the supersession of REQ-REB-012, REQ-REB-015 and SPEC-REB-007, the amendment of SPEC-REB-003 and SPEC-REB-005, the two notes, evidence and packet index. No byte of scripts/validate_engineering_artifacts.py, its templates copy, or se_harness/hash_bound_classes.json. Start preflight, completion, commit-bound verification, release and adoption are separate accountable acts."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-27T16:56:39Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's decision of 2026-08-27, 'you can start'; start preflight PASS with the exact public 0.6.0 evaluator outside the checkout on branch governance/reb-028-retire-predecessor-bootstrap off main f605e58."
+++

# Work Order: Retire the predecessor-bootstrap release path and keep its history as inert facts

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification and any release decision are separate accountable acts.

## Objective

Carry out `ADR-REB-012`: the repository has exactly one mechanism for a
predecessor-to-successor handover, `se_harness/governance_migration.py`, and
no second one. The contract-bound `[bootstrap]` tuple, the predecessor
compatibility view, and the four `repository_tools` modules that build and run
them are retired. The closed 0.6.0 bootstrap history stays on disk with its
hash-bound evidence digests intact and is no longer re-derivable.

The path being retired was authored for one event: retaining the rejected
`REL-SEH-008` / `RLS-SEH-009` pair while released 0.5.0, which emits `E009`
on `status = "rejected"`, still had to judge the 0.6.0 release. `REQ-REB-011`
made rejected history inert in 0.6.0, so no later release needs the view.
0.7.0 proved it: `RLS-SEH-014` was rejected and `RLS-SEH-015` released under
the 0.6.0 governor with no view at all. Both remaining call sites already
take their exclusion branch for every ordinary record.

## In scope

- Delete `repository_tools/release_bootstrap.py`,
  `predecessor_preparation.py`, `predecessor_publication.py` and
  `predecessor_assessment.py` with their four test modules
  (`test_release_bootstrap.py`, `test_predecessor_preparation.py`,
  `test_predecessor_publication.py`,
  `test_predecessor_assessment_contract.py`).
- Delete the four entry-point scripts: `bind_release_bootstrap.py`,
  `prepare_predecessor_release.py`, `validate_predecessor_publication_view.py`
  and `assess_predecessor_evaluator.py`.
- `release_qualification.py`, `cli.py`: retire the `predecessor-view`
  qualification operation and its `PV001` and `PV002` checks; the codes stay
  reserved. The operation lazily imports `repository_tools`, which
  `pyproject.toml` does not package, so it has never been usable from an
  installed evaluator.
- `check_portable_release_surface.py`: drop `predecessor-view` from the
  required qualification operations.
- `interpreter_safety.json`: drop the two declared sites naming
  `predecessor_assessment.py` and `predecessor_preparation.py`.
- `publish-pypi.yml`, `pages-publication.yml`: delete the selector, the
  predecessor-view step and the exclusion observation. The Pages build reads
  the complete governance snapshot unconditionally, which is what the
  exclusion branch already produces under `WO-REB-026`.
- `publish_dashboard.py`: drop the release-bootstrap contract validation and
  its evaluator and rejected-pair cross-checks. The
  `harness-dashboard-bootstrap-v2` payload is a different schema and is not
  touched.
- Supersede `REQ-REB-012` and `REQ-REB-015` by direct edit (Supersession
  section, as `REQ-DST-008`). Supersede `SPEC-REB-007`. Amend `SPEC-REB-003`
  and the predecessor-view rules of `SPEC-REB-005` with a dated paragraph,
  keeping their rejected-succession rules, which `REQ-REB-010` and
  `REQ-REB-011` still require.
- Tests for every case `VER-REB-012` lists; the two notes; evidence; packet
  index.

## Out of scope

`scripts/validate_engineering_artifacts.py` and its
`templates/repository/standard/` copy. The root file is a hash-locked managed
copy of released 0.6.0 and cannot be edited from candidate source; the
template change ships in a later release and reaches the root only at the
next governor adoption. Both validator entry points are already conditional
(`if "bootstrap" in artifact.metadata`, and an immediate return when
`preparation_schema` is absent), so leaving the rules in place changes no
verdict. `REQ-REB-010` retires with them, in that later work order.

Also out of scope: `repository_tools/predecessor_facts.py`, which carries no
bootstrap dependency and runs on every push and pull request;
`se_harness/governance_migration.py`; `se_harness/hash_bound_classes.json`,
whose `evaluator-evidence` and `standard-lock` classes keep
`preparation_view_evidence_sha256`, `evaluator_evidence_sha256` and
`from_lock_sha256` enforced after the machinery is gone; the bytes of
`REL-SEH-008`, `REL-SEH-009`, `REL-SEH-010`, `REL-SEH-011`, `RLS-SEH-009` and
`RLS-SEH-012`; `scripts/validate_governor_transition.py` and the
`predecessor-evaluator-assessment` lane, which are the live governor
transition and do not use bootstrap; releasing the result; adopting it.

## Authorized decision envelope

Whether the retired qualification operation is removed from the subparser or
kept as a refusing stub that names its replacement; how the Pages view step
is expressed once its branch disappears; which residual helpers of the four
deleted modules other retained callers need re-homed, and where; test fixture
layout.

## Constraints

No credential, network write, or root change of this repository; the root
stays exact public 0.6.0 and every lifecycle act uses it. No historical
artifact byte, digest, lock, tag, or evidence file changes. The
`harness-dashboard-bootstrap-v2` Explorer payload is a distinct schema and
must keep working. No managed path is written. `REQ-REB-010` and
`REQ-REB-011` keep their force: the closed pair remains present, validated by
the unchanged root validator, and hash-bound.

## Expected change surface

Twelve files deleted (6,393 lines: four `repository_tools` modules, four
`scripts` entry points, four test modules), eight files edited, two notes, two
requirement supersessions, one specification supersession, two specification
amendments, evidence, packet index.

## Required verification

`VER-REB-012` in full; repository-required checks; full suites on both
runtimes with no import of a deleted module surviving; the candidate graph
valid under the exact public 0.6.0 evaluator from outside the checkout, with
the six closed 0.6.0 artifacts still validating and their evidence digests
still bound; `publication-rehearsal` and `release-qualification` lanes green;
a dry `publish-pypi.yml` and `pages-publication.yml` review proving no step
references a deleted path; handoff check.

## Evidence to record

`docs/engineering/released-evaluator-boundary/evidence/WO-REB-028-verification.md`,
recording the deleted-path set with pre-deletion blob identities, the
before-and-after artifact, error and warning counts from the released
governor, and the retained digests of the six closed 0.6.0 artifacts.

## Stop and escalate conditions

Stop if any released-governor verdict on the closed 0.6.0 history changes; if
a deleted module turns out to be reachable from a lane other than the four
entry points; if the Pages build cannot produce the public Explorer without
the exclusion branch; if removing the qualification operation would break a
published release contract's declared surface; or if a release packet is in
flight whose frozen allow-list this scope would reopen.

## Completion report format

The `harnessctl check . --artifact WO-REB-028 --checkpoint handoff` schema-2
block verbatim with the complete changed-path set, and its `result_sha256`.
