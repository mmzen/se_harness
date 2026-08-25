+++
id = "WO-AEX-008"
type = "work_order"
title = "Integrate Phase 4 execution skills and package qualification"
status = "approved"
owners = ["repository-owner", "engineering-owner", "technical-owner", "quality-owner", "assurance-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[assurance]
commit_bound_verification = "required"
rationale = "The work changes the user-facing writing-skill contracts from cooperative target writers to evaluator clients and qualifies the complete Phase 4 package surface; assurance must bind exact portable cores, host adapters, package inventory, and end-to-end stop behavior."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "MANIFEST.in",
  "README.md",
  "pyproject.toml",
  "se_harness/skill_contract.py",
  "templates/repository/standard/.agents/skills/harness-draft-change/",
  "templates/repository/standard/.agents/skills/harness-execute-work-order/",
  "templates/repository/standard/.agents/skills/harness-prepare-assurance/",
  "templates/repository/standard/.claude/skills/harness-draft-change/",
  "templates/repository/standard/.claude/skills/harness-execute-work-order/",
  "templates/repository/standard/.claude/skills/harness-prepare-assurance/",
  "tests/fixtures/agentic_execution/host_activation/",
  "tests/fixtures/agentic_execution/phase3/portable_vectors.json",
  "tests/fixtures/agentic_execution/phase4/skills/",
  "tests/test_agentic_execution.py",
  "tests/test_instruction_architecture.py",
  "tests/test_public_onboarding.py",
  "tests/test_release_build.py",
  "tests/test_standard_repository_lifecycle.py",
  "docs/engineering/agentic-execution/README.md",
  "docs/engineering/agentic-execution/evidence/WO-AEX-008-verification.md",
  "docs/notes/agentic-execution-phase4-skills.md",
  "docs/notes/agentic-execution-roadmap.md",
  "docs/notes/agentic-execution-skills-mvp.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/notes/README.md",
]

[relations]
implements = ["REQ-AEX-005", "REQ-AEX-008", "REQ-AEX-009", "REQ-AEX-012"]
specifications = ["SPEC-AEX-001", "SPEC-AEX-002", "SPEC-AEX-004", "SPEC-AEX-005", "SPEC-AEX-008"]
architecture = ["ARCH-AEX-001", "ADR-AEX-001", "ADR-AEX-002", "ADR-AEX-004", "ADR-AEX-005", "ARCH-AEX-002", "ADR-AEX-006", "ADR-AEX-007"]
verification = ["VER-AEX-001", "VER-AEX-002", "VER-AEX-003", "VER-AEX-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T09:08:48Z"
decided_by = "engineering-owner"
+++

# Work Order: Integrate Phase 4 execution skills and package qualification

## Lifecycle and readiness

This work order is `draft` and authorizes no change, build, installation, host
execution, release, or target pilot. `WO-AEX-005`, `WO-AEX-006`, and
`WO-AEX-007` must first be implemented and independently commit-bound verified.
All governing artifacts and this work order require separate approval and a
separate start decision through the existing released evaluator.

The candidate package remains non-promotable. This work order does not release
or install the successor evaluator and cannot use Phase 4 to govern itself.

## Objective

Version and integrate the three writing skills as non-authoritative clients of
the verified Phase 4 evaluator interfaces; preserve their user outcomes while
prohibiting direct governed-target writes; maintain Codex and Claude activation
parity; package every required Phase 4 core, contract, template, and adapter;
and qualify the complete candidate through the assurance stop.

## In scope

- Give `harness-draft-change`, `harness-execute-work-order`, and
  `harness-prepare-assurance` explicit new major portable contract versions
  because their write/effect boundary changes materially.
- Preserve explicit-only activation, canonical `.agents` ownership, thin
  `.claude` adapters, same-name binding, and provider non-authority.
- Make execute-work-order require an approved started work order, valid Phase 4
  delegation, exact released evaluator capability, isolated session workspace,
  evaluator-built bundles, broker effects, receipt continuity, and delegated
  completion proof. It must prohibit direct target writes.
- Make prepare-assurance use delegated VREC preparation and stop for the
  independent assurance decision or separately authorized required Git commit.
- Keep draft-change limited to draft artifacts and planning notes under its
  existing decision boundary; when Phase 4 governed effects are selected, route
  its writes through the evaluator session/broker rather than the target.
- Preserve exact `harness-orient` v1 core bytes, contract, manifest, vectors,
  read-only effect class, and host behavior.
- Refresh writing-core manifests, portable vectors, Codex policy bindings, and
  thin Claude descriptions without copying the Phase 4 workflow into adapters.
- Add package inventory for all new Python modules, JSON contracts, candidate
  managed templates, skills, adapters, and tests needed by a successor release.
- Test source, wheel, fresh isolated install, fresh/adopted/upgraded repository,
  managed lock, customized conflict, rollback, root/nested Codex and Claude
  discovery, explicit activation, direct-write denial, single-agent execution,
  assurance stop, and command/skill parity.
- Update bounded public, operator, installation, skill, roadmap, domain, and
  commit-bound evidence documentation.

## Out of scope

- Changing `harness-orient` v1 or adding another skill.
- Copying evaluator authority, workflow rules, bundle logic, mutation logic, or
  canonical procedures into a provider adapter or skill prose.
- Implicit writing invocation, global/user-wide skill installation, plugins,
  marketplaces, provider accounts, or organization policy.
- Editing hash-locked root managed files, root installed skills/adapters, root
  lock, current released evaluator, or real consumer repository.
- Adding provider tool/model permissions, hooks, subagents, child delegation,
  parallelism, Git mutation, credentials, network access, release preparation,
  release decision, delivery, publication, deployment, or external action.
- Selecting a successor version, creating a release record, building a
  promotable distribution, publishing, installing, piloting, or self-hosting.

## Authorized decision envelope

After separate approval and start, the implementer may choose concise provider-
facing descriptions, internal skill-step wording that preserves exact machine
preconditions, private fixture names, and normalized host transcript formatting.

The implementer may not change a skill name, outcome, activation class,
canonical/adapter mapping, authority boundary, evaluator operation, target-
write prohibition, lifecycle stop, evidence obligation, package destination,
host support claim, orientation identity, public version, or declared path.
Escalate any such need.

## Constraints

- Preserve Python 3.11+ and standard-library-only package behavior.
- Treat the exact verified dependency commits and schemas from the three prior
  work orders as fixed inputs; do not duplicate them in skill code.
- Keep every writing skill explicit-only in portable contract and both hosts.
- Keep `.agents/skills/<name>` as the only complete core and `.claude` as thin
  discovery/activation/loading adapters.
- Provider sandbox permissions are defense in depth; skills must still require
  evaluator admission and cannot present host permission as authority.
- Preserve installer ownership, atomic upgrade, lock, customization, package,
  and candidate-vs-released boundaries.
- Preserve unrelated user changes and stop on an undeclared changed path.

## Expected change surface

Only the three writing canonical cores and their thin Claude adapters change.
`skill_contract.py` versions and validates their new evaluator-client contract.
Package metadata and declared tests prove complete distribution and installation.
The orientation core is read-only evidence input and must remain byte-identical.

If implementation requires an observer, broker, workflow, CLI, mutation guard,
installer, root managed file, orientation-core, new skill, host configuration,
provider permission, or undeclared path change, stop and revise scope or the
applicable dependency work order.

## Required verification

- Execute all applicable `VER-AEX-001` through `VER-AEX-004` methods.
- Prove exact orientation v1 source, helper, contract, manifest, vectors,
  installed bytes, discovery, invocation, and read-only behavior are unchanged.
- Prove each writing core's new major identity, manifest, portable vector,
  explicit-only policy, exact evaluator operations, direct-write prohibition,
  input/result schemas, receipt behavior, stops, and single-agent fallback.
- Prove Claude adapters remain thin, same-named, explicit-only for writing, free
  of workflow copies and permissions, and load the exact updated canonical core.
- Exercise fresh root and nested Codex/Claude sessions: listing, explicit
  invocation, implicit nonactivation, unavailable-old-evaluator stop, invalid
  delegation stop, session conflict, direct-write attempt, valid sequential
  bundle execution, completion proof, VREC preparation, and assurance stop.
- Prove skill and command-driven operations produce equivalent legal outcomes
  and that provider permission or model output cannot alter admission.
- Prove source/wheel inventory, fresh wheel install, standard init/adopt/replay/
  upgrade, managed lock, customization conflict, interrupted install, and no
  duplicated authoritative source.
- Run the complete suite, distribution and release-distribution validators,
  non-promotable candidate acceptance, exact 0.6.0 doctor/formal validation,
  CLI help, phase preflight, `git diff --check`, managed root integrity, and
  exact changed-path comparison.

## Evidence to record

Retain exact dependency and candidate commits; candidate package and external
0.6.0 evaluator identities; old/new skill contracts, versions, manifests, and
vectors; exact orientation comparison; Codex/Claude versions and root/nested
listings; explicit/implicit activation; canonical load paths; unavailable,
invalid-delegation, direct-write, successful execution, completion, VREC, and
assurance-stop transcripts; source/wheel/install/lock inventories; init/adopt/
replay/upgrade/conflict/rollback results; command parity; before/after repository
and Git manifests; tests/gates; changed paths; manual assessments; deviations;
and residual uncertainty at
`docs/engineering/agentic-execution/evidence/WO-AEX-008-verification.md`.

## Stop and escalate conditions

Stop while `draft`, before dependency verification, or without a start decision.
After start, stop before another path, skill, operation, provider permission,
root managed file, Git action, version selection, release, installation, target
pilot, credential, network call, or external action.

Stop if a skill can write the governed target directly, if host adapters need a
workflow copy, if explicit-only behavior fails, if orientation changes, if
package installation is incomplete or non-atomic, if current command behavior
regresses, or if a required verification failure cannot be corrected within
scope.

## Completion report format

Report `Outcome`, `Done`, `Not done`, conditional `Blocked by`, `Current
lifecycle state`, `Decision required`, `Next`, `Command or response`, and
conditional `Alternatives`. Name `WO-AEX-008`, all dependency/evaluator
identities, exact changed paths, old/new skill identities, orientation proof,
host and package matrices, target-write denial, assurance terminal stop,
evidence path, deviations, residual uncertainty, and intentionally unperformed
Git, release, install, pilot, network, credential, and external actions.
Recommend exactly one next authorized step: review the complete Phase 4
evidence and decide whether to draft a separately governed successor release
and disposable-pilot packet.
