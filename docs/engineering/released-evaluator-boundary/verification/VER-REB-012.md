+++
id = "VER-REB-012"
type = "verification"
title = "Retired predecessor-bootstrap surface and retained-history assurance"
status = "approved"
owners = ["quality-owner", "security-owner", "release-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
verifies = ["REQ-REB-029"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T16:43:16Z"
decided_by = "quality-owner"
reason = "Approved on 2026-08-27 by the accountable owner, 'I approve the artifacts', on the read-only sweep of 2026-08-27 following issue #190: static review of the two dispatch-only workflows is explicitly insufficient evidence, a dispatch-mode rehearsal of publish-pypi.yml and pages-publication.yml is required, and leaving both validate_engineering_artifacts.py copies byte-identical is a pass condition rather than an omission."
+++

# Verification Contract: Retired predecessor-bootstrap surface and retained-history assurance

## Amendment of 2026-08-28 (`WO-REB-030`)

The two conditions naming `se_harness/interpreter_safety.json` are retired with the declaration (`SPEC-REB-015`); the remaining conditions are unchanged.

## Independence

The retained-history cases run the exact public 0.6.0 evaluator from a virtual
environment outside the checkout with `-I`; the candidate checkout supplies the
tree under judgment and nothing else. The absence cases are static and read
the tree, not the test suite's own imports. The installed-surface case runs
against a built candidate wheel installed outside the checkout, never against
candidate source.

A verification that only ran the candidate suite would prove nothing here:
the suite's coverage of this path is exactly what is being deleted.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-REB-029 | static absence scan of the worktree | every deleted path; every import of a deleted module; every retired schema name and code | no deleted path exists, no retained file imports a deleted module, no retained file names a retired schema outside retained history and reserved-name declarations |
| REQ-REB-029 | released-governor validation before and after | exact public 0.6.0 evaluator outside the checkout, at the parent commit and at the candidate | artifact, error and warning counts differ only by this packet's own added artifacts; zero errors; the closed 0.6.0 artifacts are among the validated set |
| REQ-REB-029 | hash-bound re-verification | `RLS-SEH-012`'s `evaluator_evidence_sha256` and `preparation_view_evidence_sha256`; `REL-SEH-011`'s `from_lock_sha256` | every digest still verifies against its bound file at the candidate |
| REQ-REB-029 | installed-surface check | `check_portable_release_surface.py` against a candidate wheel installed outside the checkout | `rehearse-migration`, `released-root`, `complete-candidate`, `candidate-package` and `public-install` present; `predecessor-view` absent |
| REQ-REB-029 | workflow static review | `publish-pypi.yml`, `pages-publication.yml`, `publish_dashboard.py` | no step references a deleted path, selects a record for a view, or branches on a `[bootstrap]` tuple; no exclusion observation is written |
| REQ-REB-029 | hosted lanes | the pull request's own lanes plus `publication-rehearsal` and `release-qualification` | green, with the Pages build producing the same public Explorer content as `RLS-SEH-015` did on the exclusion branch |

## Required cases

- Each of the twelve deleted paths is absent from the worktree, and its
  pre-deletion Git blob identity is recorded in the evidence document.
- No retained Python file imports `release_bootstrap`,
  `predecessor_preparation`, `predecessor_publication` or
  `predecessor_assessment`. The scan covers `se_harness/`,
  `repository_tools/`, `scripts/`, `.github/scripts/`, `tests/` and
  `templates/`.
- `repository_tools/predecessor_facts.py` is present and imports none of
  them, and the `candidate-evidence` lane that runs it is green.
- `scripts/validate_governor_transition.py` is present and unchanged, and the
  `predecessor-evaluator-assessment` lane is green — the deletion of
  `predecessor_assessment.py` does not touch the live governor-transition
  lane.
- `se_harness/interpreter_safety.json` declares no site naming a deleted
  file, and every site it still declares resolves to a present file.
- `harnessctl qualify --help` from an installed candidate wheel offers no
  `predecessor-view` operation; `PV001` and `PV002` are emitted by no path and
  are still reserved.
- `se_harness/hash_bound_classes.json` is byte-identical to its parent-commit
  content, and `se_harness/hash_bound.py` imports no deleted module.
- The six closed 0.6.0 artifacts are byte-identical to their parent-commit
  content, `[bootstrap]` tables and `preparation_schema` markers included.
- The `harness-dashboard-bootstrap-v2` payload still generates: the Explorer
  renders from `generate_harness_dashboard.py` and
  `harness_explorer/index.template.html` unchanged.
- Negative: a fixture release contract carrying a `[bootstrap]` table is
  selected by no step, grants no authority, and causes no refusal.
- Negative: `scripts/validate_engineering_artifacts.py` and
  `templates/repository/standard/scripts/validate_engineering_artifacts.py`
  are byte-identical to their parent-commit content. Editing either is out of
  scope and its absence from the changed-path set is a pass condition, not an
  omission.

## Acceptance scenarios

1. **Ordinary release, retired surface.** Replay `RLS-SEH-015`'s publication
   and Pages build on the candidate. Both read the complete governance
   snapshot, neither selects a view, and the Explorer output matches.
2. **Retained history under the governor.** Validate the candidate with the
   exact public 0.6.0 evaluator from outside the checkout. Zero errors; the
   closed pair and `RLS-SEH-012` validate; the three bound digests verify.
3. **Nothing re-derivable.** No command in the tree reconstructs a
   predecessor view or re-derives the 0.6.0 preparation or publication
   evidence. This is a pass condition, not a defect.

## Property and invariant tests

- No retained module imports a deleted module (import-barrier property, the
  same shape the existing barrier tests use for `repository_tools` crossing
  into `se_harness`).
- Every path declared in `se_harness/interpreter_safety.json` exists.
- Every hash-bound field named in `se_harness/hash_bound_classes.json`
  resolves for every artifact that carries it.
- Retired schema names and reserved codes appear only in retained history and
  in the declarations that reserve them.

## Static and architecture checks

`ARCH-REB-012`'s prohibited patterns: no projection, view, sparse checkout or
omitting clone of this repository is constructed for any evaluator; no release
step branches on a contract-declared predecessor evaluator; no packaged
product module reaches for a repository-only module.

## Security and privacy checks

The removed boundary crossing is absent: no temporary clone of this
repository is created for an evaluator to read, so the symbolic-link
traversal, sparse-policy substitution and credential-leakage refusals the
deleted modules carried have nothing left to refuse. `RID018` isolation and
`RID021` payload proof are unchanged and still exercised by their own
verifications.

## Hosted evidence

The pull request's lanes, plus `publication-rehearsal` and
`release-qualification` in both modes. Because the retired path ran only on
`workflow_dispatch`, a dispatch-mode rehearsal of `publish-pypi.yml` and
`pages-publication.yml` on the candidate branch is required, not optional:
static review of those two files is not sufficient evidence on its own.

## Evidence retention

`docs/engineering/released-evaluator-boundary/evidence/WO-REB-028-verification.md`,
recording the twelve deleted paths with their pre-deletion blob identities,
the before-and-after governor counts, the three re-verified digests, the
installed-surface operation list, and the dispatch-mode lane results.
