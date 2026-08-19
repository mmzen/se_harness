# Verification Evidence: WO-DOC-013

Date: 2026-08-19

## Authority and scope

The accountable owner instructed `I approve REQ-DST-060, SPEC-DST-017, VER-DST-017, and WO-DOC-013 for implementation`. Start preflight returned `ready: true` with no diagnostics. Before the original implementation, the agent read the complete returned manifest:

1. `ENGINEERING_HARNESS.md`
2. `docs/engineering/REPOSITORY_CONTEXT.md`
3. `docs/engineering/README.md`
4. `docs/engineering/WORKFLOW.md`
5. `docs/engineering/DECISION_RIGHTS.md`
6. `docs/engineering/QUALITY_GATES.md`
7. `docs/engineering/TRACEABILITY.md`
8. `docs/engineering/harness-distribution/intent/INT-DST-001.md`
9. `docs/engineering/harness-distribution/capabilities/CAP-DST-001.md`
10. `docs/engineering/harness-distribution/requirements/REQ-DST-060.md`
11. `docs/engineering/harness-distribution/specifications/SPEC-DST-017.md`
12. `docs/engineering/harness-distribution/verification/VER-DST-017.md`
13. `docs/engineering/harness-distribution/work-orders/WO-DOC-013.md`

The approved scope is limited to the four priority documentation groups, the focused public-onboarding regression, this governing packet, and retained evidence. No runtime, validator, managed template, workflow, lock, package, historical release/verification record, publication, deployment, or governor-selection change is authorized or claimed.

After the implementation handoff, the accountable owner instructed `I authorize a clean candidate commit for WO-DOC-013 and preparation of a ready commit-bound verification record`. The owner later instructed `you can commit the verification record, and create a PR`, authorizing retention of the ready record and creation of pull request #79. Neither instruction authorized a `verified` transition, merge, release preparation, tagging, publication, deployment, or governor promotion.

## Concurrent-main recovery

The original candidate commit `857be9d5b3018feb353bacdc9f800488d64bf98c` and ready-record commit `a87a43635d519f9ea5483d7aabfd25fa1f694f9a` were pushed to PR #79. All three hosted self-hosting checks passed, but current `main` had advanced through PR #78 to `69b7a1db7e04d05fd0ef471dd0e2997aa49a72e8` and independently assigned `SPEC-DST-017` and `VER-DST-017` to the Explorer dashboard packet. GitHub and `git merge-tree --write-tree` both reported add/add conflicts for those two paths.

The accountable owner then instructed `I approve renumbering to SPEC-DST-018 and VER-DST-018, rebuilding the candidate and VREC on current main, and force-with-lease updating PR #79.` The original remote tip was preserved locally as `docs/wo-doc-013-pre-rebuild`. The rebuilt branch starts exactly from current `origin/main`, preserves the unrelated Explorer `SPEC-DST-017` and `VER-DST-017` bytes, and changes only this packet's identifiers and relations to the approved `018` values. The seven explanatory/test surfaces were byte-identical between the original base and current `main`, so their bounded corrections required no semantic conflict resolution.

## Implemented corrections

| Surface | Result |
| --- | --- |
| Root `README.md` | Removed the false claim that every work order needs a non-empty `architecture` relation; retained the unresolved G0-G5 policy/Explorer mismatch. |
| `tests/test_public_onboarding.py` | Requires the current limitation and rejects the obsolete validator statement; its local-link inventory no longer requires the removed contextual link. |
| `docs/engineering/README.md` | Added bounded entries for `dashboard-publication/` and release packets 0.3.0, 0.4.0, and 0.4.1. |
| `self-hosting-boundary/README.md` | Describes `reconcile-governor` as implemented and authority-bounded; mirrors selected governor 0.3.0 and `RLS-SEH-005`; keeps candidate 0.4.1 separate. |
| `evidence-keying/README.md` | Records verified `VREC-EVK-002` coverage without a release or publication claim. |
| `work-order-assurance-classification/README.md` | Records aggregate verified coverage through `VREC-SEH-006` and release through `RLS-SEH-006` for version 0.4.0. |
| `release-orchestration/README.md` | Records verified `VREC-RLO-002` and `VREC-RLO-003` coverage without release, publication, or branch authority. |

## Authoritative fact comparison

An 18-check static comparison passed. The validator's work-order relation table requires `implements`, `specifications`, and `verification`, while canonical work-order guidance permits omission of `architecture` when no active architecture addresses an implemented requirement and rejects an empty relation when present. The root README contains the remaining G0-G5 mismatch and no obsolete architecture claim.

All four indexed directories exist. `.self-hosting/governor.toml` selects version `0.3.0` and `RLS-SEH-005`. `VREC-EVK-002`, `VREC-SEH-006`, `VREC-RLO-002`, and `VREC-RLO-003` each have `status = "verified"`. `RLS-SEH-006` has `status = "released"` and includes `WO-WAC-001` in `releases_work`. The explanatory summaries name those exact facts and preserve the separate publication, deployment, branch, and governor-promotion boundaries.

## Original implementation verification results

| Check | Result |
| --- | --- |
| Start preflight | PASS: `ready: true`, no diagnostics, complete 13-file governing manifest read. |
| Focused public-onboarding tests | PASS: 15 tests. The first run found one stale link-inventory expectation for the removed conceptual-model link; the assertion was narrowed to the README's current promised links and the suite then passed. |
| Progressive-documentation tests | PASS: 17 tests. |
| Complete unit suite | PASS in the original final `implemented` state: 269 tests in 76.153 seconds, 4 expected conditional skips. |
| Formal artifact validation | PASS: 507 artifacts, 0 errors, 44 unchanged maintenance warnings (`15` W013, `14` W014, `15` W015); all structure, governance, and policy planes had zero errors and warnings. |
| Release-distribution validation | PASS: 0 distribution-bearing records in the original worktree. |
| CLI help | PASS: all 16 commands were present, including the implemented `reconcile-governor`. |
| Installed-harness doctor | PASS: required, distributed, and managed-integrity checks passed; selected governor 0.3.0 reported; 15 pre-existing W013 placement warnings remained advisory. |
| Static source comparison | PASS: 18 checks across validator guidance, directory inventory, governor descriptor, and exact VREC/RLS metadata. |
| Local Markdown links | PASS: 669 Markdown files, 60 local links, 0 broken links. |
| Final diff and whitespace review | PASS: only the approved documentation, focused test, governing packet, and retained evidence changed; `git diff --check` reported no whitespace errors. |
| Review preflight | PASS in the original final `implemented` state with no diagnostics. |

## Current-main rebuild verification results

| Check | Result |
| --- | --- |
| Base and collision boundary | PASS: rebuilt from `origin/main` commit `69b7a1db7e04d05fd0ef471dd0e2997aa49a72e8`; the concurrent Explorer `SPEC-DST-017` and `VER-DST-017` remain byte-for-byte unchanged. |
| Review preflight | PASS: `ready: true`, no diagnostics, and the complete 13-file manifest names `SPEC-DST-018` and `VER-DST-018`. |
| Focused public/progressive documentation tests | PASS: 32 tests. |
| Complete unit suite | PASS: 269 tests in 84.946 seconds, 4 expected conditional skips. |
| Formal artifact validation | PASS: 511 artifacts, 0 errors, 44 unchanged maintenance warnings (`15` W013, `14` W014, `15` W015); structure, governance, and policy planes remain clean. |
| Release-distribution validation | PASS: 0 distribution-bearing records. |
| Installed-harness doctor | PASS: required, distribution, managed-integrity, and selected-governor checks passed with the same 15 W013 placement advisories. |
| Static source comparison | PASS: all 18 validator-guidance, directory, governor, VREC, and RLS checks. |
| Local Markdown links | PASS: 674 Markdown files, 60 local links, 0 broken links. |
| Identifier and diff hygiene | PASS: unique `SPEC-DST-018`/`VER-DST-018` relations, unchanged concurrent `017` artifacts, authorized path boundary only, and no whitespace errors. |

## Deviation and recovery

The initial focused public-onboarding run failed because `test_internal_documentation_links_are_repository_relative` still required `docs/notes/harness-uml-model.md`, whose only root README link was intentionally removed with the obsolete limitation. Removing that one stale inventory item was within the approved focused-test scope. The repeated public-onboarding suite passed all 15 tests; no documentation link was broken.

Git required a process-local `safe.directory` setting because the sandbox identity differs from the checkout owner. The complete suite used only `GIT_CONFIG_COUNT`, `GIT_CONFIG_KEY_0`, and `GIT_CONFIG_VALUE_0` in its process environment; no user or repository Git configuration was changed.

The concurrent reuse of `SPEC-DST-017` and `VER-DST-017` occurred only after the original branch base was cloned and qualified. The recovery does not alter the other packet or reinterpret the original approval; it uses the owner's explicit renumbering authority and requires fresh qualification and a fresh candidate-bound ready record.

## Residual uncertainty and authority boundary

Automated checks establish exact strings, metadata status, link resolution, and repository invariants but cannot prove future reader comprehension or prevent later lifecycle and governor transitions from making present-tense prose stale. Broader generated consistency automation remains outside `WO-DOC-013`.

The recovery authority permits rebuilding and force-with-lease updating PR #79, but it does not authorize transitioning the rebuilt `VREC-DOC-006` to `verified`, merging the pull request, preparing a release, tagging, publishing to GitHub or PyPI, deploying, or reconciling/promoting the governor. Those remain separate accountable decisions.
