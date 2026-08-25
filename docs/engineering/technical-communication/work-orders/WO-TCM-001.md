+++
id = "WO-TCM-001"
type = "work_order"
title = "Implement managed technical communication and the operator-brief skill"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[assurance]
commit_bound_verification = "required"
rationale = "The work changes managed policy distribution, the managed router, preflight inputs, strict portable-skill contracts, installed package contents, and agent-visible behavior. Future engineering and release decisions depend on exact candidate behavior and therefore require commit-bound assurance."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "templates/repository/standard/ENGINEERING_HARNESS.md.tpl",
  "templates/repository/standard/docs/engineering/TECHNICAL_COMMUNICATION.md",
  "templates/repository/standard/.agents/skills/harness-operator-brief/",
  "se_harness/skill_contract.py",
  "se_harness/preflight.py",
  "pyproject.toml",
  "tests/test_agentic_execution.py",
  "tests/test_instruction_architecture.py",
  "tests/test_standard_repository_lifecycle.py",
  "tests/test_release_build.py",
  "tests/test_public_onboarding.py",
  "tests/fixtures/technical_communication/",
  "docs/notes/technical-communication.md",
  "docs/notes/README.md",
  "docs/engineering/technical-communication/evidence/",
]

[relations]
implements = ["REQ-TCM-001", "REQ-TCM-002", "REQ-TCM-003", "REQ-TCM-004"]
specifications = ["SPEC-TCM-001"]
architecture = ["ARCH-TCM-001", "ADR-TCM-001"]
verification = ["VER-TCM-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T07:53:59Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-25T07:54:58Z"
decided_by = "engineering-owner"
+++

# Work Order: Implement managed technical communication and the operator-brief skill

## Lifecycle

This work order remains `draft`. Approval would authorize only the bounded
scope below. A separate explicit engineering-owner start decision is required
before implementation. Completion changes only this work order to `implemented`
after review evidence passes. Commit-bound verification and the assurance-owner
VREC decision remain separate.

No definition approval, lifecycle transition, implementation, Git action,
standard download, network use, package publication, release, deployment, or
other external action is authorized by this draft.

## Objective

Implement one provider-neutral managed technical-communication policy, route it
through the existing managed harness, distribute it with integrity and preflight
coverage, and add the explicit read-only `harness-operator-brief` portable skill
with deterministic protected-content checks and complete verification evidence.

## In scope

- Add the canonical managed `TECHNICAL_COMMUNICATION.md` policy with the exact
  precedence, permitted claim, no-download rule, profiles, protection classes,
  deviations, human decision points, and examples in `SPEC-TCM-001`.
- Add one concise direct route in the canonical managed harness template.
- Add the policy to required and policy preflight path sets in stable order.
- Extend the strict v2 skill parser with one closed read-only
  `harness-operator-brief` instance without changing current skill contracts.
- Add the canonical three-file portable skill core with explicit-only activation,
  complete single-agent procedure, closed contract, and deterministic
  `check_brief.py` helper.
- Add wheel data-file declarations for the policy and complete skill core. Keep
  the existing sdist recursive skill inclusion valid.
- Add unit, contract, property, sentinel, installation, upgrade, package, offline,
  compatibility, trigger, and integration tests required by `VER-TCM-001`.
- Add versioned protected-content and manual-review fixtures that contain no
  copied ASD-STE100 content or secrets.
- Add non-authoritative operator and contributor documentation that explains the
  capability, claim boundary, profile selection, exact protection, invocation,
  and limitations without duplicating managed policy.
- Retain work-order-keyed verification evidence and a complete review report.

## Out of scope

- Approving or transitioning any definition or this work order.
- Editing root managed copies, `.engineering-harness.lock`, `AGENTS.md`,
  `WORKFLOW.*`, `DECISION_RIGHTS.md`, `QUALITY_GATES.*`, or `TRACEABILITY.md`.
- Downloading, bundling, reproducing, parsing, or certifying ASD-STE100 or its
  controlled dictionary.
- Claiming ASD approval, endorsement, certification, or strict compliance.
- Adding a grammar checker, readability gate, automatic semantic-equivalence
  engine, translation system, or remote terminology service.
- Automatically rewriting existing approved, historical, or repository-wide
  artifacts for style.
- Changing lifecycle, decision-right, quality-gate, traceability, artifact, or
  execution-receipt schemas.
- Changing the current four skill cores, their contract bytes, digests,
  activation, effects, or outputs.
- Adding implicit operator-brief activation, multi-agent execution, provider
  adapters, host activation metadata, Git mutation, credentials, or external
  actions.
- Building a release, changing product version, publishing a package, or
  upgrading the self-hosting managed root.

## Authorized decision envelope

The implementation agent may decide:

- internal helper functions and data classes;
- stable diagnostic numbers inside the reserved `TCM` family;
- concise policy example wording that preserves the approved semantics;
- fixture file names and organization inside the authorized fixture directory;
- test method names and factoring within the declared test files; and
- documentation layout and cross-links inside the two declared note paths.

The implementation agent may not change:

- the canonical or installed policy paths;
- the permitted public claim or no-download boundary;
- policy precedence, profile names, protected classes, or fail-closed behavior;
- skill name, version, explicit-only activation, read-only mutation class,
  single-agent fallback, closed inputs, outputs, source limits, or zero-change
  result;
- accountable roles, lifecycle meaning, normative force, or existing skill
  behavior; or
- any path outside `[execution_scope].paths`.

## Constraints

- Use the candidate source only for implementation and tests. Use the target's
  exact external released evaluator for governed identity, integrity, graph,
  focus, and preflight results.
- Do not edit the self-hosting root managed policy or lock. Test rendered
  installation in isolated targets.
- Keep one canonical policy and one canonical portable skill core. Installed
  copies are derived managed content.
- Preserve every current skill core byte and manifest digest.
- Keep the helper deterministic, standard-library-only, bounded, offline, and
  free of substantive language scoring or hidden-reasoning inspection.
- Treat source bodies, span declarations, repository paths, lock data, package
  contents, and model output as untrusted input.
- Apply the communication principles to new implementation documentation, but
  do not use them to paraphrase normative requirements or historical evidence.
- A passing tool is evidence only. It does not approve the policy, verify the
  candidate, or authorize integration or release.

## Expected change surface

- Standard managed policy template and managed router template.
- Preflight required/policy path catalogs.
- Strict skill-contract profile catalog and parser checks.
- One new standard portable skill directory.
- Wheel data-file declarations.
- Agentic-execution, instruction-architecture, standard lifecycle, release-build,
  public documentation, and focused technical-communication tests and fixtures.
- Non-authoritative notes and work-order evidence.

No root managed copy, lock, workflow machine contract, quality-gate machine
contract, formal-artifact validator, release script, CI workflow, provider
adapter, or current skill core is expected to change.

## Required verification

Execute the complete `VER-TCM-001` contract and the repository-required checks.
At minimum:

1. Run released-evaluator identity, doctor, formal graph validation, focused
   review preflight, and work-order handoff check.
2. Run focused skill-contract, protected-content, trigger, effect-sentinel,
   installation, upgrade, preflight, package, offline, and documentation tests.
3. Run the complete Python standard-library test suite.
4. Run release-distribution validation without building or publishing a
   promotable release.
5. Inspect wheel and sdist candidate payload behavior only when existing test
   fixtures create non-promotable ephemeral artifacts under authorized paths.
6. Compare current skill files and manifest digests with the recorded baseline.
7. Inspect exact changed paths and prove they are complete and in scope.
8. Complete the independent manual meaning and operator-comprehension assessment.
9. Run `git diff --check` and inspect the final diff for policy duplication,
   prohibited claims, network paths, hidden authority, and root managed changes.

All deterministic tests must pass. Exact protected content has zero byte changes.
Manual review has zero critical meaning changes and 100% correct decision/action
identification in the declared operator corpus. The candidate contains no
prohibited claim, standard payload, or network retrieval path.

## Evidence to record

Retain in `docs/engineering/technical-communication/evidence/`:

- evaluator version, identity, lock, formal snapshot, and commands;
- start and review preflight manifests and results;
- complete test commands, exit status, summaries, and relevant bounded outputs;
- canonical/installed policy and skill manifests plus package inventories;
- existing skill byte and digest baselines and candidate comparisons;
- protected-content corpus manifest, source/output hashes, and negative results;
- effect-sentinel and offline execution evidence;
- independent manual review inputs, judgments, disagreements, and dispositions;
- exact changed-path inventory and scope assessment;
- confirmation that root managed copies, lock, lifecycle, Git, network, and
  external state were not changed by the skill; and
- residual uncertainty and follow-up recommendations that do not expand scope.

Do not retain downloaded standard content, credentials, secrets, hidden
reasoning, environment dumps, or unbounded source bodies.

## Stop and escalate conditions

Stop before the associated effect when:

- a required definition or ADR is not approved;
- the work order is not approved and explicitly started;
- released-evaluator identity, managed integrity, graph validation, or preflight
  is not assessable or fails;
- implementation needs a path outside the declared scope;
- exact current skill bytes or digests would change;
- the policy must copy or retrieve external standard content to be usable;
- a protected-content requirement cannot be implemented without changing
  normative meaning or existing machine contracts;
- an open-ended skill registry, implicit activation, runtime adapter, network,
  credential, Git mutation, or external action appears necessary;
- a customized managed target would be overwritten or an upgrade would be
  partial;
- the manual review finds a critical meaning change or unresolved disagreement;
  or
- any required test fails or evidence is incomplete.

Report the exact failed requirement, rule, path, or gate and request one bounded
accountable decision. Do not widen scope or accept risk by inference.

## Completion report format

The completion report must include:

1. selected work order and unchanged approved scope;
2. exact changed paths grouped by policy, skill, package, tests, notes, and evidence;
3. implemented behavior for each of the four requirements;
4. evaluator identity, managed integrity, graph, preflight, and handoff results;
5. test and package results with exact commands and exit status;
6. protected-content and manual review results;
7. existing-skill compatibility and root-managed non-change evidence;
8. known limitations, material deviations, and residual uncertainty;
9. confirmation of no lifecycle completion decision, VREC decision, Git action,
   publication, release, network retrieval, or external action; and
10. the one current canonical next decision from the released evaluator.
