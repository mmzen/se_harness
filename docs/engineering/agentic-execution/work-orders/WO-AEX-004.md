+++
id = "WO-AEX-004"
type = "work_order"
title = "Install repository-scoped Codex and Claude skill surfaces"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "technical-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[assurance]
commit_bound_verification = "required"
rationale = "The work changes packaged managed skill identities, provider activation policy, repository installation inventory, and the discovery path used by operators at governed decision boundaries."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "MANIFEST.in",
  "README.md",
  "pyproject.toml",
  "templates/repository/standard/.agents/skills/harness-draft-change/",
  "templates/repository/standard/.agents/skills/harness-execute-work-order/",
  "templates/repository/standard/.agents/skills/harness-prepare-assurance/",
  "templates/repository/standard/.claude/skills/harness-draft-change/",
  "templates/repository/standard/.claude/skills/harness-execute-work-order/",
  "templates/repository/standard/.claude/skills/harness-orient/",
  "templates/repository/standard/.claude/skills/harness-prepare-assurance/",
  "tests/fixtures/agentic_execution/host_activation/",
  "tests/fixtures/agentic_execution/phase3/portable_vectors.json",
  "tests/test_agentic_execution.py",
  "tests/test_instruction_architecture.py",
  "tests/test_public_onboarding.py",
  "tests/test_release_build.py",
  "tests/test_standard_repository_lifecycle.py",
  "docs/engineering/agentic-execution/README.md",
  "docs/engineering/agentic-execution/evidence/WO-AEX-004-verification.md",
  "docs/notes/agentic-execution-host-adapters.md",
  "docs/notes/agentic-execution-roadmap.md",
  "docs/notes/agentic-execution-skills-mvp.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/notes/README.md",
]

[relations]
implements = ["REQ-AEX-005", "REQ-AEX-008", "REQ-AEX-009"]
specifications = ["SPEC-AEX-001", "SPEC-AEX-002", "SPEC-AEX-004", "SPEC-AEX-005"]
architecture = ["ARCH-AEX-001", "ADR-AEX-001", "ADR-AEX-002", "ADR-AEX-004", "ADR-AEX-005"]
verification = ["VER-AEX-001", "VER-AEX-002", "VER-AEX-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T16:49:43Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-24T16:49:56Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-24T17:56:55Z"
decided_by = "engineering-owner"
+++

# Work Order: Install repository-scoped Codex and Claude skill surfaces

## Lifecycle and readiness

This work order is `draft`. It authorizes no implementation, package change,
installation, host execution, lifecycle transition, evidence claim, Git
operation, network access, credential use, release, or external action.

Before approval, accountable owners must approve `REQ-AEX-009`,
`SPEC-AEX-005`, `ADR-AEX-005`, `VER-AEX-003`, and this work order through the
managed lifecycle procedure. Approval still does not start implementation.
After a separate engineering-owner start decision, the exact released
evaluator must pass the current start checkpoint and preflight for
`WO-AEX-004` before any implementation path changes.

Commit-bound verification is `required` because operators and later packages
will rely on the exact installed discovery, activation, canonical-core, and
adapter bytes to select governed skills.

## Objective

Make the four existing Phase 3 skills available by default to Codex and Claude
Code in every applicable standard repository installation. Preserve one
authoritative `.agents` core per skill, add only thin Claude discovery
adapters, enforce explicit-only host activation for the three writing skills,
and prove safe installation, package completeness, and behavioral equivalence
without changing harness authority or lifecycle behavior.

## In scope

- Add the bounded Codex `agents/openai.yaml` implicit-invocation policy to the
  three writing cores and update their patch versions and retained portable
  manifest vectors.
- Preserve every byte and vector of the exact `harness-orient` v1 canonical
  core.
- Add one managed thin Claude `SKILL.md` adapter for each of the four canonical
  names. Each adapter declares only discovery, activation, canonical mapping,
  and fail-closed loading behavior admitted by `SPEC-AEX-005`.
- Extend source and wheel distribution metadata to package the three Codex
  policy files and four Claude adapters.
- Use the existing recursive standard installer and managed-lock transaction
  to install, adopt, replay, and upgrade the added files. No installer behavior
  change is expected; if code changes become necessary, stop and revise scope.
- Add verifier-owned static, installation, packaging, customization, path,
  activation, and host-smoke fixtures and tests.
- Test fresh supported Codex and Claude Code sessions from the repository root
  and a nested directory, including explicit writing invocation and implicit
  non-activation.
- Update bounded user and contributor documentation, domain indexing, and
  work-order-keyed verification evidence.

## Out of scope

- Editing managed root instructions, workflow, decision-right, quality-gate,
  traceability, artifact templates, root lock, CI workflow, or released
  evaluator files.
- Copying a canonical procedure, contract, or helper beneath `.claude` or
  creating another authoritative skill source.
- Changing a skill's Phase 3 effects, required inputs, evaluator operations,
  path source, evidence obligations, lifecycle stops, or decision boundaries.
- Adding another skill, lifecycle state, transition, workflow command,
  decision right, gate, effect API, or runtime authority source.
- Using symbolic links, junctions, hard links, reparse points, global user
  directories, system directories, organization policy, cloud sync, plugins,
  marketplaces, or provider accounts to distribute the skills.
- Granting tools, permissions, models, subagents, hooks, shell injection,
  connectors, credentials, network access, Git mutation, or external actions
  through provider metadata.
- Implementing autonomy-envelope effect admission, multi-agent delegation,
  runtime enforcement, parallelism, or an integration coordinator.
- Publishing a new package, changing the public version, building a promotable
  release distribution, or upgrading a real consumer repository. A separately
  allowed non-promotable ephemeral package may be used only for candidate
  verification after implementation starts.
- Reviewing or redesigning `AGENTS.md`, `CLAUDE.md`, general prompts, or skill
  body quality beyond the exact host-loading additions. That is separate work.

## Authorized decision envelope

After separate approval and start authorization, the implementation actor may
choose concise host-facing descriptions, deterministic adapter formatting,
private fixture names inside the declared prefix, and normalized transcript
formatting that preserve `SPEC-AEX-005` exactly.

The actor may not choose another discovery path, canonical location, adapter
schema, skill name, activation class, provider permission, mapping strategy,
installation scope, portable-core meaning, lifecycle behavior, evaluator
boundary, package destination, changed file, or public version. Any such need
requires a revised approved contract and work order.

## Constraints

- Preserve Python 3.11+ and standard-library-only package behavior.
- Keep `.agents/skills/<name>` as the single complete core and
  `.claude/skills/<name>/SKILL.md` as a non-authoritative adapter.
- Keep writing skills explicit-only in the portable contract and both host
  policies. Keep orientation read-only and matchable.
- Increment and rebind only writing-core identities changed by the approved
  Codex metadata; preserve exact orientation identity.
- Use only regular portable UTF-8 text files and fixed repository-relative
  same-name mappings.
- Do not add tool grants, dynamic commands, remote references, arguments,
  credentials, environment data, user-home paths, or hidden reasoning to an
  adapter.
- Preserve existing installer ownership modes, conflict behavior, transaction
  rollback, lock schema, and evaluator identity boundary.
- Preserve unrelated user changes and stop on an unexpected changed path.
- Keep published 0.6.0 immutable and label all candidate package evidence
  non-promotable.

## Expected change surface

The exact authorized paths are declared in `[execution_scope]`.

The three canonical writing directories gain only Codex activation metadata
and the required patch-version identity updates. The four `.claude` directories
contain only adapter `SKILL.md` files. `MANIFEST.in` and `pyproject.toml` add
explicit distribution inventory. Existing tests change only to validate the
new package and managed installation surface; new hostile and host-smoke data
stays under the declared fixture prefix.

If implementation requires `se_harness/installer.py`,
`se_harness/skill_contract.py`, another package module, root `.claude` or
`.agents` materialization, managed policy, or an undeclared test or
documentation path, stop and revise this work order before continuing.

## Required verification

- Execute every applicable `VER-AEX-001` method for `REQ-AEX-005`, every
  applicable `VER-AEX-002` regression for the Phase 3 skills, and all
  `VER-AEX-003` methods.
- Prove exact `harness-orient` source, contract, helper, manifest digest,
  vectors, installed core, and public behavior are unchanged.
- Prove each writing core has the exact false Codex implicit-invocation policy,
  a patch-version identity update, and a matching retained manifest vector.
- Prove each Claude adapter has the exact name, activation class, adapter
  schema, and same-name canonical mapping and contains no copied procedure,
  script, contract, permission, model, hook, subagent, or dynamic command.
- Prove fresh install, adoption, no-op replay, safe upgrade, customization
  conflict, interrupted apply, source distribution, wheel, and fresh wheel
  install produce the exact declared inventory without partial writes.
- Prove fresh supported Codex and Claude Code sessions list the same four names
  at root and nested working directories.
- Prove explicit invocation of every skill reaches its canonical core and
  representative canonical procedure checks.
- Prove natural-language matches do not implicitly activate a writing skill or
  produce any repository, Git, lifecycle, helper, credential, network, or
  external effect.
- Exercise missing, malformed, renamed, mismatched, escaping, linked, case-
  colliding, permission-granting, and remote-loading adapter attacks.
- Run the complete repository test suite, distribution validation, candidate
  package acceptance, exact released-evaluator doctor and formal validation,
  `git diff --check`, and exact changed-path comparison against this work order.

## Evidence to record

Retain exact source candidate, candidate commit, non-promotable package,
external evaluator, operating system, Codex, and Claude Code identities; all
canonical manifests and versions; adapter and policy bytes and digests; source,
wheel, installed-template, and managed-lock inventories; init, adoption,
replay, upgrade, conflict, rollback, and path-attack matrices; root and nested
host listings; explicit and implicit activation results; canonical-load and
evaluator-identity results; before/after repository and Git manifests; full
test commands and normalized outputs; exact changed paths; manual assessments;
deviations; and residual uncertainty at
`docs/engineering/agentic-execution/evidence/WO-AEX-004-verification.md`.

## Stop and escalate conditions

Stop while this artifact is `draft`. After separate approval and start, stop
before changing an undeclared path, installer code, portable manifest semantics,
orientation identity, Phase 3 procedure, skill effect, evaluator boundary,
authority source, lifecycle behavior, provider permission, public version, or
distribution scope.

Stop if actual Codex or Claude Code behavior requires duplicated procedures,
global installation, user settings mutation, unsupported front matter, shell
injection, another adapter file, or a provider-specific change not closed by
`SPEC-AEX-005`. Stop on any required verification failure that cannot be
corrected within the exact declared scope.

## Completion report format

Report `Outcome`, `Done`, `Not done`, conditional `Blocked by`, `Current
lifecycle state`, `Decision required`, `Next`, `Command or response`, and
conditional `Alternatives`. Name `WO-AEX-004`, the four canonical skill names,
the two tested hosts and versions, exact changed paths, package and installation
inventories, activation results, evaluator identity, evidence path, deviations,
residual uncertainty, and intentionally unperformed lifecycle, global-install,
Git, network, release, credential, and external actions. Recommend exactly one
next authorized step.
