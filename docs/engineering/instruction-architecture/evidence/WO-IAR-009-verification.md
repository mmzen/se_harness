# Verification Evidence: WO-IAR-009

## Scope and authority

This evidence supports `WO-IAR-009`, `REQ-IAR-017`, and `VER-IAR-009`. The repository owner approved the complete IAR-009 packet and its bounded amendment to IAR-008 on 2026-08-15 with `ok i approve`. Start preflight passed while the work order was `in_progress`.

This file records implementation evidence only. It does not verify either work order, authorize a commit, prepare or approve a VREC, push, open a pull request, release, publish, or deploy. The intended later VREC must bind both `WO-IAR-008` and `WO-IAR-009`, both verification contracts, both evidence documents, and one exact clean candidate commit.

## Implemented behavior

- Added one top-level `suggestions` array to `se-harness-inspection-v1` without removing or rewriting validation, summaries, queues, or findings.
- Added all six existing queue action classes and the nine actionable derived warning rules enumerated by `SPEC-IAR-009` to a closed static catalog.
- Each suggestion contains exactly `source_kind`, `source_id`, `subjects`, `action`, `message`, `accountable_role`, and `automatic = false`.
- Validator-authority findings, informational observations, and unknown rules remain visible but receive no inferred suggestion.
- Catalog selection reads only existing machine source identifiers, severity, and authority. Repository titles, messages, paths, owners, and evidence cannot select or construct guidance.
- Human output groups repeated catalog advice while JSON preserves one deterministic suggestion per source observation.
- Suggestions contain no executable command, generated repository path, target lifecycle state, deadline, confidence, score, URL, or mutation.
- Root and canonical inspection scripts are byte-identical after the supported managed upgrade; the schema-2 lock records the applied canonical content.

## Test-first evidence

The first focused run failed with four missing-`suggestions` errors and one missing human-section assertion. After implementation, the focused inspection suite passed all nine tests.

The first complete run after lifecycle completion exposed one stale packet test that still expected the pre-completion `approved`/`in_progress` states. The assertion was corrected to the governed final `implemented` states; the focused rerun passed, followed by the clean complete runs reported below.

Affected inspection, instruction-architecture, CLI, and public-onboarding suite:

- 61 tests passed with one expected conditional skip.

Complete regression suites:

- Python 3.11: 183 tests passed with three expected conditional skips.
- Python 3.14.6: 183 tests passed with three expected conditional skips.

The tests cover the exact queue and finding catalog, complete public fields, `automatic = false`, safe omission, hostile repository text, deterministic JSON, compact grouping, control-character escaping, invalid graphs, operational failure, no writes, CLI invocation, standard installation, package data, canonical parity, and existing command compatibility.

## Managed upgrade

The initial upgrade plan refused to adopt a directly edited managed script as customized. The root script was restored to its lock-recorded IAR-008 baseline, after which the supported candidate-source transaction reported only `scripts/inspect_engineering_artifacts.py` as an update and protected the two repository-specific self-hosting controls. `harnessctl upgrade . --apply` updated the managed script and `.engineering-harness.lock`. A second small canonical wording refinement was applied through the same supported transaction.

Final idempotence, doctor, formal validation, real-report determinism, no-write status, review preflight, CLI help, and diff-hygiene results are recorded below after the final lifecycle state is present.

## Final checks

| Check | Result |
| --- | --- |
| formal graph validation | PASS; 329 artifacts, zero errors, and 40 pre-existing maintenance warnings |
| `harnessctl doctor .` | PASS; 82 checks passed, zero failures, and 11 existing non-canonical-location warnings |
| review preflight for `WO-IAR-008` | PASS with the work order `implemented` |
| review preflight for `WO-IAR-009` | PASS with the work order `implemented` |
| managed-upgrade idempotence | PASS; 34 managed entries, 32 unchanged, and the two repository-specific self-hosting controls protected |
| root/canonical inspection-script parity | PASS; byte-identical content |
| CLI parser | PASS; `harnessctl inspect --help` exposes the optional target and `--json` |
| diff hygiene | PASS; no whitespace errors, with only existing Git LF-to-CRLF notices |
| real repository inspection | PASS; valid graph, 329 artifacts, 1,180 relations, 49 unchanged source findings, 23 structured suggestions, two decision items, 12 draft definitions, and zero active work orders |
| deterministic JSON | PASS; two byte-identical runs, SHA-256 `51e259ccf85ac1c974840106a849ff5f8cc18ead6a952f3a56661e14e3cee306` |
| real worktree no-write check | PASS; complete tracked and untracked Git status was byte-identical before and after both inspection runs |

The real report's source findings remain separate: 40 validator maintenance diagnostics plus nine derived warnings. Only supported actionable derived warnings and lifecycle queue entries produce suggestions. The report remains `schema = se-harness-inspection-v1`, `authority = derived`, `producer = repository-local`, and `validation.valid = true`.

## Changed paths attributable to IAR-009

- `docs/engineering/instruction-architecture/requirements/REQ-IAR-016.md`
- `docs/engineering/instruction-architecture/specifications/SPEC-IAR-008.md`
- the six IAR-009 definition, architecture, decision, verification, and work-order artifacts
- `docs/engineering/instruction-architecture/README.md`
- `docs/engineering/instruction-architecture/evidence/WO-IAR-009-verification.md`
- `scripts/inspect_engineering_artifacts.py`
- `templates/repository/standard/scripts/inspect_engineering_artifacts.py`
- `tests/test_inspection.py`
- `tests/test_instruction_architecture.py`
- `docs/notes/harnessctl-reference.md`
- the concise root `README.md` inspect description
- `.engineering-harness.lock`

## Compatibility and deviations

- Inspection remains repository-local derived evidence and exits zero when it successfully reports an invalid graph or attention items; `validate` remains the gate.
- No new validator or Explorer rule, severity, queue condition, score, lifecycle transition, remediation command, network/plugin/model call, evaluator claim, version, wheel, sdist, release record, tag, publication, or deployment was introduced.
- No deviation from the approved catalog or work-order scope was required.

## Residual risks

- Static guidance can identify the intended accountable review path but cannot determine whether an observation matters or whether the suggested action is eligible for the current facts.
- Repository-local execution cannot provide independent-governor assurance; GitHub issue #46 remains the separate evaluator-boundary follow-up.
- Catalog additions and authority-meaning changes require separately governed specification and verification updates.
