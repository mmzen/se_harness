+++
id = "VER-ECP-021"
type = "verification"
title = "Independent evidence for the tombstone retirement"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-02"
updated = "2026-09-02"

[relations]
verifies = ["REQ-ECP-030"]
+++

# Verification: Independent evidence for the tombstone retirement

## Method

| Requirement | Method | Pass condition |
| --- | --- | --- |
| `REQ-ECP-030` no guard | test reading `main()`'s source; `--help` | `se_harness/cli.py` `main()` contains no pre-parse guard for `"focus"`, `"next"`, `"accept-candidate"` or `"--authorized-by"`; `--help` lists none of the three names and `prepare-release --help` lists no `--authorized-by` |
| `REQ-ECP-030` plain refusal | test: invoke each name through `main()` | exit 2, empty stdout, argparse usage error on stderr, no handler called |
| `REQ-ECP-030` records | inspection | the refusal tests are gone; the amendment records named by `SPEC-ECP-019` `ECP-TMB-005` are present and dated; the three notes read as `ECP-TMB-004` states |
| `REQ-ECP-030` no regression | the full suite; `validate`; `doctor` | suite at its baseline; graph 0 errors; managed set untouched |
| `SPEC-ECP-019` delegation | the work order's own lifecycle events | the start, implemented and record-preparation events name `delegated-executor` with the class, the check-run id and the head sha; the approval and verification events name humans |

## Independence

The source-reading assertion does not depend on the guard's own message;
the refusal comes from argparse, not from product code the work order
touches.

## Evidence

`docs/engineering/execution-control-plane/evidence/WO-ECP-025/`.
