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
| `REQ-ECP-030` no guard | test reading `main()`'s source; `--help` | `se_harness/cli.py` `main()` contains none of `"focus"`, `"next"`, `"accept-candidate"` as a guarded first argument; `--help` lists none of the three |
| `REQ-ECP-030` plain refusal | test: invoke each name through `main()` | exit 2, empty stdout, argparse usage error on stderr, no handler called |
| `REQ-ECP-030` records | inspection | the refusal tests are gone; the amendment records named by `SPEC-ECP-019` `ECP-TMB-005` are present and dated; the three notes read as `ECP-TMB-004` states |
| `REQ-ECP-030` no regression | the full suite; `validate`; `doctor` | suite at its baseline; graph 0 errors; managed set untouched |

## Independence

The source-reading assertion does not depend on the guard's own message;
the refusal comes from argparse, not from product code the work order
touches.

## Evidence

`docs/engineering/execution-control-plane/evidence/WO-ECP-025/`.
