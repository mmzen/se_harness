+++
id = "SPEC-AEX-005"
type = "specification"
title = "Repository host discovery and activation contract"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
specifies = ["REQ-AEX-005", "REQ-AEX-009"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T16:49:43Z"
decided_by = "technical-owner"
+++

# Specification: Repository host discovery and activation contract

## Scope

This specification makes the four Phase 3 repository skills discoverable in
Codex and Claude Code while preserving one authoritative portable core for
each skill. It defines repository paths, thin-adapter content, native
activation policy, installation ownership, package inventory, validation, and
migration.

This specification does not define a worker profile, autonomy-envelope effect
adapter, subagent, tool permission, model choice, hook, connector, hosted
service, global installation, lifecycle operation, or external action.

## Actors and external systems

- The package author supplies canonical cores and deterministic host surfaces.
- The standard installer materializes and lock-binds managed repository files.
- Codex discovers canonical skills from `.agents/skills`.
- Claude Code discovers thin adapters from `.claude/skills`.
- The operator explicitly invokes writing skills and may explicitly or
  implicitly invoke the read-only orientation skill.
- The target repository's exact released evaluator validates installed
  integrity, formal state, gates, scope, and next action.
- Accountable owners retain every decision right defined by managed policy.

## Inputs

The installation input consists of:

- the four approved skill names;
- each canonical `.agents/skills/<name>/` source directory and contract;
- the closed host mapping in this specification;
- the standard template manifest and package inventory;
- the target repository's current managed lock and destination bytes; and
- the exact candidate package identity used for installation or upgrade.

Invocation additionally uses the inputs required by the selected canonical
skill. A host adapter cannot infer or omit the repository, evaluator launcher,
expected evaluator identity, selected artifact, requested outcome, non-effects,
or any other required skill input.

## Outputs

A successful installation produces:

- one complete managed canonical core for each skill under `.agents/skills`;
- one managed Claude adapter for each skill under `.claude/skills`;
- Codex explicit-only policy metadata for each writing skill;
- one managed-lock entry for every installed canonical, metadata, and adapter
  file; and
- a deterministic no-op result when the complete desired installation already
  exists unchanged.

A supported host session exposes the same four logical skill names. An
invocation continues through the selected canonical skill and therefore emits
the existing skill result, receipt, and managed lifecycle restitution. The host
surface adds no new authoritative output.

## State model

```text
candidate_template
  -> installation_planned
  -> ownership_checked
  -> installed_and_locked
  -> host_discovered
  -> canonical_loaded
  -> canonical_skill_procedure

installation_planned | ownership_checked
  -> unchanged | blocked | failed

host_discovered | canonical_loaded
  -> stopped_when_binding_or_integrity_is_invalid
```

Host discovery is not a lifecycle state. It is an observation about the
runtime's available repository skills.

## Behavioral rules

1. **AEX-HST-001 — canonical location.** The authoritative procedure,
   contract, and scripts for `<name>` exist only under
   `.agents/skills/<name>/` in an installed repository and under the matching
   standard-template source in a distribution.
2. **AEX-HST-002 — supported names.** The initial closed catalog is
   `harness-orient`, `harness-draft-change`,
   `harness-execute-work-order`, and `harness-prepare-assurance`. An adapter
   name must equal its canonical directory name and contract name.
3. **AEX-HST-003 — Codex discovery.** Codex discovers each canonical core
   directly from `.agents/skills`. No Codex wrapper duplicates `SKILL.md`.
4. **AEX-HST-004 — Codex activation.** Each writing core contains
   `agents/openai.yaml` with `policy.allow_implicit_invocation` set to `false`.
   The file grants no dependency, tool, model, or external permission.
5. **AEX-HST-005 — orientation identity.** `harness-orient` remains eligible
   for implicit discovery without adding an OpenAI policy file or changing any
   byte in its v1 core.
6. **AEX-HST-006 — writing-core identity.** Adding bound Codex metadata changes
   each writing-core manifest. Each writing skill increments its patch version,
   refreshes its portable manifest vector, and otherwise preserves the approved
   Phase 3 contract and procedure.
7. **AEX-HST-007 — Claude discovery.** Claude Code receives exactly one
   managed `.claude/skills/<name>/SKILL.md` adapter for each canonical name.
   The adapter is not part of the portable core and contains no canonical
   script, contract, lifecycle rule, gate, role mapping, or procedure copy.
8. **AEX-HST-008 — Claude activation.** Each writing adapter sets
   `disable-model-invocation: true` and remains user-invocable. The orientation
   adapter omits that field and permits normal read-only matching.
9. **AEX-HST-009 — adapter binding.** Adapter metadata declares schema
   `se-harness-host-adapter-v1`, the exact canonical name, and fixed
   repository-relative path `.agents/skills/<name>`. Its body resolves that
   path from the Claude project root, requires the complete canonical
   `SKILL.md` to be read, and resolves all referenced resources from the
   canonical directory.
10. **AEX-HST-010 — adapter stop.** A missing canonical directory, mismatched
    name, malformed contract, failed managed integrity result, unsupported
    adapter schema, path escape, or unexpected resource location stops before
    a canonical helper or repository effect.
11. **AEX-HST-011 — no adapter authority.** A host file may control discovery
    or implicit invocation only. It cannot change skill effects, lifecycle
    legality, decision rights, required gates, path scope, evidence, evaluator
    identity, or next action.
12. **AEX-HST-012 — managed ownership.** Canonical, Codex-metadata, and Claude-
    adapter files use installer mode `managed`. `init`, `adopt`, and upgrade
    evaluate them in the same atomic plan as all other standard files.
13. **AEX-HST-013 — customization.** Existing unowned conflicts or changed
    lock-owned files block the complete applicable transaction. The installer
    does not overwrite, merge, delete, or partially update them.
14. **AEX-HST-014 — package completeness.** Source and wheel distributions
    contain every canonical file and host adapter required to reproduce the
    template. They contain no second authoritative body or script under the
    Claude surface or import package.
15. **AEX-HST-015 — repository scope.** The installer writes no user-home,
    system, organization, cloud-account, marketplace, or unrelated-repository
    skill location.
16. **AEX-HST-016 — portable filesystem.** Canonical and adapter paths are
    regular UTF-8 text files with portable names. Links, junctions, hard links,
    reparse points, absolute paths, dot segments, alternate separators, and
    case-colliding names are prohibited.
17. **AEX-HST-017 — versioned support.** Verification records the exact Codex
    and Claude Code versions exercised. A later incompatible host behavior is
    a new compatibility input, not permission to reinterpret this contract.
18. **AEX-HST-018 — unchanged governance.** Discovery success, a visible skill
    name, explicit invocation, or runtime permission creates no accountable
    decision, lifecycle transition, Git authority, credential authority, or
    external-action permission.

## Claude adapter contract

The adapter `SKILL.md` uses YAML front matter with:

- `name`: the exact canonical skill name;
- `description`: a concise discovery description that preserves the canonical
  use and non-trigger boundary;
- `disable-model-invocation: true` for the three writing skills only; and
- `metadata`: a map containing the adapter schema, canonical name, and fixed
  canonical repository path.

It must not use `allowed-tools`, `disallowed-tools`, `model`, `context`,
`agent`, `hooks`, shell injection, dynamic command substitution, remote
content, or an argument transformation. The body performs only these steps:

1. identify itself as a non-authoritative discovery adapter;
2. resolve the declared canonical directory from the project root;
3. require the same-named complete canonical `SKILL.md`, contract, and
   resources to be loaded and validated;
4. require relative procedure resources to resolve from that directory; and
5. stop on any binding, integrity, identity, or loading failure.

The adapter then yields to the canonical procedure. It does not restate that
procedure.

## Error and recovery behavior

- Installation planning reports conflicts and customizations before any write.
- An apply-time race or write failure restores prior target bytes and lock
  state through the existing installer transaction.
- An adapter invocation never searches another directory, `PATH`, user skill,
  plugin, network location, or candidate checkout when its declared canonical
  repository path fails.
- Host-native syntax rejected by a tested host version fails the applicable
  acceptance case; prose similarity is not accepted as a substitute.
- If a host requires restart after a new top-level discovery directory appears,
  the result reports that operational step without changing repository state.

## Data and interface contracts

- Managed files use UTF-8, LF-normalized text and the existing canonical lock
  hash mode.
- Adapter metadata schema is the exact string
  `se-harness-host-adapter-v1`.
- Names are portable lowercase hyphenated skill names and must be equal across
  adapter directory, front matter, metadata, canonical directory, and skill
  contract.
- Canonical paths are fixed repository-relative forward-slash strings and may
  reference only `.agents/skills/<same-name>`.
- The Codex policy document contains only the false implicit-invocation policy
  unless later approved work explicitly adds another field.
- Package inventories distinguish `canonical-core`, `codex-policy`, and
  `claude-adapter`; only the first is an authoritative portable skill core.

## Security and privacy properties

- Treat adapters, front matter, paths, contracts, locks, repository content,
  and host output as untrusted input.
- Do not embed host paths, user names, credentials, environment dumps, private
  evidence, hidden reasoning, remote URLs, or shell commands in adapters.
- Do not grant tools or permissions through provider metadata.
- Require the exact released evaluator's identity and doctor checks before
  trusting managed skill bytes, as required by the canonical procedure.
- A host's failure to enforce invocation policy cannot widen the canonical
  contract: an implicitly selected writing skill still stops under its explicit
  activation precondition.

## Performance and capacity

- Discovery surfaces add four small Claude adapter files and three bounded
  Codex policy files.
- Installation and lock planning remain linear in the template file count.
- Adapter loading performs one fixed canonical lookup and no recursive search.
- Host listing and invocation tests use bounded prompts and retain normalized,
  secret-free results.

## Observability

Record candidate package and installed-lock identities, canonical and adapter
inventories, skill names and versions, canonical manifest digests, host and
platform versions, discovery results, explicit and implicit activation
outcomes, canonical path resolution, evaluator identity results, changed paths,
upgrade actions, deviations, and residual uncertainty.

## Compatibility and migration

- Preserve exact `harness-orient` v1 core bytes, manifest digest, activation,
  and result contract.
- Update the three writing skill patch versions and canonical vectors when
  adding Codex metadata; do not reinterpret the previous digests.
- Repositories with only `.agents/skills` remain valid on their lock-recorded
  evaluator and gain Claude adapters only through an explicitly authorized
  upgrade.
- Existing owner-created `.claude` content is preserved. A destination
  collision requires review rather than inferred adoption.
- Published 0.6.0 remains immutable. Candidate source may be tested through a
  non-promotable package, while public default behavior requires a later
  governed release.
- User-wide or plugin distribution may be proposed later and must preserve the
  exact skill names or explicitly resolve provider namespace changes.

## Examples and counterexamples

### Example: Claude writing invocation

Claude Code lists `/harness-execute-work-order` from its adapter. The operator
invokes it explicitly. The adapter loads
`.agents/skills/harness-execute-work-order/SKILL.md`, and the canonical skill
requires one already-started work order and its exact evaluator checks.

### Example: Codex orientation

Codex discovers `harness-orient` directly under `.agents/skills` and may select
it for a read-only orientation request. No provider wrapper or core change is
required.

### Counterexample: copied Claude procedure

A Claude adapter contains the Phase 3 procedure body and a private copy of
`check_scope.py`. Package tests reject it because it is a second authoritative
core rather than a thin adapter.

### Counterexample: global convenience install

An installer writes the skills to the operator's user directory so every
repository can see them. The operation is outside this contract even if both
hosts list the skills successfully.

## Explicitly unspecified decisions

- Concise provider-facing descriptions that preserve the exact activation
  class and canonical mapping.
- Private fixture organization under the work order's declared fixture prefix.
- Exact normalized formatting of host smoke-test transcripts.
- A later global plugin, enterprise deployment, cloud synchronization, or
  provider marketplace strategy.

These choices do not permit another workflow body, symlink, provider-granted
permission, host-specific lifecycle behavior, implicit writing activation, or
an undeclared installation destination.
