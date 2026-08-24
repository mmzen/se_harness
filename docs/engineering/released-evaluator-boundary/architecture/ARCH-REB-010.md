+++
id = "ARCH-REB-010"
type = "architecture"
title = "One interpreter-safety rule serving two runtimes"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
addresses = ["REQ-REB-024", "REQ-REB-025", "REQ-REB-026"]
conforms_to = ["SPEC-REB-011"]

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "security-privacy-or-trust-boundary", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "The correction places a security rule that every evaluator-identity boundary depends on, and it must do so across a deliberate dependency barrier: repository_tools imports only the standard library and its own package. Choosing where the rule lives fixes the dependency direction between the package runtime and the repository-tools runtime, changes a trust boundary that six sites currently decide independently, and is difficult to reverse once boundaries and evidence formats depend on it. Importing the package, duplicating with a parity test, and a declared data contract with two loaders are materially different alternatives with different long-term drift and packaging costs."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T13:01:45Z"
decided_by = "technical-owner"
+++

# Architecture: One interpreter-safety rule serving two runtimes

## Context and scope

Six boundaries in two runtimes decide independently whether an interpreter path is a safe environment entry point. `REQ-REB-026` records their current disagreement: two are correct, one refuses junction parents only by accident of using a helper that checks them, one refuses nothing, and one is fatal on POSIX. A repair applied at the fatal site would leave the disagreement intact.

The rule is a trust-boundary rule. It determines whether a released evaluator can be relocated, aliased, or pointed at candidate bytes. That makes its placement an architecture question rather than a refactoring preference, and the placement is constrained by an existing deliberate boundary: `repository_tools` does not import `se_harness`, because it operates on candidate source and must keep working when the candidate package is not importable.

This architecture puts the rule in one declared data document with one conforming loader per runtime, and makes boundary registration and cross-runtime agreement mechanically checked.

## Components and responsibilities

### Interpreter-safety declaration

`se_harness/interpreter_safety.json` holds the ordered case list, the boundary registry, and the conformance corpus. It is data with a schema identifier and contains no code and no waiver. It is the reviewable location of the policy.

### Package loader

`se_harness/interpreter_safety.py` reads its sibling declaration and evaluates a supplied path for the package runtime. It follows the pattern already established by `se_harness/hash_bound.py` and `se_harness/governance_migration_contract.py`: a small stdlib-only module beside its declaration, shipped as package data.

### Repository-tools loader

`repository_tools/interpreter_safety.py` reads the same declaration from its position relative to the repository root and evaluates a supplied path for the repository-tools runtime. It imports only the standard library and its own package.

### Identity boundaries

Six registered call sites consume a loader instead of restating the rule:

- `se_harness/runtime_identity.py` observing `sys.executable` for the released-evaluator and candidate-package roles;
- `se_harness/release_qualification.py` locating an external predecessor evaluator;
- `se_harness/governance_migration.py` probing a predecessor or successor runtime;
- `repository_tools/release_bootstrap.py` binding a released evaluator to a release record;
- `repository_tools/predecessor_preparation.py` validating an external interpreter;
- `repository_tools/predecessor_assessment.py` normalizing a verified interpreter origin.

`repository_tools/predecessor_publication.py` reaches the rule through `predecessor_preparation` and is registered as a delegating boundary rather than a seventh rule.

A boundary may add role-specific checks on top of the rule. It may not weaken, reorder around, or restate the declared refusals.

### Interpreter identity facts

`RuntimeIdentity` carries the lexical entry point plus the terminal-link property, the resolved-target position class, and the resolved-target digest. The canonical evaluator-evidence document is a separate, frozen output and does not carry them.

### Conformance checks

One check enumerates the boundary registry and fails on an unregistered interpreter validation. One check runs the declared corpus through both loaders on Windows and Linux and fails on any disagreement, on a declared case with no implementation, or on an implementation outcome absent from the declaration.

## Dependency direction

```text
se_harness/interpreter_safety.json          (declared policy, data)
        ^                        ^
        |                        |
se_harness/interpreter_safety.py  repository_tools/interpreter_safety.py
        ^                                  ^
        |                                  |
runtime_identity                    release_bootstrap
release_qualification               predecessor_preparation
governance_migration                predecessor_assessment
                                            ^
                                            |
                                    predecessor_publication
```

Both runtimes depend on the declaration; neither depends on the other. `repository_tools` continues to import only the standard library and its own package. No identity boundary depends on another boundary's private helper for the rule, which removes the current cross-package reach into `bootstrap._path_has_link` as the definition of link safety.

The declaration depends on nothing. It is not generated, not derived from the implementation, and not written by either loader.

## Data and control flow

1. A boundary receives a supplied interpreter path and, where it has them, a checkout root and a declared environment root.
2. It calls its runtime's loader.
3. The loader evaluates the declared cases in declared order and returns either the first refusal's case identifier and subject, or an acceptance carrying the lexical entry point, the environment root, the resolved target, and the recorded facts.
4. On refusal the boundary raises its own error type carrying the case identifier, before spawning any interpreter and before validating any target.
5. On acceptance the boundary derives its expected identity from governed inputs, compares each recorded fact against its own observation, and only then performs its substantive checks.
6. Where the boundary retains evidence, it records the lexical entry point normalized against the declared root and the bounded facts, never the resolved target's path.

## Trust boundaries

- Every supplied path is untrusted, including one that arrives through a lock, a release record, a bootstrap contract, or a view manifest.
- The lexical entry path is the execution boundary. The resolved target is an identity fact about the interpreter, not the location of the environment.
- A terminal interpreter link is inside the trust boundary. Any link above it is outside, because it lets the whole environment be relocated after a check.
- A junction is a link for this purpose. Detecting it by a predicate distinct from symbolic-link detection is part of the boundary, not an implementation detail.
- A resolved target inside the candidate checkout means candidate bytes would execute as the released evaluator, regardless of where the lexical path sits.
- The declaration states policy. It confers no authority and is not a waiver mechanism.

## Required patterns

- One declared document as the single source of the rule; two loaders that read it.
- Lexical normalization before any containment or root derivation.
- Junction detection as a predicate separate from symbolic-link detection, with an explicit refusal when the predicate is unavailable.
- First-refusal-wins evaluation in declared order, so a refusal identifier is stable for a path form.
- Lexical comparison on both sides of an interpreter-path equality check.
- Recorded facts verified against the boundary's own independent observation.
- Boundary registration plus a cross-runtime corpus executed on both platforms.
- Existing diagnostic identifiers preserved where other artifacts, contracts, or fixtures bind them.

## Prohibited patterns

- `repository_tools` importing `se_harness`, or `se_harness` importing `repository_tools`.
- A second implementation of the rule in either runtime, or a boundary restating a declared refusal inline.
- Reaching into another module's private link helper as the definition of link safety.
- Deriving an environment root from a resolved interpreter target.
- Comparing an interpreter path by resolving both sides.
- Recording the resolved target's absolute path in retained evidence.
- Detecting a junction only through `is_symlink`, or silently skipping the junction check when the predicate is unavailable.
- A per-boundary waiver, an allowlisted diagnostic, or a platform-name conditional standing in for a declared case.
- Adding a field to the evaluator-evidence `origins` or `environment` objects, or changing the runtime-identity schema identifier, as part of this correction.
- Generating the declaration from the implementation, or updating it automatically from an observed outcome.

## Quality attributes

- **Safety:** an unsafe interpreter path is refused before the interpreter runs, at every boundary, under one rule.
- **Portability:** the same rule accepts an ordinary Windows interpreter and a terminal POSIX venv link with no platform branch in policy.
- **Auditability:** the accepted entry point, the terminal-link property, the resolved-target position class, and the resolved-target digest are all recorded, so a reviewer can tell what executed.
- **Drift resistance:** a rule change is one reviewable data change, and a divergence between the runtimes fails a check rather than surviving until the next release.
- **Determinism:** an immutable environment yields identical decision-bearing facts across runs and platforms.
- **Compatibility:** frozen evidence documents, bound digests, and existing diagnostic identifiers are unaffected.

## Conformance checks

- The boundary registry matches the set of interpreter validations found in both runtimes; an unregistered validation fails.
- The declared corpus produces identical outcomes from both loaders, on Windows and on Linux, with platform-unconstructable forms skipped explicitly rather than silently.
- A declared case with no implementation, and an implementation outcome absent from the declaration, both fail.
- Import checks prove `repository_tools` imports only the standard library and its own package, and that no boundary imports another boundary's private link helper.
- A digest check proves the evaluator-evidence sidecars and their recorded digests are unchanged, and that no digest bound elsewhere in the repository moved unmeasured.
- Static checks prove no boundary derives an environment root from a resolved target and no interpreter comparison resolves both sides.
- The prohibited-pattern list above is checked, not only documented.

## Related ADRs

`ADR-REB-010` selects the declared data document with one conforming loader per runtime over importing `se_harness` from `repository_tools`, duplicating the rule behind a parity test, inverting the dependency so the package imports repository tooling, or extracting a shared third package.
