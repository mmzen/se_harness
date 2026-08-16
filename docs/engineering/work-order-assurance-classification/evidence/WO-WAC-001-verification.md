# WO-WAC-001 implementation and verification evidence

## Scope and authority

This evidence records the implementation authorized when the repository owner instructed `ok go` on 2026-08-16. It covers only the accepted WAC packet. No commit, push, pull request, VREC creation or transition, release, tag, publication, or deployment is asserted here.

## Delivered behavior

- Added the exact work-order `[assurance]` contract with `required` and `not_required` classifications, bounded rationale and deciding-role strings, closed keys, and governance diagnostic `E019`.
- Required a valid declaration for approved and in-progress work while retaining completed/disposed legacy compatibility. A malformed present declaration is rejected in every lifecycle state.
- Made start and review preflight display the classification, rationale, and deciding role. Explicitly selecting legacy or malformed work without a valid declaration fails read-only with `W023`; no default is inserted.
- Versioned inspection output to `se-harness-inspection-v2` and added `assurance_pending` for implemented, explicitly required work lacking direct ready, verified, or released VREC coverage.
- Excluded missing legacy and explicit `not_required` work from inferred assurance obligations. Superseded, draft, and rejected records do not clear pending work.
- Added the closed, non-automatic `prepare-commit-bound-verification` suggestion owned by `engineering-owner`. It selects no scope, generates no ID or command, creates no record, and exercises no assurance authority.
- Preserved capture-verification, exact commit binding, VREC transitions, supersession, release coverage, work-order lifecycle, and evidence behavior.
- Updated canonical and active workflow, traceability catalog, work-order template, validator, inspector, CLI/operator notes, lifecycle guidance, and the schema-2 managed lock through the supported transactional upgrade. Protected self-hosting configuration and workflow remained unchanged.

## Verification matrix

| Concern | Result |
| --- | --- |
| Valid `required` and `not_required` tables | PASS; values and strings normalize without judging the claim |
| Absent declaration by lifecycle | PASS; `approved` and `in_progress` fail `E019`; draft and completed/disposed legacy states remain compatible |
| Malformed present declaration | PASS; scalar, partial, unknown value/key, blank, and oversized variants fail deterministically in the governance plane |
| Non-work-order declaration | PASS; rejected as work-order-only metadata |
| Start/review preflight | PASS; valid decision projected; missing actionable work emits `A-E019` and `W023`; completed legacy selection emits `W023` without changing graph compatibility |
| Pending assurance state matrix | PASS; required implemented work remains pending with absent or superseded-only coverage; ready, verified, or released direct coverage clears it |
| Aggregate ready coverage | PASS; covered work leaves pending and the ready VREC remains one accountable review item |
| Suggestion authority | PASS; deterministic, non-automatic, bounded action with no shell command, URL, generated identifier, or inferred aggregate membership |
| Managed distribution | PASS; root/canonical parity and lock reconciliation; `doctor` reports every distribution and managed-integrity check passing |
| Formal repository validation | PASS in final implemented state; 374 artifacts, 0 errors, 40 unchanged maintenance warnings |
| Review preflight | PASS for implemented `WO-WAC-001`; the dedicated section reports `required`, `repository-owner`, and the recorded rationale |
| Deterministic inspection | PASS; two byte-identical `se-harness-inspection-v2` reports, SHA-256 `5dcb90f39a066e1243d0ef27801d8c405f703d4cea41eb107ee12cbaa7fffbf1`; `WO-WAC-001` is the sole `assurance_pending` subject |
| Deterministic Harness Explorer | PASS; two current-repository runs produced 374 artifacts, 1,352 relations, 0 errors, 40 warnings, and identical snapshot `8f296ab521f093419fafaa6d5eaf33ef77eba5e9b512c9cda61d519c886e28fe` |
| Focused tests | PASS; 73 tests, 1 expected skip across assurance, inspection, preflight, architecture, CLI, and distribution-adjacent suites |
| Full Python 3.14.6 suite | PASS after final status and evidence changes; 201 tests, 3 expected skips |
| Full Python 3.11.9 suite | PASS; 201 tests, 3 expected skips |
| Candidate managed-upgrade plan | PASS; 34 entries, 32 unchanged, 2 protected self-hosting controls, no pending managed update |
| Diff hygiene | PASS; `git diff --check` reported only configured Windows line-ending notices and no whitespace errors |

## Compatibility and security observations

- No historical completed work order was bulk-classified or rewritten.
- The inspector reads assurance metadata from the existing validated artifact catalog, so the Harness Explorer snapshot schema did not change.
- Repository-provided rationale and role strings remain claims, not authenticated identity or executable guidance. Human rendering continues to JSON-escape terminal controls.
- The independently released governor remains the active CI authority. These candidate-source results are implementation evidence and do not allow the candidate to govern itself.

## Authorized verification deviation

No wheel or sdist was built. `REPOSITORY_CONTEXT.md` restricts the distribution build command to an approved release work order, while `WO-WAC-001` explicitly excludes release and publication. Candidate package-data, fresh-init, adoption, safe-upgrade, lock, parity, and installed-command behavior remain exercised by the complete regression suite; exact wheel acceptance is deferred to later release qualification rather than expanding this work order's authority.

## Residual risk

The harness can validate that a decision was explicitly and correctly shaped; it cannot prove that the rationale is honest, that the named role corresponds to the actor, or that the accountable owner chose the appropriate classification. Review and repository access controls remain necessary.

## Candidate and later assurance

`WO-WAC-001` is explicitly classified `required`. Inspection therefore reports it for commit-bound follow-up after implementation until a directly covering ready VREC exists. A separately authorized clean candidate commit must contain this implementation and evidence before `capture-verification` can truthfully bind that commit.
