+++
id = "ADR-REB-009"
type = "adr"
title = "One qualification namespace with five typed operations"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner", "release-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
decides = ["ARCH-REB-009"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T08:15:39Z"
decided_by = "technical-owner"
+++

# ADR: One qualification namespace with five typed operations

## Status

Proposed.

## Context

Release 0.6.0 showed that a valid validator invocation is not necessarily valid release evidence. The evaluator, target, trust boundary, required checks, and meaning of the result must agree. Existing workflows assemble those facts independently using executable paths and raw validator commands, making an accidental invalid combination easy to express and hard to review.

The correction becomes a public interface used across candidate, predecessor, release, publication, and future managed workflows. It must be difficult to misuse, testable without relying on workflow prose, and extensible across future governor upgrades.

## Decision drivers

- Make invalid evaluator/target combinations unrepresentable or fail before validation.
- Put trust-boundary rules in reusable product code rather than workflow conventions.
- Give reviewers one clear vocabulary for five distinct claims.
- Preserve low-level diagnostic commands without treating them as release evidence.
- Retain exact provenance and independence semantics in one machine-readable format.
- Support an immediate predecessor that does not yet implement the new CLI.
- Avoid coupling all operations to one oversized parser with caller-selected behavior.
- Keep future workflow migrations mechanical and testable.

## Considered options

### Option 1: Documentation and workflow comments only

Document which interpreter and validator should be used in each lane. This has the smallest code change but leaves invalid combinations fully expressible and repeats the original failure mode.

### Option 2: Add a free-form `--role` to `doctor` or `validate`

One command could accept role, evaluator paths, targets, and optional checks. This centralizes syntax but produces a large cross-product of options and keeps the caller responsible for assembling a coherent combination. Parser acceptance would not establish the trust boundary.

### Option 3: One `harnessctl qualify` namespace with five typed subcommands

Each operation gets a closed parser and handler, while identity, result, and output infrastructure are shared. The public vocabulary matches the five distinct release claims and prevents cross-role option combinations.

### Option 4: Five unrelated top-level commands

Separate commands maximize parser isolation but fragment discovery, naming, help, result behavior, and compatibility policy. Shared concerns would be easier to duplicate or drift.

### Option 5: GitHub Actions/YAML wrappers around current commands

Reusable workflow wrappers would improve GitHub automation but would not protect local qualification, other CI systems, or direct operator use. Trust policy would remain outside the package and difficult to test at the CLI boundary.

## Decision

Select option 3.

Create one public `harnessctl qualify` namespace with exactly five typed subcommands: `released-root`, `predecessor-view`, `complete-candidate`, `candidate-package`, and `public-install`. Each subcommand owns a closed input schema, runtime/target binding, fixed checks, isolation rule, independence classification, and canonical `se-harness-release-qualification-v1` result.

Keep `doctor`, `validate`, and `identity` as low-level diagnostics. Retain `accept-candidate` for one compatibility cycle only as a delegation alias to `qualify candidate-package`; it is not an independent implementation or sixth role.

For initial deployment only, preserve exact public 0.6.0's already released `accept-candidate` command as a version-and-digest-bound bootstrap adapter. Because those immutable bytes predate `qualify`, retain their original functional-acceptance schema and never describe the adapter as an alias or canonical qualification result. Reject every other verifier identity or selectable command. Remove the adapter after the first released verifier exposing `qualify candidate-package` becomes available.

Use the current successor as coordinator for `predecessor-view`. For predecessors that lack the new command, a version-bound internal adapter may invoke only their exact documented entry points after successor-side identity and view checks. This does not expose arbitrary script selection to workflows.

## Consequences

### Positive

- Workflow intent becomes visible and machine-enforced.
- Cross-role arguments and common evaluator/target mistakes fail early.
- Provenance and independence claims have one stable result protocol.
- Local and hosted qualification use the same product boundary.
- Future release procedures can refer to operations rather than interpreter/script recipes.

### Negative and operational

- The CLI, workflows, tests, documentation, and evidence format change together.
- Existing workflow helpers must be adapted rather than merely renamed.
- Qualification performs additional hashing, identity, isolation, and no-change checks.
- A bounded legacy predecessor adapter remains necessary until the supported predecessor implements typed qualification.
- Root managed workflow adoption occurs later through normal upgrade governance, so repository-owned workflows and the installed root workflow temporarily differ.

### Security

- The design reduces candidate/predecessor import confusion and arbitrary script selection.
- The new coordinator and canonical output become security-sensitive parsing surfaces and require hostile path, archive, environment, manifest, and subprocess tests.
- Independence remains conditional on exact provenance and process isolation; the command name alone never establishes it.

### Migration

- Migrate repository-owned release lanes and the candidate managed-workflow template in the bounded work order.
- Preserve historical evidence and the current root managed files.
- Deprecate the `accept-candidate` alias after one compatibility cycle only through a later reviewed change.
- During the first cycle, retain exact public 0.6.0 legacy acceptance for the independent package lane; record a distinct schema and removal trigger rather than weakening the permanent command or falsely rewriting immutable capability.

## Validation

`VER-REB-009` verifies the closed parser matrix, runtime/target identity matrix, candidate substitution and import-boundary attacks, predecessor-view binding, deterministic result schema, workflow-command conformance, package/template parity, Windows/POSIX behavior, and root/history/external no-change guarantees.
