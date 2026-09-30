+++
id = "WO-IAR-033"
type = "work_order"
title = "Align the CLI reference and regression checks with external resources"
status = "in_progress"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification; future acceptance and release decisions rely on the corrected regression checks and command instructions."
decided_by = "mmzen"

[execution_scope]
paths = [
  "docs/notes/harnessctl-reference.md",
  "tests/test_cli_shape.py",
  "tests/test_integrity_primitives.py",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-033.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-033/",
  "docs/engineering/instruction-architecture/verification-records/VREC-IAR-021.md",
  "docs/engineering/instruction-architecture/evidence/VREC-IAR-021-evaluator.json",
]

[relations]
implements = ["REQ-IAR-029"]
specifications = ["SPEC-IAR-016"]
architecture = ["ARCH-IAR-012", "ADR-IAR-012"]
verification = ["VER-IAR-020"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T12:29:06Z"
decided_by = "mmzen"
reason = "Human mmzen replied: i approve. Confirms WO-IAR-033 and required commit-bound verification for the reviewed three-file PR #506 CI correction. Reviewed draft SHA-256 938053837b1bebc4b54d7590a32b2b81ee35cae015a1264345517609b38b4bc5. Reviewed patch SHA-256 05dc544eb7a097222603f8adae8d55b1c8a1b7a841245c280b252fb307b4fd7a. Only confirmed assurance metadata and its explanatory paragraph were completed before preview."
scope_paths = ["docs/notes/harnessctl-reference.md", "tests/test_cli_shape.py", "tests/test_integrity_primitives.py", "docs/engineering/instruction-architecture/work-orders/WO-IAR-033.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-033/", "docs/engineering/instruction-architecture/verification-records/VREC-IAR-021.md", "docs/engineering/instruction-architecture/evidence/VREC-IAR-021-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-30T12:29:48Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Align the CLI reference and regression checks with external resources

## Objective and exact correction

Correct the three failures in PR #506's candidate-source job without changing
the resource implementation or weakening its integrity checks. CI run
36714116390 assessed commit 5249f0c586c4194b255fc90aeeb4de29483b875a:
1,175 tests ran, with three failures and two skips. All three failures were
reproduced locally on that same source. The earlier focused qualification did
not run these three regression checks.

- docs/notes/harnessctl-reference.md: add resources to the command inventory;
  document its syntax, read-only result, one-resource content selection and
  successor-layout boundary. State that the selected 0.20.0 evaluator does
  not provide this candidate command.
- tests/test_cli_shape.py: classify resources as a repository command. Keep
  the exact command census, target-shape and JSON checks.
- tests/test_integrity_primitives.py: use schema 6 for the unknown-format
  refusal now that schema 5 is supported. Retain the pre-3 floor and
  noninteger refusals. Check that schema 5 rejects a missing or wrong
  resource-layout discriminator; existing resource tests cover valid schema 5.

The proposed patch is transient review material outside the repository. Apply
the reviewed three-file correction only after this work order is approved.

## Scope and constraints

The execution_scope paths are the complete write surface. Reuse the accepted
REQ-IAR-029, SPEC-IAR-016, ARCH-IAR-012, ADR-IAR-012 and VER-IAR-020 unchanged.
No new product behavior or architecture decision is proposed.

Do not change evaluator source, workflow files, installed instructions, root
selection, accepted definitions, historical evidence, VREC-IAR-018 or earlier
approvals. Do not remove, skip or weaken a required check. Keep WO-IAR-029's
separate branch and recorded start intact. This work does not start WO-IAR-030
or implement the plugin or installer migration.

## Confirmed assurance classification

Required commit-bound verification. Human mmzen confirmed the work order and
this classification by replying "i approve" to the explicit WO-IAR-033 and
required-verification request. Future acceptance and release decisions rely
on these regression checks and command instructions.

## Authorized decision envelope

Approval permits start, the reviewed edits, local commits, checks, evidence
retention, completion recording and preparation of VREC-IAR-021 under the
selected released 0.20.0 evaluator. Recheck that this VREC ID is unused before
capture. Human verification remains separate. Reuse the existing PR #506
push/PR authorization only after required checks and verification pass and
while the exact branch and destination match. No merge, release, marketplace
publication or adoption is included.

## Required verification and evidence

Use 5249f0c586c4194b255fc90aeeb4de29483b875a as this correction's trusted base.
Retain the failing CI run URL and local reproduction, their commands, runtime
identities, exit codes and raw-output digests under this work order's evidence
directory. Keep summaries small; raw logs stay outside the repository or in
the CI artifact, with their actual availability stated.

Run tests.test_cli_shape, tests.test_integrity_primitives,
tests.test_progressive_documentation and tests.test_resources. Then run the
complete source regression with scripts/run_tests.py --workers 4 --scale full,
matching the failed CI lane. Preserve failures and stop for a correction
outside these three files. Reuse unchanged packaged-resource qualification
from WO-IAR-028/031; compare code and package inputs to the verified candidate.
Do not claim new native-host qualification.

Run released validation, start/review preflight, the complete Git-derived
handoff and completion checks. Prepare VREC-IAR-021 at the exact clean
correction commit through the released capture procedure and declared
evaluator-companion path. Its test command reruns the relevant focused suite
at that commit. Required integration CI remains a separate check.

## Stop conditions and completion

Stop affected work for an out-of-scope correction, changed accepted contract,
failed required check, changed verified source, unavailable evidence or VREC
ID conflict. Report the precise correction needed without changing history.
Complete when the three-file correction and required evidence are ready and
completion checks pass. Report actual tests, unchanged implementation, exact
candidate, remaining CI state and the evaluator's next decision. Preparing
verification supplies no human acceptance.
