+++
id = "VER-DST-027"
type = "verification"
title = "Evidence for the wave 5 managed template hygiene"
status = "draft"
owners = ["quality-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-DST-072", "REQ-DST-073", "REQ-DST-074", "REQ-DST-075"]
+++

# Verification Contract: Evidence for the wave 5 managed template hygiene

## Independence

Cases are written from the rule identifiers of `SPEC-DST-027`, not from the
diff. The install and upgrade cases run against a throwaway target from a
wheel built from the candidate and installed in a virtual environment outside
the checkout, which is how a consumer meets the change. The failure-surface
case runs the template's embedded reader as a consumer's runner would, on an
empty file and on a refusal's stderr. The candidate suite runs on the hosted
Linux lane; the local Windows suite is a control, not the record.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-DST-072` | test | the template text (DST-MWF-001) | neither `check` step appends `|| true`; each captures status and stderr |
| `REQ-DST-072` | test | the embedded reader on an empty result file (DST-MWF-002) | the step's script exits with the captured status and prints the captured stderr; no traceback |
| `REQ-DST-072` | test | the embedded reader on a completed and on a blocked result (DST-MWF-003) | the same verdicts and messages as before the change |
| `REQ-DST-074` | test | header versus steps (DST-MWF-004) | every step the header names exists; `doctor` and `validate` are not named |
| `REQ-DST-074` | test | the three `uses:` lines (DST-MWF-005) | each matches `@[0-9a-f]{40} # v\d+\.\d+\.\d+` |
| `REQ-DST-073` | test | `init` into an empty directory (DST-MWF-006) | the `.gitignore` block opens with `# se-harness:begin`; `git check-ignore` reports no rule for the marker text |
| `REQ-DST-073` | test | upgrade of a fixture installed by released 0.16.0 (DST-MWF-007, DST-MWF-008) | the plan classifies `.gitignore` as a safe fragment rewrite; afterwards the block carries hash markers, the owner lines are byte-identical, `doctor` passes |
| `REQ-DST-073` | test | the same fixture with one edited line inside the block | the plan reports customized, apply refuses, the file is unchanged |
| `REQ-DST-075` | test | the environment inventory (DST-MWF-011) | the names read under `se_harness/` are exactly the pinned two, and each occurs in a specification |
| `REQ-DST-075` | inspection | `SPEC-ECP-006` and the delegation note (DST-MWF-009, DST-MWF-010) | the amendment record names the variable and the rule it serves; the note names it beside `local-file` |
| all | inspection | this repository's root (DST-MWF-013) | the work order's diff touches no root managed file and not the lock |
| all | regression | the full suite, `validate`, `doctor`, the hosted lanes | suite at its baseline; graph 0 errors under the released 0.16.0 evaluator; every lane green at the head |
| all | the work order's own lifecycle events | the start, implemented and record-preparation events name `delegated-executor` with the class, the check-run id and the head sha; the approval and verification events name humans |

DST-MWF-014 binds the later root-adoption work order and is verified by its
contract, not this one.

## Acceptance scenarios

Scenario A, consumer install: build the candidate wheel, install it outside
the checkout, `init` an empty directory, then run `doctor` and `git
check-ignore` on the marker text. Expected: success, hash markers, no
pattern.

Scenario B, consumer upgrade: take a repository initialized by released
0.16.0, run the candidate's `upgrade` plan and `upgrade --apply`. Expected:
the ignore file planned as a safe rewrite, hash markers afterwards, owner
lines unchanged, the managed workflow rewritten with the new header and pins,
`doctor` passing.

Scenario C, refusal surface: run the template's embedded reader with an
empty result file and a stderr file holding a guard message. Expected: the
message in the output, the captured status as the exit code, no traceback.

## Evidence retention

`docs/engineering/harness-distribution/evidence/WO-DST-026-verification.md`
with the template before and after, the scenario outputs, the upgrade plan,
the environment inventory, the hosted lane's test report and the local
control reading labelled as such.

## Pass criteria

Every row passes on the hosted Linux lane and on the Windows workstation;
the released 0.16.0 evaluator's `validate` reports 0 errors; the pull
request's lanes are green through completion and the record head; no root
managed byte changes.

## Residual uncertainty

The failure surface is exercised by running the embedded reader, not by a
live refusal in a consumer's lane; the first live observation is the first
consumer refusal after the carrying release. This repository's own root is
not exercised here; the root-adoption work order verifies it.
