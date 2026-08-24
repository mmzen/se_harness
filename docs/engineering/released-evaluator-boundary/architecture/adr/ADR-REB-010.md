+++
id = "ADR-REB-010"
type = "adr"
title = "Declared interpreter-safety rule with one loader per runtime"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
decides = ["ARCH-REB-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T13:01:45Z"
decided_by = "technical-owner"
+++

# ADR: Declared interpreter-safety rule with one loader per runtime

## Status

Proposed.

## Context

Release 0.6.0 rejected a valid POSIX virtual environment because one boundary resolved `bin/python` before deriving the environment root. Investigating the fix showed the deeper problem: six boundaries across two runtimes each decide what a safe interpreter path is, and they disagree. Two are correct, one checks symbolic-link parents but not junctions, two perform no link checks at all, and one is fatal on POSIX. One of the correct boundaries already reaches into another package's private helper to borrow part of the rule.

Any correction must cross a deliberate dependency barrier. `repository_tools` imports only the standard library and its own package. That is not an oversight: it validates candidate source and must keep working when the candidate `se_harness` package is absent, broken, or deliberately excluded from the import path. Several of its boundaries exist precisely to establish that an external evaluator is not the candidate package.

The rule is also security-relevant and difficult to reverse. Once boundaries, retained evidence, and conformance checks depend on where it lives, moving it again is a second migration across the same barrier.

## Decision drivers

- One definition of interpreter safety, so a correction cannot land at one boundary and miss five.
- Preserve the `repository_tools` import barrier without weakening it for convenience.
- Make the rule reviewable as policy rather than discoverable only by reading six call sites.
- Make divergence between the two runtimes fail a check rather than survive to a release.
- Keep the frozen evaluator-evidence document, its bound sidecar digests, and existing diagnostic identifiers intact.
- Accept a terminal POSIX venv link and an ordinary Windows executable under one rule with no platform branch in policy.
- Follow a shape the repository already uses, so reviewers and packaging need no new concept.
- Avoid making the fix itself a source of drift.

## Considered options

### Option 1: Fix `release_bootstrap` only

Replace the fatal helper call at the one POSIX-fatal site and stop. This is the smallest change and unblocks the documented bootstrap path immediately. It leaves five inconsistent rules in place, leaves the junction gap unfixed, and leaves the next boundary free to invent a seventh variant. It does not satisfy `REQ-REB-026`.

### Option 2: Import `se_harness.interpreter_safety` from `repository_tools`

The package owns the rule and repository tooling calls it. This is the least code and gives one implementation directly. It breaks the import barrier that several `repository_tools` boundaries depend on, and it makes candidate package importability a precondition for validating candidate source — inverting the trust relationship those boundaries exist to establish.

### Option 3: Invert the dependency so `se_harness` imports `repository_tools`

The rule lives in repository tooling and the package consumes it. This keeps `repository_tools` self-contained but makes the shipped wheel depend on repository-owned tooling that is not part of the distribution, which is not packageable.

### Option 4: Duplicate the rule in both runtimes behind a parity test

Each runtime keeps its own implementation and a test asserts they agree. This respects the barrier and needs no new declaration. Parity tests catch divergence only for the cases they enumerate, the enumeration lives in a third place, and two implementations of a security rule remain two places to patch under time pressure.

### Option 5: Extract a shared third package that both runtimes import

A minimal package containing only the rule, imported by both. This gives one implementation and one import edge, but it adds a distribution unit, a versioning surface, and a packaging question to a project whose stated property is zero runtime dependencies and a single wheel.

### Option 6: Declared data document with one conforming loader per runtime

`se_harness/interpreter_safety.json` states the rule as data. `se_harness/interpreter_safety.py` and `repository_tools/interpreter_safety.py` each read it and neither imports the other. A boundary registry and a declared corpus executed by both loaders on both platforms make an unregistered boundary or a divergence a failing check.

## Decision

Select option 6.

Place the rule in one declared document, `se_harness/interpreter_safety.json`, with schema identifier `se-harness-interpreter-safety-v1`, holding the ordered case list, the boundary registry, and the conformance corpus. Give each runtime one stdlib-only loader that reads that declaration. Neither runtime imports the other.

This follows the shape the repository already uses for cross-cutting declared policy: `se_harness/hash_bound_classes.json` with `se_harness/hash_bound.py`, and `se_harness/governance_migration_contract.json` with `se_harness/governance_migration_contract.py`. Reviewers, packaging, and the portable-release-surface check all already handle that shape, so the declaration adds no new concept.

Register all six boundaries plus the delegating publication boundary. Make an unregistered interpreter validation, a divergence between the loaders, a declared case with no implementation, and an implementation outcome absent from the declaration each a failing check.

Record the terminal-link property, the resolved-target position class, and the resolved-target digest on `RuntimeIdentity`, additively, keeping the `se-harness-runtime-identity-v3` identifier. Leave the canonical `se-harness-evaluator-evidence-v1` document and its closed field sets unchanged, and keep `RID004`, `RID006`, and `MIG205`.

Option 1 is explicitly rejected as the whole answer, though its one-site correction is contained within this decision: the POSIX-fatal site is repaired by adopting the declared rule, not by patching the helper in place.

## Consequences

### Positive

- One reviewable location states what a safe interpreter path is.
- The POSIX bootstrap path documented in `AGENTS.md` and `REPOSITORY_CONTEXT.md` becomes usable.
- The junction gap and the two missing-check boundaries are closed by the same change that fixes the fatal one.
- The `repository_tools` import barrier is preserved without a parity-test compromise.
- A future boundary cannot quietly introduce a seventh rule.
- Retained identity evidence lets a reviewer tell which binary executed, not only which environment was named.

### Negative and operational

- A declared document plus two loaders is more moving parts than one shared function would be.
- Two loaders must be kept behaviorally identical; the corpus check is what makes that true rather than aspirational.
- Six boundaries change in one work order, including two whose observable behavior must not change, so the evidence must prove non-change as well as change.
- The declaration becomes package data and appears in the wheel, the portable-release-surface check, and any digest that covers package data.
- Windows cannot construct symbolic-link cases without privilege, so part of the corpus is provable only on Linux; junction cases are provable only on Windows. Both platforms must run.

### Security

- The rule moves from six implicit decisions to one explicit, checked policy, which is the substance of the correction.
- The declaration is a new parsed input and needs malformed-document, duplicate-key, and unknown-case tests.
- A data-driven rule must not become a waiver mechanism. The declaration carries no per-boundary exception and no allowlist, and that absence is checked.
- Junction detection is a distinct predicate with an explicit refusal when unavailable, so a platform or interpreter without it fails closed instead of skipping the check.
- Relaxing the terminal-link case is the only widening. Every other refusal is preserved or newly added.

### Migration

- Correct the POSIX-fatal boundary and the junction gap, add the missing checks at the two unchecked boundaries, and re-point the two already-correct boundaries at the declaration without changing what they decide.
- Preserve every existing bound digest, evidence sidecar, released byte, and root managed file.
- Defer a distinct runtime-identity schema identifier to a later governed change that also adopts a matching root evaluator, because the installed root validator accepts only v2 and v3.
- Do not adopt, release, publish, or tag anything as part of this decision.

## Validation

`VER-REB-010` verifies the declared corpus through both loaders on Windows and Linux, the boundary registry, the POSIX terminal-link acceptance, every refusal including the junction parent, the recorded facts and their independent verification, the unchanged evaluator-evidence sidecars and bound digests, the preserved diagnostic identifiers, the preserved behavior of the two already-correct boundaries, the `repository_tools` import barrier, and the absence of any waiver mechanism in the declaration.
