+++
id = "VER-ECP-024"
type = "verification"
title = "Independent evidence for the wave 1 deletions"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-07"
updated = "2026-09-07"

[relations]
verifies = ["REQ-ECP-033"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T20:27:10Z"
decided_by = "assurance-owner"
reason = "Approved on 2026-09-07 by the accountable owner with the words 'i approve', given after the packet PR #385 and its summary were presented: scans before and after, the parser's own choices, the wheel file list, the contract loader, the suite at its baseline, and the amendment records. Approval of a definition authorizes no work."
+++

# Verification Contract: Independent evidence for the wave 1 deletions

## Independence

Deletions are proven by tools that do not read the deleted code: the
dead-code scan, `pyflakes`, the parser's own choices, the wheel's file
list, the contract loader, and the suite at its baseline. Each work order's
evidence packet records the scan before and after, so a deletion that
removed something live shows up as a test that stopped passing.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-033` dead symbols | `vulture --min-confidence 60` and `pyflakes` over `se_harness scripts repository_tools tests`, before and after | after: nothing but the chains `SPEC-ECP-022` keeps for #377 (`ECP-DEL-001`, `-007`) |
| `REQ-ECP-033` kept surfaces | test | `RuntimeIdentity` fields unchanged; `CONTRACT_SHA256` unchanged; `AcceptanceManifest` present (`ECP-DEL-003`, `-005`, `-019`) |
| `REQ-ECP-033` alias | test: the parser-shape set; `harnessctl adopt` through `main()` | no `adopt` choice; exit 2, empty stdout, usage error (`ECP-DEL-015`, `-016`) |
| `REQ-ECP-033` dormant commands | test: the parser-shape set; both names through `main()`; the wheel file list | neither choice; exit 2 each; no `renumber.py`, `recovery_rehearsal.py`, `journaled_apply.py` in the wheel (`ECP-DEL-020`, `-021`) |
| `REQ-ECP-033` guard inventory and code index | test: `mutation_guard` operations; `tests/test_diagnostic_code_index.py` | no `renumber-artifacts-apply`; the regenerated page equals the committed one with no `REN`, `RR`, `JNL` (`ECP-DEL-022`, `-023`) |
| `REQ-ECP-033` contract entries | test: `load_validated_contracts`; `tests/test_workflow_documentation_contract.py` | no `QG-G0-INTENT`, `QGP-G0-*`, `PROC-CANDIDATE-COMMIT`, `STEP-CANDIDATE-COMMIT-AUTHORIZE`; package equals the candidate template (`ECP-DEL-024`, `-025`, `-028`) |
| `REQ-ECP-033` fixtures and config | inspection | the eight fixture files absent; `MANIFEST.in` without `*.yaml`; no `[tool.unittest]` (`ECP-DEL-008`, `-009`) |
| `REQ-ECP-033` workflow outputs | inspection of the four workflows; `tests/test_ci_pipeline.py` consumed-outputs test | the nine outputs gone; `candidate-package` reads the job output (`ECP-DEL-012` to `-014`) |
| `SPEC-ECP-022` records | inspection | every amendment record of `ECP-DEL-018`, `-029`, `-030`, `-031` present, dated, naming the specification |
| `REQ-ECP-033` no regression | the full suite; `validate`; `doctor`; the hosted lanes | suite at its baseline names; graph 0 errors; managed set untouched for group A and B; every lane green (`ECP-DEL-033`) |

## Acceptance scenarios

1. `harnessctl --help` after all three work orders lists neither `adopt`,
   `renumber-artifacts` nor `rehearse-recovery`.
2. `python -m vulture se_harness scripts repository_tools --min-confidence
   60` reports only the declared-digest chain kept for #377.
3. The candidate wheel's file list has no `journaled_apply.py`,
   `renumber.py` or `recovery_rehearsal.py`.
4. `load_validated_contracts()` succeeds and names no `QG-G0-INTENT` or
   `PROC-CANDIDATE-COMMIT`.

## Property and invariant tests

For every retired name, `main([name, …])` exits 2 with empty standard output
and the usage error on standard error; no source line in `cli.py` mentions
the name.

## Static and architecture checks

The parser-shape test; the source-reading test of `ECP-TMB-003`; the
documentation-contract test over the template `WORKFLOW.md` and
`QUALITY_GATES.md`.

## Security and privacy checks

The mutation-guard tests pass with the smaller operation set.

## Performance and resilience checks

None beyond the suite.

## Manual assessments

A reviewer reads the amendment records and the two reference sections.

## Evidence retention

`docs/engineering/execution-control-plane/evidence/WO-ECP-028/`,
`WO-ECP-029/` and `WO-ECP-030/`.

## Residual uncertainty

Whether any consumer outside this repository scripted `renumber-artifacts`
or `rehearse-recovery`; none is known, both are refused with a usage error,
and the reference keeps their history.

## Amendment record

**The guard-inventory row is corrected, proposed 2026-09-07 under `WO-ECP-030`.** The pass condition reads "no `REN`, `JNL`" where it read "no `REN`, `RR`, `JNL`": `RR` is release qualification's live family (see the `SPEC-ECP-022` record of the same date).
