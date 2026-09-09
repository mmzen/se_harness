+++
id = "VER-PLG-001"
type = "verification"
title = "Independent package contents and shared-source evidence"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-09"

[relations]
verifies = ["REQ-PLG-001","REQ-PLG-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-09T18:23:58Z"
decided_by = "assurance-owner"
reason = "Operator explicitly approved the reviewed plugin packets in this task: i approve the packets, i authorize the work. On 2026-09-09 the operator selected go for WO-PLG-001 after the D03 delivery and assembly-first sequence were presented. This records the named definition approval from proposal be8b4126; it does not start WO-PLG-002."
+++

# Verification Contract: Independent package contents and shared-source evidence

## Independence

Expected wheel bytes come from the immutable published release and its independently obtained SHA-256. Build inventories are compared with source files, not trusted as their own oracle.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-001 | test, inspection | C01–C03 | Published wheel digest and byte inventory match; forbidden payloads are absent. |
| REQ-PLG-002 | test, inspection | C01, C04–C08 | Shared bytes match; unsafe or incomplete outputs are not usable. |

## Acceptance scenarios

Each case creates new test evidence under `evidence/WO-PLG-001/Cnn/`: `actions.txt`, `stdout.txt`, `stderr.txt`, and `observations.json`; these are not plugin APIs.
`observations.json` records expected/observed values, exit status, source evidence paths and a pass/fail/unavailable conclusion. The Evidence column names additional captures.

| Case | Starting fixture | Action | Observable result | Evidence |
| --- | --- | --- | --- | --- |
| C01 | Trusted published wheel, one source revision, two empty output directories | Independently compute canonical wheel payload SHA-256 with existing wheel_payload_sha256; assemble both packages. | Both packages/ wheels match the trusted archive SHA-256; each inventory records the same evaluator version, independently computed payload SHA-256, source revision and file digests. | archive/payload calculations; both inventories |
| C02 | Missing wheel, then a wheel with one changed byte | Attempt assembly for each input. | Each attempt returns nonzero and identifies the failed wheel; no output is marked usable. | exit codes; stderr; output listing |
| C03 | Inputs containing a Python runtime, candidate wheel, extra downloaded dependency, or top-level bin/ | Assemble each forbidden variant. | No usable output contains any forbidden entry; rejection identifies the entry. | input/output inventories; rejection |
| C04 | One shared source file missing, then divergent shared bytes in one host output | Assemble or inspect both outputs. | Missing source prevents usable assembly; digest comparison rejects the divergent pair. | source and output digests |
| C05 | One manifest from each host and a conflicting destination path | Assemble each host; repeat with the conflict. | Each valid output has only its own integration files; the conflict is rejected. | host inventories; conflict result |
| C06 | Destination path escapes output; an outside sentinel file exists | Attempt the escaping write. | Nonzero result names the unsafe destination; outside sentinel bytes and directory listing remain unchanged. | before/after sentinel digest; result |
| C07 | An output inventory omits one packaged file | Run package acceptance. | Inventory comparison names the missing entry; the output is not accepted as usable. | independent listing; inventory diff |
| C08 | Assembly interrupted after its first copied file | Inspect and retry the incomplete output. | The partial output is identified as incomplete; only a complete rechecked inventory can be accepted. | interruption trace; partial/final inventories |

## Property and invariant tests

C01 and C04 compare every shared file across both outputs. C03 and C06 account for forbidden contents and writes outside the output.

## Static and architecture checks

Map the source/output inventory to PLG-PKG-001–007, ARCH-PLG-001 and ADR-PLG-001. Retain the manifest comparison as review evidence.

## Security and privacy checks

Use synthetic paths and sentinels. Inventories retain names and digests, without secret environment values.

## Performance and resilience checks

C08 retains the interruption point and output states. Record assembly durations separately from host activation.

## Manual assessments

Run assembly on each claimed Windows, Linux or macOS platform. Record platform, source revision and selected evaluator release; list unavailable platforms explicitly.

## Evidence retention

Retain each case’s fixture revision, argv, exit status, raw output and listed observations under `evidence/WO-PLG-001/Cnn/`.
Record expected and observed values separately, with a pass/fail/unavailable conclusion. Keep original failures and bind later assurance to the exact implementation candidate.

## Residual uncertainty

Package assembly does not establish native discovery or publication authority. These are planned checks, not results.
