+++
id = "VER-CIP-004"
type = "verification"
title = "Independent evidence for the issue #433 pipeline repair"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-09-10"
updated = "2026-09-10"

[relations]
verifies = ["REQ-CIP-010"]
+++

# Verification Contract: Independent evidence for the issue #433 pipeline repair

## Independence

Expected values come from `REQ-CIP-010`, the rules of `SPEC-CIP-004` and
issue #433's acceptance, never from the changed files. The grep is run as the
issue states it, over the two directories, and read as text. The graph and
lifecycle readings come from the released 0.17.0 evaluator outside the
checkout.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-CIP-010` | inspection | issue #433 acceptance 2: `grep -rn governance-migration docs/engineering/ci-pipeline/architecture docs/engineering/ci-pipeline/requirements` | every hit is inside an amendment record of `ARCH-CIP-001` or `REQ-CIP-002` (CIP-AMD-001, CIP-AMD-002, CIP-AMD-004) |
| `REQ-CIP-010` | test | the definitions test in `tests/test_ci_pipeline.py` | it finds every occurrence of the old name under the two directories inside an `## Amendment record` section, and fails naming file and line otherwise (CIP-AMD-004) |
| `REQ-CIP-010` | inspection | the two amendment records | each names the former name, `WO-CIP-007` as the renaming work order and the date; `REQ-CIP-002`'s also names the reconcile job's removal under `WO-CIP-001` |
| `REQ-CIP-010` | analysis | the diff of the two definitions against `main` | front matter changes only in `updated`; the statement, relations, lifecycle events and decision assessment are byte-identical (CIP-AMD-003) |
| `REQ-CIP-010` | inspection | the domain index and the change set | the index names the repair; no path under `.github/`, `scripts/`, `repository_tools/` or a managed path is in the change set (CIP-AMD-005) |
| `REQ-CIP-010` | regression: the full suite, `validate`, `doctor`, the hosted lanes | suite at its baseline; graph 0 errors under the released 0.17.0 evaluator; every lane green at the head |
| `REQ-CIP-010` | the work order's own lifecycle events | the start, implemented and record-preparation events name `delegated-executor` with the class, the check-run id and the head sha; the approval and verification events name humans |

## Acceptance scenarios

- Run the grep of acceptance 2 before and after; record both outputs in the
  evidence packet.
- Reinsert the old name into a scratch copy's Components section: the
  definitions test fails and names the file and line.
- Diff the two definitions' front matter against `main`: only `updated`
  differs.

## Evidence retention

`docs/engineering/ci-pipeline/evidence/WO-CIP-008/`: the grep before and
after, the front-matter diff, the `validate` and `doctor` readings, the lane
results at the head and the handoff packet.

## Pass criteria

Every row passes on the hosted Linux lane and on the Windows workstation;
the released 0.17.0 evaluator's `validate` reports 0 errors; the pull
request's lanes are green through completion and the record head.

## Residual uncertainty

Historical evidence packets and verification records under the domain keep
the old name as a statement of what was true when they were written; the
grep of acceptance 2 does not cover them, by the issue's own wording.
