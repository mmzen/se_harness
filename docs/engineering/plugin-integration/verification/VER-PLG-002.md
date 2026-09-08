+++
id = "VER-PLG-002"
type = "verification"
title = "Independent provided-Python environment evidence"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-003","REQ-PLG-004","REQ-PLG-005"]
+++

# Verification Contract: Independent provided-Python environment evidence

## Independence

The assurance owner fixes expected version, archive digest and payload digest from the independently verified release wheel before running setup. Candidate output never supplies expected identity. Use SPEC-PLG-002 and its referenced released-evaluator contracts as the oracle.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-003 | test, demonstration | ENV01, ENV02, ENV12 | Supported Python proceeds; missing prerequisites stop before Python-dependent setup or downloads. |
| REQ-PLG-004 | test, inspection | ENV01, ENV03, ENV04, ENV09, ENV12 | Offline external installation; no manual activation, global changes or repository writes. |
| REQ-PLG-005 | test, inspection | ENV04–ENV11 | Only the independently expected release, payload, archive observation and safe environment become ready. |

## Acceptance scenarios

Each case uses disposable plugin data and repository snapshots. ENV01 supplies the valid baseline; other cases change only their stated input. Evidence paths below are relative to the retention directory.

| Case | Fixture | Action | Observable pass condition | Evidence |
| --- | --- | --- | --- | --- |
| ENV01 | Supplied Python, trusted wheel, paths containing spaces; network disabled | Execute documented setup without shell activation | External environment ready; version, payload and observed archive equal fixed expectations; no network, project or system PATH changes | `env01.json`, `env01-diff.txt` |
| ENV02 | Separately missing Python, Python below 3.11, missing venv, missing ensurepip | Start setup through host shell | Each case reports its prerequisite; no environment creation, Python download or repository write | `env02.json` |
| ENV03 | Valid baseline; installation interrupted before completion | Request readiness | Incomplete environment unavailable; partial effects reported | `env03.json` |
| ENV04 | Completed matching environment | Repeat setup | Same verified environment reused; no duplicate install; identity rechecked | `env04.json` |
| ENV05 | Installed release version differs from trusted wheel | Request readiness | Version mismatch blocks readiness | `env05.json` |
| ENV06 | Correct version; modify installed payload bytes | Request readiness | Expected payload remains fixed; mismatch blocks readiness | `env06.json` |
| ENV07 | Matching payload; installed archive metadata names another digest | Request readiness | Observed archive mismatch blocks readiness | `env07.json` |
| ENV08 | Matching version/payload; remove installed archive metadata | Request readiness with expected wheel flag supplied | Plugin readiness refused despite generic identity accepting absent archive metadata | `env08.json` |
| ENV09 | Change bundled wheel bytes after trusted digest selection | Execute setup | Digest mismatch prevents installation and readiness | `env09.json` |
| ENV10 | Repository shadow module, inherited PYTHONPATH and unrelated global harnessctl | Run setup and identity | Absolute isolated interpreter and environment entry point used; PYTHONPATH cleared; controlled PATH; no repository import | `env10.json` |
| ENV11 | Separately unsafe import origin, wrong expected root, or missing/wrong entry point | Request readiness | Each unsafe identity is rejected; no substitute global executable | `env11.json` |
| ENV12 | Windows/Linux host-command fixtures; Python initially undiscovered | Inspect setup command sequence | Host/shell discovery precedes Python components; no new bootstrap executable, Python installer or system PATH mutation | `env12.json` |

## Property and invariant tests

ENV03–ENV11 retain readiness and selection observations before and after failure. ENV04 proves reuse rather than silently rebuilding a matching environment.

## Static and architecture checks

ENV12 compares instructions with existing released CLI arguments. ENV08 checks observed `evaluator_archive_sha256`, never the echoed expected `evaluator_wheel_sha256`.

## Security and privacy checks

ENV10–ENV11 reuse applicable negative inputs from SPEC-REB-011 rules 1–11 and SPEC-REB-015. Retain selected invocation fields, not credentials.

## Performance and resilience checks

Record elapsed setup and reuse times in ENV01/ENV04 evidence. ENV03 records interruption handling; these measurements grant no permission to skip required checks.

## Manual assessments

Run environment cases with released evaluator 0.16.0 and provided Python 3.11+, including 3.11, on Windows and Linux; record available macOS results. Unavailable combinations remain unqualified. Protocol fixtures alone establish no live host support.

## Evidence retention

Retain the named files, fixed identity inputs, command transcripts, identity results and snapshot comparisons under `evidence/WO-PLG-002/`. Every file records its case and exact platform/interpreter/evaluator identities.

## Residual uncertainty

These are future acceptance cases, not executed results. They establish plugin-managed readiness, not repository adoption or native host activation.
