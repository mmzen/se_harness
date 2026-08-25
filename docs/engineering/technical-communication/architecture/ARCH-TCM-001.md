+++
id = "ARCH-TCM-001"
type = "architecture"
title = "Managed communication authority with non-authoritative skill consumers"
status = "approved"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
addresses = ["REQ-TCM-001", "REQ-TCM-002", "REQ-TCM-003", "REQ-TCM-004"]
conforms_to = ["SPEC-TCM-001"]

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "public-interface-or-protocol", "cross-cutting-policy", "material-alternatives"]
rationale = "The proposal adds one managed cross-cutting policy, a public installed path and portable skill contract, and a durable dependency direction between authority, communication profiles, skills, and runtime prose. Material alternatives place the rules in skills, prompts, adapters, or the managed router. An ADR is required before this architecture can be approved."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T07:53:59Z"
decided_by = "technical-owner"
+++

# Architecture: Managed communication authority with non-authoritative skill consumers

## Context and scope

Technical communication affects ordinary agent responses and multiple current
or future outcome skills. The rules must be discoverable and integrity-protected,
but they must not become a second source of lifecycle or artifact authority.
The first concrete consumer is a read-only operator-brief skill. Technical
artifact authoring consumes the same policy selectively.

This architecture defines ownership, dependency, distribution, protection, and
failure boundaries. `SPEC-TCM-001` owns exact profile and skill behavior. Existing
agentic-execution architecture continues to own portable skill identity,
released-evaluator use, receipts, and the rule that skills are non-authoritative.
Existing instruction architecture continues to own the thin gate, managed
router, focused policy modules, and managed installation model.

## Components and responsibilities

### Managed communication policy

`TECHNICAL_COMMUNICATION.md` owns:

- permitted ASD-STE100-based claim and no-download rule;
- policy precedence and eligible-prose boundary;
- operator and technical-artifact profiles;
- exact and semantic protected-content classes;
- deviation and human-decision rules; and
- concise examples and counterexamples.

It is a focused managed policy module. It does not own lifecycle legality,
decision rights, quality gates, artifact relations, or substantive definitions.

### Managed router

`ENGINEERING_HARNESS.md` owns one concise route to the policy for eligible
operator-facing and artifact prose. It keeps global authority invariants and
canonical restitution rules. It does not copy the communication policy body.

### Portable operator-brief skill

`harness-operator-brief` owns one explicit read-only procedure that:

- validates its closed contract and portable-core identity;
- checks target evaluator identity and installed integrity;
- consumes one bounded source and protected-content declaration;
- applies `operator-communication` to eligible prose;
- verifies protected bindings; and
- returns one inline result and receipt with zero changed paths.

Its instructions and helper are execution inputs, not policy authority.

### Protected-content guard

The portable deterministic helper owns structural input bounds, source and span
digests, span ordering and overlap rejection, protected output binding, and
zero-change evidence. It does not decide semantic equivalence, grammar quality,
truth, accountable authority, or ASD-STE100 compliance.

### Ordinary agent and artifact skills

Supported agents follow the router and use the policy while composing eligible
prose. Current and future artifact-authoring skills reference the managed policy
instead of copying it. They retain their own outcome, activation, mutation,
scope, and evidence contracts.

### Installer and integrity plane

The standard template, package metadata, installer, lock, doctor, upgrade,
preflight policy-path set, and package tests distribute and protect the policy
and skill transactionally. Candidate source does not overwrite the self-hosting
root copy bound to the installed released evaluator.

### Evidence and human decision plane

Results, receipts, fixtures, test reports, and review evidence show profile
selection and preservation. Humans decide substantive meaning, new project
terms, policy approval, artifact approval, and all existing accountable actions.
No new per-sentence approval role is introduced.

## Dependency direction

```text
formal artifacts + machine contracts + managed harness policy
                              |
                              v
         managed TECHNICAL_COMMUNICATION.md policy
                              |
             +----------------+----------------+
             |                                 |
             v                                 v
 ordinary eligible agent prose       portable outcome skills
             |                                 |
             +----------------+----------------+
                              v
                 protected-content guard
                              |
                              v
                inline result and receipt
                              |
                              v
              existing accountable decision point
```

Each lower layer may consume and report higher-layer facts. It cannot redefine
or weaken them. The communication policy cannot reinterpret formal authority,
and a skill cannot redefine the communication policy.

## Data and control flow

1. The managed agent gate routes the actor through `ENGINEERING_HARNESS.md`.
2. The router identifies the focused communication policy for eligible prose.
3. The task or explicit skill identifies output purpose and protected content.
4. Exact evaluator identity and managed integrity are checked when a portable
   skill claims a policy-governed result.
5. The applicable profile is selected before prose is composed.
6. The agent writes only eligible prose and preserves higher-precedence content.
7. For `harness-operator-brief`, the helper compares source and output bindings
   and confirms zero changed paths.
8. The result records profile, source identity, deviations, and uncertainty.
9. If an accountable decision is current, the existing harness procedure supplies
   it. Communication adds no decision and no second next action.

## Trust boundaries

- Managed policy bytes are trusted only after lock and evaluator identity checks.
- The external standard is not a runtime trust dependency and is not retrieved.
- Source text, structured results, protected-span declarations, project terms,
  repository content, and model output are untrusted input.
- Exact evaluator results remain authoritative only for their defined machine
  semantics; the communication layer cannot reinterpret them.
- Skill prose and helper code are integrity-protected execution inputs but not
  product or policy authority.
- Runtime permissions are technical capability, not permission to write.
- Human review is required for meaning-sensitive decisions; it is not replaced
  by a clarity score or language-model confidence.

## Required patterns

- One focused managed policy owner and reference-only consumers.
- Thin route from the managed harness router.
- Explicit profile name and bounded scope.
- Protected-content classification before transformation.
- Exact UTF-8 byte identity and lowercase SHA-256 for exact spans.
- Closed skill contract and deterministic portable-core manifest.
- Explicit-only activation for the first skill.
- Read-only mutation class, zero changed paths, and inline-only evidence.
- Fail-closed handling of missing policy, ambiguity, and preservation mismatch.
- Representative human semantic review in addition to deterministic tests.

## Prohibited patterns

- Putting the only policy copy in `SKILL.md`, `AGENTS.md`, a runtime prompt, an
  adapter, or an explanatory note.
- Downloading, scraping, bundling, or parsing ASD-STE100 during execution.
- Claiming compliance, certification, approval, or endorsement.
- Treating readability, dictionary, or AI output as proof of correctness.
- Automatically rewriting approved or repository-wide artifacts for style.
- Rewriting canonical blocks, code, evidence, identifiers, or machine data.
- Letting a skill or profile change scope, lifecycle state, authority, or an
  external system.
- Introducing an open plug-in registry for arbitrary communication policies in
  the first increment.

## Quality attributes

- **Authority clarity:** every rule has one owner and communication grants no
  decision right.
- **Precision:** exact protected spans have zero byte changes; semantic review
  finds no critical meaning change.
- **Portability:** the policy and skill core are provider-neutral and require no
  network or hosted service.
- **Determinism:** identical source, protected declarations, policy, and explicit
  inputs produce the same structural validation and binding evidence.
- **Safety:** missing or ambiguous inputs stop before a completed claim.
- **Auditability:** result and receipt bind policy, profile, skill, source,
  evaluator, preservation, deviations, and zero changed paths.
- **Usability:** operators can identify the current outcome and decision without
  interpreting avoidable prose complexity.
- **Compatibility:** current skill contracts, managed policy modules, owner
  content, and approved artifacts remain unchanged.

## Conformance checks

- Verify one canonical and one installed managed policy path with matching lock
  identity and safe installation/upgrade behavior.
- Verify the router names the policy and no consumer duplicates its normative body.
- Parse the new closed v2 skill contract and reject altered activation, mutation,
  effects, inputs, outputs, or non-match cases.
- Compare all existing skill bytes and manifest digests to their baseline.
- Exercise protected source classes, malformed spans, overlap, digest mismatch,
  canonical blocks, normative text, code, structured data, logs, and quotations.
- Assert zero repository, Git, lifecycle, network, credential, and external effects.
- Review representative operator and formal-artifact prose for meaning and action
  comprehension without using readability as the pass authority.
- Inspect package contents and offline installed behavior.

## Related ADRs

`ADR-TCM-001` proposes one managed focused policy consumed by non-authoritative
skills and ordinary agent routes. The ADR remains draft and must be accepted or
revised by the technical owner before this architecture can be approved.
