+++
id = "WO-ADS-001"
type = "work_order"
title = "Implement enforced failure rendering, shared next-step resolution, the operating card, trap diagnostics, the restitution digest, and router scope"
status = "draft"
owners = ["engineering-owner"]
created = "2026-08-25"
updated = "2026-08-25"
[assurance]
commit_bound_verification = "required"
rationale = "The work changes the workflow machine contract, result rendering, preflight manifests, diagnostics, the managed router template, the managed CI workflow, and installed package contents. Future engineering, assurance, and release decisions depend on exact candidate behaviour and therefore require commit-bound assurance."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "templates/repository/standard/ENGINEERING_HARNESS.md.tpl",
  "templates/repository/standard/docs/engineering/WORKFLOW.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "templates/repository/standard/docs/engineering/OPERATING_CARD.md",
  "templates/repository/standard/.github/PULL_REQUEST_TEMPLATE.md.seed",
  "templates/repository/standard/.github/workflows/engineering-harness.yml",
  "templates/repository/standard/scripts/select_harness_work_order.py",
  "se_harness/workflow_contract.json",
  "se_harness/workflow_contract.py",
  "se_harness/workflow.py",
  "se_harness/workflow_procedures.py",
  "se_harness/workflow_result.py",
  "se_harness/workflow_compliance.py",
  "se_harness/preflight.py",
  "se_harness/github_ci.py",
  "se_harness/installer.py",
  "se_harness/cli.py",
  "pyproject.toml",
  "tests/test_workflow_execution.py",
  "tests/test_preflight.py",
  "tests/test_github_ci.py",
  "tests/test_instruction_architecture.py",
  "tests/test_context_routing_retirement.py",
  "tests/fixtures/agent_directive_surface/",
  "AGENTS.md",
  "docs/engineering/README.md",
  "docs/engineering/REPOSITORY_CONTEXT.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/README.md",
  "README.md",
  "docs/engineering/agent-directive-surface/evidence/",
]

[relations]
implements = ["REQ-ADS-001", "REQ-ADS-002", "REQ-ADS-003", "REQ-ADS-004", "REQ-ADS-005", "REQ-ADS-006"]
specifications = ["SPEC-ADS-001"]
architecture = ["ARCH-ADS-001", "ADR-ADS-001"]
verification = ["VER-ADS-001"]
+++

# Work Order: Implement enforced failure rendering, shared next-step resolution, the operating card, trap diagnostics, the restitution digest, and router scope

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification, the assurance-owner decision, integration, and release are
separate decisions by the roles that own them. No definition approval,
transition, Git action, or external action is authorized by this draft.

## Objective

Implement `SPEC-ADS-001` in the candidate source and standard templates so that
the six requirements are enforced or rendered by the evaluator, and fold the
owner-region cleanup that a test inventory binds into the same bounded change.

## In scope

- Extend `WORKFLOW.json` (template and packaged copy, byte-identical) with a
  `corrective` form per command-step predicate; add loader diagnostic
  `WEX-ADS-001`; add a conformance test forbidding a corrective equal to the
  evaluated command.
- Introduce one shared step resolver used by `focus` and `check`; make
  `focus` default to `--result-schema 2`; emit `WEX-ADS-002` on schema 1.
- Close the preflight reading manifest per `ADS-RDM-001`; render
  `docs/engineering/OPERATING_CARD.md` as a managed file from the contracts;
  add its conformance test; update the router template's reading instruction.
- Add `W-ADS-001` (CR in trailer) to the CI selector and to `check
  --pull-request-body`; add `W-ADS-002` (orphaned ready VREC) to review
  preflight and handoff check.
- Add `result_sha256` to `se-harness-workflow-result-v2`; add the optional
  `Harness-Restitution:` line to the pull-request template seed; add
  recomputation to the managed CI workflow template.
- Add the `Scope of these obligations` paragraph to the router template.
- Owner-region cleanup bound by `tests/test_context_routing_retirement.py`:
  fold the release-build, release-binding, and last-mile sequences into
  `AGENTS.md` under a `Release sequences` heading; add the ungoverned-paths
  declaration; add the line "`focus` without `--result-schema 2` is not
  restitution"; remove the withdrawn repository-context document and its
  index line; update the permitted-mentions inventory and the developer note.
- Version-qualify README claims that describe unreleased installation content.
- Add tests, fixtures, notes, and work-order-keyed evidence required by
  `VER-ADS-001`.

## Out of scope

- Approving or transitioning any definition or this work order.
- Editing root managed copies or `.engineering-harness.lock` in this repository.
- Changing lifecycle states, decision rights, gate predicates,
  `QUALITY_GATES.json`, traceability relations, or artifact schemas.
- Changing any skill core, its contract bytes, or its digests.
- Building a release, changing the product version, publishing, or upgrading
  the self-hosting managed root.

## Authorized decision envelope

The implementation agent may decide: internal function and class names;
diagnostic numbers inside the reserved `ADS` and `WEX-ADS` families; the exact
placeholder tokens in corrective forms; fixture layout inside the declared
fixture directory; test method names within the declared test files; note
wording and cross-links inside the declared note paths.

The implementation agent may not change: the card's size bound or content
order; the schema version of the workflow result; the router paragraph wording
in `ADS-SCP-001`; the byte-identity rule between template and packaged
contract; accountable roles or lifecycle meaning; any path outside
`[execution_scope].paths`.

## Constraints

- Use candidate source for implementation and tests. Use the exact external
  released evaluator for identity, integrity, graph, focus, and preflight
  results.
- Keep root managed copies and the lock untouched; test rendered installations
  in isolated targets.
- Treat pull-request bodies, evidence paths, Git state, and contract files as
  untrusted input.
- Write files with LF line endings; assert bytes against blobs, not the
  worktree.
- A passing tool is evidence only; it approves nothing.

## Expected change surface

Workflow contract and its loader; result renderer; step resolver; preflight;
installer rendering; CI selector and managed workflow template; pull-request
template seed; router template; owner-region instruction file; tests and
fixtures; notes; README.

## Required verification

Execute `VER-ADS-001` completely and the repository-required checks:

1. Released-evaluator identity, `doctor`, graph validation, focused review
   preflight, and handoff check with the complete changed-path set asserted.
2. Focused workflow, preflight, CI, and instruction-architecture tests.
3. The complete unit-test suite on Windows and Linux with `--no-fail-fast`
   equivalents, figures labelled per platform.
4. `python scripts/validate_release_distributions.py --root .` without building
   a promotable release.
5. Byte comparison of packaged and template `WORKFLOW.json`.
6. `git diff --check`; inspection of the final diff for root managed changes.

## Evidence to record

Under `docs/engineering/agent-directive-surface/evidence/WO-ADS-001/`: command
arrays and results, per-platform test figures, the card bytes and size, the
digest round-trip transcript, reviewer classifications for Scenario 8, and the
complete changed-path set.

## Stop and escalate conditions

Stop on: a corrective form that cannot be expressed without guessing values;
a card that cannot fit 3072 bytes without dropping contract content; a
schema change that would not be additive; any path outside scope; a failing
required check that remediation would push outside scope.

## Completion report format

Return the `harnessctl check . --artifact WO-ADS-001 --checkpoint handoff`
schema-2 block verbatim, with the complete changed-path set and
`--changes-complete` asserted, and its `result_sha256`.
