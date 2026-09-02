+++
id = "VER-CIP-002"
type = "verification"
title = "Independent evidence for the base-aware rehearsal selection"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-09-02"
updated = "2026-09-02"

[relations]
verifies = ["REQ-CIP-007"]
+++

# Verification: Independent evidence for the base-aware rehearsal selection

## Method

| Requirement | Method | Pass condition |
| --- | --- | --- |
| `REQ-CIP-007` selection | test on a temporary Git repository | with `base_ref`, only records committed on the base are candidates and the newest ready or released schema-2 one is chosen with a reason naming the ref; without it, the working tree is read as before; an explicit request absent from the base is refused |
| `REQ-CIP-007` workflow | YAML inspection by test | the `select` job fetches the base and passes `--base-ref refs/remotes/origin/BASE, where BASE is the pull request's base branch` only when `github.event_name == 'pull_request'`; the `rehearse-record` job still passes `default_ref: refs/remotes/origin/main` and `require_status` from the selection |
| `REQ-CIP-007` run observation | the pull request that carries this change | its own record-mode lane selects the newest record on `main` and passes at the head; the candidate lane passes |
| `REQ-CIP-007` no regression | the full suite; `validate`; `doctor` | suite at its baseline; graph 0 errors; managed set untouched |
| `SPEC-CIP-002` delegation | the work order's own lifecycle events | the start, implemented and record-preparation events name `delegated-executor` with the class, the check-run id and the head sha; the approval and verification events name humans |

## Independence

The selection test builds its own Git history and reads the selector's
output, not the workflow's; the workflow assertion parses the YAML; the run
observation is GitHub's check result on the pull request's head.

## Evidence

`docs/engineering/ci-pipeline/evidence/WO-CIP-006/`.
