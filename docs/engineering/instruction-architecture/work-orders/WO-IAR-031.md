+++
id = "WO-IAR-031"
type = "work_order"
title = "Bind workflow discovery to the selected resource layout"
status = "draft"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"

[execution_scope]
paths = [
  "se_harness/workflow_result.py",
  "se_harness/workflow_compliance.py",
  "tests/test_resources.py",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-031.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-031/",
  "docs/engineering/instruction-architecture/verification-records/VREC-IAR-018.md",
  "docs/engineering/instruction-architecture/evidence/VREC-IAR-018-evaluator.json",
  "docs/engineering/instruction-architecture/verification-records/VREC-IAR-020.md",
  "docs/engineering/instruction-architecture/evidence/VREC-IAR-020-evaluator.json",
]

[relations]
implements = ["REQ-IAR-029"]
specifications = ["SPEC-IAR-016"]
architecture = ["ARCH-IAR-012", "ADR-IAR-012"]
verification = ["VER-IAR-020"]
+++

# Bind workflow discovery to the selected resource layout

## Objective and scope correction

Pass the selected repository from the two result-building call sites in
workflow_compliance.py to build_result in workflow_result.py, and from there
to the resource-aware instruction discovery added under WO-IAR-028.
These two production files were omitted from WO-IAR-028's permitted paths.
The accepted behavior, architecture and verification contract remain unchanged.

The new parameter is optional for existing callers without repository context.
The selected external layout returns explicitly versioned resource references.
Keep legacy-layout results compatible. An unavailable selection reports an
instruction-discovery gap. Do not change gate predicates, lifecycle decisions,
next-action arguments or the existing result-digest algorithm. Do not put local
resource paths in portable result identity; the resource query resolves them.

## Proposed assurance

Required commit-bound verification: agents and CI rely on the returned reading
locations. Human confirmation is requested with approval; no assurance decision
is recorded by this draft.

## Execution and decision envelope

Implement the small result-wiring change after this approval, alongside the
approved resource interface. Test the actual public workflow result and its
digest under VER-IAR-020 using the shared tests/test_resources.py fixture.
Approval covers local edits, commits, checks, evidence, completion and preparation
of the named verification outputs. Human verification and external actions remain
separate. No changes to the installed 0.20.0 instructions or accepted definitions.

## Verification and evidence

Retain exact commands, runtime identities, results, failures and a reviewed diff
under evidence/WO-IAR-031/. Exercise external and legacy discovery, malformed
selection, all typed step headings, portable result identities and unchanged
lifecycle outcomes. Reuse VER-IAR-020 rather than create another verification
contract. Run released validation, start/review preflight, scope and Git-derived
handoff against the recorded implementation base. Include both this work and
WO-IAR-028 in VREC-IAR-018 at their shared exact committed candidate, then in the
already planned final integrated VREC-IAR-020 when eligible. Check ID availability
before preparation. Do not edit generated evaluator evidence by hand.

## Stop conditions and completion

Stop affected work for a changed accepted contract, an out-of-scope path,
an integrity failure or a missing decision. Report actual effects, checks,
remaining gaps and the evaluator's next typed step. This draft does not approve
implementation or rewrite WO-IAR-028's history.
