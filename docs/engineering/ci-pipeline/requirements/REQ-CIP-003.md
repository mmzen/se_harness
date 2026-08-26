+++
id = "REQ-CIP-003"
type = "requirement"
title = "Define the release qualification once and invoke it from both the rehearsal and the release"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-26"
updated = "2026-08-26"
statement = "THE SYSTEM SHALL execute the release qualification from one reusable definition invoked by both the publication-rehearsal lane and the publication workflow, with no separate declaration of step digests to keep aligned."
verification_method = "automated-workflow-inspection-and-rehearsal-run"
[relations]
derives_from = ["CAP-CIP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T15:17:28Z"
decided_by = "requirements-steward"
+++

# Requirement: Define the release qualification once and invoke it from both the rehearsal and the release

## Rationale

`rehearse_publication.py` (3,187 lines) re-implements the `qualify` leg of
`publish-pypi.yml` and proves alignment with it by parsing the YAML with a
hand-written 300-line subset parser and comparing `sha256` values of each
normalized `run:` body against `publication_rehearsal_mechanics.json`. Any
edit to a `run:` body turns the lane red until the digests are regenerated.
The script is stdlib-only and so re-implements duplicate-key JSON loading,
file hashing and a GitHub client that also exist in the package and in the
other scripts; `publish_release.py classify-pypi` is wired but never called
because the workflow re-implements it inline.

## Preconditions and trigger

Always; observed on every pull request (rehearsal) and every release
dispatch (publication).

## Required response

- The qualification leg (export, pinned build tools,
  `qualify complete-candidate`, unit suite, CLI smoke, build, normalize,
  byte comparison, bundle manifest, both `publish_release.py`
  verifications) becomes a `workflow_call` reusable workflow with inputs for
  mode (`candidate` or `release-record`), record identifier and platform.
- `publication-rehearsal.yml` and `publish-pypi.yml` both call it. The
  `divergence` job, `_WorkflowReader`, the PyYAML cross-check and
  `publication_rehearsal_mechanics.json` are removed.
- `.github/scripts/*.py` import `se_harness` and `repository_tools` for
  canonical JSON, duplicate-key refusal and hashing; each helper exists once.
  `reconcile_maintenance_branch.py` uses `gh api`. `classify-pypi` replaces
  the inline `curl`/`jq` classification or is deleted.
- What the rehearsal executes is, by construction, what the release executes.

## Failure and boundary behavior

The rehearsal keeps running credential-free; the reusable workflow declares
`permissions: contents: read` and receives no secret. A mode it does not
know fails at input validation.

## Constraints

`WO-RLO-005`'s outcome — that the last mile is rehearsed before approval —
is preserved; only its mechanism changes. `CAP-RLO-003` stays satisfied.
The `pypi` environment and `id-token: write` remain in the caller only.

## Acceptance examples

**Given** a pull request that edits one `run:` body in the qualification
**When** the rehearsal runs
**Then** it executes the edited body and passes or fails on its behaviour,
with no digest comparison.

**Given** `.github/scripts/`
**When** counted
**Then** `rehearse_publication.py` and `publication_rehearsal_mechanics.json`
are gone and the directory is at least 2,500 lines smaller than at
`e98b788`.

## Open decisions

None.
