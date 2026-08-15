+++
id = "SPEC-IAR-008"
type = "specification"
title = "Deterministic repository inspection report"
status = "implemented"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
specifies = ["REQ-IAR-016"]
+++

# Specification: Deterministic repository inspection report

## Lifecycle

Approved on 2026-08-15 through the repository owner's instruction `go for implementation` as part of the complete `IAR-008` packet. Clarified on 2026-08-15 through the separately governed `IAR-009` approval `ok i approve`: top-level suggestions governed by `SPEC-IAR-009` are permitted, while findings themselves remain unchanged and free-form or automatic recommendations remain prohibited.

## Scope

Add one read-only command, `harnessctl inspect [TARGET] [--json]`, that turns the existing validation report and Harness Explorer snapshot into a terminal-oriented attention report. The IAR-008 baseline adds presentation and lifecycle queues only; it adds no validation or Explorer finding rule. The separately governed IAR-009 extension may add a closed top-level suggestion projection without changing those sources or their authority.

## Actors and inputs

- The actor is a human operator or coding agent inspecting an installed repository.
- `TARGET` defaults to the current directory.
- `--json` selects the machine-readable contract.
- Repository artifacts, relations, evidence references, Git metadata, experiment files, titles, paths, and diagnostic text are untrusted input and are never executed or interpreted as terminal control.

## Behavioral rules

1. The CLI resolves and executes the target repository's managed `scripts/inspect_engineering_artifacts.py` using the same bounded repository-script mechanism as `validate` and `dashboard`.
2. The inspection script reuses `generate_harness_dashboard.generate_snapshot`, which in turn reuses `validate_repository`; it does not independently parse formal artifacts or recreate Explorer findings.
3. JSON uses schema identifier `se-harness-inspection-v1` and contains:
   - repository identity and observed revision from the snapshot;
   - formal validity, diagnostic counts, taxonomy version, and four-plane counts;
   - artifact, relation, and finding counts;
   - deterministic queues described below;
   - `authority = "derived"` and `producer = "repository-local"`.
4. `decision_required` contains every artifact whose declared status is `ready`.
5. `definition_pending` contains every artifact whose declared status is `draft`.
6. `active_work` contains every work order whose declared status is `approved` or `in_progress`.
7. `findings` preserves each existing snapshot finding's rule, severity, authority, message, artifacts, paths, and evidence. Findings do not embed a replacement severity or recommendation; any separate top-level suggestion must conform to `SPEC-IAR-009`.
8. Queue entries expose only stable discovery fields: ID, type, title, status, path, owners, and a mechanical action class derived from type and status.
9. Arrays are sorted by documented stable keys; JSON uses UTF-8, sorted object keys, two-space indentation, and one final newline. It contains no generation timestamp or absolute repository path.
10. Human output presents the same counts and queues in compact sections, retains finding IDs and severity, and ends with the derived-authority boundary. It contains no percentage or aggregate score.
11. Successfully producing a report exits zero even when the embedded validation result is invalid or attention queues are non-empty. Missing scripts, unsafe targets, unreadable input, malformed snapshot data, or rendering failure exit nonzero with a concise error. Operators use `harnessctl validate` when gate exit behavior is required.
12. The command creates, edits, deletes, approves, transitions, commits, pushes, publishes, or deploys nothing.

## Mechanical action classes

| Queue | Condition | Action class |
| --- | --- | --- |
| `decision_required` | any artifact in `ready` | `assurance-review` for VREC, `release-review` for RLS, otherwise `accountable-review` |
| `definition_pending` | any artifact in `draft` | `complete-definition` |
| `active_work` | approved work order | `start-authorized-work` |
| `active_work` | in-progress work order | `continue-authorized-work` |

These labels aid navigation only. They do not infer eligibility or authorize the named action.

## Compatibility

- `validate`, `dashboard`, `doctor`, and `preflight` behavior and output remain unchanged.
- Existing dashboard snapshot and finding schemas remain unchanged.
- The standard consumer installation gains the inspection script, CLI command, command-reference entry, tests, and matching lock metadata.
- Python 3.11+ standard-library-only behavior remains required.

## Explicitly unspecified decisions

Exact whitespace and decorative punctuation in human output may be chosen during implementation. Filtering, remediation, configurable thresholds, new findings, and dashboard redesign are not delegated implementation choices and remain out of scope.
