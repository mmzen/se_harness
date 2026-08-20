# WO-WEX-001 implementation evidence

Date: 2026-08-20

## Scope and authority

This evidence records the implemented candidate-source slice for `WO-WEX-001`, covering `REQ-WEX-001` through `REQ-WEX-005`. The rejected `REQ-WEX-006` is not implemented: there is no trusted-base option, diff comparison, direct-edit enforcement, or lifecycle-history CI gate.

The work remains `in_progress` while exact-commit candidate-package acceptance, platform-specific link/filesystem cases, and accountable manual assessments remain outstanding. The automated supported-agent corpus and declared scale matrix are complete. No commit, push, pull request, VREC decision, release, tag, publication, deployment, managed-root upgrade, or promotable distribution build was performed.

## Implemented candidate surfaces

- `se_harness/workflow.py`: selected-scope projection, lifecycle registry, semantic workflow result, human/JSON rendering, final-graph planning, stale-input checks, same-filesystem staging, atomic replacement, and rollback.
- `se_harness/cli.py`: public `focus` and plan-by-default `transition` commands plus canonical preparation handoffs.
- `se_harness/provenance.py`: exact implemented-WO capture, exact verification-contract union, verified-only release preparation, and preparation-only metadata.
- Candidate validator, VREC/RLS templates, Explorer projection, managed router/workflow templates, public reference material, and focused regression tests.
- Root managed files remain the exact released installation and were not reconciled from candidate source.

## Behavioral evidence

Focused tests cover:

- deterministic WO scope and unrelated-background classification;
- byte-identical repeated JSON plans with no retained plan timestamp;
- graph-valid multi-definition packet activation;
- plan-only zero mutation and explicit apply;
- VREC verification without WO or RLS mutation;
- RLS release without VREC or WO mutation;
- rejection-reason enforcement and hostile actor control characters;
- preparation/decision metadata separation;
- lifecycle-event and target-state validation;
- stale-plan refusal;
- full formal/evidence/config read-set staleness detection and a selected-file recheck at each replacement boundary;
- concurrent change during a packet apply with restoration of the earlier replacement and preservation of the concurrent owner bytes;
- injected second-replacement failure with restoration of every pre-operation byte;
- interrupted staging, full-disk simulation, denied/locked replacement, explicit unprovable-rollback escalation, and temporary-file cleanup;
- path-shaped/reserved artifact input rejection, duplicate and case-insensitive identity collision blocking, TOML/JSON/shell-like decision data encoding, and a platform-conditional symlink escape case;
- preservation of UTF-8 BOM, CRLF style, and artifact body bytes.

The verifier-owned corpus at `tests/fixtures/workflow_execution/scenarios.json` drives the same WO focus projection for ChatGPT, Claude, and Codex adapter markers. All three runs produce byte-identical canonical JSON. Human output is separately checked to expose the same completed, current-state, primary-next-step, authority, and command semantics. Exact VREC and RLS scope fixtures additionally prove that related records are projected but never synchronized.

Preparation regression tests additionally prove that capture rejects non-implemented work, release preparation rejects ready and superseded VRECs, exact aggregate coverage is retained, and new ready records omit decision fields.

## Commands and results

### Candidate-source compile and focused workflow tests

```text
python -m py_compile se_harness\workflow.py templates\repository\standard\scripts\validate_engineering_artifacts.py templates\repository\standard\scripts\generate_harness_dashboard.py
python -m unittest tests.test_workflow_execution -v
```

Result: PASS. Final focused run: `Ran 29 tests in 25.466s`; `OK (skipped=1)`. The scenarios include exact WO/VREC/RLS scope, agent-host and human/JSON conformance, repository-blocker classification, lifecycle-plane independence, hostile content and path inputs, full read-set concurrency, transaction-boundary failure injection, and deterministic scale checks. The file-symlink scenario is skipped on this Windows host because the process lacks the symlink privilege; lexical and case/identity path boundaries still execute.

### Complete candidate-source suite

```text
python -m unittest discover -s tests -p "test_*.py"
```

Result: PASS. Final run: `Ran 294 tests in 107.190s`; `OK (skipped=5)`. Four skips are existing platform/fixture-conditional cases and one is the WEX file-symlink case described above. Sandbox Git ownership/config warnings were non-failing; the affected manifest test supplies a process-local `safe.directory` setting without changing user or repository Git configuration.

### Deterministic scale matrix

The focused module incrementally constructs exact 100-, 500-, and 1,000-formal-artifact repositories. Each value below is the median of three runs on Python `3.14.6`; validation, focus, and plan remain read-only.

| Formal artifacts | Validation | Focus | Transition plan |
| ---: | ---: | ---: | ---: |
| 100 | 0.053578 s | 0.056727 s | 0.120228 s |
| 500 | 0.252163 s | 0.244681 s | 0.557355 s |
| 1,000 | 0.496483 s | 0.477451 s | 1.080235 s |

At ten times the artifact count, the respective runtime factors are 9.27, 8.42, and 8.99. No unexplained superlinear growth was observed at the declared scale.

### Canonical conformance identities

```text
candidate source version: 0.5.0
dirty working-tree baseline HEAD: 1f67f15034a3f40e2ac7395ee99d866aa9e86442
verifier-owned scenario SHA-256: 9f6250a685cdf1b599abe4dad17b5564bd46c88b77338202944536f4cdd9d609
WO-WEX-001 focus JSON: 1,641 bytes
WO-WEX-001 focus JSON SHA-256: 3881cba81600e7649ecbd0878bdf83994db2177ad461b16600240aa72944c10c
```

The baseline commit is not represented as the candidate identity because the implementation is intentionally uncommitted. Candidate-source, future candidate-package, and released-evaluator identities remain separate.

### Candidate artifact graph

```text
python -m se_harness validate .
```

Result: PASS. `535` artifacts, `0` errors, `44` maintenance warnings. The warnings are the pre-existing `W013`, `W014`, and `W015` compatibility/migration findings and are unrelated to the selected WEX scope.

### Selected scope

```text
python -m se_harness focus . --artifact WO-WEX-001 --json
```

Result: PASS. The governing set is exactly `INT-WEX-001`, `CAP-WEX-001`, `REQ-WEX-001..005`, `SPEC-WEX-001`, `ARCH-WEX-001`, `ADR-WEX-001`, and `VER-WEX-001`; the 44 unrelated warnings are one `WEX190` background summary and produce no current-scope action.

### Released evaluator integrity

```text
..\work\se_harness-evaluator-venv\Scripts\python.exe -I -m se_harness --version
..\work\se_harness-evaluator-venv\Scripts\python.exe -I -m se_harness doctor .
```

Result: PASS. Released evaluator version `0.5.0a1` on Python `3.14.6`; every required, distribution, managed-lock, and seed check passed. Fifteen historical `W013` location advisories remained non-blocking. This proves candidate template changes did not overwrite the root managed installation.

### Rejected-requirement negative proof and diff hygiene

```text
rg -n --glob '!docs/engineering/workflow-execution/**' --glob '!docs/engineering/**/evidence/**' "trusted.?base|--base|diff enforcement|lifecycle diff" se_harness templates tests README.md docs\notes
git -c safe.directory=C:/Users/mathi/Documents/Codex/2026-08-20/clone-https-github-com-mmzen-se/se_harness diff --check
```

Result: PASS. The rejected behavior search returned no match, and diff hygiene reported no whitespace error.

### Released-evaluator review preflight

```text
..\work\se_harness-evaluator-venv\Scripts\python.exe -I -m se_harness preflight . --work-order WO-WEX-001 --phase review --json
```

Result: PASS. `ready = true`, no diagnostics, exact released evaluator boundary retained, and the manifest contains only the managed policy/router plus the approved WEX governing chain. The work order remains honestly `in_progress`.

## Self-hosting and compatibility observations

- Candidate managed templates intentionally differ from the root released copies. Tests now assess candidate templates without treating a source checkout as an installed upgrade.
- Unchanged legacy VREC/RLS records without preparation fields or lifecycle events remain readable. A later explicit transition adds only the new decision data and event while retaining captured candidate facts.
- `prepare-release --authorized-by` is retained for CLI compatibility but is stored as the preparation actor (`prepared_by`) while the RLS is ready. `authorized_by` is added only by the release decision transition.
- VREC supersession uses the required `--reason ID=TEXT` value as the exact successor VREC ID because the approved public command shape contains no separate successor option.
- Repository-wide `inspect` behavior and schema are unchanged; selected-scope behavior belongs only to `focus`.

## Remaining verification before implementation completion

- Run verifier-owned candidate-package black-box acceptance after a separately authorized candidate commit and non-promotable test package are available through the released-evaluator boundary.
- Exercise real symlink/junction escape and native read-only/locked-file behavior on supported hosts that expose those capabilities. The current host denied file-symlink creation; disk-full, denial, interruption, concurrent edit, case collision, rollback success, rollback failure, and cleanup are covered by deterministic injection.
- Complete accountable product, technical, assurance, repository-owner, and supported-agent usability review of the retained corpus and representative records.
- Run final candidate/package parity and review preflight after any corrections from those assessments.

These remaining items keep `WO-WEX-001` honestly `in_progress`; they do not weaken the passing implemented kernel evidence above.
