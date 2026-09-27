```toml
artifact = "WO-IAR-017"
checkpoint = "handoff"
formal_snapshot_sha256 = "002f7bd8d23588bef8ce667761f9d2a8937ba54ed2cdbaa4699a1d3003bb8907"
rebound_at = "2026-09-27T08:55:52Z"
```

# WO-IAR-017 regression correction review

The approved test-only scope is implemented. Its lifecycle completion and
verification state are recorded separately by the released evaluator.

## Scope and review

The regression baseline is `7b57dae566bd5cce6f8ebeb76c492a1dc185cbbd`. That local commit
contains the earlier WO-IAR-013–016 implementation, whose host/platform
qualification remains incomplete. This correction changes 14 test modules
and one successor identity fixture. It changes no production behavior.

- Fresh-install and adoption tests now require AGENTS.md and CLAUDE.md to
  remain owner files. They check exact retained owner bytes and the absence
  of harness lock entries. Managed-fragment drift remains tested on .gitignore.
- Installer checks retain refusal before writes, selective seed replacement,
  transaction rollback, retry and customized-guide protection. A customized
  compatibility guide is refused until an explicit replacement is selected.
- Guidance tests follow the approved conditional routes and check typed links,
  architecture applicability, human authority and risk/decision boundaries.
  Exact lifecycle states, gate bindings and predicate assertions are unchanged.
- The retired relation wording is still checked against the preserved 0.18.0
  fixture; its explicit successor disposition is checked in the reference map.
  Retired AGENTS/CLAUDE template paths now have absence assertions.
- Provenance fixtures create their own owner instructions before capture, so
  changes to those inputs still refuse reuse. Historical skill vectors remain
  byte-identical. The new vector retains the phase-5 identity as its predecessor
  and uses canonical LF hashes for portability.

These changes serve SPEC-IAR-014's accepted ownership and discovery behavior.
No test was disabled and no lifecycle gate or authority assertion was weakened.
No new production abstraction was needed.

## Observed checks

- Initial affected-module run: 308 tests, two failures and five skips. The
  failures were test adaptations using HTML markers for .gitignore.
- The next correction run caught five stale-lock fixture errors introduced
  during editing. Those errors were corrected; their original logs remain.
- Final corrected-module run: 96 tests, zero failures/errors and three skips.
- Full suite at full scale: **Ran 1118 tests in 147.655s (175 classes, 6 workers)  OK (skipped=16)**.
- Release-distribution validation: passed, 15 distribution-bearing records.
- Candidate CLI help: passed.
- Selected released 0.18.0 doctor, graph validation and review preflight: passed.
- Historical fixture check: 7 existing agentic-execution fixture
  files unchanged. Exact changed test paths and byte hashes are in
  [test-change-inventory.json](test-change-inventory.json).

The full run covers the affected modules together with the rest of the suite.
Passing unit tests do not establish native host qualification or assurance
acceptance. Claude startup was observed under WO-IAR-015; native compaction,
Codex delivery and Linux migration remain unverified for the broader evolution.

## Evidence

The adjacent invocation JSON files contain actual arguments, interpreter,
working directory, timestamps and exit codes. Corresponding stdout/stderr files
retain successful and failed runs. The test inventory binds the reviewed bytes.
The handoff result and lifecycle readback, when present, provide the current
state; this prose does not apply any transition or assurance decision.
