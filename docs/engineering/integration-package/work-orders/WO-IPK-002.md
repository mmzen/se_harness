+++
id = "WO-IPK-002"
type = "work_order"
title = "Allow the retained source evidence within a fixed integration archive budget"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-12"
updated = "2026-10-12"

[assurance]
commit_bound_verification = "required"
rationale = "mmzen confirmed required commit-bound verification because later integration-package and review decisions rely on the exact bounded extraction behavior and CI result."
decided_by = "mmzen"

[execution_scope]
paths = [
  ".github/scripts/build_integration_package.py",
  "tests/test_integration_package.py",
  "docs/engineering/integration-package/work-orders/WO-IPK-002.md",
  "docs/engineering/integration-package/verification/VER-IPK-002.md",
  "docs/engineering/integration-package/evidence/WO-IPK-002/",
]

[relations]
implements = ["REQ-IPK-001"]
specifications = ["SPEC-IPK-001"]
architecture = ["ARCH-IPK-001", "ADR-IPK-001"]
verification = ["VER-IPK-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-12T07:49:46Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"Ok continue\" after the explicit request to approve WO-IPK-002 and VER-IPK-002, required commit-bound verification and inclusion in draft PR #543. Approves the reviewed three-line correction: fixed source-archive/expanded-total cap from 512 MiB to 1 GiB and two matching test lines, preserving all other protections and historical evidence. Authorizes bounded local execution, checks, evidence, completion and verification preparation, and ordinary review pushes/updates in mmzen/se_harness from codex/hosted-agent-qualification to main, including the ready record and later separately supplied verification decision. Keep PR #543 draft while qualification or verification is incomplete. Human verification, merge, release, deployment and changes beyond this scope remain separate."
scope_paths = [".github/scripts/build_integration_package.py", "tests/test_integration_package.py", "docs/engineering/integration-package/work-orders/WO-IPK-002.md", "docs/engineering/integration-package/verification/VER-IPK-002.md", "docs/engineering/integration-package/evidence/WO-IPK-002/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-12T07:51:31Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-12T08:18:35Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed."
+++

# Restore the integration-package build

## Objective

Build the exact qualification commit with its retained evidence, using the
existing deterministic integration-package lane and a fixed 1 GiB source budget.

## In scope

Change MAX_ARCHIVE_TOTAL from 512 MiB to 1 GiB (1,073,741,824 bytes). This constant
limits both the Git archive file and its expanded regular-file total. Update the
matching constant assertion and the existing above-limit test fixture. Retain
the old failure, actual archive counts/hashes and new check results.

## Out of scope

Evidence deletion or relocation, selecting a smaller source tree, automatic
growth, a limit override, workflow permissions/triggers, artifact retention rules,
wheel budgets, product/runtime changes, release, merge and deployment.

## Authorized decision envelope

Approval would authorize this two-file implementation, local checks, exact-commit
CI qualification, evidence, commits, implementation completion and required
verification preparation. Proposed review-publication grant: include this work,
its two formal records, evidence, ready verification record and later separately
given verification decision in mmzen/se_harness PR #543, source
codex/hosted-agent-qualification, target main. Ordinary push/update only; keep
the PR draft while qualification or human verification remains incomplete.

Human verification and merge remain separate. No scope expansion or threshold
beyond 1 GiB is authorized. The current draft records no approval.

## Proposed assurance

Require commit-bound verification: integration-package provenance and later
review decisions depend on the exact bounded extraction behavior and CI result.
The human must confirm this classification. No assurance decision-maker is
invented in draft metadata.

## Constraints and rationale

C43's exact source tar is 542,105,600 bytes, above the old 536,870,912-byte limit.
CI run 38208621228 failed its build at that check. The source and installed-package
jobs passed. The retained qualification evidence explains the growth.

Keep the 128 MiB member cap, 20,000-entry cap, all path/type/link/duplicate checks,
exact Git export, complete tree comparison, two independent builds and same-byte
Windows/Linux verification. The larger budget raises worst-case temporary disk
use; it grants no public or production authority.

The existing REQ-IPK-001, SPEC-IPK-001, ARCH-IPK-001 and ADR-IPK-001 still govern
the lane. This is a capacity choice inside that design. WO-CIP-009 and VER-CIP-005
retain their historical 512 MiB definition and observations; neither is edited
or used as authority for this new work. No accepted record is amended.

A smaller export would change the exact-source comparison. Moving historical
evidence would affect bindings and review access. Both require broader work;
a fixed bound in the existing builder is the smaller correction.

## Expected change surface

| Inspected path | Needed change |
| --- | --- |
| .github/scripts/build_integration_package.py | One source-archive constant; both existing checks continue to consume it |
| tests/test_integration_package.py | Expect 1 GiB and use nine declared 128 MiB members for the existing expanded-total refusal |
| This WO and VER-IPK-002 | Scope, verification and later actual decisions |
| evidence/WO-IPK-002/ | Review, exact diff, original failure, checks, archive facts, handoff and verification-preparation evidence |

Inspected candidate-evidence.yml remains unchanged; it already consumes this
builder and runs both platform verifiers. Public instructions, packaging,
dependencies and runtime source need no change. VREC/evaluator-sidecar paths are
allocated by released preparation later; assess their direct relationship under
the existing generated-output rule rather than granting a parent directory.

## Required verification and evidence

Run VER-IPK-002 with released evaluator 0.22.1 outside the checkout. Retain exact
commands, candidate/head/merge identities, exits, archive counts/digests, source
suite, focused checks and CI build/verify/retain results at the scoped evidence
directory. Preserve native qualification evidence unchanged.

## Stop and escalate

Stop for a changed candidate that exceeds the new bound, another boundary failure,
new path, changed protection, failed required check or uncertain external effect.
Do not make CI green by dropping evidence or weakening another check.

## Completion report

Report the changed bound, exact candidate, checks and CI identities, preserved
protections, resource cost, unresolved checks and evaluator-selected next step.
Completion does not supply human verification or merge authority.
