# WO-CIP-003 implementation evidence

artifact: WO-CIP-003
checkpoint: handoff
formal_snapshot_sha256: 7eee4b3b916e851142b95d309e2463e45be2be09cbf5da7940df0e29ffc22256

Retained by the implementation actor on 2026-08-26. This file is evidence. It
does not complete, verify, or release the work order.

## Evaluators

- Governing: released `se-harness 0.6.0` installed outside the checkout from
  the exact wheel `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
  (`C:\Users\mathi\se-harness-eval`, invoked with `-I`).
- Candidate: this checkout, `python -m se_harness` and
  `python -m repository_tools.predecessor_facts` from the repository root.

## What was built

- **`repository_tools/predecessor_facts.py` (REQ-CIP-006, CIP-PRE 1–2).**
  `derive` reads `tool_version` from `.engineering-harness.toml`, the
  `evaluator` block of `.engineering-harness.lock` (version, `archive_name`,
  `archive_sha256`, `payload_sha256`), the candidate version from
  `pyproject.toml`, and resolves
  `tests/fixtures/governance_migration/candidate-<predecessor>-to-<candidate>.json`,
  checking its canonical form, its fixture and decision digests, and the
  pair and archive it declares; it returns the fact set (`schema
  se-harness-predecessor-facts-v1`) and writes `key=value` lines for
  `$GITHUB_OUTPUT`. It fails closed with a `PRE0nn` code: disagreeing root
  declarations (`PRE007`), candidate equal to the root (`PRE008`), missing
  scenario naming the expected path (`PRE009`), scenario declaring another
  pair or another archive (`PRE010`–`PRE012`). The legacy `accept-candidate`
  contract digest of an exact public release is declared once in
  `LEGACY_ACCEPTANCE_CONTRACT_SHA256`. `write-scenario` is the canonical
  writer: it re-points a template scenario at the lock's evaluator and the
  candidate version, recomputes `fixture_sha256` and the decision digests,
  re-checks the canonical form, and writes `canonical_json` bytes. Writing the committed pair from the committed scenario reproduces
  `candidate-0.6.0-to-0.7.0.json` byte for byte (`cmp` identical; digest
  `0b21462c…`).
- **`candidate-evidence.yml` (CIP-PRE 1, 3).** One derivation step in
  `candidate-source`, before any network access, exporting eight job
  outputs; `candidate-package` takes `RELEASED_VERIFIER_*` and the artifact
  name from them and its inline assertion reads the version from an
  argument; both `governance-migration` legs take `PREDECESSOR_*`, the
  scenario path and its digest from them and refuse to run without them.
  Evaluator literals in the repository-owned workflows: 8 → 0.
- **Tests.** `tests/test_ci_pipeline.py::PredecessorDerivationTests` (seven
  tests: facts equal the lock and the table; no digest or evaluator-version
  literal in the two repository-owned workflows; one derivation and consumers
  on outputs; a version bump without a scenario fails with `PRE009` naming
  the path, from the API and from the CLI (exit 2); disagreeing root
  declarations fail with `PRE007`; the module is standard-library only and its
  writer equals the contract module's on every committed scenario; the writer reproduces the committed
  scenario and writes the next pair, which `derive` then resolves). Three
  tests that restated the literals now derive them through the module.
- **Documentation (CIP-DOC).** `developing-se-harness.md`: the derivation
  paragraph under "Evaluator and candidate evidence" and the version-bump
  step of "Release sequences" rewritten around the two commands;
  `ci-pipeline.md`: "After WO-CIP-003".

## Commands and results

| Command | Evaluator | Result |
| --- | --- | --- |
| `harnessctl preflight . --work-order WO-CIP-003 --phase review` | released 0.6.0 | `PASS` |
| `harnessctl validate .` | released 0.6.0 | PASS, 909 artifacts, 0 errors, 50 warnings |
| `harnessctl doctor .` | released 0.6.0 | 0 FAIL |
| `python scripts/validate_release_distributions.py --root .` | candidate | PASS (1 distribution-bearing record) |
| `python scripts/check_portable_release_surface.py --repository .` | candidate | PASS |
| `git diff --check` | git | clean |
| `python -m repository_tools.predecessor_facts derive --repository .` | candidate | version `0.6.0`, wheel `se_harness-0.6.0-py3-none-any.whl`, wheel digest `2a952eb6…`, payload `c2336785…`, contract `a443e93d…`, scenario `tests/fixtures/governance_migration/candidate-0.6.0-to-0.7.0.json`, digest `0b21462c…`; exit 0 |
| `python -m repository_tools.predecessor_facts write-scenario --template …/candidate-0.6.0-to-0.7.0.json --output <scratch>` then `cmp` | candidate | identical to the committed fixture (3,862 bytes) |
| PyYAML 6.0.3 parse of `candidate-evidence.yml` | workstation | `candidate-source.outputs` = candidate_version, predecessor_version, predecessor_wheel, predecessor_wheel_sha256, predecessor_payload_sha256, predecessor_acceptance_contract_sha256, migration_scenario, migration_scenario_sha256 |
| `harnessctl check . --artifact WO-CIP-003 --checkpoint handoff --changed-path … --changes-complete --json` (complete set below) | released 0.6.0 and candidate | before this file existed: blocked only by `QGP-G4I-EVIDENCE`; both report formal snapshot `7eee4b3b916e851142b95d309e2463e45be2be09cbf5da7940df0e29ffc22256` |
| `python -m unittest` over `test_ci_pipeline`, `test_governance_migration`, `test_release_qualification`, `test_standard_repository_lifecycle`, `test_integration_package` | candidate | OK |
| `python -m unittest tests.test_ci_pipeline tests.test_interpreter_safety tests.test_governance_migration` | candidate | OK, 10 skips (Windows-only guards), after the module was made standard-library only |
| `python -m unittest discover -s tests -p "test_*.py"` | candidate, Windows 11, CPython 3.14 | `Ran 1035 tests in 336.508s` — `OK (skipped=23)`; the 23 skips are the Windows-only guards. A first run failed one test: the repository_tools to se_harness import crossing is a pinned inventory; the module was made standard-library only (deviation 6) and the suite re-run |
| Hosted run | `.github/workflows/candidate-evidence.yml` | not observed locally; the pull request shows the derivation step's JSON in the `candidate-source` log and the consumers' env resolved from it |

## Deviations from the specification, recorded for the completion decision

1. **A fourth fact, declared in code.** `CIP-PRE` 1 names three facts. The
   legacy bootstrap path also needs the digest of the exact public 0.6.0
   `accept-candidate` contract, which the lock does not carry. It is declared
   once in `LEGACY_ACCEPTANCE_CONTRACT_SHA256`, keyed by version, and
   asserted by tests; the workflow reads it as an output and refuses the
   legacy path when it is empty. When a released verifier gains
   `qualify candidate-package` the table and the path go together.
2. **The writer is a `repository_tools` command, not `harnessctl`.**
   `CIP-PRE` 2 allowed either; the decision envelope names the choice. The
   scenario and its writer are repository-owned candidate concerns, and the
   released evaluator must not need them, so `harnessctl-reference.md` is
   unchanged and `developing-se-harness.md` names the command.
3. **`predecessor-evaluator-assessment.yml` is unchanged.** It is in scope;
   it carries no evaluator literal (its facts come from
   `scripts/validate_governor_transition.py plan`) and needs no derivation
   step. The grep gate covers it.
4. **The writer takes a template.** `CIP-PRE` 2 wrote
   `write-scenario --predecessor --successor` as if from nothing; a
   scenario also carries authored content (adapters, capabilities,
   decisions, description) that no declaration supplies, so the writer
   re-points an existing scenario and recomputes the digests. The
   idempotence proof (committed pair from committed scenario, byte-identical)
   is the test that the recomputation is exact.
5. **`tests/fixtures/governance_migration/` is in scope and unchanged.** The
   regenerated committed fixture is identical, so nothing was rewritten.
6. **The module is standard-library only; it does not import the package.**
   The first full suite failed `tests/test_interpreter_safety.py`: the
   `repository_tools` to `se_harness` import crossing is a pinned exhaustive
   inventory, and widening it is an interpreter-safety decision this work
   order does not hold. The canonical writer (`canonical_json`) and
   `sha256_bytes` are restated in the module in the contract module's form,
   the scenario loader checks canonical form and the two digests the writer
   maintains, and a test proves the restated writer and the contract module
   agree byte for byte on every committed scenario; full contract validation
   of a scenario remains with `rehearse-migration`. This bears on
   `WO-CIP-002`: `ADR-CIP-001`'s "scripts import the package" applies to
   `.github/scripts/`, not to `repository_tools`, whose crossing inventory
   stays as it is.

## Complete changed-path set

```
.github/workflows/candidate-evidence.yml
docs/engineering/ci-pipeline/evidence/WO-CIP-003/WO-CIP-003-verification.md
docs/notes/ci-pipeline.md
docs/notes/developing-se-harness.md
repository_tools/predecessor_facts.py
tests/test_ci_pipeline.py
tests/test_governance_migration.py
tests/test_release_qualification.py
tests/test_standard_repository_lifecycle.py
```

## Not done

- Hosted observation of the derivation step, which needs the pull request;
  the completion transition; `VREC-CIP-003`.
- The managed `engineering-harness.yml` keeps its `{{HARNESS_VERSION}}`
  literal by design (`REQ-CIP-006` constraints).
