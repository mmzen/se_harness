+++
id = "REQ-REB-015"
type = "requirement"
title = "Validate publication through an exact predecessor-compatible governance view"
status = "approved"
owners = ["requirements-steward", "repository-owner", "security-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-27"
statement = "WHEN an authorized publication transaction uses a predecessor evaluator that cannot parse retained rejected-bootstrap history, THE SYSTEM SHALL validate the complete governance graph with current semantics and validate an exact read-only compatibility view with that predecessor before any privileged publication stage."
verification_method = "automated-publication-view-provenance-and-zero-mutation-test"

[relations]
derives_from = ["CAP-REB-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T17:29:44Z"
decided_by = "requirements-steward"
+++

# Requirement: Validate publication through an exact predecessor-compatible governance view

## Retirement amendment of 2026-08-27

Retired on 2026-08-27 by `REQ-REB-029` under `WO-REB-028`, on the repository owner's direction, which decided this requirement is superseded. Publication no longer validates a predecessor-compatible view. The last mile and the release-bound Pages build read the complete governance snapshot with current semantics, unconditionally and for every release record; `repository_tools/predecessor_publication.py`, its `scripts/validate_predecessor_publication_view.py` entry point, the `predecessor-view` qualification operation, and the workflow steps that selected a record for a view are deleted. The requirement's own trigger no longer occurs: under `REQ-REB-011` a rejected record is valid but inert, so the 0.6.0 root evaluator parses the complete graph including the retained `RLS-SEH-009`, and `WO-REB-025` measured that the exclusion branch is what every ordinary record takes. The complete-graph validation this requirement also demanded is kept, in `REQ-REB-029`. Everything below records what the publication path did while this requirement was active and is retained unchanged as history; it is no longer an obligation.

The declared `superseded` status is not applied. `docs/engineering/WORKFLOW.json` admits no `approved` to `superseded` transition for a definition, and this artifact carries its own `draft` to `approved` event, which `WFL-005` requires to stay append-only. Setting the status therefore either contradicts that event (`E014`, measured on 2026-08-27) or deletes it. The retirement is recorded here instead, the instrument `WO-REB-028` already uses for `SPEC-REB-003` and `SPEC-REB-005`. Whether the status is applied through a new transition or the definition family gains one is a separate owner decision; the retirement itself does not wait on it.

## Rationale

The authorized `RLS-SEH-012` publication run `32587383130` proved the released 0.5.0 wheel and runtime identity, then failed before all privileged stages because the workflow invoked 0.5.0 validation against the complete main-history graph. That graph intentionally retains rejected `RLS-SEH-009`, which 0.5.0 cannot parse, and also contains the active released successor. The same incompatibility is already governed for release preparation; publication must not misrepresent full-checkout predecessor support or bypass the gate.

## Preconditions and trigger

- One released RLS on trusted `main` binds a candidate, verified evidence, an exact predecessor-preparation view, evaluator evidence, tag, and distribution.
- The preparation-view evidence identifies one immutable rejected RLS/REL pair and canonical sparse specification.
- Exact released evaluator bytes and external runtime identity have passed independently.
- The publication transaction has not entered any contents-write, maintenance, PyPI, Pages, or deployment stage.

## Required response

- Validate the complete committed governance graph with the current repository validator.
- Revalidate the selected released RLS, its preparation-view evidence, current rejected-history bytes, and exact two-path omission.
- Create a temporary detached view at the exact governance commit, omitting only those two paths.
- Run the exact external predecessor `doctor` and `validate` commands against that view and require zero predecessor errors.
- Revalidate the complete graph and prove the source checkout, candidate, tag, RLS, history, root lock, and external state unchanged.
- Emit bounded machine-readable observation suitable for workflow retention.

## Failure and boundary behavior

Any missing, changed, extra, ambiguous, linked, escaped, uncommitted, noncanonical, evaluator-mismatched, or nonzero observation fails before privileged publication jobs. Rerunning the unchanged full-checkout predecessor command is not remediation. A failed observation creates no GitHub Release, maintenance branch, PyPI file, Pages deployment, tag movement, or repository write.

## Constraints

- The complete graph is never claimed to have been parsed by 0.5.0.
- No historical artifact or retained preparation evidence is edited, deleted, moved, or reinterpreted.
- Candidate C6, `v0.6.0`, `RLS-SEH-012`, distribution bytes, schema-2 root state, and released 0.5.0 remain immutable.
- The view adapter receives no credential and performs no network, lifecycle, Git-ref, publication, maintenance, or deployment mutation.

## Acceptance examples

### Example: normal behavior

**Given** current main with released `RLS-SEH-012` and exact rejected `REL-SEH-008`/`RLS-SEH-009`

**When** publication validation runs before privileged jobs

**Then** current validation passes on the complete graph, exact 0.5.0 passes on the derived two-omission view, and the source checkout remains byte-identical.

### Example: failure behavior

**Given** a third omission, changed rejected-history byte, mismatched sidecar, dirty source, or unexpected predecessor diagnostic

**When** publication validation runs

**Then** it fails closed before every privileged job and retains a bounded refusal observation.

## Open decisions

No product decision remains open. Temporary-directory names and helper decomposition are delegated.
