```toml
artifact = "WO-HUP-019"
checkpoint = "handoff"
formal_snapshot_sha256 = "db010827db3f5ca02fdcf85ead63a080642c10812a9c072a20509d9210cf7a72"
rebound_at = "2026-09-15T11:31:13Z"
```

# WO-HUP-019 handoff evidence

## Outcome

The root now uses the public 0.18.0 evaluator installed from its verified wheel
outside the checkout. The reviewed transaction applied 25 updates, adopted 11
unchanged editable files and left five files unchanged. All 19 editable
replacements were passed explicitly. Replay reports 41 unchanged paths.
Candidate version declarations are 0.19.0. Current owner instructions describe
the adopted evaluator, editable supplied files and combined-work-order PRs.
Candidate templates, product behavior and historical VREC/RLS records are unchanged.

## Package and transaction identity

- Release source: RLS-SEH-027, public release v0.18.0 and its package-index wheel.
- Wheel: `se_harness-0.18.0-py3-none-any.whl`.
- Wheel SHA-256: `a683dbdf485d42aa20ea8502122c171a4c61c7d60f85db5b5f264bd336371c54`.
- Installed payload SHA-256: `cf28e03f21a0e474af8c415499c69193ab2a20e08a95c0ad3514758a84cff54d`.
- Prior committed lock SHA-256: `ac614b2bb0c9910df078a7025bef72b6da3074aa84e6728c0ecc0539bd9efc15`.
- Target lock SHA-256: `5a0e14ccfe2b143850ba7658943710b0e5e8583b421fda4518d88a2989478615`.
- Transaction: `../WO-HUP-019-evaluator-upgrade.json`; canonical installer output retained unchanged.
- Applying environment: `work/evaluator-018`, outside the repository, invoked with `python -I -m se_harness`.

The installer preserved owner text around the managed fragments. The later
owner-region edits are the separately approved instruction updates. The 16
adopted or unchanged supplied files retain their original bytes. The prior
lock was materialized as its committed LF bytes before the transaction.

## VER-HUP-019 results

| Check | Result |
| --- | --- |
| Released 0.17.0 baseline doctor | 99 passes, zero failures; 48 existing W013 warnings |
| Released 0.18.0 doctor | 70 passes, zero failures; exactly the same 48 warnings |
| Graph validation | 1,642 artifacts, zero errors, 48 warnings, zero advisories |
| Released-root qualification | RR001 through RR004 pass; runtime identity, 69 managed checks, graph, unchanged target |
| Review preflight | Ready, zero diagnostics; required reading manifest read |
| Repeated upgrade | 41 unchanged paths |
| Candidate/evaluator derivation | Root 0.18.0, candidate 0.19.0, release-bound archive and payload |
| Equal candidate/root refusal | PRE008 reproduced in an isolated minimal fixture; actual checkout unchanged |
| Candidate CLI help | Exit 0 |
| Release-distribution validation | PASS; 15 distribution-bearing records |
| Instruction tests | 29 tests pass |
| Scope and preservation | Every changed path is approved; no candidate-template or historical-record changes |

The application script inspected the public checksum and exact action set
before calling the installer and would stop on either mismatch. These guards
and the exact retained release identities are inspection evidence for the
wrong-package and unexpected-plan acceptance scenarios.

The candidate-source doctor reports three expected identity differences:
`distribution:ENGINEERING_HARNESS.md`, `evaluator-payload` and
`selected-version`. Source 0.19.0 cannot identify itself as the installed
0.18.0 evaluator. The external released evaluator passes; source output is
candidate-boundary evidence and was not used to govern this upgrade.

### Full source suite and unchanged control

All runs use `python -B scripts/run_tests.py`, the full ordinary source suite
with its default reduced scale, on Windows CPython 3.13.3. The control and
initial upgraded run used four workers; the corrected run used eight.
The control is an unchanged clone of the original 386b5b96 commit under 0.17.0.

| Run | Tests | Actual verdict |
| --- | --- | --- |
| control | 1068 | FAILED (failures=1, skipped=15) |
| initial_upgraded | 1068 | FAILED (failures=1, errors=1, skipped=15) |
| corrected | 1068 | OK (skipped=15) |

The corrected run has no new failures or errors. Exact IDs, command arguments
and raw-log hashes are retained in `source-suite-comparison.json`.

The first upgraded run exposed two obsolete root assumptions. The artifact
catalog test required the retired literal "Model transcription MUST NOT";
it now checks the adopted evaluator's handoff wording, retaining the older
expectation for older roots. The CI test indexed a hash on an editable seed;
it now checks the ownership mode appropriate to the adopted version and the
workflow's selected evaluator. Both fixes are limited to HUP-NEW-012.
All ten tests in the affected catalog and trigger-policy groups passed before
the complete corrected suite was run. Product code and candidate templates
were not changed to satisfy these assertions.

The control's one dashboard failure expected the GitHub source URL, but the
disposable clone's origin is a local filesystem path. That same test passed
when only the disposable clone's remote URL was temporarily set to the
original GitHub URL. Its original remote was then restored, and tracked files
remained unchanged. This explains the control-only failure without changing
product code or weakening an assertion.

### Review and authority

The owner approved the six artifacts and the execution scope with "i approve
evaluator upgrade". Released 0.17.0 applied approval and start. After adoption,
the executor annotated that same explicit approval with its exact reviewed
`scope_paths`, as explained in WO-HUP-019. Its original reason, actor, time,
scope and lifecycle meaning remain unchanged; no additional authority is inferred.

The implementation uses the existing installer and explicit replacement
arguments. It adds no product abstraction, runtime dependency or release.
The review confirmed every change serves adoption, current instructions,
the successor version or the approved evidence. The two test corrections
address only the demonstrated released-root assumptions.

The executor codex recorded WO-HUP-019 as implemented after the released
evaluator's selected handoff and final transition preview passed. A ready
verification record is preparation only. Its
independent assurance decision remains separate. Linux hosted CI, remote Git
integration and plugin installation have not been performed in this scope.

## Retained evidence

`qualification-summary.json` retains the measured check summaries, exact
identities, preservation facts and raw-log hashes. Raw local logs live outside
the checkout in `work/evaluator-upgrade-018/` in this Codex workspace.
