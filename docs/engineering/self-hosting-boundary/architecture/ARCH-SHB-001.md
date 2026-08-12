+++
id = "ARCH-SHB-001"
type = "architecture"
title = "Isolated governor, candidate-source, and candidate-package planes"
status = "implemented"
owners = ["technical-owner", "engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
addresses = ["REQ-SHB-001", "REQ-SHB-002", "REQ-SHB-003", "REQ-SHB-004", "REQ-SHB-005", "REQ-SHB-006"]
conforms_to = ["SPEC-SHB-001"]

[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "Separating the governor from candidate source changes the self-hosting trust boundary, managed-state ownership, CI protocol, release recovery, and post-release lifecycle; the alternatives have materially different independence and migration consequences."
assessed_by = "technical-owner"
+++

# Architecture: Isolated governor, candidate-source, and candidate-package planes

## Context

The repository currently has three logical identities but one effective filesystem and import context. Candidate self-upgrade changes the host state, released `doctor` evaluates candidate files as if they belonged to its distribution, and Python current-directory resolution can substitute source for an installed baseline. Naming two CI jobs does not create a trust boundary.

## Components

- **Governor descriptor:** immutable version, URL, filename, digest, and prior-governor provenance independent of candidate metadata.
- **Governor environment:** isolated released installation outside the checkout.
- **Governor target state:** operational router, policies, scripts, configuration, and lock created by the governor outside the checkout.
- **Candidate source plane:** checkout source, canonical templates, tests, and repository-local derived evidence.
- **Candidate package plane:** exact built artifacts and a fresh isolated installation.
- **Acceptance targets:** disposable new, adopted, and upgrade repositories outside the checkout.
- **Identity attestor:** deterministic role/version/origin/path assertions used before each lane.
- **CI orchestrator:** composes three non-substitutable gates without importing one plane into another.
- **Governor promotion workflow:** separately adopts an already-published candidate for the next cycle.

## Dependency and trust direction

```text
published governor wheel ---> governor environment ---> host governance checks
                                      |                         |
                                      | read-only compatible    | authority remains
                                      v                         v
candidate checkout ------------> candidate-source evidence   formal artifacts + humans
        |
        v
exact candidate artifacts ---> candidate environment ---> disposable acceptance targets
        |
        v
published immutable release ---> separate governor-promotion change
```

The governor never depends on candidate imports. Candidate package acceptance depends on the exact candidate commit, not the governance commit containing its VREC or RLS. Candidate evidence can support accountable review but cannot grant authority.

## State invariants

1. `external governor target == released governor distribution and governor lock`.
2. `candidate checkout == candidate source`, except its two hash-locked repository-specific self-hosting controls.
3. `candidate acceptance state == candidate canonical distribution and candidate package`.
4. Governor and candidate versions may intentionally differ during development.
5. A process has one role and one resolved harness origin.
6. No required lane writes into another plane.
7. VREC/RLS candidate identity is full-commit exact and immutable.

## Control flow

1. Resolve and verify the governor descriptor.
2. Create the governor environment outside the checkout and attest identity.
3. Prove governor same-version integrity against a governor-created target.
4. Execute bounded backward-compatible checkout checks read-only.
5. Attest candidate-source identity and run the complete candidate suite.
6. Export the candidate commit, build artifacts, attest candidate-package identity, and test disposable targets.
7. Capture verification only after one clean final candidate exists.
8. Stop promotion if the candidate changes.
9. After immutable publication, use a separate work order to promote that artifact to host governor.

## Security boundaries

- Repository files, artifact metadata, environment variables, path strings, workflow inputs, and package archives are untrusted.
- Path identity uses resolved, component-aware containment and rejects ambiguity.
- Identity diagnostics are allowlisted and never dump credentials or environment contents.
- Exact artifact hashes precede installation.
- Governor and candidate environments have no shared editable package state.
- Checkout mutation is denied in independent and package lanes.

## Migration architecture

The first transition records the mixed-state baseline, corrects CI and import isolation under an approved work order, establishes separated state invariants, and requalifies a new candidate. Historical candidate, VREC, and RLS facts remain unchanged. Future development begins only after a published version is separately promoted to governor.

## Quality attributes

Independent assurance, provenance clarity, deterministic execution, reproducible packaging, low bootstrap ambiguity, transactional migration, auditability, compatibility transparency, and standard-library Python 3.11+ runtime behavior.

## Related decision

`ADR-SHB-001` selects the three-plane boundary and deferred governor promotion over continuous candidate self-upgrade.
