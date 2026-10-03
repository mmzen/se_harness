+++
id = "WO-DST-028"
type = "work_order"
title = "Raise topology acceptance to four mebibytes"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"

[assurance]
commit_bound_verification = "required"
rationale = "mmzen authorized required verification with the bounded manual amendment and two-file correction; acceptance and publication depend on this trusted target and its tests."
decided_by = "mmzen"

[execution_scope]
paths = [
  "se_harness/engine/dashboard_bundle.py",
  "tests/test_dashboard_webui.py",
  "docs/engineering/harness-distribution/requirements/REQ-DST-055.md",
  "docs/engineering/harness-distribution/requirements/REQ-DST-062.md",
  "docs/engineering/harness-distribution/requirements/REQ-DST-063.md",
  "docs/engineering/harness-distribution/specifications/SPEC-DST-013.md",
  "docs/engineering/harness-distribution/specifications/SPEC-DST-017.md",
  "docs/engineering/harness-distribution/specifications/SPEC-DST-020.md",
  "docs/engineering/harness-distribution/specifications/SPEC-DST-023.md",
  "docs/engineering/harness-distribution/verification/VER-DST-013.md",
  "docs/engineering/harness-distribution/verification/VER-DST-017.md",
  "docs/engineering/harness-distribution/verification/VER-DST-020.md",
  "docs/engineering/harness-distribution/architecture/ARCH-DST-013.md",
  "docs/engineering/harness-distribution/work-orders/WO-DST-028.md",
  "docs/engineering/harness-distribution/verification/VER-DST-030.md",
  "docs/engineering/harness-distribution/evidence/WO-DST-028/",
  "docs/engineering/release-orchestration/verification-records/VREC-RLO-015.md",
  "docs/engineering/release-orchestration/evidence/VREC-RLO-015-evaluator.json"
]

[relations]
implements = ["REQ-DST-062", "REQ-DST-063"]
specifications = ["SPEC-DST-020"]
verification = ["VER-DST-030"]
architecture = ["ARCH-DST-013"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-03T03:35:59Z"
decided_by = "mmzen"
reason = "mmzen explicitly authorized the reviewed bounded manual amendment to exactly 4 MiB, preservation and links for the previous accepted definitions, the two-file correction and required verification. This records that supplied instruction; the manual amendment exception does not waive lifecycle gates or human assurance. The approved RLS-SEH-032 candidate and archives remain unchanged."
scope_paths = ["se_harness/engine/dashboard_bundle.py", "tests/test_dashboard_webui.py", "docs/engineering/harness-distribution/requirements/REQ-DST-055.md", "docs/engineering/harness-distribution/requirements/REQ-DST-062.md", "docs/engineering/harness-distribution/requirements/REQ-DST-063.md", "docs/engineering/harness-distribution/specifications/SPEC-DST-013.md", "docs/engineering/harness-distribution/specifications/SPEC-DST-017.md", "docs/engineering/harness-distribution/specifications/SPEC-DST-020.md", "docs/engineering/harness-distribution/specifications/SPEC-DST-023.md", "docs/engineering/harness-distribution/verification/VER-DST-013.md", "docs/engineering/harness-distribution/verification/VER-DST-017.md", "docs/engineering/harness-distribution/verification/VER-DST-020.md", "docs/engineering/harness-distribution/architecture/ARCH-DST-013.md", "docs/engineering/harness-distribution/work-orders/WO-DST-028.md", "docs/engineering/harness-distribution/verification/VER-DST-030.md", "docs/engineering/harness-distribution/evidence/WO-DST-028/", "docs/engineering/release-orchestration/verification-records/VREC-RLO-015.md", "docs/engineering/release-orchestration/evidence/VREC-RLO-015-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-03T03:37:21Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-03T03:54:10Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed."
+++

# Raise topology acceptance to four mebibytes

## Objective

Restore full-suite acceptance after ordinary artifact growth by raising the
explicit topology target from 2,097,152 to 4,194,304 UTF-8 bytes. At the reviewed
baseline the graph measured 2,099,060 bytes. This gives about 50% headroom.

## In scope and expected change surface

Change one constant in se_harness/engine/dashboard_bundle.py and two candidate
assertions in tests/test_dashboard_webui.py. Retain the legacy installed-root
assertion at its released value. Existing boundary tests use the selected target.
Apply only the eleven reviewed capacity revisions and preserve their complete
accepted predecessors and byte digests in evidence/WO-DST-028/. Record the exact
manual amendment and human authorization; do not claim a supported CLI revision.

## Authority and decision envelope

On 2026-10-03 mmzen requested the limit increase, then explicitly authorized the
reviewed 4 MiB manual amendment and correction with required verification.
This work order records that bounded instruction. No second decision on the
same limit is requested. Codex may execute local changes, tests, commits,
evidence retention, completion and combined verification preparation with
WO-RLO-018 under the recorded approval. Use proposed VREC-RLO-015 after checking
availability. Continue the existing correction branch and review PR #529 under
its retained review-push authorization. Human assurance acceptance and merge
remain separate; existing RLS-SEH-032 publication authority is not broadened.

## Constraints and out of scope

Preserve accepted predecessor bytes before amending definitions. Preserve all
lifecycle states and histories; lifecycle operations still use released 0.21.0
outside this checkout. Manual links are human-readable evidence, not invented
machine relations. No topology omission, sharding, schema, dependency, browser,
serializer, integrity, hard content budget, version, installed root or CI policy
change. No redefinition of completed work. No changes to the approved 0.22.0
candidate, RLS-SEH-032, VREC-SEH-032, archives, recipe or evaluator lock/config.
The larger constant belongs to development source for a future package release.

## Verification and retained evidence

Meet VER-DST-030 and retain its results under evidence/WO-DST-028/. Reuse the
unchanged publisher correction evidence where applicable; rerun the full suite,
dashboard tests on Windows/Linux and applicable hosted checks. Preserve the
original 2 MiB failure. Use complete PR baseline
01ec43c86c9d30949295c07ac91c742be91e713a with the union of WO-RLO-018/WO-DST-028.

## Stop conditions

Stop affected work for another source file, changed release identity, mismatched
predecessor digest, data loss, another budget change or a failed required check.
Do not raise the target beyond 4 MiB or accept verification on the owner's behalf.

## Completion report

Report the exact candidate, observed topology and headroom, boundary results,
full-suite and hosted results, unchanged release inputs, manual-amendment limits
and the remaining human verification decision.
