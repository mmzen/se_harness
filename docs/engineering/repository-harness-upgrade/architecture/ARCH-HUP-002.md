+++
id = "ARCH-HUP-002"
type = "architecture"
title = "Advance the existing external-governor boundary to schema 3"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]
addresses = ["REQ-HUP-004", "REQ-HUP-005", "REQ-HUP-006"]
conforms_to = ["SPEC-HUP-002"]

[decision_assessment]
outcome = "no_significant_decision"
triggers = []
rationale = "The proposal uses the already selected standard-repository installation, external immutable released-evaluator trust boundary, target 0.6.0 upgrade transaction, schema-3 identity format, and existing three-role CI lanes exactly as released; it introduces no new dependency direction, public interface, persistence model, deployment boundary, external service, credential path, failure strategy, or cross-cutting product policy."
assessed_by = "technical-owner"
+++

# Architecture: Advance the existing external-governor boundary to schema 3

## Context and scope

The repository already operates under an external released evaluator. This packet advances that selected immutable evaluator from 0.5.0/schema 2 to 0.6.0/schema 3 through the released standard-root transaction.

## Components and responsibilities

- The external public 0.6.0 environment supplies the applying CLI, packaged templates, payload manifest, and archive identity.
- The upgrade authorization packet binds the current lock bytes to the one permitted target identity.
- The installer plans and atomically applies safe managed changes, the schema-3 lock, and keyed evaluator evidence.
- Managed root configuration and the evaluator workflow declare the selected version.
- Owner-controlled repository facts remain outside managed ownership.
- Candidate-source and candidate-package lanes remain non-governing evidence.

## Dependency direction

`accountable approval -> current immutable lock -> external public 0.6.0 evaluator -> authorized transaction -> managed root candidate -> independent checks -> later assurance decision`

Candidate source and candidate packages never flow into the released-evaluator runtime.

## Data and control flow

`published wheel + RLS digest -> isolated install -> runtime identity -> dry-run plan -> exact work-order match -> transactional apply -> schema-3 lock + keyed evidence -> no-op replay and verification`

## Trust boundaries

- Public bytes are trusted only after archive and payload reconciliation.
- Checkout source, work-order content, locks, paths, workflows, generated output, and candidate packages are untrusted inputs.
- The current lock and exact approved packet jointly bound mutation; neither alone is sufficient.
- Human owners retain definition approval, work authorization, verification, commit, PR, merge, and external decisions.

## Required patterns

- External isolated released runtime before mutation.
- Immutable archive and payload identity.
- Exact prior-lock authorization and plan-first transaction.
- Atomic replacement, keyed evidence, rollback snapshot, and no-op replay.
- Owner-content preservation and three-role runtime provenance.

## Prohibited patterns

- Checkout or candidate-governor execution.
- Hand-editing a partial version, policy, workflow, or lock transition.
- Deleting the retired repository-context owner file.
- Expanding the plan without amended approval.
- Combining product, release, publisher, deployment, or external-state changes.

## Quality attributes

- **Integrity:** managed bytes, lock, runtime payload, and archive agree.
- **Independence:** evaluator origins remain outside the checkout.
- **Atomicity:** no partial managed state or unbound evidence survives failure.
- **Auditability:** target identity, authorization, plan, writes, and checks are retained.
- **Recoverability:** the complete pre-write state is restorable and Git history remains available.
- **Minimality:** only the released installer-owned surface changes.

## Conformance checks

- Verify archive/payload identity and isolated origins.
- Compare approved, immediate pre-apply, applied, and replay plans.
- Compare pre/post owner, product, formal-history, release, and publication hashes.
- Run doctor, validation, preflight, inspection, dashboard, tests, release-distribution, and role checks.

## Related ADRs

No ADR is required. On 2026-08-23 the accountable owner explicitly approved `ARCH-HUP-002`, including the declared `no_significant_decision` assessment, as part of the complete HUP-002 packet.
