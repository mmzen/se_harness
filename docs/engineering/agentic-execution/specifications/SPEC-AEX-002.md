+++
id = "SPEC-AEX-002"
type = "specification"
title = "Portable skills, orientation, orchestration, and runtime adapter contract"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
specifies = ["REQ-AEX-005", "REQ-AEX-006", "REQ-AEX-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T09:03:54Z"
decided_by = "technical-owner"
+++

# Specification: Portable skills, orientation, orchestration, and runtime adapter contract

## Scope

This specification defines the proposed portable SE Harness skill profile, the
first read-only `harness-orient` skill, bounded worker orchestration, and derived
runtime adapter behavior. It makes skills the preferred reusable procedure
interface while retaining `harnessctl` and managed machine contracts as the
source of workflow legality.

`WO-AEX-001` selects only the `harness-orient` portion of this specification.
Autonomous mutation skills, multi-agent writers, and adapter materialization
remain outside that first work order.

## Actors and external systems

- An operator explicitly invokes a skill or supplies a task matching its
  unambiguous description.
- A primary agent loads the portable skill core and executes the single-agent
  path.
- Optional workers execute bounded delegated tasks under logical execution
  profiles.
- The released evaluator and `harnessctl` provide repository integrity,
  validation, inspection, focus, preflight, and workflow results supported by
  the installed version.
- Runtime adapters translate logical profiles and skill metadata into
  provider-specific files.
- Agent runtimes discover skills and profiles, enforce technical permissions,
  and optionally provide subagent execution.

## Inputs

### Portable skill package

A portable skill directory contains:

```text
<skill-name>/
├── SKILL.md
├── skill-contract.json
├── scripts/          optional
├── references/       optional
└── assets/           optional
```

`SKILL.md` contains the runtime-readable instructions and the minimum portable
metadata `name` and `description`. `skill-contract.json` is the deterministic
SE Harness declaration consumed by conformance checks. It does not grant
authority.

The `se-harness-skill-contract-v1` fields are:

```json
{
  "schema": "se-harness-skill-contract-v1",
  "name": "harness-orient",
  "version": "semantic-or-project-version",
  "outcome": "human-readable outcome",
  "activation": {"explicit": true, "implicit": true, "must_not_match": []},
  "inputs": [],
  "preconditions": [],
  "mutation_class": "read-only",
  "evaluator": {
    "minimum_version": "0.5.0",
    "required_operations": ["version", "identity", "doctor", "validate-json", "inspect-json"],
    "optional_operations": ["focus-json", "preflight"],
    "missing_required": "blocked",
    "missing_optional": "degraded"
  },
  "harness_operations": [],
  "delegation": {"allowed": false, "fallback": "single-agent"},
  "evidence": {"receipt_schema": "se-harness-execution-receipt-v1", "target_retention": false},
  "stop_conditions": [],
  "outputs": []
}
```

The contract uses strict field sets and typed entries for inputs, operations,
stops, and outputs. The exact `harness-orient` instance must declare `target`,
the structured released-evaluator launcher and expected identity, and an
optional selected artifact as inputs. The launcher may be host-specific input
but is excluded from portable retained output.

### Canonical source, installed location, and digest

The canonical source for the pilot is:

```text
templates/repository/standard/.agents/skills/harness-orient/
```

The standard installer places it in the target repository at:

```text
.agents/skills/harness-orient/
```

`SKILL.md` and `skill-contract.json` are required and retained in the installed
repository. Optional `scripts/` and `references/` files are part of the same
managed portable core. The pilot permits only regular UTF-8 text files and
prohibits symlinks, junctions, binary assets, generated caches, runtime state,
and provider-specific overlays inside the core directory.

The package and source distribution include the canonical standard-template
directory exactly once. No duplicate authoritative copy is stored under
`se_harness/skills/`. The existing ownership-aware standard installer treats
the installed files as `managed`: an exact prior managed version may upgrade,
while missing, ambiguous, or customized content blocks the transaction without
partial writes.

`se-harness-skill-manifest-v1` binds the portable core:

1. recursively enumerate every regular file under the core directory;
2. reject an empty set, symlink, junction, path escape, case collision,
   duplicate normalized path, control character, and non-UTF-8 content;
3. normalize repository-relative paths to `/` and file bytes with
   `utf8-text-lf-v1`;
4. record `path`, `mode = "utf8-text-lf-v1"`, and lowercase SHA-256 for each
   file in UTF-8 path order;
5. encode the manifest with `se-harness-canonical-json-v1`; and
6. identify the skill by lowercase SHA-256 of those manifest bytes.

The manifest is returned or retained as evidence but is not written into the
core, avoiding self-reference. Runtime overlays live outside the core and bind
this digest plus their own adapter name, version, paths, and content digests.

### Logical execution profile

A logical profile describes:

- stable profile name and purpose;
- permitted operation classes;
- default mutation class;
- prohibited decisions and actions;
- required skill capabilities;
- input and result schemas;
- requested runtime characteristics without claiming they are enforceable on
  every provider.

Logical profiles never use accountable role names as their source of authority.
Runtime-specific model names, tool identifiers, sandbox syntax, hooks, MCP
configuration, memory, and thread limits belong in adapters.

### Runtime adapter request

- selected supported runtime and adapter version;
- logical profile and portable skill manifest digests;
- destination repository;
- existing runtime configuration and ownership observations;
- plan or explicit apply mode.

### Evaluator capability profile for `harness-orient`

The minimum supported exact released evaluator for the pilot is 0.5.0. The
caller supplies a structured external evaluator launcher and the expected
version and installation root required by the existing identity interface. The
skill does not search a target checkout for executable candidate code, install
an evaluator, or silently fall back to an executable found on `PATH`.

| Operation | Minimum 0.5.0 behavior | If unavailable or unsuccessful |
| --- | --- | --- |
| `version` | required; compare exact observed and target-required version | `blocked`; report expected and observed values without continuing as governed orientation |
| `identity` | required released-evaluator identity check using the supplied expected version/root and isolated invocation | `blocked`; candidate source cannot substitute |
| `doctor` | required read-only managed-integrity check | `blocked`; preserve the exact integrity diagnostic |
| `validate-json` | required formal graph validation | invalid graph produces `blocked` orientation with the exact scoped or repository findings; malformed or unavailable JSON is `failed` |
| `inspect-json` | required repository-wide lifecycle and attention result when validation permits safe inspection | unavailable output is `blocked`; unrelated findings remain separately counted |
| `focus-json` | optional capability available only when the exact evaluator exposes it | selected-scope fields become `not_assessable` and outcome is `degraded`; do not parse prose or use candidate focus |
| `preflight` | optional and run only for an explicitly selected WO and requested phase | absence is reported as `degraded`; the skill never treats preflight failure as approval or start authority |

Evaluators older than 0.5.0 are unsupported and produce `blocked`. A newer exact
released evaluator may supply optional operations only after its identity is
verified. Feature support is determined from the verified version and public
help contract, not by trial-running a mutating command.

## Outputs

### Skill result

Every skill returns:

- selected outcome and target;
- completed procedural steps;
- current lifecycle state;
- scoped and repository blockers;
- background observations kept separate from selected work;
- one recommended next step;
- required accountable role or explicit statement that no decision is needed;
- command, suggested response, or capability limitation;
- execution receipt identity.

The result maps to the managed lifecycle restitution contract where a selected
formal lifecycle stage is involved.

### Orientation result

`harness-orient` returns a read-only result containing:

- repository root and project identity without leaking unnecessary host paths;
- installed harness version and integrity outcome;
- released-evaluator identity or exact missing-evaluator diagnostic;
- formal validation and inspection summary;
- selected artifact scope when requested and supported;
- current lifecycle state, blockers, background count, and attention queues;
- next accountable decision point and required role when one exists;
- commands actually run and execution receipt digest;
- confirmation that no repository, Git, lifecycle, or external mutation was
  performed.

### Adapter plan and manifest

A runtime adapter returns a deterministic plan of create, update, preserve,
conflict, and unsupported-feature entries. Applied output includes a manifest
binding:

- logical profile and skill digests;
- adapter name and version;
- generated paths and content digests;
- preserved user-owned paths;
- declared capability degradations;
- no formal lifecycle effect.

## State model

Skills use procedure states independent from formal lifecycle state:

```text
discovered -> loaded -> preconditions_checked -> executing
executing -> completed | degraded | stopped | failed
```

An unsupported optional capability produces `degraded` with the exact
deterministic limitation. Missing authority or an accountable decision point
produces `stopped`; invalid required execution produces `failed` or `blocked` in the
orientation result. None can change a failed harness gate into `completed`.

Adapter operation uses:

```text
inspect -> planned -> applied
inspect | planned -> conflict | unsupported
```

Plan, conflict, and unsupported states are read-only. Apply changes only derived
runtime configuration explicitly covered by a future approved work order.

## Behavioral rules

1. **AEX-SKL-001:** A top-level skill represents one recognizable outcome, not
   one wrapper per CLI subcommand.
2. **AEX-SKL-002:** Skill activation and successful loading grant no mutation or
   lifecycle authority.
3. **AEX-SKL-003:** The skill queries supported machine-readable harness state
   before recommending or requesting a lifecycle operation.
4. **AEX-SKL-004:** The portable core contains no required provider-specific
   model, tool, permission, hook, or subagent syntax.
5. **AEX-SKL-005:** A skill with optional orchestration has a behaviorally
   equivalent single-agent fallback.
6. **AEX-ORI-001:** `harness-orient` is read-only across repository files, Git,
   lifecycle state, installed environments, network services, and external
   systems.
7. **AEX-ORI-002:** Orientation uses the exact released evaluator required by
   the target for installed-integrity claims and labels candidate observations
   separately.
8. **AEX-ORI-003:** Unsupported focus or workflow features produce an explicit
   reduced-capability result rather than guessed scope.
9. **AEX-ORC-001:** Every delegated task declares one profile, bounded input,
   operation class, scope, and result schema.
10. **AEX-ORC-002:** A child receives equal or narrower authority and scope than
    its parent.
11. **AEX-ORC-003:** Concurrent writers require disjoint scopes and isolated
    worktrees; one integration coordinator owns the combined candidate.
12. **AEX-ORC-004:** Final validation and evidence binding run against the
    combined repository after integration.
13. **AEX-ADP-001:** Adapter output is derived configuration and cannot become a
    decision or formal artifact merely by being generated or committed.
14. **AEX-ADP-002:** Adapter apply is plan-first, ownership-aware,
    transactional, customization-preserving, and replay-safe.

## Error and recovery behavior

- Missing or ambiguous target, damaged skill package, contract mismatch,
  unsupported evaluator, invalid repository, failed integrity, invalid graph,
  or conflicting instructions stop orientation without mutation.
- Missing `focus-json` or optional preflight support follows the declared
  reduced-capability matrix and never triggers candidate-source fallback.
- Missing optional subagent support selects the single-agent fallback.
- Worker timeout, interruption, invalid result, or coverage gap remains visible
  and cannot be summarized away.
- Overlapping writer scope rejects or serializes the plan before writes.
- Adapter ownership ambiguity preserves the existing path and reports conflict.
- Applied adapter failure restores prior generated and owner-controlled bytes or
  reports an explicit restoration failure.

## Data and interface contracts

- Skill and profile names use lowercase kebab case unless a portable upstream
  standard requires a stricter compatible form.
- `SKILL.md`, `skill-contract.json`, supporting files, and manifests are UTF-8
  text using the canonical location, manifest, path, and digest behavior above.
- Skill-contract JSON rejects duplicate keys, unknown fields, traversal,
  absolute paths, URI paths, control characters, and duplicate semantic entries.
- Command invocations use structured argument arrays and closed operation IDs.
- Runtime overlays bind the portable core digest and adapter version.
- Generated runtime files identify their derived status where the provider
  format permits it; the adapter manifest is the primary deterministic record.

## Security and privacy properties

- Treat skill packages, supporting scripts, repository instructions, adapter
  files, model output, worker results, and runtime capability reports as
  untrusted input.
- Supporting scripts execute only through the normal sandbox and permission
  boundary and cannot bypass the harness mutation guard.
- Normal skill results and receipts exclude credentials, environment dumps,
  hidden reasoning, private connector data, and unrelated artifact bodies.
- Runtime-specific permissions may be narrowed by an adapter but cannot enlarge
  an autonomy envelope or decision right.
- Orientation never installs packages, enables network access, or changes
  evaluator state automatically.

## Performance and capacity

- Initial skill discovery metadata remains concise and unambiguous.
- `harness-orient` adds bounded orchestration overhead relative to the same
  underlying read-only commands.
- Parallelism is used only when independent work is expected to reduce wall
  time or materially improve coverage.
- Concurrency has an explicit maximum; recursive unbounded spawning is
  unsupported.
- Adapter planning scales with selected logical profiles, skills, and owned
  runtime paths rather than the entire repository.

## Observability

- Report skill name, version, digest, activation mode, target, mutation class,
  fallback use, executed harness operations, evaluator identity, and outcome.
- For orchestration, report every worker profile, task, status, scope, and result
  digest.
- For adapters, report supported, degraded, omitted, preserved, conflicting,
  created, and updated features and paths.
- Metrics distinguish human decision time, procedural interruption, execution
  time, token or compute cost, retries, conflicts, and failed coverage.

## Compatibility and migration

- The command-driven workflow remains supported when no skill is installed.
- Existing repositories do not gain skills or agent definitions through an
  ordinary package update; repository installation or upgrade remains a
  separate governed transaction.
- The read-only pilot supports exact released evaluator 0.5.0 and later
  compatible versions through the declared operation matrix. Missing required
  operations block; missing optional operations degrade only their named output.
- Runtime adapter support is versioned independently from logical role and skill
  semantics.
- A second runtime is required before claiming practical cross-runtime
  portability.
- Historical runtime files and repository-owned customizations are never moved
  or rewritten automatically.

## Examples and counterexamples

### Example: read-only pilot

An operator asks an agent to orient itself in an installed repository. The
agent loads `harness-orient`, uses the required external evaluator for `doctor`,
runs validation and inspection, reports one next decision, emits a receipt, and
does not change any byte or install any tool.

### Example: optional read-only delegation

A later runtime supports subagents. The primary agent may delegate independent
read-only code mapping and test-catalog analysis, but the final orientation
result must match the single-agent authority, state, and stop semantics.

### Counterexample: generated verifier grants assurance

An adapter generates a runtime agent named `verification-evidence-analyst` with
read-only tools. That agent may analyze evidence but cannot transition a VREC to
`verified` or claim it holds the `assurance-owner` role.

### Counterexample: skill silently installs evaluator

The target requires a released evaluator that is missing. Orientation reports
the exact missing dependency and suggested installation procedure; it does not
download or install the evaluator without separate authority.

## Explicitly unspecified decisions

- Runtime-specific adapter file formats, model defaults, tool lists, sandboxes,
  hooks, MCP servers, memory, and concurrency controls.
- Whether the first distributed runtime integration is packaged as repository
  files, a plugin, or both.
- Multi-agent writer implementation, worktree lease format, and conflict
  reconciliation beyond the required invariants.

These decisions remain outside `WO-AEX-001`. They require later formal artifacts
and a separately approved bounded work order.
