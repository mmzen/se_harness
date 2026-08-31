+++
id = "VER-ECP-018"
type = "verification"
title = "Independent evidence for the harnessctl command shape"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-30"
updated = "2026-08-30"

[relations]
verifies = ["REQ-ECP-027"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-30T16:56:30Z"
decided_by = "assurance-owner"
reason = "Approved by the assurance owner on 2026-08-30 with the words 'Approve and start WO-ECP-021': target classification, naming, JSON, exit-code, stdout, one-code, one-cause, CLI-coverage and reference rows, every one driven through main() with collaborators mocked at the module boundary."
+++

# Verification Contract: Independent evidence for the harnessctl command shape

## Independence

Expected behaviour derives from `REQ-ECP-027` and the `ECP-CLI-` rules of
`SPEC-ECP-016`. Every test drives `main()`; where a command needs an
environment (a verifier venv, a wheel, a network), the collaborator is
mocked at the module boundary and the test asserts the arguments the
handler passed.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-027` target | test: parser introspection | every subcommand and `qualify` role | the three sets of `ECP-CLI-001` equal the parser's; no repository command has a second repository option |
| `REQ-ECP-027` naming | test: `prepare-release --owner`; `--authorized-by` | fixture | record `owner` recorded; `--authorized-by` exits 2, stdout empty, stderr names `--owner` |
| `REQ-ECP-027` JSON | test: `--json` on each of the eleven commands | fixture repository, mocks for `identity`/`qualify`/`rehearse-recovery` | one JSON object, `schema` and `command` present, members per `ECP-CLI-003`; existing JSON shapes unchanged (`check`, `transition`, `validate`, `inspect`, `release-unit`, `renumber-artifacts`, `qualify`) |
| `REQ-ECP-027` exit codes | test: one completed, one failed and one refused invocation per class | fixture | `0`/`1`/`2` per `ECP-CLI-004`; `capture-verification` on an `in_progress` WO exits `1` |
| `REQ-ECP-027` stdout | test: failed `capture-verification` with and without `--json` | fixture | result on stdout, stderr empty |
| `REQ-ECP-027` one code | test: `check --artifact REQ-…`; a blocked `capture-verification` | fixture | every `blocked_by` line matches `^[A-Z0-9-]+: ` exactly once at its start |
| `REQ-ECP-027` one cause | test: four refusals of `capture-verification` (state, dirty tree, evaluator script failure, bad evidence path) | fixture with the dashboard script mocked to fail | `WEX301`, `WEX302`, `WEX303`, `WEX304` respectively |
| `SPEC-ECP-016` CLI coverage | test: `main()` for the five commands | mocks | each exits per the rule and prints its JSON |
| `SPEC-ECP-016` reference | test: the reference has the rules section and `--json` in every synopsis | `docs/notes/harnessctl-reference.md` | as stated; the command table still equals the parser's set |

## Acceptance scenarios

1. `harnessctl doctor . --json` on a clean fixture: one object, every check
   `passed`, exit `0`.
2. `harnessctl capture-verification …` on an `in_progress` work order:
   stdout carries the result, `blocked_by[0]` starts with `WEX301: ` once,
   exit `1`; the same with a dirty tree: `WEX302`.
3. `harnessctl prepare-release … --authorized-by x`: exit `2`, stderr names
   `--owner`.

## Evidence retention

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-022/`.

## Pass criteria

Every deterministic test passes on the Linux lane; the Windows workstation
reading is at its baseline. Graph and integrity readings come from the
exact released evaluator, se-harness 0.11.0, installed outside the checkout.

## Residual uncertainty

The 0.11.0 root evaluator keeps the old shape until the next adoption; the
managed lane runs the root copy and is unaffected.
