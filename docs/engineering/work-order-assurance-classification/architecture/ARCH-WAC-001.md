+++
id = "ARCH-WAC-001"
type = "architecture"
title = "Explicit assurance metadata with derived lifecycle attention"
status = "implemented"
owners = ["technical-owner", "quality-owner", "security-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
addresses = ["REQ-WAC-001", "REQ-WAC-002", "REQ-WAC-003", "REQ-WAC-004", "REQ-WAC-005"]
conforms_to = ["SPEC-WAC-001"]

[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "cross-cutting-policy"]
rationale = "The change adds governed work-order metadata and versions the public inspection report while coordinating validator, preflight, inspection, templates, policy, and distribution behavior. Choosing explicit declaration rather than inference or universal VREC coverage is a cross-cutting policy decision with material alternatives."
assessed_by = "technical-owner"
+++

# Architecture: Explicit assurance metadata with derived lifecycle attention

## Context and scope

Commit-bound assurance applicability currently exists only in human reasoning. The architecture adds the smallest explicit source of truth to the work order that owns the execution boundary and projects it through existing validation, preflight, inspection, and distribution components.

## Components and responsibilities

- **Work-order metadata:** owns the explicit value, rationale, and recorded deciding role.
- **Artifact validator:** validates the table and actionable lifecycle boundary while preserving completed legacy compatibility.
- **Preflight:** displays the decision and refuses selected work without a usable declaration.
- **Inspector:** combines explicit required work with direct VREC coverage to derive non-authoritative lifecycle attention.
- **Provenance and release commands:** remain authoritative for exact candidates and receive no implicit scope from inspection.
- **Managed distribution:** keeps templates, policy, helpers, package data, installations, and upgrades consistent.

## Dependency direction

Formal work-order metadata feeds validation and preflight. Validated artifacts and declared VREC relations feed inspection. Inspection suggestions never feed back into artifacts, provenance capture, lifecycle transitions, or release authority. Canonical distribution sources render managed copies; repository-owned work orders are never rendered or rewritten by upgrade.

## Data and control flow

```text
accountable declaration -> work-order metadata -> validator/preflight
                                           \-> inspector + VREC relations -> derived queue
clean candidate + explicit human scope -------------------------------> capture-verification
```

The derived queue can point to the existing capture operation but cannot supply its record ID, aggregate membership, evidence, contracts, owner, or approval.

## Trust boundaries

Artifact metadata and prose are untrusted repository input. Existing bounded parsing and safe rendering controls apply. `decided_by` records a claimed accountable role; it is not identity authentication. Human decision rights remain outside the Python process.

## Required patterns

- One explicit work-order-owned declaration.
- Enumerated values and exact keys.
- Deterministic direct-edge VREC coverage.
- Versioned inspection output when its public shape changes.
- Canonical-first managed updates and safe reconciliation.
- Compatibility by omission only for completed legacy artifacts, never by inferred meaning.

## Prohibited patterns

- Title, date, prefix, branch, commit, or prose heuristics.
- Universal VREC requirements that create recursive governance.
- Automatic classification, scope aggregation, record creation, or lifecycle transition.
- Treating ready as verified or a work-order declaration as release evidence.
- Bulk mutation of repository-owned historical work orders during upgrade.

## Quality attributes

Prioritize explainability, deterministic output, fail-closed actionable work, backward-compatible repository validation, non-recursive governance, safe distribution, and stable human authority.

## Conformance checks

Apply `VER-WAC-001` across metadata validation, lifecycle matrices, preflight, inspection, aggregate coverage, compatibility, managed parity, fresh install, safe upgrade, supported Python versions, and full regression.

## Related ADRs

`ADR-WAC-001` selects explicit work-order metadata with bounded completed-legacy compatibility over inference, universal coverage, or a central allowlist.
