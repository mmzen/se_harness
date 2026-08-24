+++
id = "WO-REB-021"
type = "work_order"
title = "Implement the declared environment entry-point safety rule"
status = "in_progress"
owners = ["engineering-owner", "repository-owner", "quality-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[assurance]
commit_bound_verification = "required"
rationale = "This work order changes the trust rule that decides whether a released evaluator, a predecessor evaluator, or a candidate runtime may execute at all. Every later engineering, assurance, and release decision that relies on a runtime-identity observation relies on this rule being correct, and the change both relaxes one path form and adds refusals at boundaries that currently have none, so a defect could admit a relocated or candidate-backed interpreter. Verification must bind the exact implementation commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/released-evaluator-boundary/README.md",
  "docs/engineering/released-evaluator-boundary/architecture/ARCH-REB-010.md",
  "docs/engineering/released-evaluator-boundary/architecture/adr/ADR-REB-010.md",
  "docs/engineering/released-evaluator-boundary/evidence/WO-REB-021-entry-point-safety.md",
  "docs/engineering/released-evaluator-boundary/requirements/REQ-REB-023.md",
  "docs/engineering/released-evaluator-boundary/requirements/REQ-REB-024.md",
  "docs/engineering/released-evaluator-boundary/requirements/REQ-REB-025.md",
  "docs/engineering/released-evaluator-boundary/requirements/REQ-REB-026.md",
  "docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-011.md",
  "docs/engineering/released-evaluator-boundary/verification/VER-REB-010.md",
  "docs/engineering/released-evaluator-boundary/work-orders/WO-REB-021.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/evaluator-recovery-runbook.md",
  "docs/notes/harnessctl-reference.md",
  "pyproject.toml",
  "repository_tools/interpreter_safety.py",
  "repository_tools/predecessor_assessment.py",
  "repository_tools/predecessor_preparation.py",
  "repository_tools/predecessor_publication.py",
  "repository_tools/release_bootstrap.py",
  "scripts/check_portable_release_surface.py",
  "se_harness/evaluator_evidence.py",
  "se_harness/governance_migration.py",
  "se_harness/governance_migration_contract.json",
  "se_harness/interpreter_safety.json",
  "se_harness/interpreter_safety.py",
  "se_harness/release_qualification.py",
  "se_harness/runtime_identity.py",
  "tests/test_context_routing_retirement.py",
  "tests/test_dashboard_publication.py",
  "tests/test_evaluator_identity.py",
  "tests/test_governance_migration.py",
  "tests/test_harnessctl.py",
  "tests/test_hash_bound_integrity.py",
  "tests/test_instruction_architecture.py",
  "tests/test_interpreter_safety.py",
  "tests/test_mutation_guard.py",
  "tests/test_predecessor_assessment_contract.py",
  "tests/test_predecessor_preparation.py",
  "tests/test_predecessor_publication.py",
  "tests/test_release_bootstrap.py",
  "tests/test_release_build.py",
  "tests/test_release_orchestration.py",
  "tests/test_release_qualification.py",
]

[relations]
implements = ["REQ-REB-023", "REQ-REB-024", "REQ-REB-025", "REQ-REB-026"]
specifications = ["SPEC-REB-011"]
architecture = ["ARCH-REB-010", "ADR-REB-010"]
verification = ["VER-REB-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T13:01:45Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-24T13:04:22Z"
decided_by = "engineering-owner"
reason = "Explicit start of the bounded implementation for issue #106 / RC-060-06. Authorizes only the local implementation and qualification described in the work order."
+++

# Work Order: Implement the declared environment entry-point safety rule

## Lifecycle and authorization

This draft packet proposes the bounded implementation for GitHub issue #106 / RCA `RC-060-06`. It grants no execution or lifecycle authority while draft.

If the accountable owners approve the eight definition artifacts and this work order, a separate explicit start may authorize only the local implementation and qualification described here. Approval and start do not authorize a push, a pull request, a hosted dispatch, credential use, VREC or RLS preparation or transition, a release, a tag, a publication, a deployment, a maintenance mutation, an external-policy change, or a root-evaluator adoption.

The issue's own boundary applies unchanged: recording remediation work from the RCA authorizes none of those actions.

## Scope amendment, 2026-08-24

Amended on 2026-08-24 by the engineering owner, during implementation and on an
explicit request. `se_harness/governance_migration_contract.json` is added to
`[execution_scope]` for one purpose only: re-measuring the six identical
`implementation_sha256` values that pin the SHA-256 of
`se_harness/governance_migration.py`.

The reason is that this work order authorizes changing that module, and
`_implementation_identity` compares the module's own bytes against the declared
pin, so an authorized edit raises `MIG215` until the pin is re-measured. The
coupling is not new: every earlier commit that changed the module — `35f7afd`,
`f606c9a`, and `ca275ac` — changed the same six lines in the same file. The
omission from the original allowlist was a scope oversight, and the constraint
"re-measure every digest that could move … the governance-migration class"
already required this measurement without listing the file that holds it.

The amendment authorizes those six digest values and nothing else. The adapter
identifiers, `implementation_path`, the stage lists, the views, the contract
schema, and the migration stage policy are untouched, and the declared pin
remains a pin rather than becoming a computed value.

## Second scope amendment, 2026-08-24

Amended on 2026-08-24 by the engineering owner, during implementation and on an
explicit request, after the stop-and-escalate condition "Another file … is
required" fired. Two test files outside the original allowlist are added:
`tests/test_release_orchestration.py` and
`tests/test_context_routing_retirement.py`. Both changes were measured before
the decision, by applying and reverting them: four added lines in total and
none removed.

`tests/test_release_orchestration.py` builds a synthetic portable wheel from
`REQUIRED_MIGRATION_MEMBERS | REQUIRED_QUALIFICATION_MEMBERS`. This work order
authorizes listing the declaration in `scripts/check_portable_release_surface.py`,
so the checker now requires `se_harness/interpreter_safety.json` and
`se_harness/interpreter_safety.py`, and the fixture's own wheel no longer
satisfies the check it exercises. One line joining
`REQUIRED_INTERPRETER_SAFETY_MEMBERS` into each of the two fixtures corrects it.
The consequence was implied by an in-scope item and only the file holding the
fixture was omitted.

`tests/test_context_routing_retirement.py` pins an exhaustive inventory of the
files permitted to name this repository's owner-owned engineering context
document, each with the reason it is not a live obligation. `ADR-REB-010` and
`REQ-REB-023`, both approved under this packet, each name that document as an
affected operator path in the `RC-060-06` narrative. Two inventory entries with
reasons record them. The alternative — deleting the references from the two
approved artifacts — was put to the owner and rejected, because the documented
POSIX bootstrap sequence living in that document is precisely why the defect
made the governing path unusable rather than merely inconvenient. This work
order deliberately does not spell the retired path itself, so the inventory
needs exactly the two authorized entries and no third.

The amendment authorizes those four lines and nothing else. No assertion is
weakened: both inventories remain exhaustive equality checks, so a further
undeclared member or mention still fails by name.

## Specification amendment, 2026-08-24

Amended on 2026-08-24 by the engineering owner, during implementation and on an
explicit request. `SPEC-REB-011` rule 4 is amended to name the reparse-tag
`stat` route as the junction predicate where `pathlib.Path.is_junction` is
absent, refusing with `EPS011` only where neither route exists.

The reason is that `pathlib.Path.is_junction` exists only from Python 3.12,
`pyproject.toml` declares `requires-python = ">=3.11"`, and every workflow lane
pins `python-version: "3.11"`. Read literally, the approved rule would have
refused every interpreter at every boundary on every supported lane. The
amendment preserves rule 4's intent exactly — junction detection stays a
predicate distinct from symbolic-link detection, and its absence still refuses
rather than passes — and it adds no acceptance: the `stat` route only classifies
a path as a junction, so it can only produce `EPS002`.

The amendment changes rule 4's text and nothing else. No case is added,
removed, renumbered, or reordered, no acceptance becomes a refusal or the
reverse, and no waiver is introduced.

## Objective

Replace six independent, mutually inconsistent decisions about interpreter-path safety with one declared rule read by one loader per runtime, so that a real POSIX virtual environment is accepted as an evaluator entry point while every unsafe path form — including a Windows junction parent — is refused at every identity boundary, and so that both the lexical entry path and the resolved interpreter are recorded and independently verified.

## In scope

- Add `se_harness/interpreter_safety.json` declaring the ordered case list, the boundary registry, and the conformance corpus under schema identifier `se-harness-interpreter-safety-v1`.
- Add `se_harness/interpreter_safety.py` and `repository_tools/interpreter_safety.py` as the two stdlib-only conforming loaders, neither importing the other runtime.
- Correct `repository_tools/release_bootstrap.py`: validate the released-evaluator interpreter through the rule instead of `_ordinary_external_file`, derive the evaluator root from the accepted lexical entry point rather than from the resolved target, normalize the interpreter origin lexically, and compare `python_executable` lexically on both sides.
- Close the junction gap in `se_harness/governance_migration.py` by replacing its `is_symlink`-only parent check with the rule, retaining `MIG205` and reusing its existing resolved-byte read as the rule's digest.
- Add the missing link, junction, final-component, and resolved-target-in-checkout refusals to `se_harness/release_qualification.py` external-evaluator location and to `se_harness/runtime_identity.py`, retaining `RID004` and `RID006`.
- Re-point `repository_tools/predecessor_preparation.py` and `repository_tools/predecessor_assessment.py` at the declared rule without changing what they decide; keep `repository_tools/predecessor_publication.py` delegating through preparation.
- Add `python_entry_is_link`, `python_binary_position`, and `python_binary_sha256` to `RuntimeIdentity` additively, keeping the `se-harness-runtime-identity-v3` identifier, and verify each added fact at every boundary that supplies an expected environment.
- Ship the declaration as package data in `pyproject.toml` and list it in `scripts/check_portable_release_surface.py`.
- Add the boundary-registry, cross-runtime corpus, bidirectional declaration, import-barrier, and prohibited-pattern conformance checks.
- Add the focused adversarial and integration tests in `VER-REB-010` and update the adjacent existing tests those changes touch.
- Update the developer, `harnessctl` reference, and evaluator-recovery notes to describe the accepted POSIX venv entry point and the declared rule.
- Record the retained evidence required by `VER-REB-010`.

## Out of scope

- Changing the canonical `se-harness-evaluator-evidence-v1` document, its `origins` or `environment` field sets, or any existing bound `*-evaluator.json` sidecar.
- Introducing a `se-harness-runtime-identity-v4` identifier or otherwise changing the runtime-identity schema string.
- Editing `.engineering-harness.lock`, `.engineering-harness.toml`, root `ENGINEERING_HARNESS.md`, root `.github/workflows/engineering-harness.yml`, root managed docs, root managed scripts, or `docs/engineering/templates/`.
- Editing `templates/repository/standard/`, `.github/scripts/publish_dashboard.py`, or any workflow file.
- Adding the declaration to `se_harness/hash_bound_classes.json` or changing any hash-bound class.
- Changing lifecycle policy, the release-qualification result schema, the compatibility-view contract, the governance-migration stage policy, or the release-record schema.
- Changing product version, building promotable distributions, preparing or transitioning VREC or RLS records, releasing, tagging, publishing, deploying, or adopting a root evaluator.
- Rewriting historical artifacts, evidence, commits, refs, release records, verification records, tags, distributions, RCA facts, or hosted results.
- Adding a runtime dependency, network access, a credential path, a per-boundary waiver, a diagnostic allowlist, or an emergency bypass.
- Resolving any other RCA root cause, including the declared-hash-mode work tracked by `WO-HBI-002`.

## Disclosed scope overlap

`WO-HBI-002` is open on pull request #130 and is still `draft`, so it holds no authority. Its own execution scope includes `repository_tools/release_bootstrap.py` and `tests/test_release_bootstrap.py`, which this work order also lists. This packet was branched from `main` rather than stacked on that branch, so the two changes will conflict in those two files if both proceed independently.

Sequencing is an owner decision at approval, not an implementation choice. The engineering owner decided at approval that `WO-HBI-002` lands first. This work order therefore rebases onto it once it merges and re-measures every affected figure — the base-commit test baseline, the changed-path manifest, and any digest its own change could move — rather than carrying figures derived from the pre-merge base. The two changes shall not be combined into one diff.

Implementation may proceed on a branch based on `main` before `WO-HBI-002` merges. The rebase and the re-measurement are then required before this work order reaches `implemented`, and the evidence shall record both the pre-rebase and post-rebase base commits.

## Authorized decision envelope

After approval and explicit start, implementation may choose the loader module and function names, the internal result type, refusal message wording beyond the required case identifier and subject, the digest streaming block size, test-module decomposition, fixture construction helpers, and how the corpus expresses platform constructability.

It may not add, remove, renumber, or reorder a declared case; turn an acceptance into a refusal or the reverse; add a per-boundary waiver; change a recorded fact's name or value domain; change the runtime-identity or evaluator-evidence schemas; make `repository_tools` import `se_harness` or the reverse; leave a boundary unregistered; or touch an unlisted path. If a required production dependency lies outside the execution scope, stop and request a reviewed amendment.

## Constraints

- Python 3.11+ standard library only. `repository_tools` continues to import only the standard library and its own package.
- Treat every supplied path as untrusted, including paths arriving through a lock, a release record, a bootstrap contract, or a view manifest.
- Refuse before spawning any interpreter and before validating any target.
- Junction detection is a predicate distinct from symbolic-link detection, and its absence refuses rather than passes.
- The terminal interpreter link is the only widened path form. Every refusal present at the base commit remains present.
- Retained output contains no absolute path for the resolved target, no unrelated environment content, and no credential material.
- The declaration is data: no code, no platform conditional expressed as code, no waiver list.
- Preserve `RID004`, `RID006`, and `MIG205`.
- Re-measure every digest that could move — the governance-migration class, package data, and the evaluator-evidence sidecars — rather than assuming it did not.
- The execution scope is a maximum allowlist. Unnecessary files remain unchanged and the evidence records the actual changed subset.

## Expected change surface

- One new declaration and two new loader modules.
- Six registered identity boundaries plus one delegating boundary, of which two must change position without changing behavior.
- One additive change to the runtime-identity observation and its independent verification at each consuming boundary.
- Packaging metadata and the repository-owned portable-surface check.
- One new focused test module plus the adjacent existing bootstrap, preparation, assessment, publication, qualification, migration, identity, mutation-guard, hash-bound, instruction-architecture, dashboard, and release-build tests.
- Nine definition artifacts, the domain index, three operator or developer notes, and one retained evidence file.

## Required verification

- Execute every case, property, static check, and manual review in `VER-REB-010`.
- Prove POSIX acceptance end to end: a real `python -m venv` evaluator passes every boundary and every boundary derives the virtual environment as the root, not the system prefix.
- Prove every refusal in the adversarial corpus from every boundary, with instrumentation showing no interpreter was spawned and no target validated.
- Prove the junction parent is refused while independently asserting `is_symlink()` is false and `is_junction()` is true for that parent, and that a runtime lacking the predicate refuses.
- Prove the recorded facts match independently computed values and that a tampered link or altered binary is caught by the boundary's own comparison.
- Prove refusal preservation and acceptance monotonicity against an independently captured base-commit baseline.
- Prove the boundary registry matches an independent inventory, the two loaders agree on every declared case on Windows and Linux, and both bidirectional declaration checks fail as specified when violated.
- Prove the `repository_tools` import barrier and the absence of any waiver mechanism in the declaration.
- Prove the evaluator-evidence sidecars, their recorded digests, the runtime-identity schema identifier, root managed bytes, lock and configuration, history, refs, tags, and public distributions are unchanged.
- Run the focused tests, the complete supported suite, graph validation, distribution validation, the portable-surface check, and the phase-appropriate preflight. Compare full-suite failure names against an independently captured baseline in a clean worktree at the base commit; the delta shall be exactly the tests added here.
- Run the released-evaluator qualification from a released-version environment outside the checkout, not the in-tree candidate CLI.

## Evidence to record

Retain, under `docs/engineering/released-evaluator-boundary/evidence/WO-REB-021-entry-point-safety.md`: the approved packet and preflight; the base commit and its independently captured test baseline with failure names; the actual changed-path manifest; the declared case list and its bidirectional comparison with the test-owned corpus; the boundary registry and the independent inventory it was checked against; the per-boundary before-and-after outcome table covering all six boundaries; the adversarial corpus results for Windows and Linux with explicit skip reasons; subprocess and import instrumentation traces; the recorded-facts matrix with independently computed digests; the evaluator-evidence sidecar bytes and digests before and after; the re-measured governance-migration and package-data digests; the root managed, lock, history, ref, tag, and distribution non-change proofs; focused and full suite output per platform; the disclosed `WO-HBI-002` overlap resolution as decided by the owner; and the complete actions-not-performed statement.

## Stop and escalate conditions

- A declared case cannot be expressed as data, or a boundary cannot reach the rule without breaking the import barrier.
- A boundary requires a seventh variant, a waiver, a relaxed refusal, or a platform-name conditional in policy.
- Correcting a boundary would change the observable behavior of `predecessor_preparation` or `predecessor_assessment`, or would lose a refusal present at the base commit.
- The added identity facts cannot be carried without changing the evaluator-evidence document, a closed field set, a bound sidecar digest, or the runtime-identity schema identifier.
- A digest bound elsewhere in the repository moves and cannot be re-measured and recorded within this scope.
- `REQ-REB-024` cannot be fully proven because neither available platform can construct a required path form.
- The `WO-HBI-002` overlap cannot be sequenced without combining two work orders into one diff.
- Another file, lifecycle policy change, historical mutation, released-byte change, or external action is required.

Retain the exact failure and request a bounded amendment. Do not absorb another RCA issue and do not create a bypass.

## Completion report format

Report the declared case list and the boundary registry; the per-boundary before-and-after outcome table; the actual changed paths; POSIX acceptance and adversarial refusal results per platform with skip reasons; the recorded-facts matrix; refusal-preservation and acceptance-monotonicity results; frozen-document, bound-digest, root, history, and external non-change proofs; import-barrier and waiver-absence results; focused, full-suite, graph, distribution, portable-surface, and preflight results with the baseline comparison; the evidence path; the `WO-HBI-002` sequencing as decided; residual risks; actions not performed; and one next accountable decision.
