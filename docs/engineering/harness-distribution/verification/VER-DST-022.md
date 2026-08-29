+++
id = "VER-DST-022"
type = "verification"
title = "Independent evidence for the retirement of leaving-set managed paths"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
verifies = ["REQ-DST-066"]
+++

# Verification Contract: Independent evidence for the retirement of leaving-set managed paths

## Independence

Expected behaviour derives from `REQ-DST-066` and the `DST-UPR-` rules of
`SPEC-DST-022`, not from the implementation. The conformance tests build
their roots in temporary directories with lock entries and bytes the tests
write themselves, so no host Git settings and no shipped template bytes
decide an outcome; the leaving-set fixture paths are the fifteen retired
0.10.0 skill paths read from the released history, not from candidate code.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-DST-066` plan | test: a lock managing the fifteen retired paths with matching bytes | `tests/test_standard_repository_lifecycle.py` | every leaving-set path plans `remove`; in-set paths keep their classification |
| `REQ-DST-066` apply | test: apply the plan | same module | the fifteen files are deleted, their emptied directories are pruned, the lock names none of them, a replay plans no change |
| `REQ-DST-066` customization | test: one retired path carries an owner edit | same module | the path plans `customized`; `--apply` refuses before any write; every byte is retained |
| `REQ-DST-066` transaction | test: interrupt the apply after the deletions | same module | the snapshot restores every deleted file |
| `DST-UPR-001` seed and missing paths | test: a leaving-set `seed` entry and a leaving-set entry with no file | same module | the seed file is untouched; both entries leave the lock; neither plans an action |
| `DST-UPR-006` evidence | test: apply with `--evidence-output` | same module | the evidence `plan` records the `remove` actions under the unchanged schema id |
| `DST-UPR-008` note | analysis: read the note | `docs/notes/harness-installation-and-upgrades.md` | the removal rule and the fifteen 0.11.0 remediation paths are stated |
| `SPEC-DST-022` single drop point | analysis: grep `installer.py` for lock rebuild sites | the work order's evidence packet | leaving-set entries are dropped in exactly one place, through the plan |

## Acceptance scenarios

### Scenario 1: mechanical retirement

Install a root, extend its lock and disk with the fifteen retired paths and
matching digests, upgrade, and assert plan, deletion, pruning, lock omission
and no-op replay.

### Scenario 2: owner edit refuses

Edit one of the fifteen files, plan and apply, and assert the `customized`
report and the untouched tree.

### Scenario 3: interrupted apply restores

Force a failure after the deletions inside the transaction and assert every
file returns.

## Evidence retention

Under `docs/engineering/harness-distribution/evidence/WO-DST-022/`.

## Pass criteria

Every deterministic test passes on the Linux lane; the Windows workstation
reading is compared against its control baseline at the same commit. Graph
and integrity readings come from the exact released evaluator, se-harness
0.11.0, installed outside the checkout.

## Residual uncertainty

Consumers that already upgraded to 0.11.0 hold locks that no longer name the
orphaned paths; no mechanical check can see those copies, so their cleanup
rests on the documented manual deletion. The released 0.11.0 evaluator keeps
its behaviour until a release carries this change.
