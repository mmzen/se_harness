+++
id = "ARCH-EVK-001"
type = "architecture"
title = "Independent evidence-attribution execution planes"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[relations]
addresses = ["REQ-EVK-001", "REQ-EVK-002", "REQ-EVK-003", "REQ-EVK-004"]
conforms_to = ["SPEC-EVK-001"]

[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "responsibility-or-dependency-direction", "security-privacy-or-trust-boundary", "cross-cutting-policy", "material-alternatives"]
rationale = "Evidence-path keying is a public repository convention used across package preparation, formal governance validation, and derived review surfaces. Choosing where the predicate lives changes dependency direction across the candidate-package and standalone managed-script trust boundary, while loose component matching could weaken attribution. Material alternatives therefore require one explicit decision."
assessed_by = "technical-owner"
+++

# Architecture: Independent evidence-attribution execution planes

## Context and scope

Evidence attribution currently exists independently in package provenance preparation, managed validation, and managed dashboard discovery. The package and repository-local scripts intentionally occupy different assurance and deployment planes, but their observable keying result must be identical.

This architecture governs only extraction and consumption of work-order keys from already normalized paths. Existing path safety, evidence content projection, formal artifact authority, record lifecycle, Git provenance, and release controls remain in their current components.

## Components and responsibilities

- The installed-package attribution predicate supplies structural key membership to `capture-verification` without importing repository-local target code.
- The managed validator attribution predicate is the portable repository-local semantic source for formal validation.
- The dashboard generator imports the validator predicate it already depends on and owns only bounded filesystem discovery and association projection.
- Inspection consumes generated snapshot findings and does not add another matcher.
- A cross-plane contract-case suite owns observable parity between installed-package and repository-local predicates.
- Managed templates and lock data carry the portable behavior into the one standard consumer installation.

## Dependency direction

```text
harnessctl capture-verification
  -> installed package provenance
  -> package evidence-key predicate

managed validator
  -> portable evidence-key predicate

managed dashboard generator
  -> managed validator predicate
  -> evidence discovery and derived projection

managed inspection
  -> dashboard snapshot/findings

shared contract cases
  -> compare package and portable observable results
```

No dependency flows from the validator or dashboard into `se_harness` in the target checkout. No derived presentation result flows back into formal validation or provenance.

## Data and control flow

An existing caller normalizes or derives a repository-relative path and independently enforces its safety rules. The appropriate plane's pure predicate selects candidate components, extracts exact keys, deduplicates, and sorts them. Capture and validation perform explicit membership checks. Discovery builds a stable work-order-to-path map. Derived findings and readiness consume that map.

## Trust boundaries

Path strings, directory names, filenames, target checkout modules, evidence content, and formal metadata are untrusted. A matching key is attribution evidence only; it cannot bypass path safety or create verification authority. Repository-local scripts must remain operable without importing candidate package code. The released governor remains isolated from both candidate planes.

## Required patterns

- Exact, bounded, case-sensitive component-prefix matching.
- Independent safety validation before an association can qualify aggregate evidence.
- One portable repository-local predicate reused by validator and dashboard.
- One installed-package predicate with equivalent behavior but no target-code import.
- Shared positive, negative, multi-key, ordering, and platform contract cases.
- Deterministic mapping and serialized output.
- Managed root/template parity and plan-first upgrade.

## Prohibited patterns

- Searching arbitrary ancestors or repository names for work-order-like text.
- Reimplementing matching independently in inspection or Explorer.
- Importing `se_harness` from target checkout in standalone validation.
- Treating a key match as path containment, file safety, content sufficiency, or human assurance.
- Moving or rewriting historical evidence and commit-bound records.
- Adding an installation profile or runtime dependency.

## Quality attributes

Backward compatibility, auditability, deterministic behavior, cross-platform portability, least authority, hostile-input safety, independent assurance, and managed-distribution parity take precedence over avoiding a small pure implementation in each assurance plane.

## Conformance checks

`VER-EVK-001` exercises one shared case matrix against both predicates, aggregate capture and authored-record validation, Explorer/inspection findings, platform-independent path handling, unsafe-path regression, root/template parity, upgrade behavior, and complete repository checks.

## Related ADRs

`ADR-EVK-001` decides to retain independent installed-package and repository-local implementations while centralizing repository-local consumption and enforcing cross-plane behavioral parity.
