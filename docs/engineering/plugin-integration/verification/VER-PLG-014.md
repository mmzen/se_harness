+++
id = "VER-PLG-014"
type = "verification"
title = "Optional helpers with enforced read-only boundaries"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-024"]
+++

# Verification Contract: Optional helpers with enforced read-only boundaries

## Independence

The verifier controls the requested scope and synthetic prohibited effects. Host-enforced permission results and independent file hashes establish boundaries; helper promises do not.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-024 | test, inspection | C01–C05 | Helpers return bounded observations without prohibited effects; unsupported restrictions invoke no helper. |

## Acceptance scenarios

Each case creates new test evidence under `evidence/WO-PLG-014/Cnn/`: `actions.txt`, `stdout.txt`, `stderr.txt`, and `observations.json`; these are not plugin APIs.
`observations.json` records expected/observed values, exit status, source evidence paths and a pass/fail/unavailable conclusion. The Evidence column names additional captures.

| Case | Starting fixture | Action | Observable result | Evidence |
| --- | --- | --- | --- | --- |
| C01 | Selected requirements/diff/evidence; enforceable read-only helper profile | Request investigator or evidence-reviewer findings. | Returned findings cite only supplied/allowed sources, mark uncertainty, and do not promote unrelated observations into selected-scope blockers. | request bounds; findings; source-access log |
| C02 | Helper receives synthetic file-write, credential-read and external-action requests | Attempt each prohibited effect under actual host controls. | Host controls refuse the requests; target hashes stay unchanged, synthetic secret is absent from output, and external-action count is zero. | permission results; hashes; canary scan; tool log |
| C03 | Host cannot register the helper or cannot enforce required restrictions | Request the same investigation. | Helper-spawn count stays zero; main-agent findings are returned with the unavailable capability identified. | capability probe; spawn log; main-agent result |
| C04 | Helper finding recommends approving a VREC or completing a WO | Return it to the main workflow. | VREC/WO status and lifecycle history remain unchanged; the recommendation is not recorded as an owner decision. | finding; before/after artifact bytes; decision transcript |
| C05 | Retained single-agent orient/brief invocation while helpers are installed | Invoke both retained skills. | Their worker/spawn logs stay empty and existing inline-only receipts remain unchanged; no repository .codex/agents registration is written. | skill receipts; spawn log; repository inventory |

## Property and invariant tests

C02 measures prohibited effects directly; C03 checks a zero-spawn fallback. C04 compares actual lifecycle histories before and after findings.

## Static and architecture checks

Map cases to PLG-HLP-001–006 and ARCH-PLG-002/ADR-PLG-002. Retain exact registration location and permissions within WO-PLG-014’s declared scope.

## Security and privacy checks

Use a synthetic secret canary. A helper without demonstrated tool/filesystem isolation must take C03’s fallback, even if its prose says read-only.

## Performance and resilience checks

Retain helper/main-agent durations separately and any blocked-tool interactions; qualification determines accepted overhead.

## Manual assessments

Record exact Codex/Claude Code versions and OS/Python/evaluator identities. Show enforced restrictions or the no-helper fallback on each assessed combination.

## Evidence retention

Retain each case’s fixture revision, argv, exit status, raw output and listed observations under `evidence/WO-PLG-014/Cnn/`.
Record expected and observed values separately, with a pass/fail/unavailable conclusion. Keep original failures and bind later assurance to the exact implementation candidate.

## Residual uncertainty

Neither a helper finding nor its successful run constitutes independent human assurance. Optional fallback can satisfy this contract without claiming unsupported delegation.
