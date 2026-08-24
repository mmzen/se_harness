+++
id = "ARCH-HUP-003"
type = "architecture"
title = "Separate steady-state governor validation from governor succession"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]
addresses = ["REQ-HUP-008"]
conforms_to = ["SPEC-HUP-004"]

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "security-privacy-or-trust-boundary", "deployment-or-operating-model", "cross-cutting-policy", "material-alternatives"]
rationale = "The correction replaces an always-on predecessor validation model with a generic event-driven succession boundary, changes which evaluator may inspect which root, and must choose among hard-coded replacement, historical compatibility views, deletion, and version-independent transition assessment."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T20:22:49Z"
decided_by = "technical-owner"
+++

# Architecture: Separate steady-state governor validation from governor succession

## Context and scope

The managed Engineering Harness workflow already owns steady-state validation
with the selected released governor. The repository-owned predecessor workflow
was created for the 0.5.0-to-0.6.0 release bridge and incorrectly continued to
interpret a successor root as the old root. This architecture separates those
responsibilities for all future upgrades.

## Components and responsibilities

- Managed Engineering Harness workflow: ordinary current-governor identity,
  preflight, doctor, graph, and dashboard gates.
- Governor-transition workflow: event routing, read-only orchestration,
  checkout-clean proof, and retained hosted observation.
- Repository-owned transition resolver: trusted base selection, base/target
  configuration and lock comparison, approved work-order discovery, declaration
  and evidence consistency, and bounded diagnostics.
- Exact target evaluator: isolated identity, doctor, and complete target-root
  validation.
- Accountable owners: every artifact approval, work start/completion, VREC
  disposition, integration, and external action.

## Dependency direction

`event metadata -> transition resolver -> approved upgrade declaration + canonical evidence -> isolated target evaluator`

The target evaluator never imports the resolver from checkout, and the
predecessor evaluator never receives the successor root.

## Data and control flow

1. Checkout full target history without persistent credentials.
2. Resolve and validate one base commit.
3. Compare selected base and target governor identities.
4. Route equal identity to a read-only not-applicable observation.
5. Route changed identity through approved declaration and transaction-evidence
   validation.
6. Acquire and verify the exact target evaluator outside the checkout.
7. Validate the complete target root, retain bounded output, and prove no
   checkout mutation.

## Trust boundaries

- Trusted: full base Git object, canonical committed lock bytes, approved
  work-order lifecycle state, mutually agreeing immutable hashes, independently
  verified public evaluator installation.
- Untrusted until checked: PR metadata, target configuration, target work-order
  contents, downloaded archive, environment variables, paths, subprocess
  output, and candidate source.
- Never available: write credentials or privileged publication/deployment
  authority.

## Required patterns

- Exact identities, fail-closed ambiguity handling, canonical JSON evidence,
  bounded output, isolated runtime, no checkout writes, and deterministic event
  routing.

## Prohibited patterns

- Hard-coded version pairs, `latest`, running N against an N+1 root, treating
  raw byte inequality as isolation, permanent current-governance compatibility
  views, implicit approvals, or automatic lifecycle/external actions.

## Quality attributes

- Repeatability: the next version pair requires new governed identity data, not
  new routing code.
- Security: target code and event data cannot select an unverified governor.
- Portability: canonical comparisons give the same result on LF and CRLF hosts.
- Diagnosability: every stop identifies the failed identity or evidence
  predicate without large or sensitive dumps.

## Conformance checks

`VER-HUP-004` exercises same-version, version-change, ambiguity, tampering,
origin, line-ending, checkout-immutability, and hosted Linux cases.

## Related ADRs

`ADR-HUP-001` selects version-independent succession assessment over the
hard-coded, deleted, and permanent compatibility-view alternatives.
