+++
id = "ARCH-HUP-001"
type = "architecture"
title = "Apply the existing standard-repository evaluator boundary"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
addresses = ["REQ-HUP-001", "REQ-HUP-002", "REQ-HUP-003"]
conforms_to = ["SPEC-HUP-001"]

[decision_assessment]
outcome = "no_significant_decision"
triggers = []
rationale = "The proposal uses the already selected standard-repository installation, external released-evaluator trust boundary, managed upgrade transaction, and existing three-role CI lanes; it changes only the released evaluator version and introduces no new boundary, dependency direction, public interface, persistence, deployment model, external service, failure strategy, or cross-cutting policy."
assessed_by = "technical-owner"
+++

# Architecture: Apply the existing standard-repository evaluator boundary

## Context and scope

The repository already operates as a standard repository governed by an external released evaluator. This packet advances the selected immutable evaluator from bootstrap 0.5.0a1 to final 0.5.0 through the existing managed upgrade transaction.

## Components and responsibilities

- The external public 0.5.0 environment supplies the governing CLI and distribution identity.
- The managed installer plans and applies safe root-template changes and lock updates.
- Root configuration and managed contract declare the selected evaluator.
- Engineering Harness CI installs the exact evaluator outside the checkout.
- Candidate-evidence CI continues to assess source and package roles without governance authority.
- Repository-owned context and evidence explain the transition but do not create authority.

## Dependency direction

`accountable approval -> current governor preflight -> external public 0.5.0 upgrader -> managed root candidate -> independent evaluator CI -> assurance decision`

Candidate source and candidate packages never flow into the released-evaluator runtime.

## Data and control flow

`immutable wheel identity -> dry-run plan -> exact plan review -> transactional apply -> lock/integrity proof -> candidate tests and hosted CI -> later VREC review`

## Trust boundaries

- The public 0.5.0 installation is trusted only after exact role and digest checks.
- Checkout source, candidate wheels, workflows, event data, and generated output remain untrusted inputs.
- Human owners retain approval, verification, commit, PR, merge, and release decisions.
- Public 0.5.0 publication does not retroactively authorize its historical product release.

## Required patterns

- External released runtime before mutation.
- Plan-first managed transaction.
- Exact changed-surface and lock reconciliation.
- Three-role runtime provenance.
- Fail-closed preflight, validation, and hosted checks.

## Prohibited patterns

- Self-hosting data, a special implementation-repository profile, or candidate-governor execution.
- Hand-editing a partial version selection.
- Product source, version, release record, publisher, tag, Pages, or issue changes.
- Automatic lifecycle transitions or external writes.

## Quality attributes

- **Integrity:** all managed version-bearing files and lock agree.
- **Independence:** evaluator origins are outside the checkout.
- **Auditability:** exact distribution, plan, diff, and checks are retained.
- **Recoverability:** pre-merge recovery uses ordinary Git history and supported installer behavior.
- **Minimality:** only proven-safe managed root changes occur.

## Conformance checks

- Verify public evaluator role and wheel SHA-256.
- Compare dry-run and applied changed surfaces.
- Run doctor, validation, preflight, inspection, dashboard, tests, workflow parsing, and role-origin checks.
- Prove package source/version and release surfaces are byte-identical to the base.

## Related ADRs

No ADR is required. On 2026-08-20 the accountable owner explicitly approved `ARCH-HUP-001` including its `no_significant_decision` assessment as part of the complete HUP packet. The architecture applies the existing standard-repository boundary without changing a controlled trigger.
