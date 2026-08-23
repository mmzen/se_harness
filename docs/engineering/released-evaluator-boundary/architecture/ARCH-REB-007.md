+++
id = "ARCH-REB-007"
type = "architecture"
title = "Contract-driven dual-runtime governance migration boundary"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]
addresses = ["REQ-REB-016", "REQ-REB-017"]
conforms_to = ["SPEC-REB-008"]

[decision_assessment]
outcome = "adr_required"
triggers = ["system-boundary", "responsibility-or-dependency-direction", "public-interface-or-protocol", "security-privacy-or-trust-boundary", "concurrency-consistency-reliability-or-failure-strategy", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "The proposal adds a versioned public rehearsal contract, coordinates two isolated evaluator runtimes and disposable governance state, defines a new cross-cutting authority oracle and failure strategy, and must choose between checklist, component-test, candidate-authority, and contract-driven approaches. These controlled triggers require the explicit decision in ADR-REB-007."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T07:56:21Z"
decided_by = "technical-owner"
+++

# Architecture: Contract-driven dual-runtime governance migration boundary

## Context and scope

Normal product release and later root adoption cross two software versions with different roles. The predecessor remains the installed authority, while the successor must prove that its new schemas and behavior work. The 0.6.0 incident showed that testing each implementation component separately does not prove the handover.

This architecture introduces one unprivileged migration runner around existing preparation, validation, assessment, publication planning, rendering, and upgrade components. It owns stage ordering, role isolation, authority assertions, disposable state, and canonical evidence. It does not own lifecycle policy, release decisions, production compatibility-view implementation, publication, or operational adoption.

## Components and responsibilities

- **Packaged migration contract:** owns the closed schemas, stage catalog, role catalog, identity requirements, allowed effects, and result shape.
- **Scenario loader and classifier:** validates canonical scenario bytes, compares predecessor capabilities with successor needs, and binds all fixture and adapter identities.
- **Runtime resolver:** proves exact predecessor and successor environments outside the target checkout and returns immutable execution handles labeled by role.
- **Stage drivers:** adapt existing preparation, complete validation, assessment, release/publication planning, rendering, and upgrade functions to one typed local interface.
- **Authority oracle:** compares declared decision fixtures, evaluator roles, before/after snapshots, and observed effects; it rejects authority inference or role substitution.
- **Disposable repository manager:** creates one isolated fixture, provides exact complete and declared compatibility views, snapshots allowed state, and cleans only its own directory.
- **Canonical result recorder:** writes stage results and stable digests, including bounded failure evidence.
- **Candidate CI integration:** runs hermetic Windows/Linux scenarios and an exact historical 0.5.0-to-candidate integration lane without credentials or privileged actions.

## Dependency direction

```text
packaged contract + immutable scenario
                |
                v
        migration runner ------> canonical factual result
          |          |
          |          +----> authority oracle + snapshots
          |
          +----> external released predecessor
          +----> external successor candidate
          +----> disposable stage drivers and views

accountable decision fixtures ---> expected effects only
human owners --------------------> real decisions outside the runner
```

The predecessor and successor never import one another. Candidate code cannot supply the predecessor's expected identity, and a decision fixture cannot be generated from a stage result.

## Data and control flow

1. Validate canonical contract/scenario bytes and resolve every referenced digest.
2. Snapshot the clean operational source and Git refs.
3. Resolve isolated predecessor and successor identities outside the checkout.
4. Create a disposable fixture and execute the closed stage graph in order.
5. Before and after each stage, the authority oracle compares selected evaluator, graph, lifecycle facts, view, filesystem, and simulated external state with the declared effect set.
6. On first failure, mark later stages not run, retain a bounded failure result, clean disposable resources, and recheck operational state.
7. On success, reconcile the final disposable root, repeat operational immutability checks, canonicalize the result, and expose it for independent verification.

## Trust boundaries

- Contract/scenario bytes, fixture content, paths, Git data, evaluator packages, Python interpreters, adapter reports, decision fixtures, and process environment are untrusted.
- Exact released distribution and payload evidence establishes predecessor identity; exact commit/tree or non-promotable package evidence establishes successor identity but no authority.
- The operational checkout and external services are observation-only and outside disposable mutation scope.
- Accountable human authority is outside the process and is represented only as immutable attributed test input.

## Required patterns

- One versioned contract and one closed stage graph.
- Two separately resolved external runtime environments.
- Typed evaluator roles and target-view identities at every invocation.
- Exact view/adaptor binding and honest separation of complete and compatible claims.
- Snapshot-based allowed-effect checks around every stage.
- Fail-stop execution with bounded evidence and no fallback path.
- A separately modeled adoption stage after simulated immutable publication.

## Prohibited patterns

- Candidate-as-root execution, candidate-supplied predecessor identity, or shared import environments.
- Free-form shell orchestration, executable selection by path alone, ignored exit codes, accepted-error text, or caller-selected omissions.
- Automatic lifecycle, assurance, release, publication, deployment, or adoption decisions.
- Operational Git, lock, history, release, package, maintenance, Pages, or credential mutation.
- Rewriting completed historical scenarios to accommodate a new successor.

## Quality attributes

- **Integrity:** exact identities, contract digests, stage reports, and snapshots make substitutions visible.
- **Security:** isolation and zero credentials prevent candidate authority and privileged side effects.
- **Auditability:** one canonical report explains who observed what, against which view, and with which allowed effect.
- **Reliability:** closed order and fail-stop behavior prevent partial success from being promoted.
- **Portability:** host-normalized reports and Windows/Linux lanes expose platform boundaries before release.
- **Evolvability:** versioned scenarios and contracts support future N-1-to-N changes without modifying history.

## Conformance checks

Execute `VER-REB-007`. Trace both requirements through the contract schema, runtime isolation, all typed stage drivers, authority oracle, canonical result, package data, candidate workflow, and exact 0.5.0-to-0.6.0-style regression. Prove no operational or external mutation in positive and negative cases.

## Related ADRs

`ADR-REB-007` selects a contract-driven dual-runtime rehearsal rather than a checklist, disconnected component tests, diagnostic waiver, or temporary candidate authority.
