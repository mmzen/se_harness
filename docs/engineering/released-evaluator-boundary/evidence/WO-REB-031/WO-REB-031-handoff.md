```toml
artifact = "WO-REB-031"
checkpoint = "handoff"
formal_snapshot_sha256 = "3524c950d230a9c813e9c7d4fc279aa127437c07a8c40a8b1711b5e18c173d25"
rebound_at = "2026-08-30T19:09:21Z"
```

# WO-REB-031 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The candidate-evidence lane has one acceptance path. The candidate-package
job invokes the released verifier's typed `qualify candidate-package`
unconditionally and asserts the canonical result shape
(`se-harness-release-qualification-v1`, operation `candidate-package`,
`independence == "released-verifier"`, passed); the `qualify --help`
capability probe, the `accept-candidate` fallback with its inline
functional-acceptance assertions, the `RELEASED_ACCEPTANCE_CONTRACT_SHA256`
output and env plumbing, and the `candidate-package-legacy-bootstrap-*`
retention are gone. The lane retains the canonical result as
`candidate-package-qualification-<predecessor_version>`.
`repository_tools/evaluator_facts.py` declares no
`LEGACY_ACCEPTANCE_CONTRACT_SHA256` table and derives no
`acceptance_contract_sha256` fact (`REQ-REB-031`; `REB-BFH-001` to
`REB-BFH-006`).

## Evaluators

- Governing: released `se-harness 0.11.0` outside the checkout, `-I`, on
  this Windows checkout for every reading, the packet and the handoff check
  included.
- Candidate: this checkout, branch `wo/reb-031-bootstrap-history` off
  `main` at `7cac025b7b38b9a62973ee72cbf8292b4e96a846`.

## Change

- `.github/workflows/candidate-evidence.yml`: the acceptance step is
  "Qualify the candidate package with the released verifier", typed-only;
  the retention step is "Retain the canonical candidate-package
  qualification result"; the `predecessor_acceptance_contract_sha256`
  output and the `RELEASED_ACCEPTANCE_CONTRACT_SHA256` env are removed;
  the verifier-binding step is renamed "as the released verifier".
- `repository_tools/evaluator_facts.py`: the legacy table, the dataclass
  field and the output line are removed; the module docstring no longer
  names the contract digest.
- `tests/test_release_qualification.py`: the bootstrap conformance test is
  `test_candidate_workflow_acceptance_is_typed_only` with a forbidden-string
  sweep and mutation subtests.
- `tests/test_standard_repository_lifecycle.py`: `accept-candidate`,
  `se-harness-functional-acceptance-v1` and `qualify --help` are asserted
  absent; the canonical retention name and no
  `RELEASED_ACCEPTANCE_CONTRACT_SHA256` are asserted.
- `tests/test_ci_pipeline.py`: `test_facts_come_from_the_lock` asserts no
  acceptance-contract attribute or output line; the job-output test asserts
  `acceptance_contract_sha256` absent from the workflow.
- `tests/test_predecessor_bootstrap_retirement.py`: unchanged; its ledger
  only requires `evaluator_facts.py` to exist and import no deleted module.
- Notes: `developing-se-harness.md` drops the legacy-fact sentence;
  `release-qualification-roles.md` restates the bootstrap section as
  retired history; `ci-pipeline.md` names the removal.
- Amendment records on `SPEC-REB-010` (the exception is executed as
  expired) and `SPEC-REB-012` (rule 6 restated typed-only); the domain
  README carries the packet paragraph.

## Verification readings (VER-REB-015)

- Affected suites: `test_release_qualification`,
  `test_standard_repository_lifecycle`, `test_ci_pipeline`,
  `test_predecessor_bootstrap_retirement` — 82 tests OK.
- Full Windows suite: 1153 tests, 1 error — the known
  `test_artifact_authoring` temp-directory baseline — 26 Windows-only
  skips; at baseline.
- Sweep: `accept-candidate`, `qualify --help`,
  `RELEASED_ACCEPTANCE_CONTRACT_SHA256`, `acceptance_contract`,
  `legacy-bootstrap` — zero hits in the workflow.
- Facts derivation on this repository: schema
  `se-harness-evaluator-facts-v1` with exactly version 0.11.0, wheel,
  wheel digest, payload digest and candidate version 0.12.0; no
  acceptance-contract key.
- Released 0.11.0 evaluator: `doctor` 0 FAIL; `validate` 1177 artifacts,
  0 errors, 485 warnings (the pre-existing advisory flood);
  `validate_release_distributions` PASS (8 records).
- The pull request's own lanes are the lane reading; recorded on the pull
  request when green.

## Material non-effects

No `se_harness/` product module changed. No hash-locked root file changed.
No retained evidence file changed. The `accept-candidate` tombstone and its
tests are untouched.

## Hosted lanes

All thirteen lanes of pull request #295 pass at its head `e7ed556`. The
owner merged the pull request on 2026-08-30 as `8b389d5`; the push-event
check runs on `main` for that commit read all thirteen completed with
success, including Candidate package evidence executing the typed-only
acceptance step, the managed Engineering Harness `validate`, the Governor
transition assessment and both release-qualification rehearsal legs.
