+++
id = "WO-IAR-034"
type = "work_order"
title = "Align installer regression fixtures with minimal installation"
status = "implemented"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-10-01"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen approved WO-IAR-034 and required commit-bound verification, included in VREC-IAR-020. Later acceptance and release decisions rely on these tests and their fixture inputs."
decided_by = "mmzen"

[execution_scope]
paths = [
  "tests/test_harnessctl.py",
  "tests/fixture_support.py",
  "tests/test_fixture_support.py",
  "tests/test_configuration_surface.py",
  "tests/test_managed_template_hygiene.py",
  "tests/test_standard_repository_lifecycle.py",
  "tests/test_mutation_guard.py",
  "tests/test_repository_context_retirement.py",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-034.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-034/",
  "docs/engineering/instruction-architecture/verification-records/VREC-IAR-020.md",
  "docs/engineering/instruction-architecture/evidence/VREC-IAR-020-evaluator.json",
]

[relations]
implements = ["REQ-IAR-031"]
specifications = ["SPEC-IAR-016"]
architecture = ["ARCH-IAR-012", "ADR-IAR-012"]
verification = ["VER-IAR-022"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T18:14:43Z"
decided_by = "mmzen"
reason = "Human mmzen stated: i approve WO-IAR-034 and required commit-bound verification, included in VREC-IAR-020. Reviewed draft SHA256 450e493f4dc481700416f7fcb3e69a41ced3bb810faf93edd312a94c9fe2dd6c; only confirmed assurance metadata was added before this preview."
scope_paths = ["tests/test_harnessctl.py", "tests/fixture_support.py", "tests/test_fixture_support.py", "tests/test_configuration_surface.py", "tests/test_managed_template_hygiene.py", "tests/test_standard_repository_lifecycle.py", "tests/test_mutation_guard.py", "tests/test_repository_context_retirement.py", "docs/engineering/instruction-architecture/work-orders/WO-IAR-034.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-034/", "docs/engineering/instruction-architecture/verification-records/VREC-IAR-020.md", "docs/engineering/instruction-architecture/evidence/VREC-IAR-020-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-30T18:16:32Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-01T17:49:35Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Completed the approved local scope and retained integrated tests, review and complete Git handoff. Codex desktop remains explicitly unverified under the existing human instruction to continue; no assurance acceptance or external action is inferred."
+++

# Align installer regression fixtures with minimal installation

## Objective

Keep the existing regression suite useful when WO-IAR-030 changes default
initialization to the two selection files. Static review found direct callers
and assertions that still require copied instructions, templates, Git fragments,
CI files and an adoption report. The eight test files below are outside
WO-IAR-030's approved paths. No new product behavior is proposed here.

## In scope and expected change surface

| File | Bounded change |
| --- | --- |
| tests/test_harnessctl.py | Check the minimal default and explicitly selected integrations; retain existing-input, refusal and repeat-install cases. |
| tests/fixture_support.py | Make materialized legacy fixtures explicit so unrelated lifecycle tests retain their intended inputs. Do not silently change the production CLI used by tests. |
| tests/test_fixture_support.py | Keep cache reuse and byte-equality checks against the explicitly selected fixture construction. |
| tests/test_configuration_surface.py | Check new selection fields and preserve owner-configuration and supported legacy-upgrade coverage. |
| tests/test_managed_template_hygiene.py | Request the relevant optional Git or CI integration before asserting its contents; retain owner-byte and marker checks. |
| tests/test_standard_repository_lifecycle.py | Distinguish selected integration and legacy fixtures; preserve leaving-file, rollback, repetition and hash-bound byte checks. |
| tests/test_mutation_guard.py | Adapt fixture preparation while preserving mutation-authority refusals and stale-plan checks. |
| tests/test_repository_context_retirement.py | Replace the obsolete automatic adoption-report expectation with the minimal-install boundary; retain retired-context and owner-content checks. |

The execution_scope list is the complete write surface. Product implementation,
documentation, new installer tests and the shared artifact helper remain under
WO-IAR-030. Reuse the selected accepted definitions unchanged. Carry out the two
work orders together where their inputs depend on one another.

## Out of scope and constraints

No new CLI profile, test framework, product behavior, gate waiver, test skipping,
weakened refusal, or blanket interception that makes old tests silently call a
different CLI. Keep tests for older layouts explicit. Do not edit accepted
definitions, installed harness files, selection records, past decisions or
historical evidence. Any additional path returns for scope review.

## Proposed assurance classification

Required commit-bound verification. Future acceptance and release decisions rely
on these tests and their fixture inputs. This classification awaits human
confirmation; no assurance decision-maker is recorded in this draft.

## Authorized decision envelope

After approval, the executor may adapt the named tests and fixtures, run checks,
retain evidence, make local commits, record completion and prepare the combined
verification record. Human verification and external actions retain their
separate authority requirements.

## Required verification

Apply VER-IAR-022. Run affected modules during implementation and the existing
full suite on the final integrated candidate. Keep the exact two-file footprint,
explicit integration, owner preservation, invalid-input, interrupted transaction
and repeat-operation cases. Run required packaged and Windows/Linux checks
with WO-IAR-030. Report desktop qualification separately without substituting
CLI observations or changing the accepted verification contract.

## Evidence to record

Retain changes, actual invocations, results and review findings under
docs/engineering/instruction-architecture/evidence/WO-IAR-034/.
Include this work order alongside WO-IAR-028, WO-IAR-029 and WO-IAR-030 in the
planned final VREC-IAR-020, with VER-IAR-020, VER-IAR-021 and VER-IAR-022 at one
exact candidate. Check that the record ID remains unused before capture.
Do not rewrite earlier verification records or approvals.

## Stop conditions and completion

Stop affected work for changed requirements, an additional path, a weakened
check, a failed required check, or missing authority. Completion reports the
actual adapted cases, exact candidate, checks, limitations and evaluator next
step. This draft supplies no implementation authority.
