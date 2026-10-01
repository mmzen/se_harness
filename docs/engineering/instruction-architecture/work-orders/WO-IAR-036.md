+++
id = "WO-IAR-036"
type = "work_order"
title = "Align remaining onboarding and packaged-install regressions"
status = "in_progress"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification in VREC-IAR-020 by approving the reviewed WO-IAR-036 proposal. Acceptance and release rely on these regression and installed-wheel checks."
decided_by = "mmzen"

[execution_scope]
paths = [
  "tests/test_cli_shape.py",
  "tests/test_glossary.py",
  "tests/test_managed_template_texts.py",
  "tests/test_public_onboarding.py",
  "tests/test_release_build.py",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-036.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-036/",
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
decided_at = "2026-09-30T19:03:04Z"
decided_by = "mmzen"
reason = "Human mmzen: I approve WO-IAR-036. Approval answers the reviewed proposal including required commit-bound verification in VREC-IAR-020. Reviewed draft SHA256 76b8063350386b97a476ec5e2fdf75de922564110f5fe2f3fa400a05a0560559; only confirmed assurance metadata was added before preview."
scope_paths = ["tests/test_cli_shape.py", "tests/test_glossary.py", "tests/test_managed_template_texts.py", "tests/test_public_onboarding.py", "tests/test_release_build.py", "docs/engineering/instruction-architecture/work-orders/WO-IAR-036.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-036/", "docs/engineering/instruction-architecture/verification-records/VREC-IAR-020.md", "docs/engineering/instruction-architecture/evidence/VREC-IAR-020-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-30T19:03:37Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Align remaining onboarding and packaged-install regressions

## Objective

Adapt the five additional test files exposed by the integrated diagnostic run
install030-integration-diagnostic-04.json. The accepted minimal installation
changes the default CLI outputs. These files are outside WO-IAR-030, WO-IAR-034
and WO-IAR-035. This work adds no product behavior or installation profile.

## Expected change surface

| File | Bounded correction |
| --- | --- |
| tests/test_cli_shape.py | Keep JSON shape, preview and refusal checks; select external resource fixtures explicitly for minimal init. |
| tests/test_glossary.py | Preserve legacy glossary tests using explicit legacy fixtures; verify minimal init preserves an existing owner glossary without generating one. |
| tests/test_managed_template_texts.py | Select the intended resource fixture before drafting; retain the completion-authority assertions on the generated work order. |
| tests/test_public_onboarding.py | Preserve LF/CRLF legacy regressions with explicit legacy construction. Distinguish minimal init and the explicitly selected Git integration needed for evidence readiness. |
| tests/test_release_build.py | Keep wheel membership and no-duplicate checks. Update the real installed-wheel scenario to assert the two-file default, external resource identity, CLI validation and explicit integration. Do not expect copied repository skills. |

## Constraints and exclusions

Use the existing helpers and test framework. Unit resource-origin patches must
be explicit; the installed-wheel scenario must use the actual installed package
outside the checkout with isolated Python. Do not skip failures, weaken refusal
or owner-byte checks, intercept production CLI commands, or modify unrelated
legacy contracts. The two diagnostic failures caused by concurrent creation of
an incomplete WO-IAR-035 template need a stable rerun, not test edits.

Product code remains under the existing work orders. Changes to accepted
definitions, installed repository instructions, CI workflows, immutable released
evaluators, release/adoption, credentials and external actions are excluded.
Any additional path or changed requirement returns for review.

## Proposed assurance

Required commit-bound verification, included in the integrated VREC-IAR-020.
Acceptance and release decisions rely on these tests and the installed-wheel
scenario. Human confirmation is pending; no assurance decider is supplied yet.

## Authorized decision envelope

After approval, adapt the named tests, run checks, retain evidence, make local
commits, record completion and prepare the combined verification record. This
draft grants no implementation authority. Human verification and publication
remain separate decisions.

## Verification and evidence

Apply VER-IAR-022 with WO-IAR-030/034/035. Run the five affected modules and the
full suite on stable inputs. Preserve the observed failed run and actual command
results under the declared evidence prefix. Confirm both explicit legacy tests
and a real installed-wheel minimal scenario. Record Windows/Linux and native
host limitations separately; a unit patch is not installed or native evidence.

Include this work and VER-IAR-022 in VREC-IAR-020 at the same exact candidate as
the integrated resource and plugin changes. Check that the record ID remains
available before evaluator capture; do not edit a VREC template by hand.

## Stop and completion

Stop affected work for changed scope, required check failure or missing authority.
Report the exact adapted cases, candidate, test results, evidence, remaining
limitations and the released evaluator's current typed next step.
