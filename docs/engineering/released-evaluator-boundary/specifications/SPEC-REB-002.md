+++
id = "SPEC-REB-002"
type = "specification"
title = "Evaluator upgrade separation and bounded recovery"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner", "release-owner"]
created = "2026-08-21"
updated = "2026-08-27"

[relations]
specifies = ["REQ-REB-005", "REQ-REB-006", "REQ-REB-007"]
+++

# Specification: Evaluator upgrade separation and bounded recovery

## Scope

This contract defines the operator-visible policy and evidence for separate evaluator upgrades, deterministic observations of conflicting draft release chains, and a maintainer-only governance-deadlock recovery runbook with disposable rehearsal.

## Actors and external systems

- Repository, engineering, assurance, security, and release owners.
- `harnessctl inspect` and the existing validator/Explorer snapshot.
- Disposable Git repositories and local fake publication boundaries.
- GitHub OIDC Trusted Publishing and PyPI only during a separately authorized real recovery.

## Inputs

- Approved or draft work-order scopes and typed relations.
- Artifact types, lifecycle statuses, versions, commits, work-order coverage, release gates, and supersession relations.
- Standard root configuration, lock, managed workflows, candidate workflow, and publication workflow.
- Exact candidate commit, distribution digest, and external evaluator identity during an authorized recovery.

## Outputs

- Reviewable evaluator-upgrade evidence distinct from product release evidence.
- Deterministic non-authoritative conflict observations and closed-catalog suggestions.
- A maintainer recovery runbook with stop conditions, decision rights, technical procedure, restoration checklist, and evidence checklist.
- A no-credential disposable rehearsal report.

## State model

Evaluator adoption follows:

```text
published target -> draft upgrade packet -> approved upgrade work
-> reviewed plan -> authorized apply -> implemented candidate
-> commit-bound assurance -> integrated standard root
```

Product release and evaluator adoption are distinct state machines. Publication of target N+1 is a prerequisite observation for adoption; it does not approve adoption. The prior root evaluator remains selected until the standard upgrade is integrated.

Recovery follows `not-invoked -> declared -> bounded bypass -> standard-root restored -> normal controls verified -> incident follow-up`. Rehearsal may simulate these states but cannot enter a real bypass or use production credentials.

## Behavioral rules

1. **Separate scope.** An evaluator-upgrade work order names prior and target versions/digests and excludes product code, candidate version changes, release records for the target package, and external publication.
2. **Explicit sequencing.** If product release and later adoption are related, their artifacts state the dependency: target publication completes first; a later upgrade packet selects it.
3. **Upgrade evidence.** Evidence retains old and new identities, exact plan, changed managed paths, transaction outcome, rollback observation, no-op replay, doctor, validation, inspection, dashboard, supported runtimes, and hosted checks.
4. **Conflict rule R1.** Report more than one `draft` or `ready` release record declaring the same version unless records are terminally rejected or one is an explicitly historical released fact.
5. **Conflict rule R2.** Report ready VRECs at different commits with intersecting work-order coverage when no valid `superseded_by` relation resolves the older ready record.
6. **Conflict rule R3.** Report active release contracts whose `gates` sets overlap and whose associated active release proposals compete for the same work and version where that relation is structurally available.
7. **Authority boundary.** Conflict observations name IDs and available commits/versions, use `automatic = false`, and never select, reject, supersede, delete, or mutate a chain.
8. **Runbook authority.** The runbook begins with the human declaration required to invoke it, identifies rights that remain unavailable, and distinguishes technical evidence from retrospective authorization.
9. **Runbook selection.** A real recovery selects one full immutable commit and one exact distribution, records hashes before build or acquisition, and stops on a mutable or ambiguous source.
10. **Credential boundary.** Production publication requires short-lived trusted identity, least permissions, protected-environment approval, and separate action-time authority. Long-lived tokens are prohibited.
11. **Public proof.** A bootstrap artifact is not used as evaluator until public bytes are acquired into a fresh external environment and version, archive digest, payload, origins, entry point, isolation, and checkout exclusion pass.
12. **Restoration.** Recovery is incomplete until the root uses the standard config and lock, normal released-evaluator and candidate-evidence workflows pass, the normal publisher is restored, temporary publication paths are absent, and active-surface invariants pass.
13. **Incident retention.** A factual non-authoritative RCA and separately governed preventive work follow recovery; emergency actions are not retroactively normalized.
14. **Disposable rehearsal.** Automated rehearsal uses local immutable archives, simulated trusted publication, disposable roots, and no production credentials, network mutation, tags, releases, or deployment.

## Amendment, 2026-08-27

Under `WO-REB-027`, on the repository owner's direction, rule 1 no longer
governs upgrades: the evaluator-upgrade work-order packet is retired and
`SPEC-REB-012` states the simple upgrade contract (identity by version and
installed-payload digest, no packet, index installs accepted). Rules 2 to 14
— sequencing, upgrade evidence, the conflict rules, the runbook, the
credential boundary, public proof, restoration, incident retention and the
disposable rehearsal — stand unchanged. Rule 1's text is retained above as
history of what the product enforced from 2026-08-21 to this amendment.

## Error and recovery behavior

- Mixed product-release/evaluator-upgrade scope stops at definition or preflight review and requires split work orders or explicit accountable sequencing.
- Unknown semantic relationships remain visible without guessed conflict classification.
- Any recovery stop condition leaves the last known standard authority unchanged where possible and records the exact incomplete restoration stage.
- A failed rehearsal reports stage-specific diagnostics and makes no operational repository change.

## Data and interface contracts

Conflict observations use the existing inspection finding/suggestion structure with a stable rule ID, source, affected artifact IDs, available commit/version fields, accountable role, action class, and `automatic = false`.

The runbook contains, in order: applicability; decision rights; prerequisites; immutable selection; isolated acquisition/build; credential boundary; public-install proof; bounded root transaction; restoration; verification; rollback; evidence retention; incident follow-up; and explicit prohibitions.

The rehearsal report identifies the fixture, exact input digests, simulated stages, resulting standard-root identity, restored workflow/invariant checks, forbidden external actions, and overall pass/fail result.

## Security and privacy properties

- The runbook never includes live credentials, user-specific paths, or bypass instructions detached from required human authority.
- Rehearsal cannot access production publishing environments.
- Conflict diagnostics expose formal IDs and repository facts only.
- Recovery downloads or simulated archives are verified before execution and never import candidate code into the evaluator environment.

## Performance and capacity

Conflict analysis is bounded by the already-loaded artifact graph and is at most quadratic only within the small active VREC/RLS/REL subsets. Disposable rehearsal completes within the existing full-suite CI budget.

## Observability

Inspection groups repeated conflict instances while JSON retains each instance. Recovery and rehearsal output stage-specific results and explicitly state that they do not authorize lifecycle or external action.

## Compatibility and migration

- Existing historical overlapping records are assessed under closed rules without state changes.
- The 0.5.0 RCA remains the factual incident record; the runbook links to it but does not modify it.
- Existing standard repository upgrade behavior is reused and extended rather than replaced by a recovery profile.
- Terminology in historical formal artifacts remains unchanged.

## Examples and counterexamples

- **Conforming:** publish N+1 under its release work, then later approve a root-only work order to adopt the public N+1 wheel.
- **Conforming:** report two overlapping ready VRECs and let the assurance owner decide remediation.
- **Non-conforming:** one work order changes candidate product code, publishes it, and immediately makes it the root evaluator.
- **Non-conforming:** recovery rehearsal uses real Trusted Publisher credentials or mutates the operational root.
- **Non-conforming:** inspection automatically marks an older draft rejected.

## Explicitly unspecified decisions

- Stable rule-ID suffixes and human rendering details.
- The disposable fixture's project name and temporary directory layout.
- The periodic rehearsal schedule after issue #81 closes; accountable repository policy sets that cadence.
